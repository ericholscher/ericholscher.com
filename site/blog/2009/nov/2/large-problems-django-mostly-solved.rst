.. post:: 2009-11-02 17:34:04

Large Problems in Django, Mostly Solved: Search
===============================================

It's been a little over a year since I started doing Django
development full-time, for one of them real jobs. Around that time,
there were a few large problems in the community that hadn't been
solved yet. They were kind of blemishes when you would talk to
people about Django, and I'm happy that most of them have been
solved.

This will be a series of posts that talk about the different big
problems that have been solved, and how they have been addressed in
the community.

Search
------

Search was probably the biggest annoyance for Django. It is
something that every site needs, and something that just wasn't
really happening in the Django community. 2008's Summer Of Code
ended with `djangosearch <http://code.google.com/p/djangosearch/>`_
as a half-finished shell, that needed to be better architected; but
it did show a good push in the realm of search.

Out of those ashes, comes an awesome solution to the search problem
in Django. `Haystack <http://haystacksearch.org/>`_ is something I
am more familiar with (we use it in production at work), and is the
brain child of the ever modest, house rocking
`Daniel <http://daniellindsleyrocksdahouse.com/>`_
`Lindsley <http://toastdriven.com/>`_.
**It provides a number of Django patterns applied to search**,
which makes it easier to internalize.

**Note**: Another approach to search is
`available <http://github.com/bfirsh/django/commits/search>`_,
which patches django's ORM. This uses the existing full-text search
in your database.

Useful Haystack Patterns
~~~~~~~~~~~~~~~~~~~~~~~~

Registration
^^^^^^^^^^^^

The registration pattern of the admin allows you to unobtrusively
make models searchable (including code you don't have access to).
This allows you to register Django Comments as searchable for
example, without forking the code base. This will look
`similar to <http://haystacksearch.org/docs/tutorial.html#create-a-searchindex>`_
the admin:

::

    from haystack import site
    site.register(Note, NoteIndex)

Search Querysets
^^^^^^^^^^^^^^^^

Haystack provides an
`interface familiar <http://haystacksearch.org/docs/searchqueryset_api.html#why-follow-queryset>`_
to the Django ORM Queryset API. This gives you most of the commonly
used functions from the ORM, but allowing you to use them on
searches!

::

    unfriendly_results = SearchQuerySet().exclude(content='hello').filter(content='world')
    unfriendly_results.order_by('-pub_date')[:5]

It also gives you Search specific methods such as
`boost and facet <http://haystacksearch.org/docs/searchqueryset_api.html#boost>`_.

Class Based Views
^^^^^^^^^^^^^^^^^

In 1.2, hopefully generic views will be class based. Haystack
`has an implementation <http://haystacksearch.org/docs/views_and_forms.html#views>`_
of these as well. Like any other kind of class, it provides the
easy ability to override functionality through subclassing.

This (simplified) example from
`the source <http://github.com/toastdriven/django-haystack/blob/master/haystack/views.py#L119>`_
shows how easy it is to provide
`extra context <http://haystacksearch.org/docs/views_and_forms.html#extra-context-self>`_
to a search view.

::

    class FacetedSearchView(SearchView):
        def extra_context(self):
            extra = super(FacetedSearchView, self).extra_context()
            extra['facets'] = self.results.facet_counts()
            return extra

Pluggable Backends
^^^^^^^^^^^^^^^^^^

Haystack currently supports three different search backends:
Whoosh, Xapian, and Solr. With a publicly documented backend API,
you can enjoy all of the power of the search engine of your choice,
by providing a backend for it!

::

    HAYSTACK_SEARCH_ENGINE = 'solr' 

Documentation
^^^^^^^^^^^^^

A shining light in the Django world is the documentation. It is
often talked about as being the biggest factor for how people learn
Django and love it is the documentation. Haystack is another
package with fantastic documentation. Here are a couple of little
gems that really show the quality and thought that has been put
into them:


-  `7 step tutorial <http://haystacksearch.org/docs/tutorial.html>`_
-  `Debugging Haystack <http://haystacksearch.org/docs/debugging.html#debugging-haystack>`_
-  `Best Practices <http://haystacksearch.org/docs/best_practices.html#best-practices>`_
-  `Reference <http://haystacksearch.org/docs/#reference>`_

The docs cover ways to improve your search and make it awesome, as
well as just helping you get the software set up and running. The
information is invaluable, and will help you make the search on
your site really great!

Are you using Haystack?
^^^^^^^^^^^^^^^^^^^^^^^

If I'm preaching to the choir and you already use Haystack, there
is a `growing list <http://haystacksearch.org/docs/who_uses.html>`_
of users that are using haystack.
Daniel would love for you to contact
him, and get yourself added to the list.

Did I miss anything?
^^^^^^^^^^^^^^^^^^^^

Let me know what you love (or hate) about Haystack. I think it
reuses a lot of the good patterns in Django, allowing people to
take knowledge they already have, and apply it to a new problem
domain easily. Is there anything that you don't like, or something
that you love that I missed? Let me know in the comments!


