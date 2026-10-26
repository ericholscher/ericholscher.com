# AGENTS.md

Notes for coding agents working on ericholscher.com, Eric Holscher's personal site.
It is a Sphinx + ABlog site with a custom theme called **topo**, hosted on Read the Docs.
The README covers how the pieces work. This file covers how to work on them: the build,
the design rules, Eric's preferences, and what must never go into this public repo.

## Build and check

```sh
uv sync                                  # just what the build needs (the docs group)
cd site && rm -rf _build && uv run sphinx-build -b dirhtml . _build/dirhtml
```

- After building, run `uv run --group tests pytest` from the repo root. The tests check that the pilcrow clears the blaze's gold line and that the mark and search icon line up with the text, with and without the webfonts. CI runs them on every PR (`.github/workflows/tests.yml`). Locally, set `CHROMIUM_PATH` if Playwright's own Chromium isn't installed.
- Delete `_build` before building. Incremental builds can serve stale theme CSS.
- `uv sync --all-groups` adds `sphinx-autobuild` and the script dependencies.
- The build should have no warnings. A new warning means something is wrong.
- Read the Docs builds with `.readthedocs.yaml`, using the native `method: uv` install of the `docs` group, Python 3.14, and Ubuntu 26.04.
- Every PR gets a preview at `https://ericholschercom--<PR>.org.readthedocs.build/`.
- Update dependencies with `uv lock --upgrade`, then rebuild and compare the output against the old build.

Before pushing a visual change, check it in a browser at **390px** and **1280px**:

- No horizontal overflow on any page touched (`scrollWidth - innerWidth == 0`).
- The masthead nav stays on one row on a phone.
- Tap targets are about 44px tall.
- There are no console errors.

Headless Chromium can't play H.264, so a video that "won't play" there is not a bug.

## Where things live

- `site/conf.py` holds Sphinx settings only. Never put site data or copy in it: give each list its own file in `site/_data/` and load it from the extension.
- `site/_ext/topo_site.py` is the site's own Sphinx extension: it loads `site/_data/*.json` into templates as `topo_<name>`, and holds the year-letter, photo-row, and redirect-stub hooks.
- `site/_data/categories.json` lists the topics: slug, then title and intro. Topic lists follow the file order; Community comes first because Eric thinks it is his best writing.
- `site/_themes/topo/` holds the theme: `layout.html`, `static/topo.css` (all styles, with tokens on `:root`), the fonts, and `theme.toml`.
- `site/_templates/`:
  - `topo/` has the shared pieces: post lists, the Adventures timeline, the map, and the redirect page.
  - `ablog/` overrides ABlog's topic and archive pages.
  - `sidebar/` has the sidebar blocks.
- `redirects.yml` maps retired URLs to where they now forward. Read the Docs serves them; `.github/workflows/sync-redirects.yml` syncs the file with readthedocs-cli. Add redirects there, never in the Read the Docs dashboard, since the sync deletes anything not in the file. Until the `RTD_TOKEN` secret is added, the build also writes meta-refresh pages from this file.
- `site/_data/favorites.yml` holds the favorite posts: each a post path and a hand-written summary. The `/favorite-posts/` page shows all of them, and the home page shows only the first `featured` few, with a link to the rest.
- `site/_data/hikes.json` and `places.json` hold the Adventures timeline and map data. They are the source of truth for trips; edit them by hand.
- `site/_data/trips.json` groups the places and `hikes.json` entries into trips (a region and season, like "Southeast Asia, winter 2026"). Europe gets its own trip for each year. The Adventures page is one list of these trips by year, built by `site/_ext/topo_trips.py`:
  - Every entry lands in exactly one trip. The `"home": true` trip ("Close to home") splits by year; an entry no trip names becomes a trip of its own.
  - A place in no trip goes on its year's "Also" line. The world map links into the same trips, so names and counts match.
  - Each trip's map is `site/_static/maps/<slug>.svg`, drawn by `scripts/trip_maps.py` from Natural Earth. Rerun it after changing a trip's places, and commit the output.
  - The build warns if a trip names a place or entry that isn't in the other files, or a map is missing.
- `scripts/photo_trips.py` turns an osxphotos export into candidate trip rows. See the README.
- Trail pages (`site/trails/<trail>.rst`) are drawn from `site/_data/trails.json` by `site/_ext/topo_trails.py` and `topo/trail.html`:
  - The route is the public trail from OpenStreetMap, traced by `scripts/trail_routes.py` into `trail_routes.json` with a relief image. Never use a personal GPS track.
  - Nights are trail miles or a town, from `photo_trips.py --nights`; never campsite coordinates.
  - The pages hold data, maps, and structure, plus Eric's own words from `hikes.json`. Don't write narrative for them.

## Design

The look is linen paper, umber ink, forest-green links, and public-land trail signage:

- **Labels:** brown plaques with a gold inset line.
- **Type:** Newsreader serif headings, with IBM Plex Sans and Plex Mono for text and labels.
- **Texture:** a public-domain USGS topo map behind the home intro.
- **Footer:** a ridgeline above it: the Cascades from just east of Redmond, Bachelor to Jefferson with the Three Sisters, traced from real elevation data by `scripts/skyline.py`.

