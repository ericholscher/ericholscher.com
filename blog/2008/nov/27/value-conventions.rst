:Date: 2008-11-27 05:00:00
The value of conventions, aka testmaker for template tags.
==========================================================

A couple
`posts ago <http://ericholscher.com/blog/2008/nov/20/gentlemans-agreement-django-templates/>`_,
I talked about how we should have conventions for the names that we
use in Django Template Blocks. Today I will be talking about the
value that is gained from this kind of structure.

Use Cases
~~~~~~~~~

Template Tags
'''''''''''''

My use case for Template tags is what started me thinking about
this. Some of you may know that I have created a testmaker
application for Django. This allows you to automatically test your
view code, based on a browser session. Once I got most of the kinks
worked out in this code, I started thinking about what the next
best thing to test would be. I came up with template tags...

This is where I ran into a problem. With no context associated with
a template tag, there is no way to create a tool which tests
template tags well. At first I simply started out trying to test
the template tags by pulling them out of the template verbatim.

::

    {% load blog %}{% get_latest_posts for blog.post as posts limit 10 %}

However, when you try and test this, it doesn't work. That is
because all this code is doing is settings a context variable, and
not outputting anything. You can create tests for trivial template
tags that just output a string, but a lot of template tags set
context variables. So without some kind of convention here, it is
impossible to write a tool that will automatically write a test for
you. That sucks!

Luckily in Django, the above test is representative of a kind of
convention in django template tags. Most template tags use the
syntax ``as [context_var]`` to set a variable in the context. So I
went ahead and wrote some code that parses template tags for these
kind of strings.

This code is valuable for some people, but is worthless if people
use another syntax for defining context variables. This I think is
a really good example of where syntax (or convention) allow you to
do more than you previously could.

You can take a look at the source code
`here <http://github.com/ericholscher/django-test-utils/tree/master/test_utils/middleware/testmaker.py#L83>`_.
It's still a bit rough, like most of my first releases it is more
of a proof of concept.

Template Blocks
'''''''''''''''

So if we create a convention for Template blocks like I proposed in
my previous post, this gives us some really neat possibilities. We
can now create a base template that "knows" what will be included
in each of it's sections. So in turn we create a way to provide
skins or themes for Django Sites, that would be portable between
Installations.

Of course, how far we take these conventions will limit how
portable, powerful, and easy to replicate the designs will be. If
we say that all items in a ``menu`` block have to be
``<ul class=menu_item>``, then we can provide more functionality in
our portable base template. This is a bit too specific though,
because not all menus are lists. However, even with just a simple
structure around your base template, you can create some really
nice portable templates. You can create 1 and 2 column layouts,
simply based on where the menu, content, header, and footer are for
example.

I think it will be interesting seeing where we can embrace
conventions where possible, for the betterment of all. I think that
having Django Skins would be really neat :). Also, having tests
automagically generated for template tags is a big win. For no
other reason than because it does the boilerplate stuff for you.

Other places
''''''''''''

I think that there are more places where conventions could benefit
us. I think I'm going to create a section in my projects on this
site dedicated to conventions for Django. Hopefully serving as a
reference for other people who are trying to use conventions in
their Django apps.


