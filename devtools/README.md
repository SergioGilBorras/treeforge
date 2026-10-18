# Developer tools

These scripts operate on the source checkout. They are **development utilities**, separate from the installable Python package.

- `python devtools/run_validation.py`: exercise filesystem and text inputs, CLI, transformations and renderers. Results are written to `validation-output/report.json` and `validation-output/index.html`.
- `python devtools/generate_previews.py`: regenerate eight documentation SVG images (default/custom icons, vertical/horizontal, plain/boxed) from the same input tree.

See [developer validation](../docs/developer-validation.md).

- `python devtools/check_distribution.py`: install the built wheel in a temporary environment and verify native rendering and text export.
