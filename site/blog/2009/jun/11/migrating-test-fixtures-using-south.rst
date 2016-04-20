.. post:: 2009-06-11 20:16:13

Migrating Django Test Fixtures Using South
==========================================

The Problem
-----------

Migrating test fixtures is one of the biggest pains of testing. If
you create your tests too early, then change your schema, you have
to go back and touch all your old test fixtures. This discourages
people from writing tests until their app is relatively 'stable'.
As we all know, this may never happen :) This solves half of the
problem, the part where you have to manually change a bunch of
fixtures to reflect changes in your schema or data.

Possible Solution
-----------------

During the questions in my EuroDjangoCon talk, someone asked a
question about this. I didn't have a good answer, but someone from
the crowd raised their hand and suggested using
`South <http://south.aeracode.org/>`_. Once your project has data
migrations for it's real models (like any production site should),
**it should be relatively easy to then load up your test fixtures, migrate your database, and dump them back out**.

I will be writing out a pretty basic tutorial on south, alongside
of the example of how to migrate your test data using South. I
think it's pretty fantastic. I hope that if you aren't already
using south, this tutorial will show it's simplicity and power, and
if you are, I hope to show you another way to use it. If you
already understand south and have data migrations, you can skim the
Example section and just focus on the later part.

I am using my
`Django Test Utils <http://github.com/ericholscher/django-test-utils/tree/d9d718025d6aa128b4a13dab91e3013a2b6a3dd0/test_project>`_'s
test\_project at a certain revision for this demo, so you can look
there and follow along if you want to see the actual files used.
Look at the next commit to see the outcome of the project :)

Example
-------

I went ahead and made a simple little example application to test
this on. It will be the common migration scenario of adding a slug
to a model. We will be using the Polls app that everyone knows and
loves from the Django Tutorial.

I don't currently have south installed at this point in test utils,
so if you're following along, you just have to download south and
add it to the installed apps before you start.

Basic Setup
^^^^^^^^^^^

So you have the basic polls models.

::

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')
    
    class Choice(models.Model):
        poll = models.ForeignKey(Poll)
        choice = models.CharField(max_length=200)
        votes = models.IntegerField()

We realize that we don't have a way to show these well on the site,
because they don't have a slug. So we want to add a slug to the
Poll model. First off you need to have the initial migration for
your app, so that we can migrate it. We are going to use south, so
we need to create our initial migration.

::

    $ ./manage.py startmigration polls --initial 
    Creating migrations directory at '/Users/ericholscher/lib/django-test-utils/test_project/polls/migrations'...
    Creating __init__.py in '/Users/ericholscher/lib/django-test-utils/test_project/polls/migrations'...
     + Added model 'polls.Poll'
     + Added model 'polls.Choice'
    Created 0001_initial.py.

Adding your fields
^^^^^^^^^^^^^^^^^^

As you can see, south knows how to add a migrations directory to
your app and fill it up with the correct migration name. Now lets
go ahead and edit our model.

::

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')
        slug = models.SlugField(null=True)

As you can see, we added a slug field. It has to be null=True
because we will be creating a lot of them, and they must be able to
be null before we can add the data to them. Now lets go ahead and
create two migrations. We want to add one that creates the field,
and then we want to create one that fills out the slug from the
question field.

::

    $ ./manage.py startmigration polls add_slug --auto
     + Added field 'polls.poll.slug'
    Created 0002_add_slug.py.

Writing your Data Migration
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This creates the migration that we want that allows us to add the
field. Now we go ahead and run ``startmigration`` again, just
passing the app name. This creates a stub migration for us, with
the model serialized on the bottom, which allows us to just write
the code we care about.

::

    $ ./manage.py startmigration polls populate_slug_data
    Created 0003_populate_slug_data.py.

Note that it is a good practice to separate your migrations that
effect your table structure and things that actually migrate data.
Now we go in to the migration and add in the code that migrates the
data. It will end up looking something along these lines.

::

    from south.db import db
    from django.db import models
    from polls.models import *
    from django.template.defaultfilters import slugify
    
    class Migration:
    
        def forwards(self, orm):
            for poll in orm.Poll.objects.all():
                poll.slug = slugify(poll.question)
                poll.save()
    
        def backwards(self, orm):
            "Write your backwards migration here"
            for poll in orm.Poll.objects.all():
                poll.slug = ""
                poll.save()
    
    ... Chopped for clarity ...

