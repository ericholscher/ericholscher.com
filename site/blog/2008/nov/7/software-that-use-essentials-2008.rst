.. post:: 2008-11-07 17:13:36

Software that I use: Essentials 2008
====================================

Stealing an idea/meme from
`Mark Pilgrim <http://diveintomark.org/archives/2008/10/28/essentials-2008>`_
I'm going to do a post of the essential software that I use in a
day to day basis.
`Justin <http://justinlilly.com/2008/11/02/most-used-programs-an-index/>`_
also did a similar post a couple days back. I think it is
interesting to talk about what kind of tools you use, because it
gives people an understanding into how you work, and also some
pointers at stuff that maybe they too should be using.

I'm going to split my lists up rather arbitrarily, so here goes.

On the Server
~~~~~~~~~~~~~


-  `Slicehost <http://slicehost.com>`_ - I love these guys. I've
   had my slice for a good 8 months, and they are hands down the best
   web host I've ever had. Respond to tweets or e-mails within an
   hour, great customer support, and rock solid hardware. I highly
   recommend them for any sysadmin minded developer. It's a great way
   to learn a little sysadmin skills, have root on a fast box with a
   fat pipe, and is generally just awesome. Best part: $20 a month for
   256MB of RAM.
-  Vim - The venerable text editor and perennial love of my life.
   It's great for making little quick fixes to files, and the key
   bindings are burned into my brain.
-  `Django <http://djangoproject.com>`_ - Big surprise there. This
   site is running on Django, and I work and post mostly about it. Yet
   it goes to show how good the software is that I still love it, even
   when it's my day job.
-  `Varnish <http://varnish.projects.linpro.no/>`_ - This is a
   really nice "state-of-the-art, high-performance HTTP accelerator".
   It sits in front of my Apache pages and caches them, making the
   site blazingly fast. At least that's what it claims. My sysadmin at
   work recommended it and it's really nice.
-  Apache/`mod\_wsgi <http://code.google.com/p/modwsgi/>`_ - The up
   and coming way to run your Django apps on Apache. It's a great way
   to host, and makes configuration and management a lot easier.
   Again, sysadmin recommended, but IANASA (I am not a sysadmin)
-  `Ubuntu <http://ubuntu.com>`_ - My favorite Linux operating
   system these days. I run it for all my Linux needs, desktop and
   server. It makes everything really easy, and I understand it well
   since I've been running it for a couple years.
-  `screen <http://www.gnu.org/software/screen/>`_ - Screen is the
   sysadmin and programmers best friend. If you aren't using it on
   your remote servers, you're doin it wrong. It gives you some really
   nice ways to attach and detach long running processes (think IRC
   clients, DB migrations, etc), basically gives you a terminal window
   manager, and lots lots more.
-  ssh - Everyone favorite work horse. I use it for the usual
   things like system administration, but also some other neat things
   like SSH Tunneling, X forwarding, and as a poor mans VPN.
-  bash - I don't use any of those fancy shells out there. bash
   with screen is more than anyone should need.
-  `Fabric <http://pypi.python.org/pypi/Fabric/0.0.3>`_ - I am just
   starting to use this as a deployment tool for my Django
   applications. It makes life a lot easier and I'm really enjoying
   being able to automate simple repetitive tasks.
-  `git <http://git.or.cz/>`_ - I jumped on this bandwagon a week
   or 2 ago as well. It seems to be becoming the defacto DVCS tool for
   the Django community, and `Github <http://github.com>`_ is a really
   neat tool.
-  `Feedburner <http://www.feedburner.com/fb/a/home>`_ - This is a
   neat app that gives you services associated with RSS feeds. They
   tell me how many subscribers i've lost with my pointless ramblings
   on a daily basis :). I also use it as an abstraction above a feed
   url, so if my feed url scheme changes on the backend, I just update
   Feedburner to point to the new one and nobody has to change their
   feeds.

On the Desktop
~~~~~~~~~~~~~~

A note about my development environment. I try to only use tools
that are available on Linux and OS X, because that gives me the
mobility of being able to develop easily on both. Things like
MacVim are neat because they give you Vim but in a Mac friendly
way. However, software like Textmate and Coda I don't want to get
used to, because I think that Linux is the better choice for
developing software (at least for Django/Python).


-  `Firefox <http://getfirefox.com>`_ - The awesomest web browser
   ever. I don't know what we did without Firebug. It's great for web
   development, and lots of other stuff. The extensions community is
   great, and they do some good work.
   `Vimperator <https://addons.mozilla.org/en-US/firefox/addon/4891>`_
   is also really neat, it gives you Vim key bindings in Firefox ;)
