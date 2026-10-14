"""Connected geometric SVG directory-tree renderer.

Textual tree glyphs are deliberately not used to draw branches. Every parent
owns a continuous SVG trunk and each child has a geometric horizontal elbow.
"""
from __future__ import annotations

import html
from pathlib import Path
from .core import Node, TreeConfig
from .render import palette, category, DEFAULT_SYMBOLS, custom_icon


def svg_vertical(root: Node, config: TreeConfig) -> str:
    colors = palette(config)
    rows: list[tuple[Node, int, int | None]] = []
    children: dict[int, list[int]] = {}

    def collect(node: Node, depth: int, parent: int | None) -> int:
        index = len(rows)
        rows.append((node, depth, parent))
        children[index] = []
        if parent is not None:
            children[parent].append(index)
        for child in node.children:
            collect(child, depth + 1, index)
        if node.hidden:
            collect(Node(f"… {node.hidden} hidden", False), depth + 1, index)
        return index

    collect(root, 0, None)
    row_height, indent, left, top = (44 if config.boxes else 34), 40, 28, 42
    positions = [(left + depth * indent, top + index * row_height)
                 for index, (_, depth, _) in enumerate(rows)]
    width = max(480, max(
        x + 40 + 9.2 * (len(node.name) + 5 + (len(str(len(node.members))) if node.members else 0))
        for (node, _, _), (x, _) in zip(rows, positions)
    ) + 22)
    height = top + (len(rows) - 1) * row_height + 38
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" '
        f'height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">',
        f'<rect width="100%" height="100%" fill="{colors["background"]}"/>'
    ]
    # A continuous parent trunk reaches the last child; short arms meet it exactly.
    # Coordinate generation is independent of font metrics and icon rendering.
    for parent, child_indices in children.items():
        if not child_indices:
            continue
        parent_x, parent_y = positions[parent]
        trunk_x = positions[child_indices[0]][0] - indent / 2
        last_y = positions[child_indices[-1]][1]
        parts.append(
            f'<path data-tree-edge="trunk" d="M {parent_x+14:.1f} {parent_y:.1f} '
            f'H {trunk_x:.1f} V {last_y:.1f}" fill="none" '
            f'stroke="{colors["line"]}" stroke-width="1.8" stroke-linecap="round" '
            f'stroke-linejoin="round"/>'
        )
        for index in child_indices:
            x, y = positions[index]
            parts.append(
                f'<path data-tree-edge="arm" d="M {trunk_x:.1f} {y:.1f} '
                f'H {x-7:.1f}" fill="none" stroke="{colors["line"]}" '
                f'stroke-width="1.8" stroke-linecap="round"/>'
            )
    for index, (node, _, _) in enumerate(rows):
        x, y = positions[index]
        kind = category(node, config)
        suffix = Path(node.name).suffix.lower().lstrip(".")
        color = colors.get("." + suffix, colors.get(suffix,
                colors.get(kind, colors["file"])))
        label = node.name + ("/" if node.directory else "")
        if node.members and config.show_counts:
            label += f" [{len(node.members)}]"
        if config.boxes:
            box_width = max(84, 36 + len(label) * 9.2)
            parts.append(
                f'<rect data-tree-node="box" x="{x-5:.1f}" y="{y-15:.1f}" '
                f'width="{box_width:.1f}" height="30" rx="6" '
                f'fill="{color}" fill-opacity="0.07" stroke="{color}" '
                f'stroke-opacity="0.25" stroke-width="0.8"/>'
            )
        icon_uri = custom_icon(node, config)
        if icon_uri:
            parts.append(
                f'<image x="{x:.1f}" y="{y-11:.1f}" width="22" height="22" '
                f'href="{icon_uri}"/>'
            )
        else:
            symbol = DEFAULT_SYMBOLS.get(kind, DEFAULT_SYMBOLS["file"])
            parts.append(f'<text x="{x:.1f}" y="{y+6:.1f}" '
                         f'font-family="sans-serif" font-size="18">{html.escape(symbol)}</text>')
        parts.append(f'<text x="{x+29:.1f}" y="{y+5:.1f}" '
                     f'font-family="monospace" font-size="15" fill="{color}">'
                     f'{html.escape(label)}</text>')
    parts.append("</svg>")
    return "\n".join(parts)
