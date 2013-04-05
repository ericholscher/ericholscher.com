:Date: 2010-01-23 19:28:21

Questions about python packaging
================================

In a couple of my projects in the past, I have been working with
arbitrary python packages. I know that a lot of python packaging is
targeted at getting your source code onto my system, in an easy
way. However, I think that there is another aspect to the whole
thing, that I haven't been able to get my head around.

I really hope that the answers to my questions are already out
there and obvious. However, in my search I haven't been able to
find good questions to seemingly simple introspection of a
package.

So lets take a scenario. I have a source checkout of your Python
Package, and it contains a well formed setup.py. I now want to
figure out some information about your package:


-  When I install your package, what will it install?
-  When I install your package, under what name will it install?
   (import ?)
-  What dependencies do I need in order to install and use your
   package?
-  How do I run the tests on your package?

This really all comes down to information that is contained in the
setup.py file, but has no external way to access it. Does a way to
access this information not exist, or am I just missing it?


