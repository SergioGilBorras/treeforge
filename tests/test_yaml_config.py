from pathlib import Path
import pytest
from treeforge import TreeConfig

def test_yaml(tmp_path: Path):
    pytest.importorskip("yaml")
    path = tmp_path / "settings.yaml"
    path.write_text("max_depth: 2\nboxes: true\n", encoding="utf-8")
    config = TreeConfig.from_yaml(path)
    assert config.max_depth == 2 and config.boxes
