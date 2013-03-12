:Date: 2008-11-15 17:27:37
Debugging Django in Production Environments
===========================================

`Nick <http://nicksergeant.com/blog/django/automatically-setting-debug-your-django-app-based-server-hostname>`_
had a nice post about setting DEBUG based on the hostname of the
server that you're site is running on. This allows you to set DEBUG
to True for your staging site, and False for your production site.

I do something along those lines, but a little bit differently. I
can't take credit for this idea, because it came from
`this snippet <http://www.djangosnippets.org/snippets/935/>`_. It
is a really neat trick, that I have expanded on a little bit.

::

    from django.views.debug import technical_500_response
    import sys
    from django.conf import settings
    
    class UserBasedExceptionMiddleware(object):
        def process_exception(self, request, exception):
            if request.user.is_superuser or request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
                return technical_500_response(request, *sys.exc_info())

Now simply save this in a file somewhere. Add it to your
MIDDLEWARE\_CLASSES, and you are good to go. For example, mine
looks like:

::

        'tools.middleware.superuser.UserBasedExceptionMiddleware',

This is a pretty simple middleware that is crazy useful. When you
throw this inside of your site, it will give you a normal Django
error page if you're a superuser, or if your IP is in
INTERNAL\_IPS.

This makes it really nice, because you can get an error message on
your production servers, where your normal users get your normal
pretty 500 pages. This makes debugging things that are showing up
in production, but won't be reproduced on the staging server
possible. Caching behavior is a big one that I know isn't tested
when you are using DEBUG = True. This lets you keep DEBUG = False
on, but gives you some nice error pages.

Hope this tip is useful.


