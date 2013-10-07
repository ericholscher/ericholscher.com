.. :date: 2013-10-08 2:00

Announcing Grok the Docs
========================

	| Are my docs working? 
	| Are folks getting what they need?

I've asked myself these questions a lot.
Historically I have put Google Analytics on my doc pages,
and called it good.
I would browse over the Analytics data every once in a while,
gleaning basically zero interesting data out of it.

`Read the Docs`_ hosts a lot of documentation,
and I want to help these folks understand how their docs are being used.
So I have been working on a project for the last month called `Grok the Docs`_.

`Grok the Docs`_ is a bit different,
with the main difference being it embeds the information in the page for you.
This is interesting because it adds context to the data.
The main interface to Grok the Docs are keyboard shortcuts within the documentation page.
So you can access information about the current page you're on,
while you're browsing the documentation.
Check out the :ref:`example` below to see it in action.

Surfacing analytic data in the page is great for the maintainer and user alike.
The maintainer can see what parts of their docs are being heavily used,
and which parts aren't being used as much.
Users can see where other people are ending up,
which is probably where they want to go too.

This is very much just a tech demo currently.
I would love feedback from folks about how I could improve the display of the data.
Currently it's something that you `need to enable`_.

It would be great if you have ideas for other additoinal functionality that could be added.
This is very much an experiment currently,
so I'd love to hear any thoughts you have.
Please `email`_ or `tweet`_ me if you have feedback or ideas.

Once the code is more baked and solid,
the plan is to turn it on for all Read the Docs users.
After I do a full rollout across Read the Docs,
I'll consider opening it to other people.
The code is currently closed source,
and will likely remain so.
The idea is that this might become a product that can suppliment my Gittip income.
If it fails as a product,
I will then open source it.
That said,
it will always be free for documentation on Read the Docs.

This project was done as part of my :doc:`ongoing work </blog/2013/sep/25/help-me-improve-documentation>` to improve documentation.
If you think this work is important,
you should `support me on Gittip`_.

.. _Read the Docs: http://rtfd.org
.. _Grok the Docs: https://api.grokthedocs.com
.. _email: mailto:eric@ericholscher.com
.. _tweet: http://twitter.com/ericholscher
.. _need to enable: https://api.grokthedocs.com/#try-it-out
.. _support me on Gittip: http://www.gittip.com/ericholscher

.. _example:

Example
-------

This shows how user might harness this data.

.. image:: https://dl.dropboxusercontent.com/u/372293/GTD-Example.gif
	:width: 800px

	
