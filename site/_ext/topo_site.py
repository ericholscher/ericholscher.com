"""The site's own Sphinx hooks: year letters, photo rows, the redirect stubs, and the data files.

conf.py is for settings only. Site data and copy live in their own files: _data/ for the
Adventures timeline, map, topics, and favorite posts, and redirects.yml at the repo root.
"""

import datetime
import os
import re
from pathlib import Path

import yaml
from sphinx.util import logging

from docutils import nodes
from docutils.parsers.rst import Directive

logger = logging.getLogger(__name__)


def topo_data_context(app, pagename, templatename, context, doctree):
    context.update(app.topo_data)


# The footer's build stamp: when the site was built and, on Read the Docs, from which commit.
def topo_build_stamp(app):
    commit = os.environ.get("READTHEDOCS_GIT_COMMIT_HASH", "")
    repo = os.environ.get("READTHEDOCS_GIT_CLONE_URL", "").removesuffix(".git")
    app.topo_data["topo_build"] = {
        "date": datetime.date.today(),
        "commit": commit[:7],
        "url": f"{repo}/commit/{commit}" if commit and repo.startswith("https://github.com/") else "",
    }


# Redirects live in redirects.yml at the repo root, synced to Read the Docs by a GitHub workflow.
# Until that sync has a token, each redirect also gets a meta-refresh page at its old URL, unless
# a real page is still there. Read the Docs only redirects URLs that 404, so drop these pages
# once the sync is running.
def topo_redirect_pages(app):
    redirects = yaml.safe_load((Path(app.confdir).parent / "redirects.yml").read_text())
    for r in redirects:
        old, new = (r[k].strip("/") for k in ("from_url", "to_url"))
        docs = app.env.found_docs
        if r["type"] == "page" and old not in docs and f"{old}/index" not in docs:
            if f"{new}/index" in docs:
                new = f"{new}/index"
            yield (old, {"redirect": new or app.config.root_doc}, "topo/redirect.html")


# Year letters: site/adventures/<year>.md, one story per year with photos for each month.
# A letter is an ABlog post (unlisted draft until its post directive has a date), and the
# adventure-summary directive marks where the year's trips and map are filled in.
TOPO_YEAR_LETTER = re.compile(r"^adventures/(\d{4})$")
TOPO_SUMMARY_SLOT = '<div class="topo-year-summary-slot"></div>'


class AdventureSummary(Directive):
    """The year's trips and a map of its places, from hikes.json and places.json."""

    def run(self):
        return [nodes.raw("", TOPO_SUMMARY_SLOT, format="html")]


def topo_year_summary(app, pagename, templatename, context, doctree):
    m = TOPO_YEAR_LETTER.match(pagename)
    if m and TOPO_SUMMARY_SLOT in context.get("body", ""):
        html = app.builder.templates.render("topo/year-summary.html", {**context, "year": m.group(1)})
        context["body"] = context["body"].replace(TOPO_SUMMARY_SLOT, html, 1)


# Excerpts on the home page: a post's opening text, ended at the last full sentence that fits,
# so it doesn't stop mid-thought. A first sentence too long to fit falls back to a word break.
TOPO_SENTENCE_END = re.compile(r"[.!?][\"”’)]*(?=\s)")


def topo_excerpt(text, limit=220):
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    ends = [m.end() for m in TOPO_SENTENCE_END.finditer(text[: limit + 1])]
    if ends and ends[-1] >= limit // 3:
        return text[: ends[-1]]
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "…"


