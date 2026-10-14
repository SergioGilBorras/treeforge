"""Core tree model, readers and conservative grouping."""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from pathlib import Path
from collections import defaultdict
import fnmatch
import json
import re

DEFAULT_GROUPS = {
    "images": (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp"),
    "documents": (".md", ".rst", ".txt", ".pdf"),
    "data": (".json", ".yaml", ".yml", ".csv", ".xml"),
    "spreadsheets": (".xls", ".xlsx", ".xlsm", ".ods"),
    "presentations": (".ppt", ".pptx", ".odp"),
    "archives": (".zip", ".tar", ".gz", ".7z", ".rar"),
    "audio": (".mp3", ".wav", ".flac"),
    "video": (".mp4", ".mov", ".mkv"),
}
DEFAULT_EXCLUDES = (".git", ".venv", "__pycache__", "node_modules", ".mypy_cache", ".pytest_cache")
DEFAULT_PRESERVE = ("README.md", "pyproject.toml", "Dockerfile", "main.py")

@dataclass
class Node:
    name: str
    directory: bool = True
    children: list[Node] = field(default_factory=list)
    members: list[str] = field(default_factory=list)
    category: str = ""
    hidden: int = 0

@dataclass
class TreeConfig:
    max_depth: int = 4
    max_nodes: int = 100
    group_by: tuple[str, ...] = ("extension", "prefix")
    min_group: int = 3
    category_groups: dict[str, tuple[str, ...]] = field(
        default_factory=lambda: dict(DEFAULT_GROUPS)
    )
    exclude: tuple[str, ...] = DEFAULT_EXCLUDES
    preserve: tuple[str, ...] = DEFAULT_PRESERVE
    theme: str = "light"
    icons_dir: str | None = None
    boxes: bool = False
    align: str = "left"
    colors: dict[str, str] = field(default_factory=dict)
    show_counts: bool = True

    def __post_init__(self) -> None:
        if self.max_depth < 0 or self.max_nodes < 1 or self.min_group < 2:
            raise ValueError("Invalid max_depth, max_nodes or min_group")
        if self.align not in ("left", "center"):
            raise ValueError("align must be 'left' or 'center'")

    @classmethod
    def from_json(cls, path: str | Path) -> TreeConfig:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(**data)

def _categorized(name: str, groups: dict[str, tuple[str, ...]]) -> str:
    suffix = Path(name).suffix.lower()
    for category, extensions in groups.items():
        if suffix in extensions:
            return category
    return suffix.lstrip(".") or "file"

def _from_paths(paths: list[str], name: str = "project") -> Node:
    root = Node(name)
    for raw in paths:
        value = raw.strip().replace("\\", "/").strip("/")
        if not value or value == ".":
            continue
        if value.startswith("../") or "/../" in value or value == "..":
            raise ValueError("Parent traversals are not valid tree paths")
        parts = [part for part in value.split("/") if part and part != "."]
        node = root
        for i, part in enumerate(parts):
            last = i == len(parts) - 1
            directory = (not last) or raw.rstrip().endswith(("/", "\\"))
            child = next((c for c in node.children if c.name == part), None)
            if child is None:
                child = Node(part, directory=directory)
                node.children.append(child)
            elif not directory and child.directory and not child.children:
                child.directory = False
            node = child
    return root

def _parse_text(text: str) -> Node:
    lines = [s.rstrip() for s in text.splitlines() if s.strip()]
    if not lines:
        raise ValueError("Empty tree input")
    if all(not any(c in s for c in "├└│") for s in lines):
        lines = [s for s in lines if not s.lstrip().startswith(" ```")]
        # An indented tree and a simple path-list are both supported.
        if any("/" in s.strip().rstrip("/") for s in lines[1:]) and all(
            not s.startswith("  ") for s in lines[1:]
        ):
            return _from_paths(lines[1:], lines[0].strip().strip("/") or "project")
    root = Node(lines[0].strip().rstrip("/"))
    stack: list[tuple[int, Node]] = [(-1, root)]
    for raw in lines[1:]:
        # Standard tree output uses four-column indentation and branch markers.
        match = re.match(r"^([ │]*)(?:├── |└── |\|-- |\\-- )(.*)$", raw)
        if match:
            level = len(match.group(1)) // 4
            value = match.group(2).strip()
        else:
            indent = len(raw) - len(raw.lstrip(" "))
            level = indent // 2
            value = raw.strip()
        if not value:
            continue
        while len(stack) > 1 and stack[-1][0] >= level:
            stack.pop()
        parent = stack[-1][1]
        node = Node(value.rstrip("/"), directory=value.endswith("/"))
        parent.children.append(node)
        stack.append((level, node))
    # Nodes with children are always directories.
    def normalize(node: Node) -> None:
        if node.children:
            node.directory = True
        for child in node.children:
            normalize(child)
    normalize(root)
    return root

def _scan(path: Path, exclude: tuple[str, ...]) -> Node:
    if not path.is_dir():
        raise NotADirectoryError(str(path))
    root = Node(path.name or str(path))
    def descend(node: Node, current: Path) -> None:
        try:
            entries = sorted(current.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except PermissionError:
            node.hidden += 1
            return
        for item in entries:
            if any(fnmatch.fnmatch(item.name, pattern) for pattern in exclude):
                continue
            if item.is_symlink():
                node.children.append(Node(item.name + " ↗", directory=False))
            elif item.is_dir():
                child = Node(item.name, directory=True)
                node.children.append(child)
                descend(child, item)
            elif item.is_file():
                node.children.append(Node(item.name, directory=False))
    descend(root, path)
    return root

def _simplify(root: Node, config: TreeConfig) -> Node:
    """Simplify without mutating the source tree; groups retain source members."""
    budget = [config.max_nodes]
    def visit(node: Node, depth: int) -> Node:
        result = replace(node, children=[], members=list(node.members))
        if depth >= config.max_depth:
            result.hidden += count_descendants(node)
            return result
        if budget[0] <= 1:
            result.hidden += count_descendants(node)
            return result
        grouped = _group(node.children, config)
        for child in grouped:
            if budget[0] <= 1:
                result.hidden += 1 + count_descendants(child)
                continue
            budget[0] -= 1
            result.children.append(visit(child, depth + 1))
        return result
    return visit(root, 0)

def count_descendants(node: Node) -> int:
    return sum(1 + count_descendants(ch) for ch in node.children)

def _group(children: list[Node], config: TreeConfig) -> list[Node]:
    files = [c for c in children if not c.directory and not c.members]
    preserve = lambda name: any(fnmatch.fnmatch(name, pattern) for pattern in config.preserve)
    used: set[str] = set()
    groups: list[Node] = []
    if "prefix" in config.group_by:
        buckets: dict[tuple[str, str], list[Node]] = defaultdict(list)
        for item in files:
            # Conservative pattern: a repeated stem ending in separator and numeric token.
            match = re.match(r"^(.*?[_-])([0-9]{2,})(\.[^.]+)$", item.name)
            if match and not preserve(item.name):
                buckets[(match.group(1), match.group(3))].append(item)
        for (prefix, suffix), items in sorted(buckets.items()):
            if len(items) >= config.min_group:
                names = sorted(i.name for i in items)
                groups.append(Node(prefix + "*" + suffix, False, members=names,
                                   category=_categorized(names[0], config.category_groups)))
                used.update(names)
    if "extension" in config.group_by:
        buckets2: dict[str, list[Node]] = defaultdict(list)
        for item in files:
            if item.name not in used and not preserve(item.name):
                buckets2[_categorized(item.name, config.category_groups)].append(item)
        for category, items in sorted(buckets2.items()):
            if len(items) >= config.min_group:
                names = sorted(i.name for i in items)
                groups.append(Node(category.title() + f" ({len(items)} files)", False,
                                   members=names, category=category))
                used.update(names)
    remainder = [c for c in children if c.directory or c.members or c.name not in used]
    return sorted(remainder, key=lambda n: (not n.directory, n.name.lower())) + groups

class TreeForge:
    def __init__(self, root: Node, config: TreeConfig | None = None):
        self.root = root
        self.config = config or TreeConfig()

    @classmethod
    def from_directory(cls, path: str | Path, config: TreeConfig | None = None) -> TreeForge:
        config = config or TreeConfig()
        return cls(_scan(Path(path), config.exclude), config)

    @classmethod
    def from_text(cls, text: str, config: TreeConfig | None = None) -> TreeForge:
        return cls(_parse_text(text), config)

    @classmethod
    def from_paths(cls, paths: list[str], name: str = "project",
                   config: TreeConfig | None = None) -> TreeForge:
        return cls(_from_paths(paths, name), config)

    def simplified(self) -> Node:
        return _simplify(self.root, self.config)

    def render(self, output: str | Path, engine: str = "auto",
               layout: str = "vertical") -> Path:
        from .render import render
        return render(self.simplified(), Path(output), self.config, engine, layout)
