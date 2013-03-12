:Date: 2009-11-22 16:05:26

Correct way to handle default model fields.
===========================================

With Kong, I have been trying to figure out a way to provide
overridden model defaults. At work, our pythonpath's default to
``/home/code``, however your setup is probably different. It would
be useful if there was a simple way to let you override the
defaults for your Kong installation.

::

    pythonpath = models.CharField(max_length=255, default="/home/code")

I received a pull request that put a ``KONG_PYTHONPATH_DEFAULT``
setting, which would be read in as the default. However, it seems
like this doesn't scale particularly well, and would be annoying if
you have 5-10 fields to make defaults for.

So I thought up a couple of different approaches to this problem,
and am curious if people have input, or a better way to solve
this.

One Big Setting
^^^^^^^^^^^^^^^

This would allow for a setting, but it would only be one setting
for all of the kong defaults. I'm thinking about a dict, where the
key is the model\_field name, or just the field name. The key would
obviously be the default (or a callable that returns the default).

::

    KONG_DEFAULTS = {
        'servername': 'ljworld.com',
        'pythonpath': '/home/code',
    }

This would keep things in the settings, but not cause a huge amount
of settings bloat.

Specify a place to hold your defaults
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Specify a setting along the lines of ``KONG_DEFAULT_PATH``, which
would be a module on the pythonpath. I would import this module and
then try and pull the name of defaults from there. I would provide
a sane default in Kong for this, that would be an example of how to
do it.

::

    KONG_DEFAULT_PATH = 'kong.defaults'
    
    #kong/defaults.py
    pythonpath = '/home/code'
    servername = 'ljworld.com'

So you could set ``KONG_DEFALUT_PATH``, and then redefine the
values there. This is basically defining a convention for setting
the default values on a model.

However, this is basically the same problem/solution as some kind
of application specific settings. I really think this would be
valuable, allowing reusable apps to specify default settings, and
then letting users override them

Storing it in the database
^^^^^^^^^^^^^^^^^^^^^^^^^^

I could create a super simple model that would hold defaults for my
fields. This would allow the user to set the defaults in the
database, and then I could pass a callable to the default, which
would check for the existence of the model in the DB. This doesn't
seem like a very good option, but would at least allow for
configurable changes without touching the code.

I'm probably DOIN' IT WRONG
^^^^^^^^^^^^^^^^^^^^^^^^^^^

It seems like a subset of a larger problem, which is that it isn't
easy to define application specific information. That is an ongoing
Django problem, without a good solution. I am imagining a third
party application that might make this process easier. Does anyone
have a good solution to this?


