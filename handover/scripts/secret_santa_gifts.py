import numpy as np, cairosvg, io, sys, math
from PIL import Image

W, H = 1600, 1100
INK="#1A000A"; CREAM="#FDFFF3"; OFF="#FDFFF3"
CF="#FF8A73"; CS="#E5533A"; CSO="#FFC4B8"            # Secret Santa coral
BLUE="#8D98EC"; VIOLET="#8D98EC"; PINK="#C5D0FF"; YEL="#EBFF00"; BLIGHT="#C5D0FF"
SW = 4.5
ELEV = math.radians(24)
OX, OY = 900, 560
GRAINSVG = False

GRADS = {
    "coral": [(0, CSO), (0.5, CF), (1, CS)],
    "blue":  [(0, BLIGHT), (1, BLUE)],
    "pale":  [(0, OFF), (1, CSO)],
}

CAM = np.array([0.0, 950.0, 2500.0]); LOOK = np.array([0.0, 200.0, 0.0]); FOC = 2750.0
_pitch = math.atan2(CAM[1]-LOOK[1], CAM[2]-LOOK[2])
def proj(p):
    v = np.array(p, float) - CAM
    c, s_ = math.cos(_pitch), math.sin(_pitch)
    yc = v[1]*c - v[2]*s_
    d = -v[1]*s_ - v[2]*c
    return (OX + FOC*v[0]/d, OY - FOC*yc/d)

def rot(yaw, roll, pitch=0):
    a, b, c = map(math.radians, (yaw, roll, pitch))
    Ry = np.array([[math.cos(a),0,math.sin(a)],[0,1,0],[-math.sin(a),0,math.cos(a)]])
    Rz = np.array([[math.cos(b),-math.sin(b),0],[math.sin(b),math.cos(b),0],[0,0,1]])
    Rx = np.array([[1,0,0],[0,math.cos(c),-math.sin(c)],[0,math.sin(c),math.cos(c)]])
    return Ry @ Rz @ Rx

def pts(ps): return " ".join(f"{x:.1f},{y:.1f}" for x, y in ps)

