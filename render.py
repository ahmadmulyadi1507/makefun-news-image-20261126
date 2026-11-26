#!/usr/bin/env python3
"""Render the news-image-20261126 entry: a one-page front-page infographic
summing up Thursday 26 November 2026's world news. Drawn from scratch with
PIL using flat shapes only -- no photos, no copied artwork. The program uses
no network. Output: entry.png, 1024x1024, well under 1 MiB."""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
NAVY = (22, 35, 63)
GOLD = (201, 162, 39)
INK = (24, 28, 36)
GREY = (107, 101, 88)
CARD = (255, 255, 255)
BORDER = (216, 210, 196)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap: split text into lines no wider than max_w."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def star(draw, cx, cy, r_out, r_in, points, fill):
    """A filled star with the given number of points."""
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        angle = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(pts, fill=fill)


def flame(draw, cx, cy, s, fill):
    """A simple teardrop flame centred at (cx, cy), scaled by s."""
    draw.polygon([(cx, cy - 26 * s), (cx + 14 * s, cy + 4 * s),
                  (cx + 6 * s, cy + 16 * s), (cx - 6 * s, cy + 16 * s),
                  (cx - 14 * s, cy + 4 * s)], fill=fill)
    draw.ellipse([cx - 10 * s, cy + 2 * s, cx + 10 * s, cy + 22 * s], fill=fill)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------- header ----------------
d.rectangle([0, 0, W, 116], fill=NAVY)
d.rectangle([0, 116, W, 121], fill=GOLD)
f_date = font(BOLD, 25)
f_title = font(BOLD, 54)
date_line = "THURSDAY  -  26 NOVEMBER 2026"
d.text(((W - d.textlength(date_line, font=f_date)) / 2, 14),
       date_line, font=f_date, fill=GOLD)
title = "THE WORLD IN A DAY"
d.text(((W - d.textlength(title, font=f_title)) / 2, 46),
       title, font=f_title, fill=(255, 255, 255))

# ---------------- story cards ----------------
# (accent colour, headline, fact, pictogram key)
STORIES = [
    ((30, 60, 120), "US TARIFFS HIT 14 PARTNERS",
     "Washington proposes new tariffs on China, EU, Japan, India", "tariffs"),
    ((178, 34, 34), "CAIRO TANKER FIRE KILLS 31",
     "Fuel tanker overturns on ring road; at least 31 dead, 21 hurt", "fire"),
    ((20, 90, 70), "UKRAINE HITS RUSSIAN AIRBASE",
     "Five jets damaged at Savasleyka; three MiG-31s, two Su-34s", "airbase"),
    ((90, 60, 110), "FIRST PAKISTANI IN SPACE",
     "Muhammad Zeeshan Ali boards China's Tiangong station", "space"),
    ((120, 80, 30), "KIM WIDENS NUCLEAR DEPLOYMENT",
     "North Korea to deploy tactical nukes across more domains", "missile"),
    ((196, 120, 20), "13 MINERS TRAPPED IN FLOOD",
     "Rescuers race to flooded illegal gold mine near Bogor", "mine"),
]

CARD_W, CARD_H, GAP, MARGIN = 480, 269, 16, 24
f_head = font(BOLD, 30)
f_fact = font(REGULAR, 20)
f_num = font(BOLD, 22)


def pic_tariffs(x0, y0, w, h):
    # sky and sea
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(196, 222, 238))
    d.rectangle([x0, y0 + 74, x0 + w, y0 + h], fill=(52, 110, 158))
    for wx in range(0, w, 56):
        d.arc([x0 + wx, y0 + 82, x0 + wx + 44, y0 + 98], start=0, end=180,
              fill=(190, 220, 240), width=2)
    # container ship: hull, bridge, stacked containers
    d.polygon([(x0 + 40, y0 + 66), (x0 + 400, y0 + 66), (x0 + 372, y0 + 92),
               (x0 + 66, y0 + 92)], fill=(38, 48, 66))
    d.rectangle([x0 + 296, y0 + 34, x0 + 332, y0 + 66], fill=(240, 240, 238))
    d.rectangle([x0 + 306, y0 + 42, x0 + 322, y0 + 50], fill=(30, 60, 120))
    for cx, col in [(70, (178, 34, 34)), (118, (20, 90, 70)),
                    (166, (196, 120, 20)), (214, (30, 60, 120))]:
        d.rectangle([x0 + cx, y0 + 44, x0 + cx + 44, y0 + 66], fill=col)
    for cx, col in [(94, (90, 60, 110)), (142, (178, 34, 34)),
                    (190, (20, 90, 70))]:
        d.rectangle([x0 + cx, y0 + 22, x0 + cx + 44, y0 + 44], fill=col)
    # big percent sign on the right
    f_pct = font(BOLD, 64)
    d.text((x0 + 392, y0 + 4), "%", font=f_pct, fill=(255, 255, 255),
           anchor="ra")


