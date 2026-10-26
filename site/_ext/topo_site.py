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

import topo_trips

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


# The Adventures page is one list of trips by year, built from trips.json, hikes.json, and
# places.json by topo_trips.build (see that module for how entries land in trips). The world map
# and the long ones link into that list, so everything counts the same trips.
def topo_trip_log(app):
    data = app.topo_data
    trips, years, problems = topo_trips.build(data["topo_hikes"], data["topo_places"], data["topo_trips"])
    for problem in problems:
        logger.warning("trips.json: %s", problem)
    maps = Path(app.srcdir, "_static", "maps")
    for t in trips:
        if t["map"] and not (maps / f"{t['slug']}.svg").exists():
            logger.warning("No map for the trip %s: run scripts/trip_maps.py", t["slug"])
    data["topo_trip_list"] = trips
    data["topo_log"] = years


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
