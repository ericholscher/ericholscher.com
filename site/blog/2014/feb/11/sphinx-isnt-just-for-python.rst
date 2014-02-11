:Date: 2014-02-11 16:00:00

Sphinx isn't just for Python
============================

I have heard a few times over the past couple months that `Sphinx`_ is "mainly for Python projects".
This line of thinking makes sense,
because Sphinx was created to document Python itself.
Sphinx however,
is a generic documentation tool that is capable of documenting any software project.

.. _Sphinx: http://sphinx-doc.org/

The goal of Sphinx is to help you write prose documentation.
Prose docs work great for any kind of software you are documenting.

What it doesn't handle particularly well is generation of docs from source code.
This is a task that is best left to a language-specific tooling,
so I don't see this as a major downside of Sphinx.

As I run `Read the Docs`_,
I get a chance to see a lot of the different things people are doing with Sphinx.
At the beginning,
Read the Docs was mostly Python projects.
These days though,
some of our biggest and most active projects are in a number of languages.

.. _Read the Docs: http://readthedocs.org/

I think that actions speak louder than words,
so here is a small sample of projects using Sphinx for things that aren't documenting Python code.

Creating your own language
--------------------------

* Julia: http://docs.julialang.org/en/release-0.2/
* Hy: http://docs.hylang.org/en/latest/

Javascript
----------

* Bootstrap Datepicker: http://bootstrap-datepicker.readthedocs.org/en/latest/
* CasperJS: http://docs.casperjs.org/en/latest/

PHP
---

* Doctrine 2: http://docs.doctrine-project.org/en/latest/
* phpMyAdmin: http://docs.phpmyadmin.net/en/latest/
* Guzzle: http://docs.guzzlephp.org/en/latest/
* Phalcon: http://docs.phalconphp.com/en/latest/
* Bernard: http://bernardphp.com/

Java
----

* Inventory Tweaks: http://inventory-tweaks.readthedocs.org/en/latest/
* Idiorm: http://idiorm.readthedocs.org/en/latest/

Go
--

* Docker: http://docs.docker.io/en/latest/


Erlang
------

* CouchDB: http://docs.couchdb.org/en/latest/

R
-

* Little books of R: http://little-books-of-r.readthedocs.org/en/latest/

.Net
----

* MassTransit: http://docs.masstransit-project.com/en/latest/
* Topshelf: http://docs.topshelf-project.com/en/latest/

Conclusion
----------

I hope that this shows you how Sphinx can be used for documentation all kinds of software,
not just Python.
It is a fantastically powerful documentation tool,
and you shouldn't discard it without looking at it closely.
