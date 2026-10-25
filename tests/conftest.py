"""Shared fixtures for the browser tests: the built site over HTTP, and Chromium."""

import functools
import http.server
import os
import threading
from pathlib import Path

import pytest

BUILD = Path(__file__).resolve().parent.parent / "site/_build/dirhtml"


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
