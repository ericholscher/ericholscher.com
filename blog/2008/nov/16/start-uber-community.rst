:Date: 2008-11-16 06:34:57
A start to the uber community
=============================

Well I spent all day Saturday, and all night. Into Sunday morning
hacking on some code. Probably the most productive 24 hours of my
life. I have a couple of announcements, but in the spirit of
post-a-day, I'll spread them out over a couple days :).

The big one, is that I basically wrote an entire Django application
last night. You can check it out
`over here <http://ericholscher.com/django/>`_. It is basically an
aggregator for the Django Community Feed. I seeded the data with
the people who were on Django's Community Feed, and then I grabbed
as much of their social networking information as possible.

All of this code will be shown at some point over the next couple
of days. However, I don't have the energy to write it up quite yet.
However, please play around with the data, there's some really neat
possibility in there for something cool...

At the moment there is..


-  A river of data for every user, all of their services
-  A river of data for every user, for each service
-  A river of data for each service for all users combined
-  A river of data for all services for all users combined
-  Atom feeds for all of the above (it says RSS but I lied)
-  A permalink to every item a user has
-  A profile page, listing each users username at each network that
   I could find.

Feeds should be updating hourly, but I haven't tested them. This
model is currently pulling data, and will always have to for some
data. However, I plan to be open for pushing as much of this data
as possible. Most people have tumblelogs on their sites, so it
would be pretty easy for them to push all their data in, with more
metadata than I can apply from outside.

I'd love to hear some comments, feedback, and ideas for future
directions. With a solid OpenID server and distributed identity, I
think that we could really make something special.

**Note**: I also added the ability to combine (only) 2 tags in the
user and everyone views. See
http://ericholscher.com/django/river/friendfeed+twitter/ and
http://ericholscher.com/django/profile/Eric%20Holscher/friendfeed+twitter/

**PPS**: If your info isn't showing up in your page. Add some
rel="me" links to your profiles on your blog's homepage. Person
profiles get updated daily.


