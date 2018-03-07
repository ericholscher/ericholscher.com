.. post::
   :tags: python, opensource, sustainability, sustain

One Percent for Open Source
===========================

The open source ecosystem is the `most valuable part`_ of the software industry today.
All of the companies and technologies that we build today are enabled by open source software.
From the programming languages to the web frameworks,
the operating system to the cryptography,
all of it is open source.

Open source has a `funding problem`_.
There are many `warning signs`_ that open source is an ecosystem in danger.

Open source is maintained for "free" by people all over the world,
enabled by the internet (which is also built on open source).
Many people doing this work are burning out,
giving up,
or just never standing in the first place.
We need to improve the sustainability of open source in order to protect the valuable ecosystem that we have built,
and help it grow in the future.

Funding Open Source
-------------------

I'd like to propose an idea:

    A program called **1% for open source**: A program where Venture Capitalist's and startup companies agree to invest 1% of their funding round into the open source software that they use. 

I believe that this is a win/win/win for all involved:

* **Venture Capitalists** invest in the open source ecosystem that makes companies *much cheaper to build*. It's also *really good marketing* for the VC firms, to show they are investing in the common tools we all rely on.
* **Startups** invest in the tools that they use, to *ensure continued support and maintenance*, and remove risk from their future. It will also make *hiring developers* much easier for the companies, because developers love companies that invest in open source.
* **Open source projects** are able to *fund project management and maintenance* that is required to make them sustainable for the long term. This continues the *force multiplier* that open source has given to the software industry as a whole.

Why Venture Capital payments?
-----------------------------

The biggest reason is because all parties involved benefit from open source.
Secondly,
having a concrete point in time also makes it much easier to define when the money should be invested.
Third,
money is already changing hands during an investment,
so having 1% that money to go open source is easy to communicate.

I also think monetary investment is required to make a real dent in this problem. 
A lot of places have things like "Open Source Fridays" and "20% time",
but those programs are the first to be cut when a company has issues.
Investing in open source as a lump sum during funding rounds makes sure the investment up front,
where it can't be removed as an ongoing program.

How should we implement it?
---------------------------

The startup who has gotten the investment should invest 1% of the money from the VC firm into the open source projects that they use.

There are many different ways this could be implemented as a lower level.
A few of my ideas are:

* Startup companies create a list of the OSS projects they use, using tools like http://libraries.io/, and then give money to the 10 largest projects that have a way to accept money. This could be done during the license compliance phase of the investment process.
* There could be a new non-profit foundation created, which gets all the donations and then has established criteria for how to reinvest the money as grants.
* You could give the money to the existing foundations that focus on the area of open source that is most valuable to you 

I think making the execution of the investment standard is an important part of making this actually happen.
There should be standard processes and criteria for where your money will go,
so that it's not adding additional overhead to your funding round.

A simple example for a Python project could be:

* You run a script that looks at all the projects in your `requirements.txt` that your project depends on
* You give 1% of your Venture Capital investment to the Python Software Foundation
* That list is cross-referenced with a list of the Python projects you use that need funding
* The top 10 projects you use that need funding are each given 10% of your investment as a sustainability grant

Prior Art
---------

There have been a few examples of companies investing in open source in an ad hoc manner:

* `One Percent for the Planet`_ - I got the idea for a 1% investment from this wonderful non-profit.
* Stripe's `open source retreat`_ - where they fund projects to work on specific features.
* Mozilla's `open source support`_  - where they fund awards, including for projects that they specifically work on.

These are good examples,
but we need many more companies to be doing similar investment in order to make progress.

Help out
--------

I was inspired to write up my thoughts because I tweeted the idea,
and it was well received:

.. raw:: html

   <blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">We should start a movement called &quot;1% for OSS&quot;, a program where VC&#39;s and startup companies agree to invest 1% of their funding round into the infrastructure that their companies rely on. <a href="https://twitter.com/hashtag/sustain?src=hash&amp;ref_src=twsrc%5Etfw">#sustain</a> <a href="https://twitter.com/hashtag/sustainoss?src=hash&amp;ref_src=twsrc%5Etfw">#sustainoss</a></p>&mdash; Eric Holscher (@ericholscher) <a href="https://twitter.com/ericholscher/status/966845161194979328?ref_src=twsrc%5Etfw">February 23, 2018</a></blockquote>
   <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

I don't plan on actually building a new program for funding open source,
so please contact me if this is something that you'd like to actually work on!
I think something like this is a viable option for funding large amounts of open source,
but it will require a lot of work to get it there.

.. _most valuable part: https://medium.com/@nayafia/open-source-was-worth-at-least-143m-of-instagram-s-1b-acquisition-808bb85e4681
.. _funding problem: https://www.fordfoundation.org/library/reports-and-studies/roads-and-bridges-the-unseen-labor-behind-our-digital-infrastructure/
.. _warning signs: https://gist.github.com/jdorfman/099954cffd018d0ca2037a1a0f86026f

.. _One Percent for the Planet: https://www.onepercentfortheplanet.org/
.. _open source retreat: https://stripe.com/blog/open-source-retreat-2016
.. _open source support: https://wiki.mozilla.org/MOSS


