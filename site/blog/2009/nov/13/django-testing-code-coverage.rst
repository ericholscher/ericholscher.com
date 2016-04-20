.. post:: 2009-11-13 19:01:09

Django Testing Code Coverage
============================

As part of the summer of code 2009, Django test coverage has been
developed. I mentored `Kevin Kusabik <http://kubasik.net/blog/>`_,
who developed the code. It is hopefully going to be merged in 1.2,
but there are still a few issues to be worked out in the
implementation. That said, it currently works, and provides a nice
introspective view of your code. This post will tell you how to run
coverage on your code base.

It should be noted that having code coverage is a good way to look
into your code, but doesn't guarantee that there are no bugs. Ned
Batchelder's
`Pycon talk last year <http://pycon.blip.tv/file/1947218/>`_ is a
good introduction to coverage. We are using his
`Coverage.py <http://bitbucket.org/ned/coveragepy/src/tip/coverage/>`_
module in this example to produce the coverage output in Django.

I have taken the commits from the Summer of Code and put them in a
`Branch on github <http://github.com/ericholscher/django/tree/coverage>`_.
You will want to clone this and put it on your PYTHONPATH as your
django module. If you are already using the github mirror, simply
add me as a remote and pull down the coverage branch.

::

    git remote add ericholscher git://github.com/ericholscher/django
    git fetch ericholscher
    git co -b coverage ericholscher/coverage

Once you have the code, you simple run your tests in the normal
manner. However, now have the added options of ``--coverage`` and
``--report``. If you run the test command with just ``--coverage``,
it will generate a text based coverage report. If you also specify
the ``--report`` option, it will output a HTML report in the
current directory. The HTML report is where most of the value of
coverage comes from, allowing you to see what lines were covered
and missed. Here is an example
`HTML report <http://media.ericholscher.com/django_coverage/>`_,
showing the Django source code's coverage.

One of the major problems with coverage is that it slows down
running tests by a non-trivial amount. For every instruction
executed, there must be a record made. With coverage.py 3.0, this
extension is written in C for speed, however it still noticeably
slows down test speed.

I hope that you give it a try and enjoy the results. I'll be
spending some time over the next week or 2 cleaning up the code and
trying to get it into shape for inclusion in Django.


