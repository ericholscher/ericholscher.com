:Date: 2014-02-27 22:00:00

How I Judge the Quality of Documentation in 30 Seconds
======================================================

As a developer,
you develop instincts for judging quality of code.
One of my favorite interview questions is:

    When you look at a project's code for the first time,
    what are the things you look for?

I think this question is telling.
Every person has different priorities,
and this is a great way to get at them.

I have developed quick ways to tell the quality of documentation.
This post will be about what they are,
and what they mean.
Obviously it is just a heuristic,
and having these things doesn't make good documentation.
However,
the absence of them usually indicates a lack of quality.

A Website
---------

**If your documentation is a directory full of files on GitHub,
I close the tab.**
With GitHub Pages, 
Read the Docs, 
and other places to host generated documentation for free,
not making an effort is unforgivable.

If this is your project,
please check out `Mkdocs`_.
It is still a new tool,
but it will give your users something much nicer.
I also recommend `Sphinx`_ for the most mature approach to documentation.

.. _Mkdocs: http://www.mkdocs.org/
.. _Sphinx: http://sphinx-doc.org/

Prose
-----

If your documentation is generated from source code,
I am immediately skeptical.
You should use words to communicate with your users,
and those words shouldn't live in your source code.
**If you included all of the things needed to document a project in source,
your code would be unreadable.**

So please,
use a tool that allows you to write prose documentation outside of your source code.
Your users will thank you.

A great start is to read this series on `Writing Great Documentation`_, and the resources on the `Write the Docs`_ docs. [1]_ 

.. _Writing Great Documentation: http://jacobian.org/writing/great-documentation/
.. _Write the Docs: http://docs.writethedocs.org/#contents

Permalinks
----------

One of the primary uses of documentation is the ability to link information to other people.
**If your documentation doesn't have an easy way to link to sections of content on a page,
then the value decreases.**
Your users should never have to send someone a link and say "go here and search for X".
That means your documentation has failed your users.

You'll notice even my blog has permalinks.
I believe all text content should,
because it greatly increases the utility of the content.

URLs
----

There are two things I always look for in the URL:

    * Language
    * Version

Most often,
projects don't have either.
Your URL should look something like: ``https://docs.project.com/en/1.0/``

Versions
~~~~~~~~

I see versions in lots of documentation,
but not nearly enough.
If your project has versions,
your documentation should too.
Not everyone can always upgrade to the latest version.
**If someone is using an old version,
they should have access to documentation for that version**.

Along the same lines,
you should also have documentation for your development version.
If the docs don't have a version attached,
I have no idea if they are up to date or not.
You should clearly mark your released versions and development version,
otherwise users will get confused.

Language
~~~~~~~~

Language is one I rarely see.
The software world has a nasty habit of forgetting that the whole world doesn't speak English.
If you don't provide a language in your URL,
you are implicitly sending the message that the documentation will never be translated.

I believe that translating documentation is a really important step towards helping people learn to program.
**Someone shouldn't have to learn Programming and English at the same time.**

Translations are quite a bit of work,
so I understand why many projects don't have them.
But you should at least acknowledge the possibility of translation by putting the language in the URL.

Conclusion
----------

That is the 30 second way that I determine if a project's documentation is worth looking at.
These are all hints about if a project actually cares about its docs.
If the project doesn't care about its documentation,
that is a good sign that you probably shouldn't use it.

.. [1] If this kind of stuff interests you,
		I help organize a conference about documentation:
		http://conf.writethedocs.org/

