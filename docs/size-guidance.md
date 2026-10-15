# Page sizes and diagram readability

TreeForge is primarily a tool for **small, curated directory structures**. The default vertical SVG assigns each visible node one row. With boxes, rows are taller.

At a nominal CSS rendering scale of 96 pixels per inch:

| Vertical layout | Row pitch | Approximate node rows in 25 cm |
| --- | ---: | ---: |
| Plain (default) | 34 px = 0.90 cm | 27 |
| Boxed | 44 px = 1.16 cm | 21 |

These counts are **approximate design guidance**, not limits enforced by the software. SVG graphics can be resized, but text and icons become harder to read when a large tree is scaled down for an A4 page (29.7 cm high, allowing 25 cm for the diagram after margins). Headers and footers further reduce the available space.

For an A4 document, start with `--max-depth 2` and `--max-nodes 20`, then check the exported diagram. A 30–50-row tree is often better displayed in an online document or broken into smaller diagrams.

Horizontal diagrams depend on leaf count, column width and long names, so there is no useful universal page-size threshold.

The development-only `devtools/measure_scale.py` prints row-count and physical-size estimates for sample workloads without changing the rendering algorithms.
