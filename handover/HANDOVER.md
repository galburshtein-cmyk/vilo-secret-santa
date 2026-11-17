# Vilo Play landing pages: handover

Everything you need to open the project, change it, publish it and make new illustrations in the same style.

## 0. Why this exists, and what is in the package

**Goal.** A new landing page for Vilo Play that presents the whole platform (a library of games that run in Slack and in the Vilo app), not a single game. The page is modular: a new game is a data record, a colour and a drawing. Secret Santa is the first full page, built as the model for the rest.

**Decisions already made**
- The Secret Santa page departs from the template the other seven game pages on vilohub.com share (hero, the game in action, setup, why, when, Slack or app, Moment). Its order is: hero, logos, the demo as a Slack conversation, setup, HR view, prices, quotes, FAQ, closing banner, then the other games. The demo is six steps, shorter than the seven on the current Vilo page, to keep it from running long.
- Calm shell, colour from the game: black, white and one game colour per page.
- A light drawn illustration language (one object per game) and light motion in the spirit of monday.com.
- Only Vilo's own text. Numbers in demos are examples.

**In the zip file**

| Folder | What |
| --- | --- |
| `site/` | A full copy of the website: `index.html`, `art/`, `fonts/`, `README.md`. You can run it on your own computer (section 2). |
| `style-guide/` | The style guide as one HTML file. Open it in a browser. |
| `handover/` | This file, the illustration skill (`vilo-illustration/` and `.zip`), the drawing tools (`tools/`) and the scripts that drew the four existing illustrations (`scripts/`). |

## 1. What you have

| What | Where |
| --- | --- |
| The pages (preview) | https://galburshtein-cmyk.github.io/vilo-secret-santa/ |
| Style guide (preview) | https://galburshtein-cmyk.github.io/vilo-secret-santa/style-guide.html |
| The code (view only) | https://github.com/galburshtein-cmyk/vilo-secret-santa |
| Illustration skill | `handover/vilo-illustration/SKILL.md` (and `handover/vilo-illustration.zip`) |
| Illustration code helpers | `handover/tools/` |
| Scripts of the existing drawings | `handover/scripts/` |

The site is one static HTML file with no build step. It shows four pages on one template: **Secret Santa** (the default), **Who's Who**, **Secret Office Missions** and **Step Challenge**. Click a game card at the bottom of the page to open that game, or add `?game=whos`, `?game=missions` or `?game=steps` to the address. To go back to Secret Santa, click "Vilo Play" in the top menu, or the Vilo logo (on a phone the menu links are hidden, so use the logo).

The preview links and the GitHub link are for looking only. The files you work with are in the zip file, and putting the site live is up to you (section 4).

Everything on the pages is a **prototype**. See section 9 for what is still a placeholder.

## 2. Open the project and run it

You need Python 3 (any version from 3.8). From the zip file, open a terminal in the `site/` folder and run:

```bash
python3 -m http.server 4173
```

Open http://localhost:4173/ in a browser. Open `style-guide.html` the same way. To see the phone layout, open the browser's developer tools and switch to a phone view (about 375 px wide).

What is in the folder:

```
index.html         the whole site (HTML, CSS and JavaScript in one file)
style-guide.html   the style guide
art/               the four hero drawings (SVG)
fonts/             Familjen Grotesk (headline font, SIL Open Font License)
handover/          this file, the illustration skill and the drawing tools
README.md          short notes about the prototype
```

Fonts: headlines use Familjen Grotesk (bundled), body text uses Hanken Grotesk and labels use DM Mono (both loaded from Google Fonts).

## 3. How the page is built

All copy, colours and demo steps are data at the top of the `<script>` in `index.html`. You do not need to touch the layout code to change words.

