.. post:: 2011-01-23 21:25:40

Using Reviewboard with Git
==========================

`Reviewboard <http://www.reviewboard.org/>`_ is a great tool for
managing the process of Code Reviews. It has pretty good git
support, but it might not be obvious what the best way is to use
it. At work, I have a couple of different ways of pushing up code
for reviews, which I'll talk about.

This guide is assuming you are using your own bare repositories, on
the server hosting the Reviewboard instance. It's mainly here so
that I can remember how to do this next time I need to. Also,
thanks to `Travis Cline <http://traviscline.com/blog/>`_ for the
initial pointers for this post.

Setting up Reviewboard
----------------------

Once you have Reviewboard installed, you need to add a Repository
in the admin, which is located at
``/admin/db/scmtools/repository/``. The required fields have the
following values:


-  Name: The name of the project
-  Hosting service: Custom
-  Repository type: Git
-  Path: The path to the local checkout of the git repository (ex.
   /var/lib/git/name)
-  Mirror Path: The **Url** to the repository (ex.
   ssh://git@your.server.com/var/lib/git/name)

The
`Repository Documentation <http://www.reviewboard.org/docs/manual/dev/admin/management/repositories/#git>`_
has more about why you need this screwy configuration.

post Review
-----------

Before we get started, you're going to want to get the
`post-review <http://www.reviewboard.org/docs/manual/dev/users/tools/post-review/>`_
tool that works along with Reviewboard. The easiest way to get it
is to ``pip install RBTools``.

Pointing to the right Reviewboard Instance
------------------------------------------

The easiest way to make sure your pointing at the right Reviewboard
instance is the *.reviewboardrc* file in your home directory. You
only need to add one line to that file, which is:

::

    REVIEWBOARD_URL = "https://path.to.your.instance" 

If you are working with multiple instances that map to different
repos, you can set the Reviewboard instance for the specific repo
as well:

::

    git config reviewboard.url https://path.to.your.instance

Reviewing a Branch
------------------

Alright, now you are all setup to start posting reviews. The
easiest way to do that is to branch off of master, and start
committing. If you are following something similar to
`this awesome branching model <http://nvie.com/posts/a-successful-git-branching-model/>`_,
this should be your normal workflow. Once your branch is ready to
be merged back into your project, you want to get it reviewed. You
can send a review equivalent to "this branch diffed against master"
like so:

::

    post-review --guess-summary --guess-description

Reviewing one commit
--------------------

Another thing I find myself doing a lot is working on my master,
and only having one commit to review. In theory this should
probably be done on a bugfix branch, but such is life. There are
other good use cases for only reviewing the latest commit as well.
It's done like so:

::

    post-review --guess-summary --guess-description --parent=HEAD^

Reviewing arbitrary number of commits
-------------------------------------

It's also possible to review any number of previous commits. It
looks a lot like the previous command:

::

    post-review -o --guess-summary --guess-description --parent=HEAD~4 #To review last 4 commits.

If you are familiar with git, you will understand that there is a
lot more that you can do with the --parent argument. I'll leave the
possibilities up to your imagination.

Other useful post-review flags
------------------------------

The are a couple of other useful post-review flags, that I use from
time to time.


-  -d This basically outputs all of the git commands that
   post-review is using to generate the diffs. It's a great way to
   figure out what's going wrong when it can't find a diff.
-  -o: This opens a web browser to the posted review once it's
   done. Great for easily making the review public.

I hope this makes it a little easier for you to set up a git
repository with reviewboard.


