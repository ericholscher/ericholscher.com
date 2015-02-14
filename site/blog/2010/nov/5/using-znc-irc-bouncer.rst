:Date: 2010-11-05 17:00:00

Using ZNC, an IRC bouncer
=========================

I use IRC for work, play, and generic open source questions and
support. I think it's a pretty integral part of my existence as a
developer. Today I'm going to write about why using an IRC bouncer
makes IRC a ton better and show you how to get one setup.

`ZNC <http://en.znc.in/wiki/ZNC>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ZNC is the bouncer that I was recommended when I started, and I
only have good things to say about it. On ubuntu installing ZNC is
really simple.

::

    sudo apt-get install znc-extra

This will pull down ZNC and it's extra modules which offer you some
nice features. So now that you have ZNC installed, you need to make
a configuration. You can do this with the ``znc --makeconf``
command, which I've pasted a session of at the bottom of this post.
However, here is the config that I run now.

::

    Listen       = +6666
    ConnectDelay = 30
    
    <User eric>
            Pass = md5#blah
            Nick = ericholscher
            AltNick = ericholscher_
            Ident = eric
            RealName = Eric
            QuitMsg = Peace.
            StatusPrefix = *
            ChanModes = +stn
            Buffer = 5000
            KeepBuffer = false
            MultiClients = true
            BounceDCCs = true
            DenyLoadMod = false
            Admin = true
            DenySetVHost = false
            DCCLookupMethod = default
            TimestampFormat = [%H:%M:%S]
            AppendTimestamp = false
            PrependTimestamp = true
            TimezoneOffset = 0.00
            JoinTries = 0
            MaxJoins = 5
    
            LoadModule = chansaver
            LoadModule = log
    
            Server = irc.freenode.net +7000
    
            <Chan #django>
            </Chan>
    </User>

**Note**: This might be from a slightly older version of ZNC, so
you might have to modify this to work on the newest version of ZNC
in the ubuntu 10.10 repos. Using the --makeconf option with the
same answers will also make an up to date conf.

Important options
~~~~~~~~~~~~~~~~~

The ``Buffer`` setting is the number of lines to keep in the buffer
when you're not connected. If you have your ZNC not keep your
buffer, with ``KeepBuffer = false`` setting, I tend to keep the
Buffer setting pretty high. You don't want to miss messages when
you're disconnected, so it will just stream these messages back to
you when you reconnect.

The other use of ZNC that I know people have is to connect from
multiple clients, like checking IRC on an iPhone. So long as you
have the ``MultiClients`` setting set, you can do this and it is
transparent to anyone else in your channels. However, when you
connect, you always want a scrollback of the context of the last
things said. In this case, you'd want to have
``KeepBuffer = true``, but have a small ``Buffer`` playback, so you
don't spam your phone.

The ``+6666`` on the Listen portion of the config means that it is
listening on port 6666, using SSL. So make sure if you turn on SSL,
your client is connecting with SSL as well.

Good Modules
~~~~~~~~~~~~

The modules that I have enabled are the chansaver and log modules.
The chansaver module writes out your ZNC config every time you join
or part a channel, so when you restart your bouncer it will have
the rooms you're in. The log module logs all the channels your in,
which is nice because it allows you to have comprehensive logs of
your work channels.

ZNC also comes with a `webadmin <http://en.znc.in/wiki/Webadmin>`_
that I have never used, but hear is quite nice. It allows you to
configure everything through a web interface. ZNC has a lot more
power than I've shown here, including connecting to multiple
backend servers, having multiple users, inter-user chat, and lots
of other interesting things. Once you've gotten hooked, you can
share your server with your friends, and play around with modules.

Using it
~~~~~~~~

So now to connect to your proxy, in your IRC client, instead of
connecting to your normal server (eg. irc.freenode.net 6667), you
would connect to your bouncer instead. This will be running on the
IP and port that you have configured in your ZNC config. My
`Limechat <http://limechat.net/mac/>`_ config looks like this:

.. figure:: /_static/img/limechat-config.png
   :align: center
   :alt: Limechat Config
   
   Limechat Config

You should then be able to just connect to that server, and your
client will show all the channels you're connected to. You can try
logging off and back on a couple of minutes later and see that it
plays back what you've missed.

This really changes how you interact with IRC I find, because you
can keep tabs on everything that is going on when you aren't
connected. I can be in the middle of a conversation, disconnect and
move to a meeting room downstairs, and pick right back up where
I've left off.

znc --makeconf session
^^^^^^^^^^^^^^^^^^^^^^

Here is a copy of the makeconf session I talked about earlier.
Where there is no visual input, it's just me accepting the
defaults.

