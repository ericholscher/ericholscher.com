:Date: 2016-03-15 09:00:00

Why You Shouldn't Use "Markdown" for Documentation
==================================================

`"Markdown"`_ is the most commonly used lightweight markup language on the internet.
It is great for a subset of tasks,
mainly blog posts and commenting.
However,
lately it has been adopted by the technical writing community as a solution for writing documentation.

I'd like to lay out the main arguments that I have against Markdown.
Hopefully this will be useful in helping you decide whether it's a good fit for your organization.
If you are considering Markdown,
I hope that you also look at `Asciidoctor`_ and `Sphinx`_.
I find them to be much better toolsets for writing documentation.

Markdown is often chosen because it's viewed as a simple approach that handles the basic cases well.
Developers prefer it because GitHub supports it,
though GitHub supports `9 different markup languages <https://github.com/github/markup#markups>`_,
including `Asciidoc <http://asciidoctor.org/docs/asciidoc-writers-guide/>`_ and `reStructuredText <http://www.sphinx-doc.org/en/stable/rest.html>`_.
As documentation grows from a few pages into a large set of documents,
Markdown quickly falls over and becomes a liability instead of a benefit.
I'd like to explain a bit more about why this is the case.

.. _"Markdown": https://github.com/jgm/CommonMark/wiki/Markdown-Flavors
.. _Asciidoctor: http://asciidoctor.org/
.. _Sphinx: http://www.sphinx-doc.org/en/stable/

Lack of a standard
------------------

For a long time,
Markdown was defined by the `initial implementation`_ written by John Gruber. 
There was no spec,
and the "proper" behavior was whatever this script chose to do.

As Markdown got popular,
more and more sites started to implement it.
Those sites were written in other languages,
so more implementations of Markdown were created.
All of these implementations had slight variations in what was accepted.

One example is that some required a space before a heading and others didn't::

	# Heading 1

	#Heading 1

There are a number of small issues that made it hard to port your Markdown between sites and versions.

In the last few years, `Commonmark`_ was developed as a standardized Markdown.
This is great,
and should solve lots of problems!
Except that nobody has adopted it...

.. _Commonmark: http://commonmark.org/

Flavors
-------

The main reason for this lack of adoption is that people using Markdown haven't been sitting still for all these years.
Because the original Markdown is so limited,
every popular tool built on top of Markdown implements what is called a "`flavor`_" of Markdown.
This sounds great,
except that **every tool implements a different flavor**.
Even tools that do similar things with the language use different syntax for it!

For example,
in `Markdown Extra`_ code blocks look like this::

	~~~ .python

	import antigravity

	~~~

This would apply a `python` class to the HTML block that is output.

However,
with `GitHub Flavored Markdown`_ the same example would be::

	```python

	import antigravity

	```

This would apply syntax highlighting to the actual rendered HTML output.

**This is two different syntaxes for a similar concept, both called "Markdown"**

.. _GitHub Flavored Markdown: https://guides.github.com/features/mastering-markdown/#GitHub-flavored-markdown
.. _Markdown Extra: https://michelf.ca/projects/php-markdown/extra/#fenced-code-blocks
.. _flavor: https://github.com/jgm/CommonMark/wiki/Markdown-Flavors

Lack of Extensibility
---------------------

With other markup languages,
you can extend the language to provide the features that you need.
They have mechanisms in the syntax to add new functionality,
without breaking from the original spec and creating a new language.

reStructuredText for example,
has both inline and block level markup:

.. code-block:: rst

	.. contents:: All the stuff I'm going to talk about
	   :depth: 2

	Please look at :rfc:`1984` for more information.
	This is implemented in our codebase at :class:`Example.Encryption`.

You can learn more about the `rfc <http://docutils.sourceforge.net/docs/ref/rst/roles.html#rfc-reference>`_, `class <http://www.sphinx-doc.org/en/stable/domains.html?highlight=domains#cross-referencing-python-objects>`_, and `contents <http://docutils.sourceforge.net/docs/ref/rst/directives.html#table-of-contents>`_ concepts.

As a developer working with rST or Asciidoctor,
I can add new markup to the language in a simple,
pluggable way.
I don't have to change how the language is parsed,
and I can share those additions with other users via a standard extension mechanism.

**There is no way of doing this in Markdown,
in a way that would be portable across versions.**

.. note:: CommonMark is working on an `extensibility syntax`_, but it isn't implemented yet.

.. _extensibility syntax: http://talk.commonmark.org/t/generic-directives-plugins-syntax/444

Lack of Semantic Meaning
------------------------

Though many people have added extensions to Markdown,
almost none have any kind of semantic meaning.
This means that you can't write a *Class* or a *Warning*,
you can only write text.

This leads people to embed HTML directly in their Markdown:

.. code-block:: html

	<div class="warning">

	This is a Warning!

	</div>

In reStructuredText for example,
you can write:

.. code-block:: rst

	.. warning:: This is a Warning!

This will be output as a warning properly in HTML, PDF, and any other output format you can generate.

**Semantic markup firmly separates the words that you write from how they are displayed.**

Writing without semantic markup is a problem for a few reasons:

* Your Markdown is now dependent on specific CSS classes in your display, meaning your writers have to think about how your page will be designed
* Your content is no longer portable to other output formats (PDF, etc.)
* Conversion to other markup tools and page designs becomes much harder

Lock In and Lack of Portability
-------------------------------

The explosion of flavors and lack of semantic meaning leads to lock in.
Once you've built out a large set of Markdown documents,
it's quite hard to migrate them to another tool,
even if that tool claims to support Markdown!
You have a large set of custom HTML classes and weird flavor extensions that won't work anywhere but the current set of tools and designs.

You also can't migrate Markdown easily to another markup language (Asciidoc or RST),
because Pandoc and other conversion tools won't support your flavor's extensions.

I think that a lot of people choose Markdown because they think they can migrate to another tool or markup later.
Markdown is definitely the lowest common denominator,
except that for any reasonably sized set of docs you'll need things that aren't in the basic language.

**Once you start using markdown flavors,
which is required for any non-trivial documentation,
you lose all portability benefits.**

Conclusion
----------

I believe that CommonMark is a good step forward,
and if it became more widely used,
and added extension support,
I could whole-heartedly recommend it as a solution to this problem.
The current ecosystem we have around Markdown is not something that I can endorse,
and believe that it's actively holding back folks to want to make documentation better.

I hope that we can start to move forward with a more standardized set of languages,
including CommonMark, reStructuredText, and Asciidoc,
fully supporting them across the suite of tools that we use.
For now, please investigate `Sphinx`_ and `Asciidoctor`_ as good alternatives.
They come with a lot more extensibility built into the language,
and are more complete tools for building sets of documentation today.

Markdown is a concept more than it is an implementation.
It generally means "a set of incompatible extensions to something that looks kinda like Markdown".
When you are trying to author large sets of documents,
it isn't the correct tool.

*Full Disclosure:* I work on a product, `Read the Docs <https://readthedocs.com/>`_, which is based on Sphinx, so my views are likely biased.

.. _initial implementation: https://daringfireball.net/projects/markdown/
