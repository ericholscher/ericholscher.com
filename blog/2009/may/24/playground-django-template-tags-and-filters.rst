:Date: 2009-05-24 10:32:59

A playground for Django Template tags and filters
=================================================

The Problem
~~~~~~~~~~~

Any sufficiently large Django project starts to have a wide variety
of Template Tags and Filters. Even Django ships with a dizzying
array of them that allow you to do all sorts of fun and interesting
things. Ellington, our CMS at work, has a ton, and I've been
thinking about ways to make tags and filters a bit more accessible
to people who are using the CMS.

I'm thinking along the lines of people who are tech savvy, but who
were just hit with a huge wall of tags and filters to look at. I
want them to be able to really easily play with the functionality
and see what it does.

The Solution
~~~~~~~~~~~~

I created a proof of concept playground for tags and filters in the
django admin. It is released as a simple third party app that I
have up on
`Github <http://github.com/ericholscher/django-playground/tree/master>`_.
Here is a small 1:40 minute screencast that explains what I did:


.. raw:: html

   <object width="600" height="400">
   

.. raw:: html

   </object><p>
   
Django Admin Playground from Eric Holscher on Vimeo.

.. raw:: html

   </p>
   
It gives you a "Play" link next to each of the tags and filters in
the admin. Once you click on that, if the docstring for the tag has
a code example, it attempts to parse that out. This allows you to
easily test out the examples that you should have in the docstrings
for your tags.

It displays the docstring above the input areas and allows you to
input context variables (naively) and render the template. It uses
Jquery to do an ajax post and response that is displayed on the
right side of what the output of the template would be.

A simple example with the Add Template Tag:

.. figure:: http://media.ericholscher.com/images/Add_Example.png
   :align: center
   :alt: Add Template Tag
   
   Add Template Tag

Caveats
~~~~~~~

This is very hacky and basic code. Totally just a proof of concept
and might not work for you. I think that the ideas are worthwhile,
and something that could be included in Django at some point.

Currently the context values are just being parsed at the : and
split into a dictionary. If anyone knows a good way to turn a basic
list like this (using YAML?) into Django objects, then I would be
all ears. I thought about it a little bit but couldn't think of an
elegant solution.

Also the parsing of the templatetag syntax out of the templates is
incredibly simplistic. If I took some time and played around with
ReST I'm sure I could figure out a better way to do that (Pulling
out the "code blocks" somehow?). But a basic regex worked well
enough to get the idea done.

Feedback welcome.


