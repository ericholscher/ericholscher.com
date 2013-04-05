:Date: 2008-11-20 20:24:01

Gentlemans agreement on Django templates
========================================

There are a lot of reusable apps out in the Django Ecosystem. I
wrote a
`previous post <http://ericholscher.com/blog/2008/nov/14/should-reusable-apps-have-templates/>`_
about why I think that reusable apps should come with templates.
There is a problem about distributing templates that I want to
address with this post: the problem of Django Template Block
names.

There are already some unwritten conventions in the community in
regards to block names, and I think that talking about it will
help. I don't think that we're going to be able to come up with a
way that everyone will follow, but I think it would be nice if we
could create a way to easily redistribute templates.

The main reason that I have been thinking about this is because of
`Pinax <http://pinaxproject.com>`_, they use some different
template block name than my apps. So in order to use PInax and my
app, I needed to change all of the blocks of my templates! That is
a lot of work that could have been avoided by some
standardization.

There are a lot of different ways to think about the content of a
page, but I'm going to propose some basic template blocks that most
pages will have, and then talk about some more 'extended' blocks
that might be useful.

Blocks we need.
---------------

{% block title %}
^^^^^^^^^^^^^^^^^

This will be the block where you define the title of the page.
Presumably your base.html will define your Site's name (perhaps
even using the Sites framework) outside of this tag, to be places
on all pages.

{% block extra\_head %}
^^^^^^^^^^^^^^^^^^^^^^^

I think that this is a good one that most people are already using
in some form or another. In your base template you have a set of
things in your ``<head>`` that every page will have. However, a lot
of other pages need things that they also want to put in the head
of a document, like RSS feeds, Javascript, CSS, and all the other
things that should go in the head. You can and probably will have
other specialized blocks (like title above) that will fill in other
parts of the head too.

{% block body %}
^^^^^^^^^^^^^^^^

This tag will be placed around the entire body section of the page.
This allows you to create pages in your app that replace the entire
page, not just the content. This won't be used a lot, but it's a
really handy tag to have when you need it. If you haven't noticed,
I've been trying to keep tag names consistent with their html tag
names whenever possible.

{% block menu %}
^^^^^^^^^^^^^^^^

This would be where your menu goes. It would be the site-wide
navigation, and not a per-page type of navigation.

{% block content %}
^^^^^^^^^^^^^^^^^^^

This will be the place where you define the content on a page. This
will presumably change on every page. It will not include any site
navigation, headers, footers, or anything else that would belong in
a base template.

Other possible blocks
---------------------

{% block content\_title %}
^^^^^^^^^^^^^^^^^^^^^^^^^^

This would be where the "title" of a content block would be. It
includes the title of a blog. It can also include some kind of
navigation between content, or other things like that. Presumably
something that isn't the main pages content. I don't know if this
should go inside the ``content`` tag and have a ``main_content`` as
opposed to the ``content`` tag proposed above.

{% block header %} {% block footer %}
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Any text area in the header of footer that might change on a
page-by-page basis.

{% block body\_id %} {% block body\_class %}
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This would be used to set the class or id of the body tag in the
document. This is useful to set for styling and other properties.

{% block [section]\_menu %} {% block page\_menu %}
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This would be opposed to the ``menu`` block proposed above. It
would be for the section or page.

**Edit**: Updated back to include \_'s. Because I think thats more
pythonic and looks better. The Django Admin isn't meant to be a
reference implementation of the templates.

A lot of these ideas have been taken from
`Nathan <http://playgroundblues.com>`_ and his
`base.html <http://code.google.com/p/django-basic-apps/source/browse/trunk/blog/templates/base.html>`_
for basic-blog. I'm sure that he and
`Christian <http://mintchaos.com/>`_ have put way more thought into
this than I have. I'm just curious what people think, and if
there's something crazy that I have missed..


