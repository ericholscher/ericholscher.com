:Date: 2009-11-18 19:46:22

Finding Missing Indexes That Django Wants (Postgres)
====================================================

On Monday at work, our sites started to slow to a crawl. We looked
to diagnose the problem, and found that the database server had a
load of 10, and was struggling to keep up with the morning rush of
traffic. After EXPLAINing the slow queries from the slow query log,
we noticed that a lot of sequence scans were happening. This
shouldn't be happening because these queries should have indexes on
them. We realized somewhere in the porting process that we had lost
a bunch of indexes.

Check for missing indexes
^^^^^^^^^^^^^^^^^^^^^^^^^

So I went ahead and wrote a
`little script <http://github.com/ericholscher/django-debug-utils/blob/master/debug_utils/management/management/check_indexes.py>`_
that basically diffs the current indexes and the ones proposed by
Django. This allows you to see the indexes that you are missing.
This will only work on Postgres, however if you parse the indexes
for your DB it should work there.

You can simply copy that file into your management commands. Then
you can run ``django-admin.py check_indexes``, and it will output a
tuple of table and name. If you pass in the ``--show`` option, it
will actually output the CREATE statements that create the indexes.
This allows you to create the indexes in your DB by piping it in.

::

    django-admin.py check_indexes --show | django-admin.py dbshell

You want LIKE, fast queries?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In our search, `Frank <http://revsys.com>`_ and
`James <http://b-list.org>`_ also discovered that when you have a
UTF8 database (which you should), Postgres needs a special index to
do LIKE queries against text fields. James filed a
`Django bug <http://code.djangoproject.com/ticket/12234>`_ with
details. However, if you are running a postgres database, it may be
worthwhile to look for places that you might be making similar
queries. For more information check out the
`postgres docs <http://www.postgresql.org/docs/current/static/indexes-opclass.html>`_

We'll do it LIVE
^^^^^^^^^^^^^^^^

One other postgres index optimization that James and Frank
discovered was that Postgres gives you the ability to index on
state of a field. So if you have tables that have any kind of
status that is often queried, you can set a specific index on
that.

::

    create index "published_story" on "news_story" ("status") where "status" = 1;

I hope that my little script and these tips allow you to make your
Postgres Database purr. I only just got schooled in Postgres
recently. Frank has been doing this a long time and has some
`awesome postgres performance tips <http://www.revsys.com/writings/postgresql-performance.html>`_.
I recommend reading through that if you really want to make your
database run well.

**Note**: It has been pointed out that South uses a different
naming scheme, so if you have indexes created with south, this may
not work quite right.


