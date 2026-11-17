import numpy as np, cairosvg, io, sys
from PIL import Image

W, H = 1600, 1100
INK="#1A000A"; BG="#FDFFF3"; YEL="#EBFF00"; BL="#C5D0FF"; BLUE="#8D98EC"
F="#A6F5B8"; ST="#3FBF6A"; SO="#D6FBDD"     # Step Challenge
SW = 4.5
GRAINSVG = False
GRADS = {
    "heel":  ('x1="1" y1="0" x2="0" y2="1"', [(0, SO), (0.45, F), (1, ST)]),
    "knit":  ('x1="0" y1="0" x2="1" y2="1"', [(0, BG), (1, SO)]),
}

# --- geometry (side view, toe left) ---
SOLE = ("M300,700 C262,716 256,806 345,834 L1255,834 C1335,834 1378,792 1372,712 "
        "L1356,566 C1250,570 1130,590 1040,612 C900,646 790,690 690,700 L300,700 Z")
OUTSOLE = ("M268,782 C280,814 304,832 345,834 L1255,834 C1320,834 1360,806 1370,770 "
           "C1300,790 1240,796 1180,796 L420,796 C340,796 300,792 268,782 Z")
INLAY = ("M520,742 C700,730 900,690 1060,650 C1160,626 1230,632 1262,664 "
         "C1180,654 1100,668 1010,694 C860,738 700,760 560,762 C530,762 515,752 520,742 Z")
UPPER = ("M300,700 C246,662 262,566 380,528 C480,497 600,452 700,392 L792,334 "
         "L778,278 C784,252 826,244 846,262 L902,322 "
         "C990,362 1110,344 1200,272 C1250,236 1312,250 1334,292 "
         "C1364,362 1370,470 1356,566 C1250,570 1130,590 1040,612 C900,646 790,690 690,700 Z")
UPPER_NT = ("M300,700 C246,662 262,566 380,528 C480,497 600,452 700,392 L792,334 L902,322 "
            "C990,362 1110,344 1200,272 C1250,236 1312,250 1334,292 "
            "C1364,362 1370,470 1356,566 C1250,570 1130,590 1040,612 C900,646 790,690 690,700 Z")
HEELPANEL = ("M1030,346 C1110,338 1170,306 1200,272 C1250,236 1312,250 1334,292 "
             "C1364,362 1370,470 1356,566 C1250,570 1130,590 1040,612 C1010,560 990,470 1030,346 Z")
EYESTAY = ("M430,512 C540,480 650,430 760,354 L800,330 L828,372 C760,418 650,488 470,560 C440,548 428,530 430,512 Z")
TONGUE = "M778,278 C784,252 826,244 846,262 L902,322 L828,372 L792,334 Z"

def pathel(s, d, fill, sw=SW, extra=""):
    flt = ' filter="url(#grain)"' if (GRAINSVG and s["mode"]=="color" and fill in GRADS) else ""
    return f'<path d="{d}" fill="{col(s,fill)}" stroke="{ink(s)}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"{flt}{extra}/>'

def col(s, c):
    if c == "none": return "none"
    if s["mode"] == "color": return f"url(#{c})" if c in GRADS else c
    return "#fff" if c in GRADS else "#000"
def ink(s): return INK if s["mode"]=="color" else "#000"

def lace(s, p0, p1, c1):
    d = f"M{p0[0]},{p0[1]} Q{c1[0]},{c1[1]} {p1[0]},{p1[1]}"
    return (f'<path d="{d}" fill="none" stroke="{ink(s)}" stroke-width="22" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{col(s,BG)}" stroke-width="12" stroke-linecap="round"/>')

DX, DY = -26, -30
def sweep(s, d, fill, steps=14):
    o = []
    for k in range(steps+1):
        t = k/steps
        o.append(f'<path d="{d}" transform="translate({DX*t:.1f} {DY*t:.1f})" fill="{ink(s)}" stroke="{ink(s)}" stroke-width="{SW*2}" stroke-linejoin="round"/>')
    for k in range(steps+1):
        t = k/steps
        o.append(f'<path d="{d}" transform="translate({DX*t:.1f} {DY*t:.1f})" fill="{col(s,fill)}" stroke="none"/>')
    return "".join(o)

