:Date: 2010-11-04 16:00:00

Running Hudson matrix builds on multiple machines
=================================================

When I was setting up the Django Hudson instance, I ran into a
problem that seems like it should be pretty easy to solve. However,
I couldn't figure out a way. So at this point it's looking like
we're going to have to use buildbot to build out what we want
instead of Hudson. Wondering if I missed something obvious, or if
this is a missing feature.

Our setup
---------

We have our builds segmented currently by Django version and
database. So to get something up and going, we have a Django trunk
and 1.2.X build going against sqlite. We use a matrix build to run
this against python 2.4-2.6, which means 3 builds in total for each
Django version.

However,
**I can't find a way to make the matrix build choose the slave to run on based on what version of python it supports**.
I want to be able to randomly add slaves to the Hudson
configuration, and have them pick up builds based off of their
capabilities.

The problem
-----------

Hudson supports the idea of tagging, so we came up with a
`tagging scheme <http://code.djangoproject.com/wiki/BuildFarm#Desiredconfigs>`_
for the slaves. So it seems that we should be able to tell a test
to run on any slave tagged with the versions of python we want.
Hudson also supports this, but it runs all the tests across all the
different slaves each time. I need it to
**have a pool of workers capable of running a set of tests, but run each test on only one of the members of the pool**.

I was wondering if we're doing it wrong, or if other people know
the correct way to run tests across a set of slaves, based on the
capabilities of the slave? This seems like a pretty basic
requirement for people running any kind of sizable Hudson
configuration.


