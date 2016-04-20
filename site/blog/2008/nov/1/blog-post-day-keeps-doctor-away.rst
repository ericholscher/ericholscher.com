.. post:: 2008-11-01 03:00:00

A blog post a day keeps the doctor away
=======================================

November blog posting month has a special moment in my Django
history. It was this time last year that I really got serious into
Django. With the help of
`James Bennett's <http://www.b-list.org/weblog/2007/nov/>`_ and
`Marty Alchin's <http://gulopine.gamemusic.org/2007/nov/>`_ blog
post a month streak, I got an incredibly valuable insight into
Django. It showed me a lot of the power and other great things
about Django (especially the community).

In that spirit, I figured that I would jump on the blog post a
month bandwagon (that looks like it's going to be big in Djangoland
this year). All of my posts won't be about Django, most of them
will probably be about programming, or technical in nature.
However, I promise nothing along these lines. Writing 31 posts back
to back is quite a lot of work. So I might blank out somewhere
halfway through for a day and resort to posting my philosophical
musing that used to be most of this blog. You are thusly warned ;)

I mentioned that some other people in the community are doing
post-a-day for the month. So expect to get your fill of awesome
Django and Tech related content.
`Brian Rosner <http://oebfare.com>`_,
`Eric Florenzano <http://www.eflorenzano.com/blog/>`_,
`Justin Lilly <http://justinlilly.com/>`_,
`James Tauber <http://jtauber.com/>`_, and
`Greg Newman <http://20seven.org/>`_ will be trying this gargantuan
task along with me!

Some of the things that you can look forward to in this month of
blog posts from my side:


-  At least 2 code releases. One is a new addition and release to
   testmaker, the other is another neat new testing tool.
-  Pinax related material. They have their first release, and most
   of us posters are in that community.
-  Screencasts. These are time consuming, but I have plans for at
   least a couple news ones over the month.
-  A new design. The finishing touches are being put on this site
   as we speak. So there will be a new version launched sometime early
   this month.
-  A newish approach to testing code that I have been thinking
   about for a while. Hopefully it isn't new and the Google-fu isn't
   strong with this one.
-  Some talk about template tags and how to make them better
-  Multiple viewpoints expressed on topics around the different
   people doing this.
-  Lots more!

I hope that you all stayed tuned and even join in on these posts
throughout the month. In talking about doing it, one of the big
wins of doing it at the same time was to enable the separate view
points on the same topic to be discussed. The point of blogs is to
have a discussion, and I think it will be neat to see what kind of
discourse we have throughout this month.

It looks like James Tauber has already posted his first
`functional combinatorial mind bender <http://jtauber.com/blog/2008/11/01/two_functional_questions/>`_
over on his blog already. Let the games begin!

Now on with regularly scheduled programming.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

And because I feel bad that there isn't really any content in this
post, here is a little tip:

Doing template testing is a pain sometimes because it suppresses
your errors. You can load your templates on the command line to
test them, and it will show you the errors if they are having any.

::

    >>> from django.template.loader import get_template
    >>> get_template('mine/index.html')
    <django.template.Template object at 0xa833d0>
    >>> get_template('mine/error.html')
    Traceback (most recent call last):
     [Chopped a bunch off]
      File "/usr/lib/python2.5/site-packages/django/template/__init__.py", line 362, in find_filter
        raise TemplateSyntaxError("Invalid filter: '%s'" % filter_name)
    django.template.TemplateSyntaxError: Invalid filter: 'wtf'

This is incredibly useful, and great for debugging templates
without worrying about caching and other things like that. Also
note that this isn't anything special used just for testing. This
is actually the way to load templates inside of your code. Check
out
`the docs <http://docs.djangoproject.com/en/dev/ref/templates/api/#the-python-api>`_
for more. ``select_template`` is another really useful thing to
know about, so check it out!


