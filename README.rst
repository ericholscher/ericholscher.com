The Sphinx repo that powers http://ericholscher.com

Theme
-----

The site uses a custom Sphinx theme called ``topo``, which lives in ``site/_themes/topo/``.
It inherits Sphinx's ``basic`` theme and adds its own layout and stylesheet.
Fonts are self-hosted under ``site/_themes/topo/static/fonts/``.
Sidebar blocks are plain Jinja templates in ``site/_templates/sidebar/`` and are safe to edit by hand.

The home page and ``blog/index`` listings are rendered by the theme from ABlog's post data.
Posts in the ``link-blog`` category get a small "link" label next to their date.

To build locally::

    python -m venv .venv
    .venv/bin/pip install -r requirements.txt
    cd site && ../.venv/bin/sphinx-build -b dirhtml . _build/dirhtml
