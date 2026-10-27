#!/usr/bin/env python3
"""Turn an osxphotos JSON export into a short list of candidate trips.

Make the export on your Mac:

    uvx --python 3.12 osxphotos query --location --json > photo-places.json

Then:

    python3 scripts/photo_trips.py photo-places.json > trips.csv
    python3 scripts/photo_trips.py photo-places.json --outdoor-only --year 2021

Photos are grouped by day, photos near home are dropped, and consecutive days
close to each other are merged into one trip. Each trip gets the most common
place names, the Photos scene labels it saw, and a guessed kind
(bike, trek, backpacking, day-hike, coast, or visited).

Home is every "lived" place in site/_data/places.json. Family and other places
to leave out go in photo-skip.json next to your export, which git ignores so the
list stays on your machine:

    [
      {"name": "Family in Virginia", "lat": 39.15, "lon": -77.98, "km": 25},
      {"name": "Parents", "lat": 43.07, "lon": -89.40},
      {"place": "Virginia"},
      {"place": "*Beach*"}
    ]

A "lat"/"lon" entry skips photos within "km" of it (default --home-radius).
A "place" entry skips photos whose location has that name anywhere: city,
state, region, country, landmark, or the full address. It ignores case, must
match a whole name, and takes * wildcards, so "Virginia" leaves West Virginia
alone and "*Beach*" catches any beach town. For one-offs, pass
--skip-near LAT,LON[,KM] or --skip-place NAME.

Each row also lists the trip's main towns in "towns", in the order you reached
them, with the number of days photographed there. A town makes the list when it
had the most photos on some day or holds --town-share of the trip's photos, and
only the --towns biggest are kept, so drive-throughs drop out. To find the right
depth, run one year you remember and adjust those two flags until the rows read
the way you'd write them.

If your library is shared, other people's trips show up too; delete those rows.

For a long trail, --nights SLUG finds where each night was, as a trail mile, for the trail's
page. It reads only photos within --trail-km of the trail's route (site/_data/trail_routes.json,
from scripts/trail_routes.py) in the trail's year, takes the last photo of each day and the first
of the next, and puts the night halfway between them, rounded to a whole mile. A night spent off
the trail, more than --town-km away, gets the town's name instead. It prints the nights, and --write puts them in
site/_data/trails.json; no coordinates are printed or written:

    python3 scripts/photo_trips.py photo-places.json --nights john-muir-trail
    python3 scripts/photo_trips.py photo-places.json --nights john-muir-trail --write

Only dates, coordinates, place names, and scene labels are read. Filenames
and people are ignored, and nothing leaves your machine.
"""

import argparse
import collections
import csv
import fnmatch
import json
import math
import sys
from datetime import date, timedelta
from statistics import median

# Scene labels that point at hiking, at towns, and at the coast. "outdoor" and "sky"
# show up in city photos too, so they don't count as evidence of a hike.
HIKING = {
    "mountain", "mountain range", "landscape", "wilderness", "natural environment", "rocks",
    "hill", "fell", "glacier", "trail", "path", "forest", "waterfall", "canyon", "cliff",
    "tent", "camping", "backpack", "valley", "volcano", "meadow", "creek",
}
URBAN = {"building", "urban area", "city", "skyscraper", "art", "interior room", "crowd", "furniture", "statue", "arch"}
COAST = {"sea", "ocean", "beach", "coast", "water body"}
BIKE = {"bicycle", "bike", "cycling", "cyclist"}
TOWN_KEYS = ("city", "sub_locality")  # the first one present names a photo's town
PLACE_KEYS = ("area_of_interest", "inland_water", "body_of_water", "region", "city", "state_province", "country")


