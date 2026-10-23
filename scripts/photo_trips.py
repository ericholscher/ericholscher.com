#!/usr/bin/env python3
"""Turn an osxphotos JSON export into a short list of candidate trips.

Make the export on your Mac:

    uvx --python 3.12 osxphotos query --location --json > photo-places.json

Then:

    python3 scripts/photo_trips.py photo-places.json > trips.csv
    python3 scripts/photo_trips.py photo-places.json --outdoor-only --year 2021

Photos are grouped by day, days near home are dropped, and consecutive days
close to each other are merged into one trip. Each trip gets the most common
place names, the Photos scene labels it saw, and a guessed kind
(bike, thru-hike, backpacking, day-hike, or visited).

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

OUTDOOR = {
    "mountain", "hiking", "trail", "forest", "tree", "snow", "glacier", "lake", "river",
    "waterfall", "canyon", "cliff", "rock", "desert", "tent", "camping", "backpack",
    "hill", "valley", "wilderness", "volcano", "meadow", "creek", "sky", "outdoor",
}
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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", help="JSON written by `osxphotos query --json`")
    ap.add_argument("--homes", default="site/_data/places.json", help="places.json; 'lived' entries count as home")
    ap.add_argument("--home-radius", type=float, default=15, help="km around a home to ignore (default 15)")
    ap.add_argument("--merge-km", type=float, default=150, help="merge consecutive days closer than this (default 150)")
    ap.add_argument("--min-photos", type=int, default=5, help="drop trips with fewer photos (default 5)")
    ap.add_argument("--outdoor-only", action="store_true", help="keep trips that look outdoorsy")
    ap.add_argument("--year", help="only trips starting in this year")
    args = ap.parse_args()

    with open(args.export) as f:
        photos = json.load(f)
    homes = load_homes(args.homes)

    days = collections.defaultdict(list)
    skipped_home = 0
    for p in photos:
        c = coords(p)
        when = (p.get("date") or "")[:10]
        if not c or len(when) != 10:
            continue
        names, ishome = place_names(p)
        if ishome or any(haversine_km(c, h) <= args.home_radius for h in homes):
            skipped_home += 1
            continue
        labels = {str(x).lower() for x in (p.get("labels") or [])}
        days[when].append((c, names, labels))

    # Merge consecutive, nearby days into trips.
    trips, current = [], None
    for day in sorted(days):
        pts = days[day]
        centroid = (sum(c[0] for c, _, _ in pts) / len(pts), sum(c[1] for c, _, _ in pts) / len(pts))
        d = date.fromisoformat(day)
        if current and d - current["end"] <= timedelta(days=1) and haversine_km(centroid, current["last"]) <= args.merge_km:
            current["end"], current["last"] = d, centroid
            current["photos"].extend(pts)
        else:
            current = {"start": d, "end": d, "last": centroid, "photos": list(pts)}
            trips.append(current)

    out = csv.writer(sys.stdout)
    out.writerow(["start", "end", "days", "photos", "kind_guess", "name_guess", "where", "lat", "lon", "outdoor_share", "top_labels"])
    kept = 0
    for t in trips:
        pts = t["photos"]
        if len(pts) < args.min_photos or (args.year and str(t["start"].year) != args.year):
            continue
        ndays = (t["end"] - t["start"]).days + 1
        outdoor = sum(1 for _, _, l in pts if l & OUTDOOR) / len(pts)
        bike = sum(1 for _, _, l in pts if l & BIKE) / len(pts)
        if args.outdoor_only and outdoor < 0.3:
            continue
        if bike >= 0.15:
            kind = "bike"
        elif outdoor >= 0.5 and ndays >= 5:
            kind = "thru-hike"
        elif outdoor >= 0.5 and ndays >= 2:
            kind = "backpacking"
        elif outdoor >= 0.5:
            kind = "day-hike"
        else:
            kind = "visited"
        counts = {k: collections.Counter(n[k] for _, n, _ in pts if k in n) for k in PLACE_KEYS}
        top = lambda k: counts[k].most_common(1)[0][0] if counts[k] else ""
        name = top("area_of_interest") or top("inland_water") or top("region") or top("city")
        where = ", ".join(x for x in (top("city"), top("state_province"), top("country")) if x)
        lat = sum(c[0] for c, _, _ in pts) / len(pts)
        lon = sum(c[1] for c, _, _ in pts) / len(pts)
        labels = collections.Counter(x for _, _, l in pts for x in l).most_common(6)
        out.writerow([t["start"], t["end"], ndays, len(pts), kind, name, where, f"{lat:.3f}", f"{lon:.3f}",
                      f"{outdoor:.2f}", "; ".join(x for x, _ in labels)])
        kept += 1

    print(f"{len(photos)} photos read, {skipped_home} near home skipped, {len(trips)} trips found, {kept} written",
          file=sys.stderr)


if __name__ == "__main__":
    main()
