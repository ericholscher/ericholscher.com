.. post:: 2009-06-29 20:33:07

Enable setup.py test in your Django apps
========================================

Setuptools comes with a way to
`run the tests on your application <http://peak.telecommunity.com/DevCenter/setuptools#test>`_.
This allows the user of your software to download it, and run
``python setup.py test`` and check to see if the tests in your
application pass. This is really useful for distribution, because
the user doesn't need to know or care how to run your tests (nose,
django, unittest, py.test, or whatever else), and can simply see if
they pass.

To do this, you simply define a ``test_suite`` variable in the
``setup()`` function of your setup.py. This argument is a callable
that should return a test class. However, since Django has it's own
test runner, we have to point this at a simple test runner that we
construct, and allow that to run the tests. This is because we must
set a couple of environmental things, like the settings module and
PYTHONPATH.

I did this with my test\_utils project, you can see the
`commit here <http://github.com/ericholscher/django-test-utils/commit/b18893ac7230b4689f9be19ce3f8fbfd13745324>`_,
but basically I simply added this line to my setup.py:

::

    test_suite = "test_project.runtests.runtests",

Then put this in the file ``test_project/runtests``:

::

    #This file mainly exists to allow python setup.py test to work.
    import os, sys
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'
    test_dir = os.path.dirname(__file__)
    sys.path.insert(0, test_dir)
    
    from django.test.utils import get_runner
    from django.conf import settings
    
    def runtests():
        test_runner = get_runner(settings)
        failures = test_runner([], verbosity=1, interactive=True)
        sys.exit(failures)
    
    if __name__ == '__main__':
        runtests()

Note that there is a bit of path and settings hackery, this is to
enable Django to run correctly, with the test\_project in the
PYTHONPATH. However, now if you want to run the tests, you simple
do a ``python setup.py test``. You can also do a
``python runtests.py`` to have the same outcome. You could also
have the runtests function simply be a ``call_command('test')``,
but without the explicit sys.exit, setuptools complains that it
hasn't been given a TestCase back.

This has a couple drawbacks in that it simply runs the entire test
suite. You can pass in a Test Suite to setuptools, but that isn't
how the tests are organized in most Django apps. However, if you
want to run specific tests, you can still test things the regular
way through ``manage.py test``. Presumably there is a better way to
do this, but it's good to at least have a hacky way until a better
way emerges.

There is a lot of value in providing a standard interface to
running the tests on your application though. This allows the
distribution tools (pip and setuptools) to run the tests on your
application if they'd like. In the perl universe, CPAN runs the
tests on apps before installing them, and quitting if they fail. If
more people started making setup.py test work, we could hopefully
add this ability to Python's distribution tools, and make the world
a happier place with better working software.