Keep that identity. Work within the existing tokens in `topo.css` rather than adding colors.

- **Section labels:** use `.topo-plaque` (the filled brown plaque) in the content. Sidebar labels (`.topo-side-label`) are lighter on purpose: umber small caps over a short gold rule, since Eric found plaques overbearing there.
- **Calls to action:** one pattern everywhere. A paper card with a forest top edge (`.topo-cta`) holds one primary `.topo-button`, optionally with a `.topo-button-quiet` beside it. Buttons are 44px tall. (This lands with PR #42.)
- **The mark:** a diamond blaze with the Newsreader pilcrow as a path, in `layout.html` and `_static/img/favicon.svg`.
  - The pilcrow is centered so its widest points (the flag at top right, the stem foot at bottom right, the bowl at top left) sit the same distance inside the gold line: `translate(20.882 42.118) scale(0.016)`. Centering its bounding box instead pushed the flag through the gold line.
  - The name and nav labels use `text-box: trim-both cap alphabetic`, so flex centering lines the mark and search icon up on the capitals in any font. Browsers without `text-box` fall back to nudging `.topo-mark` up 2.5px.
  - Eric preferred this original pilcrow mark over the alternatives tried.
- **Fonts:** the three main fonts are preloaded and use `font-display: optional`. Don't switch back to `swap`; it made every page flash on load.
- **Images:**
  - Give transparent illustrations `:class: plain` so they skip the photo frame.
  - Add `no-scaled-link` to sized images that gain nothing from clicking through.
- **Embeds:**
  - Don't load third-party widget scripts that can fail to a blank box. X's `widgets.js` did, so it was removed.
  - Prefer a native `<video>` from `_static` with a poster image, or a plain link.
  - YouTube and Vimeo iframes scale to 16:9.
- **Maps:** inline SVG from Natural Earth land shapes, with no tiles or external scripts.
  - Interactive parts (year filter, hover labels, zoom, expand) are progressive enhancement. The page must still make sense without JavaScript.
  - The exception is the trail pages, where Eric asked for a real map (October 2026). `trail-map.js` swaps the static relief for MapLibre (vendored in `site/_static/vendor/`), with OpenFreeMap tiles and USGS terrain, only once its tiles have drawn. If they fail, the static map stays, so it never shows a blank box.
- **Mobile masthead:** the wordmark sits over a single nav row: Blog, Adventures, Speaking, Projects, About, and a search icon. It fits one row down to 375px; a 6th item would need tighter spacing or a shorter label.

## Voice and content

These are Eric's preferences, learned the hard way. Follow them without re-asking.

- It is a personal site, not a B2B landing page. No stat counters or metric bars.
- The Pacific Northwest belongs in the motifs, not the copy.
- **Understated, never braggy.**
  - The home intro is "I'm Eric. I build documentation tools and communities, and otherwise spend time outside." followed by the projects.
  - Say what he does once.
  - "Walk long trails" was cut as braggy.
- Keep the home H1 "My home on the web". Eric chose it over alternatives.
- **Don't invent facts:** no dates, routes, roles, summits, photo credits, or event names that aren't in the posts, the data files, or something Eric said.
  - When unsure, write less, or ask.
  - When summarizing a post, work from the post's own words.
- Favorite-post summaries are hand-written in `site/_data/favorites.yml`, not taken from opening lines, which can stop mid-thought.

## Privacy

This repo is public. Never commit:

- Names of friends or family.
- Where family lives, family visits, or health details.
- Trips that weren't Eric's. The shared Photos library includes his wife's own trips.
- Exact locations from photos. Map pins stay at town or region level.
- Photo metadata. Run photos through `scripts/prepare_photos.py`, which strips EXIF and GPS (PR #43).
- Personal skip lists for the photo script. They go in `photo-skip.json`, which is gitignored.

Leave a trip that is still in progress off the site until Eric says to add it.

## Facts Eric has confirmed

- **Co-founded:** Read the Docs, Write the Docs, PyCascades, and EthicalAds.
  - PyCascades: organizer 2018–2020, and co-chair of PyCascades 2020 in Portland.
- **Where he's lived:** nomadic in 2018 and 2019, settled in Bend in early 2020, and nomadic again in 2025 and 2026.
- **LinkedIn:** `https://www.linkedin.com/in/eric-holscher/`.
- **Speaking photo:** taken in Portland in 2025, by Kay Smoljak.
- **Trip details:** the PCT, JMT, and other trips are recorded in `hikes.json`; trust it over memory.
- **Not yet confirmed:** "Write the Docs Portland, 2013 to present" on the Speaking page and resume.

## Workflow

- Work on a branch and open a PR.
- Push straight to `main` only when Eric asks, for that change.
- After a PR merges, restart the branch from `main` instead of stacking on merged history.
- Write commit messages that say why, not only what.
- Open PRs when this was written (October 2026):
  - #40: photo script skip list by place or name.
  - #42: call-to-action pattern and a tidier intro.
  - #43: year letters, `site/adventures/<year>.md`.
