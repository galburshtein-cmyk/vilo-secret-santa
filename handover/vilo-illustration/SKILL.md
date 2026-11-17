---
name: vilo-illustration
description: Draw Vilo Play website illustrations (game heroes, card art) as clean outlined SVG in the Vilo illustration language, traced from a reference photo, in one game's colours.
---

# Vilo illustration language

Use this skill whenever someone asks for an illustration for the Vilo Play website: a hero drawing for a game page, the drawing on a game card, or a new game's object. The output is a clean outlined SVG drawn in code, plus a PNG and a transparent PNG.

The drawings should feel like a sticker you could pick up: one everyday object, thin dark outlines, flat colour, one smooth gradient, a little depth.

## 1. Before you draw

Settle three things. Ask only for what is missing.

1. **Which game.** It decides the colours. If the request names no game, ask which page the drawing is for. Never mix two games' colours in one drawing.
2. **The subject.** One everyday object people recognise at a glance (a magnifier, an envelope, a pair of sneakers, a Christmas tree with gifts). If the person has a reference photo, use it. If not, suggest an object and describe it before drawing.
3. **People.** No people, faces, hands or characters. If asked, explain that the palette has no skin tone and that portraits did not fit the object style, and offer an object that carries the same idea.

## 2. Palette

A drawing uses the page's own game colours plus the four illustration base colours, and nothing else. No transparency, no derived shades, no colours from other games. Depth and side faces reuse a colour already in the set.

**Illustration base, same on every page**

| Name | Hex | Use |
| --- | --- | --- |
| Snout Black | #1A000A | Every outline |
| Claw White | #FDFFF3 | White objects, light end of white gradients, PNG background |
| Scrubs Blue Light | #C5D0FF | Secondary objects, depth under white objects, implied text bars |
| Scrubs Blue | #8D98EC | Secondary objects, stripes |
| Tennis Yellow | #EBFF00 | Small accents only: a bow tip, a pendant, a star, a lace tip, the dot of a question mark |

**Game colours (fill / strong / soft)**

| Game | Fill | Strong | Soft |
| --- | --- | --- | --- |
| Secret Santa | #FF8A73 | #E5533A | #FFC4B8 |
| Secret Office Missions | #FFA3D7 | #E0509B | #FFD9EE |
| Who's Who | #F6CF6B | #C9971A | #FBEAB8 |
| Step Challenge | #A6F5B8 | #3FBF6A | #D6FBDD |
| Shoutouts | #EBFF00 | #B8C900 | #F7FFA8 |
| Recognition | #8D98EC | #5560D0 | #C5D0FF |
| Coffee Roulette | #FFB15C | #E67E1E | #FFD9AE |
| Truth or Bluff | #B79BFF | #7B55E8 | #DCCDFF |

Fill is the main surface. Strong is for depth, small marks and dark details. Soft is the light end of a gradient. The game colours are a working set that Vilo has not confirmed yet; if the person gives newer values, use theirs.

Never use the retired colours #3546F0, #8A4FD8, #FF3A3A, #FF92BE, #FFD83A, #FF7A2E, #1F8A3F, #EFE7DE or #1B1B1B.

If the object's real colour is not in the set (a green tree on a coral page), recolour it with the set: the tree becomes Scrubs Blue. That is expected, not a problem.

## 3. Anatomy of a drawing

