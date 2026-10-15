#!/usr/bin/env python3
"""Developer-only integration/visual regression runner. Not included in the wheel.

Usage: python devtools/run_validation.py [--output validation-output] [--strict-graphviz]
"""
from __future__ import annotations

import argparse
import html
import json
import shutil
import subprocess
import sys
import tempfile
import traceback
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from treeforge import TreeConfig, TreeForge  # noqa: E402

TREE = """sample/
├── assets/
│   ├── frame_001.png
│   ├── frame_002.png
│   ├── frame_003.png
│   ├── image.jpg
│   └── logo.svg
├── data/
│   ├── records.json
│   ├── schema.json
│   └── settings.yaml
├── src/
│   ├── app.py
│   └── utils.py
├── tests/
│   ├── test_app.py
│   └── test_utils.py
└── README.md
"""
PATHS = [
    "assets/frame_001.png", "assets/frame_002.png", "assets/frame_003.png",
    "assets/image.jpg", "assets/logo.svg",
    "data/records.json", "data/schema.json", "data/settings.yaml",
    "src/app.py", "src/utils.py", "tests/test_app.py", "tests/test_utils.py",
    "README.md",
]


def create_fixture(path: Path) -> Path:
    folder = path / "sample"
    for name in PATHS:
        target = folder / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("fixture\n", encoding="utf-8")
    (folder / ".git").mkdir()
    (folder / ".git" / "config").write_text("ignored\n", encoding="utf-8")
    (folder / "__pycache__").mkdir()
    (folder / "__pycache__" / "cached.pyc").write_bytes(b"fake")
    return folder


def walk(node):
    yield node
    for child in node.children:
        yield from walk(child)


def check(condition: bool, explanation: str) -> None:
    if not condition:
        raise AssertionError(explanation)


def validate_svg(path: Path) -> None:
    root = ET.parse(path).getroot()
    check(root.tag.endswith("svg"), "Invalid SVG root")
    check(path.stat().st_size > 100, "Unusually small SVG")


def run_case(title: str, fn, results: list[dict]) -> None:
    try:
        fn()
        results.append({"name": title, "status": "pass"})
        print("PASS", title)
    except Exception as exc:
        results.append({"name": title, "status": "fail", "detail": str(exc)})
        print("FAIL", title, "-", exc)
        traceback.print_exc()


