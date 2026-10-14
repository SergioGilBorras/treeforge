"""TreeForge rendering: tree-shaped text/SVG and Mermaid/Graphviz diagrams."""
from __future__ import annotations

from pathlib import Path
import html
import json
import re
import shutil
import base64
import xml.etree.ElementTree as ET
import subprocess
from .core import Node, TreeConfig, _categorized

DEFAULT_PALETTE = {
    "foreground": "#243247", "background": "#ffffff", "line": "#a3b3c7",
    "folder": "#376aab", "images": "#a855a0", "documents": "#39865f",
    "data": "#d1872c", "spreadsheets": "#268a70", "file": "#68788c",
}
DARK_PALETTE = {
    "foreground": "#e4eaf4", "background": "#161d2b", "line": "#65748b",
    "folder": "#83b6ff", "images": "#ed99e3", "documents": "#89d9a9",
    "data": "#f0bf76", "spreadsheets": "#8ae0ca", "file": "#b4c3d5",
}
DEFAULT_SYMBOLS = {
    "folder": "📁", "images": "🖼️", "documents": "📝", "data": "🧩",
    "spreadsheets": "📊", "py": "🐍", "file": "📄",
}
def palette(config: TreeConfig) -> dict[str, str]:
    result = dict(DARK_PALETTE if config.theme == "dark" else DEFAULT_PALETTE)
    result.update(config.colors)
    for color in result.values():
        if not re.fullmatch(r"#[a-fA-F0-9]{6}", color):
            raise ValueError("Colors must use six-digit hex notation, e.g. #aabbcc")
    return result

def category(node: Node, config: TreeConfig) -> str:
    return "folder" if node.directory else (node.category or _categorized(node.name, config.category_groups))

def walk_lines(root: Node):
    yield "", root
    def visit(node: Node, prefix: str):
        entries = list(node.children)
        for i, child in enumerate(entries):
            last = i == len(entries) - 1 and node.hidden == 0
            branch = "└── " if last else "├── "
            yield prefix + branch, child
            if child.children:
                yield from visit(child, prefix + ("    " if last else "│   "))
        if node.hidden:
            yield prefix + "└── ", Node(f"… {node.hidden} hidden", False)
    yield from visit(root, "")

def tree_text(root: Node, config: TreeConfig) -> str:
    symbols = DEFAULT_SYMBOLS
    rows = []
    for prefix, node in walk_lines(root):
        typ = category(node, config)
        symbol = symbols.get(typ, symbols["file"])
        count = f" [{len(node.members)}]" if node.members and config.show_counts else ""
        rows.append(f"{prefix}{symbol} {node.name}{'/' if node.directory else ''}{count}")
    return "\n".join(rows) + "\n"

def custom_icon(node: Node, config: TreeConfig) -> str | None:
    """Return a safely embedded SVG data URI for a custom icon."""
    if not config.icons_dir:
        return None
    kind = category(node, config)
    suffix = Path(node.name).suffix.lstrip(".").lower()
    candidates = ([suffix] if suffix else []) + [kind, "folder" if node.directory else "file"]
    directory = Path(config.icons_dir).expanduser()
    for candidate in candidates:
        if not re.fullmatch(r"[a-z0-9_-]+", candidate):
            continue
        icon = directory / (candidate + ".svg")
        if not icon.is_file() or icon.stat().st_size > 65536:
            continue
        content = icon.read_bytes()
        try:
            root = ET.fromstring(content)
            forbidden = {"script", "foreignObject", "image", "animate", "set"}
            if any(element.tag.split("}")[-1] in forbidden or any(
                key.lower().startswith("on") or
                key.split("}")[-1].lower() in ("href", "style")
                for key in element.attrib
            ) for element in root.iter()):
                continue
        except (ET.ParseError, UnicodeError):
            continue
        if root.tag.split("}")[-1] != "svg":
            continue
        return "data:image/svg+xml;base64," + base64.b64encode(content).decode("ascii")
    return None


