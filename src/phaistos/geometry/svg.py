"""Programmatic SVG rendering engine for the Phaistos Disc."""

import math
from pathlib import Path
from typing import List, Tuple
from phaistos.core.models import DiscCorpus, DiscSide, Group
from phaistos.visualizer.glyphs import get_sign_glyph_data


def render_side_svg(
    side: DiscSide,
    corpus: DiscCorpus,
    width: int = 800,
    height: int = 800,
    glyph_mode: str = "emoji_utf8",
) -> str:
    """
    Render a clean, publication-ready programmatic SVG spiral diagram of one disc side.
    Outside-in spiral track layout with radial group dividers and sign glyphs.
    Supports glyph_mode: 'emoji_utf8' (default), 'vector_svg', or 'unicode_raw'.
    """
    cx, cy = width / 2.0, height / 2.0
    r_max = width * 0.45
    r_min = width * 0.12

    # Map groups into sequential sign slots
    total_signs = side.sign_count
    # Archimedean spiral parameter: r(theta) = a + b * theta
    # In outside-in reading: theta goes from 0 to max_turns * 2pi, r decreases from r_max to r_min
    max_turns = 4.2
    max_theta = max_turns * 2.0 * math.pi

    svg_elements = []
    # Background and disc clay circle
    svg_elements.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r_max + 20}" fill="#F4EDE2" stroke="#B8977E" stroke-width="3" />'
    )
    svg_elements.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r_min - 15}" fill="#E8DEC8" stroke="#B8977E" stroke-width="1.5" />'
    )

    # Title
    mode_label = "Emoji + ID" if glyph_mode == "emoji_utf8" else ("Vector SVG" if glyph_mode == "vector_svg" else "Unicode SMP")
    svg_elements.append(
        f'<text x="{cx}" y="{35}" font-family="system-ui, sans-serif" font-size="22" font-weight="bold" fill="#3D312A" text-anchor="middle">PHAISTOS DISC — SIDE {side.side}</text>'
    )
    svg_elements.append(
        f'<text x="{cx}" y="{60}" font-family="system-ui, sans-serif" font-size="13" fill="#7A685D" text-anchor="middle">{side.group_count} groups | {side.sign_count} stamped signs | {side.oblique_stroke_count} incised strokes | Mode: {mode_label}</text>'
    )

    # Sign lookup
    sign_map = {s.evans_id: s for s in corpus.signs_catalogue}

    sign_index = 0
    group_boundaries: List[Tuple[float, float, float, float]] = []

    for group in side.groups:
        group_start_idx = sign_index
        group_signs_coords = []

        for sign_id in group.signs:
            frac = sign_index / float(total_signs)
            theta = frac * max_theta
            r = r_max - frac * (r_max - r_min)

            # Convert polar to cartesian (clockwise spiral starting from top-right)
            x = cx + r * math.cos(theta - math.pi / 2.0)
            y = cy + r * math.sin(theta - math.pi / 2.0)

            sign_obj = sign_map.get(sign_id)
            glyph = sign_obj.unicode_char if sign_obj else sign_id
            name = sign_obj.name if sign_obj else "UNKNOWN"

            group_signs_coords.append((x, y, r, theta, sign_id, glyph, name))
            sign_index += 1

        # Draw group separator boundary before group
        if group_signs_coords:
            first_x, first_y, first_r, first_theta, _, _, _ = group_signs_coords[0]
            # radial divider
            dr = 18.0
            x1 = cx + (first_r - dr) * math.cos(first_theta - math.pi / 2.0 - 0.05)
            y1 = cy + (first_r - dr) * math.sin(first_theta - math.pi / 2.0 - 0.05)
            x2 = cx + (first_r + dr) * math.cos(first_theta - math.pi / 2.0 - 0.05)
            y2 = cy + (first_r + dr) * math.sin(first_theta - math.pi / 2.0 - 0.05)
            svg_elements.append(
                f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#8B6B55" stroke-width="2" stroke-linecap="round" />'
            )

            # Group label
            lbl_r = first_r + 26.0
            lbl_x = cx + lbl_r * math.cos(first_theta - math.pi / 2.0)
            lbl_y = cy + lbl_r * math.sin(first_theta - math.pi / 2.0)
            svg_elements.append(
                f'<text x="{lbl_x:.1f}" y="{lbl_y:.1f}" font-family="monospace" font-size="9" font-weight="bold" fill="#6E503B" text-anchor="middle">{group.id}</text>'
            )

        # Draw signs inside group
        for idx_in_grp, (sx, sy, sr, stheta, sid, sglyph, sname) in enumerate(group_signs_coords):
            # Sign node circle
            svg_elements.append(
                f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="15" fill="#FFFDF8" stroke="#D1BEAD" stroke-width="1.2" />'
            )
            gdata = get_sign_glyph_data(sid)

            if glyph_mode == "vector_svg":
                scale = 0.60
                tx = sx - 9.6
                ty = sy - 10.5
                svg_elements.append(
                    f'<g transform="translate({tx:.1f}, {ty:.1f}) scale({scale})" color="#2C221D">{gdata["vector_svg"]}</g>'
                )
                svg_elements.append(
                    f'<text x="{sx:.1f}" y="{sy + 12.5:.1f}" font-family="monospace" font-size="5.5" font-weight="bold" fill="#8C796C" text-anchor="middle">{sid}</text>'
                )
            elif glyph_mode == "unicode_raw":
                svg_elements.append(
                    f'<text x="{sx:.1f}" y="{sy + 5:.1f}" font-family="system-ui, sans-serif" font-size="14" fill="#2C221D" text-anchor="middle">{sglyph}</text>'
                )
                svg_elements.append(
                    f'<text x="{sx:.1f}" y="{sy + 12:.1f}" font-family="monospace" font-size="5.5" font-weight="bold" fill="#8C796C" text-anchor="middle">{sid}</text>'
                )
            else:  # default "emoji_utf8"
                svg_elements.append(
                    f'<text x="{sx:.1f}" y="{sy + 3.5:.1f}" font-family="Apple Color Emoji, Segoe UI Emoji, Noto Color Emoji, sans-serif" font-size="13" text-anchor="middle" dominant-baseline="central">{gdata["emoji"]}</text>'
                )
                svg_elements.append(
                    f'<text x="{sx:.1f}" y="{sy + 11.5:.1f}" font-family="monospace" font-size="6" font-weight="bold" fill="#78350F" text-anchor="middle">{sid}</text>'
                )

            # If group has oblique stroke and this is the final sign, draw the stroke
            if group.oblique_stroke and (idx_in_grp == len(group.signs) - 1):
                # Small slash beneath sign
                stroke_x1 = sx - 6
                stroke_y1 = sy + 15
                stroke_x2 = sx + 6
                stroke_y2 = sy + 21
                svg_elements.append(
                    f'<line x1="{stroke_x1:.1f}" y1="{stroke_y1:.1f}" x2="{stroke_x2:.1f}" y2="{stroke_y2:.1f}" stroke="#B22222" stroke-width="2.5" stroke-linecap="round" />'
                )

    svg_content = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">\n'
        + "\n".join(f"  {el}" for el in svg_elements)
        + "\n</svg>"
    )
    return svg_content


def export_disc_svgs(corpus: DiscCorpus, output_dir: Path, glyph_mode: str = "emoji_utf8") -> Tuple[Path, Path]:
    """Export both Side A and Side B SVG diagrams."""
    output_dir.mkdir(parents=True, exist_ok=True)
    svg_a = render_side_svg(corpus.side_a, corpus, glyph_mode=glyph_mode)
    svg_b = render_side_svg(corpus.side_b, corpus, glyph_mode=glyph_mode)

    path_a = output_dir / "disc_side_a.svg"
    path_b = output_dir / "disc_side_b.svg"

    path_a.write_text(svg_a, encoding="utf-8")
    path_b.write_text(svg_b, encoding="utf-8")
    return path_a, path_b
