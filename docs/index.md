# TreeForge

**Beautiful directory diagrams in Python.**

Generate polished project structure diagrams from a real directory, a list of paths or text produced by an AI.

## Default appearance

TreeForge uses recognizable file-type icons by default, including folders, images, Office documents, JSON, archives, text, audio and video. The **vertical tree without boxes** is the default layout.

![Vertical directory tree with default icons](examples/vertical-plain.svg)

See [the gallery](examples/README.md) for horizontal layouts, optional boxes, and equivalent diagrams using custom SVG icons.

## Explore TreeForge

- [Getting started](getting-started.md)
- [Gallery: default vs custom icons](examples/README.md)
- [Customizing icons](icons.md)
- [Layouts and formats](rendering.md)
- [Supported file types](file-types.md)
- [Configuration](configuration.md)
- [Printing and size guidance](size-guidance.md)

## Installation

```bash
python -m pip install .
treeforge render . --max-depth 3 --output tree.svg
```
