"""Find Hacker News threads about posts on this site, and write site/_data/hn.yml.

Each post then links its threads at the bottom, next to any press mentions.
Run it again now and then to pick up new threads; it replaces the file.

    uv run --group scripts scripts/hn_discussions.py

It asks the HN search API (hn.algolia.com) for stories whose URL is on ericholscher.com,
maps each URL to a post here (following redirects.yml for moved posts), and keeps
threads with at least MIN_COMMENTS comments, since an unanswered submission is no discussion.
"""

import datetime
import re
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = SITE / "_data" / "hn.yml"
MIN_COMMENTS = 3
API = "https://hn.algolia.com/api/v1/search"


def docname_for(url, redirects):
    path = re.sub(r"^https?://(www\.)?ericholscher\.com", "", url).split("#")[0].split("?")[0]
    path = "/" + path.strip("/") + "/"
    path = redirects.get(path, path)
    name = path.strip("/")
    if name.endswith(".html"):
        name = name[: -len(".html")]
    for ext in (".rst", ".md"):
        if (SITE / (name + ext)).exists():
            return name
    return None


def load_redirects():
    redirects = {}
    data = yaml.safe_load((ROOT / "redirects.yml").read_text()) or []
    for item in data if isinstance(data, list) else []:
        src, dst = item.get("from_url"), item.get("to_url")
        if src and dst and not dst.startswith("http"):
            redirects["/" + src.strip("/") + "/"] = "/" + dst.strip("/") + "/"
    return redirects


def main():
    hits = requests.get(
        API,
        params={"query": "ericholscher.com", "restrictSearchableAttributes": "url", "tags": "story", "hitsPerPage": 1000},
        timeout=30,
    ).json()["hits"]
    redirects = load_redirects()
    threads, unmatched = [], []
    for hit in hits:
        if not hit.get("url") or "ericholscher.com" not in hit["url"]:
            continue
        if (hit.get("num_comments") or 0) < MIN_COMMENTS:
            continue
        post = docname_for(hit["url"], redirects)
        if not post:
            unmatched.append(hit["url"])
            continue
        threads.append({
            "post": post,
            "date": datetime.date.fromisoformat(hit["created_at"][:10]),
            "comments": hit["num_comments"],
            "points": hit.get("points") or 0,
            "url": f"https://news.ycombinator.com/item?id={hit['objectID']}",
        })
    threads.sort(key=lambda t: (t["post"], t["date"]))
    header = "# Hacker News threads about posts on this site. Written by scripts/hn_discussions.py, which replaces this file.\n"
    OUT.write_text(header + yaml.safe_dump(threads, sort_keys=False, allow_unicode=True))
    print(f"{len(threads)} threads on {len({t['post'] for t in threads})} posts written to {OUT.relative_to(ROOT)}")
    for url in unmatched:
        print("no post here for", url)


if __name__ == "__main__":
    main()