- **Canvas:** 1600 x 1100 px. Centre the object with even margins of at least 120 px on every side.
- **Mobile:** the same file is used on phones, where the drawing shows about 290 px high. Keep the main object in the middle 70% of the canvas, with no small detail that only reads at full size. The drawing must still read if cropped to a square or 4:5 around the centre.
- **Outline:** one Snout Black line on every shape, about 4.5 px, round caps and round joins. Small details (folds, stitches, seams, glints) are single strokes at about 3.6 px. Never leave a shape without an outline.
- **Fill:** flat colour, or a smooth two-stop linear gradient on the main object only: soft to fill, or fill to strong, running diagonally from top left to bottom right. Side faces and secondary parts are flat.
- **Depth:** draw a copy of the main shape shifted about 12 px down and right, behind it, in the game's strong colour. Under white objects use Scrubs Blue Light.
- **Text is implied:** rounded bars in Scrubs Blue Light or Scrubs Blue. Never real words, numbers, logos or lettering copied from the reference.
- **Perspective:** boxes and stacks are real 3D boxes seen through one camera with one vanishing point, so every box closes and rests on the one below. Use the box engine in section 6.
- **Pattern:** two or three patterned objects per scene at most (dots or stripes). Everything else is plain.
- **No grain:** no texture noise, no speed lines, no motion marks, no scattered dots or confetti, no background decoration. The background is empty.

## 4. Choosing and simplifying the subject

- Fewer elements beat a busy scene: three text bars, one card, one small question mark. When unsure, remove something.
- Keep it physically believable: objects rest on each other, nothing floats unless it is meant to be in motion.
- Do not fake a 3/4 view by sweeping or duplicating a side view; it doubles the toe, the sole or the edges and looks wrong. Either keep a clean side view or draw the 3/4 view from scratch.
- Drop all branding and printed words from the reference (logos, "PAR AVION", plane stamps, brand stripes that identify a maker). Replace them with plain shapes or implied text bars.
- Small accents are welcome but sparing: one bow, one pendant, one star.

Approved examples, for reference:

| Game | Drawing |
| --- | --- |
| Secret Santa | Christmas tree in Scrubs Blue with yellow garland and star, coral and white gifts in 3D around it. A second option: a pile of gifts in 3D perspective. |
| Who's Who | Magnifier with a yellow frame and handle over three implied text bars (Scrubs Blue Light, Scrubs Blue, Scrubs Blue Light). Inside the lens the bars are magnified about 1.5x. |
| Secret Office Missions | Open pink envelope with airmail stripes (Scrubs Blue and pink strong), and a white clue card in front with a dashed pink frame and a small pink question mark in its centre, its dot in Tennis Yellow. |
| Step Challenge | A pair of green sneakers mid-run: one with the toe up, one with the heel up. Scrubs Blue Light air bubbles, yellow lace tips. |

## 5. Workflow

1. **Look at the reference.** If there is a photo, make a gridded copy (lines every 50 px, labels every 100 px) and view it, so you can read coordinates of the key points.
2. **Plan in words.** List the parts back to front, the colour of each part, which part gets the gradient, and what you are leaving out.
3. **Write one Python script** that builds the SVG with the helpers in section 6, palette as constants at the top. Give every part that might move its own `<g id="...">` (the lid, the card, the glass, each shoe), so a developer can animate it later.
4. **Render and look.** Render to PNG, open the PNG and check it against the checklist in section 7. Fix and render again. Expect two or three rounds.
5. **Deliver** three files named after the game, for example `step_challenge.svg`, `step_challenge.png`, `step_challenge_transparent.png`. Show the PNG and list in one or two lines which colour went where.

Install once: `pip install cairosvg` (add `--break-system-packages` if pip asks).

## 6. Code helpers

```python
import math, cairosvg
import numpy as np

W, H = 1600, 1100
INK, CLAW, BLUE_L, BLUE, YEL = "#1A000A", "#FDFFF3", "#C5D0FF", "#8D98EC", "#EBFF00"
# Set per game, e.g. Secret Santa:
FILL, STRONG, SOFT = "#FF8A73", "#E5533A", "#FFC4B8"
SW, SW_DETAIL = 4.5, 3.6

GRADS = {"main": (SOFT, FILL)}          # id -> (start colour, end colour); add more if needed

def stroke(sw=SW):
    return f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"'

def fill(c):
    return f"url(#{c})" if c in GRADS else c

def path(d, c, sw=SW, extra=""):
    return f'<path d="{d}" fill="{fill(c)}" {stroke(sw)} {extra}/>'

def line(d, sw=SW_DETAIL):
    return f'<path d="{d}" fill="none" {stroke(sw)}/>'

def with_depth(d, front, depth=STRONG, dx=12, dy=12):
    """Main shape with its depth copy behind it."""
    return f'<g transform="translate({dx} {dy})">{path(d, depth)}</g>' + path(d, front)

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
    cairosvg.svg2png(bytestring=s.encode(), write_to=f"{name}.png")
    cairosvg.svg2png(bytestring=svg(body, False).encode(), write_to=f"{name}_transparent.png")
```

