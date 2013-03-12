:Date: 2009-10-15 23:12:10
Easily Running the Django Test Suite
====================================

**Update** As of Django 1.2, Django ships with default test
settings for sqlite. They require two databases to be defined,
because of Multidb. More information at
`Django advent <http://djangoadvent.com/1.2/django-testing-improvements/>`_
and in
`the docs <http://docs.djangoproject.com/en/dev/internals/contributing/#running-the-unit-tests>`_

Alex Gaynor had a write up about
`Running the Django Test Suite <http://lazypython.blogspot.com/2008/11/running-django-test-suite.html>`_,
which is a quick overview of how to run the suite. The
`official docs <http://docs.djangoproject.com/en/dev/internals/contributing/?from=olddocs#running-the-unit-tests>`_
also have a simple mention of how to run them. This post will be
more step by step, walking you through the steps to run the tests
for Django. This is a really important first step in writing
patches against Django. It is easy, but something that a lot of
people have a question about when they start.

Step 1: Grab the Django Source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To test Django, you need the code, so go ahead and grab the
source.

::

    svn co http://code.djangoproject.com/svn/django/trunk/ django_src

Step 2: Settings
~~~~~~~~~~~~~~~~

In order to run the Django test suite, you need to have a settings
file. Usually for testing, you run the Django test suite under
SQLite. This is the easiest and fastest way to run the tests. If
you writing code against something that touches parts of the ORM or
Database code in general, running it against another database that
you have at your disposal if generally a good idea as well.

To run the SQLite tests, you simply need a settings file with one
line in it:

::

    DATABASE_ENGINE = 'sqlite3'

Go ahead and put this command in the top-level of your django
checkout (the one with the ``tests`` directory in it).

Step 3: Run the tests
~~~~~~~~~~~~~~~~~~~~~

Now you can run the tests. Your checkout should look something like
this:

::

    django_src/
        docs
        django
        examples
        setup.py
        tests
        settings.py
        ...

We need to make sure that Django is on your PYTHONPATH, this allows
Python and thus Django to see the django module that we want it to
test. You can set this inline, and then run the tests with the
correct settings file. We can do that in a single command like so:

::

     PYTHONPATH=`pwd` ./tests/runtests.py --settings=settings

The final commands, which you should be able to copy and paste into
a shell to check out the code and run the tests is as follows:

::

    svn co http://code.djangoproject.com/svn/django/trunk/ django_src
    cd django_src
    echo "DATABASE_ENGINE = 'sqlite3'" > settings.py
    PYTHONPATH=`pwd` ./tests/runtests.py --settings=settings -v1

The ``-v1`` will set the verbosity to 1, which gives you the dots
that everyone knows and loves.

Now that you have a django source tree with running (and hopefully
passing) tests, you can apply a patch or go ahead and develop on
this code and be able to test it easily!


