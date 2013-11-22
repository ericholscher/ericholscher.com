:Date: 2013-11-21 20:00:00

A Better Javascript Workflow with Django
========================================

Javascript has always been the bane of my existence as a developer.
It was the part of the process of developing that I would dread.
On the last project I worked on,
I found a very simple change that significantly improved my experience writing Javascript.

Problem: One big file
---------------------

Historically,
Javascript lived in one really large file.
If you wanted to break up the file,
you had to edit your HTML files to make sure they were in the correct order.
This always felt really brittle,
so I never actually split up my code into multiple files.

Even if you split things up into different files,
you had to reply on implicit import mechanisms.
A variable would just magically appear in your file because of the import order of the scripts.
This incredibly brittle and unintuitive way of working puts up a high barrier to writing well-factored code.

Solution: node-style requires
-----------------------------

Node.js has the concept of `require`.
It works very similarly to Python's `import` mechanism.

`client.js`

.. code-block:: javascript

	var events = require('./lib/events')
	events.awesome()

`lib/events.js`

.. code-block:: javascript

	module.exports = {
		awesome: awesome
	}

	function awesome() {
		console.log("Do awesome stuff.")
	}

The `module.exports` is similar to Python's `__all__`,
allowing you to explicitly set your public API.

.. TODO: Explain why this is better, better.

The `require` system allows you to factor your code into multiple files.
More importantly,
this allows for code isolation.
I can put logic surrounding setting up event handlers in the `events.js` file,
without having it leak into other sections of the code.

Architecting code in this fashion allowed me to write much better code.
It gives you an entry point into the code,
where the uppermost logic lives.
Then you can dive into each specific file to understand that subsection of code.
All the benefits normally associated with an import system come to bare.

As a wise man once said:

	Namespaces are one honking great idea -- let's do more of those!

Imports in the browser
----------------------

It's great that node has an import system,
but that doesn't help me when I'm writing Javascript for the browser.
`browserify`_ is a project that allows you to have node-style imports in the browser.

Browserify takes all of your Javascript files with imports,
and renders them into one large file you can include in your project.
It does this by pointing to a file,
which is the top-level entry point into your code.
In the example above, 
`client.js` would be the entry point.

To use Browserify, simply install it with npm:

.. code-block:: bash

	npm install browserify -g # -g means globally

Then run browserify on your top-level file:

.. code-block:: bash

	browserify client.js > bundle.js

Browserify outputs the Javascript to stdout,
so you can simply redirect it to a file that will contain your bundled Javascript code.
The "bundle" is what you include in your HTML:

.. code-block:: html

	<script type="text/javascript" src="bundle.js"></script>

A New Problem
--------------

As with all preprocessors,
the main issue is the workflow around rendering the code into its final form.
There are two general approaches for handling this:

	* Have a program watch for file changes, rebuilding on change.
	* Rebuild source files on request.

You can use programs like `watchdog`_ and `grunt`_ to handle rebuilding of files automatically.
The main issue with this is the feedback loop.
You can save a file and reload your browser,
and you aren't sure if it's serving the latest change you made.

I generally prefer having it rebuild the source on request.
This works well until you have large files that have to be compiled,
where reloading each request introduces significant lag. 
Luckily for my Javascript projects,
they tend towards the smaller side.

`Beefy`_ is a project that presents an HTTP server,
which autocompiles your Javascript with Browserify.
To use beefy you install it:

.. code-block:: bash

	npm install beefy -g # -g for global install

Django Integration
------------------

Beefy also works as a simple HTTP server.
It auto-generates your Javascript through Browserify,
but also serves normal static media.
This means you can point your `STATIC_URL` at Beefy,
and it will just work.

First you have to collect your static media into a single directory:

.. code-block:: bash

	./manage.py collectstatic

Then,
from your `STATIC_ROOT` you run beefy,
pointing at your Browserify entry point:

.. code-block:: bash

	beefy client.js

You can also pass the bundle you want it to generate with a `:`.
This allows you to point at the same Javascript file in development as in production:

.. code-block:: bash

	beefy client.js:bundle.js

Beefy should now be serving on port `9966`.
You can point Django at this for static media by using the setting:

.. code-block:: python

	STATIC_URL = 'http://localhost:9966/'

Beefy should now be serving your media properly,
and auto-compiling your javascript through Browserify.

.. note:: You may want to symlink your javascript files from into `STATIC_ROOT`,
            if you are doing active development on them.

Conclusion
----------

With this workflow you can now write Javascript with a sane import system,
and have it *Just Work* in development.
I hope that it makes the Javascript part of your development a little bit more enjoyable.

.. _watchdog: https://pypi.python.org/pypi/watchdog
.. _grunt: http://gruntjs.com/
.. _Beefy: http://didact.us/beefy/
.. _browserify: http://browserify.org/
