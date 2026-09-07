#!/usr/bin/env python3
"""CLI utility to download, crop, and verify Hagia Triada Sarcophagus fresco images."""

import sys
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from phaistos.ritual.hagia_gallery import get_hagia_gallery_manifest


def main():
    print("==> Fetching and processing Hagia Triada Sarcophagus realia crops...")
    cache_dir = Path("data/hagia_triada")
    output_dir = Path("reports/visuals/hagia_triada")

    manifest = get_hagia_gallery_manifest(cache_dir=cache_dir, output_dir=output_dir)
    print(f"==> Successfully generated {manifest['total_crops']} realia crops:")
    for c in manifest["crops"]:
        out_f = output_dir / c["output_file"]
        sz_kb = out_f.stat().st_size / 1024 if out_f.exists() else 0
        signs_str = ", ".join(c["primary_signs"])
        print(f"  • {c['title']} ({c['ritual_plane']}) [Signs: {signs_str}] -> {c['output_file']} ({sz_kb:.1f} KB)")


if __name__ == "__main__":
    main()
