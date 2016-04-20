.. post:: 2009-05-27 15:06:52

Django Admin and Docs Integration
=================================

The Problem
~~~~~~~~~~~

Landing in a Django Admin page that is empty is a rather confusing
experience. You are dropped in to an empty list with an add button,
where you have to figure out what to do. You click to add a new
object, and are presented with a big list of empty fields that
hopefully have some kind of help text.

This is about the worst experience that you can have as a new user.
The 37 Signals people
`talk a lot <http://gettingreal.37signals.com/ch09_The_Blank_Slate.php>`_
about the first experience of a user, and how they should be shown
how to do the right thing. I think that there needs to be some
discussion and work done around making the admin much more
welcoming to a first time user.

There has been a lot of talk about an admin redesign, but that is a
huge project that will take a long time. I am thinking more about
little changes that could be implemented in a third party
application that would help out this experience a lot.

A partial solution
~~~~~~~~~~~~~~~~~~

I don't know what the correct answer to this is, but almost
anything we do would be better.


