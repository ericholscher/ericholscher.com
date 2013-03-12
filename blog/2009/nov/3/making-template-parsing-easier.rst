:Date: 2009-11-03 20:55:35
Making Template Tag Parsing Easier
==================================

In my
`previous post <http://ericholscher.com/blog/2009/nov/3/class-based-template-tags/>`_
about template tags, I discussed the two steps required for
template tags. Today I will be focusing on Parsing of template
tags, and how they may be improved in the framework of Class Based
Template Tags from yesterday. I have talked about
`problems with template parsing <http://ericholscher.com/blog/2008/nov/8/problem-django-template-tags/>`_
in the past as well. This post will offer 2 different approaches to
making parsing better.

I would like to thank `Cody <http://codysoyland.com/blog/>`_ and
`Chris <http://www.unbearablecomics.com/blog/>`_ who were involved
in a slightly drunken conversation that led to these tags. Chris
actually wrote the other neat parsing implementation that I will
talk about today. Cody wrote the underpinnings of that
implementation as well.

**Note:** Both of these approaches are more Proof of Concepts, and
the code probably shows. Please don't knock implementations, and
just think about the ideas housed within.

Parsing from above - A DSL approach
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I'm going to go ahead and start talking about an approach to
parsing template tags that was pointed out in yesterday's comments.
It takes `surlex <http://github.com/codysoyland/surlex>`_ which is
made for easily parsing URL's, and applies it to the concept of
parsing template tags.

In the `tag\_utils <http://github.com/chrisdickinson/tag_utils/>`_
package, I looked at
`the tests <http://github.com/chrisdickinson/tag_utils/blob/master/tag_utils/tests.py#L60>`_,
because they make great documentation. Here is an example of a
`tag definition <http://github.com/chrisdickinson/tag_utils/blob/master/tag_utils/tests.py#L74>`_.

::

    p = ParsedNode('test', '<arg1:int> <arg2:string> <kw:kwarg>', test_expected) 
    register.tag('test', p)

This defines a tag called test, which parses an int, string, and
kwarg from a surlex expression. The third argument is a function
that is executed on the arguments on rendering.

This allows you in your test\_expected function, to act on the
arguments that are defined inside of the surlex expression. A
trivial example of the test\_expected function is:

::

    def test_expected(context, arg1, arg2, kw=None):
        print "Got %s and %s" % (arg1, arg2)

So if you called the tag ``{% test 1 racoon %}``, it would print
out ``Got 1 and racoon``.

This is an interesting way to provide a sort of DSL on top of the
current mess that is parsing of template tags. I really like how it
reuses Surlex, which was made for parsing URLs. However, parsing
template tags is a similar task, and it works well here too!

I could imagine this easily being bolted on to the approach from
yesterday, which might allow for easier subclassing and reuse of
the parsing functions.

Parsing based on keywords
~~~~~~~~~~~~~~~~~~~~~~~~~

An approach that I have talked about in the past is basically a
subset of the above idea. It allows you to define kwarg type
arguments for your tags, and have them magically parsed out for
you. An example of this is my own
`SelfParsingTag <http://github.com/ericholscher/django-playground/blob/master/nodes.py#L74>`_.
The following lines allow you to specify what arguments your tag
will accept.

::

        def __init__(self, required_tags=[]):
            if not required_tags:
                self.required_tags = self._get_tags()
            else:
                self.required_tags = required_tags
    
        def _get_tags(self):
            return []

So you can either define the ``_get_tags`` function, or pass the
allowed tags into the call when you make the tag. The following 2
bits of code are equivalent.

::

    class GetContentTag(SelfParsingNode):
        def _get_tags(self):
            return ['as', 'for', 'limit']
    register.tag('get_latest_content', GetContentTag())
    
    #Is the same as the following:
    
    class GetContentTag(SelfParsingNode):
        pass
    register.tag('get_latest_content', GetContentTag(['as', 'for', 'limit']))

Once the Tag knows what it arguments it will be accepting, it
`parses them <http://github.com/ericholscher/django-playground/blob/master/nodes.py#L13>`_.

::

    def parse_content(self, parser, token):
        parsed = parse_ttag(token, self.required_tags)
        for tag, val in parsed.items():
            setattr(self, '_' + tag, val)
        return parsed

This effectively sets a private varible on the tag to the value of
the arg. So for example, if the tag was called
``{% sweet_tag for news.story as my_stories limit 10 %}``, then
``self._for`` would equal ``news.story``, and so on. It also
returns the parsed values as a dictionary. There are a lot of
improvements that could be made to ``parse_ttag``, but it works as
a basic implementation.

This approach allows us to implement a tag really easily. If you
want a (silly) tag that just updated the context with whatever
value you input, you could make a simple tag. It would be used
``{% my_tag with "awesome text" as context_var %}``

::

    class SimpleContextTag(SelfParsingTag):
        def _get_tags(self):
            return ['with', 'as']
    
        def render_content(self, tags, context):
            for tag in self.required_tags:
                context.update({tag['as']: tags['with']})
    
    register.tag('my_tag', SimpleContextTag())

To implement the get\_latest\_object code from yesterday, we can
skip all of the parsing steps.

::

    class GetContentTag(SelfParsingTag):
        def _get_tags(self):
            return ['as', 'for', 'limit']
    
        def render_content(self, context):
            self.model = get_model(*self._for.split('.'))
            if self.model is None:
                raise template.TemplateSyntaxError("Generic content tag got invalid model: %s" % model)
            query_set = self.model._default_manager.all()
            context[self._as] = list(query_set[:self._limit])
    
    register.tag('get_latest_object', GetContentTag())

Which is better?
~~~~~~~~~~~~~~~~

To be truthful, I like the Surlex approach better than my own. It
seems to have a lot of the benefits of mine, but with added
flexibility. However, that does come with the implementation being
a bit more complex. It brings some really neat ideas forward about
how template tags might be handled differently. It allows for
optional arguments, does basic type checking (based on it's regex
nature), and ensures that the order of the arguments is the same.

I could imagine some kind of dispatch based template tag scheme
that has a list of URLs, basically like the URLConf and view
structure. I think that this problem has a lot more depth to it,
and hopefully by pointing out a couple of different ways of solving
it, and looking at it, we can improve the situation.


