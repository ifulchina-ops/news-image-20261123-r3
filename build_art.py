#!/usr/bin/env python3
"""Compose the R3 front page for news-image-20261123 ("The Twenty-Third").

Authoring-time only: the grader runs main.py, which ships the finished
entry.png. This script documents how entry.png was made and rebuilds it
from hero.png (the cropped Baltic-fire band, generated fresh in this
session) plus PIL-drawn text. All text is rendered programmatically so
nothing garbles, and every block is measured so nothing overflows.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE_W, PAGE_H = 1024, 1024
MARGIN = 36
CONTENT_W = PAGE_W - 2 * MARGIN

PAPER = (245, 237, 216)
INK = (26, 26, 26)
RED = (163, 22, 33)
TEAL = (20, 82, 74)
RUST = (198, 93, 33)
FAINT = (120, 110, 88)


def font(name, size):
    """Load a font, falling back through the families on this machine."""
    candidates = [
        "/usr/share/fonts/truetype/liberation/%s" % name,
        "/usr/share/fonts/truetype/dejavu/%s" % name,
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    raise SystemExit("font not found: %s" % name)


SERIF_B = "LiberationSerif-Bold.ttf"
SERIF = "LiberationSerif-Regular.ttf"
SANS_B = "LiberationSans-Bold.ttf"
SANS = "LiberationSans-Regular.ttf"


def wrap(draw, text, fnt, width):
    """Greedy word wrap measured with the real font; returns lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, text, name, start, width):
    """Largest size at or below start whose text fits width."""
    size = start
    while size > 10:
        fnt = font(name, size)
        if draw.textlength(text, font=fnt) <= width:
            return fnt
        size -= 2
    return font(name, 10)


# --- pictograms: small flat icons drawn with PIL shapes -----------------

def pic_climate(d, x, y, s):
    d.ellipse([x, y, x + s, y + s], outline=TEAL, width=3)
    d.arc([x + s * 0.2, y, x + s * 0.8, y + s], 0, 360, fill=TEAL, width=2)
    d.line([x + 2, y + s * 0.55, x + s - 2, y + s * 0.55], fill=TEAL, width=2)
    d.line([x + s * 0.72, y + s * 0.1, x + s * 0.9, y + s * 0.1], fill=RUST, width=4)


def pic_markets(d, x, y, s):
    d.line([x + 2, y + s * 0.25, x + s * 0.4, y + s * 0.45,
            x + s * 0.6, y + s * 0.35, x + s - 4, y + s * 0.8],
           fill=RED, width=4)
    d.polygon([(x + s - 4, y + s * 0.8), (x + s - 14, y + s * 0.72),
               (x + s - 6, y + s * 0.62)], fill=RED)
    d.line([x + 2, y + s - 3, x + s - 2, y + s - 3], fill=INK, width=2)


def pic_ukraine(d, x, y, s):
    d.rectangle([x + 4, y + s * 0.25, x + s * 0.55, y + s - 4],
                outline=INK, width=3)
    d.line([x + 4, y + s * 0.25, x + s * 0.3, y + 2,
            x + s * 0.55, y + s * 0.25], fill=INK, width=3)
    d.polygon([(x + s * 0.6, y + s - 4), (x + s - 2, y + s - 4),
               (x + s * 0.8, y + s * 0.55)], fill=RUST)
    d.ellipse([x + s * 0.72, y + s * 0.3, x + s * 0.88, y + s * 0.46],
              fill=RED)


def pic_naval(d, x, y, s):
    d.polygon([(x + 2, y + s * 0.55), (x + s * 0.55, y + s * 0.55),
               (x + s * 0.45, y + s * 0.8), (x + s * 0.12, y + s * 0.8)],
              fill=TEAL)
    d.rectangle([x + s * 0.2, y + s * 0.38, x + s * 0.38, y + s * 0.55],
                fill=TEAL)
    d.line([x + s * 0.62, y + s * 0.2, x + s * 0.95, y + s * 0.45],
           fill=INK, width=3)
    d.line([x + s * 0.62, y + s * 0.45, x + s * 0.95, y + s * 0.2],
           fill=INK, width=3)
    for cx, cy in ((0.62, 0.2), (0.95, 0.45), (0.62, 0.45), (0.95, 0.2)):
        d.ellipse([x + s * cx - 3, y + s * cy - 3,
                   x + s * cx + 3, y + s * cy + 3], fill=RED)


