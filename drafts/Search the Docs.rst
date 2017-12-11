Better search for Read the Docs
===============================

We have been hard at work implementing a new search backend for Read the Docs.
With the help of Rub Hudson, and Chris Mcdonald,
we now have a fancy new Elastic Search backend.
This gives us a lot more power and flexability over how we are indexing data,
and allows for more interesting search features.

The code is really readable,
and I think it makes for a good example of how to use Elastic Search with Python.

Creating Indexes
----------------

With Elastic Search,
we have to create indexes before we can store data in them.
This is all done with JSON over a REST API,
which is abstracted with Python.

The client facing code for creating this is all python:

.. code-block:: python

    from search.indexes import Index
    index = Index()
    index_name = index.timestamped_index()
    index.create_index(index_name)
    index.update_aliases(index_name)

The boilerplate around time stamps allows us to do some neat stuff.
We have a ``readthedocs`` index that is always the index in production.
This is actually an alias that points to a timestamped index ``readthedocs_20130901``.
So when we want to reindex our data,
we can create a new index with a timestamp,
index all of the data into our new index,
then update our alias to point at the new index.
This allows us to have effectively zero downtime reindexing.

When ever we create a new index,
we also need to create the mappings for our data.
We have python objects that represent each mapping,
so we simply initialize them and call ``put_mapping`` to send the JSON to Elastic Search.

.. code-block:: python

    from search.indexes import PageIndex
    proj = ProjectIndex()
    proj.put_mapping()

Interesting Indexes
-------------------

We currently have 3 indexes, Projects, Pages, and Sections.
The ``ProjectIndex`` is the most obvious.
It simply indexes the different Projects that we have in Read the Docs.
The ``PageIndex`` contains specific pages for a Project.
This allows us to search the contents of a page and return results to it.
The most interesting index we have is the ``SectionIndex``.
This actually indexes the different sections of content on a ``Page``,
allowing us to know how many sections of a page match a given query.

Faceting
--------

We have facets on projects,
so that you can filter your results by the project that contains them.
This is really useful if you want to be able to see what projects match your query,
and then filter by only that project.

Boosting
--------

Since we have data around the number of page views,
we boost search results based on the popularity of the project and page involved.
This means that more commonly referenced pages and projects should be returned first.
This allows us to give much better results than just doing plain search,
because it takes into account things like projects that aren't really used much anymore,
or projects that are really popular.

Production Settings
-------------------

In production,
we run with the data stored in 5 shards.
We then replicate this data across 2 nodes.
This effectively means that we have 2 copies of all the data in production.


Try it out
----------

We have a demo frontend for our search API that is in active development.
It shows off the ``SectionIndex`` functionality,
returning only the specific section that you need for your results.

It is available at http://searchthedocs.org
We will also be rolling something similar to this into Read the Docs proper,
once we have a fully fleshed out interface.

You can also play with the raw API: https://readthedocs.org/api/v2/search/section/?q=git