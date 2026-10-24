# -*- coding: utf-8 -*-

import ablog

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
        ("blog/2023/feb/10/we-dont-do-that-here",
         "A short phrase that lets organizers hold the line on social norms without winning a debate every time."),
        ("blog/2025/apr/29/camino-de-costa-rica-recap",
         "Walking Costa Rica coast to coast without a guide: 165 miles and 30,000 feet of climbing in 14 days."),
        ("blog/2018/mar/9/one-percent-for-open-source",
         "A proposal: companies put 1% of a funding round or yearly profits into the open source they use."),
        ("blog/2017/jan/27/code-is-self-documenting",
         "Comments explain the why, and documentation does more than explain how the code works."),
        ("blog/2018/feb/7/the-post-i-never-published",
         "A draft from 2016, written while burned out on Read the Docs, shared to talk more openly about it."),
        ("blog/2019/sep/19/helping-first-time-conference-attendees-with-welcome-wagon",
         "How Write the Docs helps first-time attendees know what to expect, before and during the conference."),
    ],
    "topo_featured_count": 4,
    "topo_hikes": json.loads((_data / "hikes.json").read_text()),
    "topo_places": json.loads((_data / "places.json").read_text()),
}

html_theme_path = ["_themes"]
html_theme = "topo"
html_sidebars = {
    "**": [
        "sidebar/about.html",
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


def setup(app):
    app.connect("html-collect-pages", topo_redirect_pages)
