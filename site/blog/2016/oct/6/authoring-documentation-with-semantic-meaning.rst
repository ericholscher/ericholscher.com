.. post:: Oct 6, 2016
   :tags: semantic meaning, markdown, reStructuredText, semantics

.. _semantic-meaning:

Semantic Meaning in Authoring Documentation
===========================================

Semantic Meaning in documentation is the separation of what something is from what it looks like.
What we *mean* and what we *display* are very different things.

We might want to warn someone in our writing,
but we don't want to think about how to display this.
Writing with Semantic Meaning gives us this power.

Semantics
---------

As an example,
if we were writing documentation in HTML,
we could warn a user with bold:

.. code-block:: html

    <b>
        Don't do this, it will break your system!
    </b>

This has no semantics.
*Bold doesn't mean "warning",
it is simply a way of displaying text.*
A better example in HTML is:

.. code-block:: html

    <span class="warning">
        Don't do this, it will break your system!
    </span>

This allows you to write *what* something is,
but not have to worry about what it looks like.
Your designer might decide that warnings should be bold and red:

.. code-block:: css

    .warning { 
        text-format: bold; 
        color: red;
    }

The important part is that you don't need to think about what warnings look like,
just that it's a warning.

To go one step further,
in `reStructuredText <http://www.sphinx-doc.org/en/stable/rest.html>`_ we can do:

.. code-block:: rst

    .. warning:: Don't do this, it will break your system!

Then `Sphinx <http://www.sphinx-doc.org>`_ or some other tool will generate the proper HTML or PDF with styles for us.
reStructuredText is abstracted away from all of the output formats,
so you write in one format,
and it transforms it properly into HTML,
PDF,
XML,
or any other format it supports.

This approach allows your designers to work with a systematic and standardized set of class names,
generated from the tooling.
This keeps all your styles the same,
and allows the tool to warn you if you try and represent something that doesn't exist.

Value of Semantic Documentation
-------------------------------

When you write documentation,
you form a mental model in your head of the document you're writing.
When you use a powerful tool like reStructuredText,
you can *think* in terms of *warnings*,
*references*,
*classes*,
*objects*,
and other powerful semantic constructs.

You start thinking in terms of *nouns* that can be represented in your problem domain.
You can then encode this model into your document:

.. code-block:: rst

    .. warning:: Make sure you :term:`instantiate` 
                 the Response objects before you use it.

    You can read more about the :cls:`django.http.Response`
    in our :doc:`/api/response` page.


When the above section,
I thought *Hey, maybe someone doesn't know what instantiate means.*
I was able to link to the glossary with ``:term:``.
I didn't have to look up the URL for our glossary and link to that.
I didn't have to think about how to style glossary references.
**I was able to simply write what I meant,
and move on.**

When you write with semantics,
you can encode more of your mental state into the words you write.
Conversely,
if you write without semantics,
valuable information about your writing is lost.

Semantic information also acts as a type of documentation for our writing.
Similar to `type systems`_ in programming,
they allow you to be explicit about what you're talking about.
When you write documentation about a ``Response`` object,
it isn't immediately obvious *what* that is.
When you write about a ``:cls:`django.http.Response```,
it is explicitly defined what you're talking about.

.. note::
        When you write documentation in Markdown,
        there is no clear way to represent semantic information.
        You can make something *bold*,
        but you can't make something a *warning*.

        Please :doc:`don't write documentation in Markdown </blog/2016/mar/15/dont-use-markdown-for-technical-docs>`.

.. _type systems: https://en.wikipedia.org/wiki/Type_system

Conclusion
----------

Communicating with words is a much different skill than transferring communicating with design.
In the process of producing documentation however,
they are two sides of the same coin.
We have to both write and display information for users,
and make it easy for them to understand it.

As an author,
you should only need to care about communicating knowledge with words.
Writing with semantic meaning allows you to properly seperate communcation with words and design.

You should write in a format that gives you the most semantic meaning possible.
This:

* Allows you to focus on communicating information, not thinking about what HTML class you need for a concept
* Expand your own ability to think about your writing in terms of semantic nouns, allowing you to better structure your thoughts
* Allows tooling to raise errors when you try to reference semantic concepts that doesn't exist (typos, etc.)
* Give people updating your documents explicit information about what you're documenting 
* Allows your documentation systems to crosslink information and provide a better experience for your user
* Allows your designer to apply consistent styles to all types of information

When you have the ability to write with powerful semantic constructs,
writing becomes easier and more powerful.
If you want to be the most efficient and useful writer,
you write in a way that preserves the most of your mental model while writing.
You write with a tool that gives you semantic meaning.
