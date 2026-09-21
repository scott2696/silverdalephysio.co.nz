#!/usr/bin/env python3
"""Favicon set, apple-touch-icon, .ico, .svg and the Open Graph card.

Favicon sizes are 48, 96, 144, 192 and 512 — every one a multiple of 48, as
required. Google's favicon crawler wants at least 48x48 and a multiple of 48;
the browser and PWA sizes follow from the same source artwork.
"""
import html, os
from PIL import Image, ImageDraw, ImageFont

import lib                            # single source of truth for the identity

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = lib.LOGO_MARK                  # the chip face
WORD, TLD = lib.LOGO_NAME, lib.LOGO_TLD
FOREST = (28, 46, 38)
FOREST_HI = (60, 96, 80)
EMERALD = (58, 125, 96)
PAPER = (251, 250, 248)

FONTS = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial Bold.ttf",
]


def font(size):
    for p in FONTS:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def icon(size):
    """A poker chip: four copper spots on a lifted-navy edge, an ink face and
    the domain initial in white. Round reads as casino where the old square
    tile read as a bank, and four spots (not eight) still resolve at 48px."""
    ss = size * 8                      # supersample, then downscale
    im = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    box = [0, 0, ss - 1, ss - 1]

    # Edge: the spots are wedges of the full disc, hidden later under the face.
    d.ellipse(box, fill=FOREST_HI)
    for i in range(4):
        d.pieslice(box, start=i * 90 - 22.0, end=i * 90 + 22.0, fill=EMERALD)

    # Face, with the moulded inner ring the CSS mark also carries.
    inset = ss * 0.155
    face = [inset, inset, ss - 1 - inset, ss - 1 - inset]
    d.ellipse(face, fill=FOREST)
    ring = ss * 0.205
    d.ellipse([ring, ring, ss - 1 - ring, ss - 1 - ring],
              outline=(255, 255, 255, 70), width=max(2, int(ss * 0.009)))

    f = font(int(ss * 0.40))
    b = d.textbbox((0, 0), MARK, font=f)
    w, h = b[2] - b[0], b[3] - b[1]
    d.text((ss / 2 - w / 2 - b[0], ss / 2 - h / 2 - b[1]), MARK, font=f,
           fill=(255, 255, 255))

    return im.resize((size, size), Image.LANCZOS)


SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
<circle cx="24" cy="24" r="24" fill="#3C6050"/>
<g fill="#3A7D60">
<path d="M24 24 L46.3 15.0 A24 24 0 0 1 46.3 33.0 Z"/>
<path d="M24 24 L33.0 46.3 A24 24 0 0 1 15.0 46.3 Z"/>
<path d="M24 24 L1.7 33.0 A24 24 0 0 1 1.7 15.0 Z"/>
<path d="M24 24 L15.0 1.7 A24 24 0 0 1 33.0 1.7 Z"/>
</g>
<circle cx="24" cy="24" r="16.5" fill="#1C2E26"/>
<circle cx="24" cy="24" r="14" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="1"/>
<text x="24" y="31" font-family="Arial,Helvetica,sans-serif" font-size="19" font-weight="700"
 fill="#fff" text-anchor="middle">{MARK}</text>
</svg>
"""


def og():
    """1200x630 Open Graph card. Plain, legible, no stock imagery."""
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), FOREST)
    d = ImageDraw.Draw(im)
    for y in range(H):                       # vertical gradient
        t = y / H
        d.line([(0, y), (W, y)],
               fill=(int(28 + 7 * t), int(46 + 13 * t), int(38 + 9 * t)))
    d.rectangle([0, H - 10, W, H], fill=EMERALD)

    im.paste(icon(96), (72, 66), icon(96))
    # Wordmark matches the masthead: name in white, suffix set back one step —
    # and no suffix at all when LOGO_TLD is empty, so no orphan full stop.
    d.text((186, 78), WORD, font=font(44), fill=(255, 255, 255))
    if TLD:
        wlen = d.textlength(WORD, font=font(44))
        d.text((186 + wlen, 78), "." + TLD, font=font(44), fill=(150, 176, 160))
    d.text((188, 128), html.unescape(lib.TAG).upper(), font=font(18), fill=(166, 188, 174))

    d.text((72, 232), "Best Online Casino", font=font(78), fill=(255, 255, 255))
    d.text((72, 322), "Sites NZ", font=font(78), fill=(255, 255, 255))

    d.text((72, 446), "Every withdrawal ceiling priced in weeks",
           font=font(29), fill=(198, 216, 205))
    d.text((72, 492), "Checked from New Zealand  ·  Independent scores",
           font=font(29), fill=(198, 216, 205))
    d.text((72, 556), "R18  ·  Gambling can be harmful  ·  0800 654 655",
           font=font(21), fill=EMERALD)
    return im


def main():
    sizes = [48, 96, 144, 192, 512]          # every one a multiple of 48
    for s in sizes:
        icon(s).save(os.path.join(ROOT, f"favicon-{s}x{s}.png"))
    icon(180).save(os.path.join(ROOT, "apple-touch-icon.png"))
    # .ico carries the small legacy sizes browsers still ask for
    icon(256).save(os.path.join(ROOT, "favicon.ico"),
                   sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    open(os.path.join(ROOT, "favicon.svg"), "w").write(SVG)
    os.makedirs(os.path.join(ROOT, "images"), exist_ok=True)
    og().save(os.path.join(ROOT, "images", "og-default.png"), optimize=True)
    print("icons:", ", ".join(f"favicon-{s}x{s}.png" for s in sizes))
    print("also: apple-touch-icon.png, favicon.ico, favicon.svg, images/og-default.png")


if __name__ == "__main__":
    main()
