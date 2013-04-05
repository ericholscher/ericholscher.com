:Date: 2010-11-11 15:10:00

Building a Django App Server with Chef: Part 4
==============================================

Alternate title: There's no place like home!

This is Part 4, the final part, of my Chef tutorial. Today we're
talking about the odds and ends left over to make the server nice
to use. You can check out the first 3 parts of the series:


-  `Part 1: Chef Beginnings <http://ericholscher.com/blog/2010/nov/8/building-django-app-server-chef/>`_
-  `Part 2: Python environment buildout <http://ericholscher.com/blog/2010/nov/9/building-django-app-server-chef-part-2/>`_
-  `Part 3: Deployment <http://ericholscher.com/blog/2010/nov/10/building-django-app-server-chef-part-3/>`_

Today's code will be in the git repo under the tag
`blog-post-4 <https://github.com/ericholscher/chef-django-example/tree/blog-post-4>`_.

What we'll need
---------------

So we have our app server up and running, and ready for traffic.
Now we just need to add some other bits around the outside for it
to be fully functioning and nice to use.


-  Monitoring with `Munin <http://munin-monitoring.org/>`_
-  Background tasks with `Celery <http://celeryproject.org/>`_
-  A firewall for security
-  A /etc/hosts file for talking with other nodes
-  A .bash\_profile file so that when you shell in you'll have a
   nice environment

Let's get started.

Monitoring with Munin
---------------------

For doing monitoring with munin, we're going to need to learn our
final Chef concept, which is Templates. You should be pretty
familiar with them already, except they use Erb, which is a
template language that lets you embed Ruby.

We're only going to be configuring the Munin node here. This
assumes that you have a munin server running on another machine
that you want to give access to monitor your new app server. These
configs depend on you putting an entry like this in your node.json,
which points at the IP of the master server:

::

    "munin_servers": ["10.177.243.34"],

Then here is how you would write the Recipe.

``cookbooks/main/recipes/munin.rb``

::

    package "munin-node" do
        :upgrade
    end
    
    service "munin-node" do
      enabled true
      running true
      supports :status => true, :restart => true, :reload => true
      action [:enable, :start]
    end
    
    if node.attribute?("munin_servers")
      template "/etc/munin/munin-node.conf" do
        source "munin-node.conf"
        mode 0640
        owner "root"
        group "root"
        variables :munin_servers => node[:munin_servers] || []
        notifies :restart, resources(:service => "munin-node")
      end
    end

The template Resource here is the interesting part. We're
surrounding it with a conditional, that makes sure that we're
defined a 'munin\_servers' key in our node.json. Then we're saying
that we're going to render the munin-node.conf file with the source
template 'munin-node.conf'. This template will be given the extra
varibale 'munin\_servers', which is passed in using the variables
attribute.

Template are placed inside the cookbook in a similar place to
files.

``cookbooks/main/templates/default/munin-node.conf``

::

    <% @munin_servers.each do |server| -%>
    allow ^<%= server.to_s.gsub(/\./, '\.') %>$
    <% end -%>
    allow ^127\.0\.0\.1$
    
    host *
    port 4949
    
    log_level 4
    log_file /var/log/munin/munin-node.log
    pid_file /var/run/munin/munin-node.pid
    background 1
    setsid 1
    user root
    group root
    
    ignore_file ~$
    ignore_file DEADJOE$
    ignore_file \.bak$
    ignore_file %$
    ignore_file \.dpkg-(tmp|new|old|dist)$
    ignore_file \.rpm(save|new)$
    ignore_file \.pod$

The interesting part here is the iteration over the munin\_servers
list. It's just doing a simple ruby loop, and then outputting the
IP address that it contains into the format that munin's
configuration file expects.

**Note**: This data-driven template rendering is a really powerful
idiom, and one of my favorite parts about Chef. This allows you to
add a new server to your pool, and have all of your configuration
files updated automatically across all your server. This is hugely
powerful, and one of the primary wins of Configuration Management.
This will be shown to better effect in the /etc/hosts file later.

Installing Celery
-----------------

Installing celery is much akin to Gunicorn that was discussed
yesterady. The dependencies were installed from our pip
requirements file, and we just need to make it run in upstart.
We'll be doing that with the following setup.

Additions to ``cookbooks/main/recipes/readthedocs.rb``

::

    cookbook_file "/etc/init/readthedocs-celery.conf" do
        source "celery.conf"
        owner "root"
        group "root"
        mode 0644
        notifies :restart, resources(:service => "readthedocs-celery")
    end
    
    service "readthedocs-celery" do
        provider Chef::Provider::Service::Upstart
        enabled true
        running true
        supports :restart => true, :reload => true, :status => true
        action [:enable, :start]
    end

