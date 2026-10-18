# Developer tools

These utilities run from a source checkout and are separate from the installable TreeForge package.

- `python devtools/run_validation.py`: run end-to-end checks and generate `validation-output/report.json` and `validation-output/index.html`.
- `python devtools/generate_previews.py`: regenerate the eight SVG diagrams for default/custom icons and vertical/horizontal layouts, with and without boxes.
- `python devtools/check_distribution.py`: after `python -m build`, install the wheel in a temporary virtual environment and test SVG and TXT export.
- `python devtools/measure_scale.py`: estimate rendered diagram dimensions for sample workloads.

See the [developer validation guide](../docs/developer-validation.md) and [release quality checklist](../docs/release-checklist.md).