def pic_fire(x0, y0, w, h):
    # dusk sky over the ring road
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(58, 46, 54))
    d.ellipse([x0 + 34, y0 + 10, x0 + 74, y0 + 50], fill=(255, 176, 66))
    d.rectangle([x0, y0 + 76, x0 + w, y0 + h], fill=(52, 52, 58))
    for dx in range(20, w, 90):
        d.rectangle([x0 + dx, y0 + 92, x0 + dx + 40, y0 + 97], fill=(240, 220, 120))
    # overturned fuel tanker on its side
    d.ellipse([x0 + 150, y0 + 30, x0 + 300, y0 + 78], fill=(196, 120, 20))
    d.ellipse([x0 + 300, y0 + 44, x0 + 322, y0 + 66], fill=(120, 72, 30))
    d.ellipse([x0 + 182, y0 + 62, x0 + 206, y0 + 86], fill=(30, 30, 34))
    d.ellipse([x0 + 238, y0 + 62, x0 + 262, y0 + 86], fill=(30, 30, 34))
    # flames above the tank
    flame(d, x0 + 196, y0 + 34, 1.1, (255, 110, 30))
    flame(d, x0 + 246, y0 + 26, 1.4, (255, 176, 32))
    flame(d, x0 + 292, y0 + 36, 0.9, (255, 110, 30))
    # smoke puffs
    for sx, sy, sr in [(210, 8, 9), (238, 2, 11), (268, 10, 8)]:
        d.ellipse([x0 + sx - sr, y0 + sy, x0 + sx + sr, y0 + sy + sr * 2],
                  fill=(180, 175, 168))
    # warning triangle at the left
    wx, wy = x0 + 62, y0 + 52
    d.polygon([(wx, wy - 22), (wx - 24, wy + 18), (wx + 24, wy + 18)],
              fill=(255, 176, 32), outline=(255, 255, 255), width=2)
    d.rectangle([wx - 2, wy - 12, wx + 2, wy + 4], fill=(178, 34, 34))
    d.ellipse([wx - 2, wy + 8, wx + 2, wy + 12], fill=(178, 34, 34))


def pic_airbase(x0, y0, w, h):
    # sky, runway strip, grass
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(168, 198, 226))
    d.rectangle([x0, y0 + 60, x0 + w, y0 + h], fill=(96, 130, 88))
    d.polygon([(x0, y0 + 92), (x0 + w, y0 + 66), (x0 + w, y0 + 108),
               (x0, y0 + 108)], fill=(52, 54, 60))
    for dx in range(20, w - 40, 80):
        d.rectangle([x0 + dx, y0 + 82, x0 + dx + 34, y0 + 88],
                    fill=(255, 255, 255))
    # fighter jet parked on the apron, seen from above
    jx, jy = x0 + 150, y0 + 40
    d.polygon([(jx - 66, jy), (jx - 30, jy - 12), (jx + 34, jy - 8),
               (jx + 66, jy), (jx + 34, jy + 8), (jx - 30, jy + 12)],
              fill=(90, 100, 112))
    d.polygon([(jx - 6, jy - 8), (jx + 22, jy - 30), (jx + 26, jy - 8)],
              fill=(70, 78, 90))
    d.polygon([(jx - 6, jy + 8), (jx + 22, jy + 30), (jx + 26, jy + 8)],
              fill=(70, 78, 90))
    d.ellipse([jx + 44, jy - 5, jx + 66, jy + 5], fill=(30, 60, 120))
    # second jet further down the runway, smaller
    jx, jy = x0 + 360, y0 + 74
    d.polygon([(jx - 40, jy), (jx - 18, jy - 8), (jx + 22, jy - 5),
               (jx + 40, jy), (jx + 22, jy + 5), (jx - 18, jy + 8)],
              fill=(120, 128, 138))
    # impact starburst where a strike landed
    star(d, x0 + 420, y0 + 30, 26, 11, 8, (255, 176, 32))
    star(d, x0 + 420, y0 + 30, 14, 6, 8, (255, 110, 30))
    # small hangar on the left
    d.rectangle([x0 + 24, y0 + 24, x0 + 84, y0 + 58], fill=(120, 128, 138))
    d.pieslice([x0 + 24, y0 + 4, x0 + 84, y0 + 44], start=180, end=360,
               fill=(90, 96, 106))


