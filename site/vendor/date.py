blog_url = 'http://ericholscher.com'

from docutils import nodes, utils
import urllib

def blog_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    env = inliner.document.settings.env
    for docname, doc_metadata in env.metadata.iteritems():
        doc_metadata = env.metadata.get(docname, {})
        if 'date' not in doc_metadata:
            continue #don't index dateless articles
        try:
            pub_date = doc_metadata['date']
        except ValueError, exc:
            print str(exc)
    node = nodes.reference(rawtext, utils.unescape(pub_date), **options)
    return [node],[]

def setup(app):
    app.add_role('blog_date', blog_role)
