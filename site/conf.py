# -*- coding: utf-8 -*-

import alabaster
import ablog

extensions = [
    'ablog',
    'sphinx.ext.intersphinx',
]
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
fontawesome_link_cdn = 'http://netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.min.css'
blog_feed_fulltext = True
blog_feed_length = 10
blog_feed_archives = True

templates_path = ['_templates', ablog.get_html_templates_path()]
source_suffix = '.rst'
master_doc = 'index'
project = u"Surfing in Kansas - Eric Holscher"
copyright = u'2016, Eric Holscher'
version = '1.0'
release = '1.0'
exclude_patterns = ['_build', 'include/*']
pygments_style = 'sphinx'
html_theme_path = [alabaster.get_path()]
html_theme = 'alabaster'
html_sidebars = {
    '*': ['sidebarlogo.html', 'about.html', 'localtoc.html'],
    'blog/**': ['sidebarlogo.html', 'postcard.html', 'about.html', 'localtoc.html'],
}
html_title = "Surfing in Kansas"
html_favicon = '_static/img/favicon.ico'
html_static_path = ['_static']
htmlhelp_basename = 'SurfinginKansasdoc'

latex_documents = [
    ('index', 'SurfinginKansas.tex', u'Surfing in Kansas Documentation',
     u'Eric Holscher', 'manual'),
]
man_pages = [
    ('index', 'surfinginkansas', u'Surfing in Kansas Documentation',
     [u'Eric Holscher'], 1)
]
texinfo_documents = [
    ('index', 'SurfinginKansas', u'Surfing in Kansas Documentation',
     u'Eric Holscher', 'SurfinginKansas', 'One line description of project.',
     'Miscellaneous'),
]

intersphinx_mapping = {
    'sphinx': ('http://www.sphinx-doc.org/en/stable/', None)
}


def setup(app):
    app.add_stylesheet('eric.css')
