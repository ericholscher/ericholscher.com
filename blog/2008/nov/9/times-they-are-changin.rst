:Date: 2008-11-09 11:49:43

The times, they are a changin
=============================

A couple posts back, I was talking about software that I use all
the time. I was going through and linking to all of the software. I
would go to google, type in the project name, go to the first
result, and copy that URL back into my post. I figured that there
had to be a better way. Any software project worth it's name owns
the top result in google.

The web is a dynamic place, and websites move, change, and
disappear all the time. The popularity and importance of some
things change over time as well. So I was thinking about how to go
about linking to the most popular thing for a search. It also
happened to be useful for my last post and linking to things. A
similar approach could be used with Wikipedia. Creating something
that just linked to somethings wikipedia page.

Show me the code.
~~~~~~~~~~~~~~~~~

I couldn't use Google, because I couldn't find a good web search
API for them. Yahoo however has a
`really nice one <http://pysearch.sourceforge.net/>`_ that is out
there to use. This, combined with James Bennett's awesomely useful
`template utils <http://www.bitbucket.org/ubernostrum/django-template-utils/overview/>`_
allowed me to whip this up in about 10 minutes. Here's the code
below.

::

    from template_utils.nodes import ContextUpdatingNode
    from yahoo.search.web import WebSearch
    
    class SearchNode(ContextUpdatingNode):
        def __init__(self, search):
            self.search = search
    
        def get_content(self, context):
            srch = WebSearch('EricSearch', query=self.search)
            res = srch.parse_results()
            return {'top_url': res.results[0].Url}
    
    @register.tag
    def first_yahoo_link(parser, token):
        return SearchNode(token.split_contents()[1])

Easy as pie, and awesome. This ties into my previous post about
template tags being hard to write. If you just want to make a
template tag that sets a context, it's as easy as making a node and
returning a dictionary in the ``get_content()`` function. This
isn't a super robust solution, but now i can do
``{% first_yahoo_link "search terms" %}`` and ``{{ top_url }}``
will contain the Url of it!

Also note how easy it is to use Yahoo's search api! That's awesome.
If this was on a more highly trafficked site, you would want to
cache the results (maybe daily, because they shouldn't change
much). I may go ahead and do a tutorial on how to do caching with
template tags and template-utils if people are interested in it.

The observant will note that this doesn't help me writing a blog
post, because there's no way to call a template tag from within.
That might be something for me to cook up later this month. The
template tag is still neat however, for introducing yahoo's web
api, and template-utils.


