"""Hagia Triada Sarcophagus Fresco Gallery & Realia Synchronizer.

Crops and manages high-resolution archival fresco imagery (c. 1400-1350 BC,
Heraklion Archaeological Museum, inventory Λ396, found 3 km from Phaistos Palace).
Maps 10 diagnostic realia artifacts to Phaistos Disc signs and synchronizes
with rotational teleprompter simulation playback.
"""

import base64
from pathlib import Path
from typing import Any, Dict, List, Optional
import urllib.request
from PIL import Image


HAGIA_TRIADA_SOURCES = {
    "side1_overview.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Sarcophagus_archmus_Heraklion.jpg/1280px-Sarcophagus_archmus_Heraklion.jpg",
    "side1_libation.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Painting_on_limestone_sarcophagus_of_religious_rituals_from_Hagia_Triada_-_Heraklion_AM_-_05.jpg/1280px-Painting_on_limestone_sarcophagus_of_religious_rituals_from_Hagia_Triada_-_Heraklion_AM_-_05.jpg",
    "side1_votives.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Painting_on_limestone_sarcophagus_of_religious_rituals_from_Hagia_Triada_-_Heraklion_AM_-_02.jpg/1280px-Painting_on_limestone_sarcophagus_of_religious_rituals_from_Hagia_Triada_-_Heraklion_AM_-_02.jpg",
    "side2_overview.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Agia_Triada%2C_sarcophagus%2C_long_side_2%2C_limestone%2C_frescoes%2C_1370-1320_BC%2C_AMH%2C_145309.jpg/1280px-Agia_Triada%2C_sarcophagus%2C_long_side_2%2C_limestone%2C_frescoes%2C_1370-1320_BC%2C_AMH%2C_145309.jpg",
    "side2_sacrifice.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Painting_on_limestone_sarcophagus_of_religious_rituals_from_Hagia_Triada_-_Heraklion_AM_-_01_%28cropped%29.jpg/1280px-Painting_on_limestone_sarcophagus_of_religious_rituals_from_Hagia_Triada_-_Heraklion_AM_-_01_%28cropped%29.jpg",
    "side3_chariot.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Agia_Triada%2C_sarcophagus%2C_short_side_1%2C_limestone%2C_frescoes%2C_1370-1320_BC%2C_AMH%2C_145313.jpg/1280px-Agia_Triada%2C_sarcophagus%2C_short_side_1%2C_limestone%2C_frescoes%2C_1370-1320_BC%2C_AMH%2C_145313.jpg",
}


