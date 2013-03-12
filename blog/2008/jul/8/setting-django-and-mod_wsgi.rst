:Date: 2008-07-08 20:11:06

Setting up Django and mod_wsgi
==============================

I was just convinced to setup mod\_wsgi on my server instead of
mod\_python, and I'm going to write up how I did it. All of the
documentation I found on the internet was really hard to follow, so
I'm going to distill it here the best that I can.

This is assuming Ubuntu 8.04 Server Edition.

**Update**: Take note, this is installing mod\_wsgi 1.3. The latest
version of the package is 2.3. If you want to get the latest
version from apt, you should use the
`Debian 2.3 package <http://packages.debian.org/unstable/python/libapache2-mod-wsgi>`_

Step 1: ``apt-get install libapache2-mod-wsgi``

This should automatically install mod\_wsgi into your apache
instance and install it.

Step 2: Create an apache directory on your filesystem, presumably
inside of your Django project. I keep my code in ~/Python/Project,
so I did:

::

    mkdir ~/Python/PROJECT/apache
    vim ~/Python/PROJECT/apache/django.wsgi

Then in that file you need to copy this code:

::

    import os, sys
    sys.path.append('/home/eric/Python/PROJECT')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'PROJECT.settings'
    import django.core.handlers.wsgi
    application = django.core.handlers.wsgi.WSGIHandler()

This creates an interface between Django and WSGI, as far as I can
tell. If you start getting errors about not seeing your project or
modules, try adjusting and/or adding some things to your sys.path.

Step 3:

Inside your /etc/apache2/ directoy, you will find the directory
sites-available/. This is where you are going to put your
configuration for your server. Presumably it will have a file
called default in it that you will edit. So:

In /etc/apache2/sites-available/default:

::

    <VirtualHost *:80>
    ServerAdmin eric@ericholscher.com
    ServerName  ericholscher.com
    ServerAlias www.ericholscher.com
    DocumentRoot /var/www/ 
    LogLevel warn
    WSGIDaemonProcess ericholscher processes=2 maximum-requests=500 threads=1
    WSGIProcessGroup ericholscher
    WSGIScriptAlias / /home/eric/Python/PROJECT/apache/django.wsgi
    Alias /media /var/www/media/
    </VirtualHost>

The last 3 lines of WSGI stuff if what you want to pay attention
to. You are pointing WSGIScriptAlias to the file we created in Step
2. The other two WSGI prompts aren't necessary unless you are
running multiple sites on your server. The Alias is so that the
/media URLs on your site continue to work, it should point to where
ever you have your media files stored.

Hopefully this will get you started along the way to setting up
mod\_wsgi on Apache with Django. If not, feel free to leave
comments or email me

EDIT: Someone in the comments pointed out this website on the
mod\_wsgi wiki is also helpful: Integration with Django

There appears to be a page on the Django WIki as well if you need
more pointers.


