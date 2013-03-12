:Date: 2010-11-10 18:12:00
Building a Django App Server with Chef: Part 3
==============================================

Alternate title: Show the world what you've got.

This is Part 3 of my Chef tutorial. Today we're talking about
deployment. You can check out the first 2 parts of the series:


-  `Part 1: Chef Beginnings <http://ericholscher.com/blog/2010/nov/8/building-django-app-server-chef/>`_
-  `Part 2: Python environment buildout <http://ericholscher.com/blog/2010/nov/9/building-django-app-server-chef-part-2/>`_

Today's code will be in the git repo under the tag
`blog-post-3 <https://github.com/ericholscher/chef-django-example/tree/blog-post-3>`_.

What we'll need
---------------

We'll be taking the Django application that we have on the server
and actually deploying it. Let's make a list of what we'll need:


-  A web server to sit in front and proxy requests
-  A WSGI server
-  A way to keep both of these things running
-  A caching layer

We'll be using Nginx, Memcached, Upstart, and Gunicorn. This is my
preferred deployment stack as of late, mainly because of the simple
setup.

Let's get started

A web server
------------

Getting Nginx up and running should be old hat by this point. We're
going to need the package and service Resources, which will tell
Chef to install and run it.

``cookbooks/main/recipes/nginx.rb``

::

    package "nginx" do
        :upgrade
    end
    
    service "nginx" do
      enabled true
      running true
      supports :status => true, :restart => true, :reload => true
      action [:start, :enable]
    end
    
    cookbook_file "/etc/nginx/sites-enabled/readthedocs" do
      source "nginx/readthedocs"
      mode 0640
      owner "root"
      group "root"
      notifies :restart, resources(:service => "nginx")
    end
    
    cookbook_file "/etc/nginx/nginx.conf" do
      source "nginx/nginx.conf"
      mode 0640
      owner "root"
      group "root"
      notifies :restart, resources(:service => "nginx")
    end

As you can see, we're providing our own nginx.conf and a
readthedocs site configuration. I'm not going to paste these in, as
they are pretty application specific, but you can look at them
`on Github <https://github.com/ericholscher/chef-django-example/tree/blog-post-3/cookbooks/main/files/default/nginx/>`_
if you're curious. I also wrote about it
`a while back <http://ericholscher.com/blog/2010/aug/28/new-feautures-read-docs/>`_.

The only new part here is the ``notifies`` command, which is pretty
nifty. It basically means that whenever you change the nginx.conf
file, it should restart Nginx, which is a really nice feature.

A WSGI Server
-------------

Yesterday, when we installed the deploy\_requirements.txt with pip,
it pulled in `gunicorn <http://gunicorn.org/>`_. So we actually
have Gunicorn already installed in our virtualenv, waiting for us
to use it. The only difference is I actually committed a change to
the ReadTheDocs source so that it will pull Gunicorn from the git
master, which I'll explain below.

Upstart
-------

**Note**: I use upstart because it ships with Ubuntu, so you don't
need to install a separate package. However, it has pretty horrible
documentation, with the
`Stanzas <http://upstart.ubuntu.com/wiki/Stanzas>`_ doc probably
the best clue as to what it supports.

Here is where things get interesting. I spent a bunch of time
trying to get gunicorn and upstart to play nicely yesterday night,
but it wasn't working. I went on the #gunicorn IRC channel on
Freenode today, and talked with benoitc. He was awesome and
`patched gunicorn <https://github.com/benoitc/gunicorn/commit/f29c61091691135dcfae029a7eadf1663a06a73e>`_
to work with Upstart for me.

Here is the upstart script that we're using to keep gunicorn
running:

``cookbooks/main/files/default/gunicorn.conf``

::

    description "Gunicorn for ReadTheDocs"
    
    start on runlevel [2345]
    stop on runlevel [!2345]
    #Send KILL after 5 seconds
    kill timeout 5
    respawn
    
    env VENV="/home/docs/sites/readthedocs.org"
    
    #Serve Gunicorn on the internal rackspace IP.
    script
    exec sudo -u docs $VENV/bin/gunicorn_django --preload -w 2 --log-level debug --log-file $VENV/run/gunicorn.log -p $VENV/run/gunicorn.pid -b 10.177.69.207:8888 $VENV/checkouts/readthedocs.org/settings/postgres.py
    end script

As you can see, an Upstart script is a pretty clean way to do this.
If you've ever tried to write an old SysV-style init script, this
will look beautiful. You'll notice that we aren't passing the
--daemon parameter to gunicorn, this is because upstart will
background the process for us, and keep track of everything, so we
don't need gunicorn's daemonizing behavior.

It should be pointed out how awesome it is that we can run a
production ready WSGI server with a single line of bash. If you've
ever set up a mod\_wsgi install, needing to fuddle with your
apache.conf and a WSGI file and everything makes it a chore. This
is quite simply the easiest way to deploy a WSGI application.

Then we need some additions to
``cookbooks/main/recipes/readthedocs.rb``:

::

    cookbook_file "/etc/init/readthedocs-gunicorn.conf" do
        source "gunicorn.conf"
        owner "root"
        group "root"
        mode 0644
    end
    
    service "readthedocs-gunicorn" do
        provider Chef::Provider::Service::Upstart
        enabled true
        running true
        supports :restart => true, :reload => true, :status => true
        action [:enable, :start]
    end

Here you can see we're doing a similar thing to the other service
declarations. We however need to tell Chef to use Upstart for this
service, instead of defaulting to init.d. Other than that,
everything here should look similar to the other files and services
we've set up.

Memcached
---------

As you would expect, installing memcached is just like nginx:

``cookbooks/main/recipes/memcached.rb``

::

    package "memcached" do
        :upgrade
    end
    
    service "memcached" do
      enabled true
      running true
      supports :status => true, :restart => true
      action [:enable, :start]
    end
    
    cookbook_file "/etc/memcached.conf" do
      source "memcached.conf"
      mode 0640
      owner "root"
      group "root"
      notifies :restart, resources(:service => "memcached")
    end

The memcached.conf is so short, I might as well include it here:

::

    -d
    logfile /var/log/memcached.log
    -m 64
    -p 11211 
    -u nobody
    -l 127.0.0.1

Memcache's config file is pretty neat, because it's basically just
a list of arguments to pass to the daemon when it's started. A
little bit like a pip requirements file is just commands to pass to
pip install when it's run.

Wrapping up
-----------

Now that you have these awesome new recipes, and additions to old
ones, we need to make sure they're actually being run. Your
run\_list in your node.json file should now look something like
this:

::

    "run_list": [ "main::default", "main::python", "main::readthedocs", "main::memcached", "main::nginx"],

At this point, it's pretty neat. I can run a
``fab install_chef update``, wait about 5 minutes, and go from a
freshly paved server to a fully functioning app server.

Tomorrow we'll be adding some monitoring and auxiliary niceties.
This includes setting up Munin, Celery, generating the /etc/hosts
file, and throwing in a little .bashrc magic to make the user
experience nicer.

There were a couple of questions yesterday about databases and
other things. My current problem is running an application server,
which is what I've accomplished. However, with my new-found love
affair for chef, I will definitely be making my Database/Utility
box into a chef configuration really soon. I might not write it up
in so much detail, but hopefully you've learned enough from this
series that I can just publish the code.


