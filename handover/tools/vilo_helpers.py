"""Helpers for drawing Vilo Play illustrations as outlined SVG.

This is the code from the vilo-illustration skill (SKILL.md, section 6) in one importable file.
Usage in a drawing script:

    from vilo_helpers import *
    use_game("Secret Santa")
    body = with_depth("M200,300 L900,300 L900,800 L200,800 Z", "main")
    export("my_drawing", body)

Needs: pip install numpy cairosvg  (on a Mac, cairosvg also needs the cairo library: brew install cairo)
Writes my_drawing.svg, my_drawing.png and my_drawing_transparent.png in the current folder.
"""
import math
import numpy as np

W, H = 1600, 1100
INK, CLAW, BLUE_L, BLUE, YEL = "#1A000A", "#FDFFF3", "#C5D0FF", "#8D98EC", "#EBFF00"
SW, SW_DETAIL = 4.5, 3.6

# game colours: fill, strong, soft (working set, not yet confirmed by Vilo)
GAMES = {
    "Secret Santa":           ("#FF8A73", "#E5533A", "#FFC4B8"),
    "Secret Office Missions": ("#FFA3D7", "#E0509B", "#FFD9EE"),
    "Who's Who":              ("#F6CF6B", "#C9971A", "#FBEAB8"),
    "Step Challenge":         ("#A6F5B8", "#3FBF6A", "#D6FBDD"),
    "Shoutouts":              ("#EBFF00", "#B8C900", "#F7FFA8"),
    "Recognition":            ("#8D98EC", "#5560D0", "#C5D0FF"),
    "Coffee Roulette":        ("#FFB15C", "#E67E1E", "#FFD9AE"),
    "Truth or Bluff":         ("#B79BFF", "#7B55E8", "#DCCDFF"),
}

FILL, STRONG, SOFT = GAMES["Secret Santa"]
GRADS = {"main": (SOFT, FILL)}          # id -> (start colour, end colour); add more if needed


def use_game(name):
    """Set the three game colours (and the main gradient) for one game. Call this first."""
    global FILL, STRONG, SOFT
    if name not in GAMES:
        raise KeyError(f"Unknown game {name!r}. Choose one of: {', '.join(GAMES)}")
    FILL, STRONG, SOFT = GAMES[name]
    GRADS["main"] = (SOFT, FILL)


def stroke(sw=SW):
    return f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"'


def fill(c):
    return f"url(#{c})" if c in GRADS else c


def path(d, c, sw=SW, extra=""):
    return f'<path d="{d}" fill="{fill(c)}" {stroke(sw)} {extra}/>'


def line(d, sw=SW_DETAIL):
    return f'<path d="{d}" fill="none" {stroke(sw)}/>'


def with_depth(d, front, depth=None, dx=12, dy=12):
    """Main shape with its depth copy behind it (strong colour by default)."""
    return f'<g transform="translate({dx} {dy})">{path(d, depth or STRONG)}</g>' + path(d, front)


def text_bar(x, y, length, colour=BLUE_L, h=38):
    return f'<rect x="{x}" y="{y}" width="{length}" height="{h}" rx="{h/2}" fill="{colour}"/>'


def svg(body, background=True):
    defs = "".join(
        f'<linearGradient id="{k}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
        for k, (a, b) in GRADS.items())
    bg = f'<rect width="{W}" height="{H}" fill="{CLAW}"/>' if background else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs>{defs}</defs>{bg}{body}</svg>')


def export(name, body):
    s = svg(body)
    open(f"{name}.svg", "w").write(s)
    try:
        import cairosvg
    except Exception as e:  # missing package or missing cairo library
        print(f"Wrote {name}.svg. PNG not made: {e}\n"
              "Install with: pip install cairosvg  (Mac: brew install cairo first)")
        return
    cairosvg.svg2png(bytestring=s.encode(), write_to=f"{name}.png")
    cairosvg.svg2png(bytestring=svg(body, False).encode(), write_to=f"{name}_transparent.png")
    print(f"Wrote {name}.svg, {name}.png and {name}_transparent.png")


# ---------------------------------------------------------------- 3D box engine (gifts, boxes, stacks)
# Each box has a centre, a size and a rotation in world units (y is up, the ground is y = 0,
# z points toward the viewer). One perspective camera projects every box, only faces that point at
# the camera are drawn, and ribbons and stripes are mapped onto the faces. Draw boxes back to front.
CAM = np.array([0.0, 950.0, 2500.0]); LOOK_Y = 200.0; FOC = 2450.0
OX, OY = 800, 690                      # screen position of the camera axis; move to place the scene
PITCH = math.atan2(CAM[1] - LOOK_Y, CAM[2])


