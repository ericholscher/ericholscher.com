:Date: 2009-04-16 11:16:18

Testing AJAX Views in Django
============================

A lot of the Django code we use at work has a special case for
AJAX. It has been a kind of a pain to test, because the test client
by default doesn't use AJAX. Luckily the
`is\_ajax <http://code.djangoproject.com/browser/django/trunk/django/http/__init__.py#L80>`_
call in the Django HttpRequest object is a simple check of an HTTP
Environmental variable.

An undocumented feature of the Django Test Client is that you can
pass in custom HTTP ENV variables on requests. The definition of
get for example is:

::

        def get(self, path, data={}, follow=False, **extra):

Later on in the file, the request environment is then updated with
the extra keyword args: ``r.update(extra)``.

This lets us throw in arbitrary variables in our get and post
requests in the test client. Like so:

::

      r = self.client.post('/ratings/vote/', {'value': '1',}, 
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

Note that the custom env is outside of the dictionary of get
parameters. This will now return the /ratings/vote/ view with the
output that is normally called on an AJAX request.


