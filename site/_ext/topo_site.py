"""The site's own Sphinx hooks: year letters, photo rows, the redirect stubs, and the data files.

conf.py is for settings only. Site data and copy live in their own files:
_data/*.json for the Adventures timeline, map, and topics, favorites.yml for the favorite posts,
and redirects.yml at the repo root for redirects.
"""

import json
import re
from pathlib import Path

import yaml

from docutils import nodes
from docutils.parsers.rst import Directive

# Data files in site/_data, each exposed to templates as topo_<name>.
TOPO_DATA = ["categories", "hikes", "places"]


def topo_data_context(app, pagename, templatename, context, doctree):
    context.update(app.topo_data)


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


def topo_year_letters(app, pagename, templatename, context, doctree):
    from ablog.blog import Blog

    published = {p.docname for p in Blog(app).posts}
    # Years with a published letter, for the Adventures page to link to.
    context["topo_year_letters"] = {
        m.group(1): doc for doc in published if (m := TOPO_YEAR_LETTER.match(doc))
    }
    m = TOPO_YEAR_LETTER.match(pagename)
    if m and TOPO_SUMMARY_SLOT in context.get("body", ""):
        html = app.builder.templates.render("topo/year-summary.html", {**context, "year": m.group(1)})
        context["body"] = context["body"].replace(TOPO_SUMMARY_SLOT, html, 1)


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
    data = Path(app.srcdir, "_data")
    app.topo_data = {f"topo_{n}": json.loads((data / f"{n}.json").read_text()) for n in TOPO_DATA}
    app.topo_data["topo_favorites"] = yaml.safe_load((data / "favorites.yml").read_text())
    app.connect("html-page-context", topo_data_context)
    app.connect("html-collect-pages", topo_redirect_pages)
    app.add_directive("adventure-summary", AdventureSummary)
    app.connect("html-page-context", topo_year_letters)
    app.connect("doctree-resolved", topo_photo_rows)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
