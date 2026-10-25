#!/usr/bin/env python3
"""Get photos ready for a year letter: resized, rotated upright, and with all metadata removed.

Photos straight from a phone carry GPS coordinates, camera details, and timestamps in their
EXIF data. This writes clean copies that are safe to commit to this public repo:

    uv run --group photos scripts/prepare_photos.py ~/Desktop/2025-picks/*.jpg --out site/_static/photos/2025

Export your picks from Photos as JPEG first (File > Export > Export N Photos, JPEG). Output
files keep their names, lowercased with spaces as dashes, so name them for the month and
place (``04-camino-sunset.jpg``) to keep each year's folder in order.
"""

import argparse
import pathlib
import re
import sys

from PIL import Image, ImageOps


def clean_name(path):
    stem = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")
    return f"{stem or 'photo'}.jpg"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("photos", nargs="+", type=pathlib.Path, help="JPEG or PNG files to prepare")
    ap.add_argument("--out", required=True, type=pathlib.Path, help="folder to write to, like site/_static/photos/2025")
    ap.add_argument("--size", type=int, default=1600, help="longest side in pixels (default 1600)")
    ap.add_argument("--quality", type=int, default=82, help="JPEG quality (default 82)")
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    for src in args.photos:
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im)  # apply the camera's rotation before dropping EXIF
            im.thumbnail((args.size, args.size), Image.LANCZOS)
            dest = args.out / clean_name(src)
            # A fresh image carries no EXIF, GPS, or XMP; nothing is copied from the original.
            clean = Image.new("RGB", im.size)
            clean.paste(im.convert("RGB"))
            clean.save(dest, "JPEG", quality=args.quality, optimize=True, progressive=True)
        print(f"{src.name} -> {dest} ({clean.size[0]}x{clean.size[1]})", file=sys.stderr)


if __name__ == "__main__":
    main()
