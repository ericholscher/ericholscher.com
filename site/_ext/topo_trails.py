"""Trail pages: one page per long trail, drawn from trails.json, trail_routes.json, and hikes.json.

trails.json is edited by hand: which OpenStreetMap relations a walk followed, where it started and
ended, its nights as trail miles, and a few photos (in site/_static/photos/<trail>/, metadata
stripped by scripts/prepare_photos.py) with their date and trail mile. scripts/trail_routes.py turns that into trail_routes.json, a
point every quarter mile with its elevation, plus the passes on the way. This module turns both into
what the page draws: the route on a relief map, the elevation profile, and the passes and nights.

Labels sit over the map and profile in HTML, placed by percentage, so they stay readable at any
width; the drawings scale. This module has no Sphinx imports, so scripts/trail_routes.py can use it
to crop the relief to the same box.
"""

import math

MAP_ASPECT = 1.15  # the map is at least this much wider than tall
MAP_PAD = 0.12  # of the route's size, around it
SCALE = 100  # map units per degree of latitude
PROFILE_W, PROFILE_H = 1000, 200
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def project(lon, lat, lat0):
    return lon * math.cos(math.radians(lat0)) * SCALE, -lat * SCALE


def map_box(track):
    """The map's middle latitude and its viewBox, around the whole route."""
    lats = [p[1] for p in track]
    lat0 = (min(lats) + max(lats)) / 2
    xy = [project(p[2], p[1], lat0) for p in track]
    x0, x1 = min(x for x, _ in xy), max(x for x, _ in xy)
    y0, y1 = min(y for _, y in xy), max(y for _, y in xy)
    pad = max(x1 - x0, y1 - y0) * MAP_PAD
    w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    w, h = max(w, h * MAP_ASPECT), max(h, w / MAP_ASPECT)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return round(lat0, 4), [round(cx - w / 2, 2), round(cy - h / 2, 2), round(w, 2), round(h, 2)]


def path(points):
    return "M" + " ".join(f"{x:.2f} {y:.2f}" for x, y in points)


def nice_date(iso):
    y, m, d = (int(v) for v in iso.split("-"))
    return f"{MONTHS[m - 1]} {d}"


def itinerary(trail, miles, passes, nights, photos, spurs):
    """The walk day by day: where each day started and ended, in trail miles, and what was on it.

    Day N ends at night N; the last day ends at the end of the trail. A night in town keeps the
    day's miles where they were, since the walk out to town isn't on the route. A pass or side trip
    goes on the day whose miles reach it (or on its "date", for a side trip that gives one), and a
    photo on the day it was taken. Empty without nights, since then the days aren't known.
    """
    if not nights or not all(n.get("date") for n in nights):
        return []
    import datetime

    ends = [(n["date"], n) for n in nights]
    last_day = datetime.date.fromisoformat(nights[-1]["date"]) + datetime.timedelta(days=1)
    ends.append((last_day.isoformat(), None))
    days, at = [], 0.0
    for i, (date, night) in enumerate(ends, 1):
        end = miles if night is None else night.get("mile", at)
        end = at if end is None else end
        d = datetime.date.fromisoformat(date)
        span = (lambda m: at < m <= end) if i > 1 else (lambda m: 0 <= m <= end)
        days.append({
            "day": i,
            "date": date,
            "label": f"{d:%a}, {MONTHS[d.month - 1]} {d.day}",
            "start": round(at), "end": round(end), "miles": round(end - at),
            "from_pct": round(100 * at / miles, 2), "to_pct": round(100 * end / miles, 2),
            "passes": [p for p in passes if span(p["mile"])],
            "spurs": [s for s in spurs if (s["date"] == date if s["date"] else span(s["mile"]))],
            "photos": [p for p in photos if p.get("date") == date],
            "night": night,
        })
        at = end
    return days


