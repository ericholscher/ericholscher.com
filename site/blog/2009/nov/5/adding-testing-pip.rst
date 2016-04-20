.. post:: 2009-11-05 15:22:38

Adding testing to pip
=====================

Python packaging has been in a bit of a state of disarray for as
long as I've been using it. Pip has come along to make installing
python packages easier. It has a lot of features that are useful,
but they have been talked about in many other blog posts.

Today I want to talk about adding testing to pip. If you are
familiar with the Perl community, then you probably know about
`CPAN <http://cpan.org/>`_. It is basically Pypi for Perl. They
have a command, called cpan, which allows you to install packages
in a similar way to pip.

One of the steps that a package goes through before being installed
on your system is that the tests are run. This allows you to know
if the package that you have installed is actually going to work on
your system. It may be broken on your platform, or you may be
missing a library that it thought you had. Currently, pip has no
way to test packages when they are being installed. I went looking
for a way to make that happen.

It should be noted that pip is based on setuptools. Setuptools is
what parses and understands most of the logic inside of your
setup() function in the setup.py for your project (which you have,
right?). Setuptools has an option called ``test_suite``, which
allows you to run
`setup.py test <http://peak.telecommunity.com/DevCenter/setuptools#test-build-package-and-run-a-unittest-suite>`_
on your package, and have it run the unit tests. This is done by
calling whatever python function is defined in ``test_suite``.

I added the ability for pip to run ``setup.py test`` on a package
that it is installing. It is executed by running
``pip install --test <package>``. The implementation is on a
`ticket <http://bitbucket.org/ianb/pip/issue/11/allow-tests-to-be-run-upon-install#>`_
on bitbucket, and in a
`repository <http://github.com/ericholscher/pip/tree/test_command>`_
on github.

If you want to check it out, go ahead and clone my repo and check
out the test\_command branch. Then you can simply run

::

    python pip.py install --test wsgiref

for an example package. If a package doesn't have a ``test_suite``,
then it simply doesn't run anything.

Note that if the tests fail, it doesn't impact the installation of
the package. The python community's tests aren't quite good
enough,and almost any Django package you try this on will not have
any tests. I wrote about how to
`add testing to your django package <http://ericholscher.com/blog/2009/jun/29/enable-setuppy-test-your-django-apps/>`_,
but the process is long and involved. I'm working to improve the
situation for Django and hopefully having the ability to run tests
in the package management tool will spur people to add testing
ability to their setup scripts!

`Nose <http://somethingaboutorange.com/mrl/projects/nose/0.11.1/>`_
makes this really easy, by simply adding
``test_suite = 'nose.collector'`` to your setup.py, nose will run
your tests correctly. This is the level of support that I am hoping
to implement for Django.

On a side node, I talked to
`Ian Bicking <http://blog.ianbicking.org/>`_ about this, and he
suggested writing the test command as a separate command, so you
would be able to do ``pip test wsgiref``, if it was installed. This
has some other problems, which I will talk about after I have
implemented this functionality.

I would love to hear feedback, or if anyone has ideas for improving
testing in the python and django communities. I have lots of ideas,
and I will be writing more of them up over the following weeks.