def pic_space(x0, y0, w, h):
    # night sky with stars
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(12, 16, 44))
    for sx, sy, r in [(40, 18, 3), (120, 44, 2), (210, 14, 3), (300, 30, 2),
                      (380, 16, 3), (440, 48, 2), (60, 78, 2), (160, 88, 2),
                      (330, 84, 3), (420, 76, 2)]:
        d.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r],
                  fill=(255, 255, 255))
    star(d, x0 + 452, y0 + 22, 8, 3, 5, (255, 214, 90))
    # space station: core module, solar panels, docked capsule
    cx, cy = x0 + 240, y0 + 54
    d.rectangle([cx - 60, cy - 12, cx + 60, cy + 12], fill=(200, 205, 214))
    d.rectangle([cx - 60, cy - 12, cx - 44, cy + 12], fill=(140, 148, 160))
    d.rectangle([cx - 150, cy - 18, cx - 66, cy + 18], fill=(30, 60, 120))
    d.rectangle([cx + 66, cy - 18, cx + 150, cy + 18], fill=(30, 60, 120))
    for px in range(-150, -66, 14):
        d.line([cx + px, cy - 18, cx + px, cy + 18], fill=(90, 130, 190), width=1)
    for px in range(66, 150, 14):
        d.line([cx + px, cy - 18, cx + px, cy + 18], fill=(90, 130, 190), width=1)
    d.ellipse([cx + 66, cy - 10, cx + 92, cy + 10], fill=(255, 255, 255))
    # astronaut in a green-flagged suit floating beside the station
    ax, ay = x0 + 84, y0 + 62
    d.ellipse([ax - 10, ay - 26, ax + 10, ay - 6], fill=(245, 244, 238))
    d.rectangle([ax - 12, ay - 6, ax + 12, ay + 18], fill=(245, 244, 238))
    d.rectangle([ax - 4, ay + 2, ax + 12, ay + 10], fill=(20, 90, 70))
    d.rectangle([ax - 18, ay - 2, ax - 12, ay + 14], fill=(245, 244, 238))
    d.rectangle([ax + 12, ay - 2, ax + 18, ay + 14], fill=(245, 244, 238))


def pic_missile(x0, y0, w, h):
    # night sky, moon, stars
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(14, 20, 40))
    for sx, sy in [(30, 20), (90, 44), (170, 16), (250, 40), (330, 18),
                   (410, 46), (450, 22)]:
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3],
                  fill=(255, 255, 255))
    d.ellipse([x0 + 396, y0 + 10, x0 + 432, y0 + 46], fill=(235, 225, 190))
    # missile rising from the launcher, raised so its exhaust is visible
    # in the gap between the missile base and the launcher (the old flame
    # sat below the pictogram edge and was clipped invisible)
    mx, my = x0 + 190, y0 + 40
    d.polygon([(mx - 12, my + 26), (mx - 12, my - 18), (mx, my - 36),
               (mx + 12, my - 18), (mx + 12, my + 26)], fill=(210, 214, 222))
    d.polygon([(mx - 12, my - 18), (mx - 24, my + 2), (mx - 12, my + 2)],
              fill=(178, 34, 34))
    d.polygon([(mx + 12, my - 18), (mx + 24, my + 2), (mx + 12, my + 2)],
              fill=(178, 34, 34))
    d.rectangle([mx - 12, my + 6, mx + 12, my + 14], fill=(178, 34, 34))
    # exhaust flame in the gap between missile base and launcher
    flame(d, mx, my + 36, 0.7, (255, 176, 32))
    flame(d, mx, my + 44, 0.45, (255, 110, 30))
    # launcher vehicle on the ground
    d.rectangle([x0 + 120, y0 + 88, x0 + 260, y0 + 100], fill=(52, 58, 50))
    d.ellipse([x0 + 140, y0 + 96, x0 + 162, y0 + 108], fill=(20, 20, 22))
    d.ellipse([x0 + 218, y0 + 96, x0 + 240, y0 + 108], fill=(20, 20, 22))
    # second missile silhouette on the horizon
    d.rectangle([x0 + 330, y0 + 60, x0 + 342, y0 + 100], fill=(120, 124, 132))
    d.polygon([(x0 + 330, y0 + 60), (x0 + 342, y0 + 60), (x0 + 336, y0 + 46)],
              fill=(120, 124, 132))


