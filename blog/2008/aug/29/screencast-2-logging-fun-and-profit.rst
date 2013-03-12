:Date: 2008-08-29 08:46:51
Screencast 2: Logging in Django, for fun and profit
===================================================

**This is the second screencast of a week long series.**

So that I don't spam all of the Django Community Feed (Bad RSS
handling has done that more than once, Sorry!) I'm only going to be
posting this post and the last post summarizing all of the
screencasts on the aggregator. So if you're trying to keep up with
all of the screencasts that will be coming out this week, either
stay tuned to the site or subscribe to my
`feed <http://feeds.feedburner.com/EricsThoughts>`_.

Screencast 2: Logging in Django
-------------------------------

Setup
~~~~~

This screencast is going to be about how to use the python logging
module in Django. It's in the Python standard library, so there is
nothing extra to install to use the simple python logging module.
The screencast also makes use of the excellent
`Django-Logging <http://code.google.com/p/django-logging/>`_, which
should be downloaded and installed beforehand.

``svn checkout http://django-logging.googlecode.com/svn/trunk/ django-logging``

This allows for you to follow along on the second part of the
screencast. I also do a little bit of work inside my
`django-testmaker <http://code.google.com/p/django-testmaker/>`_
app, so you can go grab that if you want to follow along as well.
If not no big deal, the screencast is more about general logging
anyway.

Video and Download
~~~~~~~~~~~~~~~~~~

The video is available to download in higher res or for streaming.

`Download <http://media.ericholscher.com/casts/Using%20Logging%20in%20Django.mov>`_
(21MB H.264 .mov)


.. raw:: html

   <object width="640" height="475">   
   

.. raw:: html

   </object>
   
Screencast 2: Using Logging in Django from Eric Holscher on Vimeo.

Writeup
~~~~~~~

Part 1: python logging module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We start out with some really simple logging methods. The first is
a simple ``print`` statement inside of your views. This outputs the
command to the terminal in your development server. The next way to
do it is with a simple logging command:

::

    import logging
    logging.error('your error goes here!')

During the screencast I say that logging.error goes to Standard
Out, when in actuality it goes to Standard Error. In this case
they're the same thing...Then I go through how logging is done
within the testmaker app. This is the basic setup for python's
logging module that I used:

::

        logging.basicConfig(level=logging.INFO,
                   format='%(message)s',
                   filename= "/file/to/log/to",
                   filemode='w'
                   )

More documentation about this and the python logging module is
`available here <http://docs.python.org/lib/module-logging.html>`_
It includes a lot of really good information about the logging
module, like
`lots of message formatting options <http://docs.python.org/lib/node421.html>`_.
I show how you can tail a log file from testmaker and talk about
the neat advanced features of the logging module like
`logging across a network <http://docs.python.org/lib/network-logging.html>`_.
As you can see the logging module is **very powerful!**

Part 2: django-logging
^^^^^^^^^^^^^^^^^^^^^^

In the second part of the screencast we show how to use the Django
Logging middleware. This is what is going to go into your
settings\_debug.py:

::

    from settings import *
    DEBUG = True
    INTERNAL_IPS = ['YOUR.IP.HERE']
    MIDDLEWARE_CLASSES += ('djangologging.middleware.LoggingMiddleware',)
    LOGGING_LOG_SQL = True

This then has all of your logging output appended to the bottom of
the page you're currently on. This gives you a similiar capability
of using the error page to debug, except you don't have to have an
error. You can debug while the pages are still working.

The next and last really neat feature is showing the SQL queries
that are being executed to render a page. This is incredibly useful
for fine-tuning your django sites. With the ORM, there are tiny
little tweaks that you can sometimes make to decrease (or
increase!) the numbers of queries you execute pretty dramatically.
Having this enabled during development is a good way to catch those
mistakes, and really understand what is going on under the hood of
your Django apps.

Remember, when you wrap all of your logging stuff in the logging
module, you can do some really neat things after the fact. I was
able to use all of the django-logging stuff while still logging
output to a file and whatever else happened to be going on with the
logger at the time. This in incredibly powerful, and allows you to
almost have django-style 'pluggable logging backends' that do
different things.

Again in this one I end a little silly: Thanks for your time and
have a good day (since I'l hopefully see you again tomorrow :))