-  `Komodo Edit <http://www.activestate.com/Products/komodo_ide/komodo_edit.mhtml>`_
   - The 5.0 version of this just got released, and I'm loving it.
   This is the open source and free version of the great Komodo IDE,
   from Activestate. I use it mostly because it's cross platform, and
   because it has some great Vim key bindings. I get the convinces of
   an editor, with good key bindings, and not being tied to any
   platform. I highly recommend it for anyone doing web development,
   and I'm even considering getting the IDE version which includes
   Source control management and debugging support.
-  `Xchat <http://www.xchat.org/>`_ - The venerable IRC client.
   I've been using it on Linux since I began using it, and the Aqua
   port for OS X is a little lacking, but still has everything you
   need.
-  `Adium <http://www.adiumx.com/>`_/`Pidgin <http://pidgin.im>`_ -
   The greatest piece of IM software to be invented. Called Pidgin on
   Linux, they provided the libpurple library, which is an abstraction
   of their IM connectivity layer. On OS X, Adium uses this and gives
   you a great UI on top. You can connect to lots of IM networks, all
   in one buddy list.
-  `Quicksilver <http://docs.blacktree.com/quicksilver/quicksilver>`_/`Gnome-do <http://do.davebsd.com/>`_
   - These launcher-style programs are so integrated into my everyday
   habits, I don't know how we lived without them. Quicksilver is the
   original version (that I know of), and Gnome-do is a well done
   Gnome version of the same ideas. They allow you do basically run
   without an Applications menu and just use a key command based
   launcher to do things. If you're not using one, I highly recommend
   checking them out.
-  iTunes/`Amarok <http://amarok.kde.org/>`_ - Everyone needs a
   good audio player. iTunes and Amarok are the best of breed for OS X
   and Linux respectively. Amarok is a KDE project, but I use it
   because it is a damn fine media player.
-  Terminal.app/gnome-terminal - I used to use iTerm on OS X, and
   there are still a couple of small things I like better on it (key
   bindings mostly). However, Terminal,app has gotten nice enough that
   I can use it, and it makes it easier to use other people's
   machines. Gnome-terminal is my choice on Linux, because it's a
   great one.
-  `vlc <http://www.videolan.org/vlc/>`_/`mplayer <http://www.mplayerhq.hu/>`_
   - For your video playing needs, you can't beat these two open
   source projects. They both will play almost anything, and I tend to
   use vlc on OS X, and mplayer on Linux, because of their respective
   UIs. If these won't play a media file, then almost nothing will.
-  `sshfs <http://fuse.sourceforge.net/sshfs.html>`_/`macfuse <http://code.google.com/p/macfuse/>`_
   - I love sshfs. It uses the FUSE library to mount an SSH drive on
   your current filesystem. There are OS X and Linux versions of it,
   and it is insanely useful.
-  `Skitch <http://skitch.com/>`_ - This is a really nice tool for
   sharing images and screenshots. It allows you to capture them super
   simply, annotate them, and upload them for others in around 5
   clicks. Great for showing website brokenness and other general
   stuff.
-  `Twitterrific <http://iconfactory.com/software/twitterrific>`_ -
   A pretty good Twitter client for OS X. It isn't amazing, but it's
   good enough and it does what I need. I love me some twitter, and
   this keeps my addiction fed.
-  `iShowU <http://store.shinywhitebox.com/home/home.html>`_ - I
   use this to create those screencasts that you all love :) It's a
   great program for doing screencasts, it's pretty simple, and does
   one thing well. I'd also be curious if anyone has any free
   alternatives, or linux based screencasting apps that they can
   recommend.
-  `Transmission <http://www.transmissionbt.com/>`_ - A bit torrent
   client for the mac. It's simple and easy to use, I like it a lot.
   It was actually ported to Linux and included in Ubuntu I do
   believe.

Apps in the Cloud
~~~~~~~~~~~~~~~~~


-  Google Reader - My current RSS reader. It's simple, does what I
   need, and generally stays out of my way.
-  Gmail - My e-mail client of choice. It's just a great way to do
   e-mail, I can access it from everywhere, and the spam filtering is
   amazing. I've gotten like 1 ever, and my e-mail is right on the
   bottom of this site :)