def haversine_km(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def coords(photo):
    lat, lon = photo.get("latitude"), photo.get("longitude")
    if lat is None and isinstance(photo.get("location"), (list, tuple)) and len(photo["location"]) == 2:
        lat, lon = photo["location"]
    if lat is None or lon is None:
        return None
    return float(lat), float(lon)


def place_names(photo):
    place = photo.get("place") or {}
    names = place.get("names") or {}
    out = {}
    for key in PLACE_KEYS:
        values = names.get(key) or []
        if isinstance(values, str):
            values = [values]
        if values:
            out[key] = values[0]
    town = next((v for v in (names.get(k) for k in TOWN_KEYS) if v), None)
    if town:
        out["town"] = town if isinstance(town, str) else town[0]
    return out, bool(place.get("ishome"))


def load_homes(path):
    try:
        with open(path) as f:
            return [(p["lat"], p["lon"]) for p in json.load(f) if p.get("kind") == "lived"]
    except (OSError, ValueError, KeyError):
        return []


def all_place_names(photo):
    """Every name Photos gives a photo's location, lowercased, for --skip-place matching."""
    place = photo.get("place") or {}
    out = {str(place["name"]).lower()} if place.get("name") else set()
    for values in (place.get("names") or {}).values():
        for v in [values] if isinstance(values, str) else values or []:
            out.add(str(v).lower())
    return out


def load_skips(path, default_km):
    """Places to leave out besides home: ((lat, lon), km) pairs and lowercased name patterns.
    A missing file means none."""
    try:
        with open(path) as f:
            entries = json.load(f)
    except FileNotFoundError:
        return [], []
    near = [((float(e["lat"]), float(e["lon"])), float(e.get("km", default_km))) for e in entries if "lat" in e]
    names = [str(e["place"]).lower() for e in entries if "place" in e]
    return near, names


def parse_near(value):
    """--skip-near LAT,LON[,KM]; a missing KM is filled in from --home-radius."""
    try:
        parts = [float(x) for x in value.split(",")]
    except ValueError:
        parts = []
    if len(parts) not in (2, 3):
        raise argparse.ArgumentTypeError(f"{value!r}: use LAT,LON or LAT,LON,KM")
    return (parts[0], parts[1]), parts[2] if len(parts) == 3 else None


def main_towns(pts, top, min_share):
    """The towns a trip spent real time in, in the order reached, as "Town (days)"."""
    by_day = collections.defaultdict(collections.Counter)
    for _, n, _, day in pts:
        if "town" in n:
            by_day[day][n["town"]] += 1
    total = collections.Counter()
    for counts in by_day.values():
        total.update(counts)
    if not total:
        return ""
    leaders = {counts.most_common(1)[0][0] for counts in by_day.values()}
    keep = [t for t, n in total.most_common() if t in leaders or n / len(pts) >= min_share][:top]
    first = {t: min(d for d, c in by_day.items() if t in c) for t in keep}
    days = {t: sum(1 for c in by_day.values() if t in c) for t in keep}
    return "; ".join(f"{t} ({days[t]})" for t in sorted(keep, key=first.get))


def trail_mile(c, track):
    """The mile of the route point nearest a photo and how far off it is in km, or (None, None)
    for a photo outside the trail's box."""
    if not (track["lat"][0] <= c[0] <= track["lat"][1] and track["lon"][0] <= c[1] <= track["lon"][1]):
        return None, None
    d, mile = min((haversine_km(c, (lat, lon)), m) for m, lat, lon, _ in track["points"])
    return mile, d


def nights(args, photos):
    """Each night on a trail, as a trail mile, from the last photo of a day and the first of the next."""
    routes = json.loads(open(args.trail_routes).read())
    trails = json.loads(open(args.trails).read())
    if args.nights not in routes:
        sys.exit(f"{args.nights} isn't in {args.trail_routes}; run scripts/trail_routes.py")
    trail = next(t for t in trails if t["slug"] == args.nights)
    points = routes[args.nights]["track"]
    pad = args.town_km / 100  # degrees, roughly, so most photos skip the distance check
    track = {
        "points": points,
        "lat": (min(p[1] for p in points) - pad, max(p[1] for p in points) + pad),
        "lon": (min(p[2] for p in points) - pad * 1.5, max(p[2] for p in points) + pad * 1.5),
    }
    # Photos says where a photo was by its nearest town, which in the backcountry can be one far
    # away over the crest, so a photo counts as in town only when it's --town-km off the trail.
    # Closer than that, a camp at a lake off the trail still gets the nearest trail mile.
    days = collections.defaultdict(list)  # date: [(time, mile or None, km off the trail, town)]
    for p in photos:
        c, when = coords(p), p.get("date") or ""
        if not c or not when.startswith(trail["year"]):
            continue
        mile, km = trail_mile(c, track)
        if km is not None and km > args.town_km:
            mile = None
        town = place_names(p)[0].get("town", "")
        days[when[:10]].append((when, mile, km, town))
    on_trail = sorted(d for d, pts in days.items() if any(k is not None and k <= args.trail_km for _, _, k, _ in pts))
    if not on_trail:
        sys.exit(f"No photos within {args.trail_km} km of the {trail['entry']} in {trail['year']}")
    # The walk: the longest run of days with photos on the trail, allowing a day or two without.
    runs, run = [], [on_trail[0]]
    for a, b in zip(on_trail, on_trail[1:]):
        if (date.fromisoformat(b) - date.fromisoformat(a)).days <= 3:
            run.append(b)
        else:
            runs.append(run)
            run = [b]
    runs.append(run)
    walk = max(runs, key=lambda r: (date.fromisoformat(r[-1]) - date.fromisoformat(r[0])).days)
    first, last = date.fromisoformat(walk[0]), date.fromisoformat(walk[-1])
    print(f"{trail['entry']}: {first} to {last}, {(last - first).days + 1} days", file=sys.stderr)

    out, d = [], first
    while d < last:
        tonight, tomorrow = sorted(days.get(d.isoformat(), [])), sorted(days.get((d + timedelta(days=1)).isoformat(), []))
        evening = next((m for _, m, _, _ in reversed(tonight) if m is not None), None)
        morning = next((m for _, m, _, _ in tomorrow if m is not None), None)
        # A night in town: the day's last photo and the next day's first are far off the trail.
        town = tonight[-1][3] if tonight and tonight[-1][1] is None and (not tomorrow or tomorrow[0][1] is None) else ""
        night = {"night": len(out) + 1, "date": d.isoformat()}
        if town:
            night["town"] = town
        elif evening is not None and morning is not None:
            night["mile"] = round((evening + morning) / 2)
        elif evening is not None or morning is not None:
            night["mile"] = round(evening if evening is not None else morning)
        out.append(night)
        print(f"Night {night['night']:>2}  {night['date']}  "
              + (f"mile {night['mile']}" if "mile" in night else night.get("town") or "no photos"), file=sys.stderr)
        d += timedelta(days=1)
    if args.write:
        trail["nights"] = out
        with open(args.trails, "w") as f:
            f.write(json.dumps(trails, indent=2) + "\n")
        print(f"Wrote {len(out)} nights to {args.trails}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", help="JSON written by `osxphotos query --json`")
    ap.add_argument("--homes", default="site/_data/places.json", help="places.json; 'lived' entries count as home")
    ap.add_argument("--home-radius", type=float, default=15, help="km around a home to ignore (default 15)")
    ap.add_argument("--skip", default="photo-skip.json", help="local list of family and other places to ignore (default photo-skip.json)")
    ap.add_argument("--skip-near", action="append", default=[], type=parse_near, metavar="LAT,LON[,KM]", help="another place to ignore; repeatable")
    ap.add_argument("--skip-place", action="append", default=[], metavar="NAME", help="ignore photos at a place with this name (* wildcards); repeatable")
    ap.add_argument("--merge-km", type=float, default=150, help="merge consecutive days closer than this (default 150)")
    ap.add_argument("--towns", type=int, default=3, help="most towns to list per trip (default 3)")
    ap.add_argument("--town-share", type=float, default=0.2,
                    help="list a town holding this share of a trip's photos even if it never led a day (default 0.2)")
    ap.add_argument("--min-photos", type=int, default=5, help="drop trips with fewer photos (default 5)")
    ap.add_argument("--outdoor-only", action="store_true", help="keep trips that look outdoorsy")
    ap.add_argument("--year", help="only trips starting in this year")
    ap.add_argument("--nights", metavar="SLUG", help="find each night on this trail from trails.json instead of listing trips")
    ap.add_argument("--trail-km", type=float, default=2, help="with --nights, photos this close to the trail find the walk's days (default 2)")
    ap.add_argument("--town-km", type=float, default=8,
                    help="with --nights, a night this far off the trail is named for its town instead of a mile (default 8)")
    ap.add_argument("--trails", default="site/_data/trails.json", help="with --nights, the trails (default site/_data/trails.json)")
    ap.add_argument("--trail-routes", default="site/_data/trail_routes.json", help="with --nights, their routes")
    ap.add_argument("--write", action="store_true", help="with --nights, write the nights into --trails")
    args = ap.parse_args()

    with open(args.export) as f:
        photos = json.load(f)
    if args.nights:
        return nights(args, photos)
    skip = [(h, args.home_radius) for h in load_homes(args.homes)]
    near, skip_names = load_skips(args.skip, args.home_radius)
    skip += near
    skip_names += [n.lower() for n in args.skip_place]
    skip += [(at, km if km is not None else args.home_radius) for at, km in args.skip_near]

    days = collections.defaultdict(list)
    skipped = 0
    for p in photos:
        c = coords(p)
        when = (p.get("date") or "")[:10]
        if not c or len(when) != 10:
            continue
        names, ishome = place_names(p)
        if (ishome or any(haversine_km(c, at) <= km for at, km in skip)
                or skip_names and any(fnmatch.fnmatchcase(n, pat) for n in all_place_names(p) for pat in skip_names)):
            skipped += 1
            continue
        labels = {str(x).lower() for x in (p.get("labels") or [])}
        days[when].append((c, names, labels, when))

    # Merge consecutive, nearby days into trips.
    trips, current = [], None
    for day in sorted(days):
        pts = days[day]
        # Travel days mix far-apart places. Keep the photos near the day's median spot.
        med = (median(c[0] for c, *_ in pts), median(c[1] for c, *_ in pts))
        pts = [x for x in pts if haversine_km(x[0], med) <= args.merge_km] or pts
        centroid = (median(c[0] for c, *_ in pts), median(c[1] for c, *_ in pts))
        d = date.fromisoformat(day)
        if current and d - current["end"] <= timedelta(days=1) and haversine_km(centroid, current["last"]) <= args.merge_km:
            current["end"], current["last"] = d, centroid
            current["photos"].extend(pts)
        else:
            current = {"start": d, "end": d, "last": centroid, "photos": list(pts)}
            trips.append(current)

    out = csv.writer(sys.stdout)
    out.writerow(["start", "end", "days", "photos", "kind_guess", "name_guess", "where", "towns", "lat", "lon", "hiking_share", "top_labels"])
    kept = 0
    for t in trips:
        pts = t["photos"]
        if len(pts) < args.min_photos or (args.year and str(t["start"].year) != args.year):
            continue
        ndays = (t["end"] - t["start"]).days + 1
        share = lambda tags: sum(1 for _, _, l, _ in pts if l & tags) / len(pts)
        hiking, urban, coast, bike = share(HIKING), share(URBAN), share(COAST), share(BIKE)
        if args.outdoor_only and hiking < 0.25 and bike < 0.15:
            continue
        if bike >= 0.15:
            kind = "bike"
        elif hiking >= 0.35 and urban < 0.3:
            kind = "trek" if ndays >= 5 else "backpacking" if ndays >= 2 else "day-hike"
        elif coast >= 0.3:
            kind = "coast"
        else:
            kind = "visited"
        lat = median(c[0] for c, *_ in pts)
        lon = median(c[1] for c, *_ in pts)
        # Name the trip from one photo near its middle, so city, state, and country agree.
        rep = min(pts, key=lambda x: haversine_km(x[0], (lat, lon)))[1]
        aoi = collections.Counter(n["area_of_interest"] for _, n, _, _ in pts if "area_of_interest" in n)
        name = (aoi.most_common(1)[0][0] if aoi else "") or rep.get("inland_water") or rep.get("region") or rep.get("city", "")
        where = ", ".join(x for x in (rep.get("city"), rep.get("state_province"), rep.get("country")) if x)
        outdoor = hiking
        labels = collections.Counter(x for _, _, l, _ in pts for x in l).most_common(6)
        out.writerow([t["start"], t["end"], ndays, len(pts), kind, name, where, main_towns(pts, args.towns, args.town_share), f"{lat:.3f}", f"{lon:.3f}",
                      f"{outdoor:.2f}", "; ".join(x for x, _ in labels)])
        kept += 1

    print(f"{len(photos)} photos read, {skipped} near home or a skipped place left out, {len(trips)} trips found, {kept} written",
          file=sys.stderr)


if __name__ == "__main__":
    main()
