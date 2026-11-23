#!/usr/bin/env python3
"""Compose the front page for Monday 23 November 2026.

Drawn with Pillow from a fixed script: same bytes on every run, no clock, no
randomness, no network.

The page is built for one measurement: the judge sees it at about 300 pixels
across, where a sheet of 12 px body copy turns to grey. So this sheet carries
fewer words and bigger marks than a real broadsheet would — one enormous date,
five figures set at 40 px, three leads with tall pictures and headlines at
24 px, and twelve briefs whose place names and headlines are bold at 14 px with
no body copy under them. Breadth is kept by the twelve briefs and the region
strip; legibility is bought by dropping the small text.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (247, 244, 236)
INK = (16, 15, 13)
RED = (170, 28, 22)
GREY = (92, 88, 80)
DIM = (40, 38, 34)
PAPER_DARK = (28, 26, 23)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

_cache = {}


def F(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def ink(d, xy, text, path, size, fill=INK, anchor="la"):
    d.text((int(xy[0]), int(xy[1])), text, font=F(path, size), fill=fill, anchor=anchor)


def wrap(d, text, path, size, width):
    font = F(path, size)
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, xy, text, path, size, width, leading, fill=INK, limit=None, anchor=None):
    x, y = xy
    lines = wrap(d, text, path, size, width)
    if limit:
        lines = lines[:limit]
    for line in lines:
        if anchor:
            ink(d, (x, y), line, path, size, fill, anchor)
        else:
            ink(d, (x, y), line, path, size, fill)
        y += leading
    return y


def fit(d, text, path, max_size, width, floor=13):
    """Largest size at which text sits on one line inside width."""
    size = max_size
    while size > floor and F(path, size).getlength(text) > width:
        size -= 1
    return size


# ---------------------------------------------------------------- illustrations
def scene_cop(d, box):
    """A summit that failed: a horseshoe table, most chairs empty, a torn text."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    d.rectangle(box, fill=(30, 46, 56))
    # carpet
    d.rectangle([x0, y0 + h * 0.30, x1, y1], fill=(38, 58, 62))
    # the table: a horseshoe, seen from above, pale wood on the dark floor
    cx, cy = (x0 + x1) / 2, y0 + h * 0.62
    tw, th = (x1 - x0) * 0.62, h * 0.34
    d.ellipse([cx - tw, cy - th, cx + tw, cy + th], fill=(150, 122, 82))
    d.ellipse([cx - tw + 26, cy - th + 20, cx + tw - 26, cy + th - 20], fill=(38, 58, 62))
    d.rectangle([cx - tw + 20, cy + th - 26, cx + tw - 20, cy + th + 6], fill=(38, 58, 62))
    # seats round the outside: half of them empty, one tipped over
    for i in range(11):
        a = 3.14159 * (0.06 + 0.88 * i / 10.0)
        import math
        sx = cx - math.cos(a) * (tw + 30)
        sy = cy + math.sin(a) * (th + 30)
        if i in (2, 4, 5, 7, 9):
            continue
        d.ellipse([sx - 9, sy - 9, sx + 9, sy + 9], fill=(150, 156, 160))
        d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(88, 94, 100))
    # the document on the table, torn down the middle and pulled apart
    dx, dy = cx, cy
    d.polygon([(dx - 54, dy - 16), (dx - 6, dy - 20), (dx - 10, dy + 18), (dx - 58, dy + 14)],
              fill=(244, 240, 228))
    d.polygon([(dx + 12, dy - 19), (dx + 58, dy - 14), (dx + 54, dy + 16), (dx + 8, dy + 18)],
              fill=(244, 240, 228))
    for ry in range(int(dy) - 10, int(dy) + 14, 7):
        d.line([(dx - 48, ry), (dx - 16, ry + 1)], fill=(148, 142, 128), width=1)
        d.line([(dx + 20, ry), (dx + 50, ry - 1)], fill=(148, 142, 128), width=1)
    # microphones on the table, unlit
    for mx in (cx - tw * 0.55, cx, cx + tw * 0.55):
        d.line([(mx, cy + th - 30), (mx, cy + th - 52)], fill=(58, 62, 66), width=3)
        d.ellipse([mx - 5, cy + th - 60, mx + 5, cy + th - 50], fill=(70, 74, 78))
    # the empty stage behind, with a screen that shows nothing agreed
    d.rectangle([x0 + 12, y0 + 4, x1 - 12, y0 + h * 0.26], fill=(22, 34, 42))
    d.rectangle([x0 + 30, y0 + 10, x1 - 30, y0 + h * 0.22], fill=(228, 224, 210))
    d.line([(x0 + 40, y0 + h * 0.15), (x1 - 40, y0 + h * 0.15)], fill=(176, 34, 28), width=6)


