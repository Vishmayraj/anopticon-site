# anopticon.com

Five static pages in `public/`, with `styles.css`, `main.js` and `assets/`. No build step, no framework, about 1.1 MB.
Fonts come from Google Fonts; the pictures are public domain (`public/assets/credits.json`).

Run it locally: `python -m http.server 4173 --directory public`.

## Put it on anopticon.com with a separate Render account

1. **Repo.** https://github.com/Vishmayraj/anopticon-site (this repository).
2. **Render.** Sign in to the new Render account, connect that GitHub account, then either
   *New > Blueprint* (it reads `render.yaml`) or *New > Static Site* with build command empty and publish
   directory `public`. Static sites are free on Render. Every push to `main` redeploys.
3. **Custom domain.** In the site's *Settings > Custom Domains*, add `anopticon.com` and `www.anopticon.com`
   (the blueprint already lists both). Render shows the exact records to create; at the time of writing they are:

   | Host | Type | Value |
   |---|---|---|
   | `@` (anopticon.com) | A | `216.24.57.1` (or ALIAS/ANAME to `anopticon-site.onrender.com` if the registrar supports it) |
   | `www` | CNAME | `anopticon-site.onrender.com` |

   Use the values Render shows if they differ. Remove any parking-page A/CNAME records the registrar added.
   Render then verifies the domain and issues the TLS certificate itself (minutes to an hour after DNS propagates).
4. **Email.** The page publishes `vishmayraj@anopticon.com`. Make sure that address receives mail before the
   page goes live (Google Workspace, Zoho, or the registrar's forwarding to an existing inbox), and **do not
   touch the MX and TXT records** while editing DNS for the site.
5. **Check.** Open `https://anopticon.com` and `https://www.anopticon.com`, send a test mail to the address on the
   page, and check the page on a phone.

## Before it goes live

- "Under review, 2026" describes the paper; change it when the paper is accepted or published.
- The brand book asks for a trademark check on "Argus" before it is used publicly.
