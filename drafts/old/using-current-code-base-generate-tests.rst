.. post:: 2008-10-07 13:03:08

Using the current code base to generate tests
=============================================

So lately I have been doing a lot of thinking about how testing is
done on software applications. I have tried some Test Driven
Development, and I have been employed writing tests for probably
the largest Django code base in existence (Ellington). I think that
a lot of people are in the situation of having a code base with
little to no tests. I think that there is immense value in the
ability to get tests out of that code base. I have been doing some
thinking about how to turn this code base into tests.

A lot of the thought that I've put into testing goes into what
exactly there is that you need to test. What edge cases and crazy
input and series of parameters must I account for that will make
the program crash? How can I account for the entropy of the earth
in the form of input to my program. I feel that these are indeed
serious and important questions. But alas, the realist in me wins
out and then I think: the range of input that my program sees is
limited to that set. Simple and obvious, but alas, how do you get
that input set?

This is where the idea of testing the code that you current have
comes in. In a lot of circumstances this approach isn't a great
idea, but I think in certain subsets that it works well.. Trying to
take every line of code executed and interpreting what all of the
variables are is really hard. Using a debugger or some kind of
coverage/tracing tool to do this might work, but it is not the
answer. I think the real value comes in taking a part of the code
that you have, that can (hopefully) be stuffed into a microcosmic
hole, and evaluated easily.