### 3D box engine (gifts, boxes, stacks)

Each box has a centre, a size and a rotation in world units (y is up, the ground is y = 0, z points toward the viewer). One perspective camera projects every box, only faces that point at the camera are drawn, and ribbons and stripes are mapped onto the faces, so everything shares one vanishing point. Draw boxes back to front.

```python
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

def pts(ps): return " ".join(f"{x:.1f},{y:.1f}" for x, y in ps)

class Box:
    def __init__(self, centre, size, yaw=0, roll=0, faces=None, ribbons=(), stripes=None):
        self.c = np.array(centre, float); self.h = np.array(size, float) / 2; self.R = rot(yaw, roll)
        self.faces = faces or {"default": STRONG, "front": "main", "top": SOFT}
        self.ribbons = ribbons          # list of (axis 0=x or 2=z, half width, colour)
        self.stripes = stripes          # (colour, axis, count) or None
    def local(self, f, u, v):
        n, sg, ua, va = FACES[f]; l = [0, 0, 0]
        l[n] = sg*self.h[n]; l[ua] = u*self.h[ua]; l[va] = v*self.h[va]; return l
    def P(self, l): return proj(self.R @ np.array(l, float) + self.c)
    def quad(self, f, u0=-1, u1=1, v0=-1, v1=1):
        return [self.P(self.local(f, u, v)) for u, v in ((u0, v0), (u1, v0), (u1, v1), (u0, v1))]
    def visible(self, f):
        n, sg, _, _ = FACES[f]; nv = np.zeros(3); nv[n] = sg
        centre = self.R @ np.array(self.local(f, 0, 0)) + self.c
        return (self.R @ nv) @ (CAM - centre) > 1e-3
    def top_centre(self): return self.P([0, self.h[1], 0])

def draw_box(b):
    out = ""
    for f in FACES:
        if not b.visible(f): continue
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
            if axis == n: continue
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

# Example: two gifts, one stacked on the other
body = ""
for b, bc in [(Box((0, 90, 0), (260, 180, 200), yaw=10, ribbons=[(0, 16, CLAW), (2, 16, CLAW)]), CLAW),
              (Box((20, 230, 10), (140, 100, 120), yaw=-12,
                   faces={"default": BLUE_L, "front": CLAW, "top": CLAW, "right": CLAW},
                   ribbons=[(0, 12, STRONG), (2, 12, STRONG)]), STRONG)]:
    body += draw_box(b) + bow(b.top_centre(), bc, 0.6)
export("example_gifts", body)
```

A box resting on another has its centre y = the lower box's top (its centre y + half its height) + its own half height. For a box lying on its side or leaning, use `roll`; keep leaning boxes rare.

## 7. Checklist before delivering

- Every colour in the file is in the page's game set or the base set. Search the SVG for hex codes and compare.
- Every shape has the Snout Black outline at the right weight.
- Exactly one object or group carries the gradient; the depth copy is in the game's strong colour or Scrubs Blue Light.
- No real words, numbers, logos or copied lettering.
- No grain, speed lines, scattered decoration or background.
- Perspective is consistent: boxes close, objects rest on each other, no floating edges.
- At most two or three patterned objects.
- The object is centred with even margins and still reads at 290 px high.
- Tennis Yellow appears only as small accents.

If the person asks for a change, change only that and keep everything else as it was. Re-run the checklist after each round.
