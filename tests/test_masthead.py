"""Guards for the masthead mark, which has broken the same ways more than once.

The geometry tests read the SVG source and need nothing else. The browser
tests load the built site in Chromium and measure ink in screenshots, so they
check what a reader sees rather than CSS boxes. Build the site first:

    cd site && rm -rf _build && uv run sphinx-build -b dirhtml . _build/dirhtml
    cd .. && uv run --group tests pytest
"""

import functools
import http.server
import io
import os
import re
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
LAYOUT = ROOT / "site/_themes/topo/layout.html"
FAVICON = ROOT / "site/_static/img/favicon.svg"
BUILD = ROOT / "site/_build/dirhtml"

# The gold inset line: a diamond of radius 22 around (32, 32), stroked 1.5 wide.
GOLD_RADIUS = 22
GOLD_HALF_STROKE = 0.75
# Room the pilcrow keeps inside the gold line, in viewBox units (64 to the mark).
MIN_CLEARANCE = 1.5

# How far, in CSS pixels, two ink centers may differ and still read as aligned.
ALIGN_TOLERANCE = 0.75
SCALE = 4  # screenshot device scale factor, so ink is measured to a quarter pixel


def pilcrow(source):
    """Return the pilcrow's path data, translate, and scale from an SVG source."""
    m = re.search(r'<path d="([^"]+)"[^>]*transform="translate\(([\d.]+) ([\d.]+)\) scale\(([\d.]+) -[\d.]+\)"', source)
    assert m, "no pilcrow path with a translate and scale"
    return m.group(1), float(m.group(2)), float(m.group(3)), float(m.group(4))


def outline(d, samples=24):
    """Points along an absolute M/L/H/V/Q/Z path, sampling the curves."""
    points, x, y = [], 0.0, 0.0
    for cmd, args in re.findall(r"([MLHVQZ])([^MLHVQZ]*)", d):
        n = [float(v) for v in re.findall(r"-?[\d.]+", args)]
        if cmd in "ML":
            x, y = n
        elif cmd == "H":
            x = n[0]
        elif cmd == "V":
            y = n[0]
        elif cmd == "Q":
            cx, cy, ex, ey = n
            for i in range(1, samples + 1):
                t = i / samples
                points.append(((1 - t) ** 2 * x + 2 * (1 - t) * t * cx + t * t * ex, (1 - t) ** 2 * y + 2 * (1 - t) * t * cy + t * t * ey))
            x, y = ex, ey
        points.append((x, y))
    return points


@pytest.mark.parametrize("path", [LAYOUT, FAVICON], ids=["layout", "favicon"])
def test_pilcrow_clears_gold_line(path):
    d, tx, ty, s = pilcrow(path.read_text())
    reach = max(abs(tx + x * s - 32) + abs(ty - y * s - 32) for x, y in outline(d))
    clearance = GOLD_RADIUS - GOLD_HALF_STROKE - reach
    assert clearance >= MIN_CLEARANCE, f"pilcrow comes within {clearance:.2f} of the gold line (needs {MIN_CLEARANCE})"


def test_favicon_matches_masthead_mark():
    assert pilcrow(FAVICON.read_text()) == pilcrow(LAYOUT.read_text())


# Browser tests


@pytest.fixture(scope="module")
def site_url():
    if not (BUILD / "index.html").exists():
        pytest.skip("site not built; see this module's docstring")
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    handler = functools.partial(Quiet, directory=str(BUILD))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}/"
    server.shutdown()


@pytest.fixture(scope="module")
def browser():
    sync_playwright = pytest.importorskip("playwright.sync_api").sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH"))
        yield b
        b.close()


# Pages render with the webfonts, and without them: font-display: optional can leave
# the fallback serif on a first visit, and the mark has to line up with that too.
@pytest.fixture(params=[390, 1280], ids=lambda w: f"{w}px")
def width(request):
    return request.param


@pytest.fixture(params=[True, False], ids=["webfonts", "fallback-fonts"])
def webfonts(request):
    return request.param


@pytest.fixture
def page(browser, site_url, width, webfonts):
    page = browser.new_page(viewport={"width": width, "height": 400}, device_scale_factor=SCALE)
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    if not webfonts:
        page.route("**/*.woff2", lambda route: route.abort())
    page.goto(site_url)
    page.evaluate("document.fonts.ready")
    yield page
    page.close()
    assert not errors, errors


def ink_rows(page, box):
    """The top and bottom of the ink in a CSS-pixel box, in CSS pixels."""
    from PIL import Image

    x, y, w, h = box
    img = Image.open(io.BytesIO(page.screenshot(clip={"x": x, "y": y - 8, "width": w, "height": h + 16}))).convert("RGB")
    bg = img.getpixel((0, 0))
    px = img.load()
    rows = [r for r in range(img.height) if any(sum(abs(a - b) for a, b in zip(px[c, r], bg)) > 200 for c in range(img.width))]
    assert rows, f"no ink in {box}"
    return y - 8 + rows[0] / SCALE, y - 8 + (rows[-1] + 1) / SCALE


def center(rows):
    return (rows[0] + rows[1]) / 2


# The first letter of a link, which is a capital: its ink runs from cap height to baseline.
FIRST_LETTER = """el => { const r = document.createRange(); const t = el.querySelector("span")?.firstChild ?? el.firstChild;
  r.setStart(t, 0); r.setEnd(t, 1); const b = r.getBoundingClientRect();
  return [b.x + 1, b.y, b.width - 2, b.height]; }"""
BOX = "el => { const b = el.getBoundingClientRect(); return [b.x, b.y, b.width, b.height]; }"


def test_mark_centers_on_wordmark_capitals(page):
    mark = ink_rows(page, page.eval_on_selector(".topo-mark", BOX))
    caps = ink_rows(page, page.eval_on_selector(".topo-wordmark span", FIRST_LETTER))
    assert abs(center(mark) - center(caps)) <= ALIGN_TOLERANCE, f"mark ink {mark}, capitals {caps}"


def test_search_icon_centers_on_nav_capitals(page):
    icon = ink_rows(page, page.eval_on_selector(".topo-nav-search svg", BOX))
    # Compare with the label just before the icon. A fallback font can wrap the icon onto its own row.
    if page.eval_on_selector(".topo-nav-search", "el => el.offsetTop != el.previousElementSibling.offsetTop"):
        pytest.skip("the search icon wrapped onto its own row")
    caps = ink_rows(page, page.eval_on_selector(".topo-nav-search", f"el => ({FIRST_LETTER})(el.previousElementSibling)"))
    assert abs(center(icon) - center(caps)) <= ALIGN_TOLERANCE, f"search icon ink {icon}, capitals {caps}"


def test_nav_fits_one_row(page, webfonts):
    if not webfonts:
        pytest.skip("the one-row fit is sized for IBM Plex Sans; fallback fonts vary in width")
    tops = page.eval_on_selector_all(".topo-nav a", "els => els.map(a => a.getBoundingClientRect().top)")
    assert len(set(tops)) == 1, f"nav wraps: link tops {tops}"
    assert page.evaluate("document.documentElement.scrollWidth - innerWidth") == 0
