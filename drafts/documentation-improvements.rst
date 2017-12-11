Documentation Improvements
==========================

Current State
-------------

When we created `Read the Docs`_, 
it was because there wasn't a good solution to hosting documentation.
We created the site with the idea of making it easier to host.
I think we have solved that mission pretty admirably,
with over 6000 projects on the site now.

This has left me thinking,
what other problems might be interesting to solve.

Thinking about the problem
--------------------------

At this point I would like to ask you for ideas.
I want to think about the use cases that people have for documentation,
and try and solve some more interesting problems.

We have lots of documents now
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I think the index of all documents on the site is an untapped resource.
We are currently using this index for search,
and that is about it.
That said,
the search isn't even that great.

.. _Read the Docs: http://readthedocs.org



Have a site for generating start of docs
	- guided template
	- Capture ¶ click data as implicit bookmarks
	- Highlight interesting paragraph

	- Handle event tracking

window.onhashchange = function(ev) { console.log(document.getElementById((window.location.hash || '').slice(1))) }