:Date: 2013-11-04 10:00:00

A New Theme for Read the Docs
=============================

We have been `hard at work`_ improving `Read the Docs`_ over the past month.
A large amount of back end work has been going on,
and now we have a brand new documentation theme to showcase it.

We have looked at how people use documentation,
and built a beautiful and highly functional `new interface`_ for browsing documentation.
We created a solution that looks great and works well.

Creation
--------

`Dave Snider`_ approached me about a month ago,
interested in helping improve the documentation ecosystem.
We talked about what could improve the Read the Docs experience for the greatest number of our users, 
and a new theme seemed like a great place to start.

The New Theme
-------------

Full site
~~~~~~~~~

The full documentation page is now beautiful and streamlined.
We got rid of the visual clutter and integrated a full-project Table of Contents in the sidebar.
When you go into a specific page,
a page-level contents get embedded in the sidebar as well.
This allows you to keep context inside the documentation when you land on a page from a search.

Old
***

.. image:: http://i.imgur.com/hWOnmKy.png
	:width: 100%
	:target: http://i.imgur.com/hWOnmKy.png

New
***

.. image:: http://i.imgur.com/7oLntvR.png
	:width: 100%
	:target: http://i.imgur.com/7oLntvR.png

Flyout
~~~~~~

Read the Docs provides a lot of functionality for documentation projects.
The flyout is the avenue to accessing that functionality.
We need to pack all our functionality into this space.

In the new theme,
the flyout is integrated into the bottom left of the theme.

Old
***

The old flyout let you:

	* Change versions
	* Go back to Read the Docs

.. image:: http://i.imgur.com/CBDPzbD.png
	:width: 50%
	:target: http://i.imgur.com/CBDPzbD.png

New
***

The new flyout lets you:

	* Change versions
	* Go back to Read the Docs
	* See the current version
	* Show if the current version is out of date
	* Download docs for offline viewing
	* Contribute edits on GitHub or Bitbucket
	* Do a full-text search (Coming soon)

.. image:: http://i.imgur.com/9DRP8fj.png
	:width: 50%
	:target: http://i.imgur.com/9DRP8fj.png

Mobile
~~~~~~

The new theme really shines on mobile.
We provide a beautiful interface for phones and tablets,
while staying completely functional.

.. image:: http://i.imgur.com/29uEpVs.png
	:width: 100%
	:target: http://i.imgur.com/29uEpVs.png

Using it
--------

There are two ways that you can use this theme on Read the Docs.
The first is to simply leave your ``html_theme`` variable set to ``default``.
This is now the default Read the Docs theme.
You can also set ``RTD_NEW_THEME = True`` in your project's ``conf.py``,
and we will use our theme when building on Read the Docs no matter what ``html_theme`` is set to.

After you change these settings,
simply rebuild your docs and the theme should update.
More information about the theme can be found on the `theme documentation page`_

If you want to continue using the old theme,
simply set ``RTD_OLD_THEME = True`` in your ``conf.py``.


Conclusion
----------

This theme is a great addition to the documentation ecosystem.
It is highly functional and beautiful,
allowing users to easily navigate and find what they need.

We have a few more tricks up our sleeves,
but theme is ready to launch today.
Over the next few weeks we'll be adding a bit more functionality to it,
which should be even more delightful.

I hope that you enjoy using it.
If you have any feedback,
please `open an issue`_ on GitHub.
To follow announcements for Read the Docs,
follow `us on Twitter`_.

If you want to support work like this,
help `fund development on Read the Docs`_ on Gittip.

.. _hard at work: https://github.com/rtfd/readthedocs.org/pulse/monthly
.. _new interface: http://docs.readthedocs.org/en/latest/
.. _fund development on Read the Docs: https://www.gittip.com/readthedocs/
.. _Read the Docs: http://readthedocs.org/
.. _Dave Snider: https://twitter.com/enemykite
.. _open an issue: http://github.com/snide/sphinx_rtd_theme/issues
.. _theme documentation page: http://docs.readthedocs.org/en/latest/theme.html
.. _us on Twitter: http://twitter.com/readthedocs