def pic_mine(x0, y0, w, h):
    # rock face and tunnel mouth
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(74, 62, 52))
    d.polygon([(x0 + 140, y0 + 108), (x0 + 140, y0 + 34), (x0 + 190, y0 + 10),
               (x0 + 240, y0 + 34), (x0 + 240, y0 + 108)], fill=(24, 20, 18))
    # timber supports around the mouth
    d.rectangle([x0 + 132, y0 + 30, x0 + 140, y0 + 108], fill=(110, 72, 40))
    d.rectangle([x0 + 240, y0 + 30, x0 + 248, y0 + 108], fill=(110, 72, 40))
    d.rectangle([x0 + 132, y0 + 22, x0 + 248, y0 + 30], fill=(110, 72, 40))
    # flood water pouring out of the tunnel
    d.polygon([(x0 + 140, y0 + 78), (x0 + 240, y0 + 78), (x0 + 300, y0 + 108),
               (x0 + 80, y0 + 108)], fill=(52, 110, 158))
    for wx in range(90, 290, 40):
        d.arc([x0 + wx, y0 + 88, x0 + wx + 30, y0 + 102], start=0, end=180,
              fill=(160, 200, 230), width=2)
    # miner's helmet with headlamp beam inside the tunnel
    hx, hy = x0 + 190, y0 + 52
    d.pieslice([hx - 18, hy - 14, hx + 18, hy + 14], start=180, end=360,
               fill=(255, 196, 66))
    d.rectangle([hx - 20, hy - 2, hx + 20, hy + 4], fill=(255, 196, 66))
    d.ellipse([hx - 4, hy - 4, hx + 4, hy + 4], fill=(255, 255, 220))
    d.polygon([(hx + 4, hy), (hx + 52, hy - 12), (hx + 52, hy + 12)],
              fill=(255, 244, 180))
    # rescue rope and lantern at the right
    d.line([x0 + 330, y0 + 8, x0 + 330, y0 + 40], fill=(240, 220, 160), width=3)
    d.rectangle([x0 + 318, y0 + 40, x0 + 342, y0 + 62], fill=(255, 176, 32))
    d.rectangle([x0 + 322, y0 + 46, x0 + 338, y0 + 56], fill=(255, 244, 180))
    d.line([x0 + 330, y0 + 62, x0 + 380, y0 + 96], fill=(240, 220, 160), width=3)


PICS = {"tariffs": pic_tariffs, "fire": pic_fire, "airbase": pic_airbase,
        "space": pic_space, "missile": pic_missile, "mine": pic_mine}

for i, (accent, headline, fact, key) in enumerate(STORIES):
    col, row = i % 2, i // 2
    x0 = MARGIN + col * (CARD_W + GAP)
    y0 = 136 + row * (CARD_H + GAP)
    d.rectangle([x0, y0, x0 + CARD_W, y0 + CARD_H], fill=CARD,
                outline=BORDER, width=1)
    d.rectangle([x0, y0, x0 + CARD_W, y0 + 6], fill=accent)
    PICS[key](x0, y0 + 6, CARD_W, 108)
    # number badge
    bx, by = x0 + 14, y0 + 20
    d.ellipse([bx, by, bx + 34, by + 34], fill=accent)
    num = str(i + 1)
    d.text((bx + 17 - d.textlength(num, font=f_num) / 2, by + 4),
           num, font=f_num, fill=(255, 255, 255))
    # headline (max 2 lines) + fact (max 2 lines)
    head_lines = wrap(d, headline, f_head, CARD_W - 32)
    fact_lines = wrap(d, fact, f_fact, CARD_W - 32)
    print(f"card {i + 1}: headline {len(head_lines)} lines, "
          f"fact {len(fact_lines)} lines")
    ty = y0 + 126
    for ln in head_lines[:2]:
        d.text((x0 + 16, ty), ln, font=f_head, fill=INK)
        ty += 37
    ty = y0 + 126 + 76
    for ln in fact_lines[:2]:
        d.text((x0 + 16, ty), ln, font=f_fact, fill=GREY)
        ty += 24

# ---------------- footer ----------------
f_foot = font(REGULAR, 18)
foot = "Six stories, one day - 26 November 2026 - Reported 26 November 2026"
d.text(((W - d.textlength(foot, font=f_foot)) / 2, 988),
       foot, font=f_foot, fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
print("bytes:", os.path.getsize("entry.png"))
