"""Draw the land for each trip's map on the Adventures page.

Each trip with places gets a map cropped to them (see trip_view in site/_ext/topo_trips.py, which
also places the pins). This script draws the land under those pins, from Natural Earth: 1:10m for a
trip that fits in a region, 1:50m for one that spans a continent. The rings are clipped to the map
and simplified to suit its size, so a map is a few tens of KB.

Natural Earth is public domain. Its GeoJSON is cached in .trip-maps-cache/.

    uv run python scripts/trip_maps.py

Writes site/_static/maps/<trip>.svg, and removes maps for trips that are gone. Run it again after
changing a trip's places in site/_data/trips.json or places.json; the build warns when a map is
missing. The pins are drawn by the page, over the map, so moving a pin within a map needs no rerun,
but a map whose box changed will be drawn with the wrong crop until it is.
"""

import json
import math
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "site" / "_ext"))

import topo_trips  # noqa: E402

DATA = ROOT / "site" / "_data"
OUTPUT = ROOT / "site" / "_static" / "maps"
CACHE = ROOT / ".trip-maps-cache"
SOURCE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_{}_land.geojson"
DETAILED_UNDER = 25  # degrees of latitude: a map shorter than this uses 1:10m land

# Matches .topo-land in topo.css; the map is an <img>, so it can't use the stylesheet.
SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" preserveAspectRatio="xMidYMid slice">'
    '<path d="{d}" fill="#DCD2BA" fill-rule="evenodd" stroke="#C9BD9F" stroke-width=".6" '
    'vector-effect="non-scaling-stroke"/></svg>\n'
)

_land = {}


def land(scale):
    if scale not in _land:
        path = CACHE / f"ne_{scale}_land.geojson"
        if not path.exists():
            CACHE.mkdir(exist_ok=True)
            print(f"Downloading Natural Earth {scale} land")
            urllib.request.urlretrieve(SOURCE.format(scale), path)
        _land[scale] = json.loads(path.read_text())
    return _land[scale]


def clip(pts, x0, y0, x1, y1):
    """Sutherland–Hodgman: the ring cut to the box."""
    edges = (
        (lambda p: p[0] >= x0, lambda a, b: (x0, a[1] + (b[1] - a[1]) * (x0 - a[0]) / (b[0] - a[0]))),
        (lambda p: p[0] <= x1, lambda a, b: (x1, a[1] + (b[1] - a[1]) * (x1 - a[0]) / (b[0] - a[0]))),
        (lambda p: p[1] >= y0, lambda a, b: (a[0] + (b[0] - a[0]) * (y0 - a[1]) / (b[1] - a[1]), y0)),
        (lambda p: p[1] <= y1, lambda a, b: (a[0] + (b[0] - a[0]) * (y1 - a[1]) / (b[1] - a[1]), y1)),
    )
    for inside, cross in edges:
        out = []
        for i, b in enumerate(pts):
            a = pts[i - 1]
            if inside(b):
                if not inside(a):
                    out.append(cross(a, b))
                out.append(b)
            elif inside(a):
                out.append(cross(a, b))
        pts = out
        if not pts:
            break
    return pts


def land_path(view):
    """The land inside a trip's map, as one SVG path."""
    x, y, w, h = view["box"]
    lat0 = view["lat0"]
    scale = "10m" if h / topo_trips.SCALE < DETAILED_UNDER else "50m"
    tol = max(w, h) / 500
    digits = 2 if tol < 0.5 else 1
    m = max(w, h) * 0.05
    x0, y0, x1, y1 = x - m, y - m, x + w + m, y + h + m
    # The box in degrees, so rings outside it are skipped without projecting them.
    k = math.cos(math.radians(lat0)) * topo_trips.SCALE
    lon_lo, lon_hi, lat_lo, lat_hi = x0 / k, x1 / k, -y1 / topo_trips.SCALE, -y0 / topo_trips.SCALE
    out = []
    for f in land(scale)["features"]:
        g = f["geometry"]
        for poly in g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]:
            for ring in poly:
                lons, lats = [p[0] for p in ring], [p[1] for p in ring]
                if max(lons) < lon_lo or min(lons) > lon_hi or max(lats) < lat_lo or min(lats) > lat_hi:
                    continue
                pts = clip([topo_trips.project(lon, lat, lat0) for lon, lat in ring], x0, y0, x1, y1)
                if len(pts) < 3:
                    continue
                xs, ys = [p[0] for p in pts], [p[1] for p in pts]
                if max(max(xs) - min(xs), max(ys) - min(ys)) < tol * 2:
                    continue
                keep = [pts[0]]
                for p in pts[1:]:
                    if abs(p[0] - keep[-1][0]) + abs(p[1] - keep[-1][1]) >= tol:
                        keep.append(p)
                if len(keep) >= 3:
                    out.append("M" + " ".join(f"{px:.{digits}f} {py:.{digits}f}" for px, py in keep) + "Z")
    return "".join(out)


def main():
    load = lambda name: json.loads((DATA / name).read_text())  # noqa: E731
    trips, _, problems = topo_trips.build(load("hikes.json"), load("places.json"), load("trips.json"))
    for problem in problems:
        print("trips.json:", problem)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    wanted = set()
    for t in trips:
        if not t["map"]:
            continue
        out = OUTPUT / f"{t['slug']}.svg"
        wanted.add(out)
        svg = SVG.format(box=" ".join(str(v) for v in t["map"]["box"]), d=land_path(t["map"]))
        if not out.exists() or out.read_text() != svg:
            out.write_text(svg)
            print(f"{out.relative_to(ROOT)}: {len(svg) // 1024} KB")
    for old in OUTPUT.glob("*.svg"):
        if old not in wanted:
            old.unlink()
            print(f"Removed {old.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
