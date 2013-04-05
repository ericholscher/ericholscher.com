:Date: 2010-06-23 17:17:49

Large Problems in Django, Mostly Solved: Remote Execution
=========================================================

[This is part of the
`Large Problems in Django Series <http://ericholscher.com/tag/largeproblems/>`_,
see previous entries about:
`Delayed Execution <http://ericholscher.com/blog/2010/jun/23/large-problems-django-mostly-solved-delayed-execut/>`_,
`Documentation <http://ericholscher.com/blog/2010/feb/5/large-problems-django-mostly-solved-documentation/>`_,
`APIs <http://ericholscher.com/blog/2009/nov/11/large-problems-django-mostly-solved-rest-api/>`_,
`Search <http://ericholscher.com/blog/2009/nov/2/large-problems-django-mostly-solved/>`_,
and
`Database Migrations <http://ericholscher.com/blog/2009/nov/6/large-problems-database-migrations/>`_]

Executing code on a remote server doesn't really seem to be a
problem with Django, however it is a problem with Deployment. While
I don't want to say that Deployment is a mostly solved problem, the
part where you need to execute tasks on a remote server is. This is
done with `Fabric <http://docs.fabfile.org>`_, which defines itself
as a "Python library and command-line tool for streamlining the use
of SSH for application deployment or systems administration
tasks."

Why use Fabric
--------------

It's Python
^^^^^^^^^^^

At work we were previously using capistrano for our deployment, but
it felt very magical and was in Ruby. Now that we have switched to
Fabric, our deployment scripts can now be hacked on by all of our
developers. When we were using capistrano it felt we needed to
remove features to get it to be simple; Fabric starts out simple
and lets you build up your own complexity. I prefer this approach
more, and the move to Fabric has made me happy.

It being Python also allows you to import all of the libraries and
you know and love into your Fabfile. For example, you can use
Django's ORM to manage a list of hosts that you need to connect to
if you really wanted to.

It's not totally solved
^^^^^^^^^^^^^^^^^^^^^^^

I have 2 main problems with Fabric at current. One is that it
doesn't support SSH Agent Forwarding, which allows you to forward
your SSH credentials to your remote servers. This can be a pain if
your deployment is using your local SSH keys. The other major
weakness is the lack of concurrent execution. This isn't a problem
for me, as I usually have at more 8-10 servers to push code to, but
if you have a lot more servers I could see this being a major pain
point.