-  Google Analytics - What seems to be the big name in web
   analytics. Yahoo has a
   `competing offering <http://web.analytics.yahoo.com/>`_ that they
   launched recently, which has kicked google into gear with new
   features. Competition is a great thing, and we'll see if it's worth
   switching over time, but for me it's still Analytics.
-  `Delicous <http://delicious.com/forsaken>`_ - The great bookmark
   sharing service. I was using Ma.gnol.ia for a while, but most
   people at work are on delicious. I recommend culling a small
   network of like minded folk, and getting your network links in RSS.
   It is by far the best link feed I have, and beats any impersonal
   aggregator.
-  `Last.fm <http://www.last.fm/user/i7981>`_ - I have over 32,000
   tracks 'scrobbled' on their site. They know my taste of music
   scarily well, and it's just really neat data to have in public.
   Plus they have some good APIs and feeds for accessing it.
-  `Pandora <http://pandora.com>`_ - These guys have a brilliant
   music recommendation engine. I am constantly delighted and amazed
   by what music thay choose to play. You give it an artist and it
   plays similar music. I use this when my library is becoming stale,
   or I'm looking for good new music.
-  `Facebook <http://facebook.com>`_ - I like it less and less
   everyday, but the utility in it can't be denied. Keeping track of
   far away friends, old friends, and generally most of the people I
   know socially is key. I really hate how all the data is locked up
   and all that, but everyone uses it, so there isn't much you can do.
-  `Programming Reddit <http://www.reddit.com/r/programming/>`_ -
   I'll check out the front page something, but the programming
   section seems to have some quality content a majority of the time.
   The `Python <http://www.reddit.com/r/python/>`_ and
   `Django <http://www.reddit.com/r/django/>`_ sections also have a
   decent signal to noise ratio.
-  `Hacker News <http://news.ycombinator.com/>`_ - I don't use
   reddit or HN that much, but Hacker news consistently has
   interesting information. I don't get the RSS, but they are really
   nice resources when you're bored, or looking for inspiration.
-  `Kayak <http://kayak.com>`_ - The best way that i've found to
   find flights online. Great tool for traveling.
-  Craigslist - Everyone's favorite classifieds site. I bought a
   Wii for super cheap recently with lots of games. The free section
   is also a favorite.
-  `Freecycle <http://www.freecycle.org/>`_ - A personal favorite.
   It's like recycling, but people give stuff away for free. It's like
   craigslist's free, but generally less sketchy. This is how we got
   most of our furniture in college, it's generally in good shape.
   People are usually just happy to see it go away to good people.
   Highly recommended!

Dot files
~~~~~~~~~

`Brian <http://oebfare.com/blog/2008/nov/06/essentials/>`_ also
posted this similar post yesterday. He included his dot files, so I
figured I would share mine.

This is my .bash\_profile:

::

    export PYTHONPATH=$HOME/Python:$HOME/Python/Modules
    export PATH=$HOME/bin:$PATH
    export DJANGO_SETTINGS_MODULE="settings"
    export HISTFILESIZE=10000000
    set -o vi
    export EDITOR=vim
    export PS1="[\u@\h:\w]$ "
    
    alias rs='/usr/bin/python ~/EH/manage.py runserver 67.207.139.9:8000 --settings settings_debug'
    alias mp='/usr/bin/python ~/EH/manage.py'
    alias sp='/usr/bin/python ~/EH/manage.py shell_plus'
    alias bkup='/usr/bin/python ~/EH/manage.py dumpdata'
    alias destroy-pyc='find . -name \*.pyc -delete'
    alias dj='cd ~/Python/Modules/django-trunk'
    alias a2='sudo /etc/init.d/apache2 restart'
    alias tm='/usr/bin/python ~/EH/manage.py testmaker 67.207.139.9:8000 --settings settings_debug'
    alias p='python'
    alias x='exit'
    # ^l clear screen
    bind -m vi-insert "\C-l":clear-screen
    # ^p check for partial match in history
    bind -m vi-insert "\C-p":dynamic-complete-history
    # ^n cycle through the list of partial matches
    bind -m vi-insert "\C-n":menu-complete

My terminals look like this: ``[eric@Odin:~/Python]$``. I use Vim
keybindings in my terminal as well (I'm addicted, what can I say).
I also use similar git commands to Brian, so I'll just let his
stand as the original awesomeness.

I hope you all find these links useful and interesting. It gives
you a little peek into how I spend my days. I'd love to hear what
everyone else does. If you have any suggestions for things that I
should probably be using, please feel free to let me know.


