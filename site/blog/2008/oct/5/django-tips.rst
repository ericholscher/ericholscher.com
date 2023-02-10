.. post:: 2008-10-05 20:09:24

Big list of Django tips (and some python tips too) 
===================================================

We were talking about things that we wish we had known before while
developing for Django the other day in IRC. I proclaimed that we
should write them down somewhere. So I'm writing a post to get this
effort started. Please feel free to leave comments with your own
tips and tricks, and I'll compile them in some kind of good
fashion. These are mostly just pointers, and not full-blown
writeups, just more of a big list of stuff you should think about.
I think these tips will really help out new people when they're
trying to get the hang of Django.

App level
~~~~~~~~~

Local library installation
^^^^^^^^^^^^^^^^^^^^^^^^^^

When you don't have root access on a machine, and you want to use
`easy\_install <http://peak.telecommunity.com/DevCenter/EasyInstall#id24>`_,
you can install files into a designated directory. I use ~/lib to
hold my python modules, so when I do easy\_install I simply use the
``-d`` option like so:

``easy_install -d ~/lib nose``

Use iPython
^^^^^^^^^^^

`IPython <http://ipython.scipy.org/moin/>`_ is a python
distribution that gives you lots of handy features like tab
completion, syntax highlighting, better debugging, and lots of
other nice features. Poke around, I find more and more stuff I like
every time.

Use django command extensions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is one project I use every time I do some new code. I wrote up
a
`whole post and screencast <http://ericholscher.com/blog/2008/sep/12/screencast-django-command-extensions/>`_
about how good they are. They have gotten even better since then,
highly recommended.

Performance tips from the man himself
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Jacob (co-BDFL) wrote up some
`performance tips <http://www.jacobian.org/writing/2005/dec/12/django-performance-tips/>`_
back in '05 that are still relevant today. Some big architectural
stuff, but they still make sense.

Use mod\_wsgi
^^^^^^^^^^^^^

mod\_wsgi is currently the best way that I know of to run Django. I
did a simple
`write up <http://ericholscher.com/blog/2008/jul/8/setting-django-and-mod_wsgi/>`_
a while back that has proved popular.

Running out of memory?
^^^^^^^^^^^^^^^^^^^^^^

Web faction has a good
`blog entry <http://blog.webfaction.com/tips-to-keep-your-django-mod-python-memory-usage-down>`_
about how to keep memory usage down. Might be useful even if you're
not running on their hardware.

Use pdb
^^^^^^^

Pdb is a great debugger.
`Simon <http://simonwillison.net/2008/May/22/debugging/>`_ has a
great post on it, and I took a lot of his ideas and expanded them
to do my debugging django screencast series.
`Using pdb <http://ericholscher.com/blog/2008/aug/31/using-pdb-python-debugger-django-debugging-series-/>`_

Read b-list.org archives
^^^^^^^^^^^^^^^^^^^^^^^^

My tips here are short and sweet,
`James <http://b-list.org/weblog/categories/django/>`_ has a wealth
of amazingly informative Django information stowed away in his blog
archives. Do yourself a favor and peek through it and be
enlightened.

Don't be afraid of Reusable apps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Watch <http://www.youtube.com/watch?v=A-S0tqpPga4>`_ James'
presentation on Reusable apps at Djangocon. Learn it, and use it. A
lot of the functionality that you want to do has already been done
for you. Check out `Pinax <http://pinaxproject.com/>`_ which has a
ton of nice reusable apps.
`django-basic-apps <http://code.google.com/p/django-basic-apps/>`_
also has a ton of really nice reusable apps that use best
practices. I use the blog here and it's a great way to learn how to
use django well. Learn by other people's awesome examples!

Watch the Djangocon videos
^^^^^^^^^^^^^^^^^^^^^^^^^^

The
`videos <http://www.youtube.com/view_play_list?p=D415FAF806EC47A1>`_
from Djangocon give you some great insights into Django.

Search and replace
^^^^^^^^^^^^^^^^^^

Search and replace across an entire directory. This is useful for
changing template vars or doing basic refactoring (good editors
should do this for you too)

::

    perl -pi -w -e 's/foo/bar/g' *.html

Check out virtualenv
^^^^^^^^^^^^^^^^^^^^

`virtualenv <http://pypi.python.org/pypi/virtualenv>`_ is an
awesome python tool that allows you to create mini-sandboxes of
python. You can contain an entire django install (and supposedly
you can get mod\_wsgi and some other stuff inside). I haven't
played with it too much, but it sounds really nice to keep a
contained python environment, and allows you to run different
versions of libraries, django, and anything else you can think of.

Use Django snippets
^^^^^^^^^^^^^^^^^^^

