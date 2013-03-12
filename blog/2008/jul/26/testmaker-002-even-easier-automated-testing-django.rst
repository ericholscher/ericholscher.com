:Date: 2008-07-26 12:21:08
Testmaker .002 (Even easier automated testing in Django)
========================================================

Okay, Well I have been hacking away at django-testmaker for the
last couple of days based on some ideas from the community. It has
gotten a lot better, so here is another blog post showing what's
new.

First let me just say how awesome the Django community is, and I am
really beginning to understand (and appreciate!) the open source
ethos. I would never have gotten this code this good in 3 days
without releasing it to the public. Thanks everyone for looking
over it and giving feedback!


.. raw:: html

   <h3> 
   
New stuffs

.. raw:: html

   </h3>
   
Testmaker got a management command! Now you don't have to worry
about messing with your middlware and having to take out the
testmaker stuff when in production. You simply add testmaker to
your INSTALLED\_APPS and away you go.

Here is another video of it in action:


.. raw:: html

   <object width="400" height="300">   
   

.. raw:: html

   </object>
   
Django Testmaker v2


.. raw:: html

   <h3>
   
How to make it work

.. raw:: html

   </h3>
   
Step 1: Add testmaker to your INSTALLED\_APPS settings.

Step 2: In the directory above the APP that you want to test, run
``./manage.py testmaker -a APP``

This should tell you where it is logging to, and where the fixture
files are going. It should only make fixtures once, so if you
change something in your database, you need to go ahead and delete
the old fixtures file and it will re-create a new one. It also has
3rd grade file-naming heuristics built in. So if a tests directory
exists in your project, it will log to APP-testmaker.py, if there
is no tests.py in your APP directory, it will put itself in that
file. If you have an existing tests.py file, it will make a
tests-testmaker.py file. You will then need to take the contents of
this file and integrate it into your normal tests. In a future
version if it encounters a tests.py, it may make a tests directory
and put both files inside of that, but I don't know if that is a
good idea.

Step 3: Once you have reconciled the above changes (only necessary
if you previously had a tests.py file in your APP directory)
``./manage.py test APP``

Then you have awesome base-line tests for your app.

In my release post I had some comments about the usefulness of
these tests. I think that it is a very useful thing if you have an
existing body of code with no tests. This will give you a
non-trivial base to then at least have tests for your code.

Testing all of your views will also presumably alert you to errors
introduced in your models and URLConf files as well. Having
dedicated tests to testing models is still better and a good idea,
but this code will at least give you a good starting point.

Being able to automate a base-line level of tests for an app will
hopefully make people more inclined to include these basic tests in
their apps, and everyone knows tests are better than no tests.


.. raw:: html

   <h3>
   
Known issues

.. raw:: html

   </h3>
   
There are also a few problems that I've had with the output. It
appears Satchmo is hijacking the logging module on output? If
anyone knows a good way to fix this, please let me know.

Also, the POSTing stuff hasn't been well tested, so there might be
a few bugs in that, it is pretty rudimentary.


