:Date: 2011-01-10 19:09:27
Handling Django Settings Files
==============================

I have seen a lot of talk over the past couple years about how to
handle different settings files and databases, synced between
production and development. I have happened onto a way of doing it
that makes me happy, and figured I would share it with the world.

File structure
--------------

I use a file structure that looks like this:

::

    project/
        settings/
            __init__.py (empty)
            base.py
            sqlite.py
            postgres.py

The base.py contains all of the configuration options that are
shared among the databases. INSTALLED\_APPS, etc. All of the
DATABASE settings should be specified in the more-specific files.
As well as things that differ by environment, like remote servers,
cache settings, cookie domains, and other things.

This allows you to run the sqlite settings file, and have it be set
to localhost, or whatever your development settings are. Then in
production you just run against the postgres settings.

A good example of this being used in practice is on
`Read the Docs <https://github.com/rtfd/readthedocs.org/tree/master/settings>`_.

**But wait, there's more!**

manage.py for dev
-----------------

./manage.py is great for development. It is the easiest way to get
started, and it automatically sets up your paths and stuff. With my
setup, I actually
`explicitly set <https://github.com/rtfd/readthedocs.org/blob/master/manage.py#L3>`_
manage.py's settings file to the sqlite file.

This means that whenever you are using manage.py, you are in a
development context. So, what do you do about production?

django-admin.py is for production
---------------------------------

In production, you set your DJANGO\_SETTINGS\_MODULE to the
postgres settings file. So whenever you use django-admin.py, you
will be running against the production database.

**I really like this scheme, because it gives you a logical distinction between production and development in your code, and in your interface on the CLI.**
When you are developing, you are using manage.py and editing the
sqlite settings file. The reverse for production.


