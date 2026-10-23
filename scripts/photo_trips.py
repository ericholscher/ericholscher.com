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
      {"name": "Parents", "lat": 43.07, "lon": -89.40}
    ]

"km" defaults to --home-radius. For a one-off, pass --skip-near LAT,LON[,KM].

If your library is shared, other people's trips show up too; delete those rows.

Only dates, coordinates, place names, and scene labels are read. Filenames
and people are ignored, and nothing leaves your machine.
"""

import argparse
import collections
import csv
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
    return out, bool(place.get("ishome"))


def load_homes(path):
    try:
        with open(path) as f:
            return [(p["lat"], p["lon"]) for p in json.load(f) if p.get("kind") == "lived"]
    except (OSError, ValueError, KeyError):
        return []


def load_skips(path, default_km):
    """Places to leave out besides home, as ((lat, lon), km) pairs. A missing file means none."""
    try:
        with open(path) as f:
            entries = json.load(f)
    except FileNotFoundError:
        return []
    return [((float(e["lat"]), float(e["lon"])), float(e.get("km", default_km))) for e in entries]


def parse_near(value):
    """--skip-near LAT,LON[,KM]; a missing KM is filled in from --home-radius."""
    try:
        parts = [float(x) for x in value.split(",")]
    except ValueError:
        parts = []
    if len(parts) not in (2, 3):
        raise argparse.ArgumentTypeError(f"{value!r}: use LAT,LON or LAT,LON,KM")
    return (parts[0], parts[1]), parts[2] if len(parts) == 3 else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", help="JSON written by `osxphotos query --json`")
    ap.add_argument("--homes", default="site/_data/places.json", help="places.json; 'lived' entries count as home")
    ap.add_argument("--home-radius", type=float, default=15, help="km around a home to ignore (default 15)")
    ap.add_argument("--skip", default="photo-skip.json", help="local list of family and other places to ignore (default photo-skip.json)")
    ap.add_argument("--skip-near", action="append", default=[], type=parse_near, metavar="LAT,LON[,KM]", help="another place to ignore; repeatable")
    ap.add_argument("--merge-km", type=float, default=150, help="merge consecutive days closer than this (default 150)")
    ap.add_argument("--min-photos", type=int, default=5, help="drop trips with fewer photos (default 5)")
    ap.add_argument("--outdoor-only", action="store_true", help="keep trips that look outdoorsy")
    ap.add_argument("--year", help="only trips starting in this year")
    args = ap.parse_args()

    with open(args.export) as f:
        photos = json.load(f)
    skip = [(h, args.home_radius) for h in load_homes(args.homes)]
    skip += load_skips(args.skip, args.home_radius)
    skip += [(at, km if km is not None else args.home_radius) for at, km in args.skip_near]

    days = collections.defaultdict(list)
    skipped = 0
    for p in photos:
        c = coords(p)
        when = (p.get("date") or "")[:10]
        if not c or len(when) != 10:
            continue
        names, ishome = place_names(p)
        if ishome or any(haversine_km(c, at) <= km for at, km in skip):
            skipped += 1
            continue
        labels = {str(x).lower() for x in (p.get("labels") or [])}
        days[when].append((c, names, labels))

    # Merge consecutive, nearby days into trips.
    trips, current = [], None
    for day in sorted(days):
        pts = days[day]
        # Travel days mix far-apart places. Keep the photos near the day's median spot.
        med = (median(c[0] for c, _, _ in pts), median(c[1] for c, _, _ in pts))
        pts = [x for x in pts if haversine_km(x[0], med) <= args.merge_km] or pts
        centroid = (median(c[0] for c, _, _ in pts), median(c[1] for c, _, _ in pts))
        d = date.fromisoformat(day)
        if current and d - current["end"] <= timedelta(days=1) and haversine_km(centroid, current["last"]) <= args.merge_km:
            current["end"], current["last"] = d, centroid
            current["photos"].extend(pts)
        else:
            current = {"start": d, "end": d, "last": centroid, "photos": list(pts)}
            trips.append(current)

    out = csv.writer(sys.stdout)
    out.writerow(["start", "end", "days", "photos", "kind_guess", "name_guess", "where", "lat", "lon", "hiking_share", "top_labels"])
    kept = 0
    for t in trips:
        pts = t["photos"]
        if len(pts) < args.min_photos or (args.year and str(t["start"].year) != args.year):
            continue
        ndays = (t["end"] - t["start"]).days + 1
        share = lambda tags: sum(1 for _, _, l in pts if l & tags) / len(pts)
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
        lat = median(c[0] for c, _, _ in pts)
        lon = median(c[1] for c, _, _ in pts)
        # Name the trip from one photo near its middle, so city, state, and country agree.
        rep = min(pts, key=lambda x: haversine_km(x[0], (lat, lon)))[1]
        aoi = collections.Counter(n["area_of_interest"] for _, n, _ in pts if "area_of_interest" in n)
        name = (aoi.most_common(1)[0][0] if aoi else "") or rep.get("inland_water") or rep.get("region") or rep.get("city", "")
        where = ", ".join(x for x in (rep.get("city"), rep.get("state_province"), rep.get("country")) if x)
        outdoor = hiking
        labels = collections.Counter(x for _, _, l in pts for x in l).most_common(6)
        out.writerow([t["start"], t["end"], ndays, len(pts), kind, name, where, f"{lat:.3f}", f"{lon:.3f}",
                      f"{outdoor:.2f}", "; ".join(x for x, _ in labels)])
        kept += 1

    print(f"{len(photos)} photos read, {skipped} near home or a skipped place left out, {len(trips)} trips found, {kept} written",
          file=sys.stderr)


if __name__ == "__main__":
    main()
