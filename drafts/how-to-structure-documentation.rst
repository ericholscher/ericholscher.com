How to Structure Documentation
==============================

I think that one of the scariest things about writing documentation is staring at a blank page.
It can be overwhelming not knowing where to start.
I'd like to cover a bit about the structure of documentation in this post,
including a set of recommended files and some basics around what to put in them.

If you want another good place to get started,
I recommend this `set of posts`_ from Jacob Kaplan-Moss about writing documentation.

.. _set of posts: http://jacobian.org/writing/great-documentation/

Structure
---------

Files I like to include:

Design Document
~~~~~~~~~~~~~~~

This is a high level overview, or *rease de ente*, for your project.
It should explain why your project was created,
instead of using one of the existing projects in your space.

It should explain the various tradeoffs that your project made in it's creation.
Did you choose a specific algorithm or development methodology? Why?

Architecture Document
~~~~~~~~~~~~~~~~~~~~~

This is lower level than the Design doc.
It should be the introduction to the layout of your source code.
What do certain files do?
Why are they placed where they are?
If I want to change the way *X* works,
where should I look?



