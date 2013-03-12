:Date: 2009-11-11 18:42:40

Large Problems in Django, Mostly Solved: APIs
=============================================

This is the third part of my Large Problems Series. The first two
were
`Search <http://ericholscher.com/blog/2009/nov/2/large-problems-django-mostly-solved/>`_
and
`Database Migrations <http://ericholscher.com/blog/2009/nov/6/large-problems-database-migrations/>`_.

A lot of efforts have come and gone in the Django space, trying to
provide a API's that do various things. Some have tried to give you
automatic CRUD based off your models or by abstracting the admin,
others have extended Django serializers to provide some kind of
functionality, and there have been lots of other approaches.

I think that
`Piston <http://bitbucket.org/jespern/django-piston/overview/>`_
hits a sweet spot for creating APIs. It has a lot of nice little
features, and handles the general use case well. It is also
abstract enough that it allows you to provide your own layer on top
of it with ease.

Piston
~~~~~~

`Piston <http://bitbucket.org/jespern/django-piston/>`_ has three
major philosophical concepts that are important; Resources,
Handlers, and Emitters. A Resource is the "thing" that you are
trying to represent in your API, the domain object. This could be a
blog post, a user, or anything else. A Handler is how you do
something with that resource. It is a lot like a view, where you
get the request and it delegates to different functions based on
what you want to do (create, update, read) with it. The Handler
will return some kind of object, and the Emitter's job is to output
this. It is where you choose the format (xml, json, yaml) and other
information about how the data is returned.

The way these things are abstracted makes it really easy to create
a REST API. In fact, the documentation has a
`full working example <http://bitbucket.org/jespern/django-piston/wiki/Home#fully-functional-example>`_.

I would like to talk about some of the nicer features and abilities
of Piston.
**This is not a tutorial, but more a pointer, so that you know it exists and kicks ass.**
The
`Piston Documentation <http://bitbucket.org/jespern/django-piston/wiki/Documentation#piston-documentation>`_
is decent in regard to getting you going.

Useful Features
~~~~~~~~~~~~~~~

Authentication: OAuth, Basic Auth
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I have found
`OAuth <http://bitbucket.org/jespern/django-piston/wiki/Documentation#authentication>`_
something of a pain to implement when I tried to do it on my sites.
Piston handles this for you, and does a good job of it! This gives
you a really nice authentication scheme for your API users for
free. If you need something simpler, HTTP Basic Auth is provided
out of the box as well. The Authentication is also tied in
automatically to the Django Authentication scheme, making this
relatively hard problem of API's incredibly simple. This gives you
both ranges of Authentication mechanisms, simple and advanced,
without touching a line of code.

Automatically handles different serialization formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Out of the box you also get
`serializers <http://bitbucket.org/jespern/django-piston/wiki/Documentation#emitters>`_
for JSON, YAML, Python Pickle, XML, and Django's own model
serialization format. By default, if you append ?format=X to a URL
of a piston resource, it will automatically return the data in that
format. Thinking about serialization formats is basically
non-existent.

Guides you towards proper REST practices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Piston by default and convention returns the
`correct status <http://bitbucket.org/jespern/django-piston/wiki/Documentation#helpers-utils-decorators>`_
codes for events. It even has a convinent ``rc`` module that maps
response codes to names, to make it super simple to know what you
want to return. You have to try to not follow proper REST
convention.

::

    if not request.user == post.author:
        return rc.FORBIDDEN # returns HTTP 401

API isn't tied to models
^^^^^^^^^^^^^^^^^^^^^^^^

Tying your API to your models seems like a good idea at first.
However, you quickly want to return objects from other models,
results of methods, and other data that isn't related to your
model. Piston to start out lets you define a model to tie it to,
but this simply sets sane defaults for the handler methods. Once
you override these methods, the fact that parts of the handler is
tied to a model doesn't matter. You can keep providing the basic
parts that you don't want to write, but extend where you need more
advanced functionality.

Lots more, built in
^^^^^^^^^^^^^^^^^^^

Piston has just a ton of really useful things that you need built
in, and well configured. Among the things that I haven't mentioned,
but that you will appreciate:


-  `Throttling <http://bitbucket.org/jespern/django-piston/wiki/Documentation#throttling>`_
   (by view, user, or IP)
-  `Streaming Responses <http://bitbucket.org/jespern/django-piston/wiki/Documentation#streaming>`_
-  `Form Validation <http://bitbucket.org/jespern/django-piston/wiki/Documentation#form-validation>`_
   (using Django's form library)
-  `Generated Documentation <http://bitbucket.org/jespern/django-piston/wiki/Documentation#generating-documentation>`_
   (allowing you to document the methods you have available)

Conclusion
^^^^^^^^^^

Piston is just incredibly well configured by default. You can write
a couple of lines of code, and most of the features that you expect
in an API are there for you. However, this doesn't mean that it is
limiting you from doing complex things as well. All of the
important bits are sanely configured, but easily pluggable. It is a
really amazing piece of work when you dig down into it and realize
that most things you want to change are simple.

Like Django and Python,
**piston makes doing the correct thing simple and obvious.** If you
end up fighting against the app, you're more than likely doing
something wrong.

I know I didn't get all the way into piston, and it is amazingly
well written. There are lots of little niceties hiding in dark
corners, instead of demons. I would love to see this project get
more attention, tutorials, and blog posts in the community. Are you
using Piston? Is there something you love or hate? Let me know, or
even better, blog about it!


