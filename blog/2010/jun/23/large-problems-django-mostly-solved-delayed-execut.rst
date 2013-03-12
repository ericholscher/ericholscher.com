:Date: 2010-06-23 15:44:56
Large Problems in Django, Mostly Solved: Delayed Execution
==========================================================

[This is part of the
`Large Problems in Django Series <http://ericholscher.com/tag/largeproblems/>`_,
see previous entries about:
`Documentation <http://ericholscher.com/blog/2010/feb/5/large-problems-django-mostly-solved-documentation/>`_,
`APIs <http://ericholscher.com/blog/2009/nov/11/large-problems-django-mostly-solved-rest-api/>`_,
`Search <http://ericholscher.com/blog/2009/nov/2/large-problems-django-mostly-solved/>`_,
and
`Database Migrations <http://ericholscher.com/blog/2009/nov/6/large-problems-database-migrations/>`_]

A lot of Django applications have tasks that they need to perform
out of process. When you are executing a web request, if you try to
do all the work that you need before returning to the user, your
site will be increasingly slow. The answer to this problem is to
fire off a request to do those tasks, while returning to the user
in a reasonable amount of time.
`Celery <http://celeryproject.org/>`_ refers to itself as a
"Distributed Task Queue", and is the current best of breed in the
Python realm.

Why Use Celery
--------------

Easy
^^^^

For the most basic functionality, all you need to do is:


-  move your function into your tasks.py
-  wrap it with a
   `@task <http://celeryproject.org/docs/userguide/tasks.html#module-celery.task.base>`_
   decorator
-  call it with task.delay(\*args) just like before.

Now, your task is magically running out of process and you can get
on with whatever it is your code is meant to be doing.

Network Effects
^^^^^^^^^^^^^^^

This is currently the best and most complete application in Python
that does these things. A lot of people are using it, which means
that features will be added consistently. There is also pretty good
support in the #celery IRC channel, which usually has around 40-50
people in it. It is being actively developed and all other things
being equal, using a tool with a community around it is much
better.

Concurrency
^^^^^^^^^^^

The celeryd daemon supports multiprocessing, which allows it to run
multiple tasks at once. You can get "cheap concurrency" this way,
by loading it up with tasks and having it execute them. You can
also run multiple instances of celeryd across multiple servers, you
can get your tasks that run concurrently across servers. Running
multiple instances is also a good way of insuring redundancy in
case one of your daemons goes down.

Monitoring
^^^^^^^^^^

One of the scary things about having remote execution of tasks is
that if your daemon goes away, your site will appear not to
function. Celery has an accompanying project called
`celerymon <http://github.com/ask/celerymon>`_ which provides
monitoring services for Celery.

No more hacky cron jobs
^^^^^^^^^^^^^^^^^^^^^^^

I don't know about you, but most of the time when I want something
to be run in the background, cron is my go to choice. I'm ashamed
to admit that I've written code that is meant to run in a cron job
every minute checking for something to have happened. However,
celery has most of the features that cron has, while giving you
real support for deamonizing and delaying tasks. Being able to
retry tasks is a great benefit is has over cron, so when something
fails, you can run it again later.

Great documentation
^^^^^^^^^^^^^^^^^^^

The `celery docs <http://celeryproject.org/docs/index.html>`_ are
great, including everything from basic setup and example
instructions to howtos. We put it into production at work, and the
`docs for using redis <http://celeryproject.org/docs/tutorials/otherqueues.html>`_
as a "ghetto queue" were great and worked the first try.

Lots more
^^^^^^^^^

I highly recommend that you check out celery. Unless you are doing
a small website like a blog, you more than likely have a use case
for Delayed execution of tasks.
**It's one of those things that once you have celery set up and running, you find more and more ways to use it over time. It is one of the best ways to increase the responsiveness of your website.**
I've found that it can also clean up some of the other
infrastructure you might have in place to do similar things.