def proj(p):
    v = np.array(p, float) - CAM
    c, s = math.cos(PITCH), math.sin(PITCH)
    yc = v[1]*c - v[2]*s
    d = -v[1]*s - v[2]*c
    return (OX + FOC*v[0]/d, OY - FOC*yc/d)


def rot(yaw=0, roll=0):
    a, b = math.radians(yaw), math.radians(roll)
    Ry = np.array([[math.cos(a), 0, math.sin(a)], [0, 1, 0], [-math.sin(a), 0, math.cos(a)]])
    Rz = np.array([[math.cos(b), -math.sin(b), 0], [math.sin(b), math.cos(b), 0], [0, 0, 1]])
    return Ry @ Rz


# face -> (normal axis, sign, u axis, v axis)
FACES = {"front": (2, 1, 0, 1), "back": (2, -1, 0, 1), "right": (0, 1, 2, 1),
         "left": (0, -1, 2, 1), "top": (1, 1, 0, 2), "bottom": (1, -1, 0, 2)}


def pts(ps):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in ps)


class Box:
    def __init__(self, centre, size, yaw=0, roll=0, faces=None, ribbons=(), stripes=None):
        self.c = np.array(centre, float); self.h = np.array(size, float) / 2; self.R = rot(yaw, roll)
        self.faces = faces or {"default": STRONG, "front": "main", "top": SOFT}
        self.ribbons = ribbons          # list of (axis 0=x or 2=z, half width, colour)
        self.stripes = stripes          # (colour, axis, count) or None

    def local(self, f, u, v):
        n, sg, ua, va = FACES[f]; l = [0, 0, 0]
        l[n] = sg*self.h[n]; l[ua] = u*self.h[ua]; l[va] = v*self.h[va]; return l

    def P(self, l):
        return proj(self.R @ np.array(l, float) + self.c)

    def quad(self, f, u0=-1, u1=1, v0=-1, v1=1):
        return [self.P(self.local(f, u, v)) for u, v in ((u0, v0), (u1, v0), (u1, v1), (u0, v1))]

    def visible(self, f):
        n, sg, _, _ = FACES[f]; nv = np.zeros(3); nv[n] = sg
        centre = self.R @ np.array(self.local(f, 0, 0)) + self.c
        return (self.R @ nv) @ (CAM - centre) > 1e-3

    def top_centre(self):
        return self.P([0, self.h[1], 0])


def draw_box(b):
    out = ""
    for f in FACES:
        if not b.visible(f):
            continue
        n, _, ua, va = FACES[f]
        q = b.quad(f)
        out += f'<polygon points="{pts(q)}" fill="{fill(b.faces.get(f, b.faces["default"]))}" {stroke()}/>'
        if b.stripes and b.stripes[1] != n:
            col, axis, count = b.stripes
            for i in range(count):
                a = -1 + 2*(i + 0.25)/count; e = a + 0.9/count
                qq = b.quad(f, a, e, -1, 1) if ua == axis else b.quad(f, -1, 1, a, e)
                out += f'<polygon points="{pts(qq)}" fill="{col}" stroke="none"/>'
            out += f'<polygon points="{pts(q)}" fill="none" {stroke()}/>'
        for axis, w, col in b.ribbons:
            if axis == n:
                continue
            r = w / b.h[axis]
            qq = b.quad(f, -r, r, -1, 1) if ua == axis else b.quad(f, -1, 1, -r, r)
            out += f'<polygon points="{pts(qq)}" fill="{col}" {stroke(SW*0.8)}/>'
    return out


def bow(c, colour, k=1.0):
    x, y = c
    loop = lambda s: (f"M{x},{y} C{x+s*25*k},{y-55*k} {x+s*80*k},{y-30*k} {x+s*62*k},{y+4*k} "
                      f"C{x+s*50*k},{y+22*k} {x+s*20*k},{y+10*k} {x},{y} Z")
    tail = lambda s: f"M{x},{y} l{s*30*k},{55*k} l{-s*12*k},{-4*k} l{-s*8*k},{10*k} Z"
    return (path(tail(-1), colour) + path(tail(1), colour) + path(loop(-1), colour) + path(loop(1), colour)
            + f'<ellipse cx="{x}" cy="{y}" rx="{13*k}" ry="{11*k}" fill="{colour}" {stroke()}/>')
