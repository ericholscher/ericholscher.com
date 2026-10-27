"""Draw each trip's map: one topo map, in the site's colors, with its places named.

The map is the one trip-map.js draws live (topoTripStyle): terrain, water, and borders, with each
place as its shape from trip_shapes.json (a park's boundary, a trail's route) or as a pin, and its
name. The framing fits the places (topo_trips.trip_geo). Each trip gets two images, drawn at the
size they're shown so the names are legible: a card for the home page, and a wider map for the
Adventures page, where trip-map.js swaps in the live map when the trip is opened.

The maps are rendered once, here, and committed, so the home page loads no map library and a map
never shows a blank box. It runs MapLibre in Chromium through Playwright (the tests group):

    uv run --group tests python scripts/trip_topo.py [slug ...]

Writes site/_static/maps/<trip>-card.webp and <trip>-topo.webp, for every trip with a map or only
the ones named. Rerun it when a trip is added or its places or shapes change (after
trip_shapes.py); the build warns when a trip has none. Set CHROMIUM_PATH if Playwright's own
Chromium isn't installed.
"""

import argparse
import json
import os
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "site" / "_ext"))

import topo_trips  # noqa: E402

DATA = ROOT / "site" / "_data"
OUTPUT = ROOT / "site" / "_static" / "maps"
MAPLIBRE = ROOT / "site" / "_static" / "vendor" / "maplibre-gl-4.7.1"
SCRIPT = ROOT / "site" / "_themes" / "topo" / "static" / "trip-map.js"
# The size each map is shown at, in CSS pixels, its names' size, and how sharp to draw it.
SIZES = {
    "card": {"width": 300, "height": 200, "names": 11, "scale": 2.5},  # a home page card, 3:2
    "topo": {"width": 480, "height": 240, "names": 12, "scale": 2},  # the Adventures page, 2:1
}
RENDER = """
([geo, names]) => new Promise((resolve, reject) => {
  const el = document.getElementById('map'), b = geo.bounds;
  const map = new maplibregl.Map({ container: el, style: topoTripStyle(geo, names), bounds: [[b[0], b[1]], [b[2], b[3]]],
    fitBoundsOptions: { padding: topoTripPadding(el.clientWidth, el.clientHeight) },
    interactive: false, attributionControl: false, fadeDuration: 0, renderWorldCopies: false });
  map.on('error', e => console.log('map error: ' + (e.error && e.error.message)));
  map.once('idle', () => resolve());
  setTimeout(() => reject(new Error('timed out')), 90000);
})
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("slugs", nargs="*", help="trips to draw (default: all of them)")
    args = parser.parse_args()

    load = lambda name: json.loads((DATA / name).read_text())  # noqa: E731
    trips, _, _ = topo_trips.build(load("hikes.json"), load("places.json"), load("trips.json"))
    shapes = load("trip_shapes.json")
    chosen = [t for t in trips if t["slug"] in args.slugs] if args.slugs else trips

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH"),
                                    args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        for trip in chosen:
            if not trip["map"]:
                continue
            geo = topo_trips.trip_geo(trip, shapes)
            for kind, size in SIZES.items():
                page = browser.new_page(viewport={"width": size["width"], "height": size["height"]},
                                        device_scale_factor=size["scale"])
                page.on("console", lambda m: print("  " + m.text) if "error" in m.text else None)
                page.set_content(f'<style>body{{margin:0}}#map{{width:{size["width"]}px;height:{size["height"]}px}}</style><div id="map"></div>')
                page.add_style_tag(path=str(MAPLIBRE / "maplibre-gl.css"))
                page.add_script_tag(path=str(MAPLIBRE / "maplibre-gl.js"))
                page.add_script_tag(path=str(SCRIPT))
                page.evaluate(RENDER, [geo, size["names"]])
                out = OUTPUT / f"{trip['slug']}-{kind}.webp"
                png = OUTPUT / f".{trip['slug']}-{kind}.png"
                page.screenshot(path=str(png))
                page.close()
                Image.open(png).convert("RGB").save(out, "WEBP", quality=80, method=6)
                png.unlink()
                print(f"{out.relative_to(ROOT)}: {out.stat().st_size // 1024} KB")
        browser.close()


if __name__ == "__main__":
    main()
