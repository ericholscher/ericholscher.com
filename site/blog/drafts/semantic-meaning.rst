.. post::
   :tags: semantic meaning, markdown, restructredtext, semantics

Semantic Meaning in Documentation
=================================

Semantic Meaning in documentation is the separation of what something *is* from what it *looks like*.
What we *mean* and what we *display* are very different things.

We might want to **warn** someone in our writing,
but we don't want to think about how to display this.
Writing with Semantic Meaning gives us this power.

Semantics
---------

As an example,
if we were writing documentation in HTML,
we could warn a user with bold::

    <b>Don't do this, it will break your system!</b>

This has no semantics.
**Bold doesn't mean "warning",
it is simply a way of displaying text.**
A better example in HTML is:

    <span class="warning">Don't do this, it will break your system!</span>

This allows you to write *what* something is,
but not have to worry about what it looks like.
Your designer might decide that warnings should be bold and red::

    .warning { 
        text-format: bold; 
        color: red;
    }

To go one step further,
in reStructredText we can do::

    .. warning:: Don't do this, it will break your system!

Then Sphinx or some other tool will generate the proper HTML or PDF with styles for us.
reStructredText is abstracted away from all of the output formats,
so you write in one format,
and it transforms it properly into HTML,
PDF,
XML,
or any other format it supports.
Without having to *think* about anything more than the semantic concepts you care about.

Value of Semantic Documentation
-------------------------------

When you write documentation,
you form a mental model in your head of the document you're writing.
When you use a powerful tool like reStructredText,
you can **think** in terms of *warnings*,
*references*,
*classes*,
*objects*,
and other powerful semantic constructs.
You start thinking in terms of *nouns* that can be represented in your problem domain.
You can also encode this information into the output:

.. code-block:: rst

    .. warning:: Make sure you :term:`instantiate` the Response objects before you use it.

    You can read more about the :cls:`django.http.Response` in our :doc:`/api/response` page.

**When you write with semantics,
you can encode more of your mental state into the words you write.
Conversely,
if you write without semantics,
valuable information about your writing is lost.**

Semantic information also acts as a type of documentation for our writing.
Similar to `type systems`_ in programming,
they allow you to be explicit about what you're talking about.
When you write documentation about a ``Response`` object,
it isn't immediately obvious *what* that is.
When you write about a ``:cls:`django.http.Response```,
it is explicitly defined what you're talking about.

**When you write documentation in Markdown,
there is no clear way to represent semantic information.**
You can make something **bold**,
but you can't make something a **warning**.
As an author,
this means that you are limited in how much data you can transfer at an absolute level.

When you write something and make it bold,
what are you actually trying to communicate?

.. _type systems: TODO

Conclusion
----------

Communicating with words is a much different skill than transferring communicating with design.
We don't even group these people together in the same schools in college.
Interface Design and English aren't seen as similar fields.
In the process of producing documentation however,
they are two sides of the same coin.
We have to both write and display information for users,
and make it easy for them to understand it.

You should write in a format that gives you the most semantic meaning possible.
This allows you to:

* Allows you to focus on communicating information, not thinking about what HTML class you need for a concept
* Expand your own ability to think about your writing in terms of semantic nouns, allowing you to better structure your thoughts
* Give people updating your documents explicit information about what you're documenting 
* Allows your documentation systems to crosslink information and provide a better experience for your user
* Allows your designer to apply consistent styles to all types of information

When you empower writers with the ability to write with powerful semantic constructs,
writing becomes easier.
It also standardizes the output for your designers,
who will appreciate being able to have proper semantic classes in your HTML.
Using standard tools that enforce these constraints will make both your writers and designers life easier.