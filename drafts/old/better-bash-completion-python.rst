.. post:: 2009-11-16 17:27:36

Better Bash Completion in Python
================================

I was recently looking for a way to add bash completion to a Django
Management Command, and that sent me down a trail of bash
completion madness. In the past I have on multiple occasions looked
to adding bash completion to a program, and been turned away by the
last of documentation and good examples.

Pip and Django have both adopted the pattern that their bash
completion calls into Python in order to complete the commands. I
think that this is an interesting way to approach the problem, and
I would like to write a simple little wrapper that will hopefully
allow you to make your bash completion simpler.


