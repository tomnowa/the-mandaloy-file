#!/usr/bin/env python3
"""Open Graph social share card for The Mondaloy File.
Output: og-triangle.png at 1200x630"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

W, H = 1200, 630
BG = (13, 11, 8)
INK = (232, 227, 216)
INK_SOFT = (184, 178, 163)
INK_FAINT = (109, 102, 89)
ACCENT = (196, 71, 42)
RULE = (42, 37, 28)
OUTPUT = "og-triangle.png"

def load_font(size, style="regular"):
    serif = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ]
    serif_italic = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
    ]
    mono = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    if style == "mono":
        pool = mono
    elif style == "italic":
        pool = serif_italic
    else:
        pool = serif
    for path in pool:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# Left column: text. Right column: triangle.
# Text area: x 60-700. Triangle area: x 720-1140.

# Top kicker
kicker_font = load_font(15, "mono")
draw.line([(60, 62), (135, 62)], fill=ACCENT, width=2)
draw.text((151, 52), "THE MONDALOY FILE", font=kicker_font, fill=ACCENT)

# Headline - 4 lines of roman, 1 line of italic accent
headline_font = load_font(46, "regular")
italic_font = load_font(46, "italic")
lines = [
    "Three people knew",
    "how to make a metal",
    "America needs for",
    "its rocket engines.",
]
y = 130
for line in lines:
    draw.text((60, y), line, font=headline_font, fill=INK)
    y += 58

draw.text((60, y + 14), "They're all gone.", font=italic_font, fill=ACCENT)

# Bottom dek
dek_font = load_font(17, "regular")
dek_y = H - 118
draw.text((60, dek_y),
          "Five cleared defense personnel vanished",
          font=dek_font, fill=INK_SOFT)
draw.text((60, dek_y + 26),
          "in ten months at 10× the expected rate.",
          font=dek_font, fill=INK_SOFT)

# URL
url_font = load_font(13, "mono")
draw.text((60, dek_y + 62), "MONDALOY.NOWA.CA",
          font=url_font, fill=ACCENT)

# Triangle: center at (930, 310), radius 120
cx, cy, r = 930, 310, 120

positions = {
    "MJR": (cx, cy - r),
    "DH":  (cx - r * math.sin(math.radians(60)), cy + r * math.cos(math.radians(60))),
    "WM":  (cx + r * math.sin(math.radians(60)), cy + r * math.cos(math.radians(60))),
}

def dashed_line(draw, start, end, fill, width=1, dash=5, gap=5):
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    dist = (dx**2 + dy**2) ** 0.5
    if dist == 0: return
    steps = int(dist // (dash + gap))
    for i in range(steps):
        t0 = i * (dash + gap) / dist
        t1 = (i * (dash + gap) + dash) / dist
        draw.line(
            [(x1 + dx * t0, y1 + dy * t0), (x1 + dx * t1, y1 + dy * t1)],
            fill=fill, width=width
        )

dashed_line(draw, positions["MJR"], positions["DH"], (80, 72, 60))
dashed_line(draw, positions["DH"], positions["WM"], (80, 72, 60))
dashed_line(draw, positions["WM"], positions["MJR"], (80, 72, 60))

# Center hub
draw.ellipse([cx-42, cy-42, cx+42, cy+42], outline=ACCENT, width=2)
draw.ellipse([cx-24, cy-24, cx+24, cy+24], outline=(138, 53, 32), width=1)
hub_label = load_font(11, "regular")
hub_sub = load_font(8, "mono")
bbox = draw.textbbox((0, 0), "MONDALOY", font=hub_label)
draw.text((cx - (bbox[2]-bbox[0])/2, cy - 7), "MONDALOY", font=hub_label, fill=ACCENT)
bbox = draw.textbbox((0, 0), "AR1 ENGINE", font=hub_sub)
draw.text((cx - (bbox[2]-bbox[0])/2, cy + 7), "AR1 ENGINE", font=hub_sub, fill=INK_SOFT)

# Nodes
node_font = load_font(13, "mono")
role_font = load_font(7, "mono")
status_font = load_font(8, "mono")

def node(x, y, label, color, role):
    draw.ellipse([x-30, y-30, x+30, y+30], outline=color, width=2, fill=BG)
    bbox = draw.textbbox((0, 0), label, font=node_font)
    draw.text((x - (bbox[2]-bbox[0])/2, y - 8), label, font=node_font, fill=color)
    bbox = draw.textbbox((0, 0), role, font=role_font)
    draw.text((x - (bbox[2]-bbox[0])/2, y + 7), role, font=role_font, fill=INK_SOFT)

def status_label(x, y, text, color, above=False):
    bbox = draw.textbbox((0, 0), text, font=status_font)
    tw = bbox[2] - bbox[0]
    yoff = -48 if above else 40
    draw.text((x - tw/2, y + yoff), text, font=status_font, fill=color)

node(positions["MJR"][0], positions["MJR"][1], "MJR", ACCENT, "INVENTOR")
status_label(positions["MJR"][0], positions["MJR"][1], "MISSING · JUN 2025", ACCENT, above=True)

node(positions["DH"][0], positions["DH"][1], "DH", INK_FAINT, "QUALIFIER")
status_label(positions["DH"][0], positions["DH"][1], "DECEASED · JAN 2014", INK_FAINT)

node(positions["WM"][0], positions["WM"][1], "WM", ACCENT, "FUNDER")
status_label(positions["WM"][0], positions["WM"][1], "MISSING · FEB 2026", ACCENT)

# Triangle caption
tri_cap = load_font(9, "mono")
bbox = draw.textbbox((0, 0), "PATENTS EXPIRED 2012", font=tri_cap)
draw.text((cx - (bbox[2]-bbox[0])/2, cy + r + 80), "PATENTS EXPIRED 2012",
          font=tri_cap, fill=INK_FAINT)

# Bottom attribution strip
draw.line([(60, H - 40), (W - 60, H - 40)], fill=RULE, width=1)
attr_font = load_font(10, "mono")
draw.text((60, H - 28), "OPEN-SOURCE INVESTIGATION · V7 · APR 2026",
          font=attr_font, fill=INK_FAINT)
right_text = "SOURCE: @0xTars"
bbox = draw.textbbox((0, 0), right_text, font=attr_font)
draw.text((W - 60 - (bbox[2]-bbox[0]), H - 28), right_text,
          font=attr_font, fill=INK_FAINT)

img.save(OUTPUT, "PNG", optimize=True)
print(f"Wrote {OUTPUT} ({os.path.getsize(OUTPUT)} bytes)")
