.. post:: 2008-11-02 12:05:11

Pycon proposal
==============

Having a code base that is not tested is a scary thing for a
developer. The larger your code grows, the scarier it becomes to
make even seemingly trivial changes to your code. A test suite
gives you a guarantee that your code is running the same way before
and after a change. This is invaluable as your code grows large,
and interactions between components becomes harder to manage.

In this talk I will present this idea, and present the tools that
you need to be able to accomplish some of these goals in Django.
It's a well known fact that a lot of code bases have 0 tests for
them. With an untested code base, it is a daunting goal to write
tests for the entire thing. Being able to attain some kind of
base-line testing is incredibly valuable. The achievement of this
baseline using automated tools will be the basis for my talk.

A lot of this talk is about presenting the ideas above. I think
they are useful to think about for a lot of people trying to get a
handle on their code base. The Django applications that I have
written are a kind of proof of concept, that you can derive value
from these methods. They are still very early in development, and
there are a lot of interesting ways to go with them.

I will talk about testmaker/viewmaker and testmaker/ttagmaker. They
are pieces of code that automatically create a basic test suite for
your view code, and template tag code, respectively. They implement
the ideas mentioned above, in a naive and very simple fashion.
There value that is harnessed in such a naïve and simple
implementation tells me that there is a lot more power to this idea
than I have currently thought of. The basis of this presentation is
to get those ideas out to people, and to start a discussion about
this approach.

Outline: 5 min: Present the problem of an untested code base 5 min:
Talk about how achieving a base-line testing suite for this code is
important. 5 min: Present the tools for django that allow you to do
this. 3-5 min: Demo the tools in question 3-5 min: Talk about the
downsides of this method, and what could be made better. 8-10 min:
questions/discussion. (Hopefully a lot of suggestions for why this
is a bad idea, or what could be better.)


