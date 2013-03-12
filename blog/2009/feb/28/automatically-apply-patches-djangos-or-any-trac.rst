:Date: 2009-02-28 20:18:07

Automatically apply patches from Django's (or any) Trac
=======================================================

Lately I've been delving into Django development a bit more, and
applying people's patches has been a bit of a hassle. You know you
want to apply someones patch, but there are about five steps in
between you and applying their patch to your source tree.

So I'd like to present trac\_patch.py, which allows you to apply a
patch from Django's trac automatically. It is posted on github, so
I encourage everyone to fork it and modify it to fit your own
workflow. This was done in about 2 hours, so it's still pretty
rough. Also note, that this should work with a small modification
on just about any trac install out there.

I threw a few features in that were useful for my development
workflow. You can easily create a new git branch automatically with
the name of the patch that you're applying. You can apply and
revert a patch. It also has a mode where you can confirm the ticket
you're looking at, and choose which of the patches on the ticket
you wish to apply to your code.

You can use it by default if you're in your current top-level
django directory (or where ever you want the patches applied).
However, there is a ``django_src`` variable in the code that you
can set and then it will work from anywhere.

I'll paste in the modules docstring below, so you see some examples
of it in action.

::

    Description::
    
    Simple utility to grab and apply a Django trac ticket.
    It could in theory be used for any trac installation.
    
    Usage:: trac_patch.py [ticket_num]
    
      -h, --help     show this help message and exit
      -r, --reverse  Reverse the patch
      -g, --git      Make a git branch
      -a, --ask      Make a git branch
    
    Examples::
        trac_patch.py [ticket_num] [-r]
    
        #Apply patch 6378
        trac_patch.py 6378
    
        #Reverse patch 6378
        trac_patch.py 6378 -r
    
        #Create a git branch and apply patch
        trac_patch.py 6378 -g
    
        #Confirm patch filename and ticket filename
        trac_patch.py 6378 -a


