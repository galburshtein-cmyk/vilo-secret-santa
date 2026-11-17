import sys, math, cairosvg
import numpy as np
import secret_santa_gifts as S3

INK="#1A000A"; BG="#FDFFF3"; YEL="#EBFF00"; BL="#C5D0FF"; BLUE="#8D98EC"
CF="#FF8A73"; CS="#E5533A"; CSO="#FFC4B8"
SW = 4.5
W, H = 1600, 1100

# retarget the box engine to the Vilo palette
S3.INK=INK; S3.OFF=BG; S3.CREAM=BG; S3.BLUE=BLUE; S3.VIOLET=BLUE; S3.PINK=BL; S3.YEL=YEL
S3.GRADS.clear()
S3.GRADS.update({"coral": [(0, CSO), (0.5, CF), (1, CS)], "blue": [(0, BL), (1, BLUE)],
                 "tree": [(0, BL), (1, BLUE)]})
S3.GRAINSVG = False
S3.CAM = np.array([0.0, 950.0, 2500.0]); S3.LOOK = np.array([0.0, 200.0, 0.0]); S3.FOC = 2450.0
S3._pitch = math.atan2(750, 2500)
S3.OX, S3.OY = 800, 690

def st(sw=SW): return f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"'

TIERS = [(150, 330, 140), (240, 480, 220), (360, 640, 300), (500, 820, 390)]  # top y, bottom y, half width
CX = 800

def tier_path(top, bot, hw, n):
    d = f"M{CX},{top} C{CX+hw*0.35},{top+(bot-top)*0.35} {CX+hw*0.8},{bot-(bot-top)*0.2} {CX+hw},{bot} "
    step = 2*hw/n
    for i in range(n):
        x0 = CX + hw - i*step; x1 = x0 - step
        d += f"Q{(x0+x1)/2},{bot+26} {x1},{bot} "
    d += f"C{CX-hw*0.8},{bot-(bot-top)*0.2} {CX-hw*0.35},{top+(bot-top)*0.35} {CX},{top} Z"
    return d

def tree():
    o = ""
    o += f'<rect x="{CX-45}" y="800" width="90" height="90" fill="{CS}" {st()}/>'
    for (top, bot, hw) in reversed(TIERS):
        n = max(4, int(hw/55))
        d = tier_path(top, bot, hw, n)
        o += f'<path d="{d}" transform="translate(12 12)" fill="{BLUE}" {st()}/>'
        o += f'<path d="{d}" fill="url(#tree)" {st()}/>'
        # garland across the tier
        y0 = bot - (bot-top)*0.18
        g = f"M{CX-hw*0.82},{y0-30} Q{CX},{y0+40} {CX+hw*0.82},{y0-70}"
        o += f'<path d="{g}" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round"/>'
        o += f'<path d="{g}" fill="none" stroke="{YEL}" stroke-width="13" stroke-linecap="round"/>'
    # baubles
    balls = [(760, 290, CF), (850, 275, CS), (700, 430, CS), (880, 445, CF), (790, 470, CF),
             (640, 590, CF), (760, 610, CS), (930, 580, CS), (580, 760, CS), (700, 770, CF),
             (880, 760, CF), (1010, 740, CS)]
    for (x, y, c) in balls:
        o += f'<rect x="{x-7}" y="{y-26}" width="14" height="10" rx="2" fill="{YEL}" {st(SW*0.7)}/>'
        o += f'<circle cx="{x}" cy="{y}" r="18" fill="{c}" {st()}/>'
        o += f'<path d="M{x-8},{y-6} q4,-6 10,-7" fill="none" stroke="{BG}" stroke-width="4" stroke-linecap="round"/>'
    # star
    sx, sy, R = CX, 140, 52
    pts = []
    for i in range(10):
        a = -math.pi/2 + i*math.pi/5; r = R if i % 2 == 0 else R*0.45
        pts.append(f"{sx + r*math.cos(a):.1f},{sy + r*math.sin(a):.1f}")
    o += f'<polygon points="{" ".join(pts)}" transform="translate(8 8)" fill="{CS}" {st()}/>'
    o += f'<polygon points="{" ".join(pts)}" fill="{YEL}" {st()}/>'
    return o

def coral(rib=BG): return dict(faces={"default": CS, "front": "coral", "top": CSO}, ribbons=[(0, 14, rib), (2, 14, rib)])
def white(rib=CS): return dict(faces={"default": BL, "front": BG, "top": BG, "right": BG, "left": BL}, ribbons=[(0, 13, rib), (2, 13, rib)])
def blue(rib=YEL): return dict(faces={"default": BLUE, "front": "blue", "top": BL}, ribbons=[(0, 13, rib), (2, 13, rib)])

BACK = [
    ((-420, 65, -260), (170, 130, 150), 10, white(CS), CS),
    ((430, 75, -250), (160, 150, 150), -12, coral(), BG),
    ((330, 50, -330), (120, 100, 110), 20, blue(), YEL),
]
FRONT = [
    ((-560, 95, -20), (210, 190, 170), 12, coral(), BG),
    ((-560, 240, -20), (120, 100, 110), -10, blue(), YEL),
    ((-360, 62, 150), (180, 124, 150), -8, white(CS), CS),
    ((560, 80, 30), (190, 160, 160), -14, white(BLUE), BLUE),
    ((-150, 72, 170), (210, 144, 170), 6, coral(), BG),
    ((270, 85, 150), (220, 170, 170), -6, coral(YEL), YEL),
    ((70, 55, 270), (150, 110, 130), 14, white(CS), CS),
    ((620, 60, 230), (140, 120, 120), 10, coral(), BG),
    ((-120, 40, 380), (90, 80, 80), -12, blue(), YEL),
]

def gifts(lst):
    s = S3.S("color"); out = []
    for (c, dims, yaw, skin, bowc) in lst:
        b = S3.Box(c, dims, yaw=yaw, skin=skin)
        S3.draw_box(s, b)
        S3.bow(s, S3.top_center(b), bowc, 0.42 + dims[0]/900)
    return "\n".join(s.o if hasattr(s, "o") else s.out)

def svg(bg=True):
    defs = ""
    for k, stops in S3.GRADS.items():
        stp = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
        defs += f'<linearGradient id="{k}" x1="0" y1="0" x2="1" y2="1">{stp}</linearGradient>'
    bgr = f'<rect width="{W}" height="{H}" fill="{BG}"/>' if bg else ""
    body = f'<g transform="translate(0 -15)">{gifts(BACK)}{tree()}{gifts(FRONT)}</g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{defs}</defs>{bgr}{body}</svg>'

if __name__ == "__main__":
    out = sys.argv[1]
    open(out + ".svg", "w").write(svg())
    cairosvg.svg2png(bytestring=svg().encode(), write_to=out + ".png")
    cairosvg.svg2png(bytestring=svg(False).encode(), write_to=out + "_transparent.png")
