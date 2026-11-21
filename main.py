#!/usr/bin/env python3
"""The Passport Page of a Country That Isn't There — make.fun entry.

Draws, fully programmatically, one open passport spread for the invented
island nation of Veldoria: a data page (portrait, MRZ, trilingual labels)
and a visas page (arrival/departure stamps from the neighbouring states
Tarnovia and Ostara, a harbour-fee stamp and a visa condition that reveal
the country's seafaring character). Writes /output/entry.png.

Deterministic: fixed geometry, fixed palette, fixed fonts, no randomness,
no time, no network. Two runs produce byte-identical PNGs.
"""

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 720

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 230)      # cream passport paper
PAPER_D = (238, 231, 214)
INK = (26, 34, 56)           # deep navy ink
INK_SOFT = (74, 84, 110)
RULE = (150, 142, 122)
GOLD = (176, 141, 58)
RED = (158, 32, 32)
BLUE = (28, 74, 138)
GREEN = (28, 102, 66)
PURPLE = (96, 52, 130)
PHOTO_BG = (176, 196, 210)
SKIN = (222, 178, 140)
SKIN_D = (205, 158, 120)
HAIR = (58, 38, 28)
JACKET = (44, 62, 96)
SHIRT = (240, 238, 230)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
MONO = lambda s: font("DejaVuSansMono.ttf", s)
MONO_B = lambda s: font("DejaVuSansMono-Bold.ttf", s)


def text(draw, xy, s, f, fill=INK, anchor="la"):
    draw.text(xy, s, font=f, fill=fill, anchor=anchor)


def centre(draw, cx, y, s, f, fill=INK):
    draw.text((cx, y), s, font=f, fill=fill, anchor="ma")


# ---------------------------------------------------------------- portrait
def draw_portrait(box):
    """Flat-illustration passport portrait, 150x190, drawn from shapes."""
    w, h = box
    img = Image.new("RGB", box, PHOTO_BG)
    d = ImageDraw.Draw(img)
    # soft background vignette
    for i in range(0, h, 6):
        shade = int(8 * (1 - abs(i - h / 2) / (h / 2)))
        d.line([(0, i), (w, i)], fill=(PHOTO_BG[0] - shade, PHOTO_BG[1] - shade,
                                        PHOTO_BG[2] - shade))
    cx = w // 2
    # shoulders / jacket
    d.polygon([(cx - 62, h), (cx - 52, 138), (cx - 26, 122), (cx + 26, 122),
               (cx + 52, 138), (cx + 62, h)], fill=JACKET)
    # shirt V
    d.polygon([(cx - 16, 124), (cx, 158), (cx + 16, 124), (cx + 10, 122),
               (cx, 138), (cx - 10, 122)], fill=SHIRT)
    # collar
    d.polygon([(cx - 24, 122), (cx, 142), (cx - 8, 122)], fill=SHIRT)
    d.polygon([(cx + 24, 122), (cx, 142), (cx + 8, 122)], fill=SHIRT)
    # neck
    d.rectangle([cx - 13, 104, cx + 13, 126], fill=SKIN_D)
    # face
    d.ellipse([cx - 34, 34, cx + 34, 112], fill=SKIN)
    # ears
    d.ellipse([cx - 40, 66, cx - 30, 88], fill=SKIN)
    d.ellipse([cx + 30, 66, cx + 40, 88], fill=SKIN)
    # hair: bob framing the face
    d.pieslice([cx - 40, 18, cx + 40, 96], 180, 360, fill=HAIR)
    d.polygon([(cx - 40, 40), (cx - 34, 96), (cx - 26, 96), (cx - 34, 44)],
              fill=HAIR)
    d.polygon([(cx + 40, 40), (cx + 34, 96), (cx + 26, 96), (cx + 34, 44)],
              fill=HAIR)
    d.ellipse([cx - 36, 22, cx + 36, 58], fill=HAIR)
    # forehead fringe
    d.pieslice([cx - 34, 30, cx + 34, 66], 180, 360, fill=HAIR)
    # brows
    d.line([cx - 22, 68, cx - 8, 66], fill=HAIR, width=3)
    d.line([cx + 8, 66, cx + 22, 68], fill=HAIR, width=3)
    # eyes
    for ex in (cx - 15, cx + 15):
        d.ellipse([ex - 6, 72, ex + 6, 79], fill=(255, 255, 255))
        d.ellipse([ex - 3, 73, ex + 3, 78], fill=(52, 40, 30))
        d.line([ex - 6, 72, ex + 6, 72], fill=HAIR, width=2)
    # nose
    d.line([cx, 78, cx - 2, 92, cx + 3, 94], fill=SKIN_D, width=2)
    # lips
    d.line([cx - 9, 102, cx + 9, 102], fill=(168, 92, 80), width=3)
    # soft cheek shading
    d.ellipse([cx - 30, 84, cx - 16, 96], fill=(228, 186, 150))
    d.ellipse([cx + 16, 84, cx + 30, 96], fill=(228, 186, 150))
    # thin photo frame
    d.rectangle([0, 0, w - 1, h - 1], outline=(120, 118, 110), width=2)
    return img


