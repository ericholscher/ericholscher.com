# -*- coding: utf-8 -*-

import re

import ablog
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

extensions = [
    "ablog",
    "sphinx.ext.intersphinx",
    "notfound.extension",
    "sphinxext.opengraph",
    "myst_parser",
]
suppress_warnings = ["myst.header"]
blog_title = "Eric Holscher"
blog_path = "blog/archive"
blog_baseurl = "https://www.ericholscher.com"
post_date_format = "%b %d %Y"
post_show_prev_next = False
notfound_urls_prefix = '/'
ogp_site_url = blog_baseurl
ogp_image = "https://www.ericholscher.com/_static/img/opengraph.jpg"
ogp_use_first_image = True

# blog_authors = {
#     "Eric": ("Eric Holscher", "http://ericholscher.com"),
# }
# blog_default_author = "Eric"

# blog_locations = {
#     "Oregon": ("Somewhere, Oregon", "https://www.oregonhikers.org/field_guide/Main_Page"),
# }
# blog_default_location = "Oregon"

blog_feed_fulltext = True
blog_feed_length = 10
blog_feed_archives = True

templates_path = ["_templates"]
master_doc = "index"
project = blog_title
copyright = " Eric Holscher"
version = "1.0"
release = "1.0"
exclude_patterns = ["_build", "include/*"]
pygments_style = "sphinx"
import json
from pathlib import Path

_data = Path(__file__).parent / "_data"
html_context = {
    # Category landing pages: slug -> title and intro. Posts opt in with :category: <slug>.
    "topo_categories": {
        "documentation": ("Documentation", "How software gets explained: Read the Docs, Write the Docs, Sphinx, and the craft of docs."),
        "open-source": ("Open source", "Sustaining open source projects and the businesses around them."),
        "community": ("Community", "Conferences, events, and making rooms that are easier to walk into."),
        "code": ("Code", "Django, Python, and the tools of the trade. Much of it from the early years."),
        "outside": ("Outside", "Long trails, bike tours, and the places they go through."),
        "link-blog": ("Notes", "Short pointers to things worth reading, with a line or two of why."),
    },
    "topo_hikes": json.loads((_data / "hikes.json").read_text()),
    "topo_places": json.loads((_data / "places.json").read_text()),
}

html_theme_path = ["_themes"]
html_theme = "topo"
html_sidebars = {
    "**": [
        "sidebar/about.html",
        "sidebar/subscribe.html",
        "sidebar/archive.html",
        "sidebar/walking.html",
        "sidebar/elsewhere.html",
    ],
}
# globaltoc_collapse = False

html_title = blog_title
html_favicon = "_static/img/favicon.svg"
html_static_path = ["_static"]

# Redirects live in redirects.yml at the repo root, synced to Read the Docs by a GitHub workflow.
# Until that sync has a token, each redirect also gets a meta-refresh page at its old URL, unless
# a real page is still there. Read the Docs only redirects URLs that 404, so drop these pages
# once the sync is running.
def topo_redirect_pages(app):
    import yaml

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


# Favorite posts: the list lives in site/favorite-posts.rst, in a favorite-posts directive.
# That page shows every entry with its summary; the home page features the first few.
class FavoritePosts(SphinxDirective):
    """Each entry is a post's docname, with a one-line summary indented below it."""

    has_content = True
    option_spec = {"featured": directives.nonnegative_int}

    def run(self):
        items = []
        for line in self.content:
            if not line.strip():
                continue
            if line[0].isspace() and items:
                items[-1][1] = f"{items[-1][1]} {line.strip()}".strip()
            else:
                items.append([line.strip().strip("/"), ""])
        self.env.topo_favorites = {
            "docname": self.env.docname,
            "items": [tuple(i) for i in items],
            "featured": self.options.get("featured", 3),
        }
        return []


def topo_favorites_purge(app, env, docname):
    if getattr(env, "topo_favorites", {}).get("docname") == docname:
        del env.topo_favorites


def topo_favorites_merge(app, env, docnames, other):
    if hasattr(other, "topo_favorites"):
        env.topo_favorites = other.topo_favorites


def topo_favorites_outdated(app, env, added, changed, removed):
    # The home page shows the list too, so rebuild it when the list's page changes.
    doc = getattr(env, "topo_favorites", {}).get("docname")
    return [env.config.root_doc] if doc and doc in changed else []


def topo_favorites_context(app, pagename, templatename, context, doctree):
    favorites = getattr(app.env, "topo_favorites", {})
    context["topo_favorite_posts"] = favorites.get("items", [])
    context["topo_featured_count"] = favorites.get("featured", 3)
    context["topo_favorites_page"] = favorites.get("docname")


def topo_favorites_check(app, env):
    for doc, _ in getattr(env, "topo_favorites", {}).get("items", []):
        if doc not in env.found_docs:
            logging.getLogger(__name__).warning(
                "favorite-posts: no page %r", doc, location=env.topo_favorites["docname"]
            )


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
    app.connect("html-collect-pages", topo_redirect_pages)
    app.add_directive("favorite-posts", FavoritePosts)
    app.connect("env-purge-doc", topo_favorites_purge)
    app.connect("env-merge-info", topo_favorites_merge)
    app.connect("env-check-consistency", topo_favorites_check)
    app.connect("env-get-outdated", topo_favorites_outdated)
    app.connect("html-page-context", topo_favorites_context)
    app.add_directive("adventure-summary", AdventureSummary)
    app.connect("html-page-context", topo_year_letters)
    app.connect("doctree-resolved", topo_photo_rows)