As you can see, the migration is really simple! This uses a fake
Django ORM (which is just the real one, loaded a different way.)
Now you can go ahead and test out your fancy new migrations.

Running the migrations on your test data.
-----------------------------------------

Now as you see, you have these fancy migrations that actually
haven't touched your database yet. I'm going to walk through the
entire process of creating your database from the ``syncdb`` stage
to the outputting of your shiny new test fixtures.

Setting up your test database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

So the whole point of this exercise is to be able to migrate your
test fixtures the same way you do your real database. This means
that we simply load up a new version of our database with our test
data, run our migrations, and serialize it back out, ready for our
tests.

Go ahead and run ``syncdb`` on your project. This will do all the
normal things you're used to, except that at the bottom of the
output, you'll see a message about things not being synced because
of south:

::

    Synced:
     > django.contrib.auth
    ....
    
    Not synced (use migrations):
     - polls
    (use ./manage.py migrate to migrate these)

Now we need to go ahead and get the polls data in our database at
the point where our fixtures exist. This means that we only want
our initial data to be loaded. So we go ahead and tell south to
migrate to our first migration.

::

    $ ./manage.py migrate polls 0001
     - Soft matched migration 0001 to 0001_initial.
    Running migrations for polls:
     - Migrating forwards to 0001_initial.
     > polls: 0001_initial
       = CREATE TABLE "polls_poll" ("id" integer NOT NULL PRIMARY KEY, "question" varchar(200) NOT NULL, "pub_date" datetime NOT NULL); []
       = CREATE TABLE "polls_choice" ("id" integer NOT NULL PRIMARY KEY, "poll_id" integer NOT NULL, "choice" varchar(200) NOT NULL, "votes" integer NOT NULL); []
       = CREATE INDEX "polls_choice_poll_id" ON "polls_choice" ("poll_id"); []
     - Sending post_syncdb signal for polls: ['Poll']
     - Sending post_syncdb signal for polls: ['Choice']

Migrating your test data
^^^^^^^^^^^^^^^^^^^^^^^^

As you can see, this created out database table without the slug
field. This is good, because our fixture data doesn't include the
slug field. This is where things get a bit annoying. The loaddata
command uses the models that are on disk to check if the data loads
correctly. So you need to check out your code at the revision
before the migrations were applied (in our case, we can simply
comment out the slug line). Then you are able to go ahead and load
your test data.

::

    $ ./manage.py loaddata polls_testmaker
    Installing json fixture 'polls_testmaker' from '/Users/ericholscher/lib/django-test-utils/test_project/polls/fixtures'.
    Installed 8 object(s) from 1 fixture(s)

Then you can put the slug back in (or check out the current version
of your code). Now you have your data in your database in the old
un-migrated form. Let's go ahead and migrate out test fixtures :)

::

    ./manage.py migrate polls
    Running migrations for polls:
     - Migrating forwards to 0003_populate_slug_data.
     > polls: 0002_add_slug
       = ALTER TABLE "polls_poll" ADD COLUMN "slug" varchar(50) NULL; []
     > polls: 0003_populate_slug_data
     - Loading initial data for polls.

Now lets see if that worked. Let's go ahead and run dumpdata and
see what all you have.

::

    ./manage.py dumpdata polls --indent=4
    [
        {
            "pk": 1, 
            "model": "polls.poll", 
            "fields": {
                "pub_date": "2007-04-01 00:00:00", 
                "question": "What's up?", 
                "slug": "whats-up"
            }
        }, 
    ... snip rest of data ...

**You now have your migrated data fixture!** Hopefully everything
worked for you, and that this works for larger examples other than
this trivial example.

Conclusion
----------

The little bit at the end where you have to revert back to the old
version of your code to use loaddata is a bit of a hack. With a bit
of tinkering, you should be able to use south's serialized
representation of the model instead of the models on disk in order
to load the data. Doing this will make this whole process more
seamless.

If you would like to see the changes to the models and fixtures,
and migrations that were created, you can check out the
`south demo <http://github.com/ericholscher/django-test-utils/tree/south-demo>`_
branch of test utils.

I would also like to thank
`Andrew Godwin <http://www.aeracode.org/>`_ for creating south, of
which none of this would be possible.

Thanks for reading, and I'd be curious to see what people think,
and if there are some improvements that could be made.


