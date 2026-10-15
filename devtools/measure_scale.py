#!/usr/bin/env python3
"""Estimate physical heights of representative diagrams; developer-only."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from treeforge import TreeForge, TreeConfig  # noqa: E402


def main() -> int:
    # A deliberately large flat tree; the renderer is not modified to fit it.
    paths = [f"src/module_{i:03d}/file_{i:03d}.py" for i in range(150)]
    with tempfile.TemporaryDirectory() as temp:
        for boxes in (False, True):
            config = TreeConfig(boxes=boxes, max_depth=3, max_nodes=400,
                                group_by=())
            tree = TreeForge.from_paths(paths, name="large-sample", config=config)
            output = Path(temp) / ("boxed.svg" if boxes else "plain.svg")
            tree.render(output, layout="vertical")
            root = ET.parse(output).getroot()
            height_px = float(root.attrib["height"])
            size_cm = height_px * 2.54 / 96
            print(f"boxes={boxes}: {height_px:.0f} px, approx {size_cm:.1f} cm at 96 dpi")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
