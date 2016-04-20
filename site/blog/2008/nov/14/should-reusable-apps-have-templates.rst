.. post:: 2008-11-14 15:59:51

Should reusable apps have templates?
====================================

There is a debate among the Django community about whether people
should include templates in their reusable apps.

The arguments for including them are generally that it is nice to
simply install the app and have things just work. This is a really
nice feature to not have to dig through the code looking for
template names and context variables. Then creating your own
templates for code you didn't write. I am usually of this
persuasion, because it's really annoying to have a big up front
cost to begin using an app.

I think that an app that comes with no templates is going to be
used less. Some people might think that it a good thing, but I
think it is better for an app to be used as much as possible. I
know that I personally have tried to check out an app, and given up
because there are no templates. It is a pretty sizable mental
hurdle (and a decent bit of work) to get some template to even test
the functionality. Sure, you can look at the code, but that isn't
nearly as quick and easy as simply plugging the app in a testbed
and seeing what happens.

The argument against it are that there is no possible way to know
how your users are going to use your templates. They will file bugs
against the default templates because they don't work the way they
want them to. I understand this point of view as well. There is no
possible way to ship a set of default templates that will work for
everyone, every time. So then the question is, what do you do?

I think that there is a nice middle ground that we can achieve.
Reusable apps should ship with templates, but they shouldn't be in
a place where they are run by default. I say that they should ship
in the docs/ folder. This way they are seen as a reference
implementation. A user doesn't automatically get them to run, and
if they move them out of the docs folder, then they know it is a
reference implementation instead of something that is meant to work
for them every time.

I think that this solved the problem by letting people evaluate
apps with templates that show it's basic functionality. But it puts
a slight barrier between seeing them as templates that should work
for me. They should be seen as a reference, and as so they can go
in the docs/ directory. Of course, if you want to ship your
templates in the templates/ dir inside the app, that is cool. But I
think that apps that have views, should have templates to go along
side them, even if they're not 'installed' by default.

Yes, this is a half assed post. I was going to write a longer one,
but there is a free
`Robert Randolph <http://www.robertrandolph.net/>`_ show in
Lawrence tonight. This is scheduled to post at 11pm, so if I don't
have time to post, you will get this awesome half assed one ;)


