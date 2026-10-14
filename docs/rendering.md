# Rendering and layouts

| Layout | Format | Engine | Notes |
|---|---|---|---|
| vertical | .txt | native | Standard tree connectors |
| vertical | .svg | native | Standard tree connectors, colors and optional background boxes |
| horizontal | .dot | Graphviz source | No external executable needed |
| horizontal | .mmd | Mermaid source | Renders as a flowchart |
| horizontal | .svg/.png/.pdf | Graphviz | Requires system `dot` |
| vertical | .mmd | Mermaid | Top-down flowchart, **not** the classic tree |

Native SVG is the recommended default for vertical layouts. Graphviz is the recommended renderer for horizontal layouts.

```bash
treeforge render . -o tree.svg --layout vertical --boxes
treeforge render . -o tree.dot --layout horizontal --align center
treeforge render . -o tree.mmd --layout horizontal
```

The horizontal `align` option adjusts layout spacing. Strict left/center canvas anchoring is planned.
