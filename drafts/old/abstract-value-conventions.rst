.. post:: 2008-11-28 09:00:00

Abstract value of conventions
=============================

In my previous posts, I have talked about creating conventions for
django's templates. In this post I will try (and probably fail) to
talk about why conventions in general are a good thing.

Django's templates are interesting when viewed in the context of
restrictions. They are very strict in what you are allowed to do
inside of the templates, only display logic, and nothing more.
However, when defining Template Tags, we can define them *any* way
that we wish.

So when you define a template tag, you are given a parser object
and a string. There is absolutely no context associated with the
string, it just is. This allows you to define a template tag that
does anything you want, with any syntax. This power is a great
thing, but it makes a lot of things harder. I talked about this in
the
`annoyance of making template tags <http://ericholscher.com/blog/2008/nov/8/problem-django-template-tags/>`_.
The parser that Django gives you is mostly worthless for common
tasks, so you basically have to define a mini-language for each
template tag that you write.

So again, this isn't a bad thing per se. If there were a series of
common parsers that you could use to parse the template tags, then
only outlying tags would require a lot of effort. However, this
infrastructure isn't there. I talked about this, and gave an
example in the post mentioned above, so I'll leave that argument
alone for now.

The gripe that I currently have with template tags is that having
no syntax makes it impossible (or impractical) to build tools that
do anything with them. With no standard definition of what the
template tag is doing, it is almost impossible to discern what the
tag is doing without having internal access to the tag. It is also
practically impossible to pragmatically understand what that tag is
trying to accomplish. This is another place where conventions are
really handy.

Conventions allow humans to impart knowledge into a program. When
there is no syntax or convention associated with something, then
there is no way that I can tell what it is for. When you abstract
things well enough that a computer can understand them, this gives
you a lot of power.


