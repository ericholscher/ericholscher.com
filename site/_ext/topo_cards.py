"""Share cards: a 1200x630 JPEG per page for og:image, drawn in the topo look with Pillow.

Each card is linen paper under the masthead sign, with the page title in Newsreader, a plaque
with the post date, and the footer ridgeline. Pages with a photo of their own keep it as their
image (ogp_use_first_image), and pages without a doctree, such as redirect stubs, get no card.
"""

from pathlib import Path

from docutils import nodes
from markupsafe import Markup
import html
from functools import cache

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

W, H = 1200, 630
HERO, INK, SIGN, SIGN_TEXT, GOLD, FOREST = "#EBE2CD", "#332A20", "#4F3520", "#F2EBDC", "#DBA63E", "#255A42"
# The footer's ridgeline, from layout.html, in its 1280x48 viewBox.
RIDGE = [(0, 48), (0, 38), (60, 28), (120, 34), (200, 14), (260, 26), (340, 6), (400, 22), (470, 16), (560, 30), (640, 10), (710, 26), (790, 20), (880, 36), (960, 22), (1040, 30), (1120, 12), (1200, 26), (1280, 32), (1280, 48)]


def _font(app, name, size, axes=None):
    font = ImageFont.truetype(str(Path(app.confdir, "_themes/topo/static/fonts", name)), size)
    if axes:
        font.set_variation_by_axes(axes)
    return font


@cache
def _topo(confdir):
    """The home intro's USGS map, toned into the hero color the way .topo-hero does it, fading in from the left."""
    plain = Image.new("RGB", (W, H), HERO)
    path = Path(confdir, "_themes/topo/static/img/three-sisters-usgs.jpg")
    with Image.open(path) as im:
        terrain = ImageOps.fit(im.convert("RGB"), (W, H), centering=(0.5, 0.45))
    toned = Image.blend(plain, ImageChops.multiply(plain, terrain), 0.42)
    fade = Image.linear_gradient("L").rotate(90, expand=True).resize((W, H)).point(lambda v: 25 + v * 230 // 255)
    return Image.composite(toned, plain, fade)


def _tracked(draw, xy, text, font, fill, tracking):
    """Draw text letter-spaced, like the site's mono labels; return its width."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill, anchor="lm")
        x += draw.textlength(ch, font=font) + tracking
    return x - xy[0] - tracking


def _wrap(draw, text, font, width):
    lines, line = [], ""
    for word in text.split():
        test = f"{line} {word}".strip()
        if line and draw.textlength(test, font=font) > width:
            lines.append(line)
            line = word
        else:
            line = test
    return lines + [line] if line else lines


def draw_card(app, title, label):
    img = _topo(app.confdir).copy()
    d = ImageDraw.Draw(img)

    # Masthead: the sign, its gold edge, and the blaze mark beside the name.
    d.rectangle((0, 0, W, 112), fill=SIGN)
    d.rectangle((0, 112, W, 117), fill=GOLD)
    cx, cy, r = 92, 56, 30
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=SIGN_TEXT)
    d.polygon([(cx, cy - r + 6), (cx + r - 6, cy), (cx, cy + r - 6), (cx - r + 6, cy)], outline=GOLD, width=2)
    d.text((cx, cy + 2), "¶", font=_font(app, "Newsreader-Variable.woff2", 36, [600, 36]), fill=SIGN, anchor="mm")
    d.text((cx + r + 26, cy), "Eric Holscher", font=_font(app, "Newsreader-Variable.woff2", 46, [500, 46]), fill=SIGN_TEXT, anchor="lm")

    # Plaque: brown label with a gold inset line, like .topo-plaque.
    y = 172
    if label:
        mono = _font(app, "IBMPlexMono-Regular.woff2", 22)
        tw = _tracked(ImageDraw.Draw(Image.new("L", (1, 1))), (0, 0), label.upper(), mono, 0, 3)
        d.rounded_rectangle((80, y, 80 + tw + 36, y + 46), radius=4, fill=SIGN)
        d.rounded_rectangle((83, y + 3, 80 + tw + 33, y + 43), radius=3, outline=GOLD, width=1)
        _tracked(d, (98, y + 23), label.upper(), mono, SIGN_TEXT, 3)
        y += 82
    else:
        y += 20

    # Title: as large as fits in three lines.
    for size in (76, 66, 56):
        serif = _font(app, "Newsreader-Variable.woff2", size, [500, 72])
        lines = _wrap(d, title, serif, W - 160)
        if len(lines) <= 3:
            break
    if len(lines) > 3:
        lines = lines[:3]
        lines[2] = lines[2].rstrip(",.;:") + "…"
    for line in lines:
        d.text((80, y), line, font=serif, fill=INK, anchor="la")
        y += int(size * 1.12)

    # Footer: the ridgeline over forest, with the gold edge between them.
    base = H - 58
    d.polygon([(x * W / 1280, base - 64 + py * 64 / 48) for x, py in RIDGE], fill=FOREST)
    d.rectangle((0, base, W, base + 4), fill=GOLD)
    d.rectangle((0, base + 4, W, H), fill=FOREST)
    d.text((80, base + 31), "ericholscher.com", font=_font(app, "IBMPlexMono-Regular.woff2", 22), fill=SIGN_TEXT, anchor="lm")
    return img


def topo_share_card(app, pagename, templatename, context, doctree):
    if app.builder.format != "html" or doctree is None or doctree.next_node(nodes.image):
        return
    post = (getattr(app.env, "ablog_posts", {}).get(pagename) or [{}])[0]
    label = f"Blog · {post['date']:%b %-d, %Y}" if post.get("date") else ""
    title = Markup(context.get("title", "")).striptags()  # the title is HTML; draw it as text
    card = Path(app.outdir, "_static/cards", f"{pagename}.jpg")
    card.parent.mkdir(parents=True, exist_ok=True)
    draw_card(app, title, label).save(card, quality=82, optimize=True, progressive=True)
    # sphinxext-opengraph reads og: fields from the page's metadata; copy it rather than edit the env's.
    context["meta"] = {**(context.get("meta") or {}), "og:image": f"{app.config.ogp_site_url}/_static/cards/{pagename}.jpg", "og:image:alt": html.escape(title, quote=False), "og:image:width": str(W), "og:image:height": str(H)}


def setup(app):
    # Before sphinxext-opengraph (priority 500), so it sees the card.
    app.connect("html-page-context", topo_share_card, priority=400)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