def run(output: Path, strict_graphviz: bool = False) -> int:
    output.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    gallery: list[tuple[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="treeforge-dev-") as workspace:
        directory = create_fixture(Path(workspace))
        sources = {
            "text": TreeForge.from_text(TREE),
            "filesystem": TreeForge.from_directory(directory),
            "paths": TreeForge.from_paths(PATHS, name="sample"),
        }
        def equivalence():
            def normalize(root):
                return sorted((n.name, n.directory) for n in walk(root))
            a, b, c = [normalize(obj.root) for obj in sources.values()]
            check(a == b == c, "Text, filesystem and path-list inputs disagree")
        run_case("source equivalence: text/directory/paths", equivalence, results)

        def exclusions():
            names = [x.name for x in walk(sources["filesystem"].root)]
            check(".git" not in names and "__pycache__" not in names, "Exclusions ignored")
        run_case("default excluded folders", exclusions, results)

        def grouping():
            root = TreeForge.from_directory(directory, TreeConfig(
                max_depth=5, group_by=("prefix", "extension"), min_group=3,
            )).simplified()
            members = [n for n in walk(root) if n.members]
            check(any(n.name == "frame_*.png" and len(n.members) == 3
                      for n in members), "Numeric prefix grouping failed")
            check(any(n.name == "README.md" for n in walk(root)), "README preservation failed")
        run_case("conservative grouping and preserved files", grouping, results)

        def pruning():
            root = TreeForge.from_directory(directory, TreeConfig(max_depth=1)).simplified()
            check(any(n.hidden > 0 for n in walk(root)), "Depth truncation did not record hidden files")
            root2 = TreeForge.from_directory(directory, TreeConfig(max_nodes=3)).simplified()
            check(sum(1 for _ in walk(root2)) <= 3, "Node count exceeded max_nodes")
        run_case("depth and node budgets", pruning, results)

        def invalid_config():
            try:
                TreeConfig(max_nodes=0)
            except ValueError:
                return
            raise AssertionError("Bad config accepted")
        run_case("invalid configuration", invalid_config, results)

        def safe_icons():
            icons = Path(workspace) / "icons"
            icons.mkdir()
            (icons / "folder.svg").write_text(
                '<svg xmlns="http://www.w3.org/2000/svg"><rect width="20" height="20"/></svg>',
                encoding="utf-8",
            )
            cfg = TreeConfig(icons_dir=str(icons))
            for orientation in ("vertical", "horizontal"):
                target = output / f"icons-{orientation}.svg"
                TreeForge.from_directory(directory, cfg).render(target, layout=orientation)
                check("data:image/svg+xml;base64," in target.read_text(encoding="utf-8"),
                      "Missing custom icon")
                validate_svg(target)
                gallery.append((f"Custom icons ({orientation})", target.name))
            (icons / "folder.svg").write_text(
                '<svg xmlns="http://www.w3.org/2000/svg"><script>evil()</script></svg>',
                encoding="utf-8",
            )
            target = output / "icons-rejected.svg"
            TreeForge.from_directory(directory, cfg).render(target)
            check("data:image/svg+xml;base64," not in target.read_text(encoding="utf-8"),
                  "Unsafe SVG was embedded")
        run_case("custom icons and unsafe-icon rejection", safe_icons, results)

        for origin, tree in sources.items():
            for orientation in ("vertical", "horizontal"):
                for boxes in (False, True):
                    for theme in ("light", "dark"):
                        for align in (("left", "center") if orientation == "horizontal" else ("left",)):
                            case = f"{origin}-{orientation}-{'boxed' if boxes else 'plain'}-{theme}-{align}"
                            def render_case(case=case, tree=tree, orientation=orientation,
                                            boxes=boxes, theme=theme, align=align):
                                config = TreeConfig(boxes=boxes, theme=theme, align=align)
                                current = TreeForge(tree.root, config)
                                svg = output / f"{case}.svg"
                                current.render(svg, layout=orientation)
                                validate_svg(svg)
                                gallery.append((case, svg.name))
                            run_case(case, render_case, results)
            def exporters(tree=tree, origin=origin):
                for ext, orientation in (("txt", "vertical"), ("dot", "horizontal"),
                                         ("mmd", "horizontal")):
                    target = output / f"{origin}.{ext}"
                    tree.render(target, layout=orientation)
                    content = target.read_text(encoding="utf-8")
                    check(bool(content.strip()), f"Empty {ext} output")
                    if ext == "txt":
                        check("├──" in content and "└──" in content, "Not a standard directory tree")
                    elif ext == "mmd":
                        check(content.startswith("flowchart LR"), "Invalid Mermaid header")
                    elif ext == "dot":
                        check(content.startswith("digraph"), "Invalid DOT header")
            run_case(f"{origin} exporters: txt/dot/mmd", exporters, results)

        def graphviz():
            if shutil.which("dot") is None:
                if strict_graphviz:
                    raise AssertionError("Graphviz executable 'dot' unavailable")
                results.append({"name": "Graphviz SVG external renderer", "status": "skip",
                                "detail": "dot not installed"})
                print("SKIP Graphviz SVG external renderer")
                return
            target = output / "graphviz-horizontal.svg"
            sources["filesystem"].render(target, engine="graphviz", layout="horizontal")
            validate_svg(target)
            gallery.append(("Graphviz SVG", target.name))
        run_case("optional Graphviz verification", graphviz, results)

        # Exercise the public CLI in an isolated subprocess, without pip installing the package.
        def cli():
            target = output / "cli-text.svg"
            env = dict(__import__("os").environ)
            env["PYTHONPATH"] = str(ROOT / "src")
            path = output / "input.tree"
            path.write_text(TREE, encoding="utf-8")
            cmd = [sys.executable, "-m", "treeforge", "render", str(path),
                   "--input-format", "tree", "--output", str(target)]
            completed = subprocess.run(cmd, capture_output=True, text=True, env=env)
            check(completed.returncode == 0, completed.stderr)
            validate_svg(target)
            gallery.append(("CLI from text", target.name))
        run_case("CLI subprocess (independent fixture)", cli, results)

    counts = {status: sum(c["status"] == status for c in results)
              for status in ("pass", "fail", "skip")}
    report = {"counts": counts, "cases": results}
    (output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = ["<!doctype html><html lang='en'><head><meta charset='utf-8'>",
            "<title>TreeForge validation gallery</title><style>",
            "body{font:15px system-ui;margin:32px;background:#f5f7fb;color:#263344}",
            "main{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:18px}",
            "article{background:white;border:1px solid #dce3ed;border-radius:12px;padding:18px}",
            "object{width:100%;min-height:130px;max-height:660px}",
            "</style></head><body><h1>TreeForge validation gallery</h1>",
            f"<p>Passed: {counts['pass']} | Failed: {counts['fail']} | Skipped: {counts['skip']}</p>",
            "<main>"]
    for title, file in gallery:
        rows.append(f"<article><h3>{html.escape(title)}</h3>"
                    f"<object type='image/svg+xml' data='{html.escape(file, quote=True)}'></object>"
                    f"<p><a href='{html.escape(file, quote=True)}'>Open SVG</a></p></article>")
    rows += ["</main></body></html>"]
    (output / "index.html").write_text("\n".join(rows), encoding="utf-8")
    print(f"\nResults: {counts} | output: {output}")
    return 1 if counts["fail"] else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "validation-output")
    parser.add_argument("--strict-graphviz", action="store_true")
    arguments = parser.parse_args()
    return run(arguments.output.resolve(), arguments.strict_graphviz)


if __name__ == "__main__":
    raise SystemExit(main())
