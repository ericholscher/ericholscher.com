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
    # Home page "Most read", in order. Hand-picked; edit freely.
    "topo_popular": [
        "blog/2017/aug/2/pacman-rule-conferences",
        "blog/2023/feb/10/we-dont-do-that-here",
        "blog/2025/apr/29/camino-de-costa-rica-recap",
        "blog/2017/jan/27/code-is-self-documenting",
        "blog/2018/feb/7/the-post-i-never-published",
        "blog/2018/mar/9/one-percent-for-open-source",
        "blog/2019/sep/19/helping-first-time-conference-attendees-with-welcome-wagon",
    ],
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
