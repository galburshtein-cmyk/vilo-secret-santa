# Vilo Play: Secret Santa landing page (prototype)

A static HTML prototype of the Secret Santa page for Vilo Play, with three more game pages built on the same template. One HTML file, no build step.

## Run it

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 4173
```

then open http://localhost:4173.

## Pages

- Secret Santa is the default page.
- Click a game card at the bottom (Who's Who, Secret Office Missions, Step Challenge) to switch the hero and the "How it works" demo to that game. The page takes the game's colour.
- "Vilo Play" in the top menu goes back to Secret Santa.
- Direct links: `?game=whos`, `?game=missions`, `?game=steps`.

## What it is

- **One page template for every game.** Copy, colour, steps, prices, FAQ and quotes live in the `GAME` object at the top of the script, and the other games are in `GAMES`. A new game is a data record, a colour and a drawing.
- **One colour per page.** Black, white and a single game colour (fill, strong, soft). Change `color` and the whole page follows.
- **The product is a chat.** The demo windows are Slack threads. In the Secret Santa demo, replies and quick-answer buttons work.
- **Snow** falls on the Secret Santa page only and scrolls with the page.
- Other switches: `?season=before|after|off` (the closing banner), `?hero=A|B|C` (older hero variants).
- Respects `prefers-reduced-motion`, and there is a "Pause animations" button in the footer.
- Fonts: Familjen Grotesk (headings, bundled in `fonts/`, SIL Open Font License), Hanken Grotesk and DM Mono from Google Fonts.

## Still placeholders

- **Illustrations:** drawn as placeholders, to be replaced or refined.
- **Logo:** a CSS ring and the word "vilo". Replace with the official logo files.
- **Copy to fill in:** the banner text for "after the deadline" and "off season" (`[Copy from Vilo: …]`). Example messages in the game demos are examples.
- **Numbers** in the HR panel are example data.
- **Sign-up form is static:** nothing is sent anywhere.
