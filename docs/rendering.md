# Layouts and rendering

The default is a **vertical tree without boxes**, using connected SVG paths for branches. Use `--layout horizontal` for a left-to-right tree; add `--boxes` for slim node borders with extra spacing.

| Layout | Output | Renderer |
| --- | --- | --- |
| Vertical (default) | SVG | Native, connected geometric branches |
| Horizontal | SVG | Native, orthogonal connectors and left/center alignment |
| Vertical | TXT | Conventional Unicode tree characters |
| Either | MMD | Mermaid flowchart source |
| Either | DOT | Graphviz source |
| Either | SVG/PNG/PDF | Graphviz, when `--engine graphviz` is selected for SVG or when the extension is PNG/PDF; requires system `dot` |

```bash
treeforge render . --output vertical.svg
treeforge render . --layout vertical --boxes --output vertical-boxes.svg
treeforge render . --layout horizontal --align left --output horizontal.svg
treeforge render . --layout horizontal --align center --boxes --output horizontal-boxes.svg
treeforge render . --layout horizontal --output graph.mmd
treeforge render . --layout horizontal --output graph.dot
treeforge render . --layout horizontal --engine graphviz --output graph.pdf
```

Boxed native SVG diagrams use smaller, lighter borders and increased node separation. Vertical TXT retains text connectors; native SVG draws them geometrically.

The Graphviz engine does not use native SVG custom icons. See the [generated comparison gallery](examples/README.md).
