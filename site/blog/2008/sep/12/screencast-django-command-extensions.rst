.. post:: 2008-09-12 16:01:35

Screencast: Django Command Extensions
=====================================

This is a screencast on the
`Django Command Extensions <http://code.google.com/p/django-command-extensions/>`_
project. It is one of my favorite third party apps, and it gets
installed in every Django environment I work in. It provides a
plethora of useful manage.py commands, and a couple other little
goodies as well.

Setup
~~~~~

Before you get started using these things, there are a couple of
packages you need to install. The first is
`Graphviz <http://www.graphviz.org/>`_ which is a really nice
toolkit for graph visualization. The other is
`Werkzeug <http://werkzeug.pocoo.org/>`_ which is a little python
web framework with an amazing debugger that we'll be using. There
can easily be installed:

::

     apt-get install graphviz
     easy_install Werkzeug

Video
~~~~~

.. raw:: html

    <div style="padding:78.57% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/1720508" style="position:absolute;top:0;left:0;width:100%;height:100%;" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>
   
Django Command Extensions from Eric Holscher on Vimeo.

Writeup
~~~~~~~

The website for the django extensions has a pretty good list of all
of the commands that are available. Below I will just write about
the way to use some of them that isn't well documented or a bit
different or unclear.

As a note, for things that output something to the screen, you can
redirect that output to a file really easily. For example:
``./manage.py dumpscript blog > blog.py`` redirects the output to
blog.py. The command extensions site has a list of output formats
for export\_emails
`here <http://code.google.com/p/django-command-extensions/wiki/ExportEmails>`_.
Which is really useful.

The command for graphviz is
``/manage.py graph_models auth blog |dot -Tpng -o test.png``

The output of graphviz is awesome. There are ways that you can hook
this up to a url in your URLConf so that it will be regenerated
whenever someone requests it (for data that changes often). That is
a really nice feature for data that is changing a lot, where
someone is watching over your work (school etc.).

Just to note, ``runserver_plus`` requires that you be running
``DEBUG = True``, and that your IP Adress is in ``INTERNAL_IPS``,
look at my
(screencast)[http://ericholscher.com/blog/2008/aug/28/screencast-debugging-django-error-page/]
here for a full explanation of this, and more!

Things that weren't covered in the screencast include ``sqldiff``
which is still halfway working, and provides a diff against what
your model and the current database look like. ``create_app`` and
``create_command`` are things that just flesh out the directory
structure for a new app or management command. ``create_superuser``
creates a new supersuer for you. generate\_secret\_key gives you a
new secret key. ``passwd`` allows you to easily change a users
password. ``reset_db`` resets your current database.

Thanks for watching, and stay tuned for more screencasts (and other
content too ;))


