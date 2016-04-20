.. post:: 2008-11-08 00:00:00

The problem with Django's Template Tags
=======================================

There are a lot of things that I love about Django. Template tags
are one of them. However, they do have a couple of warts that
bother me. I know that there's a problem when I actively look for
another way to accomplish something instead of writing a template
tag. I view them as a kind of last resort; thinking 'can't we
accomplish this with a Manager instead'? I think that we need to
work on making useful template tags a little bit easier to make.
Django goes a long way in doing this with the simple\_tag and
inclusion\_tag types of tags. However, I think there needs to be
something more.

When I look at how template tags are implemented, it seems that
most of the Node classes are implemented the same way. This means
that this implementation is probably sane. A lot of the differences
I see are in the way that input is parsed. Template tags are
basically just a string that is then passed to a function. The
template tag function is responsible for parsing this string
correctly and passing it off to a Node to be rendered. Because a
template tag string can in theory contain anything, it makes it
really hard to parse these strings in any kind of standard way. I
think that this is generally a good thing, because this flexibility
is nice when you're trying to do really complex things. However, I
think that we can create some relatively simple tools that will
help us wrangle 95% of common cases.

I don't know if the right answer is to include something in Django.
So I'm going to look through the different approaches that I've
seen taken to parsing template tags, and try and figure out the
best way to do it. If there's another way to do these, then please
let me know.

If len(bits) == MAGIC\_NUMBER
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I'd say that this is probably the most pervasive way of doing
template tags. The django source uses it in some places, and a lot
of people do it this way. It basically involves breaking the
incoming string into an array, and checking to see what is in each
index of the array. For example, if your tag syntax looked like
``do_something for app.model [as contextvar]``, which has a default
context variable if you don't pass one. The code to this approach
would look like:

::

    def parse_stuff(parser, token):
        bits = token.contents.split()
        if len(bits) == 5 and bits[1] == 'for' and bits[3] == 'as':
            return FooNode(bits[1], bits[3])
        if len(bits) == 3 and bits[1] == 'for':
            return FooNode(bits[1])
        else:
            raise template.TemplateSyntaxError, "%s: Fail" % bits[0]

As you can see, this quickly gets cumbersome with larger tags, and
makes tags annoying static. It's a pain to have to remember the
order of arguments and other things that don't need to matter.

Regular Expressions
~~~~~~~~~~~~~~~~~~~

Another way that I have seen these tackles is with the use of
regluar expressions. They look a little something like this:

::

    def parse_stuff(parser, token):
        import re
        default = re.compile('tagname for (\w+) as (\w+)')
        no_as = re.compile('tagname for (\w+)')
        if default.match(token):
            return FooNode(group(0), group(1))
        elif no_as.match(token):
            return FooNode(group(0))
        else:
            raise template.TemplateSyntaxError, "%s: Fail" % token[0]

Again, this has the same problems as the above approach. It's a
little bit more annoying because of python's regular expression
support lacking, but it gets the job done. I don't want to be
writing a regex for every possible pattern though.

What I propose
~~~~~~~~~~~~~~

I say that if we standardize the variables used for certain things
in templates, then we can make some really simple parsing utils
that will do our job for us. There are already a certain amount of
best practice with template tags for what to use as command
variables, and below I will list out the commonly used ones.


-  as (Context Var): This is used to set a variable in the context
   of the page
-  for (object): This is used to designate an object for an action
   to be taken on.
-  limit (num): This is used to limit a result to a certain number
   of results.
-  exclude (object): The same as for, but is used to exclude things
   of that type.

This is just a basic set of common variables that are 'special'. I
think that it makes sense to start parsing template tag input
strings for these strings. I wrote a little snippet to do this for
you.

::

    def parse_ttag(string):
        #This could be token.contents.split()
        bits = string.split()
        tags = {}
        possible_tags = ['as', 'for', 'limit', 'exclude']
        for index, bit in enumerate(bits):
            if bit.strip() in possible_tags:
                tags[bit.strip()] = bits[index+1]
        return tags

And when I run it on a simple example, you see the value in this
approach:

::

    >>> parse_ttag('test as word for for.bit limit 23')
    {'as': 'word', 'limit': '23', 'for': 'for.bit'}

This approach is nice, because it doesn't matter what order the
arguments are in. It simply returns a list of the keywords that you
care about, and what their value was. I think that this makes it a
lot easier to make a template tag, at the moment. This could also
be extended to support multiple uses of each keyword, by using a
list instead of a string as the value in the dictionary.

This is a simple little solution, and there is plenty of room for
improvement. I think that there are some other ways to do much
neater things with this, but it has worked. We could even go out
and write some of the most common use cases for template tags into
a function that simply parses them and returns a node.

::

    def parse_ttag(string):
        return context_for_object(token, FooNode)

Where this would call FooNode with the correct arguments. It would
know that the correct syntax was [WhateverTag for Whatever as
Context]. This would then just pass into a FooNode(Whatever,
Context), where it could then do the actual action that was taking
place. The template tag parsing doesn't need to care what the
objects are, it is just parsing strings, and making sure that
certain values are passed into the correct argument.

Here is a very basic implementation, that does nothing, but shows
the ideas behind what I'm talking about.

::

    class FooNode():
        def __init__(self, por, _as='default'):
            print "Making Node: for:%s, as:%s" % (por, _as)
    
    def parse_ttag(string):
        bits = string.split()
        tags = {}
        possible_tags = ['as', 'for', 'limit', 'exclude']
        for index, bit in enumerate(bits):
            if bit.strip() in possible_tags:
                tags[bit.strip()] = bits[index+1]
        return tags
    
    def some_random_tag(parser, token):
        return context_for_object(token, FooNode)
    
    def context_for_object(token, Node):
        """This is a function that returns a Node.
        It takes a string from a template tag in the format
        TagName for [object] as [context variable]
        """
        tags = parse_ttag(token)
        if len(tags) == 2:
            return Node(tags['for'], tags['as'])
        elif len(tags) == 1:
            return Node(tags['for'])
        else:
            #raise template.TemplateSyntaxError, "%s: Fail" % bits[]
            print "ERROR"
    
    >>> some_random_tag('fake','test as word for for.bit')
    Making Node: for:for.bit, as:word
    <__main__.FooNode instance at 0x23aaa8>
    >>> some_random_tag('fake_parser', 'fail whale')
    ERROR
    None

Notice how easy and logical the implementation is using the
parse\_ttags function, I think that the tags['for'] abstraction is
a really good one. It takes the template tag string and parses out
what you really care about. Now if we just write these for the most
common cases of Template tags, we could make our lives a lot
easier. I also assume that this can probably be done with this
template parser in Django, but I've never really seen it used, or
used it myself. Hopefully this is already done for us, and just not
well documented.


