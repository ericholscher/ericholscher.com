:Date: 2008-11-30 17:29:05

Post a day in review
====================

It's the end of the Post a day for a month. I did pretty well, but
fell off about 3 weeks in because of work. First some stats.

Post stats
----------

::

    In [4]: Post.objects.published().filter(publish__year='2008', publish__month='11').count()
    Out[4]: 23L
    
    In [10]: for post in posts:
        cont = post.body.split()
        sum += len(cont)
    
    In [13]: sum
    Out[13]: 18517
    
    In [14]: sum / 23
    Out[14]: 805

This doesn't really mean much, because it is simplistic
len(body.split()), but it shows that I have been writing a ton over
the past month. I have also gotten a ton of stuff done. I have
re-written 1 project, started another, and put out some ideas into
the community.

The above stats basically mean I posted 24 times (counting this
one), averaged 800 words a post (with code examples probably
inflating that)

I only missed my first day about 3 weeks in, and that was because
of work. I was working non-stop trying to launch our main websites
at work on Django 1.0, and just didn't have enough time (energy
really) to do anything else. For Thanksgiving I was also up
visiting family in rural Ohio for 4 days, so I didn't have an
internet connection there, which made posting hard.

Traffic stats
-------------

.. figure:: http://media.ericholscher.com/images/postaday-analytics.jpg
   :align: center
   :alt: Analytics stats
   
   Analytics stats

The day after that big spike I launched my redesign, so there are
probably around 1,000 hits missing from that. I got around 30,000
Page views and 17,000 Unique visitors.

Pros and cons of post-a-day
---------------------------

Pros
~~~~

I have certainly enjoyed doing this. It has been a neat personal
challenge, and I think that the quality of my posts hasn't really
suffered. If anything, it has stayed the same, and I have just been
posting more frequently. I had a couple of "cop out" posts (like
this one), but they never really seemed to be much less popular
than some of the ones I put some time into.

Having to do a post a day makes you do a lot more! You accomplish
so much because you need something to write about. I think that
this is probably the biggest advantage to doing post a day. You're
forced to do something interesting each and every day, which is
something that more of us should be doing.

I also think that it's interesting what kind of content you end up
writing. I have done a lot more tutorials and things like that. I
have found them to be easy to write, and really valuable for people
to use.

Cons
~~~~

You write blog posts instead of doing things! I spent a ton of time
writing instead of coding. A lot of my posts took around an hour or
more to write, so that's a lot of time spent. However, I think that
this is a good thing for the open source community, since the
amount of documentation versus code produced is really unbalanced.

I really wanted to review some major django reusable apps and write
up howto's and screencasts for them, but this proved to be really
time consuming. So doing a post a day really limits your drive to
do longer blog posts (because you have to do one again tomorrow!).

After about 2 weeks I agree with other people, where they say it
turned from being fun into a burden. Not a huge burden, but it was
enough stress (along with all my other real life stuff) that it was
annoying. I missed a bunch of days at the end for this very
reason.

Reflection
----------

I'm really glad that I did it. I broke down somewhere through, but
I still feel that I accomplished my goal of posting a lot of good
content, and getting shit done. I am so happy that the month is
over, and that Ellington is now running on Django 1.0. My life has
gotten a lot less stressful. I will be taking a lot of time off in
December, so this blog will be a bit more quiet :)

Going forward, I will try and post at least once a week, and
hopefully some more screencasts and longer form content. I think
that the kind of content that was produced during this shows what's
hard and what's not. Simple tutorials are great for things you
know, but doing the research to do a screencast (that doesn't suck)
or other kind of content like that takes a lot of time!

Hope everyone enjoyed these posts, and I'll try and keep up.


