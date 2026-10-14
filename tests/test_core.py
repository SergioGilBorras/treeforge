from pathlib import Path
import pytest
from treeforge import TreeForge, TreeConfig
from treeforge.core import count_descendants

TREE = """project/
├── assets/
│   ├── img_001.png
│   ├── img_002.png
│   └── img_003.png
└── README.md
"""

def test_parse_and_group():
    tree = TreeForge.from_text(TREE, TreeConfig(min_group=3, max_depth=5))
    root = tree.simplified()
    assert root.name == "project"
    asset = root.children[0]
    assert asset.name == "assets"
    assert len(asset.children) == 1
    assert asset.children[0].name == "img_*.png"
    assert len(asset.children[0].members) == 3

def test_depth():
    tree = TreeForge.from_text(TREE, TreeConfig(max_depth=1))
    root = tree.simplified()
    assert root.children[0].hidden == 3

def test_render(tmp_path: Path):
    tree = TreeForge.from_text(TREE)
    for name, layout in [("tree.svg", "vertical"), ("tree.txt", "vertical"),
                          ("tree.dot", "horizontal"), ("tree.mmd", "horizontal")]:
        output = tree.render(tmp_path / name, layout=layout)
        assert output.exists() and output.stat().st_size > 0
    assert "└──" in (tmp_path / "tree.txt").read_text()
    assert "flowchart LR" in (tmp_path / "tree.mmd").read_text()

def test_invalid():
    with pytest.raises(ValueError):
        TreeConfig(max_depth=-1)

def test_directory(tmp_path: Path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("pass")
    root = TreeForge.from_directory(tmp_path).simplified()
    assert root.children[0].children[0].name == "main.py"
