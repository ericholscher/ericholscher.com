"""Find the Mastodon post where Eric shared each blog post, and write site/_data/mastodon.yml.

Each post then offers that thread in its reply box, as a place to discuss it.
Run it again after sharing a new post; it replaces the file.

    uv run --group scripts scripts/mastodon_shares.py

It reads Eric's public posts on fosstodon.org (no login needed), skipping boosts and replies
to other people, and keeps the first post that links each page here.
"""

import datetime
import re

import requests
import yaml

from hn_discussions import ROOT, docname_for, load_redirects

OUT = ROOT / "site" / "_data" / "mastodon.yml"
INSTANCE = "https://fosstodon.org"
ACCOUNT = "ericholscher"


def statuses():
    account = requests.get(f"{INSTANCE}/api/v1/accounts/lookup", params={"acct": ACCOUNT}, timeout=30).json()
    params = {"limit": 40, "exclude_reblogs": "true"}
    while True:
        page = requests.get(f"{INSTANCE}/api/v1/accounts/{account['id']}/statuses", params=params, timeout=30).json()
        if not page:
            return
        yield from page
        params["max_id"] = page[-1]["id"]


def main():
    redirects = load_redirects()
    shares = {}
    for status in statuses():
        # A reply to someone else isn't a share; a reply in Eric's own thread can be.
        if status["in_reply_to_id"] and status["in_reply_to_account_id"] != status["account"]["id"]:
            continue
        urls = re.findall(r'href="(https?://(?:www\.)?ericholscher\.com/[^"]+)"', status["content"])
        if status.get("card") and "ericholscher.com" in status["card"]["url"]:
            urls.append(status["card"]["url"])
        for url in urls:
            post = docname_for(url, redirects)
            if not post or not post.startswith("blog/"):
                continue
            date = datetime.date.fromisoformat(status["created_at"][:10])
            if post not in shares or date < shares[post]["date"]:
                shares[post] = {"post": post, "date": date, "url": status["url"]}
    items = sorted(shares.values(), key=lambda s: s["post"])
    header = "# The Mastodon post where Eric shared each blog post. Written by scripts/mastodon_shares.py, which replaces this file.\n"
    OUT.write_text(header + yaml.safe_dump(items, sort_keys=False, allow_unicode=True))
    print(f"{len(items)} posts written to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
