.. post:: 2010-11-01 18:00:00

Virtualenv Tips
===============

`Virtualenv <http://virtualenv.readthedocs.org/>`_ is a project
that is indispensable for most Python devs these days. I am writing
down some tips here so mainly for personal reference, and because I
found them useful.

Virtualenv & Upstart
--------------------

For my `ReadTheDocs <http://readthedocs.org>`_ project, I was
wanting to run `celery <http://celeryproject.org/>`_ as a
background process that processes documentation building. I'm
running Ubuntu, so their built-in upstart service seems like a
logical choice. I really like upstart because of it's simple
configuration, but it is rather undocumented (this
`Stanzas <http://upstart.ubuntu.com/wiki/Stanzas>`_) page is a
useful starting point).

`Carl Meyer <http://twitter.com/#!/carljm>`_ pointed out to me that
in order
**to get inside the context of a virtualenv, you don't need to munge your pythonpath or anything, but simply run the correct script from inside the virtualenv**.
So a simple ``/path/to/virtualenv/bin/django-admin.py celeryd`` was
all that was needed to get inside the virtualenv's context.

This also true of the python executable inside your python
directory. ``/path/to/virtualenv/bin/python`` will allow you to run
any python script inside of that virtualenv's context.

I also wanted to be running my jobs as the user for that site, so
``sudo`` is the correct tool for that. The final file ended up
looking like this:

::

    description "Celery for ReadTheDocs"
    
    start on runlevel [2345]
    stop on runlevel [!2345]
    #Send KILL after 20 seconds
    kill timeout 20
    
    script
    exec sudo -i -u docs django-admin.py celeryd -f /home/docs/sites/readthedocs.com/run/celery.log -c 2 -B
    end script
    
    respawn

The only other interesting bit there is the ``-i`` option to sudo,
which means it will run the command as a login shell, picking up
the environment for the user. This means it has the correct path
and everything set, so that ``django-admin.py`` works without an
explicit PATH.

Adding site-packages in after initial creation
----------------------------------------------

`Frank Wiles <http://www.frankwiles.com/>`_ ran into this problem
on IRC, where he wanted to add in the site-packages after creating
a virtualenv with ``--no-site-packages``. It turns out to be really
simple, in that you only have to remove the
``no-global-site-packages.txt`` in the ``lib/python2.x`` directory
inside the virtualenv. After that virtualenv will go ahead and
fallback to the global site packages happily.

I'd imagine this would work the other way as well, if you want to
not have your site-packages included, you could add this file into
your virtualenv.

Use virtualenvwrapper
---------------------

`Virtualenvwrapper <http://www.doughellmann.com/docs/virtualenvwrapper/>`_
is a nice set of extensions around virtualenv. It gives you handy
command line helpers, like ``workon`` which autocompletes the names
of your virtualenv's. It has its own
`Tips and Tricks <http://www.doughellmann.com/docs/virtualenvwrapper/tips.html>`_
page that has some neat ideas about how to improve your virtualenv
experience.

Deploying Virtualenv
--------------------

Deploying with virtualenv and apache has been well covered. I
recommend this
`Caktus post <http://www.caktusgroup.com/blog/2010/04/22/basic-django-deployment-with-virtualenv-fabric-pip-and-rsync/>`_
that gives some good examples.

The main idea however, is that you make sure your the virtualenv's
pythonpath is on your pythonpath, or that you are running the
virtualenv's python when you run your webserver. For apache, in
your wsgi file, you generally do something like:

::

    site_packages = os.path.join(PROJECT_ROOT, 'env/lib/python2.6/site-packages')
    site.addsitedir(os.path.abspath(site_packages))

For a gunicorn deployment, you would do something along the lines
of ``/path/to/virtualenv/bin/python manage.py run_gunicorn``.

Your tips
---------

I'd love to hear your tips about how to use virtualenv in the best
way possible. I know that my workflow is probably lacking, and
these aren't all or even many of the neat things you can do with
virtualenv.


