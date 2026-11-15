# Secret Santa landing page (prototype)

A static HTML prototype of the Secret Santa page for Vilo Play. One file, no build step.

## Run it

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 4173
```

then open http://localhost:4173.

## What it is

- **One page template for every game.** All copy, colour, steps, prices, FAQ and quotes live in the `GAME` object at the top of the script. A new game is a new data object, a colour and its mockups.
- **One colour per page.** Black, white and a single game colour (pink for Secret Santa), in four shades. Change `color` in `GAME` and the whole page follows.
- **The product is a chat.** The hero plays the DM, the demo windows are chat threads (replies and quick-answer buttons work), and the sign-up is a conversation.
- **Three looks** for review: `?look=1` (sticker), `?look=2` (soft pop), `?look=3` (editorial). A small switcher in the bottom-left corner changes them live.
- Other switches: `?season=before|after|off` (the closing banner), `?hero=A|B|C` (older hero variants).
- Falls back gracefully with `prefers-reduced-motion`, and there is a "Pause animations" button in the footer. Snow is built in but paused (`ambient:'none'` in `GAME`; set `'snow'` to bring it back).

## Still placeholders

- **Illustrations:** dashed circles labelled "Illustration".
- **Logo:** a CSS ring and the word "vilo". Replace with the official logo files.
- **Copy to fill in:** the timeline dates (`[date]`) and the banner text for "after the deadline" and "off season" (`[Copy from Vilo: …]`).
- **Numbers in the HR panel** are marked "Example data".
- **Sign-up form is static:** nothing is sent anywhere.

## Fonts

Headlines use **Cabinet Grotesk** (Fontshare, ITF Free Font License), expected at `fonts/CabinetGrotesk-Variable.ttf`. The font file is **not included** in this repository: the licence does not allow handing the font files to third parties. Download it yourselves from https://www.fontshare.com, accept the licence, and put the variable TTF in `fonts/`. Without it the page falls back to Hanken Grotesk.

Body text uses Hanken Grotesk, and the three looks also load Bricolage Grotesque, Fredoka, Nunito, Fraunces and Inter from Google Fonts.
