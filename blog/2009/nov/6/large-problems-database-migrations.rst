:Date: 2009-11-06 19:03:11

Large Problems in Django, Mostly Solved: Database Migrations
============================================================

Continuing in the series of big problems that are mostly solved, we
have database migrations. A couple days ago I talked about
`Search <http://ericholscher.com/blog/2009/nov/2/large-problems-django-mostly-solved/>`_.

Database Migrations
-------------------

Database Migrations are an interesting piece of the Django
community. Rails has the functionality built in, but Django
currently relies on third party apps for this functionality. One of
the core philosophies about not including apps in the Django core
is that ideas percolate better in the fast release environment
outside of the core. When something goes into core, it is
automatically seen as blessed, and will certainly become the
defacto answer to a problem. Leaving things outside allows multiple
different implementations to develop (as they did), and for one to
become the standard (which it has). Along the way it has picked up
ideas from others, and now provides a good answer to migrations.

South
~~~~~

`South <http://south.aeracode.org/>`_ has emerged as the obvious
choice for database migrations in the Django community. We use it
in production at work at the Journal World, and it has served us
well.

I have talked about south in the past, using it to
`migrate test fixtures <http://ericholscher.com/blog/2009/jun/11/migrating-test-fixtures-using-south/>`_.
This serves as a basic tutorial and introduction into south as
well.

Main Features
~~~~~~~~~~~~~

Automatic Migrations
^^^^^^^^^^^^^^^^^^^^

Most of the migrations that I write, I
`don't write <http://south.aeracode.org/wiki/About#AutomaticMigrationCreation>`_
a single line of code. South has the ability to how you model
looked at the end of your last migration, and then extrapolate what
has changed (in most simple and modestly complex cases). There are
obviously times that it falls down, but for simple addition,
deletion, and modification of fields it has worked almost
flawlessly for me. With a simple command, it will do all your work
for you.

::

    django-admin.py migrate app_name --auto

It has problems with Generic Foreign Keys and a couple of other
more complex models. However, I would say that it absolutely nails
the 80% case that most migrations fall in to.

Fake ORM ("ORM Freezing")
^^^^^^^^^^^^^^^^^^^^^^^^^

This is a feature that South has grown from it's
`Migratory <http://bitbucket.org/DeadWisdom/migratory/wiki/Home>`_
roots. I think it is one of the best conceptual features for
migrations. It allows you to use a Fake ORM (the real ORM, applied
to the aforementioned fake models), to do data transformation in
your migrations. This example from the
`tutorial <http://south.aeracode.org/wiki/Tutorial3>`_ shows the
value:

::

    def forwards(self, orm):
        for adopter in orm.Adopter.objects.all():
            try:
                adopter.first_name, adopter.last_name = adopter.name.split(" ", 1)
            except ValueError:
                adopter.first_name, adopter.last_name = adopter.name, ""
            adopter.save()

Database Independent
^^^^^^^^^^^^^^^^^^^^

This sounds like an obvious feature, but a lot of the approaches
for migrations were only viable on one database. The support for
SQLite is still lacking, but that is because of fundamental
limitations in the way SQLite works. Most people using SQLite can
just wipe their database and start over, if not, you should
probably be using another database.

It knows when you've been naughty
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

South
`keeps track <http://south.aeracode.org/wiki/About#MissingMigrations>`_
of all the migrations that you have run, and it intelligently
informs you if you have missed a migration. It also supports
inter-dependencies on migrations. This allows you to be safe in
your knowledge that your migrations will be run properly, and that
state is maintained. This sounds like a hand-wavey feature, but
when you're migrating your data, knowing when things aren't quite
right is a nice feeling!

South also keeps track of the migrations that are on disk, and
won't let you migrate if they are different than previous runs.
This makes sure that you aren't running against a different version
of the code; allowing you to be sure that the migrations being run
are correct.

Conclusion
^^^^^^^^^^

Overall, south solves a lot of the problems about migrations in a
good way. There have been other solutions to the migration problem,
and I think that south has taken most of the good ideas and
combined them in one place. It has some drawbacks still, but
overall it is the best of breed in Django for Database Migrations.
If you are looking for a migration tool for Django, this is your
best bet.

**There aren't a lot of flashy features in the migration realm I feel. Mostly you just want something that keeps your data safe, and allows you to write migrations as simply and foolproof as possible.**
South lets you do that, so I consider it a win.

I view migrations somewhere along the lines of testing. It is one
of those things that once you have, you don't see how you ever
lived without it. Being able to immediately see the state of your
database, what migrations haven't been run, and what all needs to
happen is incredibly useful. Having a safety net of repeatable
migrations also ensures that your databases are all the same,
across many installations and machines. The value of database
migrations are many, and South brings them to you in a nice
package.