def view(trail, route, hike):
    track = route["track"]
    lat0, box = map_box(track)
    bx, by, bw, bh = box

    def on_map(lon, lat, side=None):
        x, y = project(lon, lat, lat0)
        left = 100 * (x - bx) / bw
        # A label goes on the side with more room, so it isn't cut off at the map's edge, unless
        # trails.json says where ("label": left, right, above, or below) to keep it off the route.
        return {"x": round(x, 2), "y": round(y, 2), "left": round(left, 2), "top": round(100 * (y - by) / bh, 2),
                "side": side or ("left" if left > 58 else "right")}

    miles = route["miles"]

    def at_mile(mile):
        p = min(track, key=lambda q: abs(q[0] - mile))
        return {**on_map(p[2], p[1]), "feet": p[3], "pct": round(100 * mile / miles, 2), "lon": p[2], "lat": p[1]}

    # The profile: feet over miles, between round thousands.
    feet = [p[3] for p in track]
    floor, top = math.floor(min(feet) / 1000) * 1000, math.ceil(max(feet) / 1000) * 1000

    def py(ft):
        return PROFILE_H * (1 - (ft - floor) / (top - floor))

    pts = [(PROFILE_W * p[0] / miles, py(p[3])) for p in track]
    profile = path(pts) + f" L{PROFILE_W} {PROFILE_H} L0 {PROFILE_H}Z"
    step = 2000 if top - floor > 6000 else 1000
    grid = [{"feet": f, "top": round(100 * py(f) / PROFILE_H, 2)} for f in range(floor + step, top, step)]
    ticks = [{"mile": m, "pct": round(100 * m / miles, 2)} for m in range(0, int(miles), 50)]

    passes = []
    for i, p in enumerate(route["passes"]):
        here = at_mile(p["mile"])
        passes.append({**p, **here, "feet": p["feet"] or here["feet"], "row": i % 2})
    high = max(passes, key=lambda p: p["feet"], default=None)

    nights = []
    for n in trail.get("nights", []):
        night = {**n, "day": nice_date(n["date"]) if n.get("date") else ""}
        if n.get("mile") is not None:
            night.update(at_mile(n["mile"]))
        nights.append(night)

    photos = []
    for i, p in enumerate(trail.get("photos", []), 1):
        photo = {**p, "n": i, "day": nice_date(p["date"]) if p.get("date") else ""}
        if p.get("mile") is not None:
            photo.update(at_mile(p["mile"]))
        photos.append(photo)

    spurs = []
    for s, spur in zip(route["spurs"], trail.get("spurs", [])):
        lat, lon = s["line"][-1]  # where it leaves the route
        mile = min(track, key=lambda q: abs(q[1] - lat) + abs(q[2] - lon))[0]
        spurs.append({"name": s["name"], "miles": s["miles"], "mile": mile, "date": spur.get("date")})

    first, last = track[0], track[-1]
    days = itinerary(trail, miles, passes, nights, photos, spurs)
    return {
        "slug": trail["slug"],
        "hike": hike,
        "miles": miles,
        "start": {"name": trail["start"]["name"], **on_map(first[2], first[1], trail["start"].get("label")), "feet": first[3]},
        "end": {"name": trail["end"]["name"], **on_map(last[2], last[1], trail["end"].get("label")), "feet": last[3]},
        "map": {
            "box": box,
            "line": path(project(p[2], p[1], lat0) for p in track),
            "spurs": [
                {"name": s["name"], "miles": s["miles"], "line": path(project(lon, lat, lat0) for lat, lon in s["line"]),
                 **on_map(s["line"][0][1], s["line"][0][0], spur.get("label"))}
                for s, spur in zip(route["spurs"], trail.get("spurs", []))
            ],
        },
        "profile": {"d": profile, "line": path(pts), "w": PROFILE_W, "h": PROFILE_H, "floor": floor, "top": top, "grid": grid, "ticks": ticks},
        "passes": passes,
        "high": high,
        "nights": nights,
        "photos": photos,
        "days": days,
        # For the interactive map (topo/static/trail-map.js), in longitude and latitude.
        "geo": {
            "track": [[p[2], p[1], p[0], p[3]] for p in track],
            "spurs": [{"name": s["name"], "line": [[lon, lat] for lat, lon in s["line"]]} for s in route["spurs"]],
            "passes": [{"name": p["name"], "mile": p["mile"], "feet": p["feet"]} for p in passes],
            "nights": [{k: n[k] for k in ("night", "day", "mile", "lon", "lat") if k in n} for n in nights if "lon" in n],
            "photos": [{"n": p["n"], "file": f"photos/{trail['slug']}/{p['file']}", "day": p["day"], "mile": p.get("mile"), "lon": p.get("lon"), "lat": p.get("lat")}
                       for p in photos],
            "start": {"name": trail["start"]["name"], "lon": first[2], "lat": first[1]},
            "end": {"name": trail["end"]["name"], "lon": last[2], "lat": last[1]},
        },
    }


def build(trails, routes, hikes):
    """Each trail's page view, by slug. Returns (views, problems)."""
    views, problems = {}, []
    for t in trails:
        hike = next((h for h in hikes if h["name"] == t["entry"] and h["year"] == t["year"]), None)
        if not hike:
            problems.append(f"{t['slug']} names an entry not in hikes.json: {t['entry']}, {t['year']}")
        if t["slug"] not in routes:
            problems.append(f"No route for the trail {t['slug']}: run scripts/trail_routes.py")
            continue
        for n in t.get("nights", []):
            if n.get("mile") is not None and not 0 <= n["mile"] <= routes[t["slug"]]["miles"] + 1:
                problems.append(f"{t['slug']} night {n.get('night')} is at mile {n['mile']}, off the route")
        views[t["slug"]] = view(t, routes[t["slug"]], hike or {})
    return views, problems