``cookbooks/main/files/celery.conf``

::

    description "Celery for ReadTheDocs"
    
    start on runlevel [2345]
    stop on runlevel [!2345]
    #Send KILL after 20 seconds
    kill timeout 20
    
    script
    exec sudo -i -u docs django-admin.py celeryd -f /home/docs/sites/readthedocs.org/run/celery.log -c 2 -E -B
    end script
    
    respawn

There isn't anything new or interesting here. Just more of the same
as before, to get another piece of infrastructure up and running.

A ghetto firewall install
-------------------------

I'm a big fan of not enabling services that aren't running as a
fundamental security practice, but having a basic firewall to make
sure that those are the only ports open isn't a bad idea either.
I'm not a great expert, so this is probably the weakest part of my
knowledge in this series, so take it with a grain of salt.

My favorite firewall utility is ufw. It makes managing your
firewall really simple. Here is my super basic way to configure my
firewall, it pretty much sucks :)

``cookbooks/main/recipes/security.rb``

::

    package "ufw" do
        :upgrade
    
    service "ufw" do
      enabled true
      running true
      supports :status => true, :restart => true, :reload => true
      action [:enable, :start]
    end
    
    
    bash "Enable UFW" do
    user "root"
      code <<-EOH
      ufw allow 22 #SSH
      ufw allow 80 #Nginx
      ufw allow 4949 #Munin
      EOH
    end

As you can see, we're just enabling SSH, Nginx, and Munin. If we
need to install any more packages, we'll need to expicitly open a
port, which is usually good to remind me that I'm doing it.

/etc/hosts
----------

Whenever I'm in the cloud, I find keeping track of my other servers
to be a pain. You generally want to use the internal backplane to
communicate between your servers, so I use the /etc/hosts file to
make that simple.

We're going to depend on an entry in your node.json that looks
something like this:

::

      "all_servers": {"Golem": ["10.177.234.234", "173.203.234.234"],
                       "Chimera": ["10.177.234.234", "204.232.234.234"],
                       "Hydra": ["10.177.234.234", "173.203.234.234"] }

Which is a mapping of all your servers, with their internal and
external IPs. This will be useful to have for lots of different
recipes, and it would be nice to autogenerate this, but when you
only have a few servers it isn't so bad.

The rest of out hosts configuration looks like this:

Addition to ``cookbooks/main/recipes/default.rb``

::

    if node.attribute?("all_servers")
      template "/etc/hosts" do
        source "hosts"
        mode 644
        variables :all_servers => node[:all_servers] || {}
      end
    end

``cookbooks/main/templates/default/hosts``

::

    127.0.0.1     localhost localhost.localdomain
    
    <% @all_servers.each_pair do |name, ips| -%>
    <%= ips[0] %> <%= ips[1] %> <%= name %>
    <% end -%>

As you can see, when we add a server to the all\_servers hash, it
will propogate out to the /etc/hosts file of our app server. This
makes me really happy, and showcases some of the more advanced use
cases of Chef.

Customizing your shell
----------------------

Now that we have the server all set up, it won't be much good if it
isn't nice to use when we shell in. So here is how I go ahead and
add in some nicities to bash for when you log in.

Addition to ``cookbooks/main/recipes/readthedocs.rb``

::

    cookbook_file "/home/docs/.bash_profile" do
        source "bash_profile"
        owner "docs"
        group "docs"
        mode 0755
    end

``cookbooks/main/files/default/bash_profile``

::

    . .bashrc
    
    export PIP_DOWNLOAD_CACHE=/tmp/pip
    export DJANGO_SETTINGS_MODULE=settings
    export PYTHONPATH=$PYTHONPATH:~/sites/readthedocs.org/checkouts/readthedocs.org
    export EDITOR=vim
    
    . sites/readthedocs.org/bin/activate
    
    cd ~/sites/readthedocs.org/
    
    
    alias chk='cd /home/docs/sites/readthedocs.org/checkouts/readthedocs.org'
    alias run='cd /home/docs/sites/readthedocs.org/run'

First off, we're sourcing the .bashrc file, so that we get all the
nice things it provides, like a colored PS1. Then we're setting
some environment variables so that django-admin.py and pip work
nicely. Then we activate our virtualenv and switch into it's base
directory, so we're always starting where we want to be on login.
Then we just have a couple of aliases for easy navigation around.

I like how this makes the user experience of shelling into the
server a lot nicer, and makes the manual workflow that you'll
eventually have to fiddle with really nice.

Conclusion
----------

So that's the end of this tutorial. I hope that it was instructive
in learning Chef, as well as providing some insights into the
deployment of a Django application. Tomorrow (or if I'm too tired,
next week), I'll be providing some thoughts on how I think chef
treated me, and how I feel about the build out.


