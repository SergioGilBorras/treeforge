# Roadmap

## v0.1 — Foundation

- [x] Installable Python package and CLI
- [x] Real-directory reader and text-tree parser
- [x] Depth and node budgets
- [x] Conservative grouping by numeric prefix and extension/category
- [x] Classical native TXT/SVG vertical layout
- [x] Mermaid and Graphviz exporters
- [x] Default Unicode icons and palette configuration
- [ ] Full custom SVG icon directory support
- [ ] Precise horizontal left/center alignment
- [ ] More robust parser diagnostics and edge cases

## v0.2 — Visual system

- Bundled redistributable SVG icon pack and explicit override map.
- Custom icons directory resolving `folder.svg`, `python.svg`, `image.svg`, etc.
- SVG image embedding with secure validation, deterministic behavior and fallbacks.
- Consistent boxes, connector styles and themes across all renderers.
- Automated visual snapshots.

## v0.3 — Production readiness

- Gitignore support, Unicode/parser edge cases, stress testing.
- Interactive HTML output and group inspection.
- Cross-platform CI, wheel/sdist verification and versioned documentation.
- Stable API and publishing workflow.
