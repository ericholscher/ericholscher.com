"""Trace the footer's mountain skyline from real elevation data.

The footer ridgeline is the Cascades as seen from just east of Redmond, Oregon: Mt. Bachelor,
Broken Top, the Three Sisters, Mt. Washington, Black Butte, Three Fingered Jack, and Mt. Jefferson.
For each compass bearing across that view, the script walks outward over a digital elevation model
and keeps the highest angle above the horizon (allowing for the earth's curvature), which is the
skyline an eye at that spot would see.

Heights are then stretched to fit the footer's 1280x48 box: the foothills get the bottom 12px, and
everything above them fills the rest, so the peaks read at that size. Bearings stay to scale.

Elevation comes from the Terrain Tiles on AWS (Tilezen, terrarium format), which for this area is
USGS 3DEP data. Tiles are cached in .skyline-cache/.

    uv run --group photos python scripts/skyline.py

Writes site/_data/skyline.json: the polygon points for the footer SVG, and where each named peak's
summit lands, for the labels above it (see the footer in site/_themes/topo/layout.html).
"""

import json
import math
import urllib.request
from pathlib import Path

from PIL import Image

VIEW = (44.300, -121.080)  # east of Redmond, about 1,000 m up
EYE = 10  # metres above the ground
BEARINGS = (228, 312)  # Mt. Bachelor (234) through Mt. Jefferson (306)
RAYS = 1001
REACH = 90_000  # metres; Jefferson is about 71 km away
ZOOM = 12
CACHE = Path(__file__).resolve().parent.parent / ".skyline-cache"

WIDTH, HEIGHT = 1280, 48
FLOOR, FOOTHILLS = 0.2, 1.0  # degrees above level: where the drawing starts, and the foothills' top
FOOTHILL_PX, HEADROOM_PX = 12, 2
TOLERANCE = 0.35  # px, for simplifying the outline
OUTPUT = Path(__file__).resolve().parent.parent / "site" / "_data" / "skyline.json"

# Summits to label, south to north.
PEAKS = [
    ("Mt. Bachelor", 43.9792, -121.6886),
    ("Broken Top", 44.0827, -121.6993),
    ("South Sister", 44.1034, -121.7693),
    ("Middle Sister", 44.1484, -121.7836),
    ("North Sister", 44.1665, -121.7700),
    ("Mt. Washington", 44.3323, -121.8378),
    ("Black Butte", 44.3998, -121.6415),
    ("Three Fingered Jack", 44.4795, -121.8442),
    ("Mt. Jefferson", 44.6743, -121.7997),
]
LABEL_CHAR_PX = 6.7  # IBM Plex Mono at 11px, for spotting labels that would collide

EARTH = 6_371_000
REFRACTION = 0.13


def tile_xy(lat, lon):
    n = 2**ZOOM
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return x, y


tiles = {}


def tile(tx, ty):
    if (tx, ty) not in tiles:
        path = CACHE / f"{ZOOM}-{tx}-{ty}.png"
        if not path.exists():
            CACHE.mkdir(exist_ok=True)
            url = f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{ZOOM}/{tx}/{ty}.png"
            urllib.request.urlretrieve(url, path)
        tiles[tx, ty] = Image.open(path).convert("RGB").load()
    return tiles[tx, ty]


def height_at_pixel(px, py):
    r, g, b = tile(px // 256, py // 256)[px % 256, py % 256]
    return r * 256 + g + b / 256 - 32768


def elevation(lat, lon):
    """Bilinear elevation in metres."""
    x, y = tile_xy(lat, lon)
    x, y = x * 256, y * 256
    x0, y0 = int(x), int(y)
    fx, fy = x - x0, y - y0
    return (
        height_at_pixel(x0, y0) * (1 - fx) * (1 - fy)
        + height_at_pixel(x0 + 1, y0) * fx * (1 - fy)
        + height_at_pixel(x0, y0 + 1) * (1 - fx) * fy
        + height_at_pixel(x0 + 1, y0 + 1) * fx * fy
    )


def skyline():
    """The highest angle above level, in degrees, for each bearing."""
    lat0, lon0 = VIEW
    eye = elevation(lat0, lon0) + EYE
    angles = []
    for i in range(RAYS):
        bearing = math.radians(BEARINGS[0] + (BEARINGS[1] - BEARINGS[0]) * i / (RAYS - 1))
        best, d = -90.0, 500
        while d < REACH:
            lat = lat0 + math.degrees(d * math.cos(bearing) / EARTH)
            lon = lon0 + math.degrees(d * math.sin(bearing) / (EARTH * math.cos(math.radians(lat0))))
            drop = d * d / (2 * EARTH) * (1 - REFRACTION)
            best = max(best, math.degrees(math.atan2(elevation(lat, lon) - eye - drop, d)))
            d += 40 if d < 20_000 else 80
        angles.append(best)
    return angles


def to_points(angles):
    top = max(angles)
    points = []
    for i, angle in enumerate(angles):
        if angle < FOOTHILLS:
            h = max(0, (angle - FLOOR) / (FOOTHILLS - FLOOR)) * FOOTHILL_PX
        else:
            h = FOOTHILL_PX + (angle - FOOTHILLS) / (top - FOOTHILLS) * (HEIGHT - HEADROOM_PX - FOOTHILL_PX)
        points.append((WIDTH * i / (len(angles) - 1), HEIGHT - h))
    return points


def simplify(points):
    """Douglas-Peucker."""
    if len(points) < 3:
        return points
    (x0, y0), (x1, y1) = points[0], points[-1]
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    far, i = max((abs(dy * (x - x0) - dx * (y - y0)) / length, k) for k, (x, y) in enumerate(points[1:-1], 1))
    if far <= TOLERANCE:
        return [points[0], points[-1]]
    return simplify(points[: i + 1])[:-1] + simplify(points[i:])


def bearing_to(lat, lon):
    lat0, lon0 = VIEW
    dx = (lon - lon0) * math.cos(math.radians(lat0))
    return math.degrees(math.atan2(dx, lat - lat0)) % 360


def labels(points):
    """Each peak's x (as a percentage of the width), summit y, label row (so neighbors don't collide),
    and where its label ends at full scale (so a narrow screen can drop labels it would cut off)."""
    peaks, row_ends = [], [-1e9, -1e9]
    for name, lat, lon in PEAKS:
        x = WIDTH * (bearing_to(lat, lon) - BEARINGS[0]) / (BEARINGS[1] - BEARINGS[0])
        y = min((py for px, py in points if abs(px - x) <= 6), default=HEIGHT)  # the summit near that bearing
        half = len(name) * LABEL_CHAR_PX / 2 + 6
        row = 0 if x - half > row_ends[0] else 1
        row_ends[row] = x + half
        peaks.append({"name": name, "x": round(100 * x / WIDTH, 2), "y": round(y, 1), "row": row, "right": round(x + half)})
    return peaks


def main():
    full = to_points(skyline())
    points = simplify(full)
    coords = [f"0,{HEIGHT}"] + [f"{round(x)},{round(y, 1):g}" for x, y in points] + [f"{WIDTH},{HEIGHT}"]
    OUTPUT.write_text(json.dumps({"points": " ".join(coords), "peaks": labels(full)}, indent=2) + "\n")


if __name__ == "__main__":
    main()
