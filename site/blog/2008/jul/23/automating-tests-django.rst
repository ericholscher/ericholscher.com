.. post:: 2008-07-23 15:19:32

Automating tests in Django
==========================

`Updated </blog/2008/jul/26/testmaker-002-even-easier-automated-testing-django/>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At work lately we've been writing a bunch of tests for all of the
work we've been doing. This is generally a good thing (tm). I was
getting tired of manually having to write all of the code to test
the views inside of my app. So I decide to write a little app that
helps me automate the writing of tests.

I wrote a piece of middleware (that should obviously only be used
during development!) that shadows the current activity in django
into a log file. This log file should then be ready to copy and
paste into a doctest for easy testing of your views. This is a
little hard to explain, but the code should be pretty self
explanitory.

I created a
`google code project <http://code.google.com/p/django-testmaker/>`_for
it so that people can go ahead and hack on it and make it better.
It is pretty rudimentary at current, but it gets the job done.

I think a big win from this approach is that your testing data is
much more "real", since it's a copy of your session with a real
browser. I know writing django tests I sometimes use contrived data
because it is a pain to enter it all. This should help improve on
that situation.

Here is a video of it in action, this should allow it to make more
sense.


.. raw:: html

   <object width="400" height="300">   
   

.. raw:: html

   </object>
   
Django TestMaker from Eric Holscher on Vimeo.

Writeup
~~~~~~~

Figured it would be good to writeup the screencast.

Step 1: Get django-testmaker
``svn checkout http://django-testmaker.googlecode.com/svn/trunk/ django-testmaker-read-only``

Make sure the testmaker module is in your PYTHONPATH.

Step 2: Add
``'testmaker.middleware.testmaker.TestMakerMiddleware',``

to your MIDDLEWARE\_CLASSES in your settings file.

Step 3: Run the test server with the middleware installed.
``./manage.py runserver``

Browse around your site.

Step 4: run ``tail -f /tmp/testmaker.log``

to see your output.

Step 5: Take the output from testmaker.log and put it into a file
in PROJECT/tests.py. Make sure that your tests.py contains:

::

    """
    >>> from django.core.management import call_command
    >>> call_command('loaddata', 'PATH/TO/PROJECT/fixtures/PROJECT.json', verbosity=0)
    >>> from django.test import Client
    >>> c = Client()
    YOUR TESTS GOES HERE
    """

at the top of your tests.py file.

Step 6: Run the command
``./manage.py dumpdata > PROEJCT/fixtures/PROJECT.json``

You can have dumpdata just dump the data for a single project if
you provide PROJECT as an argument to it. Be warned though, that
the tests might break because of it using data from other apps.
(Like my example would break because the mine project uses data
from my blog app.)

Step 7: ``./manage.py test PROJECT``

Step 8: PROFIT!!

Update
~~~~~~

I added a management command to the project to simply this process
a ton. I'll be making another screencast and blog post (and maybe
even some REAL DOCS!) tonight, so stay tuned for that.


