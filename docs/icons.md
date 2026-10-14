# Icons and customization

TreeForge selects Unicode symbols by file type and uses them as fallbacks in native SVG and TXT output. For native vertical and horizontal SVG, custom SVG icon files can be provided through `--icons-dir`.

```bash
treeforge render . --icons-dir ./icons --output tree.svg
treeforge render . --icons-dir ./icons --layout horizontal --output horizontal.svg
```

Python API: `TreeConfig(icons_dir="./icons")`.

## Icon lookup

TreeForge looks in the supplied directory in this order:

1. File extension, e.g. `py.svg` or `json.svg`.
2. Category, e.g. `images.svg`, `documents.svg`, `data.svg`.
3. General fallback: `folder.svg` or `file.svg`.

Example SVG assets are available in [icons/](../icons/). Custom SVG assets must be self-contained, no larger than 64 KiB, and must not include scripts, external references or embedded images.

Mermaid diagrams use file-type Unicode symbols within labels. Graphviz uses styled labels; native SVG supports embedded custom icons.

## Future directions

A configurable icon-name mapping, a complete distributable SVG collection and additional renderer-specific icon integration are planned.
