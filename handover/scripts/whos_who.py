import numpy as np, cairosvg, io, sys, math
from PIL import Image

W, H = 1600, 1100
INK="#1A000A"; BG="#FDFFF3"; YEL="#EBFF00"; BL="#C5D0FF"; BLUE="#8D98EC"
F="#F6CF6B"; ST="#C9971A"; SO="#FBEAB8"     # Who's Who
SW = 4.5
GRAINSVG = False
GRADS = {
    "rim":    ('x1="0" y1="0" x2="1" y2="1"', [(0, SO), (0.5, F), (1, ST)]),
    "handle": ('x1="0" y1="0" x2="0" y2="1"', [(0, SO), (0.45, F), (1, ST)]),
}

CX, CY, RO, RI = 700, 450, 300, 255
ANG = 45
PAPER = dict(cx=800, cy=560, w=980, h=700, rot=-6)
MAG = 1.55

class S:
    def __init__(s, mode): s.mode=mode; s.o=[]
    def f(s, c):
        if s.mode=="color": return f"url(#{c})" if c in GRADS else c
        return "#fff" if c in GRADS else "#000"
    def ink(s): return INK if s.mode=="color" else "#000"
    def st(s, sw=SW): return f'stroke="{s.ink()}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"'
    def flt(s, c): return ' filter="url(#grain)"' if (GRAINSVG and s.mode=="color" and c in GRADS) else ""
    def add(s, x): s.o.append(x)

LH = 38
BAR_COLS = [BL, BLUE, BL]
def text_lines(s, outline=True):
    # five big bars, centered behind the lens
    xs = [(300, 800), (280, 860), (310, 780)]
    y0 = CY + 110 - 2*100
    return [(x, CY - 155 + i*130 - LH/2, L) for i, (x, L) in enumerate(xs)]

def paper_group(s, hl=False):
    p = PAPER; x0 = p["cx"]-p["w"]/2; y0 = p["cy"]-p["h"]/2
    g = f'<g transform="rotate({p["rot"]} {p["cx"]} {p["cy"]})">'
    lines = text_lines(s)
    for i, (x, y, L) in enumerate(lines):
        if False:
            g += f'<rect x="{x-10}" y="{y-8}" width="{L*0.62+20}" height="28" rx="6" fill="{s.f(YEL)}" stroke="none"/>'
        g += f'<rect x="{x}" y="{y}" width="{L}" height="{LH}" rx="{LH/2}" fill="{s.f(BAR_COLS[i % len(BAR_COLS)])}" stroke="none"/>'
    g += '</g>'
    return g

HL_LINE = 5

