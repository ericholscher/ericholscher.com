.. post:: 2016-07-25 09:00:00
   :tags: sphinx, training, jinja

The Power of Sphinx: Integrating Jinja with RST
===============================================

`Sphinx <http://www.sphinx-doc.org/en/stable/>`_ is a super powerful tool.
This has its upsides and downsides.
One of the major downsides is that historically it has been built as a framework that allows users to do just about anything.
This is great,
except it also means that a lot of the specific value out of the modular design hasn't been documented or made explicit to users.
I'm hoping to address some of this power in a set of blog posts.

Today I'll cover integrating the templating language `Jinja <http://jinja.pocoo.org/docs/dev/templates/>`_ inside your RST files.
This is a really useful thing,
and allows a large number of powerful display semantics inside of your RST files.

Jinja is also the templating engine that Sphinx uses internally for rendering HTML.
This means you already have the library installed with Sphinx,
so no external dependency is required.

The Extension
-------------

Most of the power of Sphinx comes from the ability to plug into any part of the documentation building process.
Sphinx has an exhaustive list of `Sphinx events <https://www.sphinx-doc.org/en/master/extdev/event_callbacks.html>`_,
which I recommend reading up on.
This extension will use the ``source-read`` hook,
which fires when the actual RST file is read from the disk.

From there it is the simple matter of taking the source that has been read,
and passing it through Jinja.
Here is the full extension:

.. code-block:: python

    def rstjinja(app, docname, source):
        """
        Render our pages as a jinja template for fancy templating goodness.
        """
        # Make sure we're outputting HTML
        if app.builder.format != 'html':
            return
        src = source[0]
        rendered = app.builder.templates.render_string(
            src, app.config.html_context
        )
        source[0] = rendered

    def setup(app):
        app.connect("source-read", rstjinja)


This simple extension gives us a ton of power.
Let's talk through one example.

Generating Docs from Data
-------------------------

A lot of times we have an external data set that we want to generate into our documentation.
Let's say this is a list of team members that is maintained in a remote system,
and we want to include in our docs.
If we can get that data into JSON,
it's pretty simple to add it into our project.

In our ``conf.py``,
or another Sphinx extension,
we can do:

.. code-block:: python

    import json

    staff = json.load(file('data/company-staff.json'))

    html_context = {
        'company_staff': staff
    }

This gives us the ``company_staff`` variable in our HTML context,
which will be availabe from Jinja.
Then we can generate our ``staff.rst`` file:

.. code-block:: rst

    Staff
    =====

    {% for member in company_staff %}
    {% if member.is_active %}
    * `{{ member.name }} <{{ member.url }}>`_
    {% else %}
    * {{ member.name }} (Emeritus)
    {% endif %}
    {% endfor %}

.. note:: The Jinja templates will be rendered *before* the RST is processed.

Allowing ourselves to use Jinja inside of RST gives us a whole set of logic that isn't available in the RST language itself.

This approach is incredibly powerful,
but please make sure you don't overdo it!
Try to keep the Jinja logic simple,
and only apply it to things that alter the display of the page.

Want more tips?
---------------

I love talking and thinking about the power of Sphinx.
Along with blogging,
I provide Sphinx documentation training for companies.
We do half-day, full-day, and multi-day classes.
Shoot me an `email <training@readthedocs.com>`_ or check out our `sphinx training website <http://www.sphinxtraining.com>`_ for more info.