REALIA_CROP_DEFINITIONS = [
    {
        "id": "crop_libation_hydria",
        "title": "Libation Pitcher & Krater",
        "scene_id": "HT_SCENE_1",
        "scene_title": "Scene 1: Libation at Double Axe Pillars",
        "ritual_plane": "OFFERING",
        "primary_signs": ["41", "39"],
        "all_signs": ["41", "39", "35", "36"],
        "source_file": "side1_libation.jpg",
        "crop_box": (0.15, 0.35, 0.65, 0.75),
        "output_file": "crop_libation_hydria.webp",
        "description": "Priestess pours liquid libation from a fluted pitcher into a large krater between the double axe pillars.",
    },
    {
        "id": "crop_labrys_double_axe",
        "title": "Stepped Double Axe & Epiphany Bird",
        "scene_id": "HT_SCENE_1",
        "scene_title": "Scene 1: Libation at Double Axe Pillars",
        "ritual_plane": "INVOCATION / DEITY",
        "primary_signs": ["44", "31", "32"],
        "all_signs": ["44", "31", "32"],
        "source_file": "side1_libation.jpg",
        "crop_box": (0.48, 0.15, 0.88, 0.55),
        "output_file": "crop_labrys_double_axe.webp",
        "description": "Gilded double axe (labrys) erected upon stepped base, crowned by a black bird of divine epiphany.",
    },
    {
        "id": "crop_lyre_player",
        "title": "7-String Lyre / Phorminx Musician",
        "scene_id": "HT_SCENE_1",
        "scene_title": "Scene 1: Libation at Double Axe Pillars",
        "ritual_plane": "MUSIC / CONTROL",
        "primary_signs": ["12"],
        "all_signs": ["12"],
        "source_file": "side1_libation.jpg",
        "crop_box": (0.0, 0.30, 0.35, 0.75),
        "output_file": "crop_lyre_player.webp",
        "description": "Musician in long ceremonial robe playing 7-stringed phorminx lyre accompanying liquid offering.",
    },
    {
        "id": "crop_trussed_bull",
        "title": "Trussed Sacrificial Bull",
        "scene_id": "HT_SCENE_2",
        "scene_title": "Scene 2: Blood Sacrifice of Trussed Bull",
        "ritual_plane": "OFFERING",
        "primary_signs": ["28", "27"],
        "all_signs": ["28", "27", "16"],
        "source_file": "side2_sacrifice.jpg",
        "crop_box": (0.28, 0.10, 0.72, 0.95),
        "output_file": "crop_trussed_bull.webp",
        "description": "Sacrificial bull bound on wooden table, throat incised with blood pouring into a dedicated vessel.",
    },
    {
        "id": "crop_aulos_player",
        "title": "Twin Reed Pipes (Aulos) Musician",
        "scene_id": "HT_SCENE_2",
        "scene_title": "Scene 2: Blood Sacrifice of Trussed Bull",
        "ritual_plane": "MUSIC / CONTROL",
        "primary_signs": ["21"],
        "all_signs": ["21"],
        "source_file": "side2_sacrifice.jpg",
        "crop_box": (0.52, 0.02, 0.76, 0.90),
        "output_file": "crop_aulos_player.webp",
        "description": "Musician playing twin pipes (aulos) directly behind the sacrificial altar, governing the ritual pulse.",
    },
    {
        "id": "crop_boat_model",
        "title": "Processional High-Prow Boat Model",
        "scene_id": "HT_SCENE_3",
        "scene_title": "Scene 3: Procession of Votive Offerings",
        "ritual_plane": "OFFERING",
        "primary_signs": ["26"],
        "all_signs": ["26", "33"],
        "source_file": "side1_votives.jpg",
        "crop_box": (0.38, 0.18, 0.72, 0.85),
        "output_file": "crop_boat_model.webp",
        "description": "Youth wearing animal hide skirt carrying a model of a high-prow maritime galley toward the tomb shrine.",
    },
    {
        "id": "crop_calf_offering",
        "title": "Bovine Votive Figurines",
        "scene_id": "HT_SCENE_3",
        "scene_title": "Scene 3: Procession of Votive Offerings",
        "ritual_plane": "OFFERING",
        "primary_signs": ["30", "28"],
        "all_signs": ["30", "28", "34"],
        "source_file": "side1_votives.jpg",
        "crop_box": (0.05, 0.18, 0.45, 0.85),
        "output_file": "crop_calf_offering.webp",
        "description": "Offering bearers presenting sculptural animal figures to the chthonic hero or deity.",
    },
    {
        "id": "crop_peak_shrine_tree",
        "title": "Sacred Tree & Peak Shrine Altar",
        "scene_id": "HT_SCENE_2",
        "scene_title": "Scene 2: Blood Sacrifice of Trussed Bull",
        "ritual_plane": "INVOCATION / DEITY",
        "primary_signs": ["38", "23", "37"],
        "all_signs": ["38", "23", "37"],
        "source_file": "side2_sacrifice.jpg",
        "crop_box": (0.70, 0.05, 0.98, 0.95),
        "output_file": "crop_peak_shrine_tree.webp",
        "description": "Tripartite sanctuary facade with consecrated horns, stepped altar, and sacred evergreen tree.",
    },
    {
        "id": "crop_griffin_chariot",
        "title": "Winged Griffin Chariot Epiphany",
        "scene_id": "HT_SCENE_4",
        "scene_title": "Scene 4: Divine Epiphany & Peak Shrine",
        "ritual_plane": "INVOCATION / DEITY",
        "primary_signs": ["02", "06"],
        "all_signs": ["02", "06"],
        "source_file": "side3_chariot.jpg",
        "crop_box": (0.10, 0.22, 0.90, 0.72),
        "output_file": "crop_griffin_chariot.webp",
        "description": "Two goddesses ride in a chariot drawn by winged griffins, accompanied by a soaring bird of epiphany.",
    },
    {
        "id": "crop_palace_rosette",
        "title": "Palatial Rosette Frize",
        "scene_id": "HT_SCENE_4",
        "scene_title": "Scene 4: Divine Epiphany & Peak Shrine",
        "ritual_plane": "INVOCATION / DEITY",
        "primary_signs": ["24"],
        "all_signs": ["24"],
        "source_file": "side1_overview.jpg",
        "crop_box": (0.15, 0.08, 0.85, 0.22),
        "output_file": "crop_palace_rosette.webp",
        "description": "Eight-petaled rosettes forming the running sacred frieze around the perimeter of the sarcophagus.",
    },
]


