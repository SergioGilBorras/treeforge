"""Command-line interface."""
from __future__ import annotations
import argparse
from pathlib import Path
from .core import TreeForge, TreeConfig

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="treeforge", description="Create beautiful directory trees.")
    sub = parser.add_subparsers(dest="command", required=True)
    render = sub.add_parser("render", help="Render a directory or a text tree")
    render.add_argument("source", help="Directory or text-file path")
    render.add_argument("-o", "--output", default="tree.svg")
    render.add_argument("--input-format", choices=("auto", "directory", "tree"), default="auto")
    render.add_argument("--layout", choices=("vertical", "horizontal"), default="vertical")
    render.add_argument("--align", choices=("left", "center"), default="left")
    render.add_argument("--engine", choices=("auto", "native", "graphviz", "mermaid"), default="auto")
    render.add_argument("--max-depth", type=int, default=4)
    render.add_argument("--max-nodes", type=int, default=100)
    render.add_argument("--group-by", default="extension,prefix")
    render.add_argument("--theme", choices=("light", "dark"), default="light")
    render.add_argument("--boxes", action="store_true")
    render.add_argument("--icons-dir")
    render.add_argument("--config", help="JSON or YAML configuration file")
    args = parser.parse_args(argv)
    config = (TreeConfig.from_yaml(args.config) if Path(args.config).suffix.lower() in (".yaml", ".yml")
              else TreeConfig.from_json(args.config)) if args.config else TreeConfig(
        max_depth=args.max_depth, max_nodes=args.max_nodes, group_by=tuple(
            v.strip() for v in args.group_by.split(",") if v.strip()
        ), theme=args.theme, boxes=args.boxes, align=args.align, icons_dir=args.icons_dir)
    source = Path(args.source)
    tree = (TreeForge.from_directory(source, config)
            if args.input_format == "directory" or (args.input_format == "auto" and source.is_dir())
            else TreeForge.from_text(source.read_text(encoding="utf-8"), config))
    target = tree.render(args.output, engine=args.engine, layout=args.layout)
    print(target)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
