# Vilo illustration scripts

Python scripts that draw the Vilo Play hero illustrations. Each script writes three files: an SVG, a PNG with the Claw White background, and a transparent PNG.

## Setup

```
pip install cairosvg numpy pillow
```

## Run

Pass the output name (without extension):

```
python secret_santa_gifts.py secret_santa_gifts
python secret_santa_tree.py secret_santa_tree
python whos_who.py whos_who
python step_challenge.py step_challenge
python secret_office_missions.py secret_office_missions
```

## Files

| Script | Drawing | Notes |
| --- | --- | --- |
| secret_santa_gifts.py | Secret Santa gift pile | Holds the 3D box engine (perspective camera, visible faces, ribbons, stripes). Its PNG still has the old grain pass; its SVG is clean. |
| secret_santa_tree.py | Secret Santa tree with gifts | Imports secret_santa_gifts.py for the gift boxes, so keep both files in the same folder. |
| whos_who.py | Who's Who magnifier over three text bars | Its PNG still has a light grain pass; its SVG is clean. |
| step_challenge.py | Step Challenge pair of sneakers mid-run | |
| secret_office_missions.py | Secret Office Missions envelope with a clue card | |

Colours are set as constants at the top of each script. Use only the page's game colours plus the illustration base colours from the Vilo Play Style Guide.
