.. post:: 2010-11-02 16:15:00

Celery Tips
===========

Following on yesterday's post about
`Virtualenv Tips <http://ericholscher.com/blog/2010/nov/1/virtualenv-tips/>`_,
I will be talking about `celery <http://celeryproject.org/>`_ tips.
Yesterday I talked about how to run celery with upstart easily, and
today I'll be expanding on that below as well as talking about how
to set it up using supervisord.

**Note:** Also interesting, I wrote a
`Big list of django tips <http://ericholscher.com/blog/2008/oct/5/django-tips/>`_
back in 2008, that still has a lot of good information.

Running celery in development
-----------------------------

When you run celery in production, you should be using a queue on
the backend. However, when you're running celery in development,
it's nice to execute the code paths, but not actually need a queue.
This is where the
`CELERY\_ALWAYS\_EAGER setting <http://celeryq.org/docs/configuration.html#celery-always-eager>`_
comes in handy. It makes celery run the code in process, but will
make sure your code paths work correctly.

I talk about this and more in
`my djangocon talk <http://ericholscher.com/blog/2010/sep/10/djangocon-talk/>`_.

Killing long running tasks
--------------------------

On `ReadTheDocs <http://readthedocs.org>`_ I would run into
problems with celery tasks never returning. Luckily, celery has a
way to handle this. The
`CELERYD\_TASK\_TIME\_LIMIT <http://ask.github.com/celery/configuration.html#celeryd-task-time-limit>`_
setting lets you set the number of seconds that a task can run
until it is killed. This is nice to make sure that a run-away task
won't take down all your backend processing.

Use the JSON serializer for interoperability
--------------------------------------------

I was talking on IRC to
`Eric Florenzano <http://www.eflorenzano.com/>`_ and he mentioned
that you should use the
`json serializer <http://celeryq.org/docs/userguide/executing.html#executing-serializers>`_
if you want to be able to add celery tasks from other languages.

This allows you to use another language to put a message that looks
like a
`celery task <http://ask.github.com/celery/internals/protocol.html#example-message>`_
in the queue, and it should just work.

Explictly set the number of clients
-----------------------------------

When you run celery, it defaults to having the number of workers
equal to the number of cores the machine has. If you are running
multiple queue workers on the same machine, it is a good idea to
use less. You can set this with the
`CELERYD\_CONCURRENCY <http://ask.github.com/celery/reference/celery.conf.html#celery.conf.CELERYD_CONCURRENCY>`_
setting, or passing ``-c<num>`` on the command line.

Running against multiple databases with supervisord
---------------------------------------------------

At work we run a bunch of different sites on multiple databases.
When we were figuring out how to deploy celery, we needed a good
way to make sure that celeryd was always running, and we needed
multiple celery daemons for each of our databases. We have written
our tasks to run against multiple sites on the same database in
order to reduce the number of daemons we had to use.

Celery ships with a couple of daemon configurations out of the box,
support for init.d style init scripts, and support for
`supervisord <http://supervisord.org/>`_. We first looked at the
init.d approach, but there didn't seem to be a good way to have it
run multiple settings files without creating multiple scripts,
which seemed hacky. So we went with superisord for the task. Below
is our configuration, if you are curious.

/etc/supervisord.conf
'''''''''''''''''''''

By default, the conf file is in the top-level /etc/ directory. We
kept it this way, but I kind of wish it was in it's own directory.
This is basically the exact script that
`celery ships with <http://github.com/ask/celery/blob/master/contrib/supervisord/supervisord.conf>`_

::

    unix_http_server]
    file=/tmp/supervisor.sock ; path to your socket file
    
    [supervisord]
    logfile=/var/log/supervisord/supervisord.log ; supervisord log file
    logfile_maxbytes=50MB ; maximum size of logfile before rotation
    logfile_backups=10 ; number of backed up logfiles
    loglevel=info ; info, debug, warn, trace
    pidfile=/var/run/supervisord.pid ; pidfile location
    nodaemon=false ; run supervisord as a daemon
    minfds=1024 ; number of startup file descriptors
    minprocs=200 ; number of process descriptors
    user=root ; default user
    childlogdir=/var/log/supervisord/ ; where child log files will live
    
    
    [rpcinterface:supervisor]
    supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface ;
    
    [supervisorctl]
    serverurl=unix:///tmp/supervisor.sock ; use unix:// schem for a unix sockets.
    
    [include]
    files = supervisord/celeryd.conf

Then we created a supervisord directory which we included in the
above file (in the last line) that contains the celery specific
configuration. On this machine the only thing that supervisord is
watching is celery, so that has kept our configuration simple.

/etc/supervisord/celeryd.conf
'''''''''''''''''''''''''''''

Inside of our celeryd specific configuration we went with mostly
stock options except how we are setting up the
DJANGO\_SETTINGS\_MODULE. We need to change the environment in
which we are deploying, so that the celery daemon runs against the
correct database.

::

        [program:celery-cms]
        environment = PYTHONPATH='/home/code',DJANGO_SETTINGS_MODULE='ljworld.standard'
        command=/home/code/django/bin/django-admin.py celeryd --loglevel DEBUG -c2
        user=nobody
        numprocs=1
        stdout_logfile=/var/log/celery/cms_supervisord.log
        stderr_logfile=/var/log/celery/cms_supervisord.err
        autostart=true
        autorestart=true
        startsecs=10
    
        [program:celery-weeklies]
        environment = PYTHONPATH='/home/code',DJANGO_SETTINGS_MODULE='desotoexplorer.settings'
        command=/home/code/django/bin/django-admin.py celeryd --loglevel DEBUG -c2
        user=nobody
        numprocs=1
        stdout_logfile=/var/log/celery/weeklies_supervisord.log
        stderr_logfile=/var/log/celery/weeklies_supervisord.err
        autostart=true
        autorestart=true
        startsecs=10

The really nice part about using supervisord is that our fabric
script for deploying changes to celery is just deploying the code
and then running ``supervisorctl restart celery-cms``.

I hope today's post was useful, and I'm again curious for any other
awesome celery tips!


