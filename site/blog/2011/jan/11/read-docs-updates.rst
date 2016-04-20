.. post:: 2011-01-11 02:00:00

Read the Docs Updates
=====================

Documentation writing will always be hard work. It's a much
different mind-set than programming, and people that write good
code might not necessarily write good docs. However, this is a
known issue, and something that can't really be solved.

What you can do is make it easier to write documentation. Every
step along the way that you can give yourself an excuse to not
write documentation is another undocumented open source project.

Luke Plant has a
`great post <http://lukeplant.me.uk/blog/posts/docs-or-it-doesnt-exist/>`_
up about how important documentation is, and I completely agree. I
imagine a lot of the people using Django are using it because of
the documentation. I think as members of the Django community, we
need to build a culture of documentation within the greater Python
world. Python does tend to have better documentation than a lot of
languages, but it's still not nearly what it could be.

`Read the Docs <http://readthedocs.org>`_ exists to make it easier
to host your Sphinx documentation. Over the weekend,
`Bobby <http://bobbygrace.info/>`_,
`Jonas <https://github.com/ojii>`_, and I added a bunch of new
features to the site. I think it's getting to the point where there
isn't an easier or better way to host the documentation for your
Django project, and we're only going to keep improving it!

A different
`Eric <http://www.automation-excellence.com/team/eric-pierce>`_
added a really nice
`Getting Started <http://readthedocs.org/docs/read-the-docs/latest/getting_started.html>`_
guide for RTD, that shows how easy it is to get your projects
hosted with us.

Anyway, on to the new features that we added.

New Features
------------

Versions
--------

Versions of projects are easily one of the biggest requested
features on the site. For a long time we just supported building
the latest versions of your documentation. Now we support versions
of your documentation that are tagged in your VCS (hg/git only).

A lot of larger projects need versioning because they support one
or two versions, as well as developing in the trunk. Django was the
main project we were thinking of, but some other projects have put
this to good use. A couple of examples are:


-  `Django's latest stable build <http://readthedocs.org/docs/django/1.2.4/>`_
-  `Fabric 0.9.3 <http://readthedocs.org/docs/fabric/0.9.3/>`_,
-  `django-admin-tools's awesome integration <http://django-admin-tools.readthedocs.org/>`_
   that has all it's versions hosted with us.

PDF Support
-----------

Sphinx has interesting support for PDF generation through Latex. In
my testing it was pretty unreliable, but I was able to rangle it
into working well enough to expose in the UI. So now almost every
project will have a "Download PDF" button. This code has version
support as well, so we can offer PDFs of certain versions.


-  `Django's trunk documentation PDF <http://media.readthedocs.org/pdf/django/latest/django.pdf>`_
-  `Django CMS 2.1.0-rc2 PDF <http://media.readthedocs.org/pdf/django-cms/2.1.0.rc2/django-cms.pdf>`_
-  `Varnish trunk PDF <http://media.readthedocs.org/pdf/varnish/latest/varnish.pdf>`_

Another interesting part of this feature is that this building code
has been abstracted out, so we can support epub, plain text, and
all the other Sphinx output formats that people want.

Badges on the project pages
---------------------------

We killed the RTD header on hosted documentation pages in favor of
a Badge in the lower right hand corner. The header clashed with a
lot of the themes, and the badge is nice because it gives us a
place to put functionality that is always visible, but is obviously
not part of the hosted documentation. We want to build some more
functionality into the badge, like switching between versions and
linking back to the project's RTD page, once we build a good UI for
it.

Sponsorship
-----------

`Revsys <http://www.revsys.com/>`_ has agreed to sponsor the
hosting costs for RTD. Jacob Kaplan-Moss has always been a big
proponent of documentation, and I'm glad that he and Frank Wiles
are helping us keep Read the Docs around and get better. We tried
to make the sponsorship subtle and not intrusive, so please let me
know if it bothers you and we can try and figure something out.

Conclusion
----------

I think that these features are really starting to make RTD a
compelling platform for hosting your documentation. We are planning
more awesome features that will make RTD even better. I'm really
excited about the project and I hope that you either host your docs
with us, or find docs that we host useful.


