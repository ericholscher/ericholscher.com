:Date: 2008-11-06 11:01:01

Making a Django Uber-Community
==============================

My workload at work is about to get a lot less critical and time
consuming, so I was looking for a project to start on. I am really
interested in the social aspects of the web, and below I will
outline an idea that I think will be my next project.

At Djangocon there was talk by Adrian and Jacob in their Future of
Django talk about having a common identity for a person across all
Django sites. I think that this would be a really interesting thing
to work on, and make all of our Django sites much more
approachable. So in this post I'm going to lay out what I think
this would look like, how it would likely be done, and then
hopefully get some other people that are interested in it to help
me brainstorm. There is a
`ticket <http://code.djangoproject.com/ticket/8941>`_ open about it
currently.

Information Aggregation
~~~~~~~~~~~~~~~~~~~~~~~

So first off, we need to figure out what this is going to look
like. I imagine there being a central site that would organize all
of our Django related activity. The best option at the moment is
`Django People <http://djangopeople.net>`_, because it already has
a lot of that data. I talked to
`Simon <http://simonwillison.net/>`_ at Djangocon about his plans
for Django People v2, and it sounds like this is the direction he
was wanting to go. So Django People could serve as a personal
aggregator for people. I view Django People as kind of the "Profile
Page" of a person in the realm of Django. The main page could also
function as a kind of "Life stream" of the project, so people could
see what is going on *Right now*. I think a killer feature would be
to have people be able to join into groups, based on projects, and
have a life stream for that project. This would give people an idea
of how active a project is, how many people use and develop it, and
other interesting information that weighs into whether we decide to
use a project. Simon in his scary brilliant way already has most of
this information on the site. We just need to build a way to pull
information that we care about in, and display it well.

Then we need some kind of large aggregator of content from all of
the people in Django. I think that
`This week in Django <http://thisweekindjango.com>`_ is the place
to do that. The Django Community Aggregator on the official Django
site is lacking. I think this functionality could be pushed off to
TWID. I think that this aggregation site would replace the
aggregation of blog posts. It would hopefully support tagging,
syndicated comments, language preferences, and other thing. I have
talked to the TWID guys about doing this, and they said it sounded
like a great idea.

I view these 2 sites as the foundation for what I hope to build.
Then the question is, what other sites do we include in this
'django information stream'? I'm going to list the ones that I
think have relevant information, and I would love to have
suggestions for other sites that would provide a service.

Sites to include
~~~~~~~~~~~~~~~~


-  `Django Plugables <http://djangoplugables.com/>`_ - This site is
   a directory of Django reusable apps. It is a great resource, and
   better than searching Google Code for 'django-'. Now that projects
   are getting hosted on Github, Bitbucket, Google Code, Pypi, and
   others, this aggregator of projects is useful. We could bring in
   data about what projects a person owns. The site currently supports
   handling commits, and it would be really neat to have able to pull
   in all of the commits to a project, as that is the big thing that
   this is all about, code.
-  `Django Snippets <http://www.djangosnippets.org/>`_ - This is a
   great site for Django. It allows people to submit snippets of
   useful code for others. We could bring in data about their posts
   and tags.
-  `Django Sites <http://djangosites.org/>`_ - This is a site that
   lists all of the sites that are made in django. We could pull in
   the Django Sites that people have made. We could also use this data
   to determine what host each site uses, and have a tally of hosts of
   Django web apps.
-  `Django Gigs <http://djangogigs.com>`_ - The place to look for
   Django work. Pull in people looking for work, and people with job
   postings.
-  Other non-django sites - We could also pull in data from popular
   sites about Django. Think the Django popular section of Delicious,
   Reddit Django subsection, Twitter Search for Django, etc.

Ponies
======

Luckily in this day and age, most of the data we want is available
in RSS feeds. For other things, there are APIs available. Luckily,
most of the owners of the sites are members of the community, and
I'm hoping they would be willing to have the information
aggregated. I don't think that there is much of a technical
challenge behind this, it is mostly just social and getting people
to push their data in suitable formats.

I think it would be interesting to talk about
`microformats <http://microformats.org/>`_, and other ways of
having the data on the public sites be available to be pulled. I
think it would also be interesting to have
`OpenID <http://openid.net/>`_ enabled on all of the sites (Django
people already has it). This would allow you to have a kind of
floating profile. If a layer was built on top of this (white listed
information providers?), you could edit your information on one
site, and it would be sent to all the others in the inner circle.

This is mainly just a braindump, but I am willing to take the lead
on this project and get people talking. The code would be released
open source and I think we could even make it into a series of
reusable apps (and maybe APIs) that could be extended to other
communities. I think we could create a best of breed/proof of
concept implementation of a community linked shared profile.

Using OAuth to share the information across the sites, and as
authentication for that and more is also another thing that I think
would be possible. I haven't implemented anything like this before,
so I don't know if it's the correct technology.

There is a lot of possibility for this project, and I am really
excited to get started on it. This is just mainly a feeler to see
who would be interested in participating, and to get the ball
rolling. I'd love to hear people's comments and criticisms.


