.. post:: 2008-11-02 21:01:00

Python gems of my own
=====================

**Note**: I'm launching a redesign today to address the styling
issues. Please bear with me

A great example of how this month of blog posting is spawning great
content on the interwebs.
`Other Eric <http://eflorenzano.com/blog/post/gems-python/>`_
posted a gems of python post, in which he pointed out some of the
neat functions that he uses. The python stdlib has a ridiculous
amount of really really useful things inside of it, and it's hard
to know what even exists there. I love posts like that, that point
to some neat little utility functions and tricks that make things
really nice. In that spirit, here is my own list of Python Gems

1. urlparse
~~~~~~~~~~~

`urlparse <http://docs.python.org/library/urlparse.html>`_ is a
really handy piece of functionality if you are trying to deal with
URLs on the web. As per usual, an example shows it best.

::

    >>> from urlparse import urlparse 
    >>> urlparse('http://www.ericholscher.com/example/dir/') 
    ('http', 'www.ericholscher.com', '/example/dir/', '', '', '') 
    >>> urlparse('http://www.ericholscher.com/example/dir?query=r0x0r#awesome-part')  
    ('http', 'www.ericholscher.com', '/example/dir', '', 'query=r0x0r', 'awesome-part') 
    >>> parsed = urlparse('http://www.ericholscher.com/example/dir?query=r0x0r#awesome-part') 
    >>> parsed.path 
    '/example/dir' 
    >>> parsed.scheme 
    'http' 

I was looking for a good way to check for relative versus absolute
urls, and this made it really easy. Also incredibly easy to check
for the type of link (http, https, mailto, ftp). You can access the
data via the named patterns or as a list.

2. inspect
~~~~~~~~~~

The entire `inspect <http://docs.python.org/library/inspect.html>`_
module is incredibly useful. I was looking through the Django
source, which is where I stumbled upon it. It is used inside the
`simple tag <http://code.djangoproject.com/browser/django/trunk/django/template/__init__.py#L879>`_
code for Django templates. ``getargspec`` is really handy, but
there is a lot of really interesting stuff in that file. I don't
have anything that I can show quite yet, but I'm going to use the
inspect stuff in an upcoming snippet. Here is a simple use case.

::

    >>> import inspect
    >>> def test(a, b=True, *args, **kwargs):
    ...     pass
    ... 
    >>> inspect.getargspec(test)
    (['a', 'b'], 'args', 'kwargs', (True,))
    >>> import django
    >>> inspect.getmodule(test)
    <module '__main__' (built-in)>
    >>> inspect.getfile(django)
    '/Users/ericholscher/Sites/EH/django/__init__.pyc'
    >>> inspect.getsourcefile(django)
    '/Users/ericholscher/Sites/EH/django/__init__.py'
    >>> inspect.ismodule(django)
    True
    >>> inspect.isbuiltin(django)
    False

As you can see, there is lots of really nice stuff in there.

3. Generator expressions
~~~~~~~~~~~~~~~~~~~~~~~~

These are very similar to list comprehensions, except they are
evaluated lazily. They are described "as a high performance, memory
efficient generalization of list comprehensions and generators".
The only difference in syntax is that you use a () instead of a []
around the comprehension.

::

    >>> iter = (x for x in range(1,5))
    >>> reg = [x for x in range(1,10)]
    >>> iter
    <generator object at 0x29e3c8>
    >>> reg
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> iter.next()
    1
    >>> iter.next()
    2
    >>> for x in iter:
    ...     print x
    ... 
    3
    4

The main use case that I have seen for this is if your list
comprehension is going to take a lot of memory. If you aren't sure
you're going to need all of it, or don't want to store it all in
memory, then you can use the iterator. It will then get generated
on demand when you need it. If you want to create your own
generator, you simply use the yield keyword instead of return.
Python makes this really easy!

4. 128
~~~~~~

**Note**: Some commenters pointed out that this is also re.DEBUG.
`James Tauber <http://jtauber.com/blog/2008/11/03/pythons_re_debug_flag/>`_
has a nice post explaining it more in depth.

I don't know if this is documented in the Official python
documentation, but it is an incredibly useful regex debugging tool.
You can pass in 128 to your re.compile() function and get the parse
tree back out! Really neat, check it out:

::

    >>> import re
    >>> re.compile('(\w+): (<.*?>)', 128)
    subpattern 1
      max_repeat 1 65535
        in
          category category_word
    literal 58
    literal 32
    subpattern 2
      literal 60
      min_repeat 0 65535
        any None
      literal 62
    <_sre.SRE_Pattern object at 0x29f278>
    >>> re.compile('Ahoy Globe', 128)
    literal 65
    literal 104
    literal 111
    literal 121
    literal 32
    literal 71
    literal 108
    literal 111
    literal 98
    literal 101
    <_sre.SRE_Pattern object at 0x267920>

Isn't that neat?

5. enumerate
~~~~~~~~~~~~

`enumerate <http://docs.python.org/library/functions.html#enumerate>`_
is very similar to the zip function that Eric talked about in his
post. It is useful in those cases where you want to know the index
of something in a list, but don't want to do i += 1.

::

    >>> buddy_list = ['frank', 'liza', 'bob']
    >>> for love, person in enumerate(buddy_list):
    ...     if love > 1:
    ...             print "%s is not loved" % person
    ...     else:
    ...             print "I love %s" % person
    ... 
    I love frank
    I love liza
    bob is not loved
    >>> for place, person in enumerate(buddy_list):
    ...     print place, person
    ... 
    0 frank
    1 liza
    2 bob

That's it for today. As Eric said (not talking in the third
person), there are lots of little awesome hidden corners of Python.
I'd love to hear about the things that you find really useful.


