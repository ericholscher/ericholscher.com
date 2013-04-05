:Date: 2010-11-08 17:00:00

Building a Django App Server with Chef: Part 1
==============================================

Alternate title: Fucking Chef, How does it work?

When I started looking at
`Chef <http://wiki.opscode.com/display/chef/Home>`_, I found it
incredibly complex and lacking in fundamental documentation. This
is going to be my experience understanding Chef while setting up a
single server. This strategy can be used across multiple servers,
with a little tweaking.

I'd like to thank `Jacob <http://jacobian.org/>`_ for the ideas and
some of the inspiration behind the code and ideas. The code for
this blog post can be found
`on github <https://github.com/ericholscher/chef-django-example>`_.
It will be expanded as I write updates.

Today's code will be using tag
`blog-post-1 <https://github.com/ericholscher/chef-django-example/tree/blog-post-1>`_
in the repo.

Goal
----

I'm hoping to write a blog series that goes from explaining what
Chef is, to having a working Django server, and to release all this
code so that you can tweak and use it with your own servers. I'll
be doing this to set up a new and configuration managed server for
`ReadTheDocs <http://readthedocs.org/>`_.

There are a
`couple of <http://brainspl.at/articles/2009/01/31/cooking-with-chef-101>`_
other
`good chef intros <http://morethanseven.net/2010/10/30/Chef-hello-world.html>`_
available. However, they only get you to the super basic first step
of setting up the server. Hopefully this series will be more in
depth and useful to actually getting a real server running under
Chef.

Basic terminology
-----------------

Chef has some basic terminology that you need to understand before
we get into things. I'm going to purposefully leave out a ton of
stuff, because it isn't really important for me now.


-  Cookbook (cookbooks/\*)

A cookbook, not surprisingly, contains recipes. With my
configuration, we're only going to use one cookbook, that has
multiple recipes. This is probably wrong and horrible, but it's
simple, which is the goal for now.


-  Recipe (cookbooks/\*/recipes/\*.rb)

A recipe is the basic building block of Chef. It is what does the
meat of the work that you want done.


-  Resources

A resources is an abstraction that defines a specific piece of your
configuration. It can be a file, a user, or just about anything you
want to talk about on your system.


-  Attributes (node.json)

Attributes are just a blob of JSON that Chef uses to pass around
data. It will be (slightly) different for each server that you want
to set up. I really like this approach, because I think a
data-driven approach is the correct way to solve this problem.

Bootstrapping chef
------------------

We'll be running what is called
`chef solo <http://wiki.opscode.com/display/chef/Chef+Solo>`_. This
means that chef will be run independently of a server, and just
execute on our one host. This seems to be the easiest way to get
things running.

When you first run ``chef-solo``, it will look for a ``solo.rb``
file. The
`documentation about configuring chef-solo <http://wiki.opscode.com/display/chef/Chef+Solo#ChefSolo-ConfigureChefSolo>`_
does a decent job of explaining this. By default it looks in
/etc/chef/solo.rb, so lets go ahead and use that. It has 2 required
fields, a ``cookbook_path`` and ``json_attribs``. ``cookbook_path``
tells chef where to find the "cookbooks" it uses to run your code,
and ``json_attribs`` tells it where to load in your data
dictionary.

**Note**: The docs say that ``file_cache_path`` is required, but it
just defaults to ``/var/chef/cache``.

For simplicity, we're going to keep our cookbooks and json data
file in ``/etc/chef``. On my local machine I keep everything in a
``~/projects/chef`` directory, and then sync that to the remote
box.

In production you'll probably want to set up your remote server to
pull from a repository somewhere, so that you can have a stable
deployment base, but again, syncing from the local filesystem is
simple and works.

Bootstrapping your new server
-----------------------------

I'll be using a `fabric <http://docs.fabfile.org/>`_ script to run
the commands on a remote server, which also allows me to run them
again later on a new machine in an automated fashion. So this is
the first simple script that we'll use to bootstrap our new server,
``fabfile.py``:

::

    from fabric.api import env, local, sudo
    env.user = 'root'
    env.hosts = ['204.232.205.196']
    
    env.chef_executable = '/var/lib/gems/1.8/bin/chef-solo'
    
    def install_chef():
        sudo('apt-get update', pty=True)
        sudo('apt-get install -y git-core rubygems ruby ruby-dev', pty=True)
        sudo('gem install chef', pty=True)
    
    def sync_config():
        local('rsync -av . %s@%s:/etc/chef' % (env.user, env.hosts[0]))
    
    def update():
        sync_config()
        sudo('cd /etc/chef && %s' % env.chef_executable, pty=True)

**A couple notes**: the chef executable is version-dependent, but
that's because I don't know enough ruby to query it dynamically.
You will also need to change the value of the env.hosts to a server
that you actually control.

This will install the ruby dependencies, and get chef up and
running for you. You'll need to install fabric
(``pip install fabric``, presumably in a virtualenv), and then run
``fab install_chef`` to get it up and running. Then you can go
ahead and run ``fab sync_config`` to get your chef configuration
onto the remote server.

Now we need to go ahead and figure out how to make chef actually do
something. You'll see in the ``cookbooks/main/recipes/default.rb``
file we have a simple ``package`` declaration. This simply means to
make sure that the package is installed on the remote system. This
is as simple as it gets, so lets go ahead and run it. With the
``fab update`` command, it will sync your local directory, and run
chef on the remote server.

::

    -> fab update
    [localhost] run: rsync -av . root@204.232.205.196:/etc/chef
    [204.232.205.196] sudo: cd /etc/chef && /var/lib/gems/1.8/gems/chef-0.9.12/bin/chef-solo
    [204.232.205.196] err: stdin: is not a tty
    [204.232.205.196] out: [Tue, 09 Nov 2010 01:42:01 +0000] INFO: Setting the run_list to ["main::default"] from JSON
    [204.232.205.196] out: [Tue, 09 Nov 2010 01:42:01 +0000] INFO: Starting Chef Run (Version 0.9.12)
    [204.232.205.196] out: [Tue, 09 Nov 2010 01:42:01 +0000] INFO: Installing package[curl] version 7.21.0-1ubuntu1
    [204.232.205.196] out: [Tue, 09 Nov 2010 01:42:04 +0000] INFO: Chef Run complete in 2.574963 seconds
    [204.232.205.196] out: [Tue, 09 Nov 2010 01:42:04 +0000] INFO: cleaning the checksum cache
    [204.232.205.196] out: [Tue, 09 Nov 2010 01:42:04 +0000] INFO: Running report handlers
    [204.232.205.196] out: [Tue, 09 Nov 2010 01:42:04 +0000] INFO: Report handlers complete

**You now have Chef running on your server**. That was pretty easy,
eh? For tomorrow's lesson, we'll be making it actually do
something, like installed nginx and gunicorn, and keeping track of
config files.