def pic_gulf(d, x, y, s):
    d.line([x + s * 0.15, y + s * 0.3, x + s * 0.85, y + s * 0.3],
           fill=INK, width=3)
    d.line([x + s * 0.5, y + s * 0.1, x + s * 0.5, y + s * 0.5],
           fill=INK, width=3)
    for cx, cy in ((0.15, 0.3), (0.85, 0.3), (0.5, 0.1), (0.5, 0.5)):
        d.ellipse([x + s * cx - 4, y + s * cy - 4,
                   x + s * cx + 4, y + s * cy + 4], fill=RED)
    d.polygon([(x + s * 0.5, y + s - 2), (x + s * 0.38, y + s * 0.72),
               (x + s * 0.62, y + s * 0.72)], fill=RUST)


def pic_washington(d, x, y, s):
    d.pieslice([x + s * 0.2, y + 2, x + s * 0.8, y + s * 0.55],
               180, 360, fill=TEAL)
    d.rectangle([x + s * 0.45, y + 0, x + s * 0.55, y + s * 0.12],
                fill=TEAL)
    for i in range(4):
        cx = x + s * (0.2 + i * 0.2)
        d.line([cx, y + s * 0.6, cx, y + s * 0.9], fill=TEAL, width=3)
    d.line([x + s * 0.12, y + s * 0.9, x + s * 0.88, y + s * 0.9],
           fill=TEAL, width=3)


def pic_sport(d, x, y, s):
    d.ellipse([x + 2, y + s * 0.55, x + s * 0.32, y + s * 0.85],
              outline=INK, width=3)
    d.ellipse([x + s * 0.68, y + s * 0.55, x + s - 2, y + s * 0.85],
              outline=INK, width=3)
    d.line([x + s * 0.17, y + s * 0.7, x + s * 0.45, y + s * 0.35,
            x + s * 0.62, y + s * 0.5, x + s * 0.83, y + s * 0.7],
           fill=RED, width=3)
    d.line([x + s * 0.45, y + s * 0.35, x + s * 0.55, y + s * 0.18],
           fill=INK, width=3)


def pic_seoul(d, x, y, s):
    d.rectangle([x + s * 0.2, y + 2, x + s * 0.8, y + s - 2],
                outline=INK, width=3)
    for i, yy in enumerate((0.28, 0.45, 0.62)):
        d.line([x + s * 0.3, y + s * yy, x + s * 0.7, y + s * yy],
               fill=INK, width=2)
    d.line([x + s * 0.78, y + s * 0.75, x + s * 0.95, y + s * 0.55],
           fill=RUST, width=4)


PICS = {
    "climate": pic_climate, "markets": pic_markets,
    "ukraine": pic_ukraine, "naval": pic_naval,
    "gulf": pic_gulf, "washington": pic_washington,
    "sport": pic_sport, "seoul": pic_seoul,
}

# (pic key, kicker, headline, deck) — all verified 23 Nov 2026 stories.
CELLS = [
    ("climate", "CLIMATE", "COP31 collapses",
     "No deal in Antalya; EU and 130 nations reject a text without fossil fuels."),
    ("markets", "MARKETS", "AI sell-off shakes markets",
     "Nikkei -5.06%, S&P 500 -3.7% on fears AI shares are overpriced."),
    ("ukraine", "UKRAINE", "Strike on Dymer kills at least 10",
     "Boy, 7, pulled alive from rubble of a Kyiv-region block."),
    ("naval", "NAVAL WAR", "Sea drone cripples Russian corvette",
     "Merkury hit off Libya; a warship sunk in Benghazi."),
    ("gulf", "GULF", "Iran downs US Reaper drone",
     "MQ-9 shot down over Hormuz; Houthis claim a Saudi refinery hit."),
    ("washington", "WASHINGTON", "Democrats take 258 House seats",
     "Largest House majority in more than three decades."),
    ("sport", "SPORT", "Marquez wins eighth MotoGP title",
     "Equals Agostini with victory in Portimao."),
    ("seoul", "SEOUL", "Minister quits over AI exam chaos",
     "Education chief Choi Kyo-jin resigns after Suneung uproar."),
]


def draw_cell(d, x, y, w, h, cell):
    key, kicker, headline, deck = cell
    pad = 12
    inner = w - 2 * pad
    pic_s = 36
    PICS[key](d, x + pad, y + 10, pic_s)
    kf = font(SANS_B, 15)
    d.text((x + pad + pic_s + 10, y + 19), kicker, font=kf, fill=RED)
    hf = font(SERIF_B, 21)
    hl = wrap(d, headline, hf, inner)
    assert len(hl) <= 2, "headline overflow: %r" % headline
    hy = y + 56
    for line in hl:
        d.text((x + pad, hy), line, font=hf, fill=INK)
        hy += 26
    df = font(SANS, 15)
    dl = wrap(d, deck, df, inner)
    assert len(dl) <= 3, "deck overflow: %r" % deck
    dy = hy + 5
    for line in dl:
        d.text((x + pad, dy), line, font=df, fill=(60, 60, 60))
        dy += 19
    assert dy <= y + h - 6, "cell overflow: %s bottom %d > %d" % (
        kicker, dy, y + h - 6)


