from pathlib import Path
import pytest
from treeforge import TreeForge, TreeConfig
from treeforge.render import file_symbol

@pytest.mark.parametrize("extension,symbol", [
    ("docx", "📘"), ("xls", "📗"), ("xlsx", "📗"), ("pptx", "📙"),
    ("json", "🧩"), ("zip", "🗜️"), ("txt", "📃"), ("pdf", "📕"),
    ("md", "📝"), ("mp3", "🎵"), ("mp4", "🎬"), ("py", "🐍"),
])
def test_extension_icon(extension, symbol):
    tree = TreeForge.from_paths(["example." + extension])
    assert file_symbol(tree.root.children[0], TreeConfig()) == symbol

def test_default_icons_render_both_layouts(tmp_path: Path):
    tree = TreeForge.from_paths(["report.xlsx", "data.json", "archive.zip", "notes.txt"])
    for layout in ("vertical", "horizontal"):
        svg = tree.render(tmp_path / (layout + ".svg"), layout=layout).read_text(encoding="utf-8")
        for glyph in ("📗", "🧩", "🗜️", "📃"):
            assert glyph in svg
        assert "data:image/svg+xml;base64," not in svg
