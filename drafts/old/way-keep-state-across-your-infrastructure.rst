:Date: 2011-07-05 16:42:06

A way to keep state across your infrastructure
==============================================

At work we have been needing something along the lines of what I'm
going to describe for a while. I'm guessing it exists somewhere,
but I haven't been able to find it. If it doesn't exist, then I
will be building it, but I'm hoping that I won't need to.

A State Database
~~~~~~~~~~~~~~~~

The main functionality I want is a way to keep state of all of the
applications running across our infrastructure. This Includes:


-  What machines we have
-  What the hardware configuration is on those machines
-  What services we have
-  What machines those services are running on
-  The current version of all deployed services
-  Logs of previous deployment/chef runs
-  Display of errors from services
-  Locking of deployments

--------------

Locking of deploys:

We often have times when we have changes the depend on a migration
or something else in our repos. We need to be able to have the
tooling actively disallow actions that will break our systems.
Unlocking should be simple Logs of deployments:

This will be a way to easily browse/search deployments, so you can
have a nice overview of the changes on our machines over time, as
well as the current state Display of errors:

This ties in with the new redis error/monitoring handling system.
This will be a simple display of the data, again for the visibility
of it over time.

Design
======

Gathering of Data
-----------------

Getting the data about what services are active and where they are
running is going to be an interesting part of our architecture.
Since we've moved to a mostly standardized set of service
deployments, this should ease the load.

Each service start/stop script will phone home with where it's
running, and what action happened. eg. "offline-tasks was started
on worker-0" Each deployment tool, airchef/deploy, will phone home
with what it's deploying against. eg. "deploying version 20110502
of airship to web-0" To bootstrap the data gathering, we will need
a check\_mk style process discovery

Considerations
--------------

At the beginning, this will be a place to keep state of our
infrastructure. What our stack looks like at current. Over time,
this will probably evolve to keeping configuration information
inside. For example, we might have a model that allows us to change
the threshhold that our error system uses to page vs. email
someone.

Concerns
--------

We may end up with a design that requires a seperate Model for each
type of service we run. As we start adding more and more
information about the services past simple operations level stats,
the services start to wildly diverge in what we care about. For
example, in postgres we might care about how much virtual memory
it's configured to use vs. what the machine it's running on has.
Whereas with Helium, we care about the stack size of the process.

We have servers still running in EC2 that won't easily be able to
communicate with this system.

Feedback
--------

I'd love to hear people's thoughts on this. Either in comments, or
in person.


