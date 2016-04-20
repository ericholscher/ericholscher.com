.. post:: 2010-11-15 18:28:14

Correct commands to check out and update VCS repos
==================================================

In my work in `ReadTheDocs <http://readthedocs.org/>`_, we now
support all of the major VCS repositories: svn, bzr, hg, and git.
At this point in time we're only checking out the repos to their
default branches, and then trying to trying to update them again to
another revision. While writing this code I have had at least 3
different bugs that caused the repos not to be updated correctly.
So I'm going to detail here the exact code that allows me to do
this for each of these types of repos, hopefully so that when you
or I need to do this in the future, we can at least start from
here.

Let me know if any of these are wrong, because they probably are.

Git
---

Checking out a repo:

::

    git clone --depth=1 <remote_url> <local_filepath>

Updating a repo:

::

    git --git-dir=.git fetch
    git --git-dir=.git reset --hard origin/master

I'm specifying the --git-dir here because my master repository is
git as well, and I don't want to risk the git commands cascading up
and applying to the outer repository. I'm also specifying --depth=1
so that I don't clone the entire repository, but only the latest
commit. I don't need the history, so I'm doing this. As you can
tell, I'm more familiar with git than the other VCS systems here.

Svn
---

Checking out a repo:

::

    svn checkout <remote_url> <local_filepath>

Updating a repo:

::

    svn revert --recursive .
    svn up --accept theirs-full

I ran into problems here where I was calling revert without
recursive and it wasn't doing anything! You need to do this from
the top-level of the repo, and it will make sure all the state
lower in the repo is reverted.

Bzr
---

Checking out a repo:

::

    bzr checkout <remote_url> <local_filepath>

Updating a repo:

::

    bzr revert
    bzr up

This one is nice and easy.

Hg
--

Checking out a repo:

::

    hg clone <remote_url> <local_filepath>

Updating a repo:

::

    hg pull
    hg update -C .

Again, a slightly different syntax to make sure that you're
deleting all the files, and with the update command.

I hope this helps people in the future at least get to the point
where they can pull down code and update it. My next task is
figuring out how to support branching in all of the different
repositories which is going to be fun, because they have different
filesystem structures.


