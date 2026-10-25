The Sphinx repo that powers http://ericholscher.com

Theme
-----

The site uses a custom Sphinx theme called ``topo``, which lives in ``site/_themes/topo/``.
It inherits Sphinx's ``basic`` theme and adds its own layout and stylesheet.
Fonts are self-hosted under ``site/_themes/topo/static/fonts/``.
Sidebar blocks are plain Jinja templates in ``site/_templates/sidebar/`` and are safe to edit by hand.

The home page and ``blog/index`` listings are rendered by the theme from ABlog's post data.
The home page leads with "Favorite posts": the first ``topo_featured_count`` (3) entries of ``html_context["topo_popular"]``
in ``site/conf.py``, each a (post docname, one-line summary) pair, then the eight most recent posts, then the rest of
the favorites as a short list, then the topic cards.
``blog/index`` shows the 20 latest posts, then pages by year: ABlog's year pages (``blog/archive/<year>/``) get
newer and older year links. The Archive page (``blog/archive/archive/``) lists every title by year.
Retired pages forward elsewhere through ``topo_redirects`` in ``site/conf.py`` (old docname to new), for example ``/bike/`` and
``/backpacking/`` to the Adventures page.
Posts in the ``link-blog`` category get a small "link" label next to their date.

Topics are ABlog categories. The ones listed in ``html_context["topo_categories"]`` in ``site/conf.py``
get a landing page with an intro, and a card on the home page. A post joins a topic with ``:category: <slug>``.
The Adventures page (``site/adventures.rst``) renders trips from ``site/_data/hikes.json`` and a places map
from ``site/_data/places.json``; both are plain JSON meant to be edited by hand.
Trips marked ``"feature": true`` show as cards under "The long ones".
Years and trip types are permalinks: ``/adventures/#2016`` opens that year and sets the map to it,
``/adventures/#trek`` shows only treks.
Every trip and place also shows in a year-by-year log, one collapsible section per year.
The map expands to fill the screen, with drag to pan, a label on hover (or tap) naming each pin, and zoom by pinch, ctrl+scroll, or the on-map buttons
(plain scroll and double-click also zoom once it is expanded).
Each hike has a ``kind``: ``thru-hike`` (end to end), ``trek`` (multi-day, hut or village based), ``hiking`` (a stay spent hiking from a base), ``backpacking``, ``summit``, ``day-hike``, ``camping``, ``rafting``, ``kayak``, ``cruise``, ``road-trip``, or ``bike``.

Year letters
------------

Each year can have a letter at ``site/adventures/<year>.md``: a short story of the year, month by month,
with a few photos for each month. ``2025.md`` and ``2026.md`` are started as drafts.

* **Drafts and publishing.** A letter starts with ``{post}`` and no date, which ABlog treats as a draft:
  it builds at ``/adventures/<year>/`` but isn't listed anywhere. Give it a date (```{post} 2026-12-31```)
  and it is published like any post, in the blog, the feeds, and the Outside topic, and the Adventures
  page links to it from that year ("Read the 2026 letter").
* **The year at a glance.** The ``adventure-summary`` directive near the top fills in that year's trips from
  ``hikes.json`` and a map of its places from ``places.json``, cropped to where they are. Write the story;
  the data takes care of itself.
* **Photos.** Export a few picks per month from Photos as JPEG, then make clean copies, resized and with all
  location and camera metadata removed so nothing private lands in this public repo::

      uv run --group photos scripts/prepare_photos.py ~/Desktop/picks/*.jpg --out site/_static/photos/2026

  Name them for the month and place (``04-camino-sunset.jpg``). Lay out two or three in a row under a month::

      ````{container} topo-photos
      ```{figure} /_static/photos/2026/04-camino-sunset.jpg
      Sunset over the Pacific, at the end of the trail.
      ```
      ```{figure} /_static/photos/2026/04-cloud-forest.jpg
      Cloud forest above San Gerardo.
      ```
      ````

  The photos in a row share one height and keep their own shape, so nothing is cropped. On a phone they stack.

Finding trips in your photos
----------------------------

``scripts/photo_trips.py`` turns an osxphotos export into one row per trip,
with dates, place names, and a guessed kind, to help fill ``hikes.json`` and ``places.json``::

    uvx --python 3.12 osxphotos query --location --json > photo-places.json
    python3 scripts/photo_trips.py photo-places.json --outdoor-only > trips.csv

Photos near any "lived" place in ``places.json`` are left out. To also leave out family and other
places, list them in ``photo-skip.json`` next to the export: by coordinates (``{"lat": ..., "lon": ..., "km": 25}``)
or by place name (``{"place": "Virginia"}``, matched against city, state, region, country, and address, with ``*`` wildcards).
For one-offs, pass ``--skip-near LAT,LON[,KM]`` or ``--skip-place NAME``.
Each row lists the trip's main towns in ``towns``, with days photographed in each. Tune the depth with
``--towns`` (most per trip, default 3) and ``--town-share`` (a town with this share of the photos is listed even if it never led a day, default 0.2).
All three files are gitignored, so those places stay on your machine. The script uses only the standard library.

Dependencies live in ``pyproject.toml`` and are pinned in ``uv.lock``; Read the Docs installs the ``docs`` group with uv.
To build locally::

    uv sync
    cd site && uv run sphinx-build -b dirhtml . _build/dirhtml

``uv sync --all-groups`` also installs ``sphinx-autobuild`` (``uv run sphinx-autobuild site site/_build/dirhtml -b dirhtml``)
and what ``import_substack.py`` needs. To update everything, run ``uv lock --upgrade`` and rebuild.
