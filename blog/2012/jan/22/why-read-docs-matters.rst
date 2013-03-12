:Date: 2012-01-22 14:08:01

Why Read the Docs matters 
==========================

Documenting projects is hard, hosting them shouldn't be.
`Read the Docs <http://readthedocs.org>`_ was created to make
hosting documentation simple. I think that we have solved this
problem well, but now we need to start thinking about the larger
picture.

Along with hosting, Read the Docs was created with 2 other main
goals. One was to encourage people to write documentation, by
removing the barrier of entry of hosting. The other was to create a
central platform for people to find documentation. Having a shared
platform for all documentation allows for innovation at the
platform level, allowing work to be done once and benefit everyone.
Having run the site for over a year now, I think there is a third
thing that we should be striving for. That is to make the quality
of documentation better.

I think that **we can help a documentation culture flourish**
within the open source world.
`Django <https://docs.djangoproject.com/en/1.3/>`_ is a shining
example of what a project with great documentation can do, and it
has a community that values docs more than the norm. I think we can
help
**spread this culture throughout the Python world, and beyond**.
This has already started, and I want to think about how something
like RTD can help.

What we can do to help
----------------------

I think that having a **guide for writing useful documentation**
would be a great step towards helping people along the path of
documentation enlightenment. Jacob Kaplan-Moss has started down
this road with his
`blog series <http://jacobian.org/writing/great-documentation/>`_
and Pycon 2011 `talk <http://blip.tv/file/4881071>`_ on this
subject. I think that we could start by collecting these into a
section of the site.

We could build on top of that great start with simple guides for
how to get started with Sphinx, best practices for documentation,
and providing a general place to learn more about how to write good
documentation. Since we host a lot of documentation, we could point
to live examples of techniques, and provide helpers for people to
enable the techniques.

I have started a
`reStructedText Philosophy <http://restructuredtext-philosophy.readthedocs.org/en/latest/index.html>`_
document that is meant to help people understand the ideas behind
how reST works, so that it isn't as mystifying. This
`reST cheatsteet <http://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html>`_
also appears to have similar goals. These are a very basic start,
and I think some more along these lines would really help a lot of
people get over the barrier to starting and continuing to write
good documentation.

I think that we could also help **create contributors** to
projects, if we could find an easy way to provide patches to
documentation. If you could go to the project documentation, and
fix small typos, or help add a paragraph in the tutorial, it would
lower the bar to helping.

However, it isn't a wiki. These changes would be represented to the
project author as pull requests in their VCS, and they would still
be responsible for tending the garden. This gets rid of the "Just
Edit The Wiki" solution of documentation, and also helps new
contributors get started in an easier fashion.

The Plone community has built a
`proof of concept, linking to Github's edit pages for the current document <http://opensourcehacker.com/2012/01/08/readthedocs-org-github-edit-backlink-and-short-history-of-plone-documentation/>`_.
I think we can integrate this at the platform level, and make it
available to everyone.

Want to help?
-------------

Read the Docs is
`open source <https://github.com/rtfd/readthedocs.org>`_. You can
help by writing docs for the site, writing code for the site, or
just writing documentation in general. People can also help just by
using the site, and reporting bugs. Telling us how to make the site
better helps everyone in the long run. Come join us on Freenode in
the #readthedocs channel as well.

Another area that we're hurting is in the design front. We have
been adding features over time, and the design of the site is
getting a bit strained. Having someone with a good sense of design
help re-think and re-architect some of the features and ideas that
we've been working on I think would help a lot.

A lot of the RTD contributors will be at Pycon 2012, where we will
be having a sprint on the site. If you want to get started
contributing, that is a great place to come and get started.


