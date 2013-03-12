:Date: 2009-01-15 19:01:28
Django now has fast tests
=========================

As of
`Changeset 9756 <http://code.djangoproject.com/changeset/9756>`_,
Django's test suite is A HELL OF A LOT FASTER. This was one of the
`1.1 Features <http://code.djangoproject.com/wiki/Version1.1Features>`_
and probably the one I was looking forward to the most. Django Unit
Tests now run inside of a transaction.

Karen Tracey did most of the work on this finishing one, and we owe
her a huge thanks, and a lot of our time :). Her commit message
sums up the work better than I can.

::

    Fixed #8138 -- Changed django.test.TestCase to rollback tests (when
    the database supports it) instead of flushing and reloading the database.
    This can substantially reduce the time it takes to run large test suites.
    
    This change may be slightly backwards incompatible,
    if existing tests need to test transactional behavior,
    or if they rely on invalid assumptions or a specific test case ordering.
    For the first case, django.test.TransactionTestCase should be used.
    TransactionTestCase is also a quick fix to get around test case errors
    revealed by the new rollback approach, but a better long-term fix
    is to correct the test case. See the testing doc for full details. 
    
    Many thanks to:
    * Marc Remolt for the initial proposal and implementation.
    * Luke Plant for initial testing and improving the implementation.
    * Ramiro Morales for feedback and help with tracking down a
      mysterious PostgreSQL issue.
    * Eric Holscher for feedback regarding the effect of the
      change on the Ellington testsuite.
    * Russell Keith-Magee for guidance and feedback from beginning to end. 

The amazing thing is that you don't have to do anything in order to
get the benefit from this change. People's test suites will now be
running about 8-12x (ed: was 40x, but that was a bit much) faster
than before. Depending on whether you have a larger portion of
doctests or unit tests, you will get different speedups. The
Database backend you are using is also import; MySQL/MyISAM doesn't
support transactions, and tests running in SQLite were already much
faster, so they don't get as much of a percentage gain.

Ellington's test suite, which was taking around 1.5-2 hours to run
on Postgres, has been reduced to 10 minutes. I tested changing some
of our more expensive doctests to unit tests (and thus getting
transaction support), and it looks like we can get our suite to run
in 3-4 MINUTES.

Prior to this change, before every doctest or unittest test case
was run, Django would do an entire flush and syncdb of the
database! This was time consuming, and not totally necessary. Now
all unit tests are wrapped in a transaction. This is a much faster
operation on the DB, and that is where the speed gains come from.

People using doc tests aren't having their tests run inside a
transaction, but that is the same behavior as before the change. If
you are curious more about the implementation of this patch, there
is a huge discussion on
`ticket 8138 <http://code.djangoproject.com/ticket/8138>`_ that
shows some of the interesting things encountered during this
process.

This patch applies cleanly to Django 1.0 as far as I know, so if
you are running tests on any kind of large code base I would
recommend either applying the patch in #8138, or upgrading to
trunk. This also means that you have one less excuse for not
writing or running tests ;)


