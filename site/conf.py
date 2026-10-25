# -*- coding: utf-8 -*-

import re

import ablog
from docutils import nodes
from docutils.parsers.rst import Directive

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
    # Home page favorites, in order: the first topo_featured_count are featured with their summary,
    # the rest listed by title further down. Hand-picked; edit freely.
    "topo_popular": [
        ("blog/2017/aug/2/pacman-rule-conferences",
         "When you stand in a group at a conference, leave room for one more. A simple rule for friendlier events."),
        ("blog/2025/apr/29/camino-de-costa-rica-recap",
         "Walking Costa Rica coast to coast without a guide: 165 miles and 30,000 feet of climbing in 14 days."),
        ("blog/2018/mar/9/one-percent-for-open-source",
         "A proposal: companies put 1% of a funding round or yearly profits into the open source they use."),
        ("blog/2023/feb/10/we-dont-do-that-here",
         "A short phrase that lets organizers hold the line on social norms without winning a debate every time."),
        ("blog/2017/jan/27/code-is-self-documenting",
         "Comments explain the why, and documentation does more than explain how the code works."),
        ("blog/2018/feb/7/the-post-i-never-published",
         "A draft from 2016, written while close to burn out on Read the Docs, shared to talk more openly about it."),
        ("blog/2019/sep/19/helping-first-time-conference-attendees-with-welcome-wagon",
         "How Write the Docs helps first-time attendees know what to expect, before and during the conference."),
    ],
    "topo_featured_count": 3,
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
        "searchbox.html",
    ],
}
# globaltoc_collapse = False

html_title = blog_title
html_favicon = "_static/img/favicon.svg"
html_static_path = ["_static"]

# Old pages that were folded into others: old docname -> where it now forwards.
topo_redirects = {
    "backpacking": "adventures",
    "bike": "adventures",
    "pct/thoughts": "pct/index",
}


def topo_redirect_pages(app):
    for old, new in topo_redirects.items():
        yield (old, {"redirect": new}, "topo/redirect.html")


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
    app.connect("html-collect-pages", topo_redirect_pages)
    app.add_directive("adventure-summary", AdventureSummary)
    app.connect("html-page-context", topo_year_letters)
    app.connect("doctree-resolved", topo_photo_rows)
