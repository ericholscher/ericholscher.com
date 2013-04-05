:Date: 2009-01-21 15:24:04

Review of Pro Django by Marty Alchin (1/2)
==========================================

5 second review:
**Reading this book will make you a much better Django Programmer.**

--------------

In full disclosure, I was sent a review copy of this book by the
publisher, but I had already pre-ordered it on Amazon, and the copy
I am reviewing is that copy. The review copy is now the office copy
:)

I will do an overview, and then a specific breakdown of what I
thought after reading each chapter. This is currently only the
first half of the book, but the book is already worth it's price
(perhaps in gold). This covers chapters 1-6, which is basically the
normal URLs/Models/Views/Templates stuff. The later sections appear
to cover more specialized and advanced use cases. You can
`download the table of contents <http://www.apress.com/book/downloadfile/4247>`_
also.

Also note, that you can see my further reviews and some other
peoples over on
`Readernaut <http://readernaut.com/books/952/notes/>`_

Overview
--------

Pro Django is certainly not for the beginner. It assumes a pretty
decent amount of Django experience (or at least the ability to
learn/reference it easily). I think that this is a good thing,
because it doesn't get bogged down in silly details and
explanations when what we want is upper level content. If you have
been doing Django stuff for a couple months, I think this book is
amazingly good at pushing you to the next level of knowledge in the
field.

I certainly recommend reading James Bennett's Practical Django
Projects (once version 2 gets released) before this one, as it is
an easier introduction. These two books together provide an amazing
1-2 knockup punch to getting you to be a great Django developer.
Now onto the review.

Chapter 1: Understanding Django
-------------------------------

This chapter goes over the basics of Django and the philosophy that
it has. It is a great introduction into how to be a good member of
the Django community. It is available for free on the
`Apress website <http://www.apress.com/book/downloadfile/4246>`_,
and I recommend reading it, because I felt inspired by the
prologue, and I think that Marty explains the value of the
community around Django very well.

Links from the books pages are provided as links from
prodjango.com, which is nice at first, but the obfuscation of the
URLs is a pain later in the book. It is used as a way to hide
information ("The django irc channel", with a link) instead of
#django in irc.freenode.net. Also, I have read some of the URLs
linked to, but knowing where they go helps me decide if i need to
read them.

Chapter 2: Django is Python
---------------------------

With one of the best descriptions that I have read of metaclassing
in python, this chapter starts off guns a-blazing. It tries to show
some of the more advanced Python features that Django uses, and
stresses that Django is merely Python. I loved the explanation of
the gentlemen's agreement on interfaces, including file-like
objects. The explanation of metaclassing is finished up with a
great example of implementing a plugin system for a password
validator. The code ends up being around 40-50 lines, flowing
through my brain like a river, and beautiful. It was also explained
in a way that allowed me to see the abstract value of the ideas,
and not simply how it is useful in this specific implementation.

It also includes a really heady implementation of decorators that
blew my mind a little bit. With my current intermediate level of
python knowledge, it provided a reference for things that I mostly
knew, and went into depth in the parts that were in need of it. A
great start to the book. As of page 45, my brain is already going
full throttle and I'm looking forward to what this book has in
store.

Chapter 3: Models
-----------------

I found this chapter to be a little less amazing than the previous,
but still solid. It didn't quite flow as well for me, and I had to
think about things a lot more. I didn't have a great understanding
of how all of the subject matter fit together. This might just be
the fact that I'm not as acquainted with the topics.

It has a cool example of creating a field that stores pickled data
and returns it as a normal object. As the chapter progressed the
value of the explanations earlier in the chapter start to gel a
bit, but not totally. I think that this is one that re-reading, at
least for me, will be really valuable after I'm finished. It
provided a great reference to all of the different fields, and why
we should care about them. I really like the continuing theme of
"this is a brief explanation of what X is, and this is an in depth
explanation of why you should care"

Chapter 4: Urls and Views
-------------------------

This chapter does a good job of showing how URLs and Views are
inextricably linked. Your URLConf basically just hands off data to
views, and it goes over all the interesting things that you can do
in this space. It flowed well, was just the right length, and left
me really appreciating the value of decorators around views.

The concept of using a decorator on the view function in the
URLConf, instead of around the view definition, is novel. The
ability to manipulate the arguments to the view in the URLConf
file, returning objects instead of strings to the views is very
powerful. Using decorators to abstract boilerplate is a really
powerful pattern.

The explanation of views and making them more generic was good, but
I already knew it from Practical Django Projects. This obviously
lead into generic views. He also discussed using a Class as a view
(and the downside of trying to reverse() it), but it was lacking a
discussion of Class-based Generic Views which I thought was coming.
This is going to be implemented by 1.2, so it might have been a
good time to at least mention it.

Chapter 5: Forms
----------------

This chapter is not as interesting to me, because I don't plan to
be doing a lot of work on front end forms. However, there is still
a great explanation of the way that forms work on the backend
(almost exactly like models). The harsh warning about verifying
user input is good, because user input is indeed evil.

In example at the end of the chapter, Marty goes through how to
create a form that can be saved and restored, no matter what the
contents. It ends up being implemented in a decorator, which blew
my mind. All you have is a view that handles a valid form, and a
decorator gives you the ability to save and resume that same form,
simply by posting an md5hash to it. Pretty Crazy. It also goes into
Widgets and how to create your own to display forms. There is a bit
of a lack of how to include Javascript and CSS inline in your
forms, but talks about how to embed custom attributes. Also, there
is no mention of creating forms from Models! I feel that this is
probably one of the most common operations I do with forms. This
might have been excluded because it is already well known and
un-interesting.

Chapter 6: Templates
--------------------

This chapter explains one of the simpler parts of Django. It is
pretty neat that you can understand pretty much how the entire
template system works in a chapter of about 20 pages. I knew a
decent bit about it before, but this chapter certainly made my
knowledge more concrete.

There is a really neat example at the end of the chapter about
writing themes for a website. It goes through a really in depth
usage of the Template system, including introspecting nodes. I've
needed to do something like this for my own stuff, and this example
is invaluable. It also talks about how to easily create tags and
filters by yourself.

At this point I'm at page 163 of around 300. There is still a ton
of great knowledge in this book, and I'm excited to read the rest
of it.


