:Date: 2008-08-28 17:01:22
Screencast: Debugging with the Django Error Page
================================================

**This is part 1 of a week long series of screencasts**

Hey Everyone, I'm here to make a minor announcement. In the
upcoming 7 days, I'm going to be releasing 5-7 screencasts on
Django, mostly focused on debugging, and hopefully trying to throw
in a couple of other useful ones that people might be interested
it. This is my own way of helping people get ready for 1.0 and
hopefully sharing some good tips on ways to use Django well. Please
add you own comments and tips to the end of the posts! Please
`subscribe <http://feeds.feedburner.com/EricsThoughts>`_ to my feed
to get all of the screencasts (It'll be worth it!)

Also a big thanks to `Simon Willison <http://simonwillison.net/>`_
who's excellent debugging blog post got me started and interested
in this stuff.

Screencast 1
------------

The first in the series is going to be how to use the Django error
page to it's fullest. It is a very useful piece of work (Thanks
`Wilson <http://www.wilsonminer.com/>`_).

Setup
~~~~~

\*Please install
`Django Command Extensions <http://code.google.com/p/django-command-extensions/>`_
and `The Werkzeug Debugger <http://werkzeug.pocoo.org/>`_ before
you go on.

::

    svn checkout http://django-command-extensions.googlecode.com/svn/trunk/ django-command-extensions
    easy_install Werkzeug

Make sure that they are installed (on your PYTHONPATH) before
continuing on.

Video
~~~~~

The full video can be downloaded
`here <http://media.ericholscher.com/casts/Using%20Djangos%20Error%20Page.mov>`_
(18MB H.264 .mov)


.. raw:: html

   <object width="640" height="475">   
   

.. raw:: html

   </object>
   
Debugging with the Django error page from Eric Holscher on Vimeo.

Writeup
~~~~~~~

First off I fire up the debug server. Showing people how to use
``assert False``. You use ``assert False`` when you just want to
bring up a debug page to look at your context. It will bring up an
``AssertionError`` at the point where you put this code.
``assert False, foo`` brings up the error, showing whatever is in
``foo`` on the top of the error page.

The debug page is really useful because it contains a lot of useful
information. It shows your entire ENVironment, including your GET,
POST, COOKIES, PYTHONPATH, and lots of other good data. This
information is really useful for debugging forms and session errors
especially.

I then showed how to post your error to
`dpaste <http://dpaste.com/74331/>`_ with one click in the error
page. This is really handy for sharing your errors and tracebacks
with people for them to help you debug your code.

"Part 2" of the screencast is about using the Werkzeug debugger for
**more debugging power**. The command to run the Werkzeug debugger
(with django-command-extensions) is:

``./manage.py runserver_plus 67.207.139.9:8000 --settings settings_debug``

with settings\_debug.py being in the same file as your settings
(and the current directory) containing:

::

    from settings import *
    DEBUG = True
    INTERNAL_IPS = ['YOUR_IP']

`whatismyip.com <http://whatismyip.com>`_ is a really handy utility
for getting your external IP address. Then once you restart your
debugging server, your error page should be the Werkzeug error
page!

The Werkzeug error page is similiar to the django one, it has a
traceback and all that good stuff. The killer feature however is
that you can open up a python console at any of the places in your
backtrace!

The ``dump()`` command inside the Werkzeug console is really handy.
It will output a prettyprinted version of whatever you pass in.
Allowing you to readily see what internal variables your object
that you're debugging has.

**Remember this is powerful! NEVER use this in production! People will have access to all your data!!**
It is a very powerful debugging tool, which is a double-edged
sword.

PS: I hope you enjoyed me floundering in that later part. I thought
it showed the value in the debugger so I left it in :)

Stay tuned daily at my feed for posts everyday up until Django 1.0!
Cheers.


