.. post:: 2009-01-26 21:41:26

Django Conventions Project Update
=================================

So about a month ago I
`started <http://ericholscher.com/blog/2008/dec/3/starting-django-conventions-project/>`_
a `project <http://ericholscher.com/projects/django-conventions/>`_
on my blog called the Django Conventions Project. It was an attempt
to document and record conventions that are used across the
community. Conventions are a great thing, with Python and Django
relying on them a great deal. Things like private methods being
underscored aren't enforced on a language level, but are more of a
gentleman's agreement.

I think that conventions can indeed have a lot of value, but they
are hard to discover without practice. I think that embodying this
knowledge in documentation can be extremely valuable. It proves
useful for people that are just starting to kind of establish
themselves in a code base. It is also useful for more advanced
people as a reference and to make sure they are following them. I
know that I learned about a few new ones when I started the
project.

I got around 20 comments, and people seemed really energized when I
posted last time, so I think people are genuinely interested. In
hindsight, I should have created a source repo with
`Sphinx <http://sphinx.pocoo.org/index.html>`_ at the beginning and
started accepting patches. `Brian Rosner <http://oebfare.com/>`_ is
involved in Pinax, which has these conventions and standards as a
stated goal as well. He created a
`django-reusable-apps-docs <http://github.com/brosner/django-reusable-app-docs/tree/master>`_
github project for these to live. So I went ahead and
`ported <http://github.com/ericholscher/django-reusable-app-docs/commit/abb86dbdae5490c2a22dbdc18bd63aad98bae2ea>`_
my HTML docs over to
`my fork <http://github.com/ericholscher/django-reusable-app-docs/tree/master>`_
of that project on Github.

Please feel free to branch the repo and submit patches/pull
requests back to me. Also, feel free to join the
`django-hotclub mailing list <http://groups.google.com/group/django-hotclub>`_
which was created for discussion about reusable apps. The
#django-hotclub or #pinax channel on Freenode is also a good place
to find us and talk about reusable apps in real time.

Brian has a mirror of his repo updating every 10 minutes to
http://appdocs.oebfare.com/.. I have a
`mirror of my github repo <http://ericholscher.com/projects/reusable-app-docs/>`_
up on my site as well, updating hourly. The eventual plan for these
docs is to make it into the Pinax or Django Official documentation.
I think that they can probably go into the Pinax documentation once
we clean them up a little bit, and I don't know if this is quite
something that belongs in Django docs. So I invite everyone to come
discuss what the conventions should be, contribute your own, and
lets try and make some great reusable apps.