def scene(mode):
    s = S(mode)
    a = math.radians(ANG); ux, uy = math.cos(a), math.sin(a)
    # paper (behind)
    s.add(paper_group(s))
    # handle (behind lens rim), drawn in rotated frame along +x
    hx0, hx1 = RO + 70, RO + 430
    def handle(off, front):
        g = f'<g transform="translate({CX+off} {CY+off}) rotate({ANG})">'
        # ferrule
        fx0 = RO - 12
        if front:
            g += f'<rect x="{fx0}" y="-26" width="{hx0-fx0+10}" height="52" fill="{s.f(BL)}" {s.st()}/>'
            g += f'<line x1="{fx0+22}" y1="-26" x2="{fx0+22}" y2="26" {s.st(SW*0.8)}/>'
            g += f'<line x1="{fx0+40}" y1="-26" x2="{fx0+40}" y2="26" {s.st(SW*0.8)}/>'
            g += f'<rect x="{hx0}" y="-44" width="{hx1-hx0}" height="88" rx="40" fill="{s.f("handle")}" {s.st()}{s.flt("handle")}/>'
            g += f'<path d="M{hx0+40},-24 L{hx1-60},-24" {s.st(SW*0.8)} fill="none"/>'
            g += f'<path d="M{hx0+44},-14 L{hx1-70},-14" stroke="{s.f(BG) if mode=="color" else "#000"}" stroke-width="6" stroke-linecap="round" fill="none"/>'
        else:
            g += f'<rect x="{fx0}" y="-26" width="{hx0-fx0+10}" height="52" fill="{s.f(BLUE)}" {s.st()}/>'
            g += f'<rect x="{hx0}" y="-44" width="{hx1-hx0}" height="88" rx="40" fill="{s.f(ST)}" {s.st()}/>'
        g += '</g>'
        s.add(g)
    handle(12, False); handle(0, True)
    # rim back copy
    ring = (f'M{CX-RO},{CY} a{RO},{RO} 0 1,0 {2*RO},0 a{RO},{RO} 0 1,0 {-2*RO},0 Z '
            f'M{CX-RI},{CY} a{RI},{RI} 0 1,1 {2*RI},0 a{RI},{RI} 0 1,1 {-2*RI},0 Z')
    s.add(f'<path d="{ring}" transform="translate(13 13)" fill="{s.f(ST)}" fill-rule="evenodd" {s.st()}/>')
    # lens content: magnified paper
    s.add(f'<clipPath id="lens"><circle cx="{CX}" cy="{CY}" r="{RI}"/></clipPath>')
    s.add(f'<g clip-path="url(#lens)"><rect x="0" y="0" width="{W}" height="{H}" fill="{s.f(BG)}"/>'
          f'<g transform="translate({CX} {CY}) scale({MAG}) translate({-CX} {-CY})">{paper_group(s, hl=True)}</g>')
    # glass reflections
    if True:
        r1 = RI - 22
        s.add(f'<path d="M{CX - r1*math.cos(math.radians(200-180))},{CY} " fill="none" stroke="none"/>')
        # soft blue crescent lower-left
        s.add(f'<path d="M{CX-RI},{CY} A{RI},{RI} 0 0,0 {CX},{CY+RI} A{RI*1.25},{RI*1.25} 0 0,1 {CX-RI},{CY} Z" '
              f'transform="rotate(10 {CX} {CY})" fill="none" stroke="none"/>')
        # white glare arcs upper-right
        def arc(r, a0, a1, w):
            p0 = (CX + r*math.cos(math.radians(a0)), CY + r*math.sin(math.radians(a0)))
            p1 = (CX + r*math.cos(math.radians(a1)), CY + r*math.sin(math.radians(a1)))
            return (f'<path d="M{p0[0]:.1f},{p0[1]:.1f} A{r},{r} 0 0,1 {p1[0]:.1f},{p1[1]:.1f}" fill="none" '
                    f'stroke="{s.ink()}" stroke-width="{w}" stroke-linecap="round"/>')
        s.add(arc(RI-34, -88, -38, 5))
        s.add(arc(RI-34, -28, -20, 5))
    s.add('</g>')
    # front rim
    s.add(f'<path d="{ring}" fill="{s.f("rim")}" fill-rule="evenodd" {s.st()}{s.flt("rim")}/>')
    # small rim highlight
    r = (RO+RI)/2
    p0 = (CX + r*math.cos(math.radians(-150)), CY + r*math.sin(math.radians(-150)))
    p1 = (CX + r*math.cos(math.radians(-110)), CY + r*math.sin(math.radians(-110)))
    s.add(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} A{r},{r} 0 0,1 {p1[0]:.1f},{p1[1]:.1f}" fill="none" '
          f'stroke="{s.f(BG) if mode=="color" else "#000"}" stroke-width="7" stroke-linecap="round"/>')
    return "\n".join(s.o)

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
            f'<defs>{defs}</defs>{bgrect}<g transform="translate(-10 -15)">{scene(mode)}</g></svg>')

def render(s):
    return np.array(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode()))).convert("RGBA")).astype(np.float32)

if __name__ == "__main__":
    out = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "grainsvg":
        GRAINSVG = True; open(out + ".svg","w").write(svg("color")); sys.exit()
    rng = np.random.default_rng(7)
    col = render(svg("color")); m = render(svg("mask"))[...,0]/255.0
    noise = rng.normal(0,15,m.shape) + (rng.random(m.shape)<0.10)*rng.choice([-26,26],m.shape)
    rgb = col[...,:3] + (noise*m)[...,None] + rng.normal(0,5,m.shape)[...,None]
    dust = rng.random(m.shape) < 0.0004; rgb[dust] *= 0.55
    Image.fromarray(np.clip(rgb,0,255).astype(np.uint8)).save(out + ".png")
    colt = render(svg("color", bg=False))
    rgbt = colt[...,:3] + (noise*m)[...,None]
    Image.fromarray(np.concatenate([np.clip(rgbt,0,255), colt[...,3:4]],-1).astype(np.uint8)).save(out + "_transparent.png")
    open(out + ".svg","w").write(svg("color"))
