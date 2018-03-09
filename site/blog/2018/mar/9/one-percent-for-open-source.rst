.. post:: Mar 9, 2018
   :tags: python, opensource, sustainability, sustain

One Percent for Open Source
===========================

The open source ecosystem is the `most valuable part`_ of the software industry today.
All software companies today use open source software.
From the programming languages to the web frameworks,
the operating system to the cryptography,
everyone is using open source.

Open source software is creating billions of dollars in value for companies and Venture Capitalists,
but it has a `funding problem`_ for itself.
There are not many ways for open source projects to capture the value that they create,
while being available for free and providing the fertile ecosystem that companies are built on today.

There are many `warning signs`_ that open source is an ecosystem in danger.
Many people doing this work are `burning out`_,
`giving up`_,
or just never getting involved in the first place.
We need to improve the sustainability of open source to protect the valuable ecosystem that we have built.

We need a new funding model for open source.

.. _most valuable part: https://medium.com/@nayafia/open-source-was-worth-at-least-143m-of-instagram-s-1b-acquisition-808bb85e4681
.. _funding problem: https://www.fordfoundation.org/library/reports-and-studies/roads-and-bridges-the-unseen-labor-behind-our-digital-infrastructure/
.. _warning signs: https://gist.github.com/jdorfman/099954cffd018d0ca2037a1a0f86026f
.. _giving up: https://www.drmaciver.com/2015/08/throwing-in-the-towel/
.. _burning out: https://thenewstack.io/darker-side-open-source/

Funding Open Source
-------------------

I'd like to propose an idea:

    A program called **1% for open source**: where companies agree to invest 1% of their funding round or yearly profits into the open source software that they use.

This is a win/win/win:

* **Venture Capitalists (VC's)** invest in the open source ecosystem that makes companies *much cheaper to build*. It's also *really good marketing* for the VC firms, to show they are investing in the common tools we all rely on.
* **Companies** invest in the tools that they use to *ensure continued development and support*. The companies can also use their support of open source to make hiring good developers easier.
* **Open source projects** are able to *fund project management and maintenance* that is required to make them sustainable for the long term. This continues the *force multiplier* that open source has given to the software industry as a whole.

Why is this a good solution?
----------------------------

The biggest reason is because all parties involved benefit from open source.
Secondly,
having a concrete point in time also makes it much easier to define when the money should be invested.

My focus on this program is to **increase the total revenue that all open source projects get**.
Monetary investment is required to make a real dent in this problem. 
A lot of places have "Open Source Fridays" and "20% time",
but those programs are the first to be cut when a company has issues.
Investing in open source as a lump sum during funding rounds makes sure the investment up front,
where it can't be removed as an ongoing program.

How should we implement it?
---------------------------

The company should invest 1% of the money into the open source projects that they use. There are many different ways this could be implemented.
A few of my ideas are:

* Companies create a list of the OSS projects they use, using tools like http://libraries.io/, and then give money to the 10 largest projects that have a way to accept money. This could be done during the license compliance phase of the investment process.
* There could be a new non-profit foundation created, which gets all the donations and then has established criteria for how to reinvest the money as grants.
* You could give the money to the existing foundations that focus on the area of open source that is most valuable to you 

Making the execution of the investment standard is an important part of making this actually happen.
There should be standard processes and criteria for where your money will go,
so that it's not adding additional overhead to companies who give back.

A simple example for a Python project could be:

* You give 1% of your VC investment to the Python Software Foundation
* You run a script that looks at all the projects in your `requirements.txt` that your project depends on
* That list is cross-referenced with a list of the Python projects you use that need funding
* The top 10 projects you use that need funding, sorted by least amount received that year, are each given 10% of your investment as a sustainability grant

Prior Art
---------

I have a few sources of inspiration for this idea:

* `One Percent for the Planet`_ - They ask established companies to give 1% of their revenue to help invest in the planet. This model for sustainability of an ecosystem was my inspiration here.
* Stripe's `open source retreat`_ - where they fund projects to work on specific features.
* Mozilla's `open source support`_  - where they fund awards for projects that they use internally
* Coinbase's `open source fund`_ - which is a monthly donation program
* Segment's `open fellowship`_ - which gives 3 month fellowships, similar to Stripe

.. _One Percent for the Planet: https://www.onepercentfortheplanet.org/
.. _open source retreat: https://stripe.com/blog/open-source-retreat-2016
.. _open source support: https://wiki.mozilla.org/MOSS
.. _open source fund: https://engineering.coinbase.com/introducing-coinbase-open-source-fund-116617a1f6ec
.. _open fellowship: https://open.segment.com/fellowship

Help out
--------

I was inspired to write up my thoughts because I tweeted the idea,
and it was well received:

.. raw:: html

   <blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">We should start a movement called &quot;1% for OSS&quot;, a program where VC&#39;s and startup companies agree to invest 1% of their funding round into the infrastructure that their companies rely on. <a href="https://twitter.com/hashtag/sustain?src=hash&amp;ref_src=twsrc%5Etfw">#sustain</a> <a href="https://twitter.com/hashtag/sustainoss?src=hash&amp;ref_src=twsrc%5Etfw">#sustainoss</a></p>&mdash; Eric Holscher (@ericholscher) <a href="https://twitter.com/ericholscher/status/966845161194979328?ref_src=twsrc%5Etfw">February 23, 2018</a></blockquote>
   <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

I don't plan on actually building a new program for funding open source,
so please contact me if this is something that you'd like to actually work on!
This is a viable option for funding large amounts of open source,
but it will require a lot of work.
I'm happy to help,
but it will really take motivated people to execute on this idea and make it happen.

I see the next steps being:

* Figure out the exact process for determining who gets money from a project
* Figure out the proper entity to use (an existing non-profit, or a new one?)
* Find a willing VC or Company to do a test run
* Iterate on what you learn, establishing standard processes for the next test run
* Once you have a model that everyone is happy with, start expanding the program
