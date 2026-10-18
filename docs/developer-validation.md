# Developer validation suite

The standalone script `devtools/run_validation.py` is **kept outside the installable TreeForge package** and is **not included in the wheel**. It imports the working source via `src/` for development only.

```bash
python devtools/run_validation.py
python devtools/run_validation.py --output /tmp/treeforge-validation
python devtools/run_validation.py --strict-graphviz
```

It creates an isolated temporary directory tree and checks equivalence with an AI-style text tree and a path list. It validates grouping, exclusions, depth and node limits, Unicode/CLI, optional Graphviz, SVG icon overrides, rejection of embedded SVG scripts, all native orientation/theme/box/alignment combinations, and TXT/Mermaid/DOT exporters.

It writes `validation-output/report.json` (machine-readable pass/fail/skip) and `validation-output/index.html` (visual gallery of generated SVG). Artifacts are intentionally excluded from Git, while the suite is executed by CI on Linux, macOS and Windows. Nonzero exit indicates a failed validation. Graphviz is skipped if `dot` is absent unless `--strict-graphviz` is passed.

Run `python -m pytest -q` for unit and regression tests. The integration suite checks end-to-end behavior and creates a visual HTML gallery.
