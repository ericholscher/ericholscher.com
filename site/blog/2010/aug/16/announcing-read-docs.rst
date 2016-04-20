.. post:: 2010-08-16 19:10:00

Announcing Read The Docs
========================

This year's Django Dash just came to an end, and I'm really excited
about the project that we built. I'm sure the other teams are
feeling just as stoked, because there is an amazing amount of
awesome work that was done in the last 48 hours.

I'm really happy with the work we did, I think it is close to
production quality. `Last years project <http://pypants.org>`_
didn't even get a blog post because it was "almost done". This year
I'm putting it out there because I think it is genuinely useful and
pretty damn awesome.

Our team consisted of, besides myself,
`Charlie <http://charlesleifer.com>`_ and
`Bobby <http://bobbygrace.info/>`_ who are an amazing dev and
designer, respectively.

`Read The Docs <http://readthedocs.org>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Our Django Dash project solves a real problem in the Open Source
community I think. I have a love affair with
`Sphinx <http://sphinx.pocoo.org/>`_, and it's really started to
catch on as a cross-platform documentation tool. Our idea was to
provide hosting for people's documentation, in a central place with
nice tools built around it.

I know whenever I create a project, I have this moment where I
think about documentation, and hosting it is a problem that is hard
to solve.
**I currently have a cron job running on my server pulling my docs every 5 minutes**,
this is no way to host documentation.

We created `Read The Docs <http://readthedocs.org>`_ to solve this
problem. It will automatically build your documentation for you, if
you put in a github or bitbucket URL. You can also use it to create
Sphinx documentation on the site with some basic editing tools that
we created.

Cool Features
~~~~~~~~~~~~~

`Open Source <http://github.com/rtfd/readthedocs.org>`_
'''''''''''''''''''''''''''''''''''''''''''''''''''''''

This year's Django Dash required submissions to be open source,
which I think is great. It gets a lot of knowledge from smart
people into the world, and I think focuses the projects more on
community problems. Feel free to take a look (again, written in 48
hours, be kind)
`our source <http://github.com/rtfd/readthedocs.org>`_ and
contribute, or laugh at us :)

Build your own docs
'''''''''''''''''''

If you have a really basic project that doesn't need a whole bunch
of documentation, you can use our documentation builder to create
the docs right on our site. We will host them for you and
automatically rebuild them whenever you update them. This solves a
problem for people with simple documentation needs. My teammate
`Charlie <http://charlesleifer.com>`_ made some docs for his
`own project on the site <http://readthedocs.org/projects/coleifer/django-relationships/docs/>`_

Host existing docs
''''''''''''''''''

If you already have documentation in your project, but are hosting
it in a crappy way, let us host it for you. We will update it in
real time (see below) whenever your update it, and we have lots of
neat features planned that will make it silly not to use our
hosting. For example, here is a
`mirror of pip's docs <http://readthedocs.org/projects/jezdez/pip/docs/>`_.

Web Hooks
'''''''''

Web hooks are pretty amazing, and help to turn the web into a push
instead of pull platform. We have support for hitting a URL
whenever you commit to your project and we will try and rebuild
your docs. This only rebuilds them if something has changed, so it
is cheap on the server side. As anyone who has worked with push
knows, pushing a doc update to your repo and watching it get
updated within seconds is an awesome feeling. If you're on github,
simply put ``http://readthedocs.org/github`` as a post-commit hook
on your project. Otherwise your project detail page has your
post-commit hook on it.

Bookmarking
'''''''''''

I have a problem with Django's documentation, and it's that it is
so big, I often find a page and then forget where I was when I need
that information again. We added simple bookmarking so that you can
find pages that you were on before. Check out the
`recently bookmarked pages <http://readthedocs.org/bookmarks/>`_

View Tracking
'''''''''''''

Another feature is that we track which doc pages are viewed the
most. This is a great hueristic to what pages are important and
useful, and I think will be an interesting UI feature once we
hopefully get more and bigger projects on the site. Not
suprisingly, the project's own docs are currently
`the most viewed <http://readthedocs.org/views/>`_

Planned cool features
~~~~~~~~~~~~~~~~~~~~~

Full Text Search
''''''''''''''''

Once we have a critical mass of documentation, being able to search
across all of it, based on tags and other attributes will be a
killer feature. I'm really excited about the possiblities here, and
think this will be the first big new feature that we will
implement.

Quick browser editing
'''''''''''''''''''''

When I find a typo in your documentation, there should be a 1-click
process to be able to make an edit and send you a diff. We want to
be able to support this with a nice UI. I think it will really
increase the quality of documentation if there is a super easy way
to update and edit existing documentation from it's rendered
interface.

Mobile View
           

With we will be able to make a mobile theme that we can serve based
on user agent. This will be another killer feature to hosting your
docs on our site, because you'll get a kick ass mobile version for
free.

Future
~~~~~~

I really hope that this utility becomes used by the community,
because I think it is needed. I understand that large projects
would want to and should host their own documentation, but for the
90% of projects that are small, I think this is a great solution.


