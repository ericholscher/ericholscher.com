:Date: 2010-11-09 17:00:00

Building a Django App Server with Chef: Part 2
==============================================

Alternate title: Actually doing something useful.

`Yesterday <http://ericholscher.com/blog/2010/nov/8/building-django-app-server-chef/>`_
we covered the basics to getting started with Chef. You should have
a remote server configured with chef, and have curl installed! Now
lets go ahead and get some useful bits for your Django
application.

What we'll need
---------------

So this is going to be based around the way that I set up my
servers, so if this is different than you, I'm sorry. However, I
think it is a pretty solid way of managing them. A lot of the ideas
here are stolen from `Travis <http://traviscline.com/>`_ when he
set up the server for Pypants.

So lets assemble a list of things we're going to want in order to
get a super basic Django configuration running:


-  A user to run our code as and who's home directory we'll store
   the data.
-  A basic global python ecosystem, including setuptools and pip
-  A virtualenv to store all the project-specific packages and code
   in
-  A copy of the project that we'll be running

Let's get started.

The finished code for today is located on github, with the
`tag blog-post-2 <https://github.com/ericholscher/chef-django-example/tree/blog-post-2>`_.
It is a copy of the completed steps, so feel free to peek through
that and come back here for clarification (or to ask questions).

Setting up our user
-------------------

For `RTD <http://readthedocs.org/>`_, I run everything under the
user docs. So we'll go ahead and set up that user so that we can
get our site set up. We're going to go ahead and replace our
"default" recipe, because right now it isn't doing anything much
useful. The relevant part is below:

``cookbooks/main/recipes/default.rb``

::

    node[:base_packages].each do |pkg|
        package pkg do
            :upgrade
        end
    end
    
    node[:users].each_pair do |username, info|
        group username do
           gid info[:id] 
        end
    
        user username do 
            comment info[:full_name]
            uid info[:id]
            gid info[:id]
            shell info[:disabled] ? "/sbin/nologin" : "/bin/bash"
            supports :manage_home => true
            home "/home/#{username}"
        end
    
        directory "/home/#{username}/.ssh" do
            owner username
            group username
            mode 0700
        end
    
        file "/home/#{username}/.ssh/authorized_keys" do
            owner username
            group username
            mode 0600
            content info[:key]
        end
    end
    
    node[:groups].each_pair do |name, info|
        group name do
            gid info[:gid]
            members info[:members]
        end
    end

There's a lot of stuff going on here, so lets go over it. First you
might notice that there's this node variable, the node data
structure is the JSON that you have in your node.json file. It is
looping over the keys and values with ruby's each\_pair and pair
functions.

The base\_packages bit is a cool example of the power of the chef
configuration. We have a list of packages that we want to install
in our Attributes, and we're looping over them and setting using
the package Resource.

I realize I skipped over the run\_list part yesterday, but it
basically is just a list of recipes to run. Each of the resources
in the default.rb file should be pretty self explanatory. The
`Chef Resource Documentation <http://wiki.opscode.com/display/chef/Resources>`_
is really comprehensive, and will probably be the most referenced
document that you use. The main resource's that we used were
**group, user, file, directory**, let's take a look at the
`User <http://wiki.opscode.com/display/chef/Resources#Resources-User>`_
declaration in particular.

Everything there should be pretty obvious, as it's the information
that goes into /etc/passwd for the user. However, the ``supports``
keyword isn't obvious at first. This is part of the
`Common Attributes <http://wiki.opscode.com/display/chef/Resources#Resources-CommonAttributes>`_
that can be set on all Resources. It's a way of passing along
configuration options to the Resource. manage\_home actually just
makes it so that the users home directory is created when the user
is created.

So we're going to have to go ahead and put some data in there for
it to work with. Our node.json will now look like this:

``node.json``

::

    {
      "run_list": [ "main::default", "main::python", "main::readthedocs" ],
      "base_packages": ["git-core", "bash-completion"],
    
      "users": {
        "docs": {
          "id": 1001,
          "full_name": "Docs User",
          "key": "ssh-rsa key-goes-here eric@Bahamut"
        }
      },
    
      "groups": {
        "docs": {
          "gid": 201,
          "members": ["docs"]
        }
      }
    }

Adding a Basic Python Environment
---------------------------------

Now lets go ahead and add a python recipe to build out some basic
python stuff that we'll be needing.

``cookbooks/main/recipes/python.rb``

::

    node[:ubuntu_python_packages].each do |pkg|
        package pkg do
            :upgrade
        end
    end
    
    # System-wide packages installed by pip.
    # Careful here: most Python stuff should be in a virtualenv.
    
    node[:pip_python_packages].each_pair do |pkg, version|
        execute "install-#{pkg}" do
            command "pip install #{pkg}==#{version}"
            not_if "[ `pip freeze | grep #{pkg} | cut -d'=' -f3` = '#{version}' ]"
        end
    end

Additions to ``node.json``

::

      "ubuntu_python_packages": ["python-setuptools", "python-pip", "python-dev", "libpq-dev"],
      "pip_python_packages": {"virtualenv": "1.5.1", "mercurial": "1.7"},

