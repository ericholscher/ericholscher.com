:Date: 2010-08-28 11:00:00
New features on Read The Docs
=============================

Since the Django Dash ended, We've been working on adding some
requested new features to
`Read The Docs <http://readthedocs.org>`_. There are a couple of
major ones that we have added that I'd like to talk about.

hg and svn support
^^^^^^^^^^^^^^^^^^

We've added support for all of the version control systems that
people have requested. When you sign up or edit a project, you can
now tell us which VCS you are using, and we'll use that to check
out your code to build your documentation.

There are two libraries that I wish existed: One to smartly parse
urls into the correct repository, and a standard VCS abstraction
that lets me treat all VCS' as the same. These would integrated
presumably, so I could do ``vcs clone <url>`` and ``vcs update``,
and it would "Just Work"

Whitelisting support
^^^^^^^^^^^^^^^^^^^^

By default we don't execute any python code when you import your
project. This is a security precaution that we take, so that means
disabling all extensions by default. A lot of people are using
autodoc and some other extensions, so we have added the ability to
whitelist projects so that they are built without any sanitization
on our part.

A sweet logo
^^^^^^^^^^^^

Our designer `Bobby <http://bobbygrace.info/>`_ made a sweet logo
for the site, and has been adding lots of little visual tweaks that
I'm not qualified to talk about :) However, it seems that whenever
I look at the site, it gets a little prettier, that's how I usually
know that design is being done.

Subdomain and CNAME support
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a really exciting one for me, because I've been learning
more and more about sysadminery lately, and this was a fun little
mixing of the two. For any project, you can now access the projects
documentation at ``<slug>.readthedocs.org``, for example, pip's
documentation is now at pip.readthedocs.org.

Now that we have subdomain support, this makes supporting CNAME's
really simple. So if you have your own domain name, and you'd like
those docs to point to us, it's simple. All you need to do is add a
CNAME record for that domain in your DNS settings to point at your
subdomain URL. Pip is another good example here,
`pip-installer.org <http://www.pip-installer.org/>`_ now is hosted
on RTD. Other notable examples are
`djangotesting.com <http://djangotesting.com>`_ and
`djangowoodies.com <http://www.djangowoodies.com>`_ :)

All of this support is
`implemented in middleware <http://github.com/rtfd/readthedocs.org/blob/1734c700caf7cdbfc43570cf3dea56c8fc11d2c5/core/middleware.py#L35>`_
and only ends up being about 25 lines of code. There are going to
be some complications when we try to add multiple version support,
and internationalization, as you can't really specify those well on
subdomains. I see us having a "default" project version, as well as
letting you have other versions hosted as well.

RTFD.org
^^^^^^^^

"RTFM" is a well known term in the programming community. Luckily
when we were scheming up names for our project, we noticed that
`rtfd.org <http://rtfd.org>`_ was available. We went ahead and
bought it, and now we're supporting ``<slug>.rtfd.org`` and
``rtfd.org/<slug>`` redirects that go to your RTD page. This is a
nice little keystroke saver, as well as a fun was to refer people
to your documentation. This is implemented simple in
`an Nginx server directive <http://gist.github.com/553773>`_. I'm
sure it can be improved upon, but it's working well at the moment.

I think adding the ability to have "smart slugs" here would be
interesting, so it could actually perform a search or something,
and return the top result, kinda like LMGTFY. This could be a neat
feature to add on.

LaTeX support
^^^^^^^^^^^^^

LaTeX is a pain to get setup, so if you want to support rendering
LaTeX, we now support that as well. The
`sympy <http://code.google.com/p/sympy/>`_ has been testing their
docs on RTD, and have helped me clean up a bunch of bugs. The
`Geometric Algebra <http://sympy.readthedocs.org/modules/galgebra/GA/GAsympy.html#what-is-geometric-algebra>`_
section shows off some of the LaTeX goodness.

*\* Update:*\* Just for kicks, we currently have 120 users and 80
projects currently hosted on Read The Docs. At least a couple of
these are using RTD as their official documentation host. I'm
pretty happy with the uptake that's already happened in the last 2
weeks (wow, that little?!). Thanks everyone for checking it out!

*\* Update 2*\* We also have a new IRC channel if you need help or
have questions, it's **#rtd on irc.freenode.net**.


