# anopticon.com

The website of Anopticon. Anopticon verifies the positions ships report.

Static pages, plain HTML, CSS and JavaScript. No framework; `build.py` writes the pages.

## Layout

```
build.py            every page, its title, description and JSON-LD; writes public/ and the sitemap
public/
  index.html                     home: the forged-flag hoist, flags then and now, hoist your name, Lima, Sea/Watch/Air
  ais-spoofing/  ledger/  projects/ (nereus/ argus/ aether/)  research/  team/  about/  contact/   one subject each
  404.html  sitemap.xml  robots.txt  llms.txt  site.webmanifest  favicon.ico
  assets/
    site.css      all styles; palette and the five type sizes at the top (:root)
    site.js       flags, the forged-flag hunt, hoist your name, prints, menu, entrances
    flags.js      the 26 International Code of Signals letter flags (from the public-domain ICS drawings on Wikimedia Commons)
    og.png, icons/    social card, favicon (flag U) and app icons
    img/          the three public-domain pictures and credits.json
tools/              HTML used to render og.png and the icons with headless Chrome
render.yaml         Render blueprint: publishes public/, redirects the old .html URLs
```

Edit `build.py` (copy) or `public/assets/*` (look), run `python build.py`, commit `public/`. Render needs no build step.

The one sentence that says what Anopticon does, "Anopticon verifies the positions ships report.", is `WHAT` in `build.py`
and appears on every page, in the schema, the manifest and `llms.txt`. Keep it plain; AI answer engines read it.

## Run locally

```
python -m http.server 4173 --directory public
```

Then open http://localhost:4173. Any static server works.

## The flags

Black, white and the three signal colours, one face (Schibsted Grotesk). Every flag is real and says what it means: K on Contact
("I wish to communicate with you"), U as the favicon ("You are running into danger"), N on the 404 ("Negative"). The home hoist
spells ANOPTICON with one flag forged at random; hovering or tapping reads each flag. Without JavaScript the text is all still there.

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
