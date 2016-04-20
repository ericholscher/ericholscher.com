.. post:: 2009-06-01 10:54:46

Django Dash: Announcing PyPants
===============================

First off, I'd like to thank
`Daniel Lindsley <http://www.toastdriven.com/>`_ for putting
together the `Django Dash <http://alt.djangodash.com>`_. I know it
was a lot of work, but it was an amazingly great time! I think
everyone that participated had fun, and I am looking forward to
doing it next year.

Our Project
-----------

`Nathan <http://playgroundblues.com>`_,
`Travis <http://traviscline.com>`_ and I were on a team for the
dash this year. At EuroDjangoCon there was talk about how neat it
would be for a site to be able to run tests against your code on
every commit. We took this idea and ran with it, creating a website
called `Pypants <http://pypants.org>`_. It is named after
`CPANTS <http://cpants.perl.org/index.html>`_, the CPAN Testing
Service.

As you can see, we allow you to input a project that is on
`Pypi <http://pypi.python.org>`_, and it will pull down all the
versions available and run analysis on them. We also support Git
repositories, where you give it a name and a git-compatible url,
and it will pull down your repo and analyze your last 10 commits.

The future
~~~~~~~~~~

Yes, we will be adding support for svn and hg, and for analyzing
full repositories.

The site is very barebones at the moment. There is a lot of
functionality on the back end that isn't exposed yet, and a lot of
views on the data that we think are interesting. We also think that
having a flexible API that allows you to report, create, and
interact with metrics on the site would be a big win.

We are considering the question of open sourcing the site. We are
going to clean the code up a bunch more and add some features
first. We will probably open source it to allow for the community
to make the site better, and turn it into a community resource. I
think allowing people to create new Indexes that some projects are
graded against would be a really big win. Also having categories
(like django apps) that have their own subset of custom indexes
would be a really interesting feature as well.

Other projects
--------------

There are a bunch of other projects of mention that were created in
the Dash. I won't list all of them (since there were over 50), but
there is a `gist <http://gist.github.com/121408>`_ that links to
all of the ones that are live. Pretty impressive list!