Here we're adding some global packages that we need. We're going to
install setuptools and pip so that we can install further python
packages. python-dev and libpq-dev are so that we have the headers
for libraries that need to compile against postgres and python.
We'll also be installing virtualenv and mercurial globally so that
we can create our virtualenv and install packages from mercurial.

Creating a virtualenv
---------------------

We're going to introduce the first new Chef concept here, which is
called a
`Definition <http://wiki.opscode.com/display/chef/Definitions>`_.


-  Definition (cookbooks/\*/definitions/\*.rb)

   A definition is a custom Resource that you build to abstract a set
   of operations. Pretty simple


This is a definition that
`Jacob published <https://gist.github.com/612395>`_ and then I
updated to make the permissions correct. It allows you to set up a
virtualenv:

``cookbooks/main/definitions/virtualenv.rb``

::

    define :virtualenv, :action => :create, :owner => "root", :group => "root", :mode => 0755, :packages => {} do
        path = params[:path] ? params[:path] : params[:name]
        if params[:action] == :create
            # Manage the directory.
            directory path do
                owner params[:owner]
                group params[:group]
                mode params[:mode]
            end
            execute "create-virtualenv-#{path}" do
                user params[:owner]
                group params[:group]
                command "virtualenv #{path}"
                not_if "test -f #{path}/bin/python"
            end
            params[:packages].each_pair do |package, version|
                pip = "#{path}/bin/pip"
                execute "install-#{package}-#{path}" do
                    user params[:owner]
                    group params[:group]
                    command "#{pip} install #{package}==#{version}"
                    not_if "[ `#{pip} freeze | grep #{package} | cut -d'=' -f3` = '#{version}' ]"
                end
            end
        elsif params[:action] == :delete
            directory path do
                action :delete
                recursive true
            end
        end
    end

As you can see, it takes a bunch of arguments, then just wraps up a
bunch of Resource definitions in a nice little package. There is a
little bit of magic with the pip freezing things, but it's
basically just how we're checking to make sure that a package isn't
instead before we install it. We are using only using the
**directory and execute** Resources here.

Now we're going to use this virtualenv Definition, and create the
home virtualenv for our site. I like to keep my virtualenv's in
``~/sites/<domain>``, so this will go into
``/home/docs/sites/readthedocs.org/``. Since this is becoming
specific to the site we're building, it's going to go into a
readthedocs recipe:

``cookbooks/main/recipes/readthedocs.rb``

::

    directory "/home/docs/sites/" do
        owner "docs"
        group "docs"
        mode 0775
    end
    
    virtualenv "/home/docs/sites/readthedocs.org" do
        owner "docs"
        group "docs"
        mode 0775
    end

This will set up a basic virtualenv in our directory.

Getting our site set up
-----------------------

To get our site set up, we need to pull in the source code, and
make sure our virtualenv has all the requirements. This code is a
little bit hacky, and could probably be abstracted out a bit, but
it will work for now. We're going to go ahead and add some things
to our readthedocs Recipe.

Additions to ``cookbooks/main/recipes/readthedocs.rb``

::

    directory "/home/docs/sites/readthedocs.org/run" do
        owner "docs"
        group "docs"
        mode 0775
    end
    
    git "/home/docs/sites/readthedocs.org/checkouts/readthedocs.org" do
      repository "git://github.com/rtfd/readthedocs.org.git"
      reference "HEAD"
      user "docs"
      group "docs"
      action :sync
    end
    
    script "Install Requirements" do
      interpreter "bash"
      user "docs"
      group "docs"
      code <<-EOH
      /home/docs/sites/readthedocs.org/bin/pip install -r /home/docs/sites/readthedocs.org/checkouts/readthedocs.o
    rg/deploy_requirements.txt
      EOH
    end

I like to have my runtime files in the ``venv/run`` directory, so
we'll go ahead and create that directory. Then comes the fun part.

We are checking the Readthedocs source out of github with the
`git <http://wiki.opscode.com/display/chef/Deploy+Resource#DeployResource-Examples>`_
Resource. Chef only supports git and svn as far as I can tell, so
luckily I'm using git.

Then we're going to install from the pip requirements file. This is
using the
`script Resource <http://wiki.opscode.com/display/chef/Resources#Resources-Script>`_,
which allows you to inline a bash, ruby, python, or more script
inside your Recipe. This is using a hard coded bash script to
install the requirements, which sucks, but will work for now.

**Note**: Chef appears to buffer output and not show itself as
doing anything when running the script Resource here, so it will
look like your build will hang while it installs your pip
requirements file for the first time.

Done for now
------------

Alright, this post has gotten long enough, so we're done for today.
But we're in a pretty awesome spot, I think. We now have our app
server set up with a runnable version of our code. You can go ssh
in and play around, you should be able to run simple manage.py
commands inside the virtualenv and whatnot (after a syncdb).

Tomorrow we'll talk about deploying our code with Nginx and
Gunicorn. I've been having trouble with Upstart, so we might switch
our deployment to Supervisord, but we'll see how it goes.

Don't forget to check out the finished code
`on Github <https://github.com/ericholscher/chef-django-example/tree/blog-post-2>`_
to see the actual running examples.