def download_source_images(cache_dir: Path) -> None:
    """Download source fresco images from Wikimedia Commons if not already present."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    headers = {"User-Agent": "PhaistosLab/0.2 (open-source research software; contact via GitHub issues)"}

    for fname, url in HAGIA_TRIADA_SOURCES.items():
        fpath = cache_dir / fname
        if not fpath.exists():
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                fpath.write_bytes(resp.read())


def crop_and_export_realia(cache_dir: Path, output_dir: Path) -> List[Dict[str, Any]]:
    """Crop diagnostic realia details and export optimized WebP images."""
    output_dir.mkdir(parents=True, exist_ok=True)
    download_source_images(cache_dir)

    results = []

    for defn in REALIA_CROP_DEFINITIONS:
        src_path = cache_dir / defn["source_file"]
        if not src_path.exists():
            continue

        out_path = output_dir / defn["output_file"]

        with Image.open(src_path) as img:
            w, h = img.size
            l, t, r, b = defn["crop_box"]
            box = (int(l * w), int(t * h), int(r * w), int(b * h))
            cropped = img.crop(box)

            # Ensure reasonable dimensions for web gallery (max 640px)
            max_dim = 640
            if cropped.size[0] > max_dim or cropped.size[1] > max_dim:
                cropped.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

            cropped.save(out_path, "WEBP", quality=85)

            # Generate compact thumbnail data URI for instant rendering
            thumb = cropped.copy()
            thumb.thumbnail((120, 90), Image.Resampling.LANCZOS)
            import io
            buf = io.BytesIO()
            thumb.save(buf, "WEBP", quality=70)
            data_uri = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode("ascii")

        item = dict(defn)
        item["file_path"] = str(out_path)
        item["rel_url"] = f"visuals/hagia_triada/{defn['output_file']}"
        item["thumb_data_uri"] = data_uri
        results.append(item)

    # Export overview thumbnails
    for src_name, target_name in [
        ("side1_overview.jpg", "ht_scene_1_libation_overview.webp"),
        ("side2_overview.jpg", "ht_scene_2_bull_sacrifice_overview.webp"),
        ("side3_chariot.jpg", "ht_scene_4_griffin_epiphany_overview.webp"),
    ]:
        src_path = cache_dir / src_name
        out_path = output_dir / target_name
        if src_path.exists() and not out_path.exists():
            with Image.open(src_path) as img:
                thumb = img.copy()
                thumb.thumbnail((800, 600), Image.Resampling.LANCZOS)
                thumb.save(out_path, "WEBP", quality=80)

    return results


def get_hagia_gallery_manifest(
    cache_dir: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    *,
    pages_safe: bool = False,
) -> Dict[str, Any]:
    """Retrieve the full Hagia Triada gallery manifest for UI payload integration.

    ``pages_safe=True`` skips Wikimedia downloads/crops (CI/Pages rate limits and NOTICE).
    """
    if cache_dir is None:
        cache_dir = Path("data/hagia_triada")
    if output_dir is None:
        output_dir = Path("reports/visuals/hagia_triada")

    if pages_safe:
        crops = []
        for defn in REALIA_CROP_DEFINITIONS:
            item = dict(defn)
            item["thumb_data_uri"] = ""
            item["rel_url"] = ""
            item["commons_note"] = (
                "Image omitted in pages_safe build; fetch from Wikimedia Commons locally "
                "(see HAGIA_TRIADA_SOURCES / NOTICE)."
            )
            crops.append(item)
        sign_to_crops: Dict[str, List[str]] = {}
        for c in crops:
            for s in c["all_signs"]:
                pad_s = f"{int(s):02d}" if s.isdigit() else s
                sign_to_crops.setdefault(pad_s, []).append(c["id"])
        return {
            "title": "Hagia Triada Sarcophagus Liturgical Homology Gallery",
            "date_provenance": "c. 1400–1350 BC, Hagia Triada Villa (3 km from Phaistos Palace)",
            "museum": "Heraklion Archaeological Museum (Inv. Λ396)",
            "total_crops": len(crops),
            "crops": crops,
            "sign_to_crops": sign_to_crops,
            "pages_safe": True,
        }

    crops = crop_and_export_realia(cache_dir, output_dir)

    # Build sign-to-realia lookup table
    sign_to_crops = {}
    for c in crops:
        for s in c["all_signs"]:
            pad_s = f"{int(s):02d}" if s.isdigit() else s
            if pad_s not in sign_to_crops:
                sign_to_crops[pad_s] = []
            sign_to_crops[pad_s].append(c["id"])

    return {
        "title": "Hagia Triada Sarcophagus Liturgical Homology Gallery",
        "date_provenance": "c. 1400–1350 BC, Hagia Triada Villa (3 km from Phaistos Palace)",
        "museum": "Heraklion Archaeological Museum (Inv. Λ396)",
        "total_crops": len(crops),
        "crops": crops,
        "sign_to_crops": sign_to_crops,
    }


def get_realia_for_group(signs: List[str], manifest: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Match a sign sequence to the most diagnostic Hagia Triada realia crop."""
    if manifest is None:
        manifest = get_hagia_gallery_manifest()

    crops = manifest.get("crops", [])
    if not crops:
        return None

    crop_scores: Dict[str, int] = {}
    for c in crops:
        score = 0
        for s in signs:
            pad_s = f"{int(s):02d}" if s.isdigit() else s
            if pad_s in c.get("primary_signs", []):
                score += 3
            elif pad_s in c.get("all_signs", []):
                score += 1
        if score > 0:
            crop_scores[c["id"]] = score

    if not crop_scores:
        return None

    top_crop_id = max(crop_scores.items(), key=lambda x: x[1])[0]
    return next((c for c in crops if c["id"] == top_crop_id), None)
