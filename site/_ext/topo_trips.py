"""Trips: the one grouping the Adventures page is built on.

Every hikes.json entry lands in exactly one trip:

- a trip in trips.json that names it in "along" (within the trip's years),
- or, for a trip marked "home", that trip for the entry's year ("Close to home, 2024"),
- or a trip of its own, named after the entry.

A trip is listed once, under the year it started. Each trip with places gets a map cropped to them,
in its own projection (see trip_view); scripts/trip_maps.py draws the land for each one.

This module has no Sphinx imports, so scripts/trip_maps.py can use it too.
"""

import math
import re
import unicodedata

# Trip maps are this many times wider than tall, and at least this many degrees of latitude tall.
MAP_ASPECT = 2
MAP_MIN_SPAN = 8.0
SCALE = 10  # map units per degree of latitude


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def project(lon, lat, lat0):
    """Equirectangular around lat0, so places far from the equator keep their shape."""
    return lon * math.cos(math.radians(lat0)) * SCALE, -lat * SCALE


MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def span(entries):
    """When a trip ran, from its entries' dates: "May to October 2026", "December 2018 to March 2019".

    Empty when an entry has no month to go by (like "Summer 2012").
    """
    found = []
    for h in entries:
        words = re.findall(r"[A-Z][a-z]+|\d{4}", h["when"])
        months = [w for w in words if w in MONTHS]
        if not months:
            return ""
        year = int(h["year"])
        for w in words:
            if w.isdigit():
                year = int(w)
            elif w in MONTHS:
                found.append((year, MONTHS.index(w)))
    if not found:
        return ""
    (y0, m0), (y1, m1) = min(found), max(found)
    if (y0, m0) == (y1, m1):
        return f"{MONTHS[m0]} {y0}"
    if y0 == y1:
        return f"{MONTHS[m0]} {'and' if m1 == m0 + 1 else 'to'} {MONTHS[m1]} {y1}"
    return f"{MONTHS[m0]} {y0} to {MONTHS[m1]} {y1}"


def trip_view(pins):
    """The map for a trip's places: its middle latitude, and a viewBox around them."""
    lats = [p["lat"] for p in pins]
    lat0 = (min(lats) + max(lats)) / 2
    xy = [project(p["lon"], p["lat"], lat0) for p in pins]
    x0, x1 = min(x for x, _ in xy), max(x for x, _ in xy)
    y0, y1 = min(y for _, y in xy), max(y for _, y in xy)
    # Room around the pins, and more on the right, where their names go.
    w = (x1 - x0) * 1.2 + MAP_MIN_SPAN * SCALE * 0.6
    h = (y1 - y0) * 1.3 + MAP_MIN_SPAN * SCALE * 0.4
    h = max(h, MAP_MIN_SPAN * SCALE)
    w, h = max(w, h * MAP_ASPECT), max(h, w / MAP_ASPECT)
    cx, cy = (x0 + x1) / 2 + w * 0.05, (y0 + y1) / 2
    return {
        "lat0": round(lat0, 3),
        "box": [round(cx - w / 2, 1), round(cy - h / 2, 1), round(w, 1), round(h, 1)],
        "pins": [{"place": p, "x": round(x, 1), "y": round(y, 1)} for p, (x, y) in zip(pins, xy)],
    }


MIN_SPAN = 1.2  # degrees: the least a trip map shows across, so one small park still has context


def trip_geo(trip, shapes):
    """What a trip's topo map draws (scripts/trip_topo.py and trip-map.js): each place as its shape
    from trip_shapes.json (a park's boundary, a trail's route) or as a pin, and the bounds that fit
    them all, as west, south, east, north."""
    places, xs, ys = [], [], []

    def walk(coords):
        if isinstance(coords[0], (int, float)):
            xs.append(coords[0])
            ys.append(coords[1])
        else:
            for c in coords:
                walk(c)

    for p in trip["places"]:
        shape = shapes.get(p["name"])
        places.append({"name": p["name"], "kind": p["kind"], "lon": p["lon"], "lat": p["lat"], "shape": shape})
        walk(shape["coordinates"] if shape else [p["lon"], p["lat"]])
    west, east, south, north = min(xs), max(xs), min(ys), max(ys)
    if east - west < MIN_SPAN:
        west, east = (west + east - MIN_SPAN) / 2, (west + east + MIN_SPAN) / 2
    if north - south < MIN_SPAN / 2:
        south, north = (south + north - MIN_SPAN / 2) / 2, (south + north + MIN_SPAN / 2) / 2
    # A name goes on the side of its place toward the middle of the map, so it isn't cut off at an
    # edge: to the left of a place in the east, and above or below one near the top or bottom.
    for p in places:
        x = (p["lon"] - west) / ((east - west) or 1)
        y = (north - p["lat"]) / ((north - south) or 1)
        side = "right" if x > 0.6 else "left" if x < 0.4 else ""
        level = "top" if y < 0.2 else "bottom" if y > 0.8 else ""
        p["anchor"] = "-".join(filter(None, (level, side))) or "left"
    # Within the United States, its states give a sense of where; elsewhere, countries do.
    states = west > -125 and east < -66 and south > 24 and north < 50
    return {"bounds": [round(v, 4) for v in (west, south, east, north)], "places": places, "states": states}


