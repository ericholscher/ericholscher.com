:Date: 2009-04-05 10:12:42

Adding Google Analytics to Sphinx Docs
======================================

This is just a reminder for myself later, or people looking on
Google. Also note, that this method is useful for putting any
Javascript content into your sphinx docs, but Analytics tracking is
a common use case.

Step 1: Where to put my files?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check your conf.py on your Sphinx docs. You need to make sure your
``templates_path`` variable is pointed to a directory that exists.
It is relative to your current directory. I use ``_templates``,
which I believe is the default. This is where you can override
Sphinx templates. They use Jinja2, which is a relative of Django
templates, so it should be pretty simple if you're used to Django
templates.

Step 2: Override the default template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In your ``_templates`` directory, add a file called layout.html.
The
`Sphinx Docs <http://sphinx.pocoo.org/templating.html#jinja-sphinx-templating-primer>`_
are pretty good in this area, containing a full listing of all the
template that you can override. The
`Sphinx Source layout.html <http://bitbucket.org/birkenfeld/sphinx/src/tip/sphinx/themes/basic/layout.html>`_
is also really nice, so you can see what it is by default.

Analytics says that you should put your analytics code "Right
before the ``</body>`` tag" on your site. This means at the bottom
of the footer. Google should have given you a piece of Javascript
code to paste in your site, copy that below. So in your new
``layout.html``, put in the following code:

::

    {% extends "!layout.html" %}
    
    {% block footer %}
    {{ super() }}
    <script type="text/javascript">
    var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
    document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
    </script>
    <script type="text/javascript">
    try {
    var pageTracker = _gat._getTracker("YOUR_GOOGLE_CODE_HERE");
    pageTracker._trackPageview();
    } catch(err) {}</script>
    {% endblock %}

Take note of the ``{{ super() }}`` call. This means that you are
calling the inherited template's code, which pulls in the default
Copyright notice into the footer. Then you can put in your custom
code after that.

Let me know if there are any other neat Sphinx tricks and tips that
you have. I'm in love with the software and learning more about it
daily.


