# Media attribution

## Disc facsimiles (`facsimiles/`)

Cropped photographs of the Phaistos Disc (Heraklion Archaeological Museum), sourced from Wikimedia Commons:

| File | Commons title | License | Photographer / editor |
|------|---------------|---------|------------------------|
| `facsimiles/side_a.jpg` | [Phaistos Disc - Side A - 6380 - crop1.jpg](https://commons.wikimedia.org/wiki/File:Phaistos_Disc_-_Side_A_-_6380_-_crop1.jpg) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | Photograph: C messier; crop: Bammesk |
| `facsimiles/side_b.jpg` | [Phaistos Disc - Side B - 6381 - crop1.jpg](https://commons.wikimedia.org/wiki/File:Phaistos_Disc_-_Side_B_-_6381_-_crop1.jpg) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | Photograph: C messier; crop: Bammesk |

These files are **not** MIT-relicensed. Redistribution must preserve attribution and the CC BY-SA 4.0 terms (share-alike).

Vendored copies may be resized for web delivery; derivative crops remain under CC BY-SA 4.0.

## Hagia Triada realia (`hagia_triada/`)

Derived WebP crops and scene overviews of the Hagia Triada sarcophagus frescoes (Heraklion Archaeological Museum, Inv. Λ396), generated from Wikimedia Commons sources. Used by the GitHub Pages workbench (`--pages-safe`).

### Source photographs

| Local source key | Commons title | License | Photographer |
|------------------|---------------|---------|--------------|
| `side1_overview.jpg` | [Sarcophagus archmus Heraklion.jpg](https://commons.wikimedia.org/wiki/File:Sarcophagus_archmus_Heraklion.jpg) | [CC0](https://creativecommons.org/publicdomain/zero/1.0/) | [Jebulon](https://commons.wikimedia.org/wiki/User:Jebulon) |
| `side1_libation.jpg` | [… Heraklion AM - 05.jpg](https://commons.wikimedia.org/wiki/File:Painting_on_limestone_sarcophagus_of_religious_rituals_from_Hagia_Triada_-_Heraklion_AM_-_05.jpg) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | [ArchaiOptix](https://commons.wikimedia.org/wiki/User:ArchaiOptix) |
| `side1_votives.jpg` | [… Heraklion AM - 02.jpg](https://commons.wikimedia.org/wiki/File:Painting_on_limestone_sarcophagus_of_religious_rituals_from_Hagia_Triada_-_Heraklion_AM_-_02.jpg) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | [ArchaiOptix](https://commons.wikimedia.org/wiki/User:ArchaiOptix) |
| `side2_overview.jpg` | [Agia Triada … long side 2 … 145309.jpg](https://commons.wikimedia.org/wiki/File:Agia_Triada,_sarcophagus,_long_side_2,_limestone,_frescoes,_1370-1320_BC,_AMH,_145309.jpg) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | [Zde](https://commons.wikimedia.org/wiki/User:Zde) |
| `side2_sacrifice.jpg` | [… Heraklion AM - 01 (cropped).jpg](https://commons.wikimedia.org/wiki/File:Painting_on_limestone_sarcophagus_of_religious_rituals_from_Hagia_Triada_-_Heraklion_AM_-_01_(cropped).jpg) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | [ArchaiOptix](https://commons.wikimedia.org/wiki/User:ArchaiOptix) |
| `side3_chariot.jpg` | [Agia Triada … short side 1 … 145313.jpg](https://commons.wikimedia.org/wiki/File:Agia_Triada,_sarcophagus,_short_side_1,_limestone,_frescoes,_1370-1320_BC,_AMH,_145313.jpg) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | [Zde](https://commons.wikimedia.org/wiki/User:Zde) |

### Vendored derivatives in this folder

- `crop_*.webp` — diagnostic realia crops (see `REALIA_CROP_DEFINITIONS` in `src/phaistos/ritual/hagia_gallery.py`)
- `ht_scene_*_overview.webp` — resized scene overviews

CC BY-SA source pixels remain **CC BY-SA 4.0** (share-alike; attribution required). The Jebulon overview source is CC0. These files are **not** MIT-relicensed.

Local regenerations may still fetch into gitignored `data/hagia_triada/` / `reports/visuals/hagia_triada/` via `phaistos hagia-gallery` / `scripts/fetch_hagia_images.py`.

## Workbench cover / screencast

- `workbench-cover.webp` (or `.png`) — UI screenshot of this project's pages-safe workbench.
- `workbench-hymn-playback.gif` / `.mp4` — short screencast of synthetic teleprompter / triad playback.

UI captures are project documentation. Facsimile / Hagia pixels visible in them remain subject to the Commons attribution above.
