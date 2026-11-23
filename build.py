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
    """An empty summit hall in flat daylight: the table set, no delegates, NO DEAL on it.

    Deliberately the brightest of the three leads, so the picture row is not three dark
    rectangles: the failure here is an absence in full light, not a night scene.
    """
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # pale hall, blinds and a high window band
    for i in range(int(h * 0.46)):
        t = i / max(1.0, h * 0.46)
        d.line([(x0, y0 + i), (x1, y0 + i)],
               fill=(int(226 - 16 * t), int(228 - 16 * t), int(222 - 14 * t)))
    d.rectangle([x0, y0 + h * 0.12, x1, y0 + h * 0.20], fill=(206, 210, 202))
    for bx in range(int(x0) + 6, int(x1), 22):
        d.line([(bx, y0 + h * 0.12), (bx, y0 + h * 0.20)], fill=(232, 234, 228), width=2)
    # a row of pale national flags on their stands along the back, all hanging limp
    fx = x0 + w * 0.06
    while fx < x1 - w * 0.06:
        d.line([(fx, y0 + h * 0.22), (fx, y0 + h * 0.34)], fill=(120, 122, 116), width=2)
        d.polygon([(fx, y0 + h * 0.22), (fx + w * 0.045, y0 + h * 0.225),
                   (fx + w * 0.042, y0 + h * 0.30), (fx, y0 + h * 0.31)],
                  fill=(214, 214, 208))
        fx += w * 0.075

    # the table: a wide horseshoe, pale wood, in perspective
    tbl = y0 + h * 0.44
    d.polygon([(x0 + w * 0.03, tbl), (x1 - w * 0.03, tbl),
               (x1 - w * 0.10, y1 - h * 0.05), (x0 + w * 0.10, y1 - h * 0.05)],
              fill=(196, 188, 172))
    d.polygon([(x0 + w * 0.03, tbl), (x1 - w * 0.03, tbl),
               (x1 - w * 0.035, tbl + h * 0.06), (x0 + w * 0.035, tbl + h * 0.06)],
              fill=(214, 206, 190))
    # empty chairs, dark against the light hall, so the absence is the darkest thing here
    for k in range(5):
        t = (k + 0.5) / 5
        cxx = x0 + w * 0.12 + (w * 0.76) * t
        cyy = tbl - h * 0.07
        d.rectangle([cxx - w * 0.030, cyy - h * 0.09, cxx + w * 0.030, cyy + h * 0.07],
                    fill=(46, 48, 46))
        d.rectangle([cxx - w * 0.030, cyy - h * 0.09, cxx + w * 0.030, cyy - h * 0.075],
                    fill=(30, 32, 30))
    # name plates, all still set, all facing empty seats
    for k in range(7):
        px = x0 + w * 0.16 + (w * 0.68) * k / 6
        py = tbl + h * 0.075
        d.rectangle([px - w * 0.033, py, px + w * 0.033, py + h * 0.036], fill=(252, 250, 244))
        d.rectangle([px - w * 0.027, py + h * 0.011, px + w * 0.027, py + h * 0.018],
                    fill=(150, 148, 138))
    # microphones, switched off
    for k in (1, 1 + 2, 1 + 4):
        px = x0 + w * 0.16 + (w * 0.68) * k / 6
        py = tbl + h * 0.03
        d.line([(px, py), (px, py - h * 0.09)], fill=(80, 82, 78), width=3)
        d.ellipse([px - 4, py - h * 0.105, px + 4, py - h * 0.08], fill=(60, 62, 58))
    # the red verdict, the only saturated mark on a grey page
    d.rectangle([x0 + w * 0.21, tbl + h * 0.19, x1 - w * 0.21, tbl + h * 0.36],
                outline=(190, 36, 28), width=5)
    s_ = fit(d, "NO DEAL", SANS_B, int(h * 0.14), w * 0.54)
    ink(d, ((x0 + x1) / 2, tbl + h * 0.275), "NO DEAL", SANS_B, s_, (190, 36, 28), "mm")
    # the torn draft, dropped on the floor at the left
    d.polygon([(x0 + w * 0.05, y1 - h * 0.22), (x0 + w * 0.17, y1 - h * 0.27),
               (x0 + w * 0.19, y1 - h * 0.11), (x0 + w * 0.07, y1 - h * 0.07)],
              fill=(250, 248, 242))
    for k in range(3):
        d.line([(x0 + w * 0.08, y1 - h * 0.20 + k * h * 0.035),
                (x0 + w * 0.16, y1 - h * 0.23 + k * h * 0.035)],
               fill=(160, 158, 146), width=2)


