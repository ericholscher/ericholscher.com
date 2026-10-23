The Sphinx repo that powers http://ericholscher.com

Theme
-----

The site uses a custom Sphinx theme called ``topo``, which lives in ``site/_themes/topo/``.
It inherits Sphinx's ``basic`` theme and adds its own layout and stylesheet.
Fonts are self-hosted under ``site/_themes/topo/static/fonts/``.
Sidebar blocks are plain Jinja templates in ``site/_templates/sidebar/`` and are safe to edit by hand.

The home page and ``blog/index`` listings are rendered by the theme from ABlog's post data.
Posts in the ``link-blog`` category get a small "link" label next to their date.

Topics are ABlog categories. The ones listed in ``html_context["topo_categories"]`` in ``site/conf.py``
get a landing page with an intro, and a card on the home page. A post joins a topic with ``:category: <slug>``.
The Outside landing page also renders a hike timeline from ``site/_data/hikes.json`` and a places map
from ``site/_data/places.json``; both are plain JSON meant to be edited by hand.
Each hike has a ``kind``: ``thru-hike`` (end to end), ``trek`` (multi-day, hut or village based), ``backpacking``, ``summit``, ``day-hike``, ``camping``, or ``bike``.

Finding trips in your photos
----------------------------

``scripts/photo_trips.py`` turns an osxphotos export into one row per trip,
with dates, place names, and a guessed kind, to help fill ``hikes.json`` and ``places.json``::

    uvx --python 3.12 osxphotos query --location --json > photo-places.json
    python3 scripts/photo_trips.py photo-places.json --outdoor-only > trips.csv

Both files are gitignored. The script uses only the standard library.

To build locally::

    python -m venv .venv
    .venv/bin/pip install -r requirements.txt
    cd site && ../.venv/bin/sphinx-build -b dirhtml . _build/dirhtml