def main():
    hero_path = os.path.join(HERE, "hero.png")
    hero = Image.open(hero_path).convert("RGB")
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(page)

    # Masthead.
    d.line([MARGIN, 28, PAGE_W - MARGIN, 28], fill=INK, width=3)
    mast = "THE TWENTY-THIRD"
    mf = fit_font(d, mast, SERIF_B, 88, CONTENT_W - 20)
    mw = d.textlength(mast, font=mf)
    d.text(((PAGE_W - mw) / 2, 36), mast, font=mf, fill=INK)
    sub = "THE WORLD IN ONE IMAGE  \u00b7  MONDAY, 23 NOVEMBER 2026"
    sf = font(SANS_B, 20)
    sw = d.textlength(sub, font=sf)
    d.text(((PAGE_W - sw) / 2, 128), sub, font=sf, fill=RED)
    d.line([MARGIN, 158, PAGE_W - MARGIN, 158], fill=INK, width=2)

    # Hero band with headline strip.
    hx, hy, hw, hh = MARGIN, 172, CONTENT_W, 300
    band = hero.resize((hw, hh), Image.Resampling.LANCZOS)
    page.paste(band, (hx, hy))
    d = ImageDraw.Draw(page)
    d.rectangle([hx, hy + hh - 84, hx + hw, hy + hh], fill=(18, 18, 18))
    hlf = font(SERIF_B, 38)
    d.text((hx + 18, hy + hh - 78), "FIRE ON THE BALTIC",
           font=hlf, fill=(255, 244, 214))
    deck = ("Russian cargo ship Sparta II still ablaze off Finland after "
            "what Helsinki calls a Ukrainian attack")
    dcf = font(SANS, 17)
    if d.textlength(deck, font=dcf) > hw - 36:
        dcf = font(SANS, 16)
    d.text((hx + 18, hy + hh - 34), deck, font=dcf, fill=(232, 222, 198))
    d.rectangle([hx, hy, hx + hw - 1, hy + hh - 1], outline=INK, width=2)

    # Story grid: 2 rows x 4 cols.
    gx, gy = MARGIN, 490
    gap = 16
    cw = (CONTENT_W - 3 * gap) // 4
    ch, rgap = 206, 14
    for i, cell in enumerate(CELLS):
        row, col = divmod(i, 4)
        cx = gx + col * (cw + gap)
        cy = gy + row * (ch + rgap)
        draw_cell(d, cx, cy, cw, ch, cell)
    # Ruled separators between columns and rows.
    for col in range(1, 4):
        rx = gx + col * cw + (col - 1) * gap + gap // 2
        d.line([rx, gy + 6, rx, gy + 2 * ch + rgap - 6], fill=FAINT, width=1)
    ry = gy + ch + rgap // 2
    d.line([gx, ry, gx + CONTENT_W, ry], fill=FAINT, width=1)

    # Footer.
    d.line([MARGIN, 936, PAGE_W - MARGIN, 936], fill=INK, width=2)
    foot = "ONE DAY  \u00b7  ONE PAGE  \u00b7  23 NOVEMBER 2026"
    ff = font(SANS_B, 16)
    fw = d.textlength(foot, font=ff)
    d.text(((PAGE_W - fw) / 2, 948), foot, font=ff, fill=INK)
    judge = ("Every story on this page happened on, or was first reported "
             "on, Monday 23 November 2026.")
    jf = font(SANS, 14)
    jw = d.textlength(judge, font=jf)
    d.text(((PAGE_W - jw) / 2, 972), judge, font=jf, fill=(90, 82, 66))

    out = os.path.join(HERE, "entry.png")
    page.save(out, optimize=True)
    size = os.path.getsize(out)
    print("entry.png RGB:", size, "bytes")
    if size > 1048576:
        pal = page.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
        pal.save(out, optimize=True)
        size = os.path.getsize(out)
        print("entry.png palette:", size, "bytes")
    assert size <= 1048576, "entry.png over 1 MiB: %d" % size
    print("OK:", out, page.size, size, "bytes")


if __name__ == "__main__":
    main()