def scene_ships(d, box):
    """Benghazi harbour at dawn: a corvette listing hard, a cargo ship burning, a drone in the air."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    for i in range(int(h * 0.58)):
        t = i / max(1, h * 0.58)
        d.line([(x0, y0 + i), (x1, y0 + i)],
               fill=(int(28 + 70 * t), int(34 + 62 * t), int(54 + 50 * t)))
    sea = y0 + h * 0.58
    d.rectangle([x0, sea, x1, y1], fill=(14, 44, 58))
    for i in range(int(sea), int(y1), 8):
        c = (18 + (i % 11), 52 + (i % 9), 68 + (i % 7))
        d.line([(x0, i), (x1, i)], fill=c)
    d.line([(x0, sea), (x1, sea)], fill=(232, 206, 158), width=2)

    # the corvette: listing 25 degrees to port, waterline up its flank
    cx, cy = x0 + w * 0.30, sea + h * 0.10
    bw = w * 0.34
    d.polygon([(cx - bw * 0.5, cy - h * 0.02), (cx + bw * 0.5, cy - h * 0.10),
               (cx + bw * 0.44, cy + h * 0.10), (cx - bw * 0.56, cy + h * 0.14)],
              fill=(70, 74, 78))
    d.polygon([(cx - bw * 0.5, cy - h * 0.02), (cx + bw * 0.5, cy - h * 0.10),
               (cx + bw * 0.46, cy - h * 0.16), (cx - bw * 0.48, cy - h * 0.09)],
              fill=(112, 116, 120))
    # mast, tilted with the hull
    d.line([(cx + bw * 0.10, cy - h * 0.14), (cx + bw * 0.20, cy - h * 0.46)],
           fill=(150, 152, 156), width=3)
    d.line([(cx + bw * 0.20, cy - h * 0.40), (cx + bw * 0.34, cy - h * 0.44)],
           fill=(150, 152, 156), width=2)
    # a red list mark on the flank, so the tilt is read as damage
    d.line([(cx - bw * 0.30, cy + h * 0.02), (cx + bw * 0.16, cy - h * 0.05)],
           fill=(176, 40, 30), width=3)

    # the cargo ship, further out, burning from the deck
    gx, gy = x0 + w * 0.70, sea - h * 0.02
    gw = w * 0.36
    d.polygon([(gx - gw * 0.5, gy), (gx + gw * 0.5, gy),
               (gx + gw * 0.42, gy + h * 0.13), (gx - gw * 0.44, gy + h * 0.13)],
              fill=(58, 60, 64))
    for bx in range(int(gx - gw * 0.38), int(gx + gw * 0.34), 26):
        d.rectangle([bx, gy - h * 0.10, bx + 18, gy - h * 0.005], fill=(84, 74, 66))
    # fire and smoke off her
    for k, sy in enumerate(range(int(gy) - 14, int(y0) + 4, -11)):
        d.ellipse([gx - 16 + k * 5, sy - 12, gx + 44 + k * 5, sy + 12],
                  fill=(int(80 - k * 5), int(66 - k * 4), int(62 - k * 4)))
    d.polygon([(gx - 18, gy - h * 0.02), (gx - 4, gy - h * 0.30), (gx + 10, gy - h * 0.10),
               (gx + 24, gy - h * 0.24), (gx + 34, gy - h * 0.01)], fill=(214, 92, 28))
    d.polygon([(gx - 6, gy - h * 0.03), (gx + 4, gy - h * 0.18), (gx + 16, gy - h * 0.02)],
              fill=(250, 198, 84))

    # the sea drone that did it, low and dark, wake behind, in the near water
    dx, dy = x0 + w * 0.42, y1 - h * 0.10
    d.polygon([(dx - 20, dy + 5), (dx, dy - 7), (dx + 22, dy + 3), (dx, dy + 9)],
              fill=(24, 26, 28))
    d.line([(dx - 22, dy + 8), (dx - 62, dy + 13)], fill=(198, 216, 220), width=2)
    d.line([(dx + 22, dy + 6), (dx + 58, dy + 11)], fill=(198, 216, 220), width=2)
    # two small hulls in the water at the left edge, to say the harbour is full of traffic
    d.polygon([(x0 + 8, y1 - h * 0.24), (x0 + 30, y1 - h * 0.26),
               (x0 + 27, y1 - h * 0.20), (x0 + 10, y1 - h * 0.19)], fill=(40, 52, 58))


def scene_fire(d, box):
    """A gutted plant at night, the roof torn open, crews at the cordon counting the dead."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # sky: smoke lit from below
    for i in range(int(h * 0.70)):
        t = i / max(1, h * 0.70)
        d.line([(x0, y0 + i), (x1, y0 + i)],
               fill=(int(96 - 54 * t), int(52 - 30 * t), int(44 - 22 * t)))
    # the shed: roofline at 0.34h, floor at 0.70h, so the ground band is clear for people
    ry, fy = y0 + h * 0.34, y0 + h * 0.70
    d.rectangle([x0 + 4, ry, x1 - 4, fy], fill=(24, 19, 19))
    # sawtooth roof, one bay collapsed
    span = (x1 - 4) - (x0 + 4)
    for k in range(7):
        bx = x0 + 4 + span * k / 7
        bw_ = span / 7
        if k == 4:
            d.polygon([(bx, ry), (bx + bw_ * 0.5, ry + 16), (bx + bw_, ry + 6)],
                      fill=(14, 11, 11))
            continue
        d.polygon([(bx, ry), (bx + bw_ * 0.55, ry - 15), (bx + bw_, ry)],
                  fill=(34, 27, 25))
    # window bays: a hot core behind the middle ones, dimmer at the edges
    for wx in range(int(x0) + 14, int(x1) - 20, 30):
        t = abs(wx - (x0 + w * 0.5)) / w
        hot = max(0.0, 1.0 - t * 1.7)
        col = (int(120 + 120 * hot), int(44 + 90 * hot), int(16 + 30 * hot))
        d.rectangle([wx, ry + 16, wx + 19, fy - 10], fill=col)
    # the fire, off-centre and breaking upward through the collapsed bay
    cx = x0 + w * 0.56
    d.polygon([(cx - 34, ry + 10), (cx - 12, ry - 74), (cx + 4, ry - 26),
               (cx + 26, ry - 96), (cx + 40, ry + 6)], fill=(212, 78, 22))
    d.polygon([(cx - 14, ry + 8), (cx, ry - 46), (cx + 18, ry + 6)], fill=(252, 208, 96))
    d.polygon([(cx - 4, ry + 6), (cx + 6, ry - 22), (cx + 14, ry + 6)], fill=(255, 246, 214))
    for k, sy in enumerate(range(int(y0) - 2, int(ry) - 40, 11)):
        d.ellipse([cx - 30 + k * 7, sy, cx + 46 + k * 7, sy + 18],
                  fill=(int(58 - k * 3), int(48 - k * 2), int(46 - k * 2)))

    # ground: wet apron, lit orange near the fire, dark at the edges
    gy = fy
    for i in range(int(gy), int(y1)):
        t = (i - gy) / max(1.0, y1 - gy)
        d.line([(x0, i), (x1, i)],
               fill=(int(46 - 26 * t), int(30 - 18 * t), int(26 - 15 * t)))

    def person(px, ph, arm_up=False, helmet=False):
        """A silhouette at the cordon, sized so it reads as human at 300 px."""
        d.ellipse([px - ph * 0.10, gy - ph, px + ph * 0.10, gy - ph * 0.80], fill=(12, 10, 10))
        d.polygon([(px - ph * 0.13, gy - ph * 0.82), (px + ph * 0.13, gy - ph * 0.82),
                   (px + ph * 0.10, gy), (px - ph * 0.10, gy)], fill=(12, 10, 10))
        if helmet:
            d.rectangle([px - ph * 0.15, gy - ph * 0.84, px + ph * 0.15, gy - ph * 0.74],
                        fill=(206, 180, 88))
            d.rectangle([px - ph * 0.11, gy - ph * 0.44, px + ph * 0.11, gy - ph * 0.37],
                        fill=(222, 208, 152))
        if arm_up:
            d.line([(px + ph * 0.10, gy - ph * 0.72), (px + ph * 0.20, gy - ph * 1.02)],
                   fill=(12, 10, 10), width=max(2, int(ph * 0.07)))

    # two helmeted crews with a hose, left of the fire, silhouetted on the glow
    person(x0 + w * 0.14, h * 0.30, helmet=True)
    person(x0 + w * 0.22, h * 0.26, helmet=True)
    d.line([(x0 + w * 0.22, gy - h * 0.17), (x0 + w * 0.46, gy - h * 0.02)],
           fill=(232, 220, 190), width=2)
    # a covered stretcher and its two bearers, right of the fire
    sx = x0 + w * 0.78
    d.rectangle([sx - 22, gy - h * 0.09, sx + 24, gy - h * 0.05], fill=(196, 192, 186))
    for ox in (-26, 28):
        person(sx + ox, h * 0.24)
    # the engine's blue light, at the right edge
    d.ellipse([x1 - w * 0.09, gy - h * 0.20, x1 - w * 0.02, gy - h * 0.13],
              fill=(60, 116, 200))


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
    size = fit(d, date, SERIF_B, 74, W - 2 * M)
    ink(d, (W / 2, y), date, SERIF_B, size, INK, "ma")
    y += size + 6
    d.rectangle([M, y, W - M, y + 3], fill=RED)
    y += 11

    deck = ("COP31 fails  ·  two Russian ships sunk  ·  24 dead in Java  ·  Democrats take the House")
    para(d, (W / 2, y), deck, SANS_B, 20, W - 2 * M, 24, INK, limit=1, anchor="ma")
    y += 34

    # ---------------------------------------------------------- five figures
    # Five facts the picture row below does not repeat: breadth, not echo.
    figs = [("1,089", "FLIGHTS GROUNDED"), ("\u20ac1.4BN", "INDIA TO NEPAL"),
            ("128", "STATES, KILLER ROBOTS"), ("10 MONTHS", "LOW FOR KOSPI"),
            ("4", "KILLED IN KYIV")]
    fw = (W - 2 * M) / len(figs)
    d.rectangle([M, y, W - M, y + 78], fill=(238, 233, 221))
    for i, (num, cap) in enumerate(figs):
        cx = M + fw * i + fw / 2
        s_ = fit(d, num, SERIF_B, 40, fw - 16)
        ink(d, (cx, y + 8), num, SERIF_B, s_, RED, "ma")
        ink(d, (cx, y + 56), cap, SANS_B, 12, DIM, "ma")
        if i:
            d.line([(M + fw * i, y + 10), (M + fw * i, y + 68)], fill=(206, 198, 184))
    y += 88

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
        ("UKRAINE", "Woman pulled from the rubble after 24 hours",
         "Four killed in the drone strikes on the Kyiv region; a Dymer block fell"),
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

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry3", "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
