from pathlib import Path
from treeforge import TreeForge, TreeConfig

def test_custom_icon(tmp_path: Path):
    icons = tmp_path / "icons"
    icons.mkdir()
    (icons / "folder.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><rect width="12" height="12"/></svg>',
        encoding="utf-8",
    )
    tree = TreeForge.from_paths(["src/main.py"], config=TreeConfig(icons_dir=str(icons)))
    output = tree.render(tmp_path / "tree.svg")
    assert "data:image/svg+xml;base64," in output.read_text(encoding="utf-8")

def test_reject_script_icon(tmp_path: Path):
    icons = tmp_path / "icons"
    icons.mkdir()
    (icons / "folder.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>',
        encoding="utf-8",
    )
    tree = TreeForge.from_paths(["src/main.py"], config=TreeConfig(icons_dir=str(icons)))
    output = tree.render(tmp_path / "tree.svg")
    assert "data:image/svg+xml;base64," in output.read_text(encoding="utf-8")
