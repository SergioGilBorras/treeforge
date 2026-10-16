"""SVG geometry regression checks for the classic tree layout."""
import xml.etree.ElementTree as ET
from pathlib import Path

from treeforge import TreeConfig, TreeForge

TREE = """project/
├── src/
│   ├── main.py
│   └── utils.py
├── docs/
│   └── README.md
└── pyproject.toml
"""


def test_connected_trunks_and_arms(tmp_path: Path):
    for boxes in (False, True):
        out = TreeForge.from_text(TREE, TreeConfig(boxes=boxes)).render(
            tmp_path / f"v-{boxes}.svg", layout="vertical"
        )
        root = ET.parse(out).getroot()
        paths = [e for e in root.iter() if e.tag.endswith("path")]
        trunks = [e for e in paths if e.get("data-tree-edge") == "trunk"]
        arms = [e for e in paths if e.get("data-tree-edge") == "arm"]
        assert len(trunks) == 3
        assert len(arms) == 6
        assert all(" V " in e.get("d", "") for e in trunks)
        assert all(" H " in e.get("d", "") for e in arms)
        assert "├──" not in out.read_text(encoding="utf-8")
        rects = [e for e in root.iter() if e.get("data-tree-node") == "box"]
        assert bool(rects) == boxes


def test_graphic_and_text_are_separate(tmp_path: Path):
    tree = TreeForge.from_text(TREE)
    svg = tree.render(tmp_path / "tree.svg").read_text(encoding="utf-8")
    txt = tree.render(tmp_path / "tree.txt").read_text(encoding="utf-8")
    assert 'data-tree-edge="trunk"' in svg
    assert "├──" in txt
