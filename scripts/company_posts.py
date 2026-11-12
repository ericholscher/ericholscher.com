"""List the posts Eric wrote on the company blogs, for the archive.

The archive links out to these posts instead of copying them (see topo_with_elsewhere in
site/_ext/topo_site.py). Each blog's source is a public repo with author metadata:

- readthedocs/blog: the old Read the Docs blog, blog.readthedocs.com (ABlog). Its early posts have
  no byline; those Eric committed are counted as his.
- readthedocs/website: the current Read the Docs blog, about.readthedocs.com/blog (Pelican).
- writethedocs/www: the Write the Docs blog, writethedocs.org/blog (ABlog).
- readthedocs/ethicalads.io: the EthicalAds blog, ethicalads.io/blog (Pelican).

Routine posts (newsletters, maintenance notices, hiring posts, community updates) are left out, as
are posts that appear on two of the blogs, where the first copy is kept.

    uv run python scripts/company_posts.py

Clones the repos into .company-posts-cache/ (or pulls them if already there) and writes
site/_data/elsewhere.yml, newest first. The file can be edited by hand after, but a rerun replaces
it, so add a post's URL to SKIP below to drop it for good.
"""

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".company-posts-cache"
OUTPUT = ROOT / "site" / "_data" / "elsewhere.yml"
REPOS = ["readthedocs/blog", "readthedocs/website", "writethedocs/www", "readthedocs/ethicalads.io"]

ROUTINE = re.compile(r"newsletter|maintenance|downtime|hiring|community update|community kickoff", re.I)
SKIP: set[str] = set()


def fetch(repo):
    path = CACHE / repo.replace("/", "-")
    if path.exists():
        subprocess.run(["git", "-C", str(path), "pull", "-q"], check=True)
    else:
        # Full history: the old Read the Docs blog needs it to find who added each post.
        subprocess.run(["git", "clone", "-q", f"https://github.com/{repo}.git", str(path)], check=True)
    return path


def parse_date(text):
    text = re.sub(r"\bSept\b", "Sep", text.strip())
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d", "%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Can't read the date {text!r}")


def field(text, name):
    """A metadata field: `name: value` (Pelican Markdown) or `:name: value` (reST)."""
    m = re.search(rf"^\s*:?{name}:\s*(.+)$", text, re.M | re.I)
    return m.group(1).strip() if m else None


def rst_title(text):
    m = re.search(r"^(.+)\n[=#]{3,}\s*$", text, re.M)
    return m.group(1).strip() if m else ""


def pelican_slug(title):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"['&]", "", title.lower())).strip("-")


def by_eric(author):
    return bool(author) and ("Eric Holscher" in author or author.lower().startswith("eric"))


def first_committer(repo, path):
    log = subprocess.run(
        ["git", "-C", str(repo), "log", "--diff-filter=A", "--format=%an", "--", str(path.relative_to(repo))],
        capture_output=True, text=True, check=True,
    ).stdout.split("\n")
    names = [n for n in log if n]
    return names[-1] if names else ""


def ablog_posts(repo, folder, blog, url):
    for path in sorted((repo / folder).glob("*.rst")):
        text = path.read_text()
        posted = re.search(r"^\.\. post::\s*(.+)$", text, re.M)
        if not posted:
            continue
        author = field(text, "author")
        if author is None and blog == "Read the Docs" and "Eric" in first_committer(repo, path):
            author = "Eric"
        if by_eric(author):
            yield parse_date(posted.group(1)), rst_title(text), blog, url.format(slug=path.stem)


def pelican_posts(repo, folder, blog, url, slug_from_file=False):
    """slug_from_file: the site sets SLUGIFY_SOURCE = "basename", so a URL uses the file name, not the title."""
    for path in sorted((repo / folder).glob("*.*")):
        text = path.read_text()
        if not by_eric(field(text, "authors?")) or (field(text, "status") or "").lower() == "draft":
            continue
        day = parse_date(field(text, "date"))
        title = field(text, "title") or rst_title(text)
        slug = field(text, "slug") or (path.stem if slug_from_file else pelican_slug(title))
        yield day, title, blog, url.format(date=day, slug=slug)


def main():
    rtd_old, rtd, wtd, ea = (fetch(r) for r in REPOS)
    found = [
        *ablog_posts(rtd_old, ".", "Read the Docs", "https://blog.readthedocs.com/{slug}/"),
        *pelican_posts(rtd, "content/posts", "Read the Docs", "https://about.readthedocs.com/blog/{date:%Y/%m}/{slug}/", True),
        *ablog_posts(wtd, "docs/blog", "Write the Docs", "https://www.writethedocs.org/blog/{slug}/"),
        *pelican_posts(ea, "content/posts", "EthicalAds", "https://www.ethicalads.io/blog/{date:%Y/%m}/{slug}/"),
    ]
    posts, seen = [], set()
    for day, title, blog, url in sorted(found, key=lambda p: p[0]):
        key = title.lower()[:20]
        if key in seen or ROUTINE.search(title) or url in SKIP:
            continue
        seen.add(key)
        posts.append((day, title, blog, url))

    lines = [
        "# Posts Eric wrote on company blogs. The archive links out to them; they aren't copied here.",
        "# Written by scripts/company_posts.py, which replaces this file: drop a post for good with SKIP there.",
    ]
    for day, title, blog, url in reversed(posts):
        lines += [f"- title: {quote(title)}", f"  date: {day.isoformat()}", f"  blog: {blog}", f"  url: {url}"]
    OUTPUT.write_text("\n".join(lines) + "\n")
    print(f"Wrote {len(posts)} posts to {OUTPUT.relative_to(ROOT)}", file=sys.stderr)


def quote(text):
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


if __name__ == "__main__":
    main()
