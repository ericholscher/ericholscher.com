```{post} Feb 01, 2025
:category: link-blog
```

# A pattern for updating dependencies in a Docker image

We use docker pretty heavily at [work](https://about.readthedocs.com/),
and a pattern I've often run into is that I want to play around in a
docker image to get something working, and then be able to "save" it
back into the original image. This is generally a Python dependency or
something similar that we've put into our requirements, but rebuilding
all our dependencies takes a good bit of bandwidth and time.

## Run a one off command and resave the image

To start you need to get a shell in your docker image

    docker-compose exec $container /bin/bash 

Then you can do whatever task you need to inside that shell

    pip install requirements.txt

Then you need to save the image. You could pretty easily script this to
pull the hash name from the `ps` output, but doing it manually only
takes a couple seconds.

    docker ps
    # Get hash
    docker commit -p $hash $container

I use this pattern often when the command is pretty heavy and I don't
want to rerun the whole docker build process.

I don't use this often enough to

## Use Docker caching?

We have experimented with [Docker
caching](https://docs.docker.com/build/cache/), and it generally works
pretty well. However you can definitely run into weird cases where it
decides a part of the build early on has been updated, and that then
requires downloading multiple GB of data again. I think of the pattern
above as a way to do more explicit image updating via cache, without
having to depend on any specific logic or file modified dates that might
have changed in the process.
