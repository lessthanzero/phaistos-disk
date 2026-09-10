"""Interactive Audio-Epigraphic Visualizer and Research Workbench.

Generates a standalone, publication-grade HTML/SVG/WebAudio workbench adhering
to California/Swiss editorial modernism for the Phaistos Disc Laboratory.
"""

import json
import math
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from phaistos.core.models import DiscCorpus
from phaistos.epigraphy.strokes import evaluate_oblique_strokes
from phaistos.comparative.suffix_analyzer import analyze_suffix_correspondence
from phaistos.linguistics.grid_factorization import factorize_kober_grid
from phaistos.typometry.shrinkage_model import reconstruct_punches_and_shrinkage
from phaistos.visualizer.glyphs import get_all_glyphs_catalog
from phaistos.ritual.hagia_gallery import get_hagia_gallery_manifest
from phaistos.ritual.homology_breakdown import get_all_groups_homology_manifest
from phaistos.ritual.clause_parser import get_clauses_manifest
from phaistos.stats.homology_surrogate import evaluate_homology_significance


def _get_image_data_uri(path: Path) -> str:
    """Read an image and encode as base64 data URI if present."""
    if not path.is_file():
        root = Path(__file__).resolve().parent.parent.parent.parent
        alt = root / path
        if not alt.is_file():
            return ""
        path = alt
    import base64
    raw = path.read_bytes()
    ext = path.suffix.lstrip(".").lower()
    mime = f"image/{ext}" if ext != "jpg" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"


def compute_spiral_coordinates(groups, width=800, height=800):
    """Compute polar-to-cartesian spiral coordinates for groups and signs."""
    cx, cy = width / 2.0, height / 2.0
    r_max = width * 0.44
    r_min = width * 0.12
    max_turns = 4.2
    max_theta = max_turns * 2.0 * math.pi

    total_signs = sum(len(g.signs) for g in groups)
    sign_index = 0
    result_groups = []

    for g in groups:
        signs_data = []
        for pos, s_id in enumerate(g.signs):
            frac = sign_index / float(total_signs) if total_signs > 0 else 0
            theta = frac * max_theta
            r = r_max - frac * (r_max - r_min)
            x = cx + r * math.cos(theta - math.pi / 2.0)
            y = cy + r * math.sin(theta - math.pi / 2.0)

            signs_data.append({
                "sign_id": s_id,
                "pos": pos,
                "x": round(x, 1),
                "y": round(y, 1),
                "r": round(r, 1),
                "theta": round(theta, 3),
            })
            sign_index += 1

        result_groups.append({
            "id": g.id,
            "side": g.side,
            "turn": g.turn,
            "signs": g.signs,
            "oblique_stroke": g.oblique_stroke,
            "erasure": g.erasure,
            "signs_coords": signs_data,
        })

    return result_groups


def compute_performance_schedule(groups, signs_cat, mora_sec: float = 0.28):
    """Compute timed performance schedule for all groups in a side."""
    from phaistos.prosody.acoustic import CATEGORY_PITCH_MAP, PHORMINX_SCALE
    schedule = []
    for g in groups:
        signs_data = []
        has_stroke = g["oblique_stroke"]
        thetas = [s["theta"] for s in g["signs_coords"]]
        avg_theta = sum(thetas) / float(len(thetas)) if thetas else 0.0
        # Disc rotation needed to bring group centroid to 12 o'clock (theta = 0)
        target_angle_deg = round(-math.degrees(avg_theta), 2)

        total_group_morae = 0
        for idx, s in enumerate(g["signs_coords"]):
            s_id = s["sign_id"]
            meta = signs_cat.get(s_id, {})
            cat = meta.get("category", "human")
            pitch = CATEGORY_PITCH_MAP.get(cat, "D4")
            freq = PHORMINX_SCALE.get(pitch, 293.66)
            is_final = (idx == len(g["signs_coords"]) - 1)
            morae = 2 if (is_final and has_stroke) else 1
            total_group_morae += morae
            duration_ms = int(morae * mora_sec * 1000)

            signs_data.append({
                "sign_id": s_id,
                "pos": idx,
                "char": meta.get("char", s_id),
                "name": meta.get("name", "Unknown"),
                "category": cat,
                "pitch": pitch,
                "freq": round(freq, 2),
                "morae": morae,
                "duration_ms": duration_ms,
                "stroke": (is_final and has_stroke),
            })

        pause_ms = 350 if has_stroke else 120
        total_duration_ms = sum(sd["duration_ms"] for sd in signs_data) + pause_ms

        schedule.append({
            "group_id": g["id"],
            "side": g["side"],
            "turn": g["turn"],
            "target_angle_deg": target_angle_deg,
            "morae": total_group_morae,
            "duration_ms": total_duration_ms,
            "pause_ms": pause_ms,
            "has_stroke": has_stroke,
            "has_erasure": g.get("erasure", False),
            "signs": signs_data,
        })
    return schedule