def build(hikes, places, trips):
    """Group the entries and places into trips. Returns (trips, years, problems).

    Each entry gets "trip", its trip's slug, and each place "trips", the slugs of the trips it's in.
    Each trip gets "last", where its latest entry is in hikes.json (which runs oldest first), or -1.
    trips: every trip, newest first. years: newest first, each with its trips, its places, and the
    places in no trip. problems: names in trips.json that don't match places.json or hikes.json.
    """
    by_name = {p["name"]: p for p in places}
    problems = []

    def takes(t, h):
        return h["name"] in t.get("along", []) and (t.get("home") or not t.get("years") or int(h["year"]) in t["years"])

    for t in trips:
        for name in t["places"]:
            if name not in by_name:
                problems.append(f"{t['slug']} names a place not in places.json: {name}")
            elif t.get("years") and not set(t["years"]) & set(by_name[name].get("years", [])):
                problems.append(f"{t['slug']} has {name}, but not in {t['years']}")
        for name in t.get("along", []):
            if not any(takes(t, h) for h in hikes):
                problems.append(f"{t['slug']} names an entry not in hikes.json for its years: {name}")

    found = {}

    def trip(slug, **fields):
        if slug not in found:
            found[slug] = {"slug": slug, "entries": [], "places": [], "home": False, "solo": False, "last": -1, **fields}
        return found[slug]

    for order, h in enumerate(hikes):
        y = int(h["year"])
        t = next((t for t in trips if takes(t, h)), None)
        if t and t.get("home"):
            tr = trip(f"{t['slug']}-{y}", name=f"{t['name']}, {y}", when="", year=y, years=[y], home=True, order=order)
            tr["places"] = [by_name[n] for n in t["places"] if n in by_name and y in by_name[n].get("years", [])]
        elif t:
            years = t.get("years") or [y]
            tr = trip(t["slug"], name=t["name"], when=t.get("when", ""), year=min(years), years=years, order=order)
        else:
            tr = trip(slugify(f"{h['name']}-{y}"), name=h["name"], when=h["when"], year=y, years=[y], solo=True, order=order)
            # The place named after it, or noted with its name, from that year.
            tr["places"] = [p for p in places if h["name"] in (p["name"], p.get("note")) and y in p.get("years", [])]
        tr["entries"].append(h)
        tr["last"] = order
        h["trip"] = tr["slug"]
    # Trips with places but no entries, like a year's visit to Europe, or a year close to home.
    for t in trips:
        if t.get("home"):
            for n in t["places"]:
                for y in by_name.get(n, {}).get("years", []):
                    if f"{t['slug']}-{y}" not in found:
                        tr = trip(f"{t['slug']}-{y}", name=f"{t['name']}, {y}", when="", year=y, years=[y], home=True, order=len(hikes))
                        tr["places"] = [by_name[n] for n in t["places"] if n in by_name and y in by_name[n].get("years", [])]
        elif t.get("years") and t["slug"] not in found:
            trip(t["slug"], name=t["name"], when=t.get("when", ""), year=min(t["years"]), years=t["years"], order=len(hikes))
    for t in trips:
        if t["slug"] in found and not t.get("home"):
            found[t["slug"]]["places"] = [by_name[n] for n in t["places"] if n in by_name]

    listed = sorted(found.values(), key=lambda t: (-t["year"], t["order"]))
    for p in places:
        p["trips"] = []
    for t in listed:
        for p in t["places"]:
            p["trips"].append(t["slug"])
        # A trip of one entry, named for it, reads as that entry, whether or not trips.json lists it.
        t["solo"] = t["solo"] or len(t["entries"]) == 1 and t["entries"][0]["name"] == t["name"]
        # Without a "when" in trips.json, a trip runs from its first entry to its last. One entry
        # doesn't say how long a whole trip ran, unless the trip is that entry or a year at home.
        if not t["when"] and (t["home"] or len(t["entries"]) > 1):
            t["when"] = span(t["entries"])
        t["kinds"] = sorted({h["kind"] for h in t["entries"]})
        t["long"] = any(h.get("feature") for h in t["entries"])
        t["map"] = trip_view(t["places"]) if t["places"] else None
        t.pop("order")

    covered = {(p["name"], y) for t in listed for p in t["places"] for y in t["years"]}
    all_years = {t["year"] for t in listed} | {y for p in places for y in p.get("years", [])}
    years = []
    for y in sorted(all_years, reverse=True):
        here = [p for p in places if y in p.get("years", [])]
        years.append({
            "year": str(y),
            "trips": [t for t in listed if t["year"] == y],
            "places": here,
            "other": [p for p in here if (p["name"], y) not in covered],
        })
    return listed, years, problems
