:Date: 2009-03-21 13:45:47

Really easy SSH tunneling
=========================

SSH Tunneling has become an invaluable tool that I probably use
more than I should. I love tunneling, and use it all the time. This
will be a quick tutorial on how to use the SOCKS proxy ability of
SSH to allow you to tunnel your HTTP traffic through a remote
server.

This is useful when you're on a connection that has a silly filter
on it (school or library). Since it's a
`SOCKS5 <http://en.wikipedia.org/wiki/Socks5>`_ proxy, it is useful
for tunneling other things as well (like IM). It is also useful
when browsing on public wifi or anywhere that you can't trust the
network connection you're on, since it encrypts all the data that
is sent over it.

SSH
~~~

The command to tunnel in SSH is really simple. You simply do:
``ssh -ND localhost:5555 example.com`` to tunnel traffic through
example.com. This is a nice one off, but I actually have the
configuration in my ssh config. To do that, in your ~/.ssh/config,
you need to put in the settings you want your proxy to have.

::

    Host tunnel
        Hostname example.com
        DynamicForward localhost:5555

This allows me to simply do ``ssh -N tunnel``, and it will setup a
proxy. This is basically turning my local port 5555 into a proxy
that goes through the remote host. It is encrypted from my network
to the remote network, which is really nice. The ``-N`` flag is
used so that it doesn't create a shell on the other end, and simply
creates the proxy connection.

Firefox
~~~~~~~

In firefox, you need to go into your Preferences > Advanced >
Network > Connection > Settings. This is where your proxy settings
live. Go down the the SOCKS host, and set it to localhost, with the
port you set up above, 5555 in this case. It should look something
like this:

.. figure:: http://media.ericholscher.com/images/firefox-proxy.png
   :align: center
   :alt: Configuration for Proxy
   
   Configuration for Proxy

I use the
`Quickproxy <https://addons.mozilla.org/en-US/firefox/addon/1557>`_
extension to easily turn my proxy settings on and off. It puts a
small button on your bottom status bar in Firefox, and clicking it
turns your proxy on and off.

Now you simply flip the switch on your QuickProxy, and you are
surfing through an encrypted connection. To check if it's working,
I use http://whatismyip.com to check my remote IP. If it changes
between the proxy being on and off, you know the proxy is working.

This is a really easy way to simply create a two click encrypted
proxy. Hope this is helpful, and I'd be curious if people have
other tips and tricks in this regard.


