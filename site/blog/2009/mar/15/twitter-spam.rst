:Date: 2009-03-15 19:27:41

Twitter Spam
============

I keep hearing people talking about how twitter is going to be over
run with spam now that it is becoming mainstream. I really don't
understand this viewpoint, and will take time here to outline what
they could be talking about, and what can be done.

This is in reply to
http://www.twine.com/item/123c9051b-g8/can-twitter-survive-what-is-about-to-happen-to-it
specifically, but these ideas have been mentioned over and over.

Short Version:
**We need to stop worrying about spam on twitter, and start worrying about all the cool stuff we can make.**

Kinds of Spam
~~~~~~~~~~~~~

"Hypertweeting"
'''''''''''''''

A person you are following is tweeting too much? How is that spam?
Simply unfollow them. This is one of the big ones I don't
understand people complaining about. It's OPT IN to follow people;
if you don't like what they say, unfollow them!

Hashtag Spam
''''''''''''

The current implementation of hashtag spam is indeed a problem,
because it is a publish and not a follow model. So anyone can
include a #hashtag and it will get picked up by a hashtag
aggregator. This is the common problem of broadcast mediums. It can
be solved filtering hashtags to only certain users, or some other
kind of grouping concept. (A twitter account that retweets a
hashtag only from the people it follows, for example). You could
also do the filtering on the web end, showing only hashtags from
user X and Y.

This seems like a problem that could be solved by the hashtag
aggregators. Currently they are just dumb aggregators, and adding
relevancy would probably be easy. This also screams out as an area
where
`Bayesian Filtering <http://en.wikipedia.org/wiki/Bayesian_spam_filtering>`_
would be useful, since you have a tag that is presumably about a
topic.

@reply Spam
'''''''''''

This is legitimate. If a spammer gets on twitter and @replies your
account, it will show up in your timeline. However, that spammer
can only @reply 1 person a minute, and that kind of activity should
be really easy for twitter to take care of. Alternatively, twitter
could implement an option where you only receive @replies from
people that you follow (like the settings to see their @replies to
other people). This issue can also be solved in a client by
separating @replies you get from people you follow, and those that
you don't.

All in all, this is not a very worrisome method of spamming, and if
it became used, it would statistically almost never happen to you.

Notification Overload
'''''''''''''''''''''

Again, this is the same as the "Hypertweeting argument". I follow
`@slicehoststatus <http://twitter.com/slicehoststatus>`_ because it
is just updates about my connectivity. They have a @slicehost
account that is more customer service oriented that I don't care
about. Services will have logical separation between their feeds or
they won't be used.

Solutions
~~~~~~~~~

The post does mention some good solutions to the problem. I will
address my thoughts on those here as well.

Number of Followers as a Filter.
''''''''''''''''''''''''''''''''

This seems likely to be gamed, and a trivial filter. This might be
useful when combined with other metrics, such as how long a user as
been on the site, how many people they are following (and have
followed!). This is where the idea of metadata being important
comes in.

Re-Tweeting Activity as a Filter.
'''''''''''''''''''''''''''''''''

Perhaps, but this needs to be formalized. I would really like
Twitter to formalize RT's so that I can filter them out, because I
find very little value in them personally. Twitter already has
functionality in it (liking tweets) that seems like a more logical
choice to use.

Social Network Analysis as a Filter.
''''''''''''''''''''''''''''''''''''

I love the social graph, so I'm a fan of this one. This would be a
very resource heavy way of validating anything, and the whole
premise of the spam argument is that twitter is growing really
fast. I don't think this is a viable option, at least not when
applied to every message. There is a lot of interesting data to be
gleaned from the social graph, however that is another post.

Metadata for Filtering.
'''''''''''''''''''''''

He makes a good point that metadata is what is needed. It will be
really hard to do these calculations outside of twitter (especially
as it grows, it will be hard internally). I really think that the
spam problem is something that is a non starter, and twitter will
work just fine without any more measure of spam protection. The
metadata will be really interesting for a lot of other
applications.

Conclusion
~~~~~~~~~~

I have yet to see a real post that has made me think that twitter
will have a spam problem. The opt-in subscription method is really
genius, and makes spam almost impossible. The model of twitter will
stay spam free (I will get content from people I follow). External
services (search and aggregators) will suffer from spam problems,
until they get better (spam) filtering.

I think the real problem of twitter is how to find interesting
people to follow, and not how to remove spam. This is where the
problem of spam and filtering really come into play. Starting with
a network of people you know, and branching from there is how
twitter will work. The social graph is really interesting in that
realm.

A lot of the conversation above leads itself into other really
interesting areas of data analysis. Stopping spam is easy, let's go
data mining :)