def svg_vertical(root: Node, config: TreeConfig) -> str:
    from .vertical import svg_vertical as native_vertical
    return native_vertical(root, config)
    colors = palette(config)
    rows = list(walk_lines(root))
    line_h = 29
    font_size = 15
    longest = max(len(prefix + node.name) for prefix, node in rows)
    width = max(480, 80 + longest * 10)
    height = 28 + len(rows) * line_h
    output = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="100%" height="100%" fill="{colors["background"]}"/>']
    for i, (prefix, node) in enumerate(rows):
        y = 32 + i * line_h
        typ = category(node, config)
        color = colors.get("." + Path(node.name).suffix.lower().lstrip("."),
                          colors.get(typ, colors["file"]))
        label = node.name + ("/" if node.directory else "")
        if node.members and config.show_counts:
            label += f" [{len(node.members)}]"
        x = 20 + len(prefix) * 8.5
        if config.boxes:
            output.append(f'<rect x="{x-5}" y="{y-19}" width="{max(100,len(label)*9.0+40)}" height="25" rx="6" fill="{color}" opacity="0.12"/>')
        output.append(f'<text x="20" y="{y}" font-family="monospace" font-size="{font_size}" fill="{colors["line"]}">{html.escape(prefix)}</text>')
        icon = DEFAULT_SYMBOLS.get(typ, DEFAULT_SYMBOLS["file"])
        icon_uri = custom_icon(node, config)
        if icon_uri:
            output.append(f'<image x="{x}" y="{y-17}" width="19" height="19" href="{icon_uri}"/>')
        else:
            output.append(f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{font_size}">{html.escape(icon)}</text>')
        output.append(f'<text x="{x+26}" y="{y}" font-family="monospace" font-size="{font_size}" fill="{color}">{html.escape(label)}</text>')
    output.append("</svg>")
    return "\n".join(output)

def _node_list(root: Node):
    result = []
    def visit(node: Node, parent: int | None):
        idx = len(result)
        result.append((idx, parent, node))
        for child in node.children:
            visit(child, idx)
        if node.hidden:
            n = len(result)
            result.append((n, idx, Node(f"… {node.hidden} hidden", False)))
    visit(root, None)
    return result

def to_mermaid(root: Node, config: TreeConfig, layout: str) -> str:
    direction = "LR" if layout == "horizontal" else "TB"
    lines = ["flowchart " + direction]
    for idx, parent, node in _node_list(root):
        kind = category(node, config)
        name = DEFAULT_SYMBOLS.get(kind, DEFAULT_SYMBOLS["file"]) + " " + node.name + ("/" if node.directory else "")
        if node.members and config.show_counts:
            name += f" ({len(node.members)})"
        if config.boxes:
            lines.append(f'    n{idx}["{_escape_mermaid(name)}"]')
        else:
            lines.append(f'    n{idx}("{_escape_mermaid(name)}")')
        if parent is not None:
            lines.append(f"    n{parent} --> n{idx}")
    for idx, _, node in _node_list(root):
        typ = category(node, config)
        color = palette(config).get(typ, palette(config)["file"])
        lines.append(f"    style n{idx} color:{color}")
    return "\n".join(lines) + "\n"

def _escape_mermaid(text: str) -> str:
    return html.escape(text, quote=True).replace("#", "#35;")

def to_dot(root: Node, config: TreeConfig, layout: str) -> str:
    p = palette(config)
    lines = ["digraph TreeForge {", '  graph [bgcolor="' + p["background"] + '", pad="0.25"];',
             '  rankdir=LR;' if layout == "horizontal" else '  rankdir=TB;',
             '  node [fontname="DejaVu Sans", fontsize=12];',
             '  edge [color="' + p["line"] + '", arrowhead=none];']
    if config.align == "center":
        lines.append("  graph [ranksep=0.8, nodesep=0.45];")
    else:
        lines.append("  graph [ranksep=0.55, nodesep=0.25];")
    for idx, parent, node in _node_list(root):
        typ = category(node, config)
        color = p.get(typ, p["file"])
        name = node.name + ("/" if node.directory else "")
        if node.members and config.show_counts:
            name += f" ({len(node.members)})"
        shape = "box" if config.boxes else "plain"
        label = json.dumps(name, ensure_ascii=False)
        lines.append(f'  n{idx} [label={label}, shape={shape}, fontcolor="{color}", color="{color}", style="rounded"];')
        if parent is not None:
            lines.append(f"  n{parent} -> n{idx};")
    lines.append("}")
    return "\n".join(lines) + "\n"

def render(root: Node, path: Path, config: TreeConfig, engine: str, layout: str) -> Path:
    if layout not in ("vertical", "horizontal"):
        raise ValueError("layout must be vertical or horizontal")
    path.parent.mkdir(parents=True, exist_ok=True)
    suffix = path.suffix.lower()
    if engine == "auto":
        engine = "mermaid" if suffix == ".mmd" else "graphviz" if suffix in (".dot", ".png", ".pdf") else "native"
    if suffix == ".txt":
        content = tree_text(root, config)
    elif suffix == ".mmd":
        content = to_mermaid(root, config, layout)
    elif suffix == ".dot":
        content = to_dot(root, config, layout)
    elif suffix == ".svg" and layout == "vertical" and engine == "native":
        content = svg_vertical(root, config)
    elif suffix == ".svg" and layout == "horizontal" and engine == "native":
        from .horizontal import svg_horizontal
        content = svg_horizontal(root, config)
    elif suffix in (".svg", ".png", ".pdf") and engine == "graphviz":
        if not shutil.which("dot"):
            raise RuntimeError("Graphviz 'dot' executable not found. Install Graphviz or use vertical native SVG.")
        completed = subprocess.run(["dot", "-T" + suffix[1:]], input=to_dot(root, config, layout),
                                   text=True, stdout=subprocess.PIPE if suffix == ".svg" else subprocess.DEVNULL,
                                   stderr=subprocess.PIPE, check=False) if suffix == ".svg" else None
        if suffix == ".svg":
            if completed.returncode:
                raise RuntimeError(completed.stderr)
            content = completed.stdout
        else:
            source = path.with_suffix(".dot")
            source.write_text(to_dot(root, config, layout), encoding="utf-8")
            try:
                subprocess.run(["dot", "-T" + suffix[1:], str(source), "-o", str(path)],
                               check=True, capture_output=True, text=True)
            finally:
                source.unlink(missing_ok=True)
            return path
    else:
        raise ValueError("Unsupported combination of format, engine and layout")
    path.write_text(content, encoding="utf-8")
    return path