class S:
    def __init__(self, mode): self.mode=mode; self.out=[]; self.n=0
    def fill(self, f):
        if self.mode=="color": return f"url(#{f})" if f in GRADS else f
        return "#fff" if f in GRADS else "#000"
    def ink(self): return INK if self.mode=="color" else "#000"
    def poly(self, ps, f, stroke=True, sw=SW):
        st = f'stroke="{self.ink()}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else 'stroke="none"'
        flt = ' filter="url(#grain)"' if (GRAINSVG and self.mode=="color" and f in GRADS) else ""
        self.out.append(f'<polygon points="{pts(ps)}" fill="{self.fill(f)}" {st}{flt}/>')
    def raw(self, s): self.out.append(s)
    def clip(self, ps):
        self.n+=1; cid=f"c{self.n}"
        self.out.append(f'<clipPath id="{cid}"><polygon points="{pts(ps)}"/></clipPath>'); return cid
    def ell(self, c, rx, ry, f, rot=0):
        self.out.append(f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="{rx}" ry="{ry}" transform="rotate({rot} {c[0]:.1f} {c[1]:.1f})" fill="{self.fill(f)}" stroke="{self.ink()}" stroke-width="{SW}"/>')
    def path(self, d, f="none", sw=SW):
        ff = self.fill(f) if f!="none" else "none"
        self.out.append(f'<path d="{d}" fill="{ff}" stroke="{self.ink()}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')

# faces: name -> (normal axis, sign, u axis, v axis)
FACES = {"front":(2,1,0,1), "back":(2,-1,0,1), "right":(0,1,2,1), "left":(0,-1,2,1), "top":(1,1,0,2), "bottom":(1,-1,0,2)}
AX = "xyz"

class Box:
    def __init__(self, c, dims, yaw=0, roll=0, pitch=0, skin=None):
        self.c=np.array(c,float); self.h=np.array(dims,float)/2; self.R=rot(yaw,roll,pitch); self.skin=skin or {}
    def world(self, l): return self.R @ np.array(l,float) + self.c
    def P(self, l): return proj(self.world(l))
    def face_pt(self, name, u, v):
        # u,v in [-1,1]
        n, sg, ua, va = FACES[name]
        l = [0,0,0]; l[n]=sg*self.h[n]; l[ua]=u*self.h[ua]; l[va]=v*self.h[va]
        return l
    def quad(self, name, u0=-1,u1=1,v0=-1,v1=1):
        return [self.P(self.face_pt(name,u,v)) for u,v in ((u0,v0),(u1,v0),(u1,v1),(u0,v1))]
    def visible(self, name):
        n, sg, _, _ = FACES[name]; nv=np.zeros(3); nv[n]=sg
        fc = self.world(self.face_pt(name, 0, 0))
        return (self.R @ nv) @ (CAM - fc) > 1e-3
    def band_range(self, name, axis, w):
        # returns (u0,u1,v0,v1) for a band of half-width w (local units) centered at 0 on `axis`
        n, sg, ua, va = FACES[name]
        if n == axis: return None
        r = w / self.h[axis]
        return (-r, r, -1, 1) if ua == axis else (-1, 1, -r, r)

def draw_box(s, b):
    k = b.skin
    vis = [f for f in FACES if b.visible(f)]
    for f in vis:
        fill = k["faces"].get(f, k["faces"]["default"])
        q = b.quad(f)
        s.poly(q, fill)
        pat = k.get("pattern", {}).get(f, k.get("pattern", {}).get("default"))
        if pat:
            cid = s.clip(q); s.raw(f'<g clip-path="url(#{cid})">')
            n, sg, ua, va = FACES[f]
            if pat[0] == "dots":
                _, col, step, r = pat
                nu = max(2, int(2*b.h[ua]/step)); nvv = max(2, int(2*b.h[va]/step))
                for j in range(nvv+1):
                    for i in range(nu+1):
                        u = -1 + 2*(i + (0.5 if j%2 else 0))/nu; v = -1 + 2*j/nvv
                        ring = [b.P(np.array(b.face_pt(f,u,v)) + _circ(ua,va,r,t)) for t in range(12)]
                        s.poly(ring, col, stroke=False)
            elif pat[0] == "stripes":
                _, col, axis, count, frac = pat
                if axis != n:
                    for i in range(count):
                        a = -1 + 2*(i+0.25)/count; c2 = a + 2*frac/count
                        if ua == axis: qq = b.quad(f, a, c2, -1, 1)
                        else: qq = b.quad(f, -1, 1, a, c2)
                        s.poly(qq, col, stroke=False)
            s.raw('</g>')
            s.poly(q, "none")
        for (axis, w, col) in k.get("ribbons", []):
            rg = b.band_range(f, axis, w)
            if rg: s.poly(b.quad(f, *rg), col, sw=SW*0.8)

def _circ(ua, va, r, t):
    a = 2*math.pi*t/12; v = np.zeros(3); v[ua]=r*math.cos(a); v[va]=r*math.sin(a); return v

def bow(s, c, f, size=1.0, rot=0):
    k=size; x,y=c
    s.raw(f'<g transform="rotate({rot} {x} {y})">')
    s.path(f"M{x},{y} l{-30*k},{55*k} l{12*k},{-4*k} l{8*k},{10*k} Z", f)
    s.path(f"M{x},{y} l{28*k},{58*k} l{-12*k},{-3*k} l{-9*k},{9*k} Z", f)
    s.path(f"M{x},{y} C{x-25*k},{y-55*k} {x-80*k},{y-30*k} {x-62*k},{y+4*k} C{x-50*k},{y+22*k} {x-20*k},{y+10*k} {x},{y} Z", f)
    s.path(f"M{x},{y} C{x+25*k},{y-55*k} {x+80*k},{y-30*k} {x+62*k},{y+4*k} C{x+50*k},{y+22*k} {x+20*k},{y+10*k} {x},{y} Z", f)
    s.path(f"M{x-14*k},{y-4*k} q{-20*k},{-14*k} {-38*k},{-10*k}", sw=SW*0.7)
    s.path(f"M{x+14*k},{y-4*k} q{20*k},{-14*k} {38*k},{-10*k}", sw=SW*0.7)
    s.ell(c, 13*k, 11*k, f)
    s.raw('</g>')

def rosette(s, c, f, r=48, inner=OFF):
    for rad, col, off in ((r, f, 0), (r*0.6, inner, math.pi/10)):
        P=[]
        for i in range(20):
            a = math.pi*i/10 + off; rr = rad if i%2==0 else rad*0.6
            P.append((c[0]+rr*math.cos(a), c[1]+rr*0.8*math.sin(a)))
        s.poly(P, col)
    s.ell(c, r*0.18, r*0.15, f)

def top_center(b, dy=0): return b.P([0, b.h[1]+dy, 0])

def coral(**kw):
    d = dict(faces={"default":CS, "front":"coral", "top":CSO}, ribbons=[(0,16,OFF),(2,16,OFF)]); d.update(kw); return d
def white(dot=CF, rib=CS, **kw):
    d = dict(faces={"default":CSO, "front":OFF, "top":OFF, "right":OFF, "left":CSO},
             pattern={"default":("dots", dot, 34, 6)}, ribbons=[(0,13,rib),(2,13,rib)]); d.update(kw); return d
def blue(**kw):
    d = dict(faces={"default":BLUE, "front":"blue", "top":BLIGHT}, ribbons=[(0,14,YEL),(2,14,YEL)]); d.update(kw); return d
def pale(**kw):
    d = dict(faces={"default":CSO, "front":"pale", "top":OFF}, ribbons=[(0,14,CS),(2,14,CS)]); d.update(kw); return d

def scene(mode):
    s = S(mode)
    B = []
    # back row
    b1 = Box((360,480,-250),(260,110,170), yaw=-18, roll=-12, skin=pale()); B.append(("bow", b1, CS, 0.9))
    b6 = Box((500,335,-170),(230,230,180), yaw=-24, skin=dict(faces={"default":BLUE,"front":OFF,"top":OFF,"right":OFF},
            pattern={"front":("stripes",BLUE,0,5,0.45),"right":("stripes",BLUE,2,4,0.45)})); B.append((None,b6))
    b4 = Box((-370,135,-190),(320,270,180), yaw=-14, skin=coral(ribbons=[(0,16,OFF)])); B.append((None, b4))
    b5 = Box((150,185,-140),(300,370,200), yaw=6, skin=coral(ribbons=[(0,20,OFF)])); B.append((None,b5))
    b3 = Box((-330,315,-200),(115,90,85), yaw=20, skin=blue(ribbons=[(0,10,YEL),(2,10,YEL)])); B.append(("bowsmall", b3, YEL, 0.5))
    b2 = Box((70,440,-170),(250,140,170), yaw=9, skin=white(pattern={"front":("dots",CF,40,6),"top":("dots",CF,40,6),"right":("dots",CF,40,6)})); B.append(("bow", b2, CS, 0.95))
    b8 = Box((-110,100,-30),(190,200,140), yaw=22, skin=white(rib=CS, pattern={})); B.append(("bow", b8, CS, 0.8))
    # front row
    b12 = Box((420,118,20),(330,236,150), yaw=-6, skin=coral(ribbons=[])); B.append(("rosette_front", b12, YEL, 56))
    b7 = Box((380,301,20),(170,130,120), yaw=6, skin=white(rib=BLUE, pattern={})); B.append(("bow", b7, BLUE, 0.6))
    b9 = Box((-560,100,40),(400,100,160), yaw=-10, roll=12, skin=blue()); B.append(("bow", b9, YEL, 0.85))
    b10 = Box((-300,62,170),(430,124,170), yaw=-7, skin=coral()); B.append(("bow", b10, OFF, 1.0))
    b11 = Box((60,112,140),(240,224,200), yaw=12, skin=dict(faces={"default":CS,"front":OFF,"top":OFF,"right":CSO},
            pattern={"front":("stripes",CF,1,4,0.42),"right":("stripes",CF,1,4,0.42)}, ribbons=[(0,13,BLUE),(2,13,BLUE)])); B.append(("bow", b11, BLUE, 0.85))
    b13 = Box((-40,46,360),(92,92,92), yaw=18, skin=dict(faces={"default":CS,"front":YEL,"top":OFF}, ribbons=[(0,9,CS),(2,9,CS)])); B.append(("bow", b13, CS, 0.5))
    for item in B:
        kind, b = item[0], item[1]
        draw_box(s, b)
        if kind in ("bow", "bowsmall"): bow(s, top_center(b), item[2], item[3])
        elif kind == "rosette": rosette(s, top_center(b), item[2], item[3], OFF)
        elif kind == "rosette_front":
            rosette(s, b.P([-b.h[0]*0.25, b.h[1]*0.1, b.h[2]]), item[2], item[3], OFF)
    return "\n".join(s.out)

def svg(mode, bg=True):
    defs = ""
    if mode == "color":
        for k, stops in GRADS.items():
            st = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
            defs += f'<linearGradient id="{k}" x1="0" y1="0" x2="1" y2="1">{st}</linearGradient>'
        if GRAINSVG:
            defs += ('<filter id="grain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
                     '<feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="7" result="n"/>'
                     '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.5 0.62" result="dark"/>'
                     '<feComposite in="dark" in2="SourceAlpha" operator="in" result="d2"/>'
                     '<feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1.5 -0.86" result="light"/>'
                     '<feComposite in="light" in2="SourceAlpha" operator="in" result="l2"/>'
                     '<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="d2"/><feMergeNode in="l2"/></feMerge></filter>')
    bgc = CREAM if mode=="color" else "#000"
    bgrect = f'<rect width="{W}" height="{H}" fill="{bgc}"/>' if (bg or mode!="color") else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs>{defs}</defs>{bgrect}<g>{scene(mode)}</g></svg>')

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