`Django snippets <http://djangosnippets.org>`_ is a great place to
post your tips, or get other peoples code examples. It's a big
cookbook of helpful and neat things about django. It doesn't have
search, so use google's site:djangosnippets.org syntax to find what
you need.

Use your environment!
^^^^^^^^^^^^^^^^^^^^^

I find that my .bash\_profile file is a huge help for all Django
stuff I do. Here is an example or mine, I'm really curious about
other people's awesome aliases and other settings foo.

::

    export PYTHONPATH=$HOME/Python:$HOME/Python/Modules
    export PATH=$HOME/bin:$PATH
    export DJANGO_SETTINGS_MODULE="settings"
    export HISTFILESIZE=10000000
    set -o vi
    alias rs='/usr/bin/python ~/EH/manage.py runserver 67.207.139.9:8000 --settings settings_debug'
    alias mp='/usr/bin/python ~/EH/manage.py'
    alias sp='/usr/bin/python ~/EH/manage.py shell_plus'
    alias bkup='/usr/bin/python ~/EH/manage.py dumpdata'
    alias destroy-pyc='find . -name \*.pyc -delete'
    alias mod='cd ~/Python/Modules'
    alias dj='cd ~/Python/Modules/django-trunk'
    alias a2='sudo /etc/init.d/apache2 restart'
    alias tm='/usr/bin/python ~/EH/manage.py testmaker 67.207.139.9:8000 --settings settings_debug'
    alias p='python'
    alias x='exit'
    alias tst='./manage.py test'

Models
~~~~~~

Use managers for commonly accessed queries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Writing managers is really simple, and they provide a better user
interface to your code. This code snippet simply adds a latest()
method to the default objects manager

::

    class ForecastDayManager(Manager):
        def __init__(self, *args, **kwargs):
            super(ForecastDayManager, self).__init__(*args, **kwargs)
        def latest(self):
            return self.get_query_set().order_by('forecast_date')[0]

It can be called ``ForecastDay.objects.latest()``. This is a
trivial example, but there is a lot of power that lies in this
functionality.

Meta is your friend
^^^^^^^^^^^^^^^^^^^

You can define the default ordering of your model, so when it
returns things in a queryset you don't need to do an order\_by()
clause (like above).
`Possible settings <http://docs.djangoproject.com/en/dev/ref/models/options/#ref-models-options>`_.
If you set get\_latest\_by, the above code is already written for
you.

No really, Love meta.
^^^^^^^^^^^^^^^^^^^^^

Ever wonder where all of that lovely metadata that you have set
goes? It all gets stored in your objects \_meta variable. Note the
underscore, this is private and might change at some future point.
However, a lot of it is stable and it gives you some really nice
things that you can get access to. \_default\_manager is a another
really nice one on query sets, this returns objects (or whatever
the default manager is). It's really handy for writing re-usable
code.

Settings
~~~~~~~~

Relative imports
^^^^^^^^^^^^^^^^

When you are using a setting file multiple times, it is nice to be
able to define relative variables for your things.

::

    import os
    DIRNAME = os.path.dirname(__file__)
    DATABASE_NAME = "%s/dev.db" % DIRNAME
    MEDIA_URL = os.path.join(DIRNAME, 'media')
    TEMPLATE_DIRS = (
    DIRNAME + "templates", 
    )

`more <http://rob.cogit8.org/blog/2008/Jun/20/django-and-relativity/>`_

Local settings
^^^^^^^^^^^^^^

If you have local changes to your settings file, that you don't
want to share, or that are specific to your box, there is an easy
way to accomplish that. Put this at the bottom of your settings.py
file:

::

    try:
         from local_settings import *
    except ImportError:
         pass

This allows you to define a local\_settings.py in that same
directory (or on your pythonpath if you so feel). This can then
override (or add on to) the settings previously defined in the
file.

Use a settings debug file.
^^^^^^^^^^^^^^^^^^^^^^^^^^

This kind of inverts the logic above, but runserver allows you to
pass it a settings command. So you can run runserver with the
command ``./manage.py runserver --settings settings_debug`` and I
keep a settings\_debug.py file sitting around that looks like
this:

::

    DEBUG = True
    INTERNAL_IPS = ['24.xxx.xxx.xx']
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)

This allows me to keep my normal (production) settings file from
ever having DEBUG set to True. That way there's no way to run with
it in production. The other things are just good easy way to
maintain some stuff that is useful for debugging/testing, but you
don't want to include in your normal production server.

Views
~~~~~

Wrapping generic views
^^^^^^^^^^^^^^^^^^^^^^

