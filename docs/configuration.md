# Configuration

Use `TreeConfig` in Python or load a JSON/YAML configuration file with `--config`. YAML uses the optional `treeforge[yaml]` extra.

```json
{
  "max_depth": 3,
  "max_nodes": 70,
  "min_group": 3,
  "group_by": ["prefix", "extension"],
  "theme": "light",
  "boxes": false,
  "align": "left",
  "colors": {
    "background": "#ffffff",
    "foreground": "#253047",
    "line": "#aabbcc",
    "folder": "#376aab",
    "images": "#a855a0",
    "data": "#d1872c",
    "py": "#438b56"
  }
}
```

Colors use six-digit hexadecimal values. Configuration supplied through `--config` defines the rendering settings; command-line layout and engine options still select the output representation. `colors` keys may match categories (`images`, `folder`, `data`) or extensions (`py`, `json`). Built-in light and dark palettes are available.

## Grouping

- `prefix`: only safe numeric sequences with a shared prefix and extension, e.g. `frame_001.png`, `frame_002.png`, `frame_003.png` become `frame_*.png`.
- `extension`: remaining files grouped by logical category (`images`, `documents`, `data`, `spreadsheets`) or extension.
- `min_group`: minimum files needed to create a group.
- `preserve`: files to keep visible (README, Dockerfile, etc.).
- `exclude`: directory entries to ignore while scanning.
- `max_depth`: root is depth 0.
- `max_nodes`: total diagram node budget.
- `icons_dir`: local directory of user-provided SVG icons for native SVG output in both layouts (see [Icons](icons.md)).

Grouping preserves original filenames in each aggregated node's `members` list.

## YAML configuration

Install YAML support with `pip install 'treeforge[yaml]'`, then use `treeforge render . --config treeforge.yaml`. YAML files accept the same configuration keys as JSON, using a safe parser.
