A new theme for Read the Docs
=============================

`Read the Docs`_ hasn't changed much visually since it launched.
We have had a default theme that is a slight change over the Sphinx theme.
A few colors and a nice mobile interface was about it.

That is all about to change.
We are proud to announce a `new default theme`_ for Read the Docs!

Creation Story
---------------

`Dave Snider`_ approached me about a month ago,
offering to help improve the documentation ecosystem.
He is a designer with an interest in documentation,
and wanted to help out with Read the Docs.

He has built a fantastic new default theme for Read the Docs.
We talked through a lot of the functionality of the site,
and how people tend to use documentation.
I think we have come up with a really great solution that will look great,
but also work well.

Using it
--------

There are 2 ways that you can use this theme on Read the Docs.
The first is to simply leave your ``html_theme`` variable set to ``default``.
This is now the default Read the Docs theme.
You can also set ``RTD_NEW_THEME = True`` in your project's ``conf.py``,
and we will use our theme when building on Read the Docs no matter what ``html_theme`` is set to.

After you change these settings,
simply rebuild your docs and the theme should update.
More information about the theme can be found on the `theme documentation page`_

If you want to continue using the old theme,
simply set ``RTD_OLD_THEME = True`` in your ``conf.py``. 

Screenshots
-----------

Full site
~~~~~~~~~

The full documentation page is now beautiful and streamlined.
We got rid of a bunch of the visual clutter and integrated a full-project Table of Contents on the left side.
When you go into a specific page,
the page-level contents get embedded in the sidebar as well.
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

Sidebar
~~~~~~~

The sidebar is a major feature of Read the Docs.
For a project with a custom theme,
it is the only interaction with Read the Docs.
This means we need to pack most of the functionality we offer into a small space.

In the new theme,
the sidebar is integrated into the bottom left of the theme.
For all other projects,
it stays in the same place in the bottom right.
If you have a theme and want to better integrate our sidebar,
please let me know.

The old version was very simple,
providing access to a version selector.
With the new version we wanted to do more.

Old
***

The old badge let you:

	* Change versions
	* Go back to Read the Docs

.. image:: http://i.imgur.com/CBDPzbD.png
	:width: 50%
	:target: http://i.imgur.com/CBDPzbD.png

New
***

The new badge lets you:

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

Conclusion
----------

I think that this theme is a great addition to the documentation ecosystem.
It is highly functional and beautiful,
allowing users to easily navigate and find what they need.

I hope that you enjoy using it.
If you have any feedback, 
please `open an issue`_ on GitHub for the repo.

If you want to support work like this,
help `fund development on Read the Docs`_ on Gittip.

.. _new default theme: http://docs.readthedocs.org/en/latest/
.. _fund development on Read the Docs: https://www.gittip.com/readthedocs/
.. _Read the Docs: http://readthedocs.org/
.. _Dave Snider: https://twitter.com/enemykite
.. _open an issue: http://github.com/snide/sphinx_rtd_theme/issues
.. _theme documentation page: http://docs.readthedocs.org/en/latest/theme.html