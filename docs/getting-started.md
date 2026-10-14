# Getting started

Requires Python 3.10+.

```bash
pip install -e ".[dev]"
treeforge render . -o tree.svg --max-depth 2
```

Supported source forms: a real directory, a text file containing a conventional `tree` listing, or path-list input through `TreeForge.from_paths(["src/main.py", "docs/guide.md"])`.

```python
from treeforge import TreeForge

tree = TreeForge.from_text("""project/
├── src/
│   ├── main.py
│   └── utils.py
└── README.md
""")
tree.render("overview.svg")
```

The source tree remains intact in memory; grouping and truncation are computed on a separate simplified tree.
\nFor visual and integration regression checks, run `python devtools/run_validation.py` and open `validation-output/index.html`.\n