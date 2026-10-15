# TreeForge

**Beautiful directory diagrams in Python.**

Generate polished project structure diagrams from a real directory, a list of paths or text produced by an AI.

![Default connected vertical tree](examples/vertical-plain.svg)

## Explore the project

- [Quick start](getting-started.md)
- [Four visual layouts](examples/README.md)
- [SVG icon customization](icons.md)
- [CLI and rendering options](rendering.md)
- [Supported file types](file-types.md)
- [Recommended diagram sizes](size-guidance.md)

## Installation

```bash
git clone https://github.com/SergioGilBorras/treeforge.git
cd treeforge
python -m pip install .
treeforge render . --max-depth 3 --output tree.svg
```

The package is under active development. Use the feature branch or the reviewed default branch when available.
