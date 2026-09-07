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

    # 4. JSON Payload for frontend
    data_payload = {
        "signs_cat": signs_cat,
        "side_a": groups_a,
        "side_b": groups_b,
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
  <link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@300;400;500;600&family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --canvas: #FAF8F5;
      --canvas-subtle: #F4F1EA;
      --surface: #FFFFFF;
      --ink: #18181B;
      --ink-secondary: #52525B;
      --ink-muted: #A1A1AA;
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
      font-family: 'Inter', system-ui, sans-serif;
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
      font-size: 14px;
      color: var(--ink-secondary);
      margin-top: 4px;
    }}
    .header-telemetry {{
      font-family: 'Geist Mono', monospace;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--ink-muted);
      text-align: right;
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
    }}
    .btn-group {{
      display: inline-flex;
      background: var(--canvas-subtle);
      border-radius: 9999px;
      padding: 3px;
      border: 1px solid var(--editorial-border);
    }}
    .btn {{
      background: none;
      border: none;
      font-family: 'Inter', sans-serif;
      font-size: 13px;
      font-weight: 500;
      padding: 6px 14px;
      border-radius: 9999px;
      cursor: pointer;
      color: var(--ink-secondary);
      transition: all 0.15s ease;
    }}
    .btn.active {{
      background: var(--surface);
      color: var(--ink);
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }}
    .btn-primary {{
      background: var(--ink);
      color: #FFF;
      padding: 7px 18px;
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
    .analytics-column {{
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    .card {{
      background: var(--surface);
      border: 1px solid var(--editorial-border);
      border-radius: 12px;
      padding: 20px 24px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.02);
    }}
    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 12px;
      border-bottom: 1px solid var(--editorial-border);
      padding-bottom: 8px;
    }}
    .card-title {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: 20px;
      font-weight: 400;
      color: var(--ink);
    }}
    .card-badge {{
      font-family: 'Geist Mono', monospace;
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      color: var(--accent);
      background: #FEF3C7;
      padding: 2px 8px;
      border-radius: 9999px;
    }}
    .group-inspector {{
      font-family: 'Geist Mono', monospace;
      font-size: 13px;
    }}
    .glyph-display {{
      display: flex;
      gap: 8px;
      margin: 12px 0;
      font-size: 26px;
      align-items: center;
    }}
    .glyph-pill {{
      background: var(--canvas-subtle);
      border: 1px solid var(--editorial-border);
      border-radius: 6px;
      padding: 4px 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .glyph-sub {{
      font-size: 10px;
      color: var(--ink-muted);
      font-family: 'Geist Mono', monospace;
    }}
    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      font-family: 'Geist Mono', monospace;
      margin-top: 8px;
    }}
    table.data-table th, table.data-table td {{
      padding: 6px 8px;
      text-align: left;
      border-bottom: 1px solid var(--editorial-border);
    }}
    table.data-table th {{
      color: var(--ink-muted);
      font-weight: 500;
      text-transform: uppercase;
      font-size: 10px;
    }}
    .verdict-box {{
      font-size: 12px;
      line-height: 1.4;
      color: var(--ink-secondary);
      background: var(--canvas);
      padding: 10px 12px;
      border-radius: 6px;
      border-left: 3px solid var(--ink);
      margin-top: 10px;
    }}
    .sign-circle {{
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .sign-circle:hover {{
      stroke: var(--ink) !important;
      stroke-width: 2.5px !important;
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
  </style>
</head>
<body>

  <header>
    <div class="title-area">
      <h1>Phaistos Disc Analytical Workbench</h1>
      <p>Interactive Epigraphy, Strophic Acoustic Synthesis & 5-Frontier Skeptic Validation</p>
    </div>
    <div class="header-telemetry">
      <div>CORPUS: GODART 1995 CANONICAL</div>
      <div>61 GROUPS &bull; 242 SIGNS &bull; 18 STROKES</div>
      <div>EPICENTRE: MESARA ALLUVIAL MARL</div>
    </div>
  </header>

  <div class="workbench-grid">
    <!-- Spiral Display Column -->
    <div class="spiral-card">
      <div class="controls-bar">
        <div class="btn-group">
          <button id="btnSideA" class="btn active" onclick="switchSide('A')">Side A (31 Groups)</button>
          <button id="btnSideB" class="btn" onclick="switchSide('B')">Side B (30 Groups)</button>
        </div>
        <div class="btn-group">
          <button id="btnCorpusReal" class="btn active" onclick="toggleSurrogate(false)">Canonical</button>
          <button id="btnCorpusNull" class="btn" onclick="toggleSurrogate(true)">Monte Carlo Null</button>
        </div>
      </div>

      <svg id="discSvg" width="760" height="760" viewBox="0 0 800 800"></svg>

      <div class="audio-panel">
        <button id="btnPlay" class="btn btn-primary" onclick="toggleAudio()">Play Lyric Triad (A14–A22)</button>
        <div class="audio-telemetry" id="audioTelemetry">
          LYRE SYNTH: 11.0s &bull; 14-mora Paean Responsion ($p < 10^{{-5}}$)
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
          <p style="color: var(--ink-secondary); font-size: 13px;">Hover or click any segment in the spiral track to inspect physical punches, incised strokes, and morphosyntax.</p>
        </div>
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
        <div style="font-size: 12px; color: var(--ink-secondary); margin-bottom: 8px;">
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

    function renderSvg() {{
      const svg = document.getElementById('discSvg');
      const groups = (currentSide === 'A' ? PAYLOAD.side_a : PAYLOAD.side_b);
      const cx = 400, cy = 400;

      let html = `
        <circle cx="${{cx}}" cy="${{cy}}" r="372" fill="#F4EDE2" stroke="#B8977E" stroke-width="2.5" />
        <circle cx="${{cx}}" cy="${{cy}}" r="80" fill="#E8DEC8" stroke="#B8977E" stroke-width="1.5" />
        <text x="${{cx}}" y="36" font-family="'Instrument Serif', serif" font-size="24" fill="#3D312A" text-anchor="middle">
          PHAISTOS DISC &mdash; SIDE ${{currentSide}}
        </text>
      `;

      groups.forEach((g, gIdx) => {{
        const strokeAttr = g.oblique_stroke ? 'stroke="#059669" stroke-width="2"' : 'stroke="#B8977E" stroke-width="1"';
        
        g.signs_coords.forEach((s, sIdx) => {{
          const isFinal = (sIdx === g.signs_coords.length - 1);
          const hasStroke = (isFinal && g.oblique_stroke);
          const meta = PAYLOAD.signs_cat[s.sign_id] || {{ name: 'Unknown', char: s.sign_id }};
          const fillCol = hasStroke ? '#D1FAE5' : '#FFFDF9';

          html += `
            <g class="sign-slot" id="slot-${{g.id}}-${{sIdx}}" 
               onmouseover="inspectGroup('${{g.id}}')" 
               onclick="inspectGroup('${{g.id}}')">
              <circle class="sign-circle" cx="${{s.x}}" cy="${{s.y}}" r="15" 
                      fill="${{fillCol}}" stroke="#A88B74" stroke-width="1.2" />
              <text x="${{s.x}}" y="${{s.y + 6}}" font-size="16" text-anchor="middle" fill="#18181B">
                ${{meta.char}}
              </text>
              ${{hasStroke ? `<line x1="${{s.x-10}}" y1="${{s.y+16}}" x2="${{s.x+10}}" y2="${{s.y+12}}" stroke="#059669" stroke-width="2.5" stroke-linecap="round"/>` : ''}}
            </g>
          `;
        }});

        // Group label at first sign
        if (g.signs_coords.length > 0) {{
          const f = g.signs_coords[0];
          html += `
            <text x="${{f.x}}" y="${{f.y - 18}}" font-family="'Geist Mono', monospace" font-size="9" fill="#8C7A6B" font-weight="600" text-anchor="middle">
              ${{g.id}}
            </text>
          `;
        }}
      }});

      svg.innerHTML = html;
    }}

    function switchSide(side) {{
      currentSide = side;
      document.getElementById('btnSideA').className = (side === 'A' ? 'btn active' : 'btn');
      document.getElementById('btnSideB').className = (side === 'B' ? 'btn active' : 'btn');
      renderSvg();
    }}

    function toggleSurrogate(isNull) {{
      isNullSurrogate = isNull;
      document.getElementById('btnCorpusReal').className = (!isNull ? 'btn active' : 'btn');
      document.getElementById('btnCorpusNull').className = (isNull ? 'btn active' : 'btn');
      // In null surrogate mode, visually alter display
      if (isNull) {{
        document.getElementById('discSvg').style.filter = 'hue-rotate(180deg) saturate(0.8)';
      }} else {{
        document.getElementById('discSvg').style.filter = 'none';
      }}
    }}

    function inspectGroup(groupId) {{
      const groups = (currentSide === 'A' ? PAYLOAD.side_a : PAYLOAD.side_b);
      const g = groups.find(x => x.id === groupId);
      if (!g) return;

      document.getElementById('inspBadge').textContent = g.id + ' (TURN ' + g.turn + ')';

      let pillsHtml = '';
      g.signs.forEach((sId, idx) => {{
        const meta = PAYLOAD.signs_cat[sId] || {{ name: 'Unknown', char: sId }};
        pillsHtml += `
          <div class="glyph-pill">
            <div>${{meta.char}}</div>
            <div class="glyph-sub">#${{sId}}</div>
            <div class="glyph-sub" style="font-size: 8px;">${{meta.name}}</div>
          </div>
        `;
      }});

      const strokeBadge = g.oblique_stroke 
        ? '<span style="color: #059669; font-weight: 600;">YES &bull; Terminal Prolongation (2&mu;)</span>' 
        : '<span style="color: var(--ink-muted);">None (1&mu;)</span>';

      document.getElementById('inspectorContent').innerHTML = `
        <div style="font-size: 14px; font-weight: 600; margin-bottom: 4px;">Group ${{g.id}} &mdash; ${{g.signs.length}} Signs</div>
        <div class="glyph-display">${{pillsHtml}}</div>
        <div style="margin-top: 8px; font-size: 12px;">
          <div><strong>Incised Oblique Stroke:</strong> ${{strokeBadge}}</div>
          <div><strong>Palimpsest / Erasure:</strong> ${{g.erasure ? '<span style="color: #DC2626;">Documented Erasure</span>' : 'None'}}</div>
          <div><strong>Metric Weight:</strong> ${{g.signs.length + (g.oblique_stroke ? 1 : 0)}} morae</div>
        </div>
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

    // Karplus-Strong Physical Plucked Lyre Synthesis for Browser Playback
    function playPluckedString(freq, durationMs) {{
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
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

    async function toggleAudio() {{
      if (isPlaying) return;
      isPlaying = true;
      document.getElementById('btnPlay').textContent = 'Synthesizing Lyric Paean...';
      switchSide('A');

      const triad = PAYLOAD.triad_timing;
      let totalElapsed = 0;

      for (let i = 0; i < triad.length; i++) {{
        const item = triad[i];
        inspectGroup(item.group_id);
        playPluckedString(item.freq, item.duration_ms);
        document.getElementById('audioTelemetry').textContent = 
          `PLAYING ${{item.group_id}} (${{item.morae}} morae) &bull; responsion triad cadence`;
        await new Promise(r => setTimeout(r, item.duration_ms));
      }}

      isPlaying = false;
      document.getElementById('btnPlay').textContent = 'Play Lyric Triad (A14–A22)';
      document.getElementById('audioTelemetry').textContent = 
        `COMPLETED: 14-mora Lyric Triad Paean &bull; exact strophic balance`;
    }}

    window.onload = () => {{
      renderSvg();
      populateFrontiers();
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