def scene(mode):
    s = {"mode": mode}; o = []
    o.append(f'<g transform="translate(13 13)">{pathel(s, UPPER_NT, ST)}{pathel(s, SOLE, ST)}</g>')
    # far sole outline hint at toe + far upper outline
    # collar opening (inside of the shoe)
    near = "M902,322 C990,362 1110,344 1200,272 C1250,236 1312,250 1334,292"
    far_pts = "C{a},{b} {c},{d} {e},{f}"
    def sh(x, y): return f"{x+DX:.0f},{y+DY:.0f}"
    opening = (f"M902,322 C990,362 1110,344 1200,272 C1250,236 1312,250 1334,292 "
               f"L{sh(1334,292)} C{sh(1312,250)} {sh(1250,236)} {sh(1200,272)} C{sh(1110,344)} {sh(990,362)} {sh(902,322)} Z")
    o.append(pathel(s, opening, ST))
    o.append(pathel(s, TONGUE, BG))
    o.append(pathel(s, "M786,282 C790,262 822,256 836,270 L852,292 C832,284 808,288 794,302 Z", ST, sw=SW*0.8))
    o.append(scene_side(mode, laces=False))
    eyes = [(486, 524), (560, 494), (634, 458), (706, 414), (774, 368)]
    for i in range(len(eyes)-1):
        a_, b_ = eyes[i], eyes[i+1]
        o.append(lace(s, (a_[0]-4, a_[1]+4), (b_[0]-14, b_[1]-26), ((a_[0]+b_[0])/2-18, (a_[1]+b_[1])/2-26)))
    bx, by = 778, 344
    o.append(lace(s, (bx, by), (bx-70, by-50), (bx-80, by+6)))
    o.append(lace(s, (bx-70, by-50), (bx, by), (bx-20, by-70)))
    o.append(lace(s, (bx, by), (bx+70, by-30), (bx+60, by+20)))
    o.append(lace(s, (bx+70, by-30), (bx, by), (bx+30, by-60)))
    o.append(lace(s, (bx, by), (bx-34, by+110), (bx-30, by+50)))
    o.append(lace(s, (bx, by), (bx+22, by+120), (bx+20, by+60)))
    o.append(f'<ellipse cx="{bx}" cy="{by}" rx="13" ry="11" fill="{col(s,BG)}" stroke="{ink(s)}" stroke-width="{SW}"/>')
    for (x, y, r) in [(bx-34, by+110, 14), (bx+22, by+120, -8)]:
        o.append(f'<rect x="{x-8}" y="{y-4}" width="16" height="26" rx="6" fill="{col(s,YEL)}" stroke="{ink(s)}" stroke-width="{SW*0.7}" transform="rotate({r} {x} {y})"/>')
    return "\n".join(o)

