.. post:: 2010-01-07 16:49:02

A simple Perl IRCBot
====================

A couple things I want to talk about. First of all, I will be
participating in `project52 <http://project52.info/>`_; which is a
competetion to write a blog post in every week of the year. The
last 2 years I have done the november post-a-day, and gotten about
25 of the 30 required posts. So hopefully writing twice that number
of posts in 12 times the amount of time will be easy, right?
Anyways, this is the first post in that series, so stay tuned for
more regular and hopefully useful content :)

And since I don't like posting just basic updates, here is some
perl code that I just recently dug up.

The code
~~~~~~~~

I was thinking about adding IRC integration to a side project that
I have been working on lately. I remembered that I had written
something similar while in high school, and I've decided to throw
that code up online, and clean it up a little bit. I don't really
expect anyone to use it, but I think it's pretty neat, considering
I wrote it 6 years ago.

The code is up
`over at github <http://github.com/ericholscher/Masonry>`_ with
basic installation instructions. It comes with a client in perl and
python.

The idea is that the IRCBot has a basic TCP server in it, that you
can use to send it messages across a network. So you can send a
message crafted in the form of
``password&server&channel&my sweet message``, and the bot will
display it on the correct channel.

It uses `POE <http://poe.perl.org/>`_, which I believe is perl's
analogous idea to Twisted. I assume something like this is possible
for Python, but I figured since it was already written, I should go
ahead and use and release it.

The story
~~~~~~~~~

So the reason that this code exists is because I was a huge nerd in
high school. I went to a computer class in the afternoons, where we
each had our own computers, but the networks were locked down. This
was in a time before I was good enough at SSH Tunneling, so I went
ahead and wrote this code as a way to use HTTP to get into IRC.

The code released was half of it, it would site on IRC, and log all
activity into a Mysql database. It also had a TCP server built in,
so that I could ping it from another process/server and send
messages out to other channels.

The second half was a basic web interface, which would pull and
display all of the logs from the Mysql DB. It was broken down by
channel, giving historical logs of each. It also had a firehose
display that showed all incoming messages and what channel/server
they were from. Along with this there was a form that hit a CGI
script that sent a TCP request across to the client process and
sent messages into the IRC channels. This allowed me to have two
way communication into IRC from my web browser.

I happily used this to chat with people on IRC for my last year in
high school. :)


