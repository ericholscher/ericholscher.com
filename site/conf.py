# -*- coding: utf-8 -*-

import alabaster
import ablog

extensions = [
    'ablog',
    'sphinx.ext.intersphinx',
]
blog_title = u'Eric Holscher'
blog_path = 'blog/archive'
blog_baseurl = 'http://ericholscher.com'
blog_authors = {
    'Eric': ('Eric Holscher', 'http://ericholscher.com'),
}
blog_default_author = 'Eric'

blog_locations = {
    'PDX': ('Portland, Oregon', 'http://www.portlandhikersfieldguide.org/'),
}
blog_default_location = 'PDX'
fontawesome_link_cdn = 'https://netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.min.css'
blog_feed_fulltext = True
blog_feed_length = 10
blog_feed_archives = True

templates_path = ['_templates', ablog.get_html_templates_path()]
source_suffix = '.rst'
master_doc = 'index'
project = blog_title
copyright = u'2017, Eric Holscher'
version = '1.0'
release = '1.0'
exclude_patterns = ['_build', 'include/*']
pygments_style = 'sphinx'
html_theme_path = [alabaster.get_path()]
html_theme = 'alabaster'
html_sidebars = {
    '**': ['logo.html', 'about.html', 'localtoc.html', 'searchbox.html'],
    'blog/**': ['blog_logo.html', 'postcard.html', 'about.html'],
}
html_title = blog_title
html_favicon = '_static/img/favicon.ico'
html_static_path = ['_static']

intersphinx_mapping = {
    'sphinx': ('http://www.sphinx-doc.org/en/stable/', None)
}


def setup(app):
    app.add_stylesheet('eric.css')
