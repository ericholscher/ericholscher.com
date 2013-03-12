:Date: 2009-11-03 15:32:07
Class Based Template Tags
=========================

The problem
~~~~~~~~~~~

In Django, template tags currently are separated between a Node
class and a "parsing function". The parsing function takes the tag,
represented as a string, parses the input, and passes the correct
arguments to a Node class. The Node class then does whatever
rendering it does, or updating of the context, and then renders
itself in a form suitable for the template.

This is mainly by convention that there is a separation here
between the parsing and the Node. As I see it, there is no
particular reason that the Tag can't be responsible for the parsing
and rendering itself. A lot of the time I find the parsing function
and the Node separated by hundreds of lines in a file, making it
hard to understand.

The proposed solution
~~~~~~~~~~~~~~~~~~~~~

We can combine the parsing and rendering of a node in a similar way
in something I call
`Class Based Template Tags <http://classbasedtemplatetags.bikeshed.com/>`_.
This allows the template tag to be able to parse and render
itself.

I have an example in
`my playground <http://github.com/ericholscher/django-playground/blob/8f3a6908f35afa66166a07a6b3e89cf1696c3afc/nodes.py#L40>`_
over at github. They are based around a lot of the ideas in
`django-template-utils <http://bitbucket.org/ubernostrum/django-template-utils/src/>`_.
Specifically, this example will be recreating the
`get\_latest\_objects <http://bitbucket.org/ubernostrum/django-template-utils/src/tip/template_utils/templatetags/generic_content.py#cl-66>`_
tag from that package.

::

    class ClassBasedTag(template.Node):
        """
        Tag that combined parsing and rendering
    
        Subclasses should define ``render_content()`` and ``parse_content()``.
        """
    
        def __call__(self, parser, token):
            self.token = token
            self.parser = parser
            return self
    
        def render(self, context):
            self.context = context
            self.parsed = self.parse_content(self.parser, self.token)
            return self.render_content(context)
    
        def parse_content(self, parser, token):
            """
            This is called to parse the incoming context.
    
            It's return value will be set to self.parsed
            """
            raise NotImplementedError
    
        def render_content(self, context):
            """
            This is called to return a node to the template.
    
            It should return set things in the context or return
            whatever representation is appropriate for the template.
            """
            raise NotImplementedError

As you can see, this tag combined the concepts of Parsing and
Rendering a tag into the same place. The ``parse_content`` and
``render_content`` are equivalent to the current Django way of
doing a parsing function, and Node class render function. Currently
the render function depends on self.parsed being there, and not
being passed in, this is to keep the function arguments the same as
previous render functions. The code isn't meant to be production
quality, more of a proof of concept.

A couple of gains are made from combining things together. First of
all is the fact that the code is right next to each other, as
mentioned earlier. However, it also allows you to subclass these
classes, and provide functionality that makes people's lives
easier. Having the rendering and parsing in the same class also
allows for some trickery with passing around data, like mentioned,
which may be a good or a bad thing.

Let's go ahead and show an example of an implementation of this
type of tag.

::

    class GetContentTag(ClassBasedTag):
    
        def parse_content(self, parser, token):
            bits = token.contents.split()
            return (bits[1], 1, bits[3])
    
        def render_content(self, context):
            model, pk, varname = self.parsed
            self.pk = template.Variable(pk)
            self.varname = varname
            self.model = get_model(*model.split('.'))
            context[self.varname] = self.model._default_manager.get(pk=self.pk.resolve(context))
    
    register.tag('get_latest_content', GetContentTag())

This tag is used in the following manner:

::

    {% get_latest_content news.story as latest_story %}

As you can see, I think it makes it nice and concise to be able to
have the parsing and the rendering of a tag right there in the same
place.

This code is a very simplified use case for the idea. It is
basically the simplest possible thing that could work. I will
expand on the ways that this idea gives us a lot of power and
flexibility over our Template Tags in the future, but I think this
idea stands well on it's own.


