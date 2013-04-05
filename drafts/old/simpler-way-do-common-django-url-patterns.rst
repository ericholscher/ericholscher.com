:Date: 2009-08-16 20:36:04

A simpler way to do common Django URL patterns
==============================================

I often find myself looking through old projects and the official
Django docs looking for examples of common URL pattern syntax. It
seems like this is a common enough use case, that it should exist
either in core Django, or in Django Extensions.

I propose some kind of shortcut syntax that would the ability to
abstract common URL patterns into their own little space, for easy
reuse. I imagine the code to look something along the lines of:


