The Sphinx repo that powers http://ericholscher.com

Theme
-----

The site uses a custom Sphinx theme called ``topo``, which lives in ``site/_themes/topo/``.
It inherits Sphinx's ``basic`` theme and adds its own layout and stylesheet.
Fonts are self-hosted under ``site/_themes/topo/static/fonts/``.
Sidebar blocks are plain Jinja templates in ``site/_templates/sidebar/`` and are safe to edit by hand.

The home page and ``blog/index`` listings are rendered by the theme from ABlog's post data.
The home page leads with "Most read", a hand-kept list of post docnames in ``html_context["topo_popular"]`` in ``site/conf.py``,
then the eight most recent titles and the topic cards.
``blog/index`` shows the 20 latest posts, then pages by year: ABlog's year pages (``blog/archive/<year>/``) get
newer and older year links. The Archive page (``blog/archive/archive/``) lists every title by year.
Retired pages forward elsewhere through ``topo_redirects`` in ``site/conf.py`` (old docname to new), for example ``/bike/`` and
``/backpacking/`` to the Adventures page.
Posts in the ``link-blog`` category get a small "link" label next to their date.

Topics are ABlog categories. The ones listed in ``html_context["topo_categories"]`` in ``site/conf.py``
get a landing page with an intro, and a card on the home page. A post joins a topic with ``:category: <slug>``.
The Adventures page (``site/adventures.rst``) renders trips from ``site/_data/hikes.json`` and a places map
from ``site/_data/places.json``; both are plain JSON meant to be edited by hand.
Trips marked ``"feature": true`` show as cards under "The long ones", there and on the Outside landing page.
Every trip and place also shows in a year-by-year log, one collapsible section per year.
The map expands to fill the screen, with zoom, drag to pan, and a label on hover (or tap) naming each pin.
Each hike has a ``kind``: ``thru-hike`` (end to end), ``trek`` (multi-day, hut or village based), ``hiking`` (a stay spent hiking from a base), ``backpacking``, ``summit``, ``day-hike``, ``camping``, ``rafting``, ``kayak``, ``cruise``, ``road-trip``, or ``bike``.

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
