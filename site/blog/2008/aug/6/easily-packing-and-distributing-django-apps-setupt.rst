.. post:: 2008-08-06 16:05:30

Easily packaging and distributing Django apps with setuptools and easy_install
==============================================================================

First off let me say that I know that not everyone likes setuptools
and that is fine. distutils works well and is included with python.
However, I believe that Python needs to get some parity with what
Perl has with CPAN. `Pypi <http://pypi.python.org/pypi>`_ is
Python's alternative, so tools that integrate with it are good.

Step 1: In the directory above the source directory of your
project, create a setup.py file. In that file put something like
this (editing for your project):

::

    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages
    setup(
        name = "django-testmaker",
        version = "0.1",
        packages = find_packages(),
        author = "Eric Holscher",
        author_email = "eric@ericholscher.com",
        description = "A package to help automate creation of testing in Django",
        url = "http://code.google.com/p/django-testmaker/",
        include_package_data = True
    )

This is all that you need to do to really get your file in a state
to upload. name is the name that your package will go under on
Pypi, so choose something unique and descriptive. version is the
version of your app, it understands most common versioning schemes,
more info
`here <http://peak.telecommunity.com/DevCenter/setuptools#specifying-your-project-s-version>`_.
include\_package\_data makes sure that ez\_setup.py gets included
in your package. find\_packages() is a setuptools thing that
includes everything in the current directory that it thinks is a
python module, you can also simply put the name of your app there.

``wget http://peak.telecommunity.com/dist/ez_setup.py``

If you're on a platform that doesn't have wget, simply download
that file into the directory containing setup.py and your app. This
will make sure that the person who downloads your app has
setuptools installed. If they don't, it will automatically be
installed.

Now run

::

    $ python setup.py register
    We need to know who you are, so please choose either:
     1. use your existing login,
     2. register as a new user,
     3. have the server generate a new password for you (and email it to you), or
     4. quit
    Your selection [default 1]:  2
    Username: whatever
    Password: 
     Confirm: 
       EMail: your@email.com
    You will receive an email shortly.
    Follow the instructions in it to complete registration.

Obviously, if you already have an account, simply say 1 and login.
Finish the login procedure in your e-mail and then login on the
command line.

::

    python setup.py register
    Your selection [default 1]:  1
    Username: whatever
    Password: 
    Server response (200): OK
    I can store your PyPI login so future submissions will be faster.
    (the login will be stored in /home/eric/.pypirc)
    Save your login (y/N)?y

Now you will be logged into Pypi and will be able to upload your
files. Then you want to upload your package to Pypi.

``python setup.py sdist upload``

This should output a bunch of code with your app being packaged.
The bottom of it should contain a 200 and say that it was
successfully uploaded.

::

    running upload
    Submitting dist/django-testmaker-0.1.tar.gz to http://pypi.python.org/pypi
    Server response (200): OK

Congrats! Your code is now in Pypi! It can be seen and downloaded
by the world, and easily installed on people's machines. If you
want to tell people how to install your app, it's as easy as..

``[sudo] easy_install django-testmaker``

For some reason if easy\_install doesn't work, you can still resort
to installing things the old way. You can grab the code out of svn,
or take the package from Pypi, unzip it, and move the project
directory somewhere on your PYTHONPATH.

Let me know if this doesn't work, of if I've missed something
obvious. This is my first work done packaging a django app. I
really think that it would help a lot if all django (and python in
general) apps were easily installable and listed at Pypi. Having
the directory really helps with people locating apps. Hopefully a
culture of apps getting put up on Pypi will make this reality a
little bit closer.

`Setuptools <http://peak.telecommunity.com/DevCenter/setuptools>`_
can do a lot of neat things. Look at their site for more
information on advanced packaging (like dependencies and other
things).


