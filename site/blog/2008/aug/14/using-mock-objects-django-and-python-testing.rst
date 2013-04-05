:Date: 2008-08-14 10:20:51

Using Mock objects in Django for testing the current date
=========================================================

Today I ran into a fun problem when writing template tags at work.
(I'll write another post later on the fun-ness that is testing of
template tags :) In ellington we have some templatetags that test
for the current time of day. ifmorning, ifnight and so on. These
template tags are using datetime.datetime.now() to check to see if
the time is within a certain range. This is impossible to test in a
standard way without doing some hacking on the datetime.datetime
object.

The solution is actually pretty easy. Let me warn, although this is
the correct solution in this case,
**monkeypatching is generally BAD**. You don't want to just be
playing around with python or django's stdlib and breaking things
for other people. With that warning, let me show you how I went
about doing this.

This code is called in this fashion:

::

    import unittest
    class LoadDateutil(TemplateTestCase):
        def test_load(self):
            olddatetime = datetime.datetime
            datetime.datetime = make_datetime(5)
            self.assertEqual(self.render(u'{% load dateutil %}{% ifnight %}Hi{% endifnight %}'), u'')
            datetime.datetime = olddatetime

Now let me explain what all is going on here. TemplateTestCase is
an internal base class for doing templatetag tests. This will
probably be released (by me or
`Matt Croydon <http://postneo.com>`_) sometime soonish.

The first thing you want to make sure you do is leave everything
how you found it. So before we go about editing the
``datetime.datetime`` object, we save it into ``olddatetime``, and
once we are done with the test, we return ``datetime.datetime``
back to its original value. In the middle of the test, we are
calling ``datetime.datetime = make_datetime(5)`` which is returning
a datetime.datetime object that has it's now() method overwritten.
The argument to ``make_datetime`` is the hour of the day you want
to represent.

Let's take a look at how make\_datetime is working:

::

    import datetime
    def make_datetime(hour):
        class MockDatetime(datetime.datetime):
            @classmethod
            def now(cls):
                return datetime.datetime(2007, 1, 1, hour)
        return MockDatetime

This code is creating the ``MockDatetime`` class, and then defining
the now() method. The ``@classmethod`` decorator must be used
because the now() method is a class method. Then the now() method
simply returns a ``datetime.datetime`` object with the correct hour
in it.

This is pretty simple, and is the correct and best way to do
testing of this nature. I hope this is helpful to someone out there
:) Also note that these methods are not django specific, and can be
used in anything with python.

As a caveat, make sure that the templatetag code you are running
this test against is importing the datetime module, and not
datetime.datetime, because in that instance this code will not work
(because the code we're overwriting will be re-imported in the
templatetag (as far as I can tell))

Thanks to `Malcolm <http://www.pointy-stick.com/blog/>`_ for
helping me with this.


