#!/usr/bin/env python3
"""Author portraits: square, face-centred, 148x148 JPEG.

Sources live in `_source/authors/<slug>.png` and are not served. They arrive as
tall ID-style crops (142x176), and the avatars on this site are circles at 34px
in a byline and 62px in an author box — so a straight resize would squash the
frame and a centre crop would cut the chin. Both are fixed here rather than in
CSS, because `object-fit:cover` on a badly framed source just crops the wrong
part on every page at once.

148px is 2x the largest display size, which keeps the author box crisp on a
retina screen without shipping a file bigger than the logo beside it.

Run after replacing any source portrait:

    python3 _build/gen_authors.py
"""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_source", "authors")
OUT = os.path.join(ROOT, "images", "authors")

SIZE = 148

# Vertical bias for the square crop, as a fraction of the slack between the
# source height and its width. 0 is hard to the top of the frame, 1 to the
# bottom. Faces in a passport-style crop sit high, so the head lands centred at
# about a third of the way down rather than at the midpoint.
FACE_BIAS = 0.34

# Per-portrait overrides, where a source needs framing the default does not give.
# ari-mcconnell's source has the top edge of a laptop screen across the bottom
# of the frame at y=152 of 176; cropping hard to the top of the image drops it.
BIAS = {"ari-mcconnell": 0.0}


def square(im, bias=FACE_BIAS):
    """Crop to the largest centred square, biased up towards the face."""
    w, h = im.size
    if h > w:
        top = round((h - w) * bias)
        return im.crop((0, top, w, top + w))
    if w > h:
        left = round((w - h) / 2)
        return im.crop((left, 0, left + h, h))
    return im


def main():
    if not os.path.isdir(SRC):
        raise SystemExit(f"no source directory: {SRC}")
    os.makedirs(OUT, exist_ok=True)
    done = []
    for fn in sorted(os.listdir(SRC)):
        if not fn.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            continue
        slug = os.path.splitext(fn)[0]
        im = Image.open(os.path.join(SRC, fn))
        # Flatten any alpha onto white first: a JPEG has no alpha channel, and
        # compositing after the resize leaves a dark fringe on the edge pixels.
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")
        im = square(im, BIAS.get(slug, FACE_BIAS)).resize((SIZE, SIZE), Image.LANCZOS)
        path = os.path.join(OUT, f"{slug}.jpg")
        im.save(path, "JPEG", quality=86, optimize=True, progressive=True)
        done.append(f"{slug}.jpg ({os.path.getsize(path) // 1024}KB)")
    print(f"author portraits ({SIZE}x{SIZE}): " + ", ".join(done))


if __name__ == "__main__":
    main()
