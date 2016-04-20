.. post:: 2008-11-22 16:09:35

Django Aggregator v2 now has tagging, and you should too.
=========================================================

I have been doing some more work on my Django Community Aggregator
/ Django People v2 project. A big feature that I want to
incorporate is tagging. I want people to be able to sort data by
tag, among other things. I think that this is a pretty killer
feature.

This allows someone to say "I want to get all of the data about
`testing <http://ericholscher.com/django/tag/testing/>`_ or
`debugging <http://ericholscher.com/django/tag/debugging/>`_ that
the Django community is doing". However, if nobody is tagging their
posts, then only services that provide tags will be available in
those views. A lot of people are using
`django-tagging <http://django-tagging.googlecode.com/>`_ on the
backend of their blogs, but they just aren't exposing that data in
feeds.

Note: Yes I know the data can't be edited yet (on the aggregator).
That is because it is a project that is just living on my site for
the moment. Once it gets moved off and the Uber community of Django
gets more off the ground, all of those issues will be solved.

Luckily, it is really easy to expose your tagging data in your
Django feeds. This assumes you are using Django Tagging, however,
it's really easy with anything else.

Say we have our feed class that looks like this.

::

    class BlogPostsFeed(Feed):
        title = 'My awesome blog' 
        description = 'My awesome blog"
    
        def link(self):
            return "http://mysite.com"
    
        def items(self):
            return Post.objects.published()[:10]
    
        def item_pubdate(self, obj):
            return obj.publish

That is a pretty basic feed, but much akin to what most people
have. Now lets add some tagging in there! Assuming that you have
the Tag model imported from tagging, you can simply do this:

::

    def item_categories(self, obj):
        return [tag.name for tag in  Tag.objects.get_for_object(obj)]

You can test to make sure that your feeds are working by using
`feedparser <http://www.feedparser.org/>`_

::

    In [1]: import feedparser
    
    In [3]: p = feedparser.parse('http://ericholscher.com/feeds/posts/')
    
    In [4]: p.entries[0].tags
    Out[4]: 
    [{'label': None, 'scheme': None, 'term': u'lawrence'},
     {'label': None, 'scheme': None, 'term': u'mediaphormedia'},
     {'label': None, 'scheme': None, 'term': u'philosophy'},
     {'label': None, 'scheme': None, 'term': u'post-a-day'},
     {'label': None, 'scheme': None, 'term': u'ramblings'}]

That's it! Now everyone go do that to their feeds, so that I can
harvest your tags and make them useful :)


