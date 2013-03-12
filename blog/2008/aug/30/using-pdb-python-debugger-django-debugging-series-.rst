:Date: 2008-08-30 21:36:21
Using pdb, the Python Debugger (Django Debugging Series, Part 3)
================================================================

I had a couple of comments about my last post saying that I should
be sending all of the screencasts to the aggregator because this is
content and isn't spam. So I'm going to do that. Thanks for all the
feedback everyone! Hope you're enjoying the series.

Screencast 3
------------

Setup
~~~~~

No setup today. pdb is included with python, so everything that you
need is available at a python install near you.

Video and Download
~~~~~~~~~~~~~~~~~~

You can download the video
`here <http://media.ericholscher.com/casts/Using%20pdb%20in%20Django%20views.mov>`_
(17MB mov)


.. raw:: html

   <object width="640" height="500">   
   

.. raw:: html

   </object>
   
Screencast 3: Using pdb from Eric Holscher on Vimeo.

Writeup
~~~~~~~

I started the show by talking about a little bash alias that I made
to be able to run the testserver from anywhere. Here is that code,
edit accordingly:

``alias rs='/usr/bin/python ~/EH/manage.py runserver 67.207.139.9:8000 --settings settings_debug'``

In order to get into the debugger, you need to call it inside of
any of your python code.

::

    import pdb
    pdb.set_trace()

Then I go in to talk about the basic
`Pdb commands <http://docs.python.org/lib/debugger-commands.html>`_:


-  l (list): Shows the current code around the line that your on.
   The line that is about to be executed has a -> before it.
-  n (next): Executes the current line and moves to the next in the
   current file.
-  c (continue): Finishes the debugging session. If there are more
   breakpoints (or if your set\_trace() code gets called again before
   the request finishes) then you will get back to the debugger,
   otherwise the requests will complete back to the browser.
-  s (step): Goes down into the next level of execution (presumably
   a different file). You can follow your code through Django's
   internals this way. This is really good for finding bugs and
   getting a better understanding about how Django works.
-  w (where): Shows you a backtrace of the calls that have gotten
   you to the current point in the code execution. This is really
   handy for the following 2 commands.
-  u (up): Allows you to go up one level in the backtrace.
-  d (down): Allows you to go down one level in the backtrace.
   These two commands allow you to see where you came from, and what
   variables were called where. This lets you see how the state ended
   up the current way that it did, which is great for figuring out how
   to fix it. :)
-  locals(): This isn't a debugger function, but it is really handy
   for seeing what is in the current scope that you can muck around
   with. locals().keys() is really nice too just to see the variables
   that are there, because request tends to pollute the locals()
   command.

I had about double the content that is in this screencast to talk
about pdb. It is incredibly powerful and there are lots of other
neat things you can do with it. This screencast was running a
decent length already, so I decided to split it into 2 parts. This
is more of the "Intro to pdb" part, and tomorrow, I will be
presenting a little bit more advanced/different use case for the
debugger.

Stay tuned and have a good labor day weekend if you're in America.
Cheers!


