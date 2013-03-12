:Date: 2010-02-05 01:43:55

Large Problems in Django, Mostly Solved: Documentation
======================================================

*\* [This is part of the `Large Problems in Django Series <http://ericholscher.com/tag/largeproblems/>`_, see previous entries about: `APIs <http://ericholscher.com/blog/2009/nov/11/large-problems-django-mostly-solved-rest-api/>`_, `Search <http://ericholscher.com/blog/2009/nov/2/large-problems-django-mostly-solved/>`_, and `Database Migrations <http://ericholscher.com/blog/2009/nov/6/large-problems-database-migrations/>`_]*\*

Django is well known across the open source community for it's
stellar documentation. While the tech behind the documentation
plays only a little role in how good it is, the tools behind both
Python and Django's documentation is
`Sphinx <http://sphinx.pocoo.org/index.html>`_. Luckily, we can all
use Sphinx to document our projects, and I'd like to talk a little
about why you might want to.

Why use Sphinx
~~~~~~~~~~~~~~

Network Effects
'''''''''''''''

One of the big reasons is because it is becoming the standard
documentation tool in the Python community. Once your projects
documentation is in Sphinx, most everyone will know how to
contribute to it. You will also be able to contribute to other
projects easily as well. You can look through the
`Python <http://code.python.org/hg/trunk/file/99eac34f25bb/Doc/>`_
and
`Django <http://code.djangoproject.com/browser/django/trunk/docs>`_
docs for examples of how to do neat things, and it is really the
best solution to the problem.

It uses Restructured Text
'''''''''''''''''''''''''

If you are writing plain text about python, more than likely you
should be using
`Restructured Text <http://sphinx.pocoo.org/rest.html>`_. All
docstrings are parsed for it, and you only need to learn this one
markup language for all of your plain text needs. It even works
great for blog posts, with most Django blogging engines supporting
it. It is also easy to extend, and is generally a useful thing to
know how to do.

Write once, compile to HTML, PDF, etc.
''''''''''''''''''''''''''''''''''''''

By writing in Restructured Text, you write your documentation with
metadata about what all of your text means. This then allows it to
be transformed intelligently into other formats. This is how Django
can provide HTML and PDF versions of the documentation all from the
same source format. By rendering through LaTeX, you are given a
large amount of flexibility in the style of your PDF output,
allowing for really nice designs with a little effort.

Your docs are beautiful
'''''''''''''''''''''''

Sphinx has native support through
`Pygments <http://pygments.org/>`_ for syntax highlighting most
languages that exist. It also ships with support for themes, with
the community
`providing <http://github.com/bartTC/sphinx-schemes>`_
`themes <http://github.com/coordt/ADCtheme>`_ out of the box to
make your documentation look great. This is another place where
having a critical mass of people behind the project makes your docs
better.

Cross References
''''''''''''''''

With simple markup rules applied to your documentation, you get
indexes and cross referencing for free. This makes your
documentation much more discoverable, and useful for people who are
browsing it. The Django documentation makes
`extensive use <http://docs.djangoproject.com/en/dev/topics/testing/#id1>`_
of this, making it easy to jump to the definition of a setting
where ever it is referenced for example.

Lots and lots more.
'''''''''''''''''''

Please just go look at Sphinx, and read a little more about it. The
`Overview <http://sphinx.pocoo.org/contents.html>`_ at the Sphinx
page gives you a nice example of actual Sphinx docs, and points to
lots of little tidbits of information. Sphinx has made documenting
your project a real joy, and I can't recommend it enough.


