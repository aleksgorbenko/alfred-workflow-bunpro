#!/usr/bin/env python3
"""Render the 'bpm' List Filter row icons: emoji centered on a rounded square.

BG is BunPro's own brand red, sampled directly from their public logo
(bunpro.jp/fe/mobile-logo-512.png) - matches the "Red" accent cosmetic
returned by /user, and is what the unauthenticated logo/app icon shows
everywhere. BunPro has no fixed radical/kanji/vocab-style color taxonomy
(accents are user-customizable), so one consistent brand color is used
across all commands rather than an invented split.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG = "#C74A4A"  # BunPro brand red, sampled from their public logo
SIZE = 512
SS = 4  # supersample factor
RADIUS = 0.22  # corner radius as fraction of size, matches other workflows
EMOJI_FONT = "/System/Library/Fonts/Apple Color Emoji.ttc"
EMOJI_NATIVE_SIZE = 160  # largest embedded Apple Color Emoji bitmap strike
GLYPH = 0.62  # glyph height as fraction of size

# command (List Filter item `arg`) -> emoji
ICONS = {
    "summary": "📋",
    "stats": "📊",
    "levels": "🪜",
    "forecast": "📅",
    "leeches": "👻",
}

# SRS stage badge (stats.py) -> (emoji, brand color for that stage)
STAGE_ICONS = {
    "beginner": ("🌱", "#10252F"),
    "adept": ("🌿", "#1D3354"),
    "seasoned": ("🟣", "#51396B"),
    "expert": ("🔵", "#cd5c5c"),
    "master": ("⚪", "#C74A4A"),
}

# summary.py row -> emoji, brand red bg (no per-row color taxonomy for summary)
SUMMARY_ICONS = {
    "level": "🎓",
    "grammar_due": "📚",
    "vocab_due": "📖",
    "streak": "🔥",
}


def render(emoji: str, out: Path, bg: str = BG) -> None:
    canvas = SIZE * SS
    img = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle(
        (0, 0, canvas - 1, canvas - 1), radius=RADIUS * canvas, fill=bg
    )

    font = ImageFont.truetype(EMOJI_FONT, EMOJI_NATIVE_SIZE)
    glyph = Image.new("RGBA", (EMOJI_NATIVE_SIZE, EMOJI_NATIVE_SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(glyph).text((0, 0), emoji, font=font, embedded_color=True)

    target = round(GLYPH * canvas)
    glyph = glyph.resize((target, target), Image.LANCZOS)
    offset = ((canvas - target) // 2, (canvas - target) // 2)
    img.alpha_composite(glyph, offset)

    img.resize((SIZE, SIZE), Image.LANCZOS).save(out)


def main() -> int:
    out_dir = Path(__file__).resolve().parent.parent / "icons"
    wanted = sys.argv[1:] or list(ICONS)
    for key in wanted:
        if key not in ICONS:
            print(f"unknown key: {key}", file=sys.stderr)
            return 1
        path = out_dir / f"icon_{key}.png"
        render(ICONS[key], path)
        print(path)
    for key, (emoji, bg) in STAGE_ICONS.items():
        path = out_dir / f"icon_stage_{key}.png"
        render(emoji, path, bg=bg)
        print(path)
    for key, emoji in SUMMARY_ICONS.items():
        path = out_dir / f"icon_summary_{key}.png"
        render(emoji, path)
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
