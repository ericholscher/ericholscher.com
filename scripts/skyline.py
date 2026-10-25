"""Trace the footer's mountain skyline from real elevation data.

The footer ridgeline is the Cascades as seen from the top of Pilot Butte in Bend, Oregon: Mt. Bachelor,
Broken Top, the Three Sisters, Mt. Washington, Three Fingered Jack, Black Butte, and Mt. Jefferson.
For each compass bearing across that view, the script walks outward over a digital elevation model
and keeps the highest angle above the horizon (allowing for the earth's curvature), which is the
skyline an eye at that spot would see.

Heights are then stretched to fit the footer's 1280x48 box: the foothills get the bottom 12px, and
everything above them fills the rest, so the peaks read at that size. Bearings stay to scale.

Elevation comes from the Terrain Tiles on AWS (Tilezen, terrarium format), which for this area is
USGS 3DEP data. Tiles are cached in .skyline-cache/.

    uv run --group photos python scripts/skyline.py

Prints the polygon points for the ``topo-ridge`` SVG in site/_themes/topo/layout.html.
"""

import math
import urllib.request
from pathlib import Path

from PIL import Image

VIEW = (44.0597, -121.2806)  # the summit of Pilot Butte
EYE = 2  # metres above the ground
BEARINGS = (248, 334)  # Mt. Bachelor (255) through Mt. Jefferson (329)
RAYS = 1001
REACH = 90_000  # metres; Jefferson is about 80 km away
ZOOM = 12
CACHE = Path(__file__).resolve().parent.parent / ".skyline-cache"

WIDTH, HEIGHT = 1280, 48
FLOOR, FOOTHILLS = 0.1, 1.6  # degrees above level: where the drawing starts, and the foothills' top
FOOTHILL_PX, HEADROOM_PX = 12, 2
TOLERANCE = 0.35  # px, for simplifying the outline

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


def main():
    points = simplify(to_points(skyline()))
    coords = [f"0,{HEIGHT}"] + [f"{round(x)},{round(y, 1):g}" for x, y in points] + [f"{WIDTH},{HEIGHT}"]
    print(" ".join(coords))


if __name__ == "__main__":
    main()
