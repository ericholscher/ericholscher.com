:Date: 2010-08-22 12:00:00
Lessons Learned From The Dash: Nginx SSI
========================================

Continuing from my
`previous post <http://ericholscher.com/blog/2010/aug/16/lessons-learned-dash-easy-django-deployment/>`_
about `Django Dash <http://djangodash.com>`_, I will be talking
about another thing that I learned from the dash. This isn't as big
of a post, but just something that we ran into that caused us some
trouble.

We are hosting documentation for other projects, and we needed a
way to put a toolbar on the top of the pages so users can still get
around our site. We started out by hacking this into the sphinx
template as static html, which was annoying because it didn't let
us determine if the user was logged in, owned the project, etc. So
we decided to load the header dynamically.

Using Nginx Ghetto ESI
~~~~~~~~~~~~~~~~~~~~~~

We were deploying on Nginx, and luckily
`this post <http://joshuajonah.ca/blog/2010/06/18/poor-mans-esi-nginx-ssis-and-django/>`_
about Ghetto ESI with Nginx laid it out pretty well. We only ran
into one problem with this approach, and it was minor.

The implementation is that we are hacking the SSI tag into the
Sphinx template's we are rendering at the top of the page.

::

    {% block relbar1 %}
    <!--# include virtual="/render_header/" -->
    {{ super() }}
    {% endblock %}

Then you simply add a ``ssi on;`` into your Nginx configuration for
your site. This makes the page call /render\_header/ to fill out
the top of the page when the user hits a documentation page.

The problem
~~~~~~~~~~~

The problem with this is that this doesn't work in your local
testing environment. So Joshua's post earlier has a piece of
middleware that you can include in your Django project to emulate
the Nginx include behavior.

We turned this on, but every once in a while our pages were getting
randomly cut off halfway through the response. We looked into it a
little bit, and figured out that it was because of the response's
Content Length header was still set to the old value. So
`our updated middleware <http://github.com/rtfd/readthedocs.org/blob/c35c9e142e5a602eca8fae88c9bfd54497c5ddf8/core/middleware.py#L30>`_
simply added one line to the reponse.

::

    response['Content-Length'] = len(response.content)

This allowed our pages to render correctly in testing, and then in
production Nginx will hit the include before Django sees it, so the
middleware never processed.
**If you are changing the content of your response in middleware, make sure that you update the Content-Length header.**


