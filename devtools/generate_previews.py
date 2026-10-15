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
├── office/
│   ├── budget.xlsx
│   ├── proposal.docx
│   └── slides.pptx
├── media/
│   ├── soundtrack.mp3
│   └── video.mp4
├── archives/
│   └── backup.zip
├── data/
│   ├── notes.txt
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
            for icon_style in ("default", "custom"):
                config = TreeConfig(
                    max_depth=5, boxes=boxes, max_nodes=70,
                    group_by=("prefix", "extension"), theme="light",
                    icons_dir=str(ROOT / "icons") if icon_style == "custom" else None,
                )
                tree = TreeForge.from_text(STRUCTURE, config)
                suffix = "-boxes" if boxes else "-plain"
                # Four historical URLs always show default icons.
                name = layout + suffix + ("" if icon_style == "default" else "-custom") + ".svg"
                target = output / name
                tree.render(target, engine="native", layout=layout)
                print(target.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
