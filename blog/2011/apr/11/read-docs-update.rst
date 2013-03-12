:Date: 2011-04-11 19:22:37

Read the Docs Update 
=====================

It's been a while since I last talked about
`Read the Docs <http://readthedocs.org>`_, and there has been a lot
of activity. This is an update on the latest and greatest new
features.

PSF Funding
-----------

The biggest news that has happened is that we have been given a
grant from the Python Software Foundation to help host the site.
Thanks PSF! They have
`blogged about it <http://pyfound.blogspot.com/2011/03/psf-funds-readthedocsorg.html>`_,
and I am grateful that they have given us support. With the funds
they have offered, we have been able to make Read the Docs a lot
faster, and more robust. I will outline some of the changes below.

This also means we won't be going away any time soon!

New Theme
---------

We have a fancy
`new theme <http://read-the-docs.readthedocs.org/en/latest/getting_started.html>`_
for documentation on Read the Docs! If you have the 'default' theme
for your project, it will show up on the build of your docs on the
site. I think it is pretty great, thanks to the designers who spent
their time making it awesome. A really great feature is that the
**new theme is mobile ready**. Go ahead and view a project using it
on your phone, or make your browser smaller and you will see the
fanciness. Having a custom theme will give us a base to build lots
of other neat features on top of.

Better architecture
-------------------

We had some connectivity trouble in between our servers a while
back, and this prompted me to make the site respond better to these
conditions. Every time you view documentation on a subdomain of
readthedocs.org, your request will never hit Django. So all of
these requests will work without a database. We have also added a
second application server with a load balance in front, which means
that one of the app servers could go away and your documentation
would still get served.

That leaves our load balancer as the main single point of failure
at the moment. We're using Varnish for the load balancer, and we've
implemented strong caching of data. Varnish will cache your docs
for up to a week, and it will be actively purged when you rebuild
your docs. This means that your docs will usually be served out of
memory, and without dependence on any other server but that one. We
have plans to elininate Varnish as a single POF, and then it would
only be our hosting provider that would be a single point of
failure (famous last words).

Intersphinx support
-------------------

`Intersphinx <http://sphinx.readthedocs.org/en/latest/ext/intersphinx.html#sphinx.ext.intersphinx>`_
is an awesome feature of Sphinx that allows you to reference remote
sphinx documentation easily.
`RTD now supports it <http://read-the-docs.readthedocs.org/en/latest/features.html#intersphinx-support>`_
for every project that we host.

Improved rtfd.org
-----------------

I've always had big ideas for rtfd.org, since it can act as a
short-url for things. *projectname*.rtfd.org has always redirects
to the projects docs, but now we have something a lot better.
Inspired by Jacob Kaplan-Moss and his work on django.me, we now
support human-edited deep-linking within documentation hosted on
RTD.

Taking another page from Jacob's book, we seeded the index of our
projects with their Intersphinx data, so a lot of references will
automatically work. This works best with API reference docs, but
anything people have put links to in their documentation should
have been picked up. A couple of examples:


-  `http://pip.rtfd.org/git <http://pip.rtfd.org/git>`_
-  `http://celery.rtfd.org/Task <http://celery.rtfd.org/Task>`_
-  `http://sqlalchemy.rtfd.org/relationship <http://sqlalchemy.rtfd.org/relationship>`_

If you go to a non-existent link on rtfd.org, you will be prompted
to enter a suggested URL. This will help build the data, and make
it more useful for everyone.

`rtd <https://github.com/ericholscher/rtd>`_ command line utility
-----------------------------------------------------------------

RTD has had an
`API <http://read-the-docs.readthedocs.org/en/latest/api.html>`_
for a while now, and with the addition of the support for rtfd.org,
I thought it would be neat to make it easier to access docs from
the command line. With a simple ``pip install rtd``, you will get
an rtd utility that will open docs on RTD. It supports 2 arguments,
the first being a project name, and the second being a slug to
append for the rtfd.org functionality. So like the example above:

::

    -> rtd pip
    Pip Installs Packages. 
    Opening browser to http://pip.rtfd.org/
    -> rtd celery Task
    Distributed task queue
    Opening browser to http://celery.rtfd.org/Task

It hits the RTD API to see if the project is on the site, and only
opens your browser if it doesn't exist. I hope that in the future
we'll make it easy to upload a project from the shell, and more.

More docs
---------

Since we are a documentation site, we've always had documentation.
I've been adding more as time has gone on, and most of the features
I'll be talking about today are
`already documented <http://read-the-docs.readthedocs.org/en/latest/features.html>`_.
I also broke the documentation up into sections for users of the
site, and developers on the codebase, so it should be easier to
find for everyone to find what they are looking for.

Conclusion
----------

I think that RTD can be doing a lot more to help out the community
with regards to documentation. I'll write another post about that
soon. But if you are interested in helping out with the effort, all
of the code is
`open source <https://github.com/rtfd/readthedocs.org>`_ and we
love people to contribute. Feel free to jump in #readthedocs on
Freenode as well, if you have any questions or thoughts.