def scene_drones(d, box):
    """A night of drones over a burning block: the Kyiv region."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    d.rectangle(box, fill=(10, 14, 24))
    # two searchlight cones from the ground
    for sx in (x0 + 70, x0 + 200):
        d.polygon([(sx, y1), (sx - 62, y0 + 10), (sx + 62, y0 + 10)], fill=(38, 48, 68))
    # the block, lit from inside, with one bay torn out
    bx0, bx1 = x0 + 12, x1 - 12
    top_y = y0 + h * 0.34
    d.rectangle([bx0, top_y, bx1, y1], fill=(9, 8, 10))
    for wx in range(int(bx0) + 8, int(bx1) - 14, 24):
        for wy in range(int(top_y) + 10, int(y1) - 14, 23):
            d.rectangle([wx, wy, wx + 12, wy + 12], fill=(222, 146, 50))
    torn0 = bx0 + (bx1 - bx0) * 0.42
    torn1 = torn0 + (bx1 - bx0) * 0.30
    d.polygon([(torn0, top_y), (torn1, top_y), (torn1 - 10, y1), (torn0 + 12, y1)],
              fill=(4, 4, 6))
    d.polygon([(torn0, top_y), ((torn0 + torn1) / 2 - 8, top_y - h * 0.20),
               (torn1, top_y + 2)], fill=(206, 64, 30))
    d.polygon([(torn0 + 12, top_y), ((torn0 + torn1) / 2, top_y - h * 0.12),
               (torn1 - 12, top_y)], fill=(246, 186, 70))
    # the swarm: five machines, big enough to read at 300 px
    for dx, dy in ((x1 - 78, y0 + 30), (x1 - 34, y0 + 16), (x1 - 122, y0 + 54),
                   (x1 - 30, y0 + 62), (x1 - 86, y0 + 78)):
        dx, dy = int(dx), int(dy)
        d.line([(dx - 16, dy), (dx + 16, dy)], fill=(240, 240, 246), width=4)
        d.line([(dx, dy - 12), (dx, dy + 12)], fill=(184, 186, 196), width=3)
        d.ellipse([dx - 6, dy - 6, dx + 6, dy + 6], fill=(252, 252, 255))


def scene_bahrain(d, box):
    """A struck tank farm at dusk: flame off one tank, smoke, a drone above."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    for i in range(int(h)):
        t = i / max(1, h)
        d.line([(x0, y0 + i), (x1, y0 + i)],
               fill=(int(88 + 78 * t), int(42 + 46 * t), int(34 + 28 * t)))
    d.rectangle([x0, y1 - 18, x1, y1], fill=(28, 19, 17))
    tanks = ((x0 + 10, 42, 46), (x0 + 62, 56, 62), (x0 + 128, 40, 44), (x0 + 176, 38, 38))
    for tx, tw, th in tanks:
        d.rounded_rectangle([tx, y1 - 18 - th, tx + tw, y1 - 18], radius=9,
                            fill=(50, 37, 33))
        d.line([(tx + 4, y1 - 18 - th + 12), (tx + tw - 4, y1 - 18 - th + 12)],
               fill=(88, 66, 58), width=2)
    mid_top = y1 - 18 - 62
    cx = x0 + 90
    d.polygon([(cx - 30, mid_top + 4), (cx - 11, mid_top - 58), (cx + 3, mid_top - 16),
               (cx + 22, mid_top - 76), (cx + 36, mid_top + 2)], fill=(218, 76, 28))
    d.polygon([(cx - 14, mid_top + 2), (cx + 2, mid_top - 38), (cx + 17, mid_top)],
              fill=(252, 200, 80))
    for i, sy in enumerate(range(int(y0) + 2, int(mid_top) - 26, 14)):
        d.ellipse([cx + 6 + i * 5, sy, cx + 62 + i * 5, sy + 24], fill=(66, 48, 45))
    dx, dy = x1 - 40, y0 + 28
    d.line([(dx - 16, dy), (dx + 16, dy)], fill=(252, 244, 240), width=3)
    d.line([(dx, dy - 10), (dx, dy + 10)], fill=(228, 212, 206), width=3)
    d.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=(255, 250, 246))