# ---------------------------------------------------------------- emblem
def draw_emblem(d, cx, cy, s):
    """Veldoria arms: shield, three waves, one star."""
    w, h = s, int(s * 1.15)
    x0, y0 = cx - w // 2, cy - h // 2
    # shield
    pts = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h * 0.62),
           (cx, y0 + h), (x0, y0 + h * 0.62)]
    d.polygon(pts, outline=GOLD, width=3)
    d.polygon([(x0 + 3, y0 + 3), (x0 + w - 3, y0 + 3),
               (x0 + w - 3, y0 + h * 0.62 - 2), (cx, y0 + h - 4),
               (x0 + 3, y0 + h * 0.62 - 2)], fill=(232, 222, 196))
    # star
    r = s * 0.16
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        star.append((cx + rr * math.cos(ang), cy - h * 0.16 + rr * math.sin(ang)))
    d.polygon(star, fill=GOLD)
    # three waves
    for k, yy in enumerate((0.18, 0.32, 0.46)):
        y = y0 + h * yy
        d.arc([x0 + 6, y, x0 + w - 6, y + 12], 180, 360, fill=BLUE, width=2)


# ---------------------------------------------------------------- stamps
def stamp_layer(lines, color, w, h, radius=6):
    """A rectangular ink stamp on its own transparent layer.

    Lines are (text, font, y) with explicit y positions so no line ever
    crosses the stamp's border.
    """
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([2, 2, w - 3, h - 3], radius=radius,
                        outline=color + (235,), width=3)
    d.rounded_rectangle([7, 7, w - 8, h - 8], radius=radius - 2,
                        outline=color + (200,), width=1)
    for s, f, y in lines:
        d.text((w // 2, y), s, font=f, fill=color + (235,), anchor="ma")
    return layer


def circle_stamp(d, cx, cy, r, color, top, mid, bot):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color + (220,), width=3)
    d.ellipse([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6],
              outline=color + (180,), width=1)
    d.text((cx, cy - r + 14), top, font=SANS_B(11), fill=color + (220,),
           anchor="ma")
    d.text((cx, cy - 8), mid, font=SANS_B(13), fill=color + (225,), anchor="ma")
    d.text((cx, cy + r - 24), bot, font=SANS_B(10), fill=color + (220,),
           anchor="ma")


def paste_rotated(base, layer, cx, cy, angle):
    rot = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    base.paste(rot, (int(cx - rot.width // 2), int(cy - rot.height // 2)), rot)


# ---------------------------------------------------------------- pages
def draw_left(d, img):
    x0, x1 = 28, 496
    # outer frame
    d.rectangle([x0, 20, x1, 700], outline=INK, width=2)
    d.rectangle([x0 + 5, 25, x1 - 5, 695], outline=RULE, width=1)
    # header
    draw_emblem(d, 262, 66, 44)
    centre(d, 262, 96, "REPUBLIC OF VELDORIA", SERIF_B(21))
    centre(d, 262, 122, "PASSPORT  ·  PASSEPORT  ·  PASAPORT", SANS(10),
           INK_SOFT)
    d.line([48, 144, 476, 144], fill=RULE, width=1)

    # photo, top right
    photo = draw_portrait((150, 190))
    img.paste(photo, (326, 158))
    d.rectangle([326, 158, 475, 347], outline=INK, width=1)
    centre(d, 401, 352, "PHOTOGRAPH  ·  PHOTO", SANS(8), INK_SOFT)

    # data fields, left column
    fields = [
        ("Type / Type", "P"),
        ("Country code / Code du pays", "VLD"),
        ("Passport No. / No. du passeport", "VD 482 917"),
        ("Surname / Nom", "KOVAC"),
        ("Given names / Prénoms", "ELENA MARA"),
        ("Nationality / Nationalité", "VELDORIAN"),
        ("Date of birth / Date de naissance", "14 MAR 1992"),
        ("Place of birth / Lieu de naissance", "PORT MERIDIAN"),
        ("Sex / Sexe", "F"),
        ("Date of issue / Date de délivrance", "02 JUN 2024"),
        ("Date of expiry / Date d'expiration", "01 JUN 2034"),
        ("Authority / Autorité", "HARBOURMASTER GENERAL"),
    ]
    y = 158
    for label, value in fields:
        text(d, (48, y), label, SANS(9), INK_SOFT)
        text(d, (48, y + 11), value, SERIF_B(14))
        y += 30
    # signature
    d.line([48, 540, 240, 540], fill=INK, width=1)
    text(d, (48, 546), "ELENA M. KOVAC", SERIF(15))
    text(d, (48, 566), "Holder's signature / Signature du titulaire",
         SANS(8), INK_SOFT)

    # MRZ
    mrz1 = "P<VLDKOVAC<<ELENA<MARA<<<<<<<<<<<<<<<<<<<<<<"
    mrz2 = "VD482917<4VLD9203141F3406012<<<<<<<<<<<<<<04"
    assert len(mrz1) == 44 and len(mrz2) == 44
    d.rectangle([48, 600, 476, 668], fill=(232, 226, 208))
    text(d, (52, 608), mrz1, MONO(12))
    text(d, (52, 630), mrz2, MONO(12))
    text(d, (48, 672), "Machine readable zone — do not fold",
         SANS(8), INK_SOFT)


def draw_right(d, img):
    x0, x1 = 528, 996
    d.rectangle([x0, 20, x1, 700], outline=INK, width=2)
    d.rectangle([x0 + 5, 25, x1 - 5, 695], outline=RULE, width=1)
    centre(d, 762, 36, "VISAS", SERIF_B(20))
    centre(d, 762, 62, "Entries, exits and conditions of stay",
           SANS(10), INK_SOFT)
    d.line([548, 84, 976, 84], fill=RULE, width=1)

    # --- stamp 1: Tarnovia entry, 18 SEP 2025
    s1 = stamp_layer([
        ("REPUBLIC OF TARNOVIA", SANS_B(13), 10),
        ("—  ENTRY  —", SANS_B(12), 30),
        ("BORDER POST KESTREL BRIDGE", SANS(10), 48),
        ("18 SEP 2025", SANS_B(13), 66),
    ], BLUE, 260, 88)
    paste_rotated(img, s1, 660, 150, -4)
    circle_stamp(d, 872, 150, 44, BLUE, "TARNOVIA", "18 SEP", "2025")

    # --- stamp 2: Ostara entry, 03 NOV 2025
    s2 = stamp_layer([
        ("KINGDOM OF OSTARA", SANS_B(13), 10),
        ("—  ENTRY  —", SANS_B(12), 30),
        ("PORT OF OSTARA — FERRY TERMINAL", SANS(10), 48),
        ("03 NOV 2025", SANS_B(13), 66),
    ], GREEN, 260, 88)
    paste_rotated(img, s2, 660, 268, 3)
    circle_stamp(d, 872, 268, 44, GREEN, "OSTARA", "03 NOV", "2025")

    # --- stamp 3: Ostara exit, 17 NOV 2025 (14 days after entry)
    s3 = stamp_layer([
        ("KINGDOM OF OSTARA", SANS_B(13), 10),
        ("—  EXIT  —", SANS_B(12), 30),
        ("PORT OF OSTARA — FERRY TERMINAL", SANS(10), 48),
        ("17 NOV 2025", SANS_B(13), 66),
    ], GREEN, 260, 88)
    paste_rotated(img, s3, 660, 386, -3)
    s4 = stamp_layer([
        ("REPUBLIC OF TARNOVIA", SANS_B(13), 10),
        ("—  ENTRY  —", SANS_B(12), 30),
        ("BORDER POST KESTREL BRIDGE", SANS(10), 48),
        ("12 MAR 2026", SANS_B(13), 66),
    ], PURPLE, 260, 88)
    paste_rotated(img, s4, 660, 500, 4)

    # --- fee stamp: the telling detail (red ink, bottom right)
    fee = stamp_layer([
        ("HARBOUR FEE — 40 CROWNS PAID", SANS_B(11), 12),
        ("PORT MERIDIAN  ·  12 MAR 2026", SANS(11), 34),
    ], RED, 240, 62)
    paste_rotated(img, fee, 872, 502, -6)

    # --- visa condition box: what kind of place Veldoria is
    d.rectangle([548, 560, 976, 668], outline=INK, width=1)
    d.rectangle([552, 564, 972, 664], outline=RULE, width=1)
    text(d, (564, 572), "CONDITION 7 — VELDORIAN BORDER CODE §7.2",
         SANS_B(11))
    cond = ("The holder must register with the Harbourmaster within "
            "48 hours of arrival. A passport that has not been stamped "
            "at a harbour office is not valid for onward travel by sea.")
    # manual wrap
    words, lines, cur = cond.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=SANS(10)) <= 396:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    lines.append(cur)
    y = 592
    for ln in lines:
        text(d, (564, y), ln, SANS(10))
        y += 14
    text(d, (564, 648), "Languages of this passport: Veldor · English · French",
         SANS(9), INK_SOFT)


def main():
    img = Image.new("RGB", (W, H), (214, 206, 188))
    d = ImageDraw.Draw(img, "RGBA")
    # spread background + centre fold shadow
    d.rectangle([0, 0, W - 1, H - 1], fill=(222, 214, 196))
    d.rectangle([508, 0, 516, H - 1], fill=(190, 180, 158))
    d.rectangle([500, 0, 507, H - 1], fill=(200, 190, 168))
    d.rectangle([517, 0, 524, H - 1], fill=(200, 190, 168))
    # pages
    d.rectangle([16, 8, 508, 712], fill=PAPER)
    d.rectangle([516, 8, 1008, 712], fill=PAPER)
    draw_left(d, img)
    draw_right(d, img)
    # title strip under the spread
    centre(d, 512, 696, "", SANS(9), INK_SOFT)

    out = Path("/output/entry.png")
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out, format="PNG")
    except OSError:
        out = Path("output/entry.png")
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out, format="PNG")
    print(f"wrote {out} {out.stat().st_size} bytes {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