- **`GAME`** is the Secret Santa page: colour (`color`), hero text (`hero`), demo section heading (`demo`), the demo steps (`steps`), setup cards (`setup`), the HR numbers (`hrp`), prices (`pricing`), quotes, FAQ, closing banner (`end`) and the game cards at the bottom (`more`).
- **`GAMES`** holds the other three games (`whos`, `missions`, `steps`). Each record has `tag`, `color`, `name`, `art`, `msg` (the floating message), `hero`, `cta`, `demo` and `steps`. Clicking a game card, or the `?game=` address, swaps the hero and the demo section to that record and sets the page colour. Only the hero and the demo section change per game; the other sections stay as Secret Santa's.
- **Colours** are three CSS variables set from the record: `--g` (fill), `--gs` (strong) and `--g-soft`. One game colour per page; the rest of the page uses the base colours.
- **A demo step** looks like `{when:'Day one', t:'One DM. One tap.', d:'description', tip:'small note', mock:()=>…}`. `mock` returns the message window, built with `vm(time, html)` for a Vilo message and `um(name, time, html)` for a colleague.

Rules the page follows are written in the style guide: clickable things have a black outline and a hard shadow and press in, everything else is flat; colour comes only from the game; no real words inside drawings.

### Change copy or colours

1. Open `index.html` and find `const GAME={` (Secret Santa) or `const GAMES={` (the other games).
2. Edit the text or the hex values.
3. Reload the browser.

Use only text that Vilo has approved. Anything missing is marked in square brackets, like `[Copy from Vilo: off season]`.

### Add a new game page

Today the games are wired by name in three places, so a new game needs these steps:

1. **Record.** Add a record to `GAMES` (copy `whos` and change it). Add its name to the `SLUG` table near the bottom (`'Name':'key'`).
2. **Card.** Add an item `[name, one line, colour]` to `GAME.more.items`, and a colour rule `.games .gc:nth-child(n){--c:#…}`.
3. **Drawing.** Make the drawing (section 6). Put the SVG in `art/`. For the animated version on the card and in the hero, the drawing must be inline SVG: paste it into the card template in `render()` (search for `ww-art`, `mo-art` and `sc-art` to see how the three existing ones are done) and add its selector to the `sel` table in `switchGame()` (search for `svg.ww-art`).
4. **Motion.** Add CSS for the moving parts, copying the rules for `.mag`, `.shoe-a` or `.mo-letter` (search the file for them). Hero loop, card hover and the phone version each have their own rule.
5. Check the page on desktop and on a phone width.

This hand-wiring is the part most worth cleaning up next: moving each game's drawing into its record in `GAMES` would let a new game be added by data alone.

### Where the copy comes from

The words on the pages come from Vilo's own site. When something changes there, update the data in `index.html`.

| Page | Source |
| --- | --- |
| Secret Santa | https://vilohub.com/secret-santa (seven steps there; the prototype shows six, with the "within hours of sending" step folded into step five) |
| Who's Who | https://vilohub.com/game-whos |
| Secret Office Missions | https://vilohub.com/game-missions |
| Step Challenge | https://vilohub.com/game-steps |

Each of the three game pages has four demo steps there, and so does the prototype.

## 4. Put it live

The site is plain static files: HTML, SVG drawings and one font file, with no build step and no server code. To put it live, upload the contents of the `site/` folder to any static host or to your own web server. The preview links in section 1 are only for looking; they are not the production site.

## 5. The style guide

`style-guide.html` documents colours, type, components, icons, the illustration language, motion, responsive behaviour, accessibility, copy and tokens. Keep it in step with the page: when a rule changes in `index.html`, change it in the guide too.

## 6. Make new illustrations in the Vilo style

The illustration language is written as a **skill** for Claude. With it, you give Claude an ordinary photo of an object and it draws that object as a Vilo illustration: clean outlined SVG, in one game's colours, with the same line weight, depth and palette as the existing drawings.

### One-time setup

1. **Install the skill.** Pick one:
   - **Claude Code (terminal or desktop app):** copy the folder `handover/vilo-illustration` into `~/.claude/skills/` so that `~/.claude/skills/vilo-illustration/SKILL.md` exists. Restart Claude Code.
   - **Claude.ai chat:** open Settings, then Capabilities (Skills), and upload `handover/vilo-illustration.zip`. If the Skills option is not in your plan, paste the contents of `SKILL.md` as the first message of a new chat instead.
2. **Install the drawing tools** (so Claude can draw and render the PNG):
   ```bash
   pip install numpy cairosvg
   ```
   On a Mac, `cairosvg` also needs the cairo library: run `brew install cairo` first. Without it the SVG is still written, only the PNG preview fails.
