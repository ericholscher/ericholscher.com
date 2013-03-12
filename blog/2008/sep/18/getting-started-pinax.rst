:Date: 2008-09-18 18:52:54
Getting started with Pinax
==========================

NOTE: This content is a little out of date. Some of the layout might be wrong, but the ideas are still relavent.
----------------------------------------------------------------------------------------------------------------

I went ahead today and figured that I would try out
`Pinax <http://pinaxproject.com/>`_, seeing as it's been getting a
lot of good press in the Django community lately. The talk from
James Tauber at Djangocon was really good, and I certainly
recommend checking it out. This is going to be a basic introduction
to pinax.

First thing you need to do is grab the code from the pinax
repository.

``svn checkout http://svn.pinaxproject.com/pinax/trunk/ pinax``

Once you have the code checked out you are already half of the way
there. The only current external dependency is on PIL, the Python
Imaging Library. Django itself has this dependency for the
ImageField in forms. More than likely you already have this
installed, so it shouldn't be a problem. If not, that is the only
dependency of Pinax.

The directory structure of Pinax is pretty simple, copying from the
README:

::

    pinax/          contains a django project and templates
    external_apps/  contains external re-usable apps brought in via svn:externals
    local_apps/     contains re-usable apps that aren't yet externalized
    core_apps/      contains non re-usable apps specific to pinax site
    external_libs/  contains external libraries

The manage.py script inside of pinax links up all of the apps
correctly for you. So all you need to do to get started is go into
``pinax/`` and run ``./manage.py syncdb``. Then go ahead and run
``./manage.py runserver`` and you should see the pinax welcome
page! That is pretty awesomely simple to get up and running!

At this point, you now basically have an entire social application
working on your box. That is pretty damn impressive. The ``pinax``
directory is the project directory in this setup. Then, all you
have to do is swap out the templates, and you have your own site
with the exact same functionality.

The main use case for me with Pinax is to take the groundwork that
they're layed and throw a little bit of custom code on top. That is
the goal of the project. They are trying to give you a really solid
base that provides all of the generic functionality that 99% of
websites need. From this base it is then incredibly easy and fast
to get "yet another X site" going, wherein you then add the magic
that makes your site unique.

A couple days ago I actually took my first Django site I'd ever
done and converted it over to Pinax. It took all of about two
hours, with the awesome help of James Tauber and Brian Rosner in
the #pinax IRC channel on Freenode. They were helpful and I
bemoaned the lack of documentation, so that's why I'm writing this
up :) The site is now about 100x more powerful, and it's really
cool the power of Pinax there.

I want to talk about my philosophy behind the usage of Pinax. The
way that I've been thinking about it is basically it gives you the
groundwork with some nice default templates for the apps. The way
that you go about skinning the app is with the ``base.html`` and
``site_base.html`` in the ``pinax/templates/`` directory.
``base.html`` allows you to change the basic layout of the site.
This is where I changed out my CSS and Javscript code. Basically
you don't want to be changing any of the block tags here, just
HTML. I ripped everything out of the ``<head>`` except for
``<title>`` and ``{% block extra_head %}``. In the ``<body>`` I
basically ripped everything out, and put in my previous template,
then adjusted the block tags to make them appropriate.

One of the big gotcha's is the way that template blocks are named.
The pinax app templates are all coded to specific block names (as
they have to be), but if you're trying to use existing templates
then you might need to update your blocks if you want to be able to
have the backend stuff "just work". Here is a listing of the main
template block names and what they are. Remember, these simply need
to be present in your ``base.html``, and they will be given content
in ``site_base.html``.

{%block logo\_link\_image %} This is where your image goes (in the
header) {% block login %} Is where the login stuff goes (leave this
empty if you want to use their auth) {% block tabs %} Menu or tabs,
since it's only used in base and site\_base, this can really be
anything. {% block body %} This is where your main content goes. {%
block footer %} This is where you put the footer contents

A couple more gotchas:


-  The pinax manage.py does a decent amount of editing of your
   PYTHONPATH, so if you want to deploy it then you need to understand
   how this works. Check out
   `this post <http://www.20seven.org/journal/2008/09/pinax-setup-and-deploy.html>`_
   by Greg Newman for help with deployment!
-  The media in pinax is served out of ``pinax/site_media`` and in
   URLs are site\_media, so you need to put all of your css and
   javascript in there to get it working on the dev server. When you
   deploy this can go back to where it was previously (assuming
   previous install).
-  At the bottom of the pinax settings file, you see it does an
   import of localsettings. You can define your own settings than
   override the pinax ones in a localsettings.py file anywhere on the
   PYTHONPATH. This keeps you pretty safe from updating pinax and
   having it wipe your settings in the default settings file.
-  Remember this is still a work in progress, so the code will be
   updated (and probably break backwards compatibility) pretty
   frequently. Keep an eye on the
   `BackwardsIncompatibleChanges <http://code.google.com/p/django-hotclub/wiki/BackwardsIncompatibleChanges>`_

That's enough for today. That should get you up and running with
Pinax. I will be doing a screencast on this stuff sometime this
weekend, so look out for that. It should make this a lot more
obvious.


