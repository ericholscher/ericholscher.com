The Value of Protocols
======================

A while back a friend of mine wrote `ZenIRCBot`_.
It is a protocol for writing IRC bots.

ZenIRCBot
---------

	An IRC bot that knows nothing of its past, nor its future.

The Zen in ZenIRCBot is because it uses PubSub to broadcast messages.
There is no history of the messages stored,
so if you aren't listening when a message comes in,
the message is lost.

It uses Redis PubSub as an implementation.
Messages coming from IRC are put on the ``in`` channel.
Messages going back out to IRC are put on the ``out`` channel.

.. image:: zenircbot.png

The actual bot commands are implemented as services.
They simply listen on the ``in`` channel,
and if they have a response to the message,
they put it back on the ``out`` channel.

Protocol
--------

The protocol it uses for messags are very simple.

.. code-block:: javascript

	// ZenIRCBot Basic Message
	{
	    "version": 1,
	    "type": "msg",
	    "data": {
	        "sender": "",
	        "channel": "",
	        "message": ""
	    }
	}

You might notice there is nothing IRC specific about this format.
It is a very abstract protocol,
which would be valid for most any kind of messaging platform.

Whispering Gophers
------------------

I have been learning the Go language,
and a group here in Portland has been working on `Whispering Gophers`_.
Whispering Gophers is a basic chat protocol written in Go.
It has a chat message format very similar to what ZenIRCBot uses::

	type Message struct {
		ID string
		Addr string
		Body string
		Nick string 
	}

All our bots are belong to IRC
------------------------------

Herein lies the beauty of ZenIRCBot.
All of the existing bots that I had written as IRC bots can be ported to Whispering Gophers.
All you need to do is transform the messages into the ZenIRCBot protocol format,
and publish them to Redis.

Conclusion
----------

By abstracting the message away from the protocol,
ZenIRCBot has become a protocol for making any kind of bot.
The bots can be written in any language,
as long as they have Redis and JSON bindings.

This is powerful because all ZenIRCBot services can be used on any messaging platform.
It also removes lock in of the current messaging platform.
So if your company wants to move from IRC to XMPP,
all of your bots will still work once you write a bridge.

.. _ZenIRCBot: http://zenircbot.readthedocs.org/en/latest/
.. _Whispering Gophers: http://whispering-gophers.appspot.com/