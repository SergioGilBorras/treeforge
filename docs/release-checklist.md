# Release quality checklist

TreeForge versions are distributed through GitHub Releases, with source installation supported directly from Git tags. The published release is [v0.1.0](https://github.com/SergioGilBorras/treeforge/releases/tag/v0.1.0).

For each new release:

1. Check that the version in `pyproject.toml` matches `src/treeforge/__init__.py`.
2. Confirm the automated tests pass across the supported Python versions and operating systems.
3. Run `python -m build` to create a wheel and source distribution.
4. Run `python -m twine check dist/*` to validate distribution metadata.
5. Run `python devtools/check_distribution.py` to test the built wheel in a separate virtual environment.
6. Review the default and custom icon galleries, and verify that GitHub Pages builds successfully.
7. Update the release notes and changelog to describe only the features included in the version.
8. Create a version tag. The [release workflow](https://github.com/SergioGilBorras/treeforge/actions/workflows/release.yml) builds and attaches the distribution artifacts to its GitHub Release.

TreeForge is distributed through GitHub. Consult the [roadmap](roadmap.md) for planned enhancements and [size guidance](size-guidance.md) for practical diagram dimensions.
