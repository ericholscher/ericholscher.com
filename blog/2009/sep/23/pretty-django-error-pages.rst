:Date: 2009-09-23 15:14:29
Pretty Django Error Pages
=========================

Continuing on with the
`simple <http://ericholscher.com/blog/2009/sep/5/debugging-django-production-revisited/>`_
`tricks <http://ericholscher.com/blog/2009/jun/29/enable-setuppy-test-your-django-apps/>`_
that make everyone's life a little bit better, I know a lot of
people hate that Django's 500 pages don't get rendered as a
RequestContext. This means that if you have context processors
(like one that sets a MEDIA\_URL), they don't get called. This was
causing our 500 pages not only to make users sad because something
broke, but knock them out of context becaue our entire design blew
up.

Luckily, Django makes it incredibly simple to redefine your 500
handler in your URLConf. Most pythonistas know that ``import *`` is
a bad thing, but it is standard in the Django community in your
URLConf to do a ``from django.conf.urls.defaults import *``. This
has the effect of pulling in Django's default ``handler500``
function. So if you want to override Django's default, you simply
set it up like so.

::

    from django.conf.urls.defaults import *
    handler500 = 'path.to.my.sweet.views.server_error'

Then you simply define a server\_error view that renders the error
page with a RequestContext.

::

    from django.shortcuts import render_to_response
    from django.template import RequestContext
    
    def server_error(request, template_name='500.html'):
        """
        500 error handler.
    
        Templates: `500.html`
        Context: None
        """
        return render_to_response(template_name,
            context_instance = RequestContext(request)
        )

If you're feeling extra special, you can even change the template
rendered. Note that you can also do this for the 404 handler by
defining a ``404handler`` in your URLConf in the same fashion. Then
you can get
`pretty error pages <http://www2.kusports.com/users/oldalum/>`_!


