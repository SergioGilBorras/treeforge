# Getting started

TreeForge requires Python 3.10 or later.

## Install from the repository

```bash
python -m pip install .
```

## Render a real directory

```bash
treeforge render ./project --output tree.svg
treeforge render ./project --layout horizontal --boxes --output horizontal.svg
```

By default, TreeForge generates a **vertical SVG without boxes**.

## Render a text tree

Create a file called `structure.txt`:

```text
project/
├── src/
│   ├── main.py
│   └── utils.py
└── README.md
```

```bash
treeforge render structure.txt --input-format tree --output structure.svg
```

## Python API

```python
from treeforge import TreeForge, TreeConfig

config = TreeConfig(max_depth=3, boxes=False, theme="light")
tree = TreeForge.from_directory("./project", config)
tree.render("project.svg", layout="vertical")

from_text = TreeForge.from_text("project/\n├── src/\n│   └── app.py\n└── README.md")
from_text.render("diagram.svg")
```

For path-list input, use `TreeForge.from_paths(["src/main.py", "docs/guide.md"])`.

See [configuration](configuration.md) and [rendering](rendering.md) for other options.
