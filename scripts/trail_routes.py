"""Trace each long trail's route from OpenStreetMap, with its elevation, for the trail pages.

Each trail in site/_data/trails.json names the OpenStreetMap route relations it follows and where
the walk started and ended. The script downloads those relations, joins their ways into one graph,
and takes the shortest path along them from the start to the end, so a walk that began partway
along a trail (the JMT from Cottonwood Pass, on the PCT) or followed two of them comes out as one
line. "spurs" are side trips drawn on the map but not counted, like the JMT's last miles up Mount
Whitney; a spur's own "relations" are the trails it takes off the route.

The route is the public trail, never a GPS track, so nothing here comes from Eric's own photos or
devices. Nights on the trail are trail miles in trails.json (see --nights in photo_trips.py).

Elevation comes from the Terrain Tiles on AWS (Tilezen, terrarium format), which for the US is
USGS 3DEP data, as in skyline.py. The named passes on the route come from the same OpenStreetMap
data, with their tagged elevations. OpenStreetMap data is © OpenStreetMap contributors, under the
ODbL; the trail page credits it. Downloads are cached in .trail-cache/.

    uv run --group photos python scripts/trail_routes.py

Writes site/_data/trail_routes.json: for each trail, a point every quarter mile (mile, latitude,
longitude, feet), the spurs, and the passes. The trail page is drawn from it at build time (see
site/_ext/topo_trails.py), so changing a trail's nights needs no rerun. Also writes a shaded relief
for each trail's map, site/_static/trails/<trail>-relief.webp, in the page's colors, cropped to the
map's box.
"""

import heapq
import json
import math
import sys
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "site" / "_ext"))

import topo_trails  # noqa: E402

TRAILS = ROOT / "site" / "_data" / "trails.json"
OUTPUT = ROOT / "site" / "_data" / "trail_routes.json"
RELIEF = ROOT / "site" / "_static" / "trails"
CACHE = ROOT / ".trail-cache"
OSM = "https://www.openstreetmap.org/api/0.6/relation/{}/full.json"
TERRAIN = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{}/{}/{}.png"
ZOOM = 12  # about 30 m per pixel in the Sierra, for the profile
RELIEF_ZOOM = 10  # about 120 m, for the relief
RELIEF_WIDTH = 1200  # pixels, for the map at up to 780px wide on a sharp screen
SUN = (315, 40)  # azimuth and altitude, in degrees: light from the northwest, as on paper maps
# The relief's colors: --paper on flat ground, toward --rule-strong in shadow and lighter in sun.
PAPER, SHADOW, SUNLIT = (0xF2, 0xEB, 0xDC), (0xA8, 0x98, 0x76), (0xFB, 0xF7, 0xEE)
STEP = 0.25  # miles between points on the route
SNAP_KM = 0.5  # a start, end, or spur must be this close to the trail
PASS_KM = 0.15  # a named pass within this of the route is on it
METERS_PER_MILE = 1609.344
EARTH = 6_371_000
USER_AGENT = "ericholscher.com trail maps (https://www.ericholscher.com/)"


def fetch(url, path):
    if not path.exists():
        CACHE.mkdir(exist_ok=True)
        print(f"Downloading {url}")
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=120) as r:
            path.write_bytes(r.read())
    return path


