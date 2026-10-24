# anopticon.com

The website of Anopticon. Anopticon tests what machines report against what the physical world allows.

Static pages, plain HTML, CSS and JavaScript. No framework; `build.py` writes the pages.

## Layout

```
build.py            every page, its title, description and JSON-LD; writes public/ and the sitemap
public/
  index.html                     home: five real cases of ships that were not where they said
  ais-spoofing/  ledger/  projects/ (nereus/ argus/ aether/)  research/  team/  about/  contact/   one subject each
  404.html  sitemap.xml  robots.txt  llms.txt  site.webmanifest  favicon.ico
  assets/
    site.css      all styles; palette and the five type sizes at the top (:root)
    site.js       page colour on scroll, drawings that draw with the scroll, menu, entrances
    world.js      land outline from Natural Earth (public domain), for the Lima case
    og.png, icons/    social card, favicon (an orange position ring) and app icons
    img/          the three public-domain pictures and credits.json
tools/              HTML used to render og.png and the icons with headless Chrome
render.yaml         Render blueprint: publishes public/, redirects the old .html URLs
```

Edit `build.py` (copy) or `public/assets/*` (look), run `python build.py`, commit `public/`. Render needs no build step.

The one sentence that says what Anopticon does, "Anopticon tests what machines report against what the physical world allows.", is `WHAT` in `build.py`
and appears on every page, in the schema, the manifest and `llms.txt`. Keep it plain; AI answer engines read it.

## Run locally

```
python -m http.server 4173 --directory public
```

Then open http://localhost:4173. Any static server works.

## The home page

Five real cases, oldest first: the 2013 "pwned" ship, Point Reyes 2019, Shanghai 2019, Los Angeles and Long Beach 2026, and our
own Lima record of October 2026. Each case has a drawing whose lines draw as you scroll, and the page colour follows the case on
screen (black, white, International Orange). All text is in the HTML; the drawings and the world map add to it, nothing waits on
them. Sources are linked under each case.

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
