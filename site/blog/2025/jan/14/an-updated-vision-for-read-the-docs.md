```{post} Jan 14, 2025
:category: link-blog
```

# An updated vision for Read the Docs

I'm excited that we published our [2025 vision for Read the
Docs](https://about.readthedocs.com/blog/2025/01/2025-vision/). It's
been a long-term goal to build more support for other documentation
tools, and better UX for documentation authors and readers.

> The major steps here have been:
>
> -   **Removing build magic:** Removing the injection of data or
>     configuration into your documentation builds. We used to have a
>     full Sphinx extension that we injected, and a lot of configuration
>     file manipulation for both
>     [Sphinx](https://about.readthedocs.com/blog/2024/07/addons-by-default/)
>     and
>     [MkDocs](https://about.readthedocs.com/blog/2024/03/mkdocs-yaml-manipulation/).
>     This has been removed, which means builds should happen exactly as
>     they do locally.
>
> -   **Adding build support for all tools:** We built support into our
>     build system for [fully custom
>     builds](https://blog.readthedocs.com/build-customization/), which
>     allows any build process that outputs HTML to be hosted on Read
>     the Docs.
>
> -   **Adding frontend support for all tools:** We rebuilt our [flyout
>     menu](https://docs.readthedocs.io/en/stable/flyout-menu.html#addons-flyout-menu)
>     and the JavaScript that is injected into your documentation builds
>     as a set of [Read the Docs
>     Addons](https://about.readthedocs.com/blog/2024/04/enable-beta-addons/).
>     This enables granular configuration, and disabling of various
>     frontend features via user settings.
>
> -   **Supporting custom integrations:** We\'re exposing all the data
>     that we use to build Addons to documentation users, who can build
>     [custom data
>     integrations](https://docs.readthedocs.io/en/stable/flyout-menu.html#custom-event-integration).
>     This allows you to integrate the versions from the API into a
>     version selector, offline formats into a download UI, and provide
>     an integrated UX for your users.

Our [actual website](https://about.readthedocs.com/) is currently
running on Read the Docs, and [built with
Pelican](https://github.com/readthedocs/website/blob/main/.readthedocs.yml#L9-L14).
Just a small example of what we can support now!
