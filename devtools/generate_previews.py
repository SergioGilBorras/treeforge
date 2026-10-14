"""Regenerate README previews using the actual installed TreeForge rendering API.

This developer-only script is not part of the distributable wheel.
Run: python devtools/generate_previews.py
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from treeforge import TreeConfig, TreeForge  # noqa: E402

STRUCTURE = """treeforge/
├── src/
│   ├── core/
│   │   ├── parser.py
│   │   └── renderer.py
│   └── cli.py
├── assets/
│   ├── image_001.png
│   ├── image_002.png
│   └── image_003.png
├── data/
│   ├── report_001.json
│   ├── report_002.json
│   └── report_003.json
├── docs/
│   └── guide.md
├── tests/
│   └── test_core.py
└── README.md
"""


def main() -> int:
    output = ROOT / "docs" / "examples"
    output.mkdir(parents=True, exist_ok=True)
    for layout in ("vertical", "horizontal"):
        for boxes in (False, True):
            config = TreeConfig(
                max_depth=5, boxes=boxes, max_nodes=70,
                group_by=("prefix", "extension"), theme="light",
            )
            tree = TreeForge.from_text(STRUCTURE, config)
            target = output / (layout + ("-boxes" if boxes else "-plain") + ".svg")
            tree.render(target, engine="native", layout=layout)
            print(target.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
