.. post:: 2008-09-02 00:55:21

Using pdb to debug management commands and unit tests (Debugging Django Series,Part 4)
======================================================================================

Screencast 4
------------

Today's screencast is about pdb again. This time we are going to be
debugging management commands, and unit tests for django. This is a
little bit more powerful than the previous screencast which just
introduced the basic debugging commands.

Setup
~~~~~

This screencast uses a couple of really handy pieces of software.
`iPython <http://ipython.scipy.org/moin/>`_ is a wonderful piece of
software for all python developers. It gives you handy things like
tab completion, syntax highlighting, and all the modern amenities
that we're used to in our editor from the python shell. Django's
manage.py shell even uses ipython if it detects it, that's an
endorsement if i've ever heard one.

`ipdb <http://pypi.python.org/pypi/ipdb>`_ is a simple wrapper
around pdb that allows you to use ipython when you are doing your
debugging. This is really handy as well. To get the code for these
projects, go to their websites linked above or use the following
code:

::

    bzr branch lp:ipython
    easy_install ipdb

Download and Video
~~~~~~~~~~~~~~~~~~

You can download the video
`here <http://media.ericholscher.com/casts/Debugging%20management%20commands%20and%20unit%20tests.mov>`_
(20MB mov)


.. raw:: html

   <object width="640" height="500">   
   

.. raw:: html

   </object>
   
Debugging management commands and unit tests from Eric Holscher on
Vimeo.

Writeup
~~~~~~~

We start the screencast by breaking the testmaker management
command that I've written. We call it like this:

::

    python -i ~/EH/manage.py testmaker 67.207.139.9:8000 

The import thing to note is the ``-i``, which tells python to drop
into the python (>>>) shell after the command is run. I then show
how to use pdb postmordem command to go back into the crashed
management command. This is called like so:

::

    import pdb
    pdb.pm()

and this allows you to actually go back into the previous command!
Even if pdb isn't currently loaded at the time. This is a really
neat feature of the debugger, and incredibly useful for diagnosing
breakage that is hard to reproduce. You can go back up into the
application and see the actual state of the variables at that
time.

Next I introduce `ipython <http://ipython.scipy.org/moin/>`_ which
is a really nice python distribution. It has a really nice
debugger, called idpb, which gives you all the ipython commands
inside the debugger.

Next we go on to run testmaker with valid input after showing how
to do a simple fix to check if the input was correct. We call
ipython with an app passed in:

::

    ipython ~/EH/manage.py testmaker 67.207.139.9:8000 -- -a mine

Note that -- is meant to tell bash that the input is done for
ipython, and the rest will actually go to manage.py and into your
python code. This is good to know for trying to pass things into
management commands in ipython on the command line. This code will
generate tests and fixtures for the application inside of the mine/
directory. Once we browser around a little on the test server, we
have generated a unit test based on what we have done.

Assuming you have ipdb installed from
`Pypi <http://pypi.python.org/pypi/ipdb/0.1dev-r1716>`_, you can
include ipdb inside of your unit test (or any python file being
executed) and get the ipython debugger instead of vanilla pdb:

::

    import ipdb
    ipdb.set_trace()

Although I don't expound on it inside of the screencast, getting
inside of tests is probably one of the more useful things you can
do with the debugger. Trying to debug tests is really difficult,
and sometimes they return really strange errors that are hard to
get a handle on. Sometimes the line numbers are also off, and
debugging doctests are notoriously hard to debug. You can debug
doctests just as easily, with the following code (using ipdb if
preferred):

::

    >>> import pdb
    >>> pdb.set_trace()

I figured out that the error in the unit test was actually due to a
stale fixture left over from a previous run of the testmaker app.
It didn't have enough data to return a paginated list, so has\_next
was false instead of true like when we ran it against the live
database.

In related news, searching for ipdb on google made me stumble onto
the `The Internet Pinball Machine Database <http://ipdb.org>`_,
which I didn't know existed previously. Yess!


