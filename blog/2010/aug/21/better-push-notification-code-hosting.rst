:Date: 2010-08-21 13:00:00
A better webhook for code hosting
=================================

I have written a couple of different services that have needed to
be required when your repository has had code committed to it. The
normal path of getting this to happen is to ask your users to add
your special URL to their list of post-commit hooks for their
repository. However, once you have 3 or 4 or 10 services that need
to do this, it becomes cumbersome.
**If I am a user that has 5 repos and I want to use 5 services, this is 25 times that I need to copy/paste some URLs into a form on a website.**

I think that a publish subscribe model is better here, because that
way the end user doesn't need to constantly be caring about who is
listening to their commits. I think that
`Pub Sub Hub Bub <http://code.google.com/p/pubsubhubbub/>`_ sounds
like it does what I want. However, I think it should be baked into
the tools.

I am imagining an opt-in service for your repository (and other
things), that gets pushed to when a user commits, and I can
subscribe to. So an example workflow would be


-  User adds their repository to the PSHB or whatever service
   (push.github.com/eric/my\_repo)
-  I POST to the Hub with my URL I want to be pushed to on commit
-  When a User commits, github pings the PSHB Hub, which pushs the
   commits to anyone listening.

This allows my service to listen in to your repositories updates
without having to force you to go through a bunch of hassle. This
just feels like a better fit for the current webhook model that we
have.

I think that this is what PSHB does, but it is more focuses on
RSS/ATOM, instead of just being a replication hub for JSON data. I
assume that PSHB could be shoehorned into this task, and it would
make the atmosphere of apps around code a lot easier to write.

As a side note, it would be pretty awesome if this same service
allowed bitbucket, github, google code, and launchpad to post data
into it, but sanitized it so the listener on the other side only
had to support one format of data.

**Edit**: Looks like Superfeedr has
`already done this <http://github.superfeedr.com/>`_.


