# Developer tools

These scripts operate on the source checkout. They are **development utilities**, separate from the installable Python package.

- `python devtools/run_validation.py`: exercise filesystem and text inputs, CLI, transformations and renderers. Results are written to `validation-output/report.json` and `validation-output/index.html`.
- `python devtools/generate_previews.py`: regenerate four documentation SVG images from the same input tree.

See [developer validation](../docs/developer-validation.md).
