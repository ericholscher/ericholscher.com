:Date: 2009-03-21 12:31:29

Django on Github
================

A lot of people are developing with git these days, and
`Github <https://github.com/>`_ is a great place to put your code
while you're working on it. I haven't really seen this addressed
anywhere, but there is a decent amount of Django work happening on
Github, so I figured I would post a link to some of the notable
Django forks on Github. A lot of the feature development on Django
has been happening on Github, which is great for collaboration.

**Note**: Look under the *all branches* link to see all of a
persons branches that they have.

The *unofficial* Django Github Mirror is located at
`django/django <http://github.com/django/django/tree/master>`_.
`Jannis Leidel <http://jannisleidel.com/>`_ has this fork updating
from the Django SVN Trunk every 15 minutes, so it is a good place
to fork or watch to keep up with Django changes.

This branch is the defacto git branch, so everyone that is using it
can add each other as a remote. This makes it really nice to work
together, so it is best to make this your django git branch.

`Russell Keith-Magee <http://cecinestpasun.com/>`_ has a
`branch <http://github.com/freakboy3742/django/tree/master>`_ that
was used for the work on F expressions and Aggregates.

`Brian Rosner <http://oebfare.com>`_ has a
`place <http://github.com/brosner/django/tree/master>`_ where he
has put up some of his work on the Changelist refactor in the
admin.

Honza Krai's
`model validation branch <http://wiki.github.com/HonzaKral/django/>`_
is developed on Github as well. This is going to be one of the big
features for 1.2.

`Alex Gaynor's <http://lazypython.blogspot.com/>`_ many
`branches <http://github.com/alex/django/tree/master>`_ have a lot
of really good stuff in them. He will be participating in the push
to get Django MultiDB support into 1.2, so I imagine that branch
will be living in his github repo. The current
`admin actions <http://github.com/alex/django/tree/admin-actions>`_
branch is really interesting, and should be getting committed over
the weekend.

Watching people's work on Github is interesting, because it gives
you a view of the process behind patches before they go into trunk.
Looking at all the patches on a ticket is a similar way to achieve
this, but DVCS' make this process really neat and easy.

It should also be noted that `Bitbucket <http://bitbucket.org>`_ is
hosting a `Django Mirror <http://bitbucket.org/mirror/django/>`_ on
their servers. I would assume this is probably what most people use
for the mercurial Django clones as well.

I know there is a bunch of other neat Django Reusable App work
happening on Github. This post was mostly to point people to some
of the work happening that might otherwise be "invisible". I'm
curious where other neat Django development is happening as well,
so please feel free to mention some in the comments.