# Trips in _data/trips.json group the places (from places.json) and the entries along the way
# (from hikes.json, within the trip's years; a trip with no years takes the named entries from any
# year). The map steps through these trips, and the year-by-year log groups each year by them, so
# both show the same trips and counts: topo_log has, per year, its trips (and each entry that's in
# no trip, on its own), each trip's places from that year, and the places that are in no trip.
# A name that doesn't match would quietly drop out of both, so say so.
def topo_trip_log(app):
    data = app.topo_data
    places = {p["name"]: p for p in data["topo_places"]}
    hikes, trips = data["topo_hikes"], data["topo_trips"]

    def takes(t, h):
        return h["name"] in t.get("along", []) and (not t.get("years") or int(h["year"]) in t["years"])

    for t in trips:
        years = set(t.get("years", []))
        for name in t["places"]:
            p = places.get(name)
            if not p:
                logger.warning("trips.json: %s names a place not in places.json: %s", t["slug"], name)
            elif years and not years & set(p.get("years", [])):
                logger.warning("trips.json: %s has %s, but not in %s", t["slug"], name, sorted(years))
        for name in t.get("along", []):
            if not any(takes(t, h) for h in hikes):
                logger.warning("trips.json: %s names a trip not in hikes.json for its years: %s", t["slug"], name)

    years = {int(h["year"]) for h in hikes} | {y for p in places.values() for y in p.get("years", [])}
    log = []
    for y in sorted(years, reverse=True):
        groups = {}
        for h in hikes:
            if int(h["year"]) == y:
                t = next((t for t in trips if takes(t, h)), None)
                g = groups.setdefault(t["slug"] if t else id(h), {"trip": t, "entries": [], "places": []})
                g["entries"].append(h)
        for t in trips:
            here = [places[n] for n in t["places"] if n in places and y in places[n].get("years", [])]
            if here and (y in t.get("years", []) or t["slug"] in groups):
                groups.setdefault(t["slug"], {"trip": t, "entries": [], "places": []})["places"] = here
        # An entry on its own takes the place of the same name, if there is one.
        for g in groups.values():
            if not g["trip"] and g["entries"][0]["name"] in places:
                p = places[g["entries"][0]["name"]]
                g["places"] = [p] if y in p.get("years", []) else []
        named = {p["name"] for g in groups.values() for p in g["places"]}
        # In the order they happened: a trip carried over from last year first, then by first entry.
        order = list(groups.values())
        order.sort(key=lambda g: 0 if g["trip"] and min(g["trip"].get("years") or [y]) < y else 1)
        log.append({
            "year": str(y),
            "groups": order,
            "places": [p for p in data["topo_places"] if y in p.get("years", [])],
            "other": [p for p in data["topo_places"] if y in p.get("years", []) and p["name"] not in named],
        })
    data["topo_log"] = log
    # Every trip once, counting each entry that's in no trip as its own, for the map's overview.
    data["topo_trip_count"] = len(trips) + sum(1 for yr in log for g in yr["groups"] if not g["trip"])


def topo_template_filters(app):
    if hasattr(app.builder, "templates"):
        app.builder.templates.environment.filters["topo_excerpt"] = topo_excerpt


def topo_photo_rows(app, doctree, docname):
    """Size each photo in a topo-photos row by its aspect ratio, so the row shares one height uncropped."""
    import imagesize

    for row in doctree.findall(nodes.container):
        if "topo-photos" not in row["classes"]:
            continue
        figures = [f for f in row.children if isinstance(f, nodes.figure)]
        ratios = []
        for fig in figures:
            img = next(fig.findall(nodes.image), None)
            src = img and img.get("candidates", {}).get("*")
            w, h = imagesize.get(str(Path(app.srcdir, src))) if src else (-1, -1)
            ratios.append(w / h if w > 0 and h > 0 else None)
        if len(figures) < 2 or None in ratios:
            continue
        gaps = (len(figures) - 1) * 12  # matches the row's gap in topo.css
        for fig, r in zip(figures, ratios):
            fig["width"] = f"calc((100% - {gaps}px) * {r / sum(ratios):.4f})"


def setup(app):
    # Each file in site/_data is exposed to templates as topo_<name>. YAML is a superset of JSON.
    app.topo_data = {f"topo_{f.stem}": yaml.safe_load(f.read_text()) for f in Path(app.srcdir, "_data").iterdir()}
    topo_build_stamp(app)
    app.connect("html-page-context", topo_data_context)
    app.connect("html-collect-pages", topo_redirect_pages)
    app.add_directive("adventure-summary", AdventureSummary)
    app.connect("html-page-context", topo_year_summary)
    app.connect("doctree-resolved", topo_photo_rows)
    app.connect("builder-inited", topo_template_filters)
    app.connect("builder-inited", topo_trip_log)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
