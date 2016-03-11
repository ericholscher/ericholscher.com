Why I Hate "Markdown" for Documentation
=======================================

"Markdown" is the most commonly used markup language on the internet.
It is great for a subset of tasks,
mainly blog posts and commenting.
However,
lately it has been adopted by the technical writing community as a solution for writing longer form documents.

I'd like to lay out the main arguments that I have against Markdown.
Hopefully this will be useful in helping you decide whether it's a good fit for your organization.
If you are considering markdown,
I hope that you also look at AsciiDoc + `Asciidoctor`_, and reStructuredText + `Sphinx`_.
I find them to be much better toolsets for writing documentation.

.. _Asciidoctor: http://asciidoctor.org/
.. _Sphinx: http://www.sphinx-doc.org/en/stable/

Lack of a standard
------------------

For a long time,
Markdown was defined by the `initial implementation`_ written by John Gruber. 
There was no spec,
and the "proper" behavior was whatever this script chose to do.

As Markdown got more popular,
more and more sites started to implement it.
Those sites were written in other languages,
so more implementations of "Markdown" were created.
All of these implementations had slight variations in what was accepted.

One example is that some required a space before a heading and others didn't::

	# Heading 1

	#Heading 1

There are a number of small issues that made it hard to port your Markdown between sites and verisons.

In the last few years, `Commonmark`_ was developed as a standardized Markdown.
This is great,
and should solve lots of problems!
Except that nobody has adopted it...

.. _Commonmark: http://commonmark.org/

Flavors
-------

The main reason for this lack of adoption is that people using Markdown haven't been sitting still for all these years.
Because the original Markdown is so limited,
every popular tool built on top of Markdown implements what is called a "`flavor`_" of "Markdown".
This sounds great,
except that **every tool implements a different flavor**.
Even tools that do similar things with the language use different syntax for it!

.. _flavor: https://github.com/jgm/CommonMark/wiki/Markdown-Flavors

Lack of referencing and includes
--------------------------------


Lack of Semantic Meaning
------------------------

Though many people have added extensions to Markdown,
almost none have any kind of semantic meaning.
This means that you can't write a *Note* or a *Warning*,
you can only write text.

This leads people to embeding HTML directly in their Markdown::

	<div class="warning">

	This is a Warning!

	</div>

In reStructuredText for example,
you can write::

	.. warning:: This is a Warning!

This will be output as a warning properly in HTML, PDF, and any other output format you can generate.

This has a number of issues:

* Your Markdown is now dependent on specific CSS classes in your display, meaning your writers have to think about how your page will be designed
* Markdown is no longer portable to other output formats (PDF)
* Conversion to other markup tools becomes impossible

Lock In and Lack of Portability
-------------------------------

The explosion of flavors and lack of semantic meaning leads to lock in.
Once you've built out a large set of "Markdown" documents,
it's quite hard to migrate them to another tool,
even if that tool claims to support "Markdown"!
You have a large set of custom HTML classes and weird flavors that won't work anywhere but the current set of tools.

You also can't migrate them easily to another markup languages (Asciidoc or RST).


Conclusion
----------

I love Markdown for it's simplicity.
However,
when you are trying to author 

.. _initial implementation: https://daringfireball.net/projects/markdown/