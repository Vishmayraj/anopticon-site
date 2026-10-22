# anopticon.com

The public page for Anopticon: solving for data poisoning in the maritime domain.

One static page. Plain HTML, CSS and JavaScript, no framework and no build step.

## Layout

```
public/
  index.html        the page
  styles.css        all styles; brand tokens at the top (:root)
  main.js           the hero canvas, the lens, section entrances
  assets/
    anopticon-*.svg, favicon-paper.svg   brand wordmark and favicon
    nereus-lekythos.jpg, argus-vase.jpg, aether-icarus.jpg   project pictures
    credits.json    source and licence of every picture
render.yaml         Render blueprint (static site, publishes public/)
DEPLOY.md           domain and DNS steps
```

## Run locally

```
python -m http.server 4173 --directory public
```

Then open http://localhost:4173. Any static server works.

## The hero

`main.js` draws ship tracks on a canvas. Each ship moves along a lane and broadcasts reports. Every few seconds some
reports are pulled onto one point (a pile-up, the way interference moves real positions). Outside the ring every report
looks the same; inside it, poisoned reports are drawn in red and tied back to where the ship really was. The ring
follows the mouse, or moves to a tap on touch screens, and drifts on its own when idle.

It is an illustration, not data. The only real figures on the page are the Lima event (10 October 2026) and the
paper's.

With `prefers-reduced-motion`, the canvas draws one still frame and nothing else moves. Without JavaScript all content
is still visible.

## Brand

Colours, type and the wordmark follow the Anopticon brand book: Paper `#FAF9F5`, Ink `#0E1116`, Signal `#E5482D`
(what does not fit), Archivo Expanded for display, Source Serif 4 for prose, IBM Plex Mono for figures only. Fonts load
from Google Fonts.

## Pictures

All public domain:

- Heracles and Nereus, black-figure lekythos by the Istanbul Painter, about 590 BC, Louvre CA 823. Wikimedia Commons.
- Hermes and Argus, drawing after an Athenian red-figure vase, W. H. Roscher, 1890. Wikimedia Commons (cropped).
- Armed three-master with Daedalus and Icarus in the sky, after Pieter Bruegel the Elder, 1561-65. The Metropolitan
  Museum of Art (CC0).

## Deploy

Hosted on Render as a static site; every push to `main` redeploys. See [DEPLOY.md](DEPLOY.md).

## Contact

vishmayraj@anopticon.com
