from pathlib import Path
import pytest
from treeforge import TreeForge, TreeConfig
from treeforge.render import file_symbol

@pytest.mark.parametrize("extension,symbol", [
    ("docx", "📘"), ("xls", "📗"), ("xlsx", "📗"), ("pptx", "📙"),
    ("json", "🧩"), ("zip", "🗜️"), ("txt", "📃"), ("pdf", "📕"),
    ("md", "📝"), ("mp3", "🎵"), ("mp4", "🎬"), ("py", "🐍"),
])
def test_icon_for_extension(extension, symbol):
    tree = TreeForge.from_paths([f"file.{extension}"])
    assert file_symbol(tree.root.children[0], TreeConfig()) == symbol

def test_render_icons_both_orientations(tmp_path: Path):
    tree = TreeForge.from_paths(["report.xlsx", "data.json", "archive.zip", "notes.txt"])
    for layout in ("vertical", "horizontal"):
        result = tree.render(tmp_path / f"{layout}.svg", layout=layout).read_text(encoding="utf-8")
        assert "data:image/svg+xml;base64," in result
        assert "data.json" in result
        assert "archive.zip" in result
        assert "notes.txt" in result
