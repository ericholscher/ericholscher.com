.. post:: 2009-01-29 08:56:33

Using rsync with django
=======================

Just a quick warning/tip on using Django with rsync, for other
people pulling their hair out later.

When you use rsync a good way to get a directory is using
``rsync -aCq``, which means recursively, quietly, move a directory
ignoring common files. The -a command means 'archive'; keep
permissions and as much data about the files as possible. We use -C
because it ignores .pyc and .svn files. However, in the list of
included files is 'core', so that you don't move over core dumps.

Django however has a core directory inside of it, and using -C
causes rsync to ignore that directory. So we ended up using the
rsync command like so:

::

    rsync -aCq --include=core 

Hopefully this saves people some time trying to rsync Django in the
future. I'd be curious what other rsync commands that people use
for moving around django and/or other files.


