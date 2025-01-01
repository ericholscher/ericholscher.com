# -*- coding: utf-8 -*-

import alabaster
import ablog

extensions = [
    "ablog",
    "sphinx.ext.intersphinx",
    "notfound.extension",
    "sphinxext.opengraph",
]
blog_title = "Eric Holscher"
blog_path = "blog/archive"
blog_baseurl = "http://ericholscher.com"
post_date_format = "%b %d %Y"
post_show_prev_next = False
ogp_social_cards = {
    "line_color": "#4078c0",
    "image": "_static/img/headshot-circle.png",
}

# blog_authors = {
#     "Eric": ("Eric Holscher", "http://ericholscher.com"),
# }
# blog_default_author = "Eric"

# blog_locations = {
#     "Oregon": ("Somewhere, Oregon", "https://www.oregonhikers.org/field_guide/Main_Page"),
# }
# blog_default_location = "Oregon"

fontawesome_link_cdn = (
    "https://netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.min.css"
)
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
html_theme_path = [alabaster.get_path()]
html_theme = "alabaster"
html_sidebars = {
    "**": [
        "logo.html",
        "ablog/postcard.html",
        "about.html",
        "searchbox.html",
        "ablog/archives.html",
    ],
}
# globaltoc_collapse = False

html_title = blog_title
html_favicon = "_static/img/favicon.ico"
html_static_path = ["_static"]

intersphinx_mapping = {"sphinx": ("http://www.sphinx-doc.org/en/stable/", None)}
