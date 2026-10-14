# TreeForge

**Beautiful project structure diagrams, from directories or AI-generated text.**

TreeForge is a Python CLI and library that reads real directories or textual folder trees, simplifies them with conservative grouping, and exports classical vertical directory trees or horizontal diagrams.

> **Status:** initial development release (v0.1.0). The package has not yet been published on PyPI.

## Features

- Inputs: real filesystem, textual tree, or path list.
- Vertical **classic directory tree** in TXT or native SVG (optional colored background boxes).
- Horizontal diagrams with **Graphviz** (DOT, SVG, PNG, PDF) or **Mermaid** (MMD).
- Configurable depth, node budget, themes, and extension/category grouping.
- Custom palette by file type (via `TreeConfig.colors`).
- No runtime Python dependencies for native TXT/SVG/Mermaid/DOT output.
- Python >= 3.10.

## Installation

From a checkout:

```bash
python -m pip install .
# or build a wheel:
python -m pip install build
python -m build
python -m pip install dist/*.whl
```

To render Graphviz SVG/PNG/PDF, install the system's Graphviz `dot` executable.

## Quick start

```bash
treeforge render . --layout vertical --output structure.svg --max-depth 3
treeforge render . --layout vertical --output structure.txt
treeforge render . --layout horizontal --output structure.mmd
treeforge render . --layout horizontal --engine graphviz --output structure.svg
treeforge render tree.txt --input-format tree --layout vertical --boxes --output example.svg
```

### Python API

```python
from treeforge import TreeForge, TreeConfig

config = TreeConfig(
    max_depth=3,
    group_by=("prefix", "extension"),
    boxes=True,
    colors={"folder": "#3366aa", "py": "#4b9e61", "background": "#ffffff"},
)
tree = TreeForge.from_directory(".", config)
tree.render("structure.svg", layout="vertical")
tree.render("structure.mmd", layout="horizontal")
```

### Text input

```text
my-project/
├── src/
│   ├── main.py
│   └── helper.py
└── README.md
```

## Design and documentation

See [Getting started](docs/getting-started.md), [Rendering and layouts](docs/rendering.md), [Configuration](docs/configuration.md), and [Roadmap](docs/roadmap.md).

**Notes on layout:** Mermaid's flowchart layout does not reproduce the exact classic connector tree; use native SVG/TXT for that. In horizontal mode Graphviz offers more geometry control; `align` currently changes spacing, not a strict bounding-box anchor.

**Custom icons:** the `icons_dir` parameter is reserved for external icon packs and is documented as an upcoming feature. Built-in Unicode symbols are currently used for vertical SVG/TXT. The project will add its own bundled SVG pack and icon overrides as the next iteration.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
python -m build
```

## License

MIT — see [LICENSE](LICENSE).