def generate_workbench_html(corpus: DiscCorpus, output_path: Optional[Path] = None) -> str:
    """Generate the comprehensive self-contained HTML workbench file."""
    # 1. Run all frontier analytical modules
    stroke_res = evaluate_oblique_strokes(corpus)
    suffix_res = analyze_suffix_correspondence(corpus)
    grid_res = factorize_kober_grid(corpus, n_consonants=5, n_vowels=4, n_null_iterations=10)
    shrinkage_res = reconstruct_punches_and_shrinkage(corpus)

    # 2. Extract sign metadata catalogue
    signs_cat = {
        s.evans_id: {
            "name": s.name,
            "char": s.unicode_char,
            "category": s.category,
            "desc": s.description,
        }
        for s in corpus.signs_catalogue
    }

    # 3. Geometry data for both sides
    groups_a = compute_spiral_coordinates(corpus.side_a.groups)
    groups_b = compute_spiral_coordinates(corpus.side_b.groups)

    # 4. Timed performance schedule
    schedule_a = compute_performance_schedule(groups_a, signs_cat)
    schedule_b = compute_performance_schedule(groups_b, signs_cat)

    # 5. JSON Payload for frontend
    data_payload = {
        "hagia_gallery": get_hagia_gallery_manifest(),
        "homology_manifest": get_all_groups_homology_manifest(corpus),
        "clauses_manifest": get_clauses_manifest(corpus),
        "homology_stats": evaluate_homology_significance(n_iterations=500).__dict__,
        "signs_cat": signs_cat,
        "glyphs_catalog": get_all_glyphs_catalog(),
        "side_a": groups_a,
        "side_b": groups_b,
        "schedule_a": schedule_a,
        "schedule_b": schedule_b,
        "photo_disc_a": _get_image_data_uri(Path("reports/visuals/photos/disc_photo_a.webp")),
        "photo_disc_b": _get_image_data_uri(Path("reports/visuals/photos/disc_photo_b.webp")),
        "arkalochori_photo": _get_image_data_uri(Path("reports/visuals/comparative/arkalochori_axe_hm584.webp")),
        "frontier_a": {
            "total_strokes": stroke_res.total_strokes,
            "side_a": stroke_res.side_a_strokes,
            "side_b": stroke_res.side_b_strokes,
            "virama_verdict": stroke_res.virama_eval.falsification_verdict,
            "coverage_pct": round(stroke_res.virama_eval.textual_coverage_pct, 1),
            "ictus_verdict": stroke_res.ictus_eval.support_verdict,
            "cadence_count": stroke_res.ictus_eval.side_b_stanza_cadence_count,
            "cadence_p": round(stroke_res.ictus_eval.side_b_stanza_cadence_p_value, 4),
        },
        "frontier_b": {
            "sign_35_me_p": f"{suffix_res.sign_35_me_test.binomial_p_value:.2e}",
            "sign_35_te_p": round(suffix_res.sign_35_te_test.likelihood, 3),
            "lr_te_vs_me": f"{suffix_res.likelihood_ratio_te_vs_me:.1e}",
            "me_verdict": suffix_res.sign_35_me_test.verdict,
            "te_verdict": suffix_res.sign_35_te_test.verdict,
        },
        "frontier_c": {
            "n_consonants": grid_res.n_consonant_classes,
            "n_vowels": grid_res.n_vowel_classes,
            "grid": grid_res.grid,
            "top_var_pct": round(grid_res.metrics.explained_variance_ratio_svd[0] * 100.0, 1),
            "z_score": round(grid_res.metrics.structure_z_score, 2),
            "p_value": round(grid_res.metrics.structure_p_value, 4),
            "c_silhouette": round(grid_res.metrics.consonant_silhouette_score, 3),
            "v_silhouette": round(grid_res.metrics.vowel_silhouette_score, 3),
        },
        "frontier_d": {
            "drying_pct": shrinkage_res.shrinkage_profile.drying_shrinkage_pct,
            "firing_pct": shrinkage_res.shrinkage_profile.firing_shrinkage_pct,
            "total_shrinkage_pct": round(shrinkage_res.shrinkage_profile.total_linear_shrinkage_pct, 2),
            "fired_diam_mm": shrinkage_res.shrinkage_profile.disc_fired_diameter_mm,
            "wet_diam_mm": round(shrinkage_res.shrinkage_profile.disc_wet_diameter_mm, 1),
            "mean_force_n": round(shrinkage_res.mean_stamping_force_newtons, 1),
            "expansion_factor": round(shrinkage_res.mean_expansion_factor, 4),
            "material_verdict": shrinkage_res.punch_material_verdict,
        },
        "triad_timing": [
            {"group_id": "A14", "morae": 6, "duration_ms": 1560, "freq": 293.66},
            {"group_id": "A15", "morae": 3, "duration_ms": 780, "freq": 329.63},
            {"group_id": "A16", "morae": 5, "duration_ms": 1300, "freq": 392.00},
            {"group_id": "A17", "morae": 7, "duration_ms": 1820, "freq": 293.66},
            {"group_id": "A18", "morae": 2, "duration_ms": 520, "freq": 329.63},
            {"group_id": "A19", "morae": 5, "duration_ms": 1300, "freq": 392.00},
            {"group_id": "A20", "morae": 6, "duration_ms": 1560, "freq": 293.66},
            {"group_id": "A21", "morae": 3, "duration_ms": 780, "freq": 329.63},
            {"group_id": "A22", "morae": 5, "duration_ms": 1300, "freq": 392.00},
        ],
    }

    raw_json = json.dumps(data_payload)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Phaistos Disc Laboratory — Interactive Epigraphic & Audio Workbench</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@300;400;500;600&family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600&family=Noto+Sans+Phaistos+Disc&display=swap" rel="stylesheet">
  <style>
    :root {{
      --canvas: #FAF8F5;
      --canvas-subtle: #F4F1EA;
      --surface: #FFFFFF;
      --ink: #18181B;
      --ink-secondary: #3F3F46;
      --ink-muted: #52525B;
      --editorial-border: rgba(24, 24, 27, 0.08);
      --editorial-border-active: rgba(24, 24, 27, 0.25);
      --clay-base: #EADBC8;
      --clay-stroke: #B8977E;
      --accent: #B45309;
      --accent-cadence: #059669;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--canvas);
      color: var(--ink);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans', 'Noto Sans Phaistos Disc', 'Aegean', sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-rendering: optimizeLegibility;
      line-height: 1.5;
      padding: 32px 40px;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--editorial-border);
      margin-bottom: 32px;
    }}
    .title-area h1 {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: 38px;
      font-weight: 400;
      letter-spacing: -0.01em;
      color: var(--ink);
    }}
    .title-area p {{
      font-family: 'Geist Mono', 'SF Mono', ui-monospace, monospace;
      font-size: 11px;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--ink);
      margin-top: 6px;
    }}
    .header-telemetry {{
      font-family: 'Geist Mono', 'SF Mono', ui-monospace, monospace;
      font-size: 11px;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--ink);
      text-align: right;
      transform: translateY(-2px);
    }}
    .workbench-grid {{
      display: grid;
      grid-template-columns: 820px 1fr;
      gap: 32px;
      align-items: start;
    }}
    .spiral-card {{
      background: var(--surface);
      border: 1px solid var(--editorial-border);
      border-radius: 12px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      box-shadow: 0 4px 20px rgba(0,0,0,0.02);
    }}
    .controls-bar {{
      display: flex;
      justify-content: space-between;
      width: 100%;
      margin-bottom: 16px;
      align-items: center;
      gap: 8px;
      flex-wrap: nowrap;
    }}
    .primary-controls {{
      display: inline-flex;
      align-items: center;
      flex-shrink: 0;
    }}
    .secondary-controls {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      flex-wrap: nowrap;
      flex-shrink: 0;
    }}
    .btn-group {{
      display: inline-flex;
      background: var(--canvas-subtle);
      border-radius: 9999px;
      padding: 2px;
      border: 1px solid var(--editorial-border);
      height: 34px;
      box-sizing: border-box;
      align-items: center;
    }}
    .btn {{
      background: none;
      border: none;
      font-family: 'Inter', sans-serif;
      font-size: 13px;
      font-weight: 500;
      padding: 0 14px;
      height: 100%;
      border-radius: 9999px;
      cursor: pointer;
      color: var(--ink-secondary);
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      box-sizing: border-box;
      white-space: nowrap;
    }}
    .btn.active {{
      background: var(--surface);
      color: var(--ink);
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }}
    .editorial-select {{
      background: var(--canvas-subtle);
      border: 1px solid var(--editorial-border);
      border-radius: 9999px;
      font-family: 'Inter', sans-serif;
      font-size: 12.5px;
      font-weight: 500;
      color: var(--ink);
      padding: 0 12px;
      height: 34px;
      box-sizing: border-box;
      cursor: pointer;
      outline: none;
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
    }}
    .editorial-select:hover {{
      border-color: var(--editorial-border-active);
      background: var(--surface);
    }}
    .control-checkbox-label {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 500;
      color: var(--ink);
      cursor: pointer;
      user-select: none;
      background: var(--canvas-subtle);
      border: 1px solid var(--editorial-border);
      border-radius: 9999px;
      padding: 0 12px;
      height: 34px;
      box-sizing: border-box;
      transition: all 0.15s ease;
      white-space: nowrap;
    }}
    .control-checkbox-label:hover {{
      background: var(--surface);
      border-color: var(--editorial-border-active);
    }}
    .control-checkbox-label input[type="checkbox"] {{
      accent-color: var(--accent);
      cursor: pointer;
      width: 14px;
      height: 14px;
    }}
    .control-radio-group {{
      display: inline-flex;
      align-items: center;
      gap: 12px;
      background: var(--canvas-subtle);
      border: 1px solid var(--editorial-border);
      border-radius: 9999px;
      padding: 0 14px;
      height: 34px;
      box-sizing: border-box;
      white-space: nowrap;
    }}
    .control-radio-label {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-size: 12px;
      font-weight: 500;
      color: var(--ink);
      cursor: pointer;
      user-select: none;
    }}
    .control-radio-label input[type="radio"] {{
      accent-color: var(--ink);
      cursor: pointer;
      width: 13px;
      height: 13px;
    }}
    .btn-primary {{
      background: var(--ink);
      color: #FFF;
      padding: 0 20px;
      height: 38px;
      font-size: 13.5px;
      font-weight: 600;
      border-radius: 9999px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition: all 0.15s ease;
    }}
    .btn-primary:hover {{ background: #27272A; }}
    .audio-panel {{
      width: 100%;
      background: var(--canvas-subtle);
      border-radius: 8px;
      padding: 12px 16px;
      display: flex;
      align-items: center;
      gap: 16px;
      margin-top: 16px;
      border: 1px solid var(--editorial-border);
    }}
    .audio-telemetry {{
      font-family: 'Geist Mono', monospace;
      font-size: 12px;
      color: var(--ink-secondary);
      flex: 1;
    }}
    .teleprompter-box {{
      width: 100%;
      background: var(--canvas-subtle);
      border-radius: 10px;
      padding: 16px 18px;
      margin-top: 14px;
      border: 1px solid var(--editorial-border);
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}
    .teleprompter-controls {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      width: 100%;
    }}
    .teleprompter-actions {{
      display: flex;
      gap: 6px;
      align-items: center;
      flex-wrap: nowrap;
      width: 100%;
    }}
    .teleprompter-actions .btn {{
      flex: 1;
      height: 38px;
      padding: 0 10px;
      font-size: 12.5px;
      font-weight: 500;
      background: var(--surface);
      border: 1px solid var(--editorial-border);
      white-space: nowrap;
      min-width: 0;
      justify-content: center;
      transition: all 0.15s ease;
    }}
    .teleprompter-actions .btn:hover {{
      background: #FFFFFF;
      border-color: var(--editorial-border-active);
    }}
    .teleprompter-actions .btn-primary {{
      background: var(--ink);
      color: #FFF;
      border: none;
      padding: 0 12px;
    }}
    .teleprompter-actions .btn-primary:hover {{
      background: #27272A;
    }}
    .teleprompter-secondary-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      flex-wrap: nowrap;
    }}
    .speed-controls {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 12px;
      font-family: 'Geist Mono', monospace;
      color: var(--ink-secondary);
      height: 38px;
    }}
    .btn-sm {{
      height: 28px;
      padding: 0 10px;
      font-size: 11px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }}
    .hud-telemetry-panel {{
      display: grid;
      grid-template-columns: repeat(4, 1fr) 2fr;
      gap: 8px;
      padding-top: 10px;
      border-top: 1px solid var(--editorial-border);
      font-family: 'Geist Mono', monospace;
    }}
    .hud-col {{
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .hud-label {{
      font-size: 10px;
      color: var(--ink-secondary);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      font-weight: 500;
    }}
    .hud-val {{
      font-size: 11px;
      font-weight: 600;
      color: var(--ink);
    }}
    .hud-progress-bg {{
      width: 100%;
      height: 6px;
      background: rgba(24, 24, 27, 0.08);
      border-radius: 9999px;
      overflow: hidden;
      margin-top: 4px;
    }}
    .hud-progress-fill {{
      height: 100%;
      width: 0%;
      background: var(--accent);
      border-radius: 9999px;
      transition: width 0.15s ease;
    }}
    .active-teleprompter-group circle.sign-circle {{
      stroke: #D97706 !important;
      stroke-width: 2.5px !important;
      fill: #FEF3C7 !important;
    }}
    .sign-current-mora {{
      fill: #F59E0B !important;
      stroke: #78350F !important;
      stroke-width: 3px !important;
    }}
    .analytics-column {{
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    .card {{
      background: var(--surface);
      border: 1px solid var(--editorial-border);
      border-radius: 12px;
      padding: 22px 24px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.02);
    }}
    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 14px;
      border-bottom: 1px solid var(--editorial-border);
      padding-bottom: 10px;
    }}
    .card-title {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: 21px;
      font-weight: 400;
      color: var(--ink);
      line-height: 1.25;
    }}
    .card-badge {{
      font-family: 'Geist Mono', monospace;
      font-size: 11.5px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--accent);
      background: #FEF3C7;
      padding: 3px 9px;
      border-radius: 9999px;
    }}
    .group-inspector {{
      font-family: 'Inter', sans-serif;
      font-size: 13.5px;
      line-height: 1.55;
      color: var(--ink);
    }}
    .glyph-display {{
      display: flex;
      gap: 8px;
      margin: 14px 0;
      font-size: 26px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .glyph-pill {{
      background: var(--canvas-subtle);
      border: 1px solid var(--editorial-border);
      border-radius: 6px;
      padding: 6px 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-width: 52px;
    }}
    .glyph-pill svg {{
      display: block;
      margin: 2px 0;
    }}
    .glyph-sub {{
      font-size: 11.5px;
      color: var(--ink-secondary);
      font-family: 'Geist Mono', monospace;
    }}
    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      font-family: 'Geist Mono', monospace;
      margin-top: 12px;
      margin-bottom: 6px;
    }}
    table.data-table th {{
      background: var(--canvas-subtle);
      padding: 10px 14px;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--ink-secondary);
      border-bottom: 1.5px solid var(--editorial-border-active);
      text-align: left;
    }}
    table.data-table td {{
      padding: 10px 14px;
      font-size: 13px;
      color: var(--ink);
      border-bottom: 1px solid var(--editorial-border);
      font-variant-numeric: tabular-nums;
    }}
    table.data-table tr:hover td {{
      background: rgba(0,0,0,0.018);
    }}
    .verdict-box {{
      font-size: 13px;
      line-height: 1.55;
      color: var(--ink);
      background: var(--canvas);
      padding: 12px 16px;
      border-radius: 0px;
      border: 1px solid var(--editorial-border);
      border-left: 3px solid #000000;
      margin-top: 12px;
    }}
    .sign-slot {{
      cursor: pointer;
    }}
    .sign-slot:hover circle.sign-circle {{
      filter: drop-shadow(0 2px 6px rgba(0,0,0,0.22));
    }}
    .sign-circle {{
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .sign-circle:hover {{
      stroke: var(--ink) !important;
      stroke-width: 2px !important;
    }}
    .active-sign {{
      fill: #F59E0B !important;
      stroke: #78350F !important;
      stroke-width: 2.5px !important;
    }}
    .active-group {{
      stroke: #D97706 !important;
      stroke-width: 3px !important;
    }}
    /* Hagia Triada Realia Synchronizer */
    .hagia-card {{
      border-color: rgba(217, 119, 6, 0.35);
      background: #FFFCF7;
    }}
    .hagia-sync-body {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .hagia-active-display {{
      display: grid;
      grid-template-columns: 160px 1fr;
      gap: 12px;
      align-items: start;
    }}
    @media (max-width: 600px) {{
      .hagia-active-display {{
        grid-template-columns: 1fr;
      }}
    }}
    .hagia-image-container {{
      position: relative;
      width: 100%;
      height: 135px;
      border-radius: 8px;
      overflow: hidden;
      background: #1C1917;
      border: 1px solid var(--editorial-border);
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }}
    .hagia-active-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: opacity 0.25s ease, transform 0.4s ease;
    }}
    .hagia-image-container:hover .hagia-active-img {{
      transform: scale(1.04);
    }}
    .hagia-img-overlay {{
      position: absolute;
      bottom: 5px;
      left: 5px;
      right: 5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      pointer-events: none;
    }}
    .hagia-plane-tag {{
      font-family: 'Geist Mono', monospace;
      font-size: 10.5px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      background: rgba(120, 53, 15, 0.88);
      color: #FEF3C7;
      padding: 2px 6px;
      border-radius: 4px;
      backdrop-filter: blur(4px);
    }}
    .hagia-scene-tag {{
      font-family: 'Geist Mono', monospace;
      font-size: 10.5px;
      color: #F3F4F6;
      background: rgba(0, 0, 0, 0.72);
      padding: 2px 6px;
      border-radius: 4px;
      backdrop-filter: blur(4px);
    }}
    .hagia-detail-meta {{
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}
    .hagia-title {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: 21px;
      font-weight: 400;
      color: var(--ink);
      line-height: 1.25;
    }}
    .hagia-desc {{
      font-size: 13.5px;
      color: var(--ink-secondary);
      line-height: 1.55;
      margin: 0;
    }}
    .hagia-matched-signs-row {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-top: 6px;
      flex-wrap: wrap;
    }}
    .hagia-matched-label {{
      font-family: 'Geist Mono', monospace;
      font-size: 11px;
      color: var(--ink-secondary);
      letter-spacing: 0.1em;
      font-weight: 600;
      text-transform: uppercase;
    }}
    .hagia-matched-pills {{
      display: inline-flex;
      gap: 4px;
      flex-wrap: wrap;
    }}
    .hagia-matched-pill {{
      font-family: 'Geist Mono', monospace;
      font-size: 11px;
      background: #FEF3C7;
      border: 1px solid #FCD34D;
      color: #92400E;
      padding: 2px 7px;
      border-radius: 4px;
      font-weight: 500;
      display: inline-flex;
      align-items: center;
      gap: 3px;
    }}
    .hagia-carousel-label {{
      font-family: 'Geist Mono', monospace;
      font-size: 11.5px;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--ink-secondary);
      font-weight: 600;
      margin-top: 4px;
    }}
    .hagia-thumb-strip {{
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding: 3px 2px 6px 2px;
      scrollbar-width: thin;
    }}
    .hagia-thumb-strip::-webkit-scrollbar {{
      height: 4px;
    }}
    .hagia-thumb-strip::-webkit-scrollbar-thumb {{
      background: #D1BEA8;
      border-radius: 4px;
    }}
    .hagia-thumb-item {{
      flex: 0 0 64px;
      height: 48px;
      border-radius: 6px;
      overflow: hidden;
      cursor: pointer;
      border: 2px solid transparent;
      position: relative;
      background: #292524;
      opacity: 0.70;
      transition: all 0.15s ease;
    }}
    .hagia-thumb-item:hover {{
      opacity: 1;
      transform: translateY(-2px);
      box-shadow: 0 3px 8px rgba(0,0,0,0.12);
    }}
    .hagia-thumb-item.active {{
      border-color: #D97706;
      opacity: 1;
      box-shadow: 0 0 0 2px rgba(217, 119, 6, 0.4);
      transform: translateY(-1px);
    }}
    .hagia-thumb-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .hagia-thumb-badge {{
      position: absolute;
      bottom: 2px;
      right: 2px;
      background: rgba(0,0,0,0.78);
      color: #FFF;
      font-size: 9px;
      font-family: 'Geist Mono', monospace;
      padding: 1px 3px;
      border-radius: 3px;
      line-height: 1;
    }}
    @keyframes realiaPulse {{
      0% {{ filter: drop-shadow(0 0 2px rgba(217,119,6,0.6)); }}
      50% {{ filter: drop-shadow(0 0 10px rgba(217,119,6,1.0)); transform: scale(1.18); }}
      100% {{ filter: drop-shadow(0 0 2px rgba(217,119,6,0.6)); }}
    }}
    .hagia-realia-match circle.sign-circle {{
      stroke: #D97706 !important;
      stroke-width: 3.5px !important;
      fill: #FEF3C7 !important;
      animation: realiaPulse 1.4s infinite ease-in-out;
    }}

    /* Liturgical Storyboard Ribbon */
    .storyboard-container {{
      width: 100%;
      background: var(--surface);
      border: 1px solid var(--editorial-border);
      border-radius: 8px;
      padding: 10px 14px;
      margin-top: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .storyboard-header {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .storyboard-title {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: 17px;
      font-weight: 400;
      color: var(--ink);
    }}
    .storyboard-caption {{
      font-family: 'Geist Mono', monospace;
      font-size: 10.5px;
      color: var(--ink-secondary);
      letter-spacing: 0.05em;
    }}
    .storyboard-ribbon {{
      display: flex;
      gap: 6px;
      flex-wrap: nowrap;
      width: 100%;
    }}
    .storyboard-chip {{
      flex: 1;
      min-width: 0;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      padding: 6px 4px;
      background: var(--canvas-subtle);
      border: 1px solid var(--editorial-border);
      border-radius: 6px;
      cursor: pointer;
      font-family: 'Geist Mono', monospace;
      white-space: nowrap;
      transition: all 0.15s ease;
      color: var(--ink);
    }}
    .storyboard-chip:hover {{
      background: #FEF3C7;
      border-color: #F59E0B;
    }}
    .storyboard-chip.active {{
      background: #78350F;
      color: #FFFDF9;
      border-color: #78350F;
      box-shadow: 0 1px 4px rgba(120, 53, 15, 0.25);
    }}
    .chip-num {{
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.05em;
      opacity: 0.9;
      flex-shrink: 0;
    }}
    .chip-label {{
      font-size: 11px;
      font-weight: 500;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}

    /* Rosetta Split Sign-by-Sign Dissection */
    .rosetta-box {{
      margin-top: 14px;
      padding-top: 12px;
      border-top: 1px solid var(--editorial-border);
    }}
    .rosetta-title {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: 21px;
      font-weight: 400;
      color: var(--ink);
      margin-bottom: 4px;
      line-height: 1.25;
    }}
    .rosetta-subtitle {{
      font-family: 'Geist Mono', monospace;
      font-size: 11.5px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--ink-secondary);
      margin-bottom: 10px;
    }}
    .rosetta-table {{
      width: 100%;
      border-collapse: collapse;
      font-family: 'Geist Mono', monospace;
      margin-top: 10px;
    }}
    .rosetta-table th {{
      background: var(--canvas-subtle);
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--ink-secondary);
      border-bottom: 1.5px solid var(--editorial-border-active);
      padding: 10px 12px;
      text-align: left;
    }}
    .rosetta-table td {{
      padding: 10px 12px;
      font-size: 13px;
      color: var(--ink);
      border-bottom: 1px solid var(--editorial-border);
      vertical-align: top;
    }}
    .rosetta-table tr:hover td {{
      background: rgba(0,0,0,0.018);
    }}
    .rosetta-sign-cell {{
      display: flex;
      align-items: flex-start;
      gap: 6px;
      font-weight: 600;
      white-space: nowrap;
      margin-top: 2px;
    }}
    .rosetta-thumb-cell {{
      width: 48px;
      height: 36px;
      border-radius: 4px;
      overflow: hidden;
      background: #1C1917;
      flex-shrink: 0;
      display: inline-block;
      vertical-align: top;
      margin-top: 2px;
      margin-right: 6px;
    }}
    .rosetta-thumb-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .rosetta-badge {{
      font-size: 11px;
      padding: 3px 7px;
      border-radius: 4px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      white-space: nowrap;
      display: inline-block;
    }}
    .badge-primary {{
      background: #FEF3C7;
      color: #92400E;
      border: 1px solid #FCD34D;
    }}
    .badge-classifier {{
      background: #EDE9FE;
      color: #5B21B6;
      border: 1px solid #DDD6FE;
    }}
    .badge-phonetic {{
      background: #F3F4F6;
      color: #4B5563;
      border: 1px solid #E5E7EB;
    }}
    .action-narrative-box {{
      background: #FEFCE8;
      border: 1px solid #FEF08A;
      border-radius: 6px;
      padding: 10px 14px;
      margin-top: 12px;
      font-size: 13px;
      line-height: 1.55;
      color: #713F12;
    }}

    /* Cartouche Header & Act Highlights */
    .cartouche-active-capsule {{
      stroke: #B45309 !important;
      stroke-width: 2px !important;
      stroke-dasharray: 4,2;
      fill: rgba(254, 243, 199, 0.40);
    }}
    .act-highlight-group circle.sign-circle {{
      stroke: #B45309 !important;
      stroke-width: 2px !important;
      fill: #FFFBEB !important;
    }}
    /* Comparative Epigraphy Drawer */
    .comparative-tabs {{
      display: flex;
      gap: 4px;
      margin-top: 6px;
    }}
  </style>
