"""The places map on the Adventures page: trips from site/_data/trips.json, and the year strip.

Build the site first (see test_masthead.py).
"""

import pytest

TRIP = "southeast-asia-2026"


@pytest.fixture(params=[390, 1280], ids=lambda w: f"{w}px")
def page(browser, site_url, request):
    page = browser.new_page(viewport={"width": request.param, "height": 844})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    yield page
    page.close()
    assert not errors, errors


def test_trip_permalink_fits_and_names_its_pins(page, site_url):
    page.goto(f"{site_url}adventures/#{TRIP}")
    page.wait_for_timeout(300)
    trip = page.locator(f"#{TRIP}")
    assert page.locator(".topo-tripnav-title").text_content() == trip.locator("h4").text_content()
    names = trip.get_attribute("data-places").split("|")
    lit = page.eval_on_selector_all(".topo-pin:not(.is-dim)", "ps => ps.map(p => p.dataset.name)")
    assert sorted(lit) == sorted(names)
    # Every pin of the trip is in the frame, and so is every name drawn on the map.
    frame = page.locator(".topo-map-scroll").bounding_box()
    inside = lambda b: frame["x"] - 1 <= b["x"] and b["x"] + b["width"] <= frame["x"] + frame["width"] + 1 and frame["y"] - 1 <= b["y"] and b["y"] + b["height"] <= frame["y"] + frame["height"] + 1
    for b in page.eval_on_selector_all(".topo-pin:not(.is-dim) circle", "cs => cs.map(c => c.getBoundingClientRect().toJSON())"):
        assert inside(b), b
    labels = page.eval_on_selector_all(".topo-pin-labels text", "ts => ts.map(t => t.getBoundingClientRect().toJSON())")
    assert len(labels) >= len(names) // 2
    for b in labels:
        assert inside(b), b
    assert page.evaluate("document.documentElement.scrollWidth - innerWidth") == 0


def test_arrows_step_through_trips(page, site_url):
    page.goto(f"{site_url}adventures/")
    first = page.locator(".topo-trip").first
    page.click('.topo-tripnav-step[data-step="1"]')
    assert page.locator(".topo-tripnav-title").text_content() == first.locator("h4").text_content()
    assert page.evaluate("location.hash") == "#" + first.get_attribute("id")
    page.click('.topo-tripnav-step[data-step="-1"]')
    assert page.locator(".topo-tripnav-title").text_content() == "All places"
    assert page.evaluate("location.hash") == ""


def test_year_strip_shows_a_year(page, site_url):
    page.goto(f"{site_url}adventures/")
    page.click('.topo-spark button[data-year="2016"]')
    assert page.locator(".topo-tripnav-title").text_content() == "2016"
    assert page.evaluate("location.hash") == "#2016"
    assert page.locator('details[id="2016"]').get_attribute("open") is not None
    years = page.eval_on_selector_all(".topo-pin:not(.is-dim):not(.topo-pin-lived)", "ps => ps.map(p => p.dataset.years)")
    assert years and all("2016" in y.split() for y in years)
