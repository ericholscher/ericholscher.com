.. post:: 2008-11-11 18:37:12

Practical Django Test Examples: Models
======================================

Today we will be continuing the series of
`practical django testing </tag/practical/%20which%20is%20part%20of%20my%20over%20arching%20[testing%20series](/tag/testing-series/>`_,
working on Models. In the last post I covered Views. Models are the
other really big component that you will need to test for almost
every app that you write.

Again today, we'll be doing our testing on
`Nathan <http://playgroundblues.com>`_'s great
`basic blog <http://code.google.com/p/django-basic-apps/source/browse/trunk/blog/>`_.
This time we will be focusing more on models than on views, so the
tools and outcome we're looking for will be a bit different.

Since this part of the app doesn't really have any legacy code, I'm
going to use Unit tests this time instead of Doc tests. This will
allow us to use fixtures easily, write more manageable tests, and
allow me to show you some other tips and tricks that are useful in
the realm of testing. So let's get started.

What outcome we're looking for
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We want to have all of the model tested. This generally means all
of it's Methods, Managers, and Meta (alteration FTW). It also means
being able to save, edit, and delete it. Presumably the choice on
what operations to test in the
`CRUD <http://en.wikipedia.org/wiki/Create,_read,_update_and_delete>`_
section will depend on what you're doing in your models. The blog
is actually rather view heavy


