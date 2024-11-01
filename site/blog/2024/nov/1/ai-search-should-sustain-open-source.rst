.. post:: Nov 1, 2024
   :tags: open-source, sustainability, ai, python
   :category: sustainability

AI search should sustain open source, not just index it
=======================================================

Open source funding has been a long standing issue,
and something that I have been working on for almost 15 years now.
Historically the sustainability model that has worked the best is:

* Publish open source and get a lot of users
* Put advertising on your website, docs, and other web properties
* Let Google index it for free
* Have Google send traffic, which is monetized by `(ethical) <https://www.ethicalads.io/advertising-vision/>`_ ads

This is obviously not a model that works for many open source projects,
and requires large scale to work.
`Funding open source with advertising <https://www.ericholscher.com/blog/2016/aug/31/funding-oss-marketing-money/>`_ is a model that aligns incentives well,
but we need to find additional revenue streams to make more projects sustainable.

AI search: paying for content
-----------------------------

There are moral issues with the creation of LLM models and content licensing,
but a recent development has been `OpenAI signing content deals with major news publishers <https://www.theverge.com/2024/5/29/24167072/openai-content-copyright-vox-media-the-atlantic>`_
This appears to be so that they can include the results in their AI search engine.

There is a strong argument that AI companies should do similar deals to be able to search and index the content of open source projects.
Given that coding and knowledge of software is one of the most common uses of AI so far,
it seems that up to date knowledge of software is a valuable asset.

**There is a strong incentive for AI companies to have up to date and canonical knowledge of the software you are using.**

Current open source licenses mean that these companies could just train on the software and not pay for it.
This is what they are currently doing,
and with somewhat firmer legal standing than training on other copyrighted works that aren't openly licensed.
But there seems like an opportunity for them to pay for the content,
similar to what they are doing with news publishing.

There is a risk that AI training could incentivize people and companies to not open source their code,
or to license their docs in a way that is not open.
This would force a conversation around licensing them in a similar fashion to the news publishers.

I'd really like to see AI companies creative more incentive for open source,
not less.

AI companies need developer good will and open source code
----------------------------------------------------------

A lot of open source programmers didn't understand that training AI models would be a major use of their code when they chose their license.
**This could lead to a longer term reduction in the amount of open source,
and slow down the overall progress of the software industry.**
I argued a while back of the `importance of open source for VC and startups <https://www.ericholscher.com/blog/2018/mar/9/one-percent-for-open-source/>`_,
and this is very much true for AI companies as well.

Putting some of the AI gold rush money into open source would achieve two important goals:

* Increase the standing of the AI companies in the tech community, where many people love their products, but are skeptical of the usage of IP is foundational to their business model.
* Increase the likelihood that more open source software is created, which sustains the ability of the models to be trained into the future.

Outcomes of large structural changes in industry are hard to predict,
but there need to be new incentives for people to create open source,
otherwise we risk the foundations that the modern software industry is built on.

Let's make more open source projects sustainable
------------------------------------------------

I would love to talk with any of the major AI companies about a licensing deal for some or all of Read the Docs content.
We have a lot of documentation for many open source projects related to AI,
and it would be great to have a licensing deal that would allow us to pass along some of the revenue to the projects that we host documentation for.

We have done some testing of this with advertising,
but it required a lot of traffic for any project to get real revenue.
If we can find multiple revenue streams for open source projects,
it would lower the size of project that would become sustainable.

This could enable a model that looks like:

* Publish open source, write great docs, and get some users
* AI companies pay for this content to be able to search it and use it in their models
* AI models use this content to be able to provide better suggestions
* AI search drives traffic to your site, which still monetizes with ads

This would be a more sustainable model for open source projects,
and importantly,
continue having a strong incentive to open source software into the future.
