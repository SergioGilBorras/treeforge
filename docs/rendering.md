# Rendering and layouts

| Layout | Format | Engine | Notes |
|---|---|---|---|
| vertical | .txt | native | Standard tree connectors |
| vertical | .svg | native | Standard tree connectors, colors and optional background boxes |
| horizontal | .svg | native | Orthogonal connectors, actual left/center alignment, SVG icons |\n| horizontal | .dot | Graphviz source | No external executable needed |
| horizontal | .mmd | Mermaid source | Renders as a flowchart |
| horizontal | .svg/.png/.pdf | Graphviz | Requires system `dot` |
| vertical | .mmd | Mermaid | Top-down flowchart, **not** the classic tree |

Native SVG is the recommended default for vertical layouts. Graphviz is the recommended renderer for horizontal layouts.

```bash
treeforge render . -o tree.svg --layout vertical --boxes
treeforge render . -o tree.svg --layout horizontal --align center\ntreeforge render . -o tree.dot --layout horizontal --align center
treeforge render . -o tree.mmd --layout horizontal
```

Native horizontal SVG honors `align=left` or `align=center` for canvas positioning. Graphviz's `align` still adjusts spacing rather than anchoring. The native SVG layout computes a column for each depth and centers parents above their descendants.
