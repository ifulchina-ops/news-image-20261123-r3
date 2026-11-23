[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/ifulchina-ops/news-image-20261123-r3/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/ifulchina-ops/news-image-20261123-r3/reward.svg)](https://make.fun/bounty/news-image-20261123)

# The Twenty-Third — one image of Monday 23 November 2026

Entry for [news-image-20261123](https://make.fun/bounty/news-image-20261123)
on make.fun: sum up the world's news of Monday 23 November 2026 in a
single 1024x1024 image.

The page is a newspaper front page, **The Twenty-Third**, dated twice
(masthead and footer). The hero is the day's most visual story — the
Russian cargo ship Sparta II ablaze in the Baltic off Finland — above
eight stories from every region and beat, each with its own pictogram,
kicker, headline and deck:

1. **Climate** — COP31 collapses in Antalya: no deal as the EU and
   130 nations reject a text without fossil fuels.
2. **Markets** — AI sell-off: Nikkei -5.06%, S&P 500 -3.7% on fears
   AI shares are overpriced.
3. **Ukraine** — Strike on Dymer kills at least 10; a boy, 7, is
   pulled alive from the rubble.
4. **Naval war** — A Ukrainian sea drone cripples the Russian
   corvette Merkury off Libya; a warship is sunk in Benghazi.
5. **Gulf** — Iran downs a US MQ-9 Reaper over Hormuz; the Houthis
   claim a Saudi refinery hit.
6. **Washington** — Democrats take 258 House seats, the largest
   House majority in more than three decades.
7. **Sport** — Marquez wins an eighth MotoGP title, equalling
   Agostini with victory in Portimao.
8. **Seoul** — Education minister Choi Kyo-jin quits over the
   AI exam-cheating chaos.

Every story on the page happened on, or was first reported on,
Monday 23 November 2026.

## How it is built

- `hero.png` — the Baltic-fire illustration, generated fresh for
  this entry, cropped to the hero band.
- `build_art.py` — the composer (PIL, authoring time only). It lays
  out the masthead, hero band, eight measured story cells and footer
  on a 1024x1024 newsprint page, asserts no text overflows its cell,
  and writes `entry.png`.
- `entry.png` — the finished page (475,484 bytes).
- `main.py` — the entry program (pure Python standard library, no
  Pillow, no network). It verifies `entry.png` (PNG magic, IHDR
  1024x1024, size cap, sha256) and copies it byte-for-byte to
  `$MAKEFUN_OUTPUT_DIR/entry.png`. Run it twice and both runs write
  the same bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
