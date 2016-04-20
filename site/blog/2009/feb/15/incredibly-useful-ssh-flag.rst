.. post:: 2009-02-15 17:05:59

Incredibly useful SSH flag
==========================

So at work we have a lot of different django environments,
scattered across varies servers. All of this information is kept in
a central resource. We have the pythonpath, settings file, and the
remote server that the client is on. So every time that I want to
go do work on a different site, I have to ssh into that server, set
the PYTHONPATH and DJANGO\_SETTINGS\_MODULE environmental variable,
and then do what I want to do. This is not a huge deal, but it is
annoying when you're doing it 10-20 times a day.

So I went along and tried to figure out the best way to handle this
situation. One of the popular ways to achieve this type of
functionality is a simple shell script on the remote client, that
sets the environment. You ssh into the client, change into the
clients directory, and source it into bash to get into your
environment. This didn't really solve my problem, because it's
basically what I was already doing.

It would be really nice to be able to run an ssh command, to the
remote server, and have it executed. SSH has this ability, simply
by passing a command after your connect string.

::

    $ ssh ericholscher.com uptime
    19:11:28 up 69 days, 21:29,  1 user,  load average: 0.00, 0.00, 0.00

However, this simply executes and returns. I want to be able to set
up my environment on the remote side. With the ``-t`` command to
SSH, this allows you to do exactly that. It sets up a psuedo-tty on
the remote side, which then lets you execute commands! So you can
do something like this:

::

    $ ssh ericholscher.com -t DJANGO_SETTINGS_MODULE=test.settings bash
    eric@Odin:~$ env |grep DJ
    DJANGO_SETTINGS_MODULE=test.settings
    
    $ ssh ericholscher.com -t PYTHONPATH='$HOME/Python' django-admin.py dbshell
    SQLite version 3.5.9
    Enter ".help" for instructions
    sqlite>
    
    $ ssh ericholscher.com -t PYTHONPATH='$HOME/Python' django-admin.py shell
    [..ipython startup truncated..]
    In [1]: import django
    
    In [2]: django.VERSION
    Out[2]: (1, 1, 0, 'alpha', 0)

Note that the PYTHONPATH variable is quoted. This is because I am
using the $HOME variable, if you don't quote it, it will be
evaluated on the client side. If you quote it, it gets passed to
the server to be set.

I have written a datastore backend that keeps all of my sites
settings and pythonpaths (along with other information), and then I
wrote a simple wrapper script around that. I will hopefully be
releasing this code in the near future, but it allows me to do
things along these lines.

::

    $ ./assume.py production my_site shell
    $ ./assume.py production test_project shell
    $ ./assume.py staging my_site dbshell
    $ ./assume.py local my_site syncdb

and end up in the correct place.

A really neat part of this is that when you do something like
dbshell, you are sent to the remote site, and you can perform an
action. However, when you leave that command, you are brought back
to the local environment that you were already working in. This
makes it really easy to be able to do simple one off actions on a
remote site (like fixing a bug). This comes up a lot at work, eg:
someone is reporting X on server Y, can you please check the
database over there really quick.

This gives you a lot of value because you are connected to the
database with the credentials in the settings. It really allows you
to abstract the knowledge that is in your settings files and build
commands around them. Any custom management commands that are
defined on the remote server are also really easy to activate as
well. This allows you to think "I need to reindex the search on
client Z", you simply do something like ``./assume.py Z reindex``,
and then go on about your previously scheduled activity. You don't
have to think what server the client is running on, what version of
django, where the code lives, or anything like that.

I'd love to hear other ideas that people have for this kind of
system. I think that a simple reusable app that keeps track of your
different servers and commands would be really neat and useful.
Perhaps integrating it into Fabric or something would be possible
as well.


