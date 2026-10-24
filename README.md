# anopticon.com

The website of Anopticon. Anopticon tests what machines report against what the physical world allows.

Static pages, plain HTML, CSS and JavaScript. No framework; `build.py` writes the pages.

## Layout

```
build.py            every page, its title, description and JSON-LD; writes public/ and the sitemap
public/
  index.html                     home: what we do, and a way into every page
  about/  projects/ (nereus/ argus/ aether/)  ledger/  research/  primer/  partners/  join/  team/  contact/
  ais-spoofing/                  forwards to /primer/ (the old address)
  404.html  sitemap.xml  robots.txt  llms.txt  site.webmanifest  favicon.ico
  assets/
    site.css      all styles; palette and the five type sizes at the top (:root)
    site.js       page colour on scroll, drawings that draw with the scroll, menu, entrances
    og.png, icons/    social card, favicon (an orange position ring) and app icons
    img/          public-domain pictures, with credits.json listing each source
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

## The pages

The home page is an overview with a picture and a section for each part of the site. About opens with one real case, the 2013
"pwned" ship, whose track draws itself as you scroll. Design partners and Join us both end in a prepared email. Each project page
links to the previous and next project and back to all projects. The page colour follows the section on screen (black, white,
International Orange).

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
