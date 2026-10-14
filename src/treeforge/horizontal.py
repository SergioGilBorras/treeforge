"""Native SVG horizontal tree with explicit left or center node alignment."""
from __future__ import annotations

import html
from .core import Node, TreeConfig
from .render import category, palette, custom_icon, DEFAULT_SYMBOLS


def svg_horizontal(root: Node, config: TreeConfig) -> str:
    colors = palette(config)
    nodes: list[tuple[Node, int, int | None]] = []
    depths: list[int] = []
    def collect(node: Node, depth: int, parent: int | None) -> int:
        index = len(nodes)
        nodes.append((node, depth, parent))
        depths.append(depth)
        for child in node.children:
            collect(child, depth + 1, index)
        if node.hidden:
            collect(Node(f"… {node.hidden} hidden", False), depth + 1, index)
        return index
    collect(root, 0, None)

    # Determine column widths from actual label lengths, avoiding overlap.
    column_widths: dict[int, float] = {}
    for node, depth, _ in nodes:
        label = node.name + ("/" if node.directory else "")
        if node.members and config.show_counts:
            label += f" [{len(node.members)}]"
        column_widths[depth] = max(column_widths.get(depth, 0), 54 + len(label) * 8.7)

    left: dict[int, float] = {}
    start = 30.0
    for depth in sorted(column_widths):
        left[depth] = start
        start += column_widths[depth] + 64
    width = max(480.0, start + 24)

    children: dict[int, list[int]] = {i: [] for i in range(len(nodes))}
    for i, (_, _, parent) in enumerate(nodes):
        if parent is not None:
            children[parent].append(i)
    y: dict[int, float] = {}
    leaf_index = [0]
    def position(index: int) -> float:
        if not children[index]:
            result = 48 + leaf_index[0] * (68 if config.boxes else 48)
            leaf_index[0] += 1
        else:
            ys = [position(child) for child in children[index]]
            result = (ys[0] + ys[-1]) / 2
        y[index] = result
        return result
    position(0)
    height = max(110, 48 + max(1, leaf_index[0]) * (68 if config.boxes else 48))
    # With center alignment, center the entire layout in a symmetric canvas.
    if config.align == "center":
        content_end = max(left[depth] + column_widths[depth] for depth in left)
        width = max(width, content_end + 60)
        offset = max(0.0, (width - content_end - 30) / 2)
    else:
        offset = 0.0

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">',
        f'<rect width="100%" height="100%" fill="{colors["background"]}"/>',
    ]
    # Draw elbows behind node labels. Routes are deterministic, with orthogonal edges.
    for index, (node, depth, parent) in enumerate(nodes):
        if parent is None:
            continue
        parent_depth = nodes[parent][1]
        x1 = left[parent_depth] + column_widths[parent_depth] - (2 if config.boxes else 8) + offset
        x2 = left[depth] - (14 if config.boxes else 12) + offset
        halfway = x1 + (x2 - x1) * 0.52
        parts.append(
            f'<path d="M {x1:.1f} {y[parent]:.1f} H {halfway:.1f} '
            f'V {y[index]:.1f} H {x2:.1f}" fill="none" '
            f'stroke="{colors["line"]}" stroke-width="1.5"/>'
        )

    for index, (node, depth, _) in enumerate(nodes):
        x = left[depth] + offset
        cy = y[index]
        kind = category(node, config)
        color = colors.get(kind, colors.get("file", "#68788c"))
        suffix = node.name.rsplit(".", 1)[-1].lower()
        color = colors.get("." + suffix, colors.get(suffix, color))
        label = node.name + ("/" if node.directory else "")
        if node.members and config.show_counts:
            label += f" [{len(node.members)}]"
        if config.boxes:
            parts.append(
                f'<rect x="{x-8:.1f}" y="{cy-16:.1f}" width="{min(column_widths[depth]-5, 42+len(label)*8.7):.1f}" '
                f'height="32" rx="7" fill="{color}" fill-opacity="0.07" '
                f'stroke="{color}" stroke-opacity="0.28" stroke-width="0.8"/>'
            )
        icon = custom_icon(node, config)
        if icon:
            parts.append(f'<image x="{x:.1f}" y="{cy-11:.1f}" width="22" height="22" href="{icon}"/>')
        else:
            symbol = DEFAULT_SYMBOLS.get(kind, DEFAULT_SYMBOLS["file"])
            parts.append(
                f'<text x="{x:.1f}" y="{cy+6:.1f}" font-size="18" '
                f'font-family="sans-serif">{html.escape(symbol)}</text>'
            )
        parts.append(
            f'<text x="{x+29:.1f}" y="{cy+5:.1f}" fill="{color}" font-size="14" '
            f'font-family="monospace">{html.escape(label)}</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts)
