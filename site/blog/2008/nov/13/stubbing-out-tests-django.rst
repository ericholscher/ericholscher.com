.. post:: 2008-11-13 16:43:02

Encouraging Testing in Django
=============================

I was having a conversation with
`Jacob <http://www.jacobian.org/>`_ tonight about testing in
Django. He has shot down
`testmaker <http://code.google.com/p/django-testmaker/>`_ for being
too specific for Django core, which I almost agree with, given my
grandiose plans for it before the month is out. I'm quite okay with
it staying a third party app for a little while longer.

However, that got us on the topic of testing, and I think it's
interesting enough to post here to get some feedback and to tell
people what's up. First we talked about trying to stub out some
tests for people in the startapp command in Django. Like Rails
does, except there is a really hard question about what to provide
in that file. Should we provide a simple test that passes and makes
people feel good about testing? Do we be evil and provide a test
that fails, with ``assert False, 'Write some tests yo!'``?

So the idea then progressed into perhaps having a command that can
be called later in the process to stub out your tests files with
real data. Perhaps stubbing a test for each view in your URLconf
and each method in your Models or something like that.

We also talked about the possibility of adding a fifth part to the
Django Intro Tutorial about testing. I think that this is a really
great idea, and would help further the testing culture inside of
the Django community. I volunteered to write the first draft of
that document, so expect that to be posted to this blog sometime
next week.

So I'm just kind of curious what people think is a good way to get
testing integrated into the Django community better. I am trying to
write some tools that will help people write tests, which would
help them have tests :). But I think that there is a lot more that
can be done to get people thinking about testing their
applications.

Should we be encouraging people to be testing from when they start
a new application in Django? If so, what should we put in the
tests.py file when they create an application? Should we just stub
out an empty tests.py file to remind them that they should be
writing tests? Should we be pushing best practices from the
beginning in that form, or giving people a builtin option to
perhaps then stub it out later?

I think that the Django community is lacking in the testing realm
these days, and I'm curious what we can be doing to get more people
**excited** about testing. It's a great tool, and something that
everyone should be doing. So I'd love to hear feedback or ideas
about what people think can and should be done with regards to
testing.