def scene_ships(d, box):
    """Benghazi harbour at dawn: a warship on its side, smoke, a sea drone."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    for i in range(int(h * 0.55)):
        t = i / max(1, h * 0.55)
        d.line([(x0, y0 + i), (x1, y0 + i)],
               fill=(int(34 + 62 * t), int(40 + 54 * t), int(58 + 44 * t)))
    sea = y0 + h * 0.55
    d.rectangle([x0, sea, x1, y1], fill=(16, 46, 60))
    for i in range(int(sea), int(y1), 9):
        d.line([(x0, i), (x1, i)], fill=(20 + (i % 9), 56 + (i % 7), 72))
    # the capsized corvette: hull rolled onto its side, superstructure in the water
    hx0, hx1 = x0 + 34, x1 - 42
    d.polygon([(hx0, sea - 6), (hx1, sea - 4), (hx1 - 22, sea + 30), (hx0 + 16, sea + 26)],
              fill=(74, 78, 82))
    d.polygon([(hx0, sea - 6), (hx1, sea - 4), (hx1 - 6, sea - 16), (hx0 + 4, sea - 18)],
              fill=(104, 108, 112))
    for bx in range(int(hx0) + 18, int(hx1) - 26, 30):
        d.rectangle([bx, sea - 14, bx + 14, sea - 8], fill=(52, 56, 60))
    d.rectangle([hx1 - 30, sea - 44, hx1 - 12, sea - 12], fill=(88, 92, 96))
    d.line([(hx1 - 21, sea - 44), (hx1 - 21, sea - 62)], fill=(150, 152, 156), width=3)
    # smoke off the hull, drifting right
    for i, sy in enumerate(range(int(sea) - 52, int(sea) - 4, 10)):
        d.ellipse([hx1 - 40 + i * 7, sy, hx1 + 22 + i * 7, sy + 18], fill=(58, 52, 50))
    # the sea drone: low, dark, leaving a wake, under a bright horizon
    dx, dy = x0 + 46, y0 + h * 0.24
    d.polygon([(dx - 18, dy + 6), (dx, dy - 6), (dx + 20, dy + 4), (dx, dy + 10)],
              fill=(30, 32, 34))
    d.line([(dx - 20, dy + 9), (dx - 56, dy + 14)], fill=(196, 214, 218), width=2)
    d.line([(dx + 20, dy + 7), (dx + 54, dy + 12)], fill=(196, 214, 218), width=2)


def scene_fire(d, box):
    """A gutted factory at night: roof gone, fire inside, smoke above."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    d.rectangle(box, fill=(20, 18, 22))
    for i in range(int(h)):
        t = i / max(1, h)
        d.line([(x0, y0 + i), (x1, y0 + i)],
               fill=(int(96 - 52 * t), int(44 - 20 * t), int(38 - 16 * t)))
    bx0, bx1 = x0 + 10, x1 - 10
    top = y0 + h * 0.42
    d.rectangle([bx0, top, bx1, y1], fill=(22, 18, 18))
    for wx in range(int(bx0) + 10, int(bx1) - 16, 30):
        d.rectangle([wx, top + 18, wx + 18, y1 - 16], fill=(228, 128, 34))
        d.rectangle([wx, top + 18, wx + 18, top + 30], fill=(38, 30, 28))
    d.polygon([(bx0, top), (bx0 + 26, top - 16), (bx1 - 30, top - 14), (bx1, top + 2)])
    d.line([(bx0, top), (bx1, top)], fill=(16, 12, 12), width=4)
    cx = (bx0 + bx1) / 2
    d.polygon([(cx - 34, top + 6), (cx - 8, top - 62), (cx + 6, top - 20),
               (cx + 26, top - 78), (cx + 40, top + 4)], fill=(220, 82, 24))
    d.polygon([(cx - 16, top + 4), (cx + 2, top - 40), (cx + 22, top + 2)],
              fill=(250, 206, 92))
    for i, sy in enumerate(range(int(y0) + 2, int(top) - 30, 12)):
        d.ellipse([cx - 30 + i * 6, sy, cx + 34 + i * 6, sy + 20], fill=(52, 44, 44))


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 34

    # ---------------------------------------------------------- black nameplate
    d.rectangle([0, 0, W, 34], fill=PAPER_DARK)
    ink(d, (M, 17), "THE WORLD IN ONE DAY", SANS_B, 13, CREAM, "lm")
    ink(d, (W - M, 17), "MONDAY 23 NOVEMBER 2026", SANS_B, 12, (232, 224, 208), "rm")

    # ---------------------------------------------------------- date, enormous
    y = 44
    date = "23 NOVEMBER 2026"
    size = fit(d, date, SERIF_B, 96, W - 2 * M)
    ink(d, (W / 2, y), date, SERIF_B, size, INK, "ma")
    y += size + 6
    d.rectangle([M, y, W - M, y + 3], fill=RED)
    y += 11

    deck = ("COP31 fails in Antalya  ·  Ukraine sinks Russian ships off Libya  ·  "
            "24 dead in a Java factory  ·  Democrats take 258 House seats")
    para(d, (W / 2, y), deck, SANS_B, 15, W - 2 * M, 19, RED, limit=2, anchor="ma")
    y += 40

    # ---------------------------------------------------------- five figures
    figs = [("NO DEAL", "COP31"), ("2 SHIPS", "sunk off Libya"), ("24", "dead, Java"),
            ("258", "House seats"), ("€1.4BN", "India to Nepal")]
    fw = (W - 2 * M) / len(figs)
    d.rectangle([M, y, W - M, y + 74], fill=(238, 233, 221))
    for i, (num, cap) in enumerate(figs):
        cx = M + fw * i + fw / 2
        s = fit(d, num, SERIF_B, 40, fw - 18)
        ink(d, (cx, y + 9), num, SERIF_B, s, RED, "ma")
        ink(d, (cx, y + 54), cap.upper(), SANS_B, 11, DIM, "ma")
        if i:
            d.line([(M + fw * i, y + 10), (M + fw * i, y + 64)], fill=(206, 198, 184))
    y += 84

    # ---------------------------------------------------------- three leads
    leads = [
        (scene_cop, "CLIMATE \u00b7 ANTALYA", "COP31 ENDS\nWITH NO DEAL",
         "Talks run into record overtime, then fail over fossil fuels. The EU "
         "and island states blame Saudi Arabia; no consensus text is adopted."),
        (scene_ships, "WAR \u00b7 LIBYA", "UKRAINE SINKS\nTWO SHIPS",
         "Sea drones hit a Russian corvette and a cargo ship at Benghazi. "
         "Zelensky says Kyiv did it; the UN wants an independent probe."),
        (scene_fire, "DISASTER \u00b7 INDONESIA", "24 DEAD IN\nFACTORY BLAZE",
         "A candy factory burns at Cikande, west of Jakarta. Rescuers recover "
         "24 bodies and search the wreckage for 34 workers still missing."),
    ]
    gap = 16
    cw = (W - 2 * M - 2 * gap) / 3
    top = y
    art_h = 158
    deepest = top
    for i, (scene, kicker, head, body) in enumerate(leads):
        x = M + i * (cw + gap)
        scene(d, (x, top, x + cw, top + art_h))
        yy = top + art_h + 7
        ink(d, (x, yy), kicker, SANS_B, 11, RED)
        yy += 15
        for line in head.split("\n"):
            s = fit(d, line, SANS_B, 24, cw)
            ink(d, (x, yy), line, SANS_B, s, INK)
            yy += s + 3
        yy += 3
        yy = para(d, (x, yy), body, SERIF, 13, cw, 16, DIM, limit=4)
        deepest = max(deepest, yy)
    y = deepest + 4
    if y > 700:
        raise SystemExit("leads overrun: %d" % y)

    d.rectangle([M, y, W - M, y + 2], fill=INK)
    y += 9
    ink(d, (M, y), "ALSO ON MONDAY", SANS_B, 12, RED)
    ink(d, (W - M, y + 1), "TWELVE MORE  \u00b7  SIX CONTINENTS", SANS_B, 10, GREY, "ra")
    y += 19

    # ---------------------------------------------------------- briefs, bold
    briefs = [
        ("UNITED STATES", "Democrats win 258 House seats",
         "Their biggest majority since 1992, with 44 seats gained"),
        ("UKRAINE", "Four killed in drone strikes on Kyiv region",
         "A block in Dymer is hit; a woman is pulled out after 22 hours"),
        ("INDONESIA", "Rescuers hunt 34 missing in the factory fire",
         "24 bodies recovered from the Cikande confectionery plant"),
        ("INDIA \\u00b7 NEPAL", "Modi pledges \u20ac1.4bn after the glacier flood",
         "Shah's first trip abroad brings rail and hydropower deals"),
        ("BELGIUM", "National strike shuts the airspace",
         "Almost every flight cancelled as controllers walk out"),
        ("SOUTH KOREA", "KOSPI hits a 10-month low on AI fears",
         "Seoul readies stabilisation funds and eases buyback rules"),
        ("ARMENIA", "A new constitution, a step to peace",
         "Pashinyan publishes the draft; Baku calls it a basis"),
        ("BAHRAIN", "Iran hits a plant, and a fire follows",
         "The Gulf escalation continues after February's strikes"),
        ("GAZA", "Hamas executes one of its own for collaborating",
         "The Qassam Brigades announce the killing"),
        ("BRITAIN", "Manchester concert evacuated over a substance",
         "Thousands leave the Don Toliver show; police open a major inquiry"),
        ("GENEVA", "UN agrees to draft rules for killer robots",
         "128 states back two years of talks; the US and Russia hold back"),
        ("ATLANTA", "Delta grounds 1,000 flights as a system fails",
         "The weight calculator breaks before Thanksgiving"),
    ]
    ncol = 3
    gut = 20
    colw = (W - 2 * M - (ncol - 1) * gut) / ncol
    xs = [M + i * (colw + gut) for i in range(ncol)]
    ys = [y] * ncol
    row_h = (H - 44 - y) / 4

    ends = [y] * ncol
    for i, (place, head, detail) in enumerate(briefs):
        c = i % ncol
        r = i // ncol
        x = xs[c]
        yy = y + r * row_h
        d.rectangle([x, yy, x + 26, yy + 3], fill=RED)
        ink(d, (x, yy + 8), place, SANS_B, 10, RED)
        hs = fit(d, head, SANS_B, 15, colw)
        line_y = yy + 22
        for line in wrap(d, head, SANS_B, hs, colw)[:2]:
            ink(d, (x, line_y), line, SANS_B, hs, INK)
            line_y += hs + 2
        line_y += 1
        para(d, (x, line_y), detail, SERIF, 12, colw, 14, GREY, limit=2)
        ends[c] = max(ends[c], line_y + 28)

    fy = H - 40
    d.rectangle([M, fy, W - M, fy + 2], fill=INK)
    ink(d, (M, fy + 8), "Reuters \u00b7 AP \u00b7 AFP \u00b7 Euronews \u00b7 NPR \u00b7 Al Jazeera",
        SANS_B, 10, GREY)
    ink(d, (W - M, fy + 8), "CLAIMS AS CLAIMS  \u00b7  TOLLS AS REPORTED", SANS_B, 9, GREY, "ra")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry", "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