It's really easy to use generic views in Django. Sometimes you want
to change a little functionality or what they return, so you think
you have to write a whole new function. Malcolm
`goes into <http://www.pointy-stick.com/blog/2006/06/29/django-tips-extending-generic-views/>`_
how to extend them, to save you some time.

Use RequestContext
^^^^^^^^^^^^^^^^^^

By default, when you render a template, you aren't given the
request object. It's nice to have and really simple to make django
give it to you.

::

    from django.template import RequestContext
    def index(request):
        return render_to_response('weather/index.html', {},
                      context_instance=RequestContext(request))    

Templates
~~~~~~~~~

Use the {% url %} tag.
^^^^^^^^^^^^^^^^^^^^^^

Using the
`url tag <http://docs.djangoproject.com/en/dev/ref/templates/builtins/#url>`_
allows you to make your templates portable and is a good way to
implement DRY. Whenever the links in your view changes, your
templates automatically update, and they always have the correct
links.

Use Template Utils
^^^^^^^^^^^^^^^^^^

`django-template-utils <http://code.google.com/p/django-template-utils/>`_
contain some really nice generic template tags and other goodies
that make your life easier. From getting the latest X number of
objects from a model, getting a random object from a module, or
getting the last updated one; they provide you with a really nice
generic way of extending template nodes and doing generic content
tags really easy.

Use MEDIA\_URL
^^^^^^^^^^^^^^

Django now comes with a
`Context Processor <http://docs.djangoproject.com/en/dev/ref/templates/api/#django-core-context-processors-media>`_
that gives you
`MEDIA\_URL <http://docs.djangoproject.com/en/dev/ref/settings/#media-url>`_
in your templates. Use this so that you can apply DRY to all of
your external media Urls, like you did with the {% url %} tag for
internal things.

Use a 3-level template hierarchy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is referenced in the
`Django docs <http://docs.djangoproject.com/en/dev/topics/templates/#id1>`_ (about
a page down). But it works really well to do a base.html,
app-base.html, and then templates on top of that. This gives you a
really nice way to contain site-wide, app-wide, and view-wide
functionality inside their own little spaces.

Using template inheritance to extend itself
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a really neat trick when dealing with multiple template
directories. It allows you to take most of a chunk of one template,
and overwrite just a small part of it.
`They explain it <http://code.djangoproject.com/wiki/ExtendingTemplates>`_
better than I do.

Testing
~~~~~~~

Using the tests/ directory
^^^^^^^^^^^^^^^^^^^^^^^^^^

inside of your application you can define a tests.py that will hold
tests. You can also define a tests/ directory that can hold tests.
Inside the tests directory **init**.py you need to import all of
your unit tests. Inside **init**.py you need:

::

     from basic import *
     from views import *

etc. Assuming your tests are named basic.py and views.py.

Watch Files
^^^^^^^^^^^

This tip is useful for doing TDD. You can go ahead and watch the
output of your test file and see when something changes based on
the edits you're making to your files.

``watch "python tests.py"``

Nose tests
^^^^^^^^^^

Use
`nose tests <http://somethingaboutorange.com/mrl/projects/nose/>`_.
They have some neat auto-discovery tools and lots more.
`nose-django <http://www.assembla.com/wiki/show/nosedjango>`_
allows this to work with Django fixtures (note it may not work well
yet). This would be nice if someone wrote a test runner in django
for nose.

Mock objects
^^^^^^^^^^^^

Using mock objects to test is really handy. There are a couple of
good mock testing libraries for python, and i show a simple way to
do it
`here <http://ericholscher.com/blog/2008/aug/14/using-mock-objects-django-and-python-testing/>`_
This allows you to try your code when it's interacting with things
that are somewhat random (like times of day, random numbers, etc.)

Use testmaker
^^^^^^^^^^^^^

I wrote an app that writes view tests for you. A little
`self promotion <http://ericholscher.com/blog/2008/jul/26/testmaker-002-even-easier-automated-testing-django/>`_,
but go ahead and check it out.

Want to do something a little different?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can
`define your own test runner <http://docs.djangoproject.com/en/dev/topics/testing/?from=olddocs#defining-a-test-runner>`_
and set it in the settings. Then you can tweak the way that django
runs your tests for you. This is a lighter weight approach than
using nose or something to run your tests, and is integrated with
django, which makes it more portable.

Use testserver
^^^^^^^^^^^^^^

Django comes with the
`testserver <http://docs.djangoproject.com/en/dev/ref/django-admin/#testserver-fixture-fixture>`_
command that allows you to load a fixture into the development
server and run against that. This is really useful. It also leaves
the database around after it's done, so you can inspect it. This
can be really handy in debugging fixtures and tests.


