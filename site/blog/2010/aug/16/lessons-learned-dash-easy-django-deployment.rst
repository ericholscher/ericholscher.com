.. post:: 2010-08-16 18:00:00

Lessons Learned From The Dash: Easy Django Deployment
=====================================================

This is going to be a series of posts that talk about what I
learned from the `Django Dash <http://djangodash.com/>`_. I think
it's a really fun competetion that is also a great learning
experience. I hope that this series catch on, and other people
write about some of the things that they learned in the Django
Dash.

What I learned
~~~~~~~~~~~~~~

The thing that I learned about during my dash project was the
awesomeness that is `Gunicorn <http://gunicorn.org/>`_. It is an
awesome HTTP server that I think has really solved the "how do I
deploy Django" problem.

Here are the steps involved in deploying a site using
`the gunicorn <http://thegunicorn.com/>`_:


-  pip install gunicorn
-  Add 'gunicorn' to your installed apps
-  ./manage.py run\_gunicorn -b 127.0.0.1:1337 --daemon

It really is that simple. Gunicorn is the fastest way to having a
production ready web server serving your site that I've found in
the Django realm. However, Gunicorn by itself isn't production
ready. It is recommended to deploy something in front of it. We
used `Nginx <http://wiki.nginx.org/Main>`_, which is another super
simple web server.

Here is basically the simplest possible configuration of nginx that
will work for your gunicorn backend server.

::

    server {
            listen 80;
            server_name  example.com;
            access_log  /var/log/nginx/example.log;
    
            location / {
                    proxy_pass   http://127.0.0.1:1337;
            }
    }

After you restart Nginx, you should be able to hit your server at
port 80 and have it be serving your Django web app. This allowed us
to get our application into production during the dash in about 10
minutes, which was a great time saver.

I'd be curious if people have had any trouble with Gunicorn in
deployment, because as far as I've seen its production ready. As a
"first Django deployment" set up I think it's hard to beat. I've
also noticed that is uses significantly less RAM than an
Apache/mod\_wsgi set up (I know this can be configured away, but by
default it's much better). This is great for the memory constrained
deployment platforms a lot of us are running on.


