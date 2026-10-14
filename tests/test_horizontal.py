from pathlib import Path
import xml.etree.ElementTree as ET
from treeforge import TreeForge, TreeConfig

TREE = """project/
├── src/
│   ├── alpha.py
│   └── beta.py
├── assets/
│   ├── photo_001.png
│   ├── photo_002.png
│   └── photo_003.png
└── README.md
"""

def test_horizontal_svg_alignment_and_boxes(tmp_path: Path):
    for align in ("left", "center"):
        tree = TreeForge.from_text(TREE, TreeConfig(align=align, boxes=True))
        path = tree.render(tmp_path / (align + ".svg"), layout="horizontal")
        data = path.read_text(encoding="utf-8")
        ET.fromstring(data)
        assert "<path" in data and "<rect" in data and "photo_*.png" in data

def test_horizontal_custom_icon(tmp_path: Path):
    icon_dir = tmp_path / "icons"
    icon_dir.mkdir()
    (icon_dir / "folder.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><rect width="10" height="10"/></svg>',
        encoding="utf-8",
    )
    tree = TreeForge.from_text(TREE, TreeConfig(icons_dir=str(icon_dir)))
    data = tree.render(tmp_path / "custom.svg", layout="horizontal").read_text(encoding="utf-8")
    assert "data:image/svg+xml;base64," in data