::

    eric@Chimera:~$ znc --makeconf
    [ ** ] Building new config
    [ ** ] 
    [ ** ] First lets start with some global settings...
    [ ** ] 
    [ ?? ] What port would you like ZNC to listen on? (1 to 65535): 6666
    [ ?? ] Would you like ZNC to listen using SSL? (yes/no) [no]: yes
    [ ** ] Unable to locate pem file: [/home/eric/.znc/znc.pem]
    [ ?? ] Would you like to create a new pem file now? (yes/no) [yes]: yes
    [ ?? ] hostname of your shell (including the '.com' portion): irc.ericholscher.com
    [ ok ] Writing Pem file [/home/eric/.znc/znc.pem]... 
    [ ?? ] Would you like ZNC to listen using ipv6? (yes/no) [no]:   
    [ ?? ] Listen Host (Blank for all ips): 
    [ ** ] 
    [ ** ] -- Global Modules --
    [ ** ] 
    [ ?? ] Do you want to load any global modules? (yes/no): yes
    [ ** ] +-----------+----------------------------------------------------------+
    [ ** ] | Name      | Description                                              |
    [ ** ] +-----------+----------------------------------------------------------+
    [ ** ] | partyline | Internal channels and queries for users connected to znc |
    [ ** ] | webadmin  | Web based administration module                          |
    [ ** ] +-----------+----------------------------------------------------------+
    [ ** ] And 10 other (uncommon) modules. You can enable those later.
    [ ** ] 
    [ ?? ] Load global module <partyline>? (yes/no) [no]: no
    [ ?? ] Load global module <webadmin>? (yes/no) [no]: yes
    [ ** ] 
    [ ** ] Now we need to setup a user...
    [ ** ] 
    [ ?? ] Username (AlphaNumeric): eric
    [ ?? ] Enter Password: 
    [ ?? ] Confirm Password: 
    [ ?? ] Would you like this user to be an admin? (yes/no) [yes]:  
    [ ?? ] Nick [eric]: 
    [ ?? ] Alt Nick [eric_]: 
    [ ?? ] Ident [eric]: 
    [ ?? ] Real Name [Got ZNC?]: 
    [ ?? ] VHost (optional): 
    [ ?? ] Number of lines to buffer per channel [50]: 500
    [ ?? ] Would you like to keep buffers after replay? (yes/no) [no]: 
    [ ?? ] Default channel modes [+stn]: 
    [ ** ] 
    [ ** ] -- User Modules --
    [ ** ] 
    [ ?? ] Do you want to automatically load any user modules for this user? (yes/no): yes
    [ ** ] +-------------+-------------------------------------------------------------------+
    [ ** ] | Name        | Description                                                       |
    [ ** ] +-------------+-------------------------------------------------------------------+
    [ ** ] | admin       | Dynamic configuration of users/settings through irc               |
    [ ** ] | chansaver   | Keep config up-to-date when user joins/parts                      |
    [ ** ] | keepnick    | Keep trying for your primary nick                                 |
    [ ** ] | kickrejoin  | Autorejoin on kick                                                |
    [ ** ] | nickserv    | Auths you with NickServ                                           |
    [ ** ] | perform     | Keeps a list of commands to be executed when ZNC connects to IRC. |
    [ ** ] | simple_away | Auto away when last client disconnects                            |
    [ ** ] +-------------+-------------------------------------------------------------------+
    [ ** ] And 33 other (uncommon) modules. You can enable those later.
    [ ** ] 
    [ ?? ] Load module <admin>? (yes/no) [no]: yes
    [ ?? ] Load module <chansaver>? (yes/no) [no]: yes
    [ ?? ] Load module <keepnick>? (yes/no) [no]: yes
    [ ?? ] Load module <kickrejoin>? (yes/no) [no]:   
    [ ?? ] Load module <nickserv>? (yes/no) [no]: 
    [ ?? ] Load module <perform>? (yes/no) [no]: 
    [ ?? ] Load module <simple_away>? (yes/no) [no]: yes
    [ ** ] 
    [ ** ] -- IRC Servers --
    [ ** ] 
    [ ?? ] IRC server (host only): irc.freenode.net
    [ ?? ] [irc.freenode.net] Port (1 to 65535) [6667]: 
    [ ?? ] [irc.freenode.net] Password (probably empty): 
    [ ?? ] Does this server use SSL? (probably no) (yes/no) [no]: 
    [ ** ] 
    [ ?? ] Would you like to add another server? (yes/no) [no]: 
    [ ** ] 
    [ ** ] -- Channels --
    [ ** ] 
    [ ?? ] Would you like to add a channel for ZNC to automatically join? (yes/no) [yes]: yes
    [ ?? ] Channel name: #django
    [ ?? ] Would you like to add another channel? (yes/no) [no]:   
    [ ** ] 
    [ ?? ] Would you like to setup another user? (yes/no) [no]: 
    [ ok ] Writing config [/home/eric/.znc/configs/znc.conf]... 
    [ ** ] 
    [ ** ] To connect to this znc you need to connect to it as your irc server
    [ ** ] using the port that you supplied.  You have to supply your login info
    [ ** ] as the irc server password like so... user:pass.
    [ ** ] 
    [ ** ] Try something like this in your IRC client...
    [ ** ] /server <znc_server_ip> 6666 eric:<pass>
    [ ** ] 
    [ ?? ] Launch znc now? (yes/no) [yes]: 
    [ ok ] Opening Config [/home/eric/.znc/configs/znc.conf]... 
    [ ok ] Binding to port [+6666] using ipv4... 
    [ ** ] Loading user [eric]
    [ ok ] Loading Module [admin]... [/usr/lib/znc/admin.so]
    [ ok ] Loading Module [chansaver]... [/usr/lib/znc/chansaver.so]
    [ ok ] Loading Module [keepnick]... [/usr/lib/znc/keepnick.so]
    [ ok ] Loading Module [simple_away]... [/usr/lib/znc/simple_away.so]
    [ ok ] Adding Server [irc.freenode.net 6667]... 
    [ ok ] Loading Global Module [webadmin]... [/usr/lib/znc/webadmin.so]
    [ ok ] Forking into the background... [pid: 15983]
    [ ** ] ZNC 0.092+deb3 - http://znc.sourceforge.net


