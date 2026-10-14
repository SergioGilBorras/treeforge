# Contributing to TreeForge

TreeForge is developed in Python 3.10+.

## Local environment

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python devtools/run_validation.py
python devtools/generate_previews.py
python -m build
```

Before proposing visual changes, inspect the generated SVG gallery in `validation-output/index.html` and the four examples in `docs/examples/`.

Use pull requests with focused scope and tests. Keep user documentation focused on supported behavior; describe planned additions in `docs/roadmap.md` and release-to-release changes in `CHANGELOG.md`.
