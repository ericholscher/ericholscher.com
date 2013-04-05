:Date: 2008-02-19 09:35:18

Security Vulnerabilities on the Internet
========================================

I was reading an article on LWN about security vulnerabilities on
newly shipped machines. The qualm is that the same place that the
updates for vulnerabilities come from is the same place where you
are going to get infected. They are asking if there isn't possibly
a better way to do it. I think there is:

Don't let the user use network facing services until the system is
patched. When the user first gets the machine, don't let
ftp/ssh/etc. connect and give them a warning that they have to
update their systems before they can have access to the internet.
This will keep them protected until their machine has a chance to
update, with the update mechanism the only way for them to be
infected.


