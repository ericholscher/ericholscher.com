:Date: 2009-11-10 18:46:16

What they didn't teach me in college
====================================

**Updated at the bottom of the post.**

**Warning**: This is a bit of a brain dump.

In the software industry there is a lot of back and forth about the
value of a college degree. This post won't go into that too much, I
just want to talk about the notable things that were left out of my
Computer Science degree. Mostly things that are used in the day to
day environment outside of a university, but aren't used
extensively inside of them.

My degree was a more classical CS degree, which focused on
algorithms and theory. However, there was a decent bit of actual
"real world" knowledge that they tried to impart. After being at a
real job for over a year, I think it is interesting to look back on
what I wasn't taught.

Software testing
^^^^^^^^^^^^^^^^

In college, the concept of testing was basically 'compare your work
against this expected output file'. Sometimes that job was
automated, other times it wasn't. There was absolutely not concept
of an automated test suite. However, I think that this may be a
limitation of the semester long class idea. A lot of the value from
testing comes from things that are real (production, refactoring)
or looking back at code that you wrote a long time ago. I have a
lot more thoughts on this, and it deserves it's own post. However,
it was certainly a glaring part of what I do now that I had no
experience with out of school.

Version Control
^^^^^^^^^^^^^^^

In the classes that I took, we simply submitted the work to the
teacher and that was that. We didn't check it into a repository, or
even version the work we were doing locally. At the time the whole
DVCS movement wasn't quite as big, so I can imagine a lot more
people doing local versioning now. I think that the fact that
viewing other students work is sometimes considered "cheating"
(which is silly), makes it difficult to have a shared repository
for all students.

A big problem with universities is that knowledge the old mindset
that sharing knowledge is cheating. Luckily mine was a bit more
enlightened, but I think having a shared repository of code would
make this philosophy a bit too "real".

Web development
^^^^^^^^^^^^^^^

We had optional classes that offered PHP/MySQL based website
making, but nothing in the curriculm about web development. It
seems that in this day and age, so much of what we do is centered
around the internet that ignoring it in the classroom is silly.
That may be the fact that I now do web development, but I feel that
someone coming out of a Computer Science degree not understanding
the basics of Web Development is a bit silly.

Bug Tracking / Maintenance
^^^^^^^^^^^^^^^^^^^^^^^^^^

Our code in university only had to be written once. There was no
concept of going back and looking at old code and fixing it. It is
one of those realities of everyday work that is totally ignored by
universities. I think this one may be a bit hard for them to teach,
but mostly because of systematic problems.

What to do about it?
~~~~~~~~~~~~~~~~~~~~

I think that a lot of the problems come from the
**Single Semester Class Paradigm**. You do some kind of programming
for a class, and then it disappears into the ether never to be seen
again. A lot of the value and reality of coding is that you write
code and then have to keep changing it and making it work.

Imagine if you were tasked with writing code your first year. This
code was checked into the schools version control system in a
branch of that class for that semester. Then in your following year
you have a class that recalls that code, and you update it with
some new technique you have learned. You are a bit dismayed at how
badly you used to code, and how hard it is to understand.

Then your third year you go back to your code and have to write
tests for it. The class that you had taken the year before is
tasked with taking your code and adopting it for a new purpose.
They file bug reports on your code, and your commits fix their bugs
and contain tests. This allows you to
**learn how to do maintence, interact with a bug tracker, and write tests.**
For the younger students, it allows them to figure out how to write
good bug reports, and interact with other coders.

Conclusion
----------

I think the really important part is that your code doesn't die.
You write code in a class, and it is used by other people, or it is
kept and brought back up later. This you as a student to reach the
"aha" moments where you see how much you have learned in the past
year, by how much your old code sucks. It provides a lot more
knowledge of useful tools and real workflow.
**Without too much effort, it makes the educational nature of college more valuable and more realistic.**

I would be interested to hear people's thoughts. If you got a
degree, did they do anything similar to this? Are you using up
tools and practices?

As a bonus, I think that a lot of the parts missing in universities
are missing in good real world software shops. There are a lot of
software houses that don't use version control, write tests, or use
a bug tracker. This strikes me as crazy.

Update (11-11 13:20)
--------------------

A lot of people in the comments have said that computer science is
more about math and algorithms, and that it shouldn't teach you
these things. Most people who take this stand say that you
shouldn't be teaching programming at all, and it should be a more
math based education. I agree with that point of view, but that
isn't how CS is taught these days.

CS students are doing a lot of programming, and performing tasks
that could be made better with these use of tools.
**I am simply arguing that if you're going to be teaching programming to CS students, you should also teach them the best practices and tools associated with that craft.**
It would only take 1 or 2 classes out of a CS curriculum full of
theory and math based classes.


