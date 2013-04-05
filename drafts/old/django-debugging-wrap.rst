:Date: 2008-08-28 23:23:45

Django Debugging Wrap Up
========================

In this post I want to talk about a little bit of the mindset that
I have when I go into debugging, and how it related back to the
ideas and techniques expressed in the previous series of
screencasts. It has always interested me what the best way to look
at debugging is, and this is simply my approach to explaining it.
Having all of these powerful tools in your toolbox is worthless if
you don't think about using them. Using them in the wrong places is
also less than optimal, but generally doing some form of debugging
is better than none.

Django-logging for data that you don't know what it is going to be.
pdb for data that you need to see into (see the members, wrong part
of set being chosen. Random breakage) Error page for quickly
debugging errors. (esp with werkzeug).

pdb -> logging -> errorpage -- ish