def meters(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return EARTH * 2 * math.asin(math.sqrt(h))


def load_graph(relations):
    """Every node on the relations' ways, and which nodes each one connects to, with distances."""
    nodes, edges, tags = {}, {}, {}
    for rel in relations:
        data = json.loads(fetch(OSM.format(rel), CACHE / f"relation-{rel}.json").read_text())["elements"]
        for e in data:
            if e["type"] == "node":
                nodes[e["id"]] = (e["lat"], e["lon"])
                if e.get("tags"):
                    tags[e["id"]] = e["tags"]
        for e in data:
            if e["type"] == "way":
                for a, b in zip(e["nodes"], e["nodes"][1:]):
                    d = meters(nodes[a], nodes[b])
                    edges.setdefault(a, {})[b] = d
                    edges.setdefault(b, {})[a] = d
    return nodes, edges, tags


def nearest(nodes, edges, point):
    best = min(edges, key=lambda n: meters(nodes[n], point))
    if meters(nodes[best], point) > SNAP_KM * 1000:
        raise SystemExit(f"{point} is {meters(nodes[best], point) / 1000:.1f} km from the trail")
    return best


def shortest_path(edges, start, goals):
    """Dijkstra from start to the nearest of goals, as a list of node ids."""
    goals = set(goals)
    dist, prev, queue = {start: 0}, {}, [(0, start)]
    while queue:
        d, n = heapq.heappop(queue)
        if n in goals:
            path = [n]
            while path[-1] != start:
                path.append(prev[path[-1]])
            return path[::-1]
        if d > dist[n]:
            continue
        for m, w in edges[n].items():
            if d + w < dist.get(m, math.inf):
                dist[m], prev[m] = d + w, n
                heapq.heappush(queue, (d + w, m))
    raise SystemExit("The start and end aren't connected along these relations")


def tile_xy(lat, lon, zoom):
    n = 2**zoom
    return (lon + 180) / 360 * n * 256, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n * 256


tiles = {}


def height_at_pixel(px, py, zoom):
    key = (zoom, px // 256, py // 256)
    if key not in tiles:
        path = fetch(TERRAIN.format(*key), CACHE / f"terrain-{key[0]}-{key[1]}-{key[2]}.png")
        tiles[key] = Image.open(path).convert("RGB").load()
    r, g, b = tiles[key][px % 256, py % 256]
    return r * 256 + g + b / 256 - 32768


def elevation(lat, lon, zoom=ZOOM):
    """Bilinear elevation in metres."""
    x, y = tile_xy(lat, lon, zoom)
    x0, y0 = int(x), int(y)
    fx, fy = x - x0, y - y0
    return (
        height_at_pixel(x0, y0, zoom) * (1 - fx) * (1 - fy)
        + height_at_pixel(x0 + 1, y0, zoom) * fx * (1 - fy)
        + height_at_pixel(x0, y0 + 1, zoom) * (1 - fx) * fy
        + height_at_pixel(x0 + 1, y0 + 1, zoom) * fx * fy
    )


def relief(track, out):
    """Shaded relief for the trail's map box, in the map's own projection."""
    lat0, (bx, by, bw, bh) = topo_trails.map_box(track)
    w, h = RELIEF_WIDTH, round(RELIEF_WIDTH * bh / bw)
    k = math.cos(math.radians(lat0)) * topo_trails.SCALE
    grid = [[elevation(-(by + bh * (j + 0.5) / h) / topo_trails.SCALE, (bx + bw * (i + 0.5) / w) / k, RELIEF_ZOOM)
             for i in range(w)] for j in range(h)]
    cell = bw / w / topo_trails.SCALE * 111_195  # metres per pixel, the same both ways
    az, alt = (math.radians(v) for v in SUN)
    flat = math.sin(alt)
    img = Image.new("RGB", (w, h))
    px = img.load()
    for j in range(h):
        for i in range(w):
            dzdx = (grid[j][min(i + 1, w - 1)] - grid[j][max(i - 1, 0)]) / (2 * cell)
            dzdy = (grid[max(j - 1, 0)][i] - grid[min(j + 1, h - 1)][i]) / (2 * cell)  # north is up
            slope = math.atan(math.hypot(dzdx, dzdy))
            aspect = math.atan2(-dzdx, -dzdy)
            shade = math.sin(alt) * math.cos(slope) + math.cos(alt) * math.sin(slope) * math.cos(az - aspect)
            t = max(-1.0, min(1.0, (flat - shade) * 2.0))
            to = SHADOW if t > 0 else SUNLIT
            t = abs(t) * (1 if t > 0 else 0.6)
            px[i, j] = tuple(round(a + (b - a) * t) for a, b in zip(PAPER, to))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "WEBP", quality=72, method=6)
    print(f"{out.relative_to(ROOT)}: {out.stat().st_size // 1024} KB")


def resample(points, step):
    """Points every `step` metres along a line, and the line's length."""
    out, total, next_at = [points[0]], 0.0, step
    for a, b in zip(points, points[1:]):
        d = meters(a, b)
        while d > 0 and total + d >= next_at:
            t = (next_at - total) / d
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
            next_at += step
        total += d
    if out[-1] != points[-1]:
        out.append(points[-1])
    return out, total


def coords(p, digits=5):
    return [round(p[0], digits), round(p[1], digits)]


def trace(trail):
    nodes, edges, tags = load_graph(trail["relations"])
    start = nearest(nodes, edges, (trail["start"]["lat"], trail["start"]["lon"]))
    end = nearest(nodes, edges, (trail["end"]["lat"], trail["end"]["lon"]))
    route = shortest_path(edges, start, [end])
    line = [nodes[n] for n in route]
    points, total = resample(line, STEP * METERS_PER_MILE)
    track = []
    for i, p in enumerate(points):
        mile = total / METERS_PER_MILE if i == len(points) - 1 else i * STEP
        track.append([round(mile, 2), *coords(p), round(elevation(*p) * 3.28084)])

    # Named passes within reach of the route, at the mile nearest them.
    on_route = set(route)
    passes = []
    for n, t in tags.items():
        if not t.get("name") or not (t.get("mountain_pass") == "yes" or t.get("natural") == "saddle"):
            continue
        if n not in on_route and min(meters(nodes[n], p) for p in points) > PASS_KM * 1000:
            continue
        mile = min(track, key=lambda q: meters(nodes[n], (q[1], q[2])))[0]
        feet = round(float(t["ele"]) * 3.28084) if t.get("ele", "").replace(".", "", 1).isdigit() else None
        passes.append({"name": t["name"], "mile": mile, "feet": feet})
    passes.sort(key=lambda p: p["mile"])

    spurs = []
    for spur in trail.get("spurs", []):
        # A spur can follow trails of its own; they join the graph only for it, so the route itself
        # never takes them as a shortcut.
        if spur.get("relations"):
            more_nodes, more_edges, _ = load_graph(trail["relations"] + spur["relations"])
            nodes, edges = {**nodes, **more_nodes}, more_edges
        tip = nearest(nodes, edges, (spur["lat"], spur["lon"]))
        path = shortest_path(edges, tip, on_route)
        spur_line, length = resample([nodes[n] for n in path], STEP * METERS_PER_MILE)
        spurs.append({"name": spur["name"], "miles": round(length / METERS_PER_MILE, 1), "line": [coords(p) for p in spur_line]})

    print(f"{trail['slug']}: {total / METERS_PER_MILE:.1f} miles, {len(passes)} passes, {len(spurs)} spurs")
    return {"miles": round(total / METERS_PER_MILE, 1), "track": track, "passes": passes, "spurs": spurs}


def main():
    trails = json.loads(TRAILS.read_text())
    routes = {t["slug"]: trace(t) for t in trails}
    for slug, route in routes.items():
        relief(route["track"], RELIEF / f"{slug}-relief.webp")
    OUTPUT.write_text(json.dumps(routes, separators=(",", ":")) + "\n")
    print(f"{OUTPUT.relative_to(ROOT)}: {OUTPUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
