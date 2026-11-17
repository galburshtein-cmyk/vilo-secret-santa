"""Example drawing: two gifts, one stacked on the other, in the Secret Santa colours.

Run from this folder:  python3 example_gifts.py
It writes example_gifts.svg (and the PNGs if cairosvg is installed).
Copy this file as a starting point for a new drawing.
"""
from vilo_helpers import *

use_game("Secret Santa")          # sets fill, strong and soft for this game

body = ""
for b, bc in [
    (Box((0, 90, 0), (260, 180, 200), yaw=10, ribbons=[(0, 16, CLAW), (2, 16, CLAW)]), CLAW),
    (Box((20, 230, 10), (140, 100, 120), yaw=-12,
         faces={"default": BLUE_L, "front": CLAW, "top": CLAW, "right": CLAW},
         ribbons=[(0, 12, STRONG), (2, 12, STRONG)]), STRONG),
]:
    body += draw_box(b) + bow(b.top_centre(), bc, 0.6)

export("example_gifts", body)
