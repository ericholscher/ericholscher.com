# -*- coding: utf-8 -*-

import sys
from pathlib import Path

# The site's own hooks live in _ext/topo_site.py, and its data and copy in _data/ and the pages.
sys.path.insert(0, str(Path(__file__).parent / "_ext"))

extensions = [
    "ablog",
    "sphinx.ext.intersphinx",
    "notfound.extension",
    "sphinxext.opengraph",
    "myst_parser",
    "topo_site",
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
