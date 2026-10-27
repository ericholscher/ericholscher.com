"""Fetch the shape of each place that has one, for the trip maps.

A place in site/_data/places.json is a pin unless it has a "shape", which says what it looked like
on the ground:

    "shape": {"osm": "R3724941"}                     a park or forest: its boundary in OpenStreetMap
                                                     (R relation, W way), from Nominatim, simplified
    "shape": {"trail": "john-muir-trail"}            a trail with a page: its route from trail_routes.json
    "shape": {"relation": 3094865}                   a whole waymarked route, walked end to end (thinned
                                                     to about 400 m steps, plenty at a trip's scale)
    "shape": {"route": [1116809, 360167],            a stretch of a waymarked route: the shortest way
              "from": [lat, lon], "to": [lat, lon]}  along those OpenStreetMap relations, as in
                                                     trail_routes.py

Only public data: boundaries and waymarked routes, never a GPS track. OpenStreetMap data is
© OpenStreetMap contributors, under the ODbL. Downloads are cached in .trail-cache/.

    uv run --group photos python scripts/trip_shapes.py

Writes site/_data/trip_shapes.json: each place's shape as GeoJSON geometry, by name. Rerun it after
adding a shape, then scripts/trip_topo.py to draw the maps.
"""

import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import trail_routes  # noqa: E402

DATA = ROOT / "site" / "_data"
OUTPUT = DATA / "trip_shapes.json"
NOMINATIM = "https://nominatim.openstreetmap.org/lookup?format=json&osm_ids={}&polygon_geojson=1&polygon_threshold=0.004"
ROUTE_STEP = 0.5  # miles between points on a route
TRAIL_EVERY = 4  # every 4th of a trail page's quarter-mile points
THIN = 0.004  # degrees, about 400 m: the least step kept along a whole route


def rounded(coords, digits=4):
    if isinstance(coords[0], (int, float)):
        return [round(coords[0], digits), round(coords[1], digits)]
    return [rounded(c, digits) for c in coords]


def area(osm_id):
    path = trail_routes.fetch(NOMINATIM.format(osm_id), trail_routes.CACHE / f"nominatim-{osm_id}.json")
    found = json.loads(path.read_text())
    if not found:
        raise SystemExit(f"Nominatim has no {osm_id}")
    geometry = found[0]["geojson"]
    return {"type": geometry["type"], "coordinates": rounded(geometry["coordinates"])}


def whole_route(rel):
    """Every way of a route relation (and of its stages, for a superroute), as a MultiLineString."""
    data = json.loads(trail_routes.fetch(trail_routes.OSM.format(rel), trail_routes.CACHE / f"relation-{rel}.json").read_text())["elements"]
    nodes = {e["id"]: (e["lon"], e["lat"]) for e in data if e["type"] == "node"}
    lines = []
    for e in data:
        if e["type"] == "way":
            line = [rounded(nodes[n], 3) for n in e["nodes"] if n in nodes]
            kept = line[:1]
            for i, p in enumerate(line[1:], 1):
                if i == len(line) - 1 or abs(p[0] - kept[-1][0]) + abs(p[1] - kept[-1][1]) > THIN:
                    kept.append(p)
            lines.append(kept)
        elif e["type"] == "relation" and e["id"] == rel:
            lines += [ln for m in e["members"] if m["type"] == "relation" for ln in whole_route(m["ref"])["coordinates"]]
    return {"type": "MultiLineString", "coordinates": [ln for ln in lines if len(ln) > 1]}


def route(shape):
    nodes, edges, _ = trail_routes.load_graph(shape["route"])
    start = trail_routes.nearest(nodes, edges, tuple(shape["from"]))
    end = trail_routes.nearest(nodes, edges, tuple(shape["to"]))
    line = [nodes[n] for n in trail_routes.shortest_path(edges, start, [end])]
    points, total = trail_routes.resample(line, ROUTE_STEP * trail_routes.METERS_PER_MILE)
    print(f"  {total / trail_routes.METERS_PER_MILE:.0f} miles")
    return {"type": "LineString", "coordinates": [[round(lon, 4), round(lat, 4)] for lat, lon in points]}


def main():
    places = json.loads((DATA / "places.json").read_text())
    routes = json.loads((DATA / "trail_routes.json").read_text())
    shapes = {}
    for p in places:
        shape = p.get("shape")
        if not shape:
            continue
        print(p["name"])
        if "osm" in shape:
            shapes[p["name"]] = area(shape["osm"])
        elif "relation" in shape:
            shapes[p["name"]] = whole_route(shape["relation"])
        elif "trail" in shape:
            track = routes[shape["trail"]]["track"]
            shapes[p["name"]] = {"type": "LineString", "coordinates": [[q[2], q[1]] for q in track[::TRAIL_EVERY] + track[-1:]]}
        else:
            shapes[p["name"]] = route(shape)
    OUTPUT.write_text(json.dumps(shapes, separators=(",", ":"), ensure_ascii=False) + "\n")
    print(f"{OUTPUT.relative_to(ROOT)}: {OUTPUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