def scene_side(mode, laces=True):
    s = {"mode": mode}; o = []
    # extrusion (darker copy behind)
    # upper
    o.append(pathel(s, UPPER_NT, "knit"))
    # wing streaks on the side (tapered)
    for i, (x, y) in enumerate([(930, 420), (950, 470), (960, 522), (955, 572)]):
        L = 300 - i*30
        o.append(pathel(s, f"M{x},{y} C{x-L*0.45},{y+20} {x-L*0.8},{y+60} {x-L},{y+100} "
                           f"C{x-L*0.78},{y+76} {x-L*0.42},{y+40} {x},{y+22} Z", F, sw=SW*0.8))
    # heel panel + double stripes
    o.append(pathel(s, HEELPANEL, "heel"))
    for off in (0, 34):
        o.append(pathel(s, f"M{1236+off*0.4},{262+off*0.2} C{1252+off},{360} {1240+off},{470} {1206+off},{582-off*0.2} "
                           f"L{1226+off},{578-off*0.2} C{1262+off},{466} {1272+off},{356} {1258+off*0.4},{256+off*0.2} Z", BG, sw=SW*0.8))
    # heel pull tab
    o.append(pathel(s, "M1262,252 C1270,214 1298,196 1322,206 C1338,214 1340,240 1334,292 C1316,262 1290,250 1262,252 Z", ST))
    # collar stitch line
    o.append(f'<path d="M910,348 C1000,386 1120,366 1206,300" fill="none" stroke="{ink(s)}" stroke-width="{SW*0.7}" stroke-dasharray="2 14" stroke-linecap="round"/>')
    # eyestay
    o.append(pathel(s, EYESTAY, BG))
    # eyelets
    eyes = [(486, 524), (560, 494), (634, 458), (706, 414), (774, 368)]
    for (x, y) in eyes:
        o.append(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="7" fill="{col(s,ST)}" stroke="{ink(s)}" stroke-width="{SW*0.7}"/>')
    # sole
    o.append(pathel(s, SOLE, BG))
    o.append(pathel(s, INLAY, F, sw=SW*0.8))
    o.append(pathel(s, OUTSOLE, ST))
    # air windows
    for (x, w) in [(1150, 96), (1268, 70)]:
        o.append(f'<rect x="{x}" y="690" width="{w}" height="58" rx="29" fill="{col(s,BL)}" stroke="{ink(s)}" stroke-width="{SW}"/>')
        o.append(f'<path d="M{x+18},708 L{x+w-26},708" stroke="{col(s,BG)}" stroke-width="7" stroke-linecap="round"/>')
    return "\n".join(o)

import math
SHOES = [  # (tx, ty, scale, angle)  angle>0 = toe up (swing), <0 = heel up (push-off)
    (100, 70, 0.64, 14),
    (500, 340, 0.64, -20),
]
def xf(p, t):
    tx, ty, sc, a = t; cx, cy = 810, 520
    r = math.radians(a); x, y = p[0]-cx, p[1]-cy
    x, y = x*math.cos(r) - y*math.sin(r) + cx, x*math.sin(r) + y*math.cos(r) + cy
    return (tx + sc*x, ty + sc*y)
def shoes(mode):
    s = {"mode": mode}; out = ""
    for t in SHOES:
        tx, ty, sc, a = t
        out += f'<g transform="translate({tx} {ty}) scale({sc}) rotate({a} 810 520)">{scene(mode)}</g>'
    return out

def svg(mode, bg=True):
    defs = ""
    if mode == "color":
        for k, (coords, stops) in GRADS.items():
            st = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
            defs += f'<linearGradient id="{k}" {coords}>{st}</linearGradient>'
        if GRAINSVG:
            defs += ('<filter id="grain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
                     '<feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="7" result="n"/>'
                     '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.5 0.62" result="dark"/>'
                     '<feComposite in="dark" in2="SourceAlpha" operator="in" result="d2"/>'
                     '<feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1.5 -0.86" result="light"/>'
                     '<feComposite in="light" in2="SourceAlpha" operator="in" result="l2"/>'
                     '<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="d2"/><feMergeNode in="l2"/></feMerge></filter>')
    bgc = BG if mode=="color" else "#000"
    bgrect = f'<rect width="{W}" height="{H}" fill="{bgc}"/>' if (bg or mode!="color") else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs>{defs}</defs>{bgrect}'
            f'{shoes(mode)}</svg>')

def render(s):
    return np.array(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode()))).convert("RGBA")).astype(np.float32)

if __name__ == "__main__":
    out = sys.argv[1]
    open(out + ".svg","w").write(svg("color"))
    cairosvg.svg2png(bytestring=svg("color").encode(), write_to=out + ".png")
    cairosvg.svg2png(bytestring=svg("color", bg=False).encode(), write_to=out + "_transparent.png")
