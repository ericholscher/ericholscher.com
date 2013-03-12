:Date: 2010-11-12 19:48:34
Site upgrades
=============

Today I went ahead and flipped the switch on a couple of server
migrations I've had queued up. One of these updates is moving
`ReadTheDocs <http://readthedocs.org>`_ over to its own dedicated
server, that I built up over the week in my
`Chef Tutorials <http://ericholscher.com/tag/chef-series/>`_.

Over at RTD, you won't notice too many changes, other than it
should be FASTER! I had a bunch of sites running on an underpowered
server, and now I have it set up nicely, and running on it's own
machine, it's chugging along great.

The other change is that I migrated my blog (what you're reading!)
over to `Mingus <https://github.com/montylounge/django-mingus>`_. I
was running an oold copy of django-basic-blog, which is what Mingus
is based off, so the migration was easy. I moved it over from my
legacy Slicehost account onto my new server infrastructure that
I've been building. There is also a slight refresh of the theme of
the sight, mainly the Mingus defaults poking through on top of my
old theme.

The other bits you might notice is that my code snippets should now
be syntax highlighted. It seems pygments gets confused sometimes,
but it's better than it was.

Please report any bugs that you see on either of the sites above to
me on Twitter, or here in the comments. Thanks!


