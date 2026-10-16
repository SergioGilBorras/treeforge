"""Regression checks for readable spacing between boxed SVG nodes."""
from pathlib import Path
import xml.etree.ElementTree as ET

from treeforge import TreeConfig, TreeForge

TEXT = """project/
├── src/
│   ├── a.py
│   └── b.py
├── docs/
│   ├── one.md
│   └── two.md
└── README.md
"""


def test_box_spacing(tmp_path: Path):
    for layout in ("vertical", "horizontal"):
        output = TreeForge.from_text(TEXT, TreeConfig(boxes=True)).render(
            tmp_path / (layout + ".svg"), layout=layout
        )
        svg = ET.parse(output).getroot()
        boxes = [node for node in svg.iter()
                 if node.tag.endswith("rect") and node.get("rx")]
        assert len(boxes) >= 6
        assert all(float(box.get("height", "0")) <= 32 for box in boxes)
        # Within a depth column, row boxes must not visually overlap.
        for index, left in enumerate(boxes):
            x, y = float(left.get("x")), float(left.get("y"))
            w, h = float(left.get("width")), float(left.get("height"))
            for right in boxes[index + 1:]:
                rx, ry = float(right.get("x")), float(right.get("y"))
                rw, rh = float(right.get("width")), float(right.get("height"))
                assert not (x < rx + rw and rx < x + w and
                            y < ry + rh and ry < y + h)
