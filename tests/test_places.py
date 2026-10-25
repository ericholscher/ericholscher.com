"""The Adventures page: trips, year by year, each with its own map, and the world map above them.

Every hikes.json entry should be listed once, in its trip; every trip once, under the year it
started; and the world map should link into the same trips. Build the site first (see
test_masthead.py).
"""

import json
import sys
from pathlib import Path

import pytest

SITE = Path(__file__).resolve().parent.parent / "site"
sys.path.insert(0, str(SITE / "_ext"))

import topo_trips  # noqa: E402

TRIP = "europe-2025"


def load(name):
    return json.loads((SITE / "_data" / name).read_text())


@pytest.fixture(scope="module")
def built():
    hikes, places = load("hikes.json"), load("places.json")
    trips, years, problems = topo_trips.build(hikes, places, load("trips.json"))
    return {"hikes": hikes, "places": places, "trips": trips, "years": years, "problems": problems}


@pytest.fixture(params=[390, 1280], ids=lambda w: f"{w}px")
def page(browser, site_url, request):
    page = browser.new_page(viewport={"width": request.param, "height": 844})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: m.type == "error" and errors.append(m.text))
    yield page
    page.close()
    assert not errors, errors


def test_every_entry_and_place_has_one_home(built):
    assert not built["problems"]
    assert sorted(id(h) for t in built["trips"] for h in t["entries"]) == sorted(id(h) for h in built["hikes"])
    slugs = [t["slug"] for t in built["trips"]]
    assert len(slugs) == len(set(slugs))
    # Each year's places are in one of its trips or on its "Also" line.
    for yr in built["years"]:
        y = int(yr["year"])
        in_trips = {p["name"] for t in built["trips"] if y in t["years"] for p in t["places"]}
        assert {p["name"] for p in yr["places"]} <= in_trips | {p["name"] for p in yr["other"]}


def test_list_shows_every_trip_and_entry_once(page, site_url, built):
    page.goto(f"{site_url}adventures/")
    ids = page.eval_on_selector_all("details.topo-trip", "ds => ds.map(d => d.id)")
    assert ids == [t["slug"] for t in built["trips"]]
    # A trip of one entry shows that entry in its summary; the others list theirs inside.
    assert page.locator(".topo-tl-item").count() + page.locator("details.is-solo").count() == len(built["hikes"])
    for t in built["trips"]:
        if t["map"]:
            assert (SITE / "_static" / "maps" / f"{t['slug']}.svg").exists(), t["slug"]
    assert page.evaluate("document.documentElement.scrollWidth - innerWidth") == 0


def test_trip_permalink_opens_and_names_its_pins(page, site_url):
    page.goto(f"{site_url}adventures/#{TRIP}")
    page.wait_for_timeout(300)
    trip = page.locator(f"#{TRIP}")
    assert trip.get_attribute("open") is not None
    frame = trip.locator(".topo-trip-map").bounding_box()
    inside = lambda b: frame["x"] - 1 <= b["x"] and b["x"] + b["width"] <= frame["x"] + frame["width"] + 1 and frame["y"] - 1 <= b["y"] and b["y"] + b["height"] <= frame["y"] + frame["height"] + 1
    pins = trip.locator(".topo-pin circle").evaluate_all("cs => cs.map(c => c.getBoundingClientRect().toJSON())")
    labels = trip.locator(".topo-pin-labels text").evaluate_all("ts => ts.map(t => t.getBoundingClientRect().toJSON())")
    assert pins and len(labels) >= len(pins) // 3
    for b in pins + labels:
        assert inside(b), b
    assert page.evaluate("document.documentElement.scrollWidth - innerWidth") == 0


def test_long_ones_link_to_their_trips(page, site_url):
    page.goto(f"{site_url}adventures/")
    link = page.locator(".topo-feature-list a").first
    slug = link.get_attribute("href").lstrip("#")
    link.click()
    # The trip opens on hashchange, which fires after the click returns.
    page.wait_for_function(f"document.getElementById('{slug}').open")
    assert page.locator(f"#{slug} .topo-long-mark").count() >= 1


def test_year_strip_links_to_that_years_trips(page, site_url):
    page.goto(f"{site_url}adventures/")
    for year in ("2026", "2018", "2016"):
        page.click(f'.topo-spark button[data-year="{year}"]')
        on_map = page.locator(".topo-map-readout a").all_text_contents()
        in_list = page.locator(f'.topo-log-year[data-year="{year}"] .topo-trip-name').all_text_contents()
        assert on_map == in_list
        years = page.eval_on_selector_all("#places .topo-pin:not(.is-dim):not(.topo-pin-lived)", "ps => ps.map(p => p.dataset.years)")
        assert years and all(year in y.split() for y in years)
        page.click(f'.topo-spark button[data-year="{year}"]')
    page.click('.topo-spark button[data-year="2018"]')
    page.locator(".topo-map-readout a").first.click()
    assert page.locator(f'.topo-log-year[data-year="2018"] details.topo-trip').first.get_attribute("open") is not None


def test_filter_narrows_the_list_and_the_map(page, site_url, built):
    page.goto(f"{site_url}adventures/#long")
    page.wait_for_timeout(300)
    shown = page.eval_on_selector_all(".topo-trip-item:not([hidden]) details", "ds => ds.map(d => d.id)")
    assert shown == [t["slug"] for t in built["trips"] if t["long"]]
    lit = page.eval_on_selector_all("#places .topo-pin:not(.is-dim)", "ps => ps.map(p => p.dataset.trips)")
    assert lit and all(set(t.split()) & set(shown) for t in lit)
    page.click(".topo-log-filter a")
    page.wait_for_function("!document.querySelector('.topo-trip-item[hidden]')")
    assert page.locator("#places .topo-pin.is-dim").count() == 0