3. Optional check: `cd handover/tools && python3 example_gifts.py` writes `example_gifts.svg` (and the PNGs).

### Turn a photo into a Vilo drawing

1. **Pick the game.** The game decides the colours. Never mix two games in one drawing. The colour sets are in the skill and in the style guide.
2. **Pick a photo.** One everyday object, clear and well lit, ideally from the side or front. No people, no hands, no faces. A stock photo is fine. Brand names and printed words in the photo are dropped automatically.
3. **Ask Claude.** Attach the photo and write something like:

   > Use the vilo-illustration skill. Game: Coffee Roulette. Draw the object in this photo as a hero illustration.

   If you leave out the game or the photo, Claude asks for it.
4. **Claude plans, then draws.** It describes the parts back to front and which colour each gets, writes one Python script using `tools/vilo_helpers.py`, renders a PNG and checks it against the skill's checklist. Expect two or three rounds. Say exactly what to change ("make the handle shorter") and Claude changes only that.
5. **You get three files**, named after the game: `coffee_roulette.svg`, `coffee_roulette.png` and `coffee_roulette_transparent.png`. The SVG is the one used on the site; each part that may move is its own group with an id.
6. **Check it yourself** against the list below, then add it to the project (next section).

### What a good drawing looks like

- One object, centred, with empty space around it. It must still read at about 290 px high on a phone.
- One thin dark outline on every shape, and nothing outside the page's game colours plus the four base colours.
- Flat colour with one smooth gradient on the main object, and a copy of it shifted 12 px down and right behind it for depth.
- Text is shown as rounded bars, never real words.
- No grain, speed lines, background or scattered decoration.

### Change one of the existing drawings

The scripts that drew the four hero illustrations are in `handover/scripts/` (see the `README.md` there). Each writes an SVG and two PNGs:

```bash
cd handover/scripts
pip install cairosvg numpy pillow
python3 whos_who.py whos_who
```

The scripts draw static pictures. The moving parts on the site (the magnifier, the shoes, the envelope flap and card, the falling gifts) are groups with class names that were added to the SVGs in `art/`, so after re-running a script, add them again: `mag` (Who's Who), `shoe shoe-a` and `shoe shoe-b` (Step Challenge), `mo-flap-back`, `mo-letter` and `mo-flap-front` (Secret Office Missions). The Secret Santa tree in `art/secret_santa_tree_anim.svg` has its own animation inside the file. The `.png` files from two of the scripts still carry an old grain pass; use the SVGs.

You can also ask Claude (with the skill) to edit a script: "In `whos_who.py`, make the handle shorter."

### Put a new drawing on the site

1. Copy the SVG into `art/` and follow section 3, "Add a new game page", for the card, the hero and the motion.
2. To make parts move, give them classes in the SVG (for example `class="lid"`) and write CSS for them like the existing `.mag` (the magnifier) and `.shoe-a` (a shoe). Set `transform-box: fill-box` and a `transform-origin` on each moving part.
3. Add the drawing to the style guide's illustration section.

## 7. Working with Claude on the site itself

You can also open this folder in Claude Code and ask for changes in plain words ("add a fourth step to the Who's Who demo", "make the Missions hero message shorter"). Tell Claude to read `index.html` and `style-guide.html` first, and to keep to the style guide.

## 8. Checks before you publish

- Reload on a desktop width (about 1280 px) and on a phone width (375 px). No sideways scrolling on any of the four pages.
- Click each game card and use the Back and Next buttons in the phone demo.
- Every colour is from the page's game set or the base set.
- The page text is Vilo's own, and numbers in demos are marked as examples.

## 9. Still open

These are left for you to finish:

- The logo. The page uses a placeholder (a ring and the word "vilo"); replace it with the official logo files.
- Phones: the game card drawer and drawing motion rely on hover on desktop; on phones the cards are a swipe row and the drawings move on their own. Test on a real phone, because the checks so far used a browser's phone view.
- A new game still needs hand-wiring (section 3). Moving drawings into the `GAMES` records is the suggested cleanup.
