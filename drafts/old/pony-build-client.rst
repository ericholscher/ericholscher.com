:Date: 2010-01-01 14:08:06

Pony Build
==========

Pony Build started off as an interestingly simple approach to
continuous integration. You can read more over at
`Titus's post <http://lists.idyll.org/pipermail/testing-in-python/2009-March/001277.html>`_.
There have been people talking about how this is an example of NIH,
and what not. I do agree to some extent, however that hasn't
stopped me from participating.

However, today I want to talk about a different part about
pony-build which I think is important and interesting. That is the
actual test description harness that the pony-build client
supports. This allows you to write executable code that shows how
to run your tests, leaving your users able to run the tests by
simply executing that script. The python community has a couple of
different ways that tests can be run currently, and there isn't
really a good way to let people know which to use (other than
documentation).


