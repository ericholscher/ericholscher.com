.. post:: 2009-07-15 14:15:03

Some great Python Software
==========================

Currently in the Django (Python?) Community, there isn't a good
place to go and find what are the 'best of breed' apps for certain
categories. There have been some rumblings of fixing these, and if
things like `DJApp <http://djapp.org/>`_ caught on, we might have
that ability. However, I'm going to go ahead and list some of the
applications that I use and think are just great. Please comment
here and talk about other ones you love, or feel free to write your
own post as well.

Python
------

Sphinx
^^^^^^

What can I say, `Sphinx <http://sphinx.pocoo.org/>`_ is an amazing
piece of software. The `Pocoo <http://pocoo.org/>`_ guys do some
great work, and Sphinx is no exception. It is fast becoming the
defacto documentation solution used in the Python Community,
powering Django and Python's own docs. In it's latest release it
has theme support, support for multiple output formats (HTML and
PDF!), and much more. If you are writing documentation for a Python
project (or any other language for that matter!) Sphinx is worth a
serious look.

**Pro Tip**: Check out my post on
`Adding Analytics <http://ericholscher.com/blog/2009/apr/5/adding-google-analytics-sphinx-docs/>`_
to sphinx for an example of extending Sphinx Templates

Pygments
^^^^^^^^

The other Pocoo project on this list,
`Pygments <http://dev.pocoo.org/projects/pygments/>`_ is the best
way I know to syntax highlight code using Python. It supports about
any language you can throw at it, and allows you to simply style
your output using css.

**Pro Trip**:
`Django Snippets <http://www.google.com/search?q=site:djangosnippets.org+pygments>`_
has lots of snippets for adding styling to your code.

Fabric
^^^^^^

`Fabric <http://fabfile.org/>`_ is a useful Python utility that
allow you to easily automate tasks on local and remote machines.
This is most obviously useful for deployment, but is good for
automating all sorts of deployment tasks. My friend
`Jeff <http://bitprophet.org/>`_ has just done a major refactor in
the upcoming 0.9 release, which looks to make Fabric a lot more
user friendly and generally useful. If you are still sshing and svn
up'ing or git pull'ing on a regular basis, take a look at fabric to
make your life a little bit easier.

Pip
^^^

`Pip <http://pip.openplans.org/>`_ is how all the cool kids are
installing packages these days. It builds on setuptools and
easy\_install of lore, but works better and is more up to date. It
allows you to install your code from hg/git/bzr repos as well as
pointing it at tarballs and Pypi. It also plays nicely with
virtualenv. \*\*Rumor has it that the next version will even have
an uninstall command!

**Pro Tip**: ``alias pimp='pip install'``, then you can
``pimp Django`` ;)

Virtualenv
^^^^^^^^^^

`Virtualenv <http://pypi.python.org/pypi/virtualenv>`_ is a way to
keep all of your source code seperated into logical directories,
without having the code interact. This is really useful if you have
multiple versions of the same code running against different
libraries. For example at work, we have our software running
against 3 (or more) versions of Django, all needing different
versions of BeautifulSoup, Markdown, different search dependencies
etc. Managing all this on a local development box becauses a pain
without the sane separation that Virtualenv gives you.

**Pro Tip**: Use
`virtualenvwrapper <http://www.doughellmann.com/projects/virtualenvwrapper/>`_
to get some nice commands on top of virtualenv to make it easier to
manage.

For more information on Fabric, Pip, and Virtualenv, check out
`this post <http://clemesha.org/blog/2009/jul/05/modern-python-hacker-tools-virtualenv-fabric-pip/>`_.
In the same category as well is zc.buildout, which
`Jacob's Intro <http://jacobian.org/writing/django-apps-with-buildout/>`_
seems to be the best resource for online.


