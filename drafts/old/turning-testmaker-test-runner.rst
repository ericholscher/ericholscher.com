.. post:: 2008-10-25 23:17:28

Turning testmaker into a test runner.
=====================================

I have been writing a couple of django testing automation tools
lately, and I think that there may be a really neat abstraction
that can be made out of them. Currently I am simply running tests
and creating unit tests out of them. Presumably these can then be
taken and turned back into the data that they were originated from.
But this begs the question, why not just store the initial data,
and then have a separate process that generates the tests from that
data. This way the tests could be re-generated later with new data.
But it also gives you more data! Data is good, and can be used for
other things.

The idea is basically to have a log of activity on your site, but
have more data about it.


