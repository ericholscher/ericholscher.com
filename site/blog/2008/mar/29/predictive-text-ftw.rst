.. post:: 2008-03-29 02:47:29

Predictive text FTW
===================

I am just starting to use Gnome Do, and it's amazing. You hit
(windows key) + space, and it pops up a little window where you
give it commands. It tries to figure out what you mean when you
type a certain combination of words, and remembers what you usually
do on those combos, and does that in the future.

Eventually this could replace my entire need for a command line, in
a much more intuitive and user friendly sense. Getting instant
feedback, and seeing where you can stop typing into the command
gives you a "free hint" as to the minimum amount of typing required
to perform an action.

Presumably all actions can't be condensed down into a simple
combination of 3-4 keystrokes (the level where you see a noticable
time savings), so only the most commonly used actions will be
useful for this (the whole learning from you thing). I believe that
if somehow you incorporated context into the choice when you are
figuring out what to call from what combination of letters, you
could solve that problem....The hard part, defining the context.

I think that for example, since I'm writing a blog post, and I type
(after calling Gnome do) 'sp', then I want to check the SPelling of
whatever I'm typing. However, if I'm inside my mail application (or
G-mail if you want to get fancy), 'sp' means SPam, either that this
is spam, or call the spam dialog (or whatever I usually do when I
type spam(while viewing a message, or from the Start screen)). This
was a trivial example, but it lead to a very easy analogy. I feel
that this concept could be extended almost indefinitely, with the
only limitation being on how we define context, and how smart the
algorithm is.

If the algorithm gets good enough, you get to stop typing the
shortcut.

Edit: I feel this is the same way that spam filtering currently
works. Look at all of the incoming mail, and look for patterns in
it. If you dont' define an "action" and a "recipient", then the
input becomes one item, dependent on the context. I think you could
adapt a Bayesian algorithm to do this very thing. (Completely
ignorant on how Bayesian filters actually work, could be way off
point).

I also believe the major downfall of this idea is the concept of
"modes". Modes are generally a bad thing, and having all of this
context will confuse some people. If they don't understand the
different contexts, and doing the same thing has different results
sometimes, they will consider it "broken". I think the visual
feedback provided by the program will be crucial in how this is
interpreted. Having the feedback will allow the person to know what
the program is going to do. Also, some visual representation of the
current context (like a favicon in the corner) will allow them to
understand what context their in, and why the program is doing what
it is doing.


