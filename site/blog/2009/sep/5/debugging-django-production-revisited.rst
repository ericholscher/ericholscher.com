.. post:: 2009-09-05 07:04:43

Debugging Django in Production Revisited
========================================

In a
`previous post <http://ericholscher.com/blog/2008/nov/15/debugging-django-production-environments/>`_
I talked about a neat middleware to debug production environments
in Django. It basically checked to see if you were a superuser, or
if you were in settings.INTERNAL\_IPS, and if so, then it displayed
a technical 500 page for you (The yellow one you know and love).
Anyway, at that point it was more of a simple idea, and not really
used in production.

At work the other day I was working on a bug that was only showing
up in production, and not on staging. I remember back to this
middleware and thought it would be perfect. Anyway, at work we have
a lot of non-technical people that are superusers (think my bosses
boss). We also all have the same external IP's when at work, so
none of the previous methods I had would work for this.

Thinking about it, and talking to my co-worker
`Ben Spaulding <http://benspaulding.com>`_, we thought that Django
has Groups built in, so why not use that? So I went ahead and
re-jiggered the middleware to be based around groups.

::

    from django.views.debug import technical_500_response
    from django.contrib.auth.models import Group
    from django.core.cache import cache
    import sys
    
    class UserBasedExceptionMiddleware(object):
        def process_exception(self, request, exception):
            users = cache.get('technical_error_users')
            if not users:
                skip = cache.get('no_technical_error_users')
                if skip:
                    return None
                try:
                    g = Group.objects.get(name='Technical Errors')
                    users = g.user_set.all()
                    cache.set('technical_error_users', users, 60)
                except Group.DoesNotExist:
                    cache.set('no_technical_error_users', True, 60*60)
                    return None
            if request.user in users and request.user.is_superuser:
                return technical_500_response(request, *sys.exc_info())
            return None

Since it is middleware, I went ahead and decided to use the cache
framework to make sure that we weren't doing a DB query on every
request. Also, I had to account for the case when the group hasn't
been added yet, so when that happens, it caches the fact and
doesn't check again for another hour. If the Technical Errors group
exists, it caches the members that are in it for a minute. This
means that a DB query only happens every minute, which is fine.

I'd be curious how other people might improve this, as it seems a
little bit janky still. However, it works for us, and is incredibly
useful when debugging. Instead of getting a link to a broken page,
you go to the page and get a nice 500, telling you exactly what
went wrong.

I can think of one basic improvement in just writing this post,
which would be to import settings and to just return None if DEBUG
was True, or if the CACHE\_BACKEND was set to None. This would
allow it to stay out of the way if there was no caching, or the
Technical 500 was already going to be raised.

I do think that this middleware removes a lot of the reason to run
a site under DEBUG=True, so hopefully it will result in less sites
launching with DEBUG on.


