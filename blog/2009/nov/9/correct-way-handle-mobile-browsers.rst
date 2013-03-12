:Date: 2009-11-09 15:33:37
Correct way to handle mobile browsers
=====================================

At work, a lot of our sites have
`sweet <http://m.ljworld.com/marketplace/all/>`_
`mobile <http://m.kusports.com/>`_
`versions <http://m.lawrence.com>`_. The problem is how to educate
people of their existence. Currently we just have little ads that
show up on the site that promote the mobile site, which seems a
subpar solution. So I was tasked with doing providing a way to
redirect to the mobile sites. Luckily, as a lot of the time with
Django, most of my work was done for me.

`Minidetector <http://code.google.com/p/minidetector/>`_ is a
Django reusable app that allows you to know if a request is being
viewed on a mobile device. It provides a middleware and a view
decorator that sets a request.mobile variable to True if the
request is coming from a mobile device. It's
`method <http://code.google.com/p/minidetector/source/browse/trunk/minidetector/__init__.py#11>`_
of figuring out if a device is mobile is simple; It first checks
for a special Opera Mini header, then for WAP support, then finally
checks the User Agent against a
`list of known mobile strings <http://code.google.com/p/minidetector/source/browse/trunk/minidetector/search_strings.txt>`_.

So at work I have implemented a simple way to promote the mobile
sites through redirecting, allowing for a couple of different use
cases. This has lead to a problem that a lot of internet sites
face, and I haven't found a good solution to the problem:
**how do I redirect users to a mobile site?**

Obviously, **you should keep the request path**, so that when you
go to SITE/blog/2009, you get redirected to m.SITE/blog/2009. A lot
of sites actually chop off the request path, bringing you to the
mobile home page!

The use case
~~~~~~~~~~~~

The use case I am thinking about is a user that is using twitter,
and they click on a lot of links to a site, through a mobile
browser. They should be gentley introduced to the existance of the
mobile site, and have the ability to always have mobile links go to
the mobile site. However, they should also have the ability to say
'never show me the mobile site' as well.

Three approaches
----------------

No Redirects
^^^^^^^^^^^^

I see two basic approaches to the problem. The first is that we
don't automatically redirect anyone to our mobile sites. We are
able to detect if they are identifying as a mobile browser, so we
can show them a message about our mobile site, and let them
choose.

An option could be made to allow a user to say "Always redirect me"
if they enjoy usage of the mobile site. This seems to allow the
user to get expected behavior, but allow them to choose to use the
mobile site on their mobile device if they want. However, you run
into the problem of users ignoring the message about the mobile
site, or just not caring enough to click it.

Redirect once (opt in)
''''''''''''''''''''''

Redirect once is the plan where you redirect the user once, and
then set a cookie to never redirect them again. This allows the
mobile user to get a glimpse of your mobile site the first time
they visit, and can then choose to visit in the future.

You can also allow them to set a cookie to automatically redirect
all of their mobile requests in the future. This allows the user to
get a glimpse of the mobile site, and see if they want to use it.
Then based on this experience, they can choose to visit it by
default if they want.

Always redirect (opt out)
'''''''''''''''''''''''''

The third option is to always redirect mobile browsers to the
mobile site, with the ability to go back to the main site. You
would have a setting that the user could set to never be
redirected. This is more of a 'all mobile users will use our mobile
site, unless they choose not to'. I don't know if the mobile web is
quite there yet (for example, we don't have a mobile version for
every page), and it might lead to user confusion.

What do you think?
^^^^^^^^^^^^^^^^^^

I think that redirecting the user on their first visit on a mobile
browser is a good idea. This introduces them to the mobile site,
and by setting a cookie on that redirect, you can be sure that they
won't be redirected again. Then you can have an opt in cookie, that
basically says redirect me every time. This makes it do what people
expect most of the time, while still allowing the choice to always
be redirected.

Have you implemented mobile redirecting before on a site? How have
you solves this problem? Am I missing some obvious solution that
handles all these cases gracefully?


