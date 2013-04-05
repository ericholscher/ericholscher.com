:Date: 2008-04-08 10:23:15

Browser Login Discovery
=======================

There are some really cool ideas floating around the interwebs
these days, dealing with discovery of authentication. A lot of the
talk is about integrating OpenID into the browser, but I don't
think it needs to be limited to that. People are working on good
ways to auto-discover what the login end-points are on some pages.
So when I go to ericholscher.com, there will be a specific URL to
go to that will list the places where you can login, and what they
support. For example: /authEnds.xml would say that /account/login/
is the endpoint of login on my site.

I feel that this could be builtin to the browser. That wouldn't be
too hard, but I think we can do it with already existing
technologies. All of the major browsers currently support saving of
passwords for logins on a site. This means that they know what
page, and what domain they are on, for the correct login
information to be displayed. Why can't we make a Firefox extension
that does:

Land on a page. Search saved passwords for that domain. If a saved
password exists, display a small dropdown box to ask if we would
like to login (if we aren't already). Submit saved login
information to the saved login form destination. PROFIT!


