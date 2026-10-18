# Release checklist

TreeForge is distributed as a Python package under the MIT license. Release preparation is separate from publishing.

## Technical checks

1. Confirm the desired version is identical in `pyproject.toml` and `src/treeforge/__init__.py`.
2. Confirm Linux, macOS and Windows CI jobs are green.
3. Build the wheel and source distribution: `python -m build`.
4. Validate package metadata: `python -m twine check dist/*`.
5. Install and smoke-test the wheel in a new virtual environment: `python devtools/check_distribution.py`.
6. Confirm the default icon SVG gallery and the custom icon gallery display as intended.
7. Check the published GitHub Pages documentation and package links.
8. Confirm that GitHub Release artifacts and source installation instructions are ready.

## Release publication

Once the checks have passed, finalize the changelog, create a version tag and prepare a GitHub release. The release workflow builds downloadable Python distribution artifacts for GitHub. TreeForge is distributed from its GitHub repository and GitHub Releases.

## Supported scope

The library targets concise diagrams of directory structures. See [page size guidance](size-guidance.md) for printed output. Additional capabilities are listed in the [roadmap](roadmap.md).
