.. post:: 2008-11-26 20:41:05

Testmaker 0.2: Rewritten and improved
=====================================

About a week ago, I went ahead and re-wrote
`testmaker <http://code.google.com/p/django-testmaker/>`_ and moved
it into my
`django-test-utils <http://github.com/ericholscher/django-test-utils/tree/master>`_
project on github. The syntax is now a bit different, and the whole
thing is much improved. This is version 0.2. The screencast
from the last release still shows the gist of the project, except
for the changed syntax.

Also note that my projects have permanent pages for documentation
over at my `projects page <http://ericholscher.com/projects/>`_.
This will stay up to date with the most current version of the
software, and basically be a copy of this post for now.

Testmaker
---------

What is does
~~~~~~~~~~~~

Django testmaker is an application that writes tests for your
Django views for you. You simply run a special development server,
and it records tests for your application into your project for
you. Tests will be in a Unit Test format, and it will create a
separate test for each view that you hit.

Usage
~~~~~

Step 1: Add ``test_utils`` to your INSTALLED\_APPS settings.

Step 2:

::

    ./manage.py testmaker APP

This will start the development server with testmaker loaded in.
APP must be in installed apps, and it will use Django's mechanism
for finding it. It should look a little something like this:

::

    eric@Odin:~/EH$ ./manage.py testmaker mine
    Handling app 'mine'
    Logging tests to /home/eric/Python/EH/mine/tests/mine_testmaker.py
    Appending to current log file
    Inserting TestMaker logging server...
    Validating models...
    0 errors found
    
    Django version 1.0.1 final, using settings 'EH.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Then, as you browse around your site it will create unit test files
for you, outputting the context variables and status code for each
view that you visit. The test file used is in
``APP/tests/APP_testmaker.py``. Once you have your tests written,
you simply have to add them into your ``__init__.py``, and then run
your tests.

Step 3:

::

    ./manage.py test APP

Things to notice
~~~~~~~~~~~~~~~~

This fixes a lot of complaints that people had about previous
versions of test maker. This allows you to test apps that are
anywhere on your Python Path (and in your INSTALLED\_APPS), which
makes life a lot easier. Each view also has it's own test name,
which is a slugified version of the request path and the time when
you hit it (because I needed something unique :)) You also may
notice that there is rudimentary support for template tags; this
will be explained upon in my
`next post <http://ericholscher.com/blog/2008/nov/27/value-conventions/>`_.
However, for now know that it only works for template tags that
don't set a context variable, or use the format
``as <context_var>`` to set one.

Improvements over 0.1
~~~~~~~~~~~~~~~~~~~~~


-  Each page request is in its own test, for easier debugging
-  It will append tests if your APP\_testmaker.py file already
   exists.
-  You can now test admin views
-  POST support is improved
-  The code is cleaner and more readable
-  Git!

Options
~~~~~~~

-f --fixture
^^^^^^^^^^^^

If you pass the ``-f`` option to testmaker, it will create fixtures
for you. They will be saved in
``APP/fixtures/APP_fixtures.FORMAT``. The default format is XML
because I was having problems with JSON.

--format
^^^^^^^^

Pass this in with a valid serialization format for Django. Options
are currently json, yaml, or xml.

--addrport
^^^^^^^^^^

This allows you to pass in the normal address and post options for
runserver.

Future improvements
~~~~~~~~~~~~~~~~~~~

Force app filtering
^^^^^^^^^^^^^^^^^^^

I plan on having an option that allows you to restrict the views to
the app that you passed in on the command line. This would inspect
the URLConf for the app, and only output tests matching those URLs.
This would allow you to fine tune your tests so that it is
guaranteed to only test views in the app.

Better test naming scheme
^^^^^^^^^^^^^^^^^^^^^^^^^

The current way of naming tests is a bit hackish, and could be
improved. It works for now, and keeps names unique, so it's
achieving that goal. Suggestions welcome for a better way to name
things.

Improve template tag testmaker
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is a total hack at current, but it works. Certainly a first,
rough draft.