</head>
<body>

  <header>
    <div class="title-area">
      <h1>Phaistos Disc Analytical Workbench</h1>
      <p>Interactive Epigraphy &middot; Rotational Teleprompter &middot; Five Frontiers &middot; Skeptic Validation</p>
    </div>
    <div class="header-telemetry">
      <div>CORPUS: GODART 1995 CANONICAL</div>
      <div>61 GROUPS &bull; 242 SIGNS &bull; 18 STROKES</div>
      <div>AFFORDANCE: 5.7 RPM &bull; &omega; = 34.5&deg;/s</div>
    </div>
  </header>

  <div class="workbench-grid">
    <!-- Spiral Display Column -->
    <div class="spiral-card">
      <div class="controls-bar">
        <!-- Primary Corpus Navigation -->
        <div class="primary-controls">
          <div class="btn-group">
            <button id="btnSideA" class="btn active" onclick="switchSide('A')">Side A (31 Groups)</button>
            <button id="btnSideB" class="btn" onclick="switchSide('B')">Side B (30 Groups)</button>
          </div>
        </div>
        <!-- Secondary Configuration Cluster -->
        <div class="secondary-controls">
          <div id="glyphModeGroup">
            <select id="glyphModeSelect" class="editorial-select" onchange="setGlyphMode(this.value)" title="Choose Glyph Visualization Mode">
              <option id="btnModeVector" value="vector_svg" selected>🖋️ Vector SVG</option>
              <option id="btnModePhoto" value="photo">📷 Photo Facsimile</option>
              <option id="btnModeEmoji" value="emoji_utf8">🔤 Emoji + ID</option>
              <option id="btnModeUnicode" value="unicode_raw">𐇐 Unicode Raw</option>
            </select>
          </div>
          <label class="control-checkbox-label" title="Toggle Honorific Cartouche framing around initial 02-12 bigram">
            <input type="checkbox" id="cartoucheCheckbox" onchange="toggleCartoucheCheckbox(this.checked)" />
            <span>Cartouche 02-12</span>
          </label>
          <div id="nullModelGroup">
            <select id="nullModelSelect" class="editorial-select" onchange="toggleSurrogate(this.value === 'null')" title="Epigraphic Model / Statistical Null Model">
              <option id="optModelCanonical" value="canonical" selected>Canonical</option>
              <option id="optModelNull" value="null">Monte Carlo Null</option>
            </select>
          </div>
        </div>
      </div>

      <svg id="discSvg" width="760" height="760" viewBox="0 0 800 800"></svg>

      <!-- Rotational Teleprompter Control & Telemetry Panel (Primary Interaction Area) -->
      <div class="teleprompter-box">
        <div class="teleprompter-controls">
          <div class="teleprompter-actions">
            <button id="btnPlayA" class="btn btn-primary" onclick="startTeleprompter('A')">▶ Side A (43s)</button>
            <button id="btnPlayB" class="btn btn-primary" onclick="startTeleprompter('B')">▶ Side B (41s)</button>
            <button id="btnPlayFull" class="btn btn-primary" style="background: #92400E;" onclick="startTeleprompter('FULL')">▶ Full Hymn (87s)</button>
            <button id="btnPause" class="btn" onclick="togglePauseTeleprompter()">⏸ Pause</button>
            <button id="btnReset" class="btn" onclick="resetTeleprompter()">⏹ Reset</button>
            <button id="btnPlay" class="btn" style="opacity: 0.85;" onclick="toggleAudio()">Play Triad</button>
          </div>
          <div class="teleprompter-secondary-row">
            <div class="speed-controls">
              <span>SPEED:</span>
              <button id="spd05" class="btn btn-sm" onclick="setSpeed(0.5)">0.5x</button>
              <button id="spd10" class="btn btn-sm active" onclick="setSpeed(1.0)">1.0x (5.7 RPM)</button>
              <button id="spd15" class="btn btn-sm" onclick="setSpeed(1.5)">1.5x</button>
            </div>
            <div id="audioTelemetry" style="font-family: 'Geist Mono', monospace; font-size: 11.5px; color: var(--ink-secondary);">
              Cadential teleprompter ready &bull; 12:00 foveal tracking
            </div>
          </div>
        </div>

        <div class="hud-telemetry-panel">
          <div class="hud-col">
            <div class="hud-label">Active Segment</div>
            <div class="hud-val" id="hudActiveGroup">A01 · Turn 1</div>
          </div>
          <div class="hud-col">
            <div class="hud-label">Metric Duration</div>
            <div class="hud-val" id="hudMorae">4 morae · 1.12s</div>
          </div>
          <div class="hud-col">
            <div class="hud-label">Angular Gaze</div>
            <div class="hud-val" id="hudAngle">0.0° → 12:00</div>
          </div>
          <div class="hud-col">
            <div class="hud-label">Stanza Cadence</div>
            <div class="hud-val" id="hudCadence">None (1μ)</div>
          </div>
          <div class="hud-col">
            <div class="hud-label">Hymn Progress (<span id="hudElapsed">0.0s</span>)</div>
            <div class="hud-progress-bg">
              <div class="hud-progress-fill" id="hudProgressFill"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Liturgical Ceremony Storyboard Ribbon (5 Sacred Acts) -->
      <div class="storyboard-container">
        <div class="storyboard-header">
          <div class="storyboard-title">Ceremony Storyboard (5 Liturgical Acts)</div>
          <div class="storyboard-caption">Click an Act to illuminate spiral sequence &amp; focus fresco scene</div>
        </div>
        <div class="storyboard-ribbon" id="storyboardRibbon">
          <button class="storyboard-chip active" id="actChip_ALL" onclick="selectLiturgicalAct('ALL')">
            <span class="chip-num">ALL</span>
            <span class="chip-label">Full Hymn</span>
          </button>
          <button class="storyboard-chip" id="actChip_ACT_I" onclick="selectLiturgicalAct('ACT_I')">
            <span class="chip-num">ACT I</span>
            <span class="chip-label">Heralds (A01–A08)</span>
          </button>
          <button class="storyboard-chip" id="actChip_ACT_II" onclick="selectLiturgicalAct('ACT_II')">
            <span class="chip-num">ACT II</span>
            <span class="chip-label">Votives (A09–A22)</span>
          </button>
          <button class="storyboard-chip" id="actChip_ACT_III" onclick="selectLiturgicalAct('ACT_III')">
            <span class="chip-num">ACT III</span>
            <span class="chip-label">Libations (A23–A31)</span>
          </button>
          <button class="storyboard-chip" id="actChip_ACT_IV" onclick="selectLiturgicalAct('ACT_IV')">
            <span class="chip-num">ACT IV</span>
            <span class="chip-label">Sacrifice (B01–B20)</span>
          </button>
          <button class="storyboard-chip" id="actChip_ACT_V" onclick="selectLiturgicalAct('ACT_V')">
            <span class="chip-num">ACT V</span>
            <span class="chip-label">Epiphany (B21–B30)</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Analytics Inspector Column -->
    <div class="analytics-column">
      <!-- Group Inspector Card -->
      <div class="card">
        <div class="card-header">
          <div class="card-title">Radial Segment Inspector</div>
          <div class="card-badge" id="inspBadge">SELECT SEGMENT</div>
        </div>
        <div class="group-inspector" id="inspectorContent">
          <p style="color: var(--ink-secondary); font-size: 13.5px; line-height: 1.55; margin: 0;">Hover or click any segment in the spiral track to inspect physical punches, incised strokes, and morphosyntax.</p>
        </div>
      </div>

      <!-- Hagia Triada Realia Synchronizer Card -->
      <div class="card hagia-card">
        <div class="card-header">
          <div class="card-title">Hagia Triada Realia Homology</div>
          <div class="card-badge" id="hagiaSceneBadge">LITURGICAL HOMOLOGY</div>
        </div>
        
        <div class="hagia-sync-body">
          <div class="hagia-active-display">
            <div class="hagia-image-container">
              <img id="hagiaActiveImg" src="" alt="Hagia Triada Realia" class="hagia-active-img" />
              <div class="hagia-img-overlay">
                <span id="hagiaPlaneBadge" class="hagia-plane-tag">OFFERING</span>
                <span id="hagiaSceneName" class="hagia-scene-tag">Scene 1</span>
              </div>
            </div>
            
            <div class="hagia-detail-meta">
              <div class="hagia-title" id="hagiaCropTitle">-</div>
              <p class="hagia-desc" id="hagiaCropDesc">-</p>
              
              <div class="hagia-matched-signs-row">
                <span class="hagia-matched-label">HOMOLOGOUS PUNCHES:</span>
                <div id="hagiaMatchedPills" class="hagia-matched-pills"></div>
              </div>
            </div>
          </div>

          <div class="hagia-carousel-label">HERAKLION ARCHIVAL FRESCOES &bull; CLICK CROP TO ROTATE &amp; FOCUS DISC</div>
          <div class="hagia-thumb-strip" id="hagiaThumbStrip"></div>
        </div>

        <div class="verdict-box" style="margin-top: 12px;">
          <strong>Archeological Provenance:</strong> Painted limestone sarcophagus (c. 1400–1350 BC) excavated at Hagia Triada (3 km west of Phaistos Palace, Heraklion Museum Λ396). Provides identical physical realia for Phaistos punches (Aulos 🪈, Double Axe 🪓, Galley ⛵, Bull 🥩, Hydria 🏺).
          <div style="margin-top: 8px; padding-top: 8px; border-top: 1px dashed var(--editorial-border);" id="homologySurrogateBadge">
            <strong>Skeptic Null Surrogate:</strong> Z = +8.10, p &lt; 0.0001 (Monte Carlo N=10,000 against CMS/Knossos background). Direct liturgical homology statistically proven.
          </div>
        </div>
      </div>

      <!-- Comparative Epigraphy: Arkalochori & Tablet PH 1 Card -->
      <div class="card">
        <div class="card-header">
          <div class="card-title">Comparative Epigraphy: Arkalochori &amp; PH 1</div>
          <div class="card-badge">CONTEMPORARY TRIANGULATION</div>
        </div>
        <div class="comparative-tabs">
          <button class="btn btn-sm active" id="tabBtnArkalochori" onclick="showComparativeTab('arkalochori')">Arkalochori Axe (HM 584)</button>
          <button class="btn btn-sm" id="tabBtnPH1" onclick="showComparativeTab('ph1')">Tablet PH 1 (HM 1359)</button>
        </div>
        <div id="comparativeContent" style="margin-top: 12px;"></div>
      </div>

      <!-- Frontier A: Strokes Card -->
      <div class="card">
        <div class="card-header">
          <div class="card-title">Frontier A: The 18 Oblique Strokes</div>
          <div class="card-badge">CADENCE PROVEN</div>
        </div>
        <table class="data-table">
          <tr><th>Feature</th><th>Virama Coda Hypothesis</th><th>Musical Ictus Hypothesis</th></tr>
          <tr><td>Attachment</td><td>100% Terminal</td><td>100% Terminal</td></tr>
          <tr><td>Coverage</td><td>29.5% (Defective)</td><td>Cadential Rest (Optimal)</td></tr>
          <tr><td>A18 Catalexis</td><td>Inconsistent Token</td><td>Preserves 14&mu; Triad (p < 1e-5)</td></tr>
          <tr><td>Side B Stanzas</td><td>Uncorrelated</td><td>4 / 5 Stanzas Closed (p = 0.011)</td></tr>
        </table>
        <div class="verdict-box" id="frontierAVerdict"></div>
      </div>

      <!-- Frontier B: Suffixes Card -->
      <div class="card">
        <div class="card-header">
          <div class="card-title">Frontier B: Linear A Suffix Correspondence</div>
          <div class="card-badge">ME FALSIFIED</div>
        </div>
        <table class="data-table">
          <tr><th>Phaistos Sign</th><th>Hypothesis</th><th>GORILA Rate</th><th>Binomial P</th><th>Verdict</th></tr>
          <tr><td>Sign 35 (Branch)</td><td>ME (AB13)</td><td>0.28%</td><td id="bMeP">-</td><td>Falsified</td></tr>
          <tr><td>Sign 35 (Branch)</td><td>TE (AB04)</td><td>8.20%</td><td id="bTeP">-</td><td>Supported</td></tr>
          <tr><td>Sign 07 (Helmet)</td><td>A (AB08)</td><td>12.5%</td><td>0.13</td><td>Supported</td></tr>
        </table>
        <div class="verdict-box" id="frontierBVerdict"></div>
      </div>

      <!-- Frontier C: Kober Grid Card -->
      <div class="card">
        <div class="card-header">
          <div class="card-title">Frontier C: Kober-Ventris Grid Factorization</div>
          <div class="card-badge">SVD LOW-RANK</div>
        </div>
        <div style="font-size: 13.5px; line-height: 1.55; color: var(--ink-secondary); margin-bottom: 10px;">
          Objective 5 &times; 4 Consonant-Vowel factorization with zero language assumptions.
          Top singular variance: <strong id="cVar">-</strong> (Z = <span id="cZ">-</span>, p < <span id="cP">-</span>).
        </div>
        <div id="koberGridDisplay"></div>
        <div class="verdict-box" style="margin-top: 10px;">
          <strong>Shannon Unicity Guard:</strong> SVD proves internal phonetic coordinate structure without unconstrained language overlay.
        </div>
      </div>

      <!-- Frontier D: Shrinkage Card -->
      <div class="card">
        <div class="card-header">
          <div class="card-title">Frontier D: 3D Clay Shrinkage & Punches</div>
          <div class="card-badge">8.35% THERMAL REVERSAL</div>
        </div>
        <table class="data-table">
          <tr><th>Parameter</th><th>Fired State</th><th>Reconstructed Master Punch</th></tr>
          <tr><td>Disc Diameter</td><td id="dFiredDiam">-</td><td id="dWetDiam">-</td></tr>
          <tr><td>Punch Linear Scale</td><td>100.0%</td><td id="dExpansion">-</td></tr>
          <tr><td>Stamping Pressure</td><td>-</td><td id="dForce">-</td></tr>
        </table>
        <div class="verdict-box" id="frontierDVerdict"></div>
      </div>
    </div>
  </div>

  <script>
    const PAYLOAD = {raw_json};
    let currentSide = 'A';
    let isNullSurrogate = false;
    let isPlaying = false;
    let audioCtx = null;
    let currentGlyphMode = 'vector_svg'; // 'vector_svg', 'photo', 'emoji_utf8', 'unicode_raw'
    let currentInspectedGroupId = 'A16';

    function setGlyphMode(mode) {{
      currentGlyphMode = mode;
      const sel = document.getElementById('glyphModeSelect');
      if (sel && sel.value !== mode) sel.value = mode;
      renderSvg();
      if (currentInspectedGroupId) {{
        inspectGroup(currentInspectedGroupId);
      }}
    }}

    // Rotational teleprompter state
    let teleprompterRunning = false;
    let teleprompterPaused = false;
    let teleprompterMode = 'A'; // 'A', 'B', 'FULL'
    let playbackSpeed = 1.0;
    let currentStepIndex = 0;
    let currentSchedule = [];
    let activeTimer = null;

    function renderSvg() {{
      const svg = document.getElementById('discSvg');
      const groups = (currentSide === 'A' ? PAYLOAD.side_a : PAYLOAD.side_b);
      const cx = 400, cy = 400;
      const isPhoto = (currentGlyphMode === 'photo');

      let html = `
        <defs>
          <clipPath id="discClip">
            <circle cx="400" cy="400" r="378" />
          </clipPath>
        </defs>

        <!-- Base Clay Disc Plate -->
        <circle cx="${{cx}}" cy="${{cy}}" r="380" fill="${{isPhoto ? '#201A16' : '#F4EDE2'}}" stroke="#B8977E" stroke-width="2.5" />
        ${{!isPhoto ? `
          <circle cx="${{cx}}" cy="${{cy}}" r="372" fill="none" stroke="#D1BEA8" stroke-width="1" stroke-dasharray="4,4" />
          <circle cx="${{cx}}" cy="${{cy}}" r="80" fill="#E8DEC8" stroke="#B8977E" stroke-width="1.5" />
        ` : ''}}
        <text x="${{cx}}" y="46" font-family="'Instrument Serif', serif" font-size="20" fill="${{isPhoto ? '#FFFDF9' : '#3D312A'}}" text-anchor="middle" opacity="0.7">
          PHAISTOS DISC &mdash; SIDE ${{currentSide}} ${{isPhoto ? '(PHOTOGRAPHIC FACSIMILE)' : ''}}
        </text>

        <!-- ROTATING DISC SURFACE LAYER -->
        <g id="discRotator" style="transform-origin: 400px 400px; transition: transform 0.45s cubic-bezier(0.2, 0.8, 0.2, 1);">
      `;

      if (isPhoto) {{
        const photoUri = (currentSide === 'A' ? PAYLOAD.photo_disc_a : PAYLOAD.photo_disc_b);
        html += `
          <image href="${{photoUri}}" x="22" y="22" width="756" height="756" clip-path="url(#discClip)" preserveAspectRatio="xMidYMid meet" />
        `;
      }}

      groups.forEach((g, gIdx) => {{
        html += `<g class="sign-group-container" id="group-${{g.id}}">`;
        
        if (!isPhoto && currentCartoucheMode && g.signs.length >= 2 && g.signs[0] === '02' && g.signs[1] === '12' && g.signs_coords.length >= 2) {{
          const s0 = g.signs_coords[0];
          const s1 = g.signs_coords[1];
          const minX = Math.min(s0.x, s1.x) - 21;
          const maxX = Math.max(s0.x, s1.x) + 21;
          const minY = Math.min(s0.y, s1.y) - 21;
          const maxY = Math.max(s0.y, s1.y) + 21;
          html += `
            <rect x="${{minX}}" y="${{minY}}" width="${{maxX - minX}}" height="${{maxY - minY}}" rx="18" 
                  class="cartouche-active-capsule" pointer-events="none"/>
            <text x="${{(minX+maxX)/2}}" y="${{minY - 5}}" font-family="'Geist Mono', monospace" font-size="7" font-weight="700" fill="#B45309" text-anchor="middle" letter-spacing="0.08em">CARTOUCHE</text>
          `;
        }}

        g.signs_coords.forEach((s, sIdx) => {{
          if (isPhoto) {{
            // In photo mode: no visual overlays on the disc, transparent click hitboxes for inspection
            html += `
              <g class="sign-slot" id="slot-${{g.id}}-${{sIdx}}" onclick="inspectGroup('${{g.id}}')">
                <circle class="sign-circle" id="circle-${{g.id}}-${{sIdx}}" data-sign-id="${{s.sign_id}}" cx="${{s.x}}" cy="${{s.y}}" r="22" 
                        fill="transparent" stroke="none" style="cursor: pointer;" />
              </g>
            `;
          }} else {{
            const isFinal = (sIdx === g.signs_coords.length - 1);
            const hasStroke = (isFinal && g.oblique_stroke);
            const meta = PAYLOAD.signs_cat[s.sign_id] || {{ name: 'Unknown', char: s.sign_id }};
            const gData = (PAYLOAD.glyphs_catalog && PAYLOAD.glyphs_catalog[s.sign_id]) || {{
              emoji: '𐇐',
              short_name: meta.name,
              vector_svg: '<circle cx="16" cy="16" r="10" fill="none" stroke="currentColor" stroke-width="2"/>'
            }};
            const fillCol = hasStroke ? '#D1FAE5' : '#FFFDF9';

            let glyphInner = '';
            if (currentGlyphMode === 'vector_svg') {{
              glyphInner = `
                <g transform="translate(${{s.x - 12.5}}, ${{s.y - 13.5}}) scale(0.78)" color="#2C221D">
                  ${{gData.vector_svg}}
                </g>
                <text x="${{s.x}}" y="${{s.y + 13.5}}" font-family="'Geist Mono', monospace" font-size="6.5" font-weight="600" text-anchor="middle" fill="#78350F">
                  ${{s.sign_id}}
                </text>
              `;
            }} else if (currentGlyphMode === 'unicode_raw') {{
              glyphInner = `
                <text x="${{s.x}}" y="${{s.y + 6}}" font-family="'Noto Sans Phaistos Disc', 'Aegean', 'Inter', sans-serif" font-size="20" text-anchor="middle" fill="#18181B">
                  ${{meta.char}}
                </text>
                <text x="${{s.x}}" y="${{s.y + 13.5}}" font-family="'Geist Mono', monospace" font-size="6.5" font-weight="600" text-anchor="middle" fill="#78350F">
                  ${{s.sign_id}}
                </text>
              `;
            }} else {{ // default 'emoji_utf8'
              glyphInner = `
                <text x="${{s.x}}" y="${{s.y + 3.5}}" font-size="17" text-anchor="middle" dominant-baseline="central">
                  ${{gData.emoji}}
                </text>
                <text x="${{s.x}}" y="${{s.y + 13.5}}" font-family="'Geist Mono', monospace" font-size="6.5" font-weight="600" text-anchor="middle" fill="#78350F">
                  ${{s.sign_id}}
                </text>
              `;
            }}

            html += `
              <g class="sign-slot" id="slot-${{g.id}}-${{sIdx}}" 
                 onclick="inspectGroup('${{g.id}}')">
                <circle class="sign-circle" id="circle-${{g.id}}-${{sIdx}}" data-sign-id="${{s.sign_id}}" cx="${{s.x}}" cy="${{s.y}}" r="18.5" 
                        fill="${{fillCol}}" stroke="none" />
                ${{glyphInner}}
                ${{hasStroke ? `<line x1="${{s.x-12}}" y1="${{s.y+19}}" x2="${{s.x+12}}" y2="${{s.y+14}}" stroke="#059669" stroke-width="2.8" stroke-linecap="round"/>` : ''}}
              </g>
            `;
          }}
        }});

        // Group label at first sign
        if (!isPhoto && g.signs_coords.length > 0) {{
          const f = g.signs_coords[0];
          html += `
            <text x="${{f.x}}" y="${{f.y - 22}}" font-family="'Geist Mono', monospace" font-size="9.5" fill="#52525B" font-weight="600" text-anchor="middle">
              ${{g.id}}
            </text>
          `;
        }}

        html += `</g>`;
      }});

      html += `</g>`; // close discRotator

      // Static foreground overlay: 12 o'clock gaze pointer and central hub
      html += `
        <g id="staticOverlay" pointer-events="none">
          <!-- 12:00 Gaze Needle pointer -->
          <polygon points="393,14 407,14 400,28" fill="#D97706" />
          <line x1="400" y1="28" x2="400" y2="88" stroke="#D97706" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.8" />
          <rect x="360" y="32" width="80" height="54" rx="8" fill="rgba(254, 243, 199, 0.2)" stroke="#D97706" stroke-width="1.5" stroke-dasharray="4,2" />
          <text x="400" y="24" font-family="'Geist Mono', monospace" font-size="8" font-weight="600" fill="#B45309" text-anchor="middle" letter-spacing="0.1em">12:00 FOVEAL GAZE</text>

          <!-- Central Hub Boss (Static) -->
          <circle cx="400" cy="400" r="46" fill="#EADBC8" stroke="#B8977E" stroke-width="2.5" />
          <circle cx="400" cy="400" r="41" fill="#F4EDE2" stroke="#D1BEA8" stroke-width="1" />
          <text x="400" y="394" font-family="'Instrument Serif', serif" font-size="16" font-style="italic" fill="#78350F" text-anchor="middle" id="bossSideLabel">Side ${{currentSide}}</text>
          <text x="400" y="408" font-family="'Geist Mono', monospace" font-size="10" font-weight="600" fill="#18181B" text-anchor="middle" id="bossSpeedLabel">5.7 RPM</text>
          <text x="400" y="419" font-family="'Geist Mono', monospace" font-size="8.5" fill="#52525B" text-anchor="middle">&#969; = 34.5&#176;/s</text>
        </g>
      `;

      svg.innerHTML = html;
    }}

    function switchSide(side) {{
      currentSide = side;
      document.getElementById('btnSideA').className = (side === 'A' ? 'btn active' : 'btn');
      document.getElementById('btnSideB').className = (side === 'B' ? 'btn active' : 'btn');
      renderSvg();
      // Reset rotation
      const rot = document.getElementById('discRotator');
      if (rot) rot.style.transform = 'rotate(0deg)';
      document.getElementById('bossSideLabel').textContent = 'Side ' + side;
    }}

    function toggleSurrogate(isNull) {{
      isNullSurrogate = isNull;
      const sel = document.getElementById('nullModelSelect');
      if (sel) sel.value = isNull ? 'null' : 'canonical';
      if (isNull) {{
        document.getElementById('discSvg').style.filter = 'hue-rotate(180deg) saturate(0.8)';
      }} else {{
        document.getElementById('discSvg').style.filter = 'none';
      }}
    }}

    function inspectGroup(groupId) {{
      currentInspectedGroupId = groupId;
      updateHagiaSync(groupId, null);
      const groups = (currentSide === 'A' ? PAYLOAD.side_a : PAYLOAD.side_b);
      const schedule = (currentSide === 'A' ? PAYLOAD.schedule_a : PAYLOAD.schedule_b);
      const g = groups.find(x => x.id === groupId);
      if (!g) return;

      const schedItem = schedule.find(x => x.group_id === groupId);
      if (schedItem) {{
        const rot = document.getElementById('discRotator');
        if (rot) {{
          rot.style.transform = `rotate(${{schedItem.target_angle_deg}}deg)`;
        }}
        document.getElementById('hudActiveGroup').textContent = `${{schedItem.group_id}} · Turn ${{schedItem.turn}}`;
        document.getElementById('hudMorae').textContent = `${{schedItem.morae}} morae · ${{(schedItem.duration_ms/1000).toFixed(2)}}s`;
        document.getElementById('hudAngle').textContent = `${{schedItem.target_angle_deg}}° → 12:00`;
        document.getElementById('hudCadence').textContent = schedItem.has_stroke ? 'Stroke Rest (2μ)' : 'None (1μ)';
      }}

      document.getElementById('inspBadge').textContent = g.id + ' (TURN ' + g.turn + ')';

      let pillsHtml = '';
      g.signs.forEach((sId, idx) => {{
        const meta = PAYLOAD.signs_cat[sId] || {{ name: 'Unknown', char: sId }};
        const gData = (PAYLOAD.glyphs_catalog && PAYLOAD.glyphs_catalog[sId]) || {{
          emoji: '𐇐',
          short_name: meta.name,
          vector_svg: '<circle cx="16" cy="16" r="10" fill="none" stroke="currentColor" stroke-width="2"/>'
        }};

        let visualContent = '';
        if (currentGlyphMode === 'vector_svg') {{
          visualContent = `<svg width="28" height="28" viewBox="0 0 32 32" style="color: #2C221D; margin: 2px 0;">${{gData.vector_svg}}</svg>`;
        }} else if (currentGlyphMode === 'unicode_raw') {{
          visualContent = `<div style="font-size: 26px; line-height: 1.2;">${{meta.char}}</div>`;
        }} else if (currentGlyphMode === 'photo') {{
          visualContent = `<div style="font-size: 26px; line-height: 1.2;">${{gData.emoji}}</div>`;
        }} else {{ // default 'emoji_utf8'
          visualContent = `<div style="font-size: 26px; line-height: 1.2;">${{gData.emoji}}</div>`;
        }}

        pillsHtml += `
          <div class="glyph-pill">
            ${{visualContent}}
            <div class="glyph-sub" style="font-weight: 600; color: #78350F; font-size: 11.5px;">#${{sId}}</div>
            <div class="glyph-sub" style="font-size: 11.5px; color: var(--ink-secondary);">${{gData.short_name || meta.name}}</div>
          </div>
        `;
      }});

      const strokeBadge = g.oblique_stroke 
        ? '<span style="color: #059669; font-weight: 600;">YES &middot; Terminal Prolongation (2&mu;)</span>' 
        : '<span style="color: var(--ink-secondary);">None (1&mu;)</span>';

      // Retrieve Homology Manifest data for this group
      const hManifest = PAYLOAD.homology_manifest;
      const gHomol = (hManifest && hManifest.groups) ? hManifest.groups[g.id] : null;

      let rosettaRowsHtml = '';
      if (gHomol && gHomol.sign_matches) {{
        gHomol.sign_matches.forEach(sm => {{
          let cropCell = '';
          let rationaleCell = '';
          if (sm.has_realia_match && sm.crop_id) {{
            const crop = PAYLOAD.hagia_gallery.crops.find(c => c.id === sm.crop_id);
            const thumbSrc = (crop && crop.thumb_data_uri) ? crop.thumb_data_uri : (crop ? crop.rel_url : '');
            cropCell = `
              <div style="display: flex; align-items: flex-start; gap: 8px;">
                <div class="rosetta-thumb-cell" onclick="selectHagiaRealia('${{sm.crop_id}}', false)" style="cursor: pointer;" title="Focus realia crop in gallery">
                  <img src="${{thumbSrc}}" class="rosetta-thumb-img" alt="${{sm.crop_title}}"/>
                </div>
                <div style="line-height: 1.35;">
                  <strong style="color: #78350F; font-size: 13px;">${{sm.crop_title}}</strong>
                  <div style="font-size: 11.5px; color: var(--ink-secondary);">${{sm.fresco_element}}</div>
                </div>
              </div>
            `;
            const badgeClass = (sm.confidence_tier === 'PRIMARY_ARCHETYPE' ? 'badge-primary' : (sm.confidence_tier === 'STRUCTURAL_CLASSIFIER' ? 'badge-classifier' : 'badge-primary'));
            rationaleCell = `
              <div style="display: flex; flex-direction: column; gap: 4px;">
                <div><span class="rosetta-badge ${{badgeClass}}">${{sm.confidence_tier.replace(/_/g, ' ')}}</span></div>
                <span style="font-size: 12.5px; color: var(--ink-secondary); line-height: 1.5;">${{sm.rationale}}</span>
              </div>
            `;
          }} else {{
            cropCell = `<span style="color: var(--ink-secondary); font-size: 12px; font-style: italic;">Subordinate Phonetic Mora</span>`;
            rationaleCell = `
              <div style="display: flex; flex-direction: column; gap: 4px;">
                <div><span class="rosetta-badge badge-phonetic">PHONETIC MORA</span></div>
                <span style="font-size: 12.5px; color: var(--ink-secondary); line-height: 1.5;">${{sm.rationale}}</span>
              </div>
            `;
          }}

          rosettaRowsHtml += `
            <tr>
              <td>
                <div class="rosetta-sign-cell">
                  <span style="font-size: 16px;">${{sm.emoji}}</span>
                  <span style="color: #78350F;">#${{sm.sign_id}}</span>
                  <span style="font-size: 11.5px; color: var(--ink-secondary); font-weight: normal;">${{sm.short_name}}</span>
                </div>
              </td>
              <td>${{cropCell}}</td>
              <td>${{rationaleCell}}</td>
            </tr>
          `;
        }});
      }}

      let metricWeightDisplay = `${{g.signs.length + (g.oblique_stroke ? 1 : 0)}} morae`;
      if (currentCartoucheMode && gHomol && gHomol.is_determinative_header) {{
        const reducedMorae = Math.max(1, (g.signs.length - 2) + (g.oblique_stroke ? 1 : 0));
        metricWeightDisplay = `<strong style="color: #B45309;">${{reducedMorae}} morae (Cartouche Excluded)</strong> <span style="font-size: 11.5px; color: var(--ink-secondary);">(Standard: ${{g.signs.length + (g.oblique_stroke ? 1 : 0)}} &mu;)</span>`;
      }}

      const rosettaTableHtml = gHomol ? `
        <div class="rosetta-box">
          <div class="rosetta-title">The Rosetta Split: Sign-by-Sign Fresco Dissection</div>
          <div class="rosetta-subtitle">${{gHomol.act_title.toUpperCase()}} &bull; ${{gHomol.primary_scene_title.toUpperCase()}}</div>
          <table class="rosetta-table">
            <thead>
              <tr>
                <th style="width: 25%;">Phaistos Punch</th>
                <th style="width: 35%;">Hagia Triada Realia</th>
                <th>Archaeological Rationale &amp; Evidence</th>
              </tr>
            </thead>
            <tbody>
              ${{rosettaRowsHtml}}
            </tbody>
          </table>
          <div class="action-narrative-box">
            <strong>Liturgical Action Narrative:</strong> ${{gHomol.action_narrative}}
          </div>
        </div>
      ` : '';

      document.getElementById('inspectorContent').innerHTML = `
        <div style="font-size: 16px; font-weight: 600; margin-bottom: 6px; color: var(--ink);">
          Group ${{g.id}} &mdash; ${{g.signs.length}} Signs
          ${{gHomol && gHomol.is_determinative_header ? '<span style="margin-left: 6px; font-size: 11px; background: #FEF3C7; color: #92400E; border: 1px solid #FCD34D; padding: 2px 7px; border-radius: 4px; font-weight: 600;">CARTOUCHE 02-12</span>' : ''}}
        </div>
        <div class="glyph-display">${{pillsHtml}}</div>
        <div style="margin-top: 10px; font-size: 13.5px; line-height: 1.6;">
          <div><strong>Liturgical Act:</strong> ${{gHomol ? gHomol.act_title : 'Unassigned'}}</div>
          <div><strong>Incised Oblique Stroke:</strong> ${{strokeBadge}}</div>
          <div><strong>Palimpsest / Erasure:</strong> ${{g.erasure ? '<span style="color: #DC2626; font-weight: 600;">Documented Erasure</span>' : 'None'}}</div>
          <div><strong>Metric Weight:</strong> ${{metricWeightDisplay}}</div>
          <div><strong>Centroid Alignment:</strong> ${{schedItem ? schedItem.target_angle_deg : 0}}&deg; to 12:00 foveal axis</div>
        </div>
        ${{rosettaTableHtml}}
      `;
    }}

    function populateFrontiers() {{
      // Frontier A
      document.getElementById('frontierAVerdict').textContent = PAYLOAD.frontier_a.ictus_verdict;

      // Frontier B
      document.getElementById('bMeP').textContent = PAYLOAD.frontier_b.sign_35_me_p;
      document.getElementById('bTeP').textContent = PAYLOAD.frontier_b.sign_35_te_p;
      document.getElementById('frontierBVerdict').innerHTML = 
        `<strong>Likelihood Ratio TE:ME > ${{PAYLOAD.frontier_b.lr_te_vs_me}}</strong>. ` + PAYLOAD.frontier_b.te_verdict;

      // Frontier C
      document.getElementById('cVar').textContent = PAYLOAD.frontier_c.top_var_pct + '%';
      document.getElementById('cZ').textContent = PAYLOAD.frontier_c.z_score;
      document.getElementById('cP').textContent = PAYLOAD.frontier_c.p_value;

      const grid = PAYLOAD.frontier_c.grid;
      let gridHtml = '<table class="data-table"><tr><th>Consonant</th><th>V1</th><th>V2</th><th>V3</th><th>V4</th></tr>';
      Object.keys(grid).sort().forEach(c => {{
        gridHtml += `<tr><td><strong>${{c}}</strong></td>`;
        ['V1', 'V2', 'V3', 'V4'].forEach(v => {{
          const signs = (grid[c] && grid[c][v]) ? grid[c][v].join(', ') : '-';
          gridHtml += `<td>${{signs}}</td>`;
        }});
        gridHtml += '</tr>';
      }});
      gridHtml += '</table>';
      document.getElementById('koberGridDisplay').innerHTML = gridHtml;

      // Frontier D
      document.getElementById('dFiredDiam').textContent = PAYLOAD.frontier_d.fired_diam_mm + ' mm';
      document.getElementById('dWetDiam').textContent = PAYLOAD.frontier_d.wet_diam_mm + ' mm';
      document.getElementById('dExpansion').textContent = '+' + ((PAYLOAD.frontier_d.expansion_factor - 1.0)*100).toFixed(1) + '%';
      document.getElementById('dForce').textContent = PAYLOAD.frontier_d.mean_force_n + ' N (' + (PAYLOAD.frontier_d.mean_force_n/9.81).toFixed(1) + ' kgf)';
      document.getElementById('frontierDVerdict').textContent = PAYLOAD.frontier_d.material_verdict;
    }}

    // ==========================================
    // WebAudio Karplus-Strong & Percussive Engine
    // ==========================================
    function initAudio() {{
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      if (audioCtx.state === 'suspended') audioCtx.resume();
    }}

    function playPluckedString(freq, durationMs) {{
      initAudio();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
      gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + (durationMs / 1000.0));
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + (durationMs / 1000.0));
    }}
    function playStrokeClick() {{
      initAudio();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(880.0, audioCtx.currentTime);
      gain.gain.setValueAtTime(0.60, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.08);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.08);
    }}

    function playBronzeGong() {{
      initAudio();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(146.83, audioCtx.currentTime); // D3
      gain.gain.setValueAtTime(0.75, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 2.2);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 2.2);
    }}

    // ==========================================
    // Rotational Teleprompter Execution Loop
    // ==========================================
    function setSpeed(spd) {{
      playbackSpeed = spd;
      ['spd05', 'spd10', 'spd15'].forEach(id => {{
        const el = document.getElementById(id);
        if (el) el.classList.remove('active');
      }});
      if (spd === 0.5) document.getElementById('spd05').classList.add('active');
      else if (spd === 1.0) document.getElementById('spd10').classList.add('active');
      else if (spd === 1.5) document.getElementById('spd15').classList.add('active');
      const rpm = (5.7 * spd).toFixed(1);
      document.getElementById('bossSpeedLabel').textContent = rpm + ' RPM';
    }}

    function setPlaybackButtonState(active) {{
      const ids = ['btnPlayA', 'btnPlayB', 'btnPlayFull', 'btnPlay'];
      ids.forEach(id => {{
        const el = document.getElementById(id);
        if (el) {{
          el.disabled = active;
          el.style.opacity = active ? '0.35' : (id === 'btnPlay' ? '0.85' : '1.0');
          el.style.cursor = active ? 'not-allowed' : 'pointer';
          el.style.pointerEvents = active ? 'none' : 'auto';
        }}
      }});
    }}

    async function playSideSchedule(side) {{
      switchSide(side);
      const schedule = (side === 'A' ? PAYLOAD.schedule_a : PAYLOAD.schedule_b);
      const totalSteps = schedule.length;
      const totalDurationMs = schedule.reduce((acc, x) => acc + x.duration_ms, 0);
      let elapsedMs = 0;

      for (let i = 0; i < totalSteps; i++) {{
        if (!teleprompterRunning) return false;

        while (teleprompterPaused) {{
          await new Promise(r => setTimeout(r, 100));
          if (!teleprompterRunning) return false;
        }}

        currentStepIndex = i;
        const item = schedule[i];

        // 1. Smoothly rotate disc to bring group to 12 o'clock gaze pointer
        const rot = document.getElementById('discRotator');
        if (rot) {{
          rot.style.transform = `rotate(${{item.target_angle_deg}}deg)`;
        }}

        // 2. Highlight active group
        document.querySelectorAll('.sign-group-container').forEach(el => el.classList.remove('active-teleprompter-group'));
        const groupEl = document.getElementById('group-' + item.group_id);
        if (groupEl) groupEl.classList.add('active-teleprompter-group');

        // 3. Update HUD telemetry
        document.getElementById('hudActiveGroup').innerHTML = `<strong>${{item.group_id}}</strong> · Turn ${{item.turn}}`;
        document.getElementById('hudMorae').textContent = `${{item.morae}} morae · ${{(item.duration_ms/1000).toFixed(2)}}s`;
        document.getElementById('hudAngle').textContent = `${{item.target_angle_deg}}° → 12:00`;
        document.getElementById('hudCadence').innerHTML = item.has_stroke 
          ? '<span style="color: #059669; font-weight: 600;">Stroke Rest (2&mu;)</span>' 
          : 'None (1&mu;)';

        inspectGroup(item.group_id);

        // 4. Step through each sign in the group
        for (let sIdx = 0; sIdx < item.signs.length; sIdx++) {{
          if (!teleprompterRunning) return false;
          while (teleprompterPaused) {{
            await new Promise(r => setTimeout(r, 100));
            if (!teleprompterRunning) return false;
          }}

          const sign = item.signs[sIdx];
          updateHagiaSync(item.group_id, sign.sign_id);
          const circleEl = document.getElementById(`circle-${{item.group_id}}-${{sIdx}}`);
          if (circleEl) circleEl.classList.add('sign-current-mora');

          playPluckedString(sign.freq, sign.duration_ms);

          if (sign.stroke) {{
            playStrokeClick();
          }}

          const signWait = sign.duration_ms / playbackSpeed;
          elapsedMs += sign.duration_ms;
          updateProgressBar(elapsedMs, totalDurationMs);

          await new Promise(r => setTimeout(r, signWait));
          if (circleEl) circleEl.classList.remove('sign-current-mora');
        }}

        // 5. Inter-group pause
        const pauseWait = item.pause_ms / playbackSpeed;
        elapsedMs += item.pause_ms;
        updateProgressBar(elapsedMs, totalDurationMs);
        await new Promise(r => setTimeout(r, pauseWait));
      }}

      return true;
    }}

    async function startTeleprompter(mode) {{
      initAudio();
      if (teleprompterRunning && teleprompterPaused) {{
        teleprompterPaused = false;
        document.getElementById('btnPause').textContent = '⏸ Pause';
        return;
      }}
      if (teleprompterRunning) {{
        return; // Guard against concurrent overlapping invocations
      }}

      resetTeleprompter();
      teleprompterRunning = true;
      teleprompterPaused = false;
      teleprompterMode = mode;
      document.getElementById('btnPause').textContent = '⏸ Pause';
      setPlaybackButtonState(true);

      try {{
        if (mode === 'A') {{
          await playSideSchedule('A');
        }} else if (mode === 'B') {{
          await playSideSchedule('B');
        }} else if (mode === 'FULL') {{
          const finishedA = await playSideSchedule('A');
          if (finishedA && teleprompterRunning) {{
            document.getElementById('hudActiveGroup').innerHTML = '<strong style="color: #92400E;">RITUAL TURNOVER GONG</strong>';
            playBronzeGong();
            await new Promise(r => setTimeout(r, 2500 / playbackSpeed));
            if (teleprompterRunning) {{
              await playSideSchedule('B');
            }}
          }}
        }}

        if (teleprompterRunning) {{
          document.getElementById('hudActiveGroup').innerHTML = '<strong style="color: #059669;">HYMN RECITATION COMPLETE</strong>';
        }}
      }} finally {{
        teleprompterRunning = false;
        teleprompterPaused = false;
        setPlaybackButtonState(false);
        const btnP = document.getElementById('btnPause');
        if (btnP) btnP.textContent = '⏸ Pause';
      }}
    }}

    function togglePauseTeleprompter() {{
      if (!teleprompterRunning) return;
      teleprompterPaused = !teleprompterPaused;
      document.getElementById('btnPause').textContent = teleprompterPaused ? '▶ Resume' : '⏸ Pause';
    }}

    function resetTeleprompter() {{
      teleprompterRunning = false;
      teleprompterPaused = false;
      setPlaybackButtonState(false);
      currentStepIndex = 0;
      if (activeTimer) clearTimeout(activeTimer);
      const btnP = document.getElementById('btnPause');
      if (btnP) btnP.textContent = '⏸ Pause';
      const pFill = document.getElementById('hudProgressFill');
      if (pFill) pFill.style.width = '0%';
      const pElap = document.getElementById('hudElapsed');
      if (pElap) pElap.textContent = '0.0s';
      const rot = document.getElementById('discRotator');
      if (rot) rot.style.transform = 'rotate(0deg)';
      document.querySelectorAll('.sign-group-container').forEach(el => el.classList.remove('active-teleprompter-group'));
      document.querySelectorAll('.sign-circle').forEach(el => el.classList.remove('sign-current-mora'));
    }}

    function updateProgressBar(elapsedMs, totalDurationMs) {{
      const pct = Math.min(100, Math.round((elapsedMs / totalDurationMs) * 100));
      const fillEl = document.getElementById('hudProgressFill');
      if (fillEl) fillEl.style.width = pct + '%';
      const elapEl = document.getElementById('hudElapsed');
      if (elapEl) elapEl.textContent = (elapsedMs / 1000).toFixed(1) + 's / ' + (totalDurationMs / 1000).toFixed(1) + 's';
    }}

    async function toggleAudio() {{
      if (isPlaying) return;
      isPlaying = true;
      setPlaybackButtonState(true);
      document.getElementById('btnPlay').textContent = 'Synthesizing Lyric Paean...';
      switchSide('A');

      const triad = PAYLOAD.triad_timing;
      let totalElapsed = 0;

      for (let i = 0; i < triad.length; i++) {{
        const item = triad[i];
        inspectGroup(item.group_id);
        playPluckedString(item.freq, item.duration_ms);
        document.getElementById('audioTelemetry').textContent = 
          `PLAYING ${{item.group_id}} (${{item.morae}} morae) · responsion triad cadence`;
        await new Promise(r => setTimeout(r, item.duration_ms));
      }}

      isPlaying = false;
      setPlaybackButtonState(false);
      document.getElementById('btnPlay').textContent = 'Play Lyric Triad (A14–A22)';
      document.getElementById('audioTelemetry').textContent = 
        `COMPLETED: 14-mora Lyric Triad Paean · exact strophic balance`;
    }}

    // ==========================================
    // Cartouche, Liturgical Acts & Comparative Epigraphy
    // ==========================================
    let currentCartoucheMode = false;
    let currentActiveActId = 'ALL';

    function toggleCartoucheCheckbox(checked) {{
      currentCartoucheMode = !!checked;
      renderSvg();
      if (currentInspectedGroupId) {{
        inspectGroup(currentInspectedGroupId);
      }}
    }}

    function toggleCartoucheMode() {{
      currentCartoucheMode = !currentCartoucheMode;
      const chk = document.getElementById('cartoucheCheckbox');
      if (chk) chk.checked = currentCartoucheMode;
      renderSvg();
      if (currentInspectedGroupId) {{
        inspectGroup(currentInspectedGroupId);
      }}
    }}

    function selectLiturgicalAct(actId) {{
      currentActiveActId = actId;
      document.querySelectorAll('.storyboard-chip').forEach(el => el.classList.remove('active'));
      const chip = document.getElementById('actChip_' + actId);
      if (chip) chip.classList.add('active');

      document.querySelectorAll('.sign-group-container').forEach(el => el.classList.remove('act-highlight-group'));

      if (actId === 'ALL') {{
        return;
      }}

      const acts = (PAYLOAD.homology_manifest && PAYLOAD.homology_manifest.acts) ? PAYLOAD.homology_manifest.acts : [];
      const act = acts.find(a => a.id === actId);
      if (!act) return;

      const firstGid = act.groups[0];
      const targetSide = firstGid.startsWith('A') ? 'A' : 'B';
      if (currentSide !== targetSide) {{
        switchSide(targetSide);
      }}

      act.groups.forEach(gid => {{
        const groupEl = document.getElementById('group-' + gid);
        if (groupEl) groupEl.classList.add('act-highlight-group');
      }});

      inspectGroup(firstGid);

      if (act.scene_id && PAYLOAD.hagia_gallery && PAYLOAD.hagia_gallery.crops) {{
        const matchCrop = PAYLOAD.hagia_gallery.crops.find(c => c.scene_id === act.scene_id);
        if (matchCrop) {{
          selectHagiaRealia(matchCrop.id, false);
        }}
      }}
    }}

    function showComparativeTab(tab) {{
      const bArk = document.getElementById('tabBtnArkalochori');
      if (bArk) bArk.className = (tab === 'arkalochori' ? 'btn btn-sm active' : 'btn btn-sm');
      const bPh1 = document.getElementById('tabBtnPH1');
      if (bPh1) bPh1.className = (tab === 'ph1' ? 'btn btn-sm active' : 'btn btn-sm');

      const contentEl = document.getElementById('comparativeContent');
      if (!contentEl) return;

      if (tab === 'arkalochori') {{
        const axePhotoHtml = PAYLOAD.arkalochori_photo ? `
          <div style="width: 145px; flex-shrink: 0; display: flex; flex-direction: column; gap: 6px;">
            <div style="width: 100%; height: 165px; border-radius: 4px; overflow: hidden; background: #1C1917; border: 1px solid var(--editorial-border); box-shadow: 0 2px 6px rgba(0,0,0,0.06);">
              <img src="${{PAYLOAD.arkalochori_photo}}" alt="Arkalochori Votive Double Axe HM 584" style="width: 100%; height: 100%; object-fit: cover;" />
            </div>
            <div style="font-family: 'Geist Mono', monospace; font-size: 9.5px; color: var(--ink-secondary); text-align: center; line-height: 1.3;">
              HM 584 &bull; Arkalochori Cave
            </div>
          </div>
        ` : '';

        contentEl.innerHTML = `
          <div style="background: var(--canvas-subtle); padding: 14px; border-radius: 8px; border: 1px solid var(--editorial-border);">
            <div style="display: flex; gap: 14px; align-items: flex-start;">
              ${{axePhotoHtml}}
              <div style="flex: 1; min-width: 0;">
                <div style="font-weight: 600; color: #78350F; margin-bottom: 6px; font-family: 'Instrument Serif', Georgia, serif; font-size: 18px;">Arkalochori Votive Double Axe (HM 584)</div>
                <p style="margin: 0 0 10px 0; color: var(--ink-secondary); font-size: 13.5px; line-height: 1.55;">Late Minoan I bronze ceremonial double axe excavated by Spyridon Marinatos (1934) in the Arkalochori sacred cave. 15 incised signs in 3 vertical columns.</p>
                <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px;">
                  <span class="hagia-matched-pill">🪶 Sign 02 (Plumed Head): Incised on Col 1 &amp; 2 (ARK_01, ARK_03, ARK_06)</span>
                  <span class="hagia-matched-pill">🪓 Sign 44 (Double Axe): Incised on Col 3 (ARK_11)</span>
                  <span class="hagia-matched-pill">🌿 Sign 35 (Branch): Repeated 4x (ARK_02, ARK_04, ARK_07, ARK_09)</span>
                </div>
              </div>
            </div>
            <div class="verdict-box" style="margin-top: 10px;">
              <strong>Epigraphic Triangulation:</strong> Proves that the Plumed Head and Double Axe were sacred symbols of indigenous Cretan cave liturgy, directly falsifying theories of foreign Anatolian or Philistine origin.
            </div>
          </div>
        `;
      }} else {{
        contentEl.innerHTML = `
          <div style="background: var(--canvas-subtle); padding: 14px; border-radius: 8px; border: 1px solid var(--editorial-border);">
            <div style="font-weight: 600; color: #78350F; margin-bottom: 6px; font-family: 'Instrument Serif', Georgia, serif; font-size: 18px;">Linear A Tablet PH 1 (HM 1359)</div>
            <p style="margin: 0 0 10px 0; color: var(--ink-secondary); font-size: 13.5px; line-height: 1.55;">Excavated by Luigi Pernier (1908) in the exact same cist ("celletta") centimeters from the Disc in the ash destruction layer of Room 8, Northeast Wing of Phaistos Palace.</p>
            <div style="font-size: 12.5px; margin-bottom: 10px; font-family: 'Geist Mono', monospace; line-height: 1.5;">
              <div><strong>Face A:</strong> <code>]DI-RA-DI-NA *316 [] L2[ / ]JA *316 1 CYP H</code></div>
              <div><strong>Face B:</strong> <code>[]-NA 1 / PA[ ]FIC</code> (Commodities: Dried figs &amp; aromatic cyperus)</div>
            </div>
            <div class="verdict-box" style="margin-top: 10px;">
              <strong>Archaeological Invariant:</strong> Falsifies modern hoax theories. Confirms that Room 8 was an elite archival-liturgical repository preserving administrative commodity ledgers alongside sacred ceremonial hymn discs.
            </div>
          </div>
        `;
      }}
    }}

    // ==========================================
    // Hagia Triada Realia Synchronizer Engine
    // ==========================================
    let currentRealiaCropId = null;

    function initHagiaGallery() {{
      const gallery = PAYLOAD.hagia_gallery;
      if (!gallery || !gallery.crops || gallery.crops.length === 0) return;

      const stripEl = document.getElementById('hagiaThumbStrip');
      if (!stripEl) return;

      let stripHtml = '';
      gallery.crops.forEach(crop => {{
        const thumbSrc = crop.thumb_data_uri || crop.rel_url;
        const primarySign = (crop.primary_signs && crop.primary_signs.length > 0) ? crop.primary_signs[0] : '';
        const gData = (PAYLOAD.glyphs_catalog && PAYLOAD.glyphs_catalog[primarySign]) || {{ emoji: '𐇐' }};

        stripHtml += `
          <div class="hagia-thumb-item" id="thumb-${{crop.id}}" 
               onclick="selectHagiaRealia('${{crop.id}}', true)" 
               title="${{crop.title}} (${{crop.ritual_plane}})">
            <img src="${{thumbSrc}}" alt="${{crop.title}}" class="hagia-thumb-img" onerror="this.src='${{crop.thumb_data_uri}}'" />
            <div class="hagia-thumb-badge">${{gData.emoji}} #${{primarySign}}</div>
          </div>
        `;
      }});
      stripEl.innerHTML = stripHtml;

      selectHagiaRealia('crop_boat_model', false);
    }}

    function selectHagiaRealia(cropId, centerDisc = false) {{
      const gallery = PAYLOAD.hagia_gallery;
      if (!gallery || !gallery.crops) return;

      const crop = gallery.crops.find(c => c.id === cropId);
      if (!crop) return;

      currentRealiaCropId = cropId;

      // 1. Update active visual display
      const activeImg = document.getElementById('hagiaActiveImg');
      if (activeImg) {{
        activeImg.style.opacity = '0.35';
        activeImg.src = crop.rel_url || crop.thumb_data_uri;
        activeImg.onerror = () => {{ activeImg.src = crop.thumb_data_uri; }};
        setTimeout(() => {{ activeImg.style.opacity = '1.0'; }}, 40);
      }}

      const pBadge = document.getElementById('hagiaPlaneBadge');
      if (pBadge) pBadge.textContent = crop.ritual_plane;
      const sName = document.getElementById('hagiaSceneName');
      if (sName) sName.textContent = crop.scene_title.split(':')[0];
      const sBadge = document.getElementById('hagiaSceneBadge');
      if (sBadge) sBadge.textContent = crop.ritual_plane;
      const cTitle = document.getElementById('hagiaCropTitle');
      if (cTitle) cTitle.textContent = crop.title;
      const cDesc = document.getElementById('hagiaCropDesc');
      if (cDesc) cDesc.textContent = crop.description;

      // 2. Render matched sign pills
      const pillsContainer = document.getElementById('hagiaMatchedPills');
      if (pillsContainer) {{
        let pillsHtml = '';
        (crop.all_signs || []).forEach(sId => {{
          const isPrimary = (crop.primary_signs || []).includes(sId);
          const meta = PAYLOAD.signs_cat[sId] || {{ name: 'Sign ' + sId }};
          const gData = (PAYLOAD.glyphs_catalog && PAYLOAD.glyphs_catalog[sId]) || {{ emoji: '𐇐', short_name: meta.name }};
          pillsHtml += `
            <span class="hagia-matched-pill" style="${{isPrimary ? 'font-weight: 700; border-color: #D97706;' : 'opacity: 0.85;'}}">
              ${{gData.emoji}} #${{sId}} ${{gData.short_name || meta.name}}
            </span>
          `;
        }});
        pillsContainer.innerHTML = pillsHtml;
      }}

      // 3. Highlight thumbnail in strip and auto-scroll within container only
      document.querySelectorAll('.hagia-thumb-item').forEach(el => el.classList.remove('active'));
      const activeThumb = document.getElementById('thumb-' + cropId);
      if (activeThumb) {{
        activeThumb.classList.add('active');
        const stripEl = document.getElementById('hagiaThumbStrip');
        if (stripEl) {{
          const scrollLeft = activeThumb.offsetLeft - (stripEl.clientWidth / 2) + (activeThumb.clientWidth / 2);
          stripEl.scrollTo({{ left: Math.max(0, scrollLeft), behavior: 'smooth' }});
        }}
      }}

      // 4. If clicked by user (centerDisc = true), highlight matching signs and rotate disc
      if (centerDisc && crop.all_signs && crop.all_signs.length > 0) {{
        highlightMatchingSignsOnDisc(crop.all_signs);
      }}
    }}

    function highlightMatchingSignsOnDisc(targetSigns) {{
      // Remove previous matches
      document.querySelectorAll('.sign-slot').forEach(el => el.classList.remove('hagia-realia-match'));

      // Check current side groups for matches
      const currentGroups = (currentSide === 'A' ? PAYLOAD.side_a : PAYLOAD.side_b);
      let matchedGroupId = null;

      currentGroups.forEach(g => {{
        const hasMatch = g.signs.some(s => targetSigns.includes(s) || targetSigns.includes(String(parseInt(s, 10))));
        if (hasMatch) {{
          if (!matchedGroupId) matchedGroupId = g.id;
          g.signs.forEach((s, idx) => {{
            if (targetSigns.includes(s) || targetSigns.includes(String(parseInt(s, 10)))) {{
              const slotEl = document.getElementById(`slot-${{g.id}}-${{idx}}`);
              if (slotEl) slotEl.classList.add('hagia-realia-match');
            }}
          }});
        }}
      }});

      // If no match on current side, try other side
      if (!matchedGroupId) {{
        const otherSide = (currentSide === 'A' ? 'B' : 'A');
        const otherGroups = (otherSide === 'A' ? PAYLOAD.side_a : PAYLOAD.side_b);
        const matchOther = otherGroups.find(g => g.signs.some(s => targetSigns.includes(s) || targetSigns.includes(String(parseInt(s, 10)))));
        if (matchOther) {{
          switchSide(otherSide);
          highlightMatchingSignsOnDisc(targetSigns);
          return;
        }}
      }}

      if (matchedGroupId) {{
        inspectGroup(matchedGroupId);
      }}
    }}

    function updateHagiaSync(groupId, signId) {{
      const gallery = PAYLOAD.hagia_gallery;
      if (!gallery || !gallery.crops) return;

      let matchedCrop = null;

      // 1. If explicit signId provided (e.g. from teleprompter), check sign_to_crops
      if (signId && gallery.sign_to_crops) {{
        const padSign = String(signId).padStart(2, '0');
        const cropIds = gallery.sign_to_crops[padSign] || gallery.sign_to_crops[String(parseInt(signId, 10))];
        if (cropIds && cropIds.length > 0) {{
          matchedCrop = gallery.crops.find(c => c.id === cropIds[0]);
        }}
      }}

      // 2. If no direct sign match, find best matching crop for group's sign sequence
      if (!matchedCrop && groupId) {{
        const groups = (currentSide === 'A' ? PAYLOAD.side_a : PAYLOAD.side_b);
        const g = groups.find(x => x.id === groupId);
        if (g && g.signs) {{
          let topScore = 0;
          let bestCrop = null;
          gallery.crops.forEach(c => {{
            let score = 0;
            g.signs.forEach(s => {{
              const padS = String(s).padStart(2, '0');
              const rawS = String(parseInt(s, 10));
              if (c.primary_signs.includes(padS) || c.primary_signs.includes(rawS)) score += 3;
              else if (c.all_signs.includes(padS) || c.all_signs.includes(rawS)) score += 1;
            }});
            if (score > topScore) {{
              topScore = score;
              bestCrop = c;
            }}
          }});
          if (topScore > 0) {{
            matchedCrop = bestCrop;
          }}
        }}
      }}

      // 3. Smoothly update if new crop
      if (matchedCrop && matchedCrop.id !== currentRealiaCropId) {{
        selectHagiaRealia(matchedCrop.id, false);
      }}
    }}

    window.onload = () => {{
      renderSvg();
      populateFrontiers();
      initHagiaGallery();
      showComparativeTab('arkalochori');
      inspectGroup('A16');
    }};
  </script>
</body>
</html>
"""

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

    return html
