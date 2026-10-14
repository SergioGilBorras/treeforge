# Icons and icon packs

TreeForge always has built-in Unicode fallback icons. To customize the **native vertical SVG** renderer, pass a directory of your own small, self-contained SVG icons:

```bash
treeforge render . -o tree.svg --icons-dir ./icons
```

Or from Python: `TreeConfig(icons_dir="./icons")`.

For each node, icons are selected in this order: **file extension** (e.g. `py.svg`, `json.svg`), **category** (e.g. `images.svg`, `data.svg`), and **fallback kind** (`folder.svg` or `file.svg`). The first usable icon is embedded directly in the final SVG. Sample icons are located in the repository's [icons directory](../icons/). Copy and edit them freely.

The icon importer accepts small SVG files (64 KiB maximum each) and rejects scripting, external references and embedded images. Restrict custom packs to trusted assets. If no suitable icon is found, a Unicode icon is displayed.

**Current scope:** custom SVG icons apply to native SVG output in vertical and horizontal layouts; the Mermaid/Graphviz and TXT exporters do not currently embed those icons. In this first release, built-in defaults are Unicode, not bundled SVG icon replacements.

Planned upgrades: configurable mapping table, SVG-backed built-in icon pack, horizontal icon support, richer inheritance and fully consistent renderer themes.
