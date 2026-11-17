import sys, cairosvg

W, H = 1600, 1100
INK="#1A000A"; BG="#FDFFF3"; YEL="#EBFF00"; BL="#C5D0FF"; BLUE="#8D98EC"
F="#FFA3D7"; ST="#E0509B"; SO="#FFD9EE"      # Secret Office Missions
SW = 4.5

DEFS = f'''
<linearGradient id="pinkg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{SO}"/><stop offset="1" stop-color="{F}"/></linearGradient>
<linearGradient id="cardg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BL}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>
<pattern id="air" width="64" height="64" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  <rect width="64" height="64" fill="{BG}"/>
  <rect x="0" width="20" height="64" fill="{BLUE}"/><rect x="32" width="20" height="64" fill="{ST}"/>
</pattern>
<pattern id="air2" width="64" height="64" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  <rect width="64" height="64" fill="url(#pinkg)"/>
  <rect x="0" width="20" height="64" fill="{BLUE}"/><rect x="32" width="20" height="64" fill="{ST}"/>
</pattern>
'''

def st(sw=SW): return f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"'

def border(w, h, inset, band, pat, sides="lrtb"):
    o = ""
    if "t" in sides: o += f'<rect x="{inset}" y="{inset}" width="{w-2*inset}" height="{band}" fill="url(#{pat})"/>'
    if "b" in sides: o += f'<rect x="{inset}" y="{h-inset-band}" width="{w-2*inset}" height="{band}" fill="url(#{pat})"/>'
    if "l" in sides: o += f'<rect x="{inset}" y="{inset}" width="{band}" height="{h-2*inset}" fill="url(#{pat})"/>'
    if "r" in sides: o += f'<rect x="{w-inset-band}" y="{inset}" width="{band}" height="{h-2*inset}" fill="url(#{pat})"/>'
    return o

def back_envelope():
    w, h = 470, 330
    o = f'<rect x="12" y="12" width="{w}" height="{h}" rx="22" fill="{BL}" {st()}/>'
    o += f'<rect width="{w}" height="{h}" rx="22" fill="{BG}" {st()}/>'
    o += f'<rect x="22" y="22" width="{w-44}" height="{h-44}" rx="12" fill="none" stroke="{ST}" stroke-width="4" stroke-dasharray="14 12" stroke-linecap="round"/>'
    cx, cy = w/2, h/2 + 4
    q = f"M{cx-32},{cy-36} C{cx-32},{cy-80} {cx+32},{cy-80} {cx+32},{cy-36} C{cx+32},{cy-8} {cx},{cy-2} {cx},{cy+22}"
    o += f'<path d="{q}" fill="none" stroke="{INK}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>'
    o += f'<path d="{q}" fill="none" stroke="{ST}" stroke-width="21" stroke-linecap="round" stroke-linejoin="round"/>'
    o += f'<circle cx="{cx}" cy="{cy+60}" r="14" fill="{YEL}" {st()}/>'
    return o

def front_envelope():
    w, h = 580, 420
    o = ""
    # open flap behind (inside of the flap)
    flap = f"M0,0 L{w},0 L{w-70},-176 C{w-80},-194 {w-100},-200 {w-120},-200 L130,-200 C110,-200 92,-194 82,-176 Z"
    o += f'<path d="{flap}" transform="translate(12 12)" fill="{ST}" {st()}/>'
    o += f'<path d="{flap}" fill="{SO}" {st()}/>'
    # body
    o += f'<rect x="12" y="12" width="{w}" height="{h}" rx="8" fill="{ST}" {st()}/>'
    o += f'<rect width="{w}" height="{h}" rx="8" fill="url(#pinkg)" {st()}/>'
    o += f'<clipPath id="fe"><rect width="{w}" height="{h}" rx="8"/></clipPath><g clip-path="url(#fe)">{border(w,h,0,28,"air2","lrb")}</g>'
    o += f'<rect width="{w}" height="{h}" rx="8" fill="none" {st()}/>'
    # soft fold lines
    return o

def svg(bg=True):
    body = (f'<g transform="translate(330 400) rotate(-8)">{front_envelope()}</g>'
            f'<g transform="translate(800 470) rotate(10)">{back_envelope()}</g>')
    bgr = f'<rect width="{W}" height="{H}" fill="{BG}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{DEFS}</defs>{bgr}{body}</svg>'

if __name__ == "__main__":
    out = sys.argv[1]
    open(out + ".svg", "w").write(svg())
    cairosvg.svg2png(bytestring=svg().encode(), write_to=out + ".png")
    cairosvg.svg2png(bytestring=svg(False).encode(), write_to=out + "_transparent.png")
