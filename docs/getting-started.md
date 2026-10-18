# Getting started

TreeForge is a Python library and command-line tool for generating directory-structure diagrams. It requires Python 3.10 or later.

## Install TreeForge

Install the published v0.1.0 release directly from GitHub:

```bash
python -m pip install git+https://github.com/SergioGilBorras/treeforge.git@v0.1.0
```

To work from a local clone, run `python -m pip install .` in the repository root instead. Git must be installed for the GitHub-based command.

## Render a directory

```bash
treeforge render . --max-depth 3 --output tree.svg
treeforge render . --layout horizontal --boxes --output horizontal.svg
```

The default is a vertical SVG diagram without boxes, using file-type Unicode icons.

## Render an AI-generated tree

Save the following as `structure.txt`:

```text
project/
├── src/
│   ├── main.py
│   └── utils.py
└── README.md
```

Then render it:

```bash
treeforge render structure.txt --input-format tree --output structure.svg
```

## Python API

```python
from treeforge import TreeForge, TreeConfig

config = TreeConfig(max_depth=3, boxes=False, theme="light")
tree = TreeForge.from_directory(".", config)
tree.render("project.svg", layout="vertical")

text_tree = TreeForge.from_text("project/\n├── src/\n│   └── app.py\n└── README.md")
text_tree.render("diagram.svg")

paths_tree = TreeForge.from_paths(["src/main.py", "docs/guide.md"])
paths_tree.render("paths.svg")
```

See [configuration](configuration.md), [rendering formats](rendering.md) and the [diagram gallery](examples/README.md).
