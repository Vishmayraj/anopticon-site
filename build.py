"""Build anopticon.com into public/.

    python build.py

Pages are defined below. Every page gets the same head (title, description, canonical, Open Graph, JSON-LD), nav and
footer. The flags are drawn in the browser from assets/flags.js (the International Code of Signals). Commit public/;
Render serves it as it is.
"""
import datetime
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / 'public'
SITE = 'https://anopticon.com'
TODAY = datetime.date.today().isoformat()
MAIL = 'vishmayraj@anopticon.com'
ZENODO = 'https://doi.org/10.5281/zenodo.23538896'

# What the company does, in one sentence. Used on every page, in the schema and in llms.txt.
WHAT = 'Anopticon verifies the positions ships report.'

ORG = {
    '@type': 'Organization', '@id': f'{SITE}/#org', 'name': 'Anopticon', 'url': f'{SITE}/',
    'logo': {'@type': 'ImageObject', 'url': f'{SITE}/assets/icons/logo-512.png', 'width': 512, 'height': 512},
    'image': f'{SITE}/assets/og.png', 'email': MAIL,
    'description': ('Anopticon verifies the positions ships report. It is a maritime data company from Gujarat, '
                    'India, working on AIS spoofing, GNSS (GPS) jamming and forged ship positions, which it calls '
                    'data poisoning at sea. Each reported position is checked against what the ship can physically '
                    'do and against independent sources.'),
    'disambiguatingDescription': ('The maritime ship-position verification company at anopticon.com. Not a general '
                                  'cybersecurity firm, and not the 2009 Venice CCTV-mapping project of the same name.'),
    'foundingDate': '2026', 'foundingLocation': {'@type': 'Place', 'name': 'Gujarat, India'},
    'knowsAbout': ['AIS spoofing', 'GNSS jamming', 'GPS spoofing at sea', 'Automatic Identification System',
                   'Ship position verification', 'Maritime domain awareness', 'Data poisoning'],
    'founder': [{'@id': f'{SITE}/team/#vishmayraj-zala'}, {'@id': f'{SITE}/team/#kathan-patel'}],
    'sameAs': ['https://github.com/Vishmayraj/anopticon-site'],
    'contactPoint': {'@type': 'ContactPoint', 'email': MAIL, 'contactType': 'sales', 'availableLanguage': 'English'},
}
WEBSITE = {'@type': 'WebSite', '@id': f'{SITE}/#site', 'url': f'{SITE}/', 'name': 'Anopticon',
           'alternateName': 'Anopticon, ship position verification', 'publisher': {'@id': f'{SITE}/#org'},
           'inLanguage': 'en'}
PEOPLE = [
    {'@type': 'Person', '@id': f'{SITE}/team/#vishmayraj-zala', 'name': 'Vishmayraj Zala', 'jobTitle': 'Founder',
     'worksFor': {'@id': f'{SITE}/#org'}, 'email': MAIL, 'alumniOf': 'Gujarat Technological University',
     'sameAs': ['https://github.com/Vishmayraj', 'https://www.linkedin.com/in/vishmayraj-zala',
                'https://orcid.org/0009-0007-9796-9449']},
    {'@type': 'Person', '@id': f'{SITE}/team/#kathan-patel', 'name': 'Kathan Patel', 'jobTitle': 'Co-founder',
     'worksFor': {'@id': f'{SITE}/#org'}, 'alumniOf': 'Gujarat Technological University',
     'sameAs': ['https://github.com/KathanPatel1310', 'https://www.linkedin.com/in/kathan-patel-0235a3354']},
]
PAPER = {
    '@type': 'ScholarlyArticle', '@id': f'{SITE}/research/#p1',
    'headline': ('Ship manoeuvring and resistance models under sparse AIS sampling: '
                 'what can be predicted, identified and bounded'),
    'author': [{'@id': f'{SITE}/team/#vishmayraj-zala'}, {'@id': f'{SITE}/team/#kathan-patel'}],
    'publisher': {'@id': f'{SITE}/#org'}, 'datePublished': '2026', 'isBasedOn': ZENODO,
    'keywords': 'AIS, dead reckoning, Nomoto model, identifiability, Holtrop-Mennen, conformal prediction, GNSS interference',
}

NAV = [('/ais-spoofing/', 'AIS spoofing'), ('/ledger/', 'Ledger'), ('/projects/', 'Projects'),
       ('/research/', 'Research'), ('/team/', 'Team')]
HERE = ' aria-current="page"'

IMG = {
    'bruegel': ('/assets/img/aether-icarus.jpg', 1600, 1228,
                'Engraving of an armed three-masted ship under sail; high in the sky Daedalus flies on and Icarus falls from the sun.',
                'Armed three-master with Daedalus and Icarus in the sky. After Pieter Bruegel the Elder, 1561&ndash;65. The Met.'),
    'nereus': ('/assets/img/nereus-lekythos.jpg', 1600, 1285,
               "Black-figure painting on an oil jar: Heracles grips Nereus, who has a fish's scaled tail and a lion springing from his back.",
               'Heracles and Nereus. Black-figure lekythos by the Istanbul Painter, about 590 BC. Louvre, CA 823.'),
    'argus': ('/assets/img/argus-vase.jpg', 1090, 430,
              'Line drawing from a Greek vase: Hermes strikes Argus, whose body is covered in eyes, while Zeus watches.',
              'Hermes kills Argus. Drawing after an Athenian red-figure vase, W. H. Roscher, 1890.'),
}


def picture(key, cls='print', lazy=True, caption=True):
    src, w, h, alt, cap = IMG[key]
    lz = ' loading="lazy"' if lazy else ''
    fc = f'<figcaption>{cap}</figcaption>' if caption else ''
    return (f'<figure class="{cls}" data-reveal><div class="print__frame" style="--src:url({src})">'
            f'<img src="{src}" width="{w}" height="{h}" alt="{html.escape(alt)}"{lz} decoding="async"></div>{fc}</figure>')


def hoist(word, cls='hoist'):
    return f'<div class="{cls}" data-hoist="{word}" role="img" aria-label="{word} in signal flags"></div>'


def crumbs(page):
    items = [('Anopticon', '/')] + page.get('crumbs', [])
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + u} for i, (n, u) in enumerate(items)]}


PAGES = []

# ---------------------------------------------------------------------------------------------------------------- home
PAGES.append(dict(
    path='', home=True,
    title='Anopticon | Ship position verification: AIS spoofing and GNSS jamming',
    desc=('Anopticon verifies the positions ships report. AIS spoofing, GNSS jamming and forged ship positions, '
          'checked against what a ship can physically do.'),
    schema=[ORG, WEBSITE] + PEOPLE,
    body=f'''
<header class="hero">
  <div class="hero__hoist" data-hoist="ANOPTICON" data-forge role="img" aria-label="ANOPTICON in signal flags, one of them forged"></div>
  <p class="hero__game" id="game" aria-live="polite">One flag in this hoist is forged. Hover or tap the flags to read them, and find it.</p>
  <div class="hero__text wrap">
    <h1 class="hero__h"><span class="line"><span>Is that ship</span></span><span class="line"><span>really there?</span></span></h1>
    <p class="hero__lede">{WHAT} Every ship broadcasts where it is. Those broadcasts can be jammed, spoofed and forged, and everything downstream believes them.</p>
  </div>
</header>

<main id="main">
<section class="band band--white" aria-labelledby="then-h">
  <div class="wrap duo">
    {picture('bruegel', 'print print--tall')}
    <div class="duo__copy">
      <h2 id="then-h" class="h2 reveal">Flags couldn&rsquo;t lie from far away.</h2>
      <p class="lead reveal">For a century and a half ships spoke in flags. To forge a ship&rsquo;s signal you had to be standing on it.</p>
      <p class="reveal">Now they speak in radio. A ship&rsquo;s position comes from a satellite signal, goes out over AIS, and is read by ports, insurers, sanctions desks and models that never see the sea. That signal can be faked from the shore, out of sight. That is data poisoning, and it is what we work on.</p>
    </div>
  </div>
</section>

<section class="band band--black" aria-labelledby="own-h">
  <div class="wrap duo duo--rev">
    <div>
      <h2 id="own-h" class="h2 reveal">Hoist your name.</h2>
      <p class="lead reveal">Then forge one flag, and see whether you can still tell.</p>
      <label class="own reveal"><span class="sr-only">Your name or your ship&rsquo;s</span>
        <input id="own" type="text" maxlength="12" value="Nereus" autocomplete="off" spellcheck="false" aria-describedby="own-read">
      </label>
      <div class="own__buttons reveal">
        <button class="btn btn--light" type="button" id="forge">Forge one</button>
        <button class="btn btn--ghost" type="button" id="check">Check</button>
      </div>
    </div>
    <div class="own__out">
      <div class="hoist hoist--own" id="own-hoist" role="img" aria-label="Your name in signal flags"></div>
      <p class="own__read" id="own-read" aria-live="polite"></p>
    </div>
  </div>
</section>

<section class="band band--white" aria-labelledby="lima-h">
  <div class="wrap">
    <h2 id="lima-h" class="h2 reveal">The Bosphorus, reported as Lima.</h2>
    <p class="lead reveal measure">On 10 October 2026, 49 ships near Istanbul broadcast positions inside one 3&nbsp;km patch of inland Peru, 12,221&nbsp;km away, at a median reported 94.9 knots.</p>
    <p class="reveal"><a class="link" href="/ledger/">Read the entry in the Ledger</a></p>
  </div>
</section>

<section class="domains" aria-labelledby="dom-h">
  <h2 id="dom-h" class="sr-only">Projects</h2>
  <a class="domain domain--sea" href="/projects/nereus/"><span class="domain__word">Sea</span><span class="domain__name">Nereus</span><span class="domain__when">Now</span></a>
  <a class="domain domain--watch" href="/projects/argus/"><span class="domain__word">Watch</span><span class="domain__name">Argus</span><span class="domain__when">Next</span></a>
  <a class="domain domain--air" href="/projects/aether/"><span class="domain__word">Air</span><span class="domain__name">Aether</span><span class="domain__when">Later</span></a>
</section>
</main>
'''))

# ---------------------------------------------------------------------------------------------------- AIS spoofing
FAQ = [
    ('What is AIS spoofing?',
     'AIS spoofing is a ship broadcasting a position, identity or movement over the Automatic Identification System '
     'that is not real. It happens when the ship\'s satellite-navigation receiver is fed a false signal, or when the AIS '
     'messages themselves are forged or altered.'),
    ('What is the difference between GNSS jamming and spoofing?',
     'Jamming drowns the satellite signal, so the receiver loses its fix and positions freeze, drift or disappear. '
     'Spoofing replaces the signal with a false one, so the receiver confidently reports the wrong place. Mild jamming '
     'can look like spoofing in the data.'),
    ('Can AIS spoofing be detected?',
     'Much of it can be flagged from the data itself: a report that needs a speed no hull can reach, or many ships '
     'reporting the same impossible spot. AIS alone rarely shows who did it. Independent sources such as radar '
     'satellites can confirm where a ship really was.'),
    ('Where does AIS spoofing happen?',
     'Interference with ship navigation is reported regularly in the Baltic, the Black Sea, the eastern Mediterranean '
     'and the Gulf, and has been recorded off major ports elsewhere, including Los Angeles and Long Beach in January 2026.'),
    ('What does Anopticon do about it?',
     'Anopticon verifies the positions ships report: each one is checked against what that ship can physically do and '
     'against other ships and independent sources, and the finding is published with the data behind it.'),
]

PAGES.append(dict(
    path='ais-spoofing/', crumbs=[('AIS spoofing', '/ais-spoofing/')], word='SPOOF',
    title='What is AIS spoofing? GNSS jamming explained | Anopticon',
    desc=('AIS spoofing and GNSS jamming explained: what they are, how they show up in ship-tracking data, how they are '
          'detected, and why forged ship positions poison everything built on them.'),
    h1='AIS spoofing', lede='How a ship comes to broadcast a position it is not in, and how to tell.',
    faq=FAQ,
    body='''
<section class="band band--white" aria-labelledby="ais-h">
  <div class="wrap duo">
    <h2 id="ais-h" class="h2 reveal">A radio beacon on every ship.</h2>
    <div class="prose reveal">
      <p>The Automatic Identification System makes every large ship broadcast its name, position, course and speed every few seconds on two VHF channels anyone can receive. Under the SOLAS convention it is carried by ships of 300 gross tonnage and upwards on international voyages, by cargo ships of 500 gross tonnage and upwards, and by all passenger ships.</p>
      <p>The position in each message comes from the ship&rsquo;s own satellite-navigation receiver. AIS repeats whatever that receiver believes.</p>
    </div>
  </div>
</section>

<section class="band band--black" aria-labelledby="ways-h">
  <div class="wrap">
    <h2 id="ways-h" class="h2 reveal">Three ways the beacon lies.</h2>
    <dl class="ways">
      <div class="reveal"><dt><span class="chip" data-flag="J"></span>Jamming</dt><dd>Noise drowns the satellite signal. The receiver loses its fix; positions freeze, drift or vanish.</dd></div>
      <div class="reveal"><dt><span class="chip" data-flag="Y"></span>Spoofing</dt><dd>A false signal replaces the real one. The receiver reports the wrong place with full confidence, often many ships at once, often on land.</dd></div>
      <div class="reveal"><dt><span class="chip" data-flag="X"></span>Forgery</dt><dd>The messages themselves are altered: a borrowed identity, a transponder switched off, a track that was never sailed.</dd></div>
    </dl>
  </div>
</section>

<section class="band band--white" aria-labelledby="tell-h">
  <div class="wrap duo">
    <h2 id="tell-h" class="h2 reveal">How you tell.</h2>
    <div class="prose reveal">
      <p><b>The hull.</b> A ship has a length, an engine and a top speed. A report that needs more than the hull can give did not happen as reported. Our <a href="/research/">research</a> measures how far ship physics can be trusted between sparse reports.</p>
      <p><b>The crowd.</b> One ship jumping is a fault. Forty ships jumping to one place is a pattern.</p>
      <p><b>A second witness.</b> Radar satellites see ships whether or not they broadcast. Where an image exists, it settles where the ship was.</p>
    </div>
  </div>
</section>
'''))

# ---------------------------------------------------------------------------------------------------------- ledger
PAGES.append(dict(
    path='ledger/', crumbs=[('Ledger', '/ledger/')], word='LEDGER',
    title='AIS spoofing incidents: the Interference Ledger | Anopticon',
    desc=('A public record of GNSS interference seen in ship AIS data: dates, ship counts, distances and reported speeds. '
          'Ships near Istanbul reported in Lima, Peru, 10 and 11 October 2026.'),
    h1='Ledger', lede='Interference events in ship position data, one entry per event, with where the evidence stops.',
    body='''
<section class="band band--white" aria-labelledby="e1-h">
  <article class="wrap">
    <h2 id="e1-h" class="h2 reveal">Lima, 10 October 2026</h2>
    <p class="lead reveal measure">Ships in the Bosphorus and the western Black Sea broadcast positions inside one 3&nbsp;km patch of inland Lima, Peru.</p>
    <table class="data reveal">
      <caption class="sr-only">Lima event, 10 October 2026</caption>
      <tbody>
        <tr><th scope="row">Ships</th><td>49</td><td>247 reports</td></tr>
        <tr><th scope="row">Window</th><td>12:00&ndash;18:34</td><td>UTC</td></tr>
        <tr class="is-false"><th scope="row">Reported at</th><td>Inland Lima</td><td>12.04&deg; S, 77.05&deg; W</td></tr>
        <tr><th scope="row">Really near</th><td>The Bosphorus</td><td>41.56&deg; N, 28.98&deg; E</td></tr>
        <tr><th scope="row">Apart</th><td>12,221 km</td><td>median, per ship</td></tr>
        <tr><th scope="row">Reported speed</th><td>94.9 kn</td><td>median; fastest 102.0</td></tr>
      </tbody>
    </table>
  </article>
</section>

<section class="band band--grey" aria-labelledby="e2-h">
  <article class="wrap">
    <h2 id="e2-h" class="h2 reveal">Lima, 11 October 2026</h2>
    <p class="lead reveal measure">The same patch, the next morning, shorter.</p>
    <table class="data reveal">
      <caption class="sr-only">Lima event, 11 October 2026</caption>
      <tbody>
        <tr><th scope="row">Ships</th><td>23</td><td>45 reports</td></tr>
        <tr><th scope="row">Window</th><td>10:41&ndash;11:15</td><td>UTC</td></tr>
        <tr><th scope="row">Apart</th><td>12,261 km</td><td>median, per ship</td></tr>
        <tr><th scope="row">Reported speed</th><td>94.9 kn</td><td>median; fastest 101.5</td></tr>
      </tbody>
    </table>
  </article>
</section>

<section class="band band--black" aria-labelledby="stop-h">
  <div class="wrap duo">
    <h2 id="stop-h" class="h2 reveal">Where it stops.</h2>
    <p class="lead reveal">The positions were moved, not sailed. The pattern fits interference with satellite navigation. It does not, on its own, show who or what caused it.</p>
  </div>
</section>
'''))

# --------------------------------------------------------------------------------------------------------- projects
PROJ = [('nereus', 'Nereus', 'Sea', 'Now'), ('argus', 'Argus', 'Watch', 'Next'), ('aether', 'Aether', 'Air', 'Later')]
PAGES.append(dict(
    path='projects/', crumbs=[('Projects', '/projects/')], word='SEA',
    title='Projects: Nereus, Argus and Aether | Anopticon',
    desc='Three projects on one question, is the reported position real: Nereus for the sea, Argus for those who watch it, Aether for the air.',
    h1='Projects', lede='One question, asked of every machine that reports where it is.',
    body='''
<section class="domains" aria-label="Projects">
''' + ''.join(f'  <a class="domain domain--{w.lower()}" href="/projects/{k}/"><span class="domain__word">{w}</span>'
              f'<span class="domain__name">{n}</span><span class="domain__when">{t}</span></a>\n' for k, n, w, t in PROJ) + '</section>\n'))


def project(key, name, word, when, title, desc, lede, img, h2, paras, nxt):
    fig = picture(img, 'print print--wide', lazy=False) if img else ''
    return dict(
        path=f'projects/{key}/', crumbs=[('Projects', '/projects/'), (name, f'/projects/{key}/')], word=name.upper(),
        title=title, desc=desc, h1=name, lede=lede,
        body=f'''
<section class="band band--white" aria-labelledby="{key}-h">
  <div class="wrap">
    {fig}
    <div class="duo duo--text">
      <h2 id="{key}-h" class="h2 reveal">{h2}</h2>
      <div class="prose reveal">{''.join(f'<p>{p}</p>' for p in paras)}<p class="status">{word}. {when}.</p></div>
    </div>
  </div>
</section>

<nav class="next" aria-label="Next project">
  <a class="domain domain--{nxt[2].lower()}" href="/projects/{nxt[0]}/"><span class="domain__word">{nxt[2]}</span><span class="domain__name">{nxt[1]}</span><span class="domain__when">Next project</span></a>
</nav>
''')


PAGES.append(project(
    'nereus', 'Nereus', 'Sea', 'Now',
    'Project Nereus: verifying ship positions at sea | Anopticon',
    'Project Nereus is Anopticon\'s work at sea: telling real ship positions from jammed, spoofed and forged ones, with the evidence to show it.',
    'Project Nereus: verifying the positions ships report at sea. Running now.', 'nereus', 'Hold on until it tells the truth.',
    ['Nereus, the old man of the sea, would answer any question, if you could hold him while he became a lion, a serpent, water. Heracles held on.',
     'Ship data changes shape the same way. Nereus is our work at sea: shipping, insurance and disputes, where a position has to be right.'],
    ('argus', 'Argus', 'Watch')))
PAGES.append(project(
    'argus', 'Argus', 'Watch', 'Next',
    'Project Argus: for navies and coast guards | Anopticon',
    'Project Argus brings Anopticon\'s ship-position verification to the navies and coast guards who watch the sea.',
    'Project Argus: ship-position verification for navies and coast guards. Next.', 'argus', 'A hundred eyes, and still fooled.',
    ['Argus Panoptes had a hundred eyes and never closed them all. Hermes lulled every one to sleep.',
     'Seeing everything is not the same as seeing what is true. Argus is for navies and coast guards, on the same core as Nereus.'],
    ('aether', 'Aether', 'Air')))
PAGES.append(project(
    'aether', 'Aether', 'Air', 'Later',
    'Project Aether: position verification in the air | Anopticon',
    'Project Aether takes the same question to the air: aircraft broadcast where they are, and that record can be poisoned too.',
    'Project Aether: the same question, asked of aircraft. Later.', 'bruegel', 'The sky reports too.',
    ['Aether is the bright upper air. In Bruegel\'s engraving a warship holds its course while Icarus falls out of the sky above it.',
     'Aircraft broadcast where they are as well, and that broadcast can be jammed and spoofed the same way. Aether takes the question up.'],
    ('nereus', 'Nereus', 'Sea')))

# --------------------------------------------------------------------------------------------------------- research
PAGES.append(dict(
    path='research/', crumbs=[('Research', '/research/')], word='DATA', schema_extra=[PAPER],
    title='Research: ship physics under sparse AIS sampling | Anopticon',
    desc=('What sparse AIS reports let ship manoeuvring and resistance models predict, identify and bound, measured on '
          '47.7 million reports from the Baltic and North Sea. Code and data on Zenodo.'),
    h1='Research', lede='The method in the open. The code for every number is public.',
    body=f'''
<section class="band band--white" aria-labelledby="p1-h">
  <div class="wrap duo">
    <div>
      <h2 id="p1-h" class="paper-title reveal">Ship manoeuvring and resistance models under sparse AIS sampling: what can be predicted, identified and bounded</h2>
      <p class="byline reveal">Vishmayraj Zala, Kathan Patel. Under review, 2026.</p>
      <p class="reveal"><a class="btn" href="{ZENODO}">Code and data on Zenodo</a></p>
    </div>
    <div class="prose reveal">
      <p>Shore stations see a ship only through AIS reports, seconds to minutes apart. We measured what those reports let ship physics predict, identify and bound: 47,739,929 reports from four networks over eleven days in the Baltic and North Sea, tested on held-out ships.</p>
      <table class="data data--plain">
        <caption class="sr-only">Findings</caption>
        <tbody>
          <tr><th scope="row">Turns</th><td>On course changes of 45&deg; or more, textbook turn models place the ship about 22% worse at the 95th percentile than averaging the two reports.</td></tr>
          <tr><th scope="row">Steering</th><td>A hull&rsquo;s steering constants can&rsquo;t be identified from AIS. It carries no rudder angle.</td></tr>
          <tr><th scope="row">Speed</th><td>A Holtrop&ndash;Mennen speed screen is crossed by 4 of 8,472 ships up to Froude number 0.45, and by 181 of 199 above it.</td></tr>
          <tr><th scope="row">So</th><td>Between sparse reports, ship physics is good for bounds, not for filling in the gaps.</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
'''))

# ------------------------------------------------------------------------------------------------------------- team
PAGES.append(dict(
    path='team/', crumbs=[('Team', '/team/')], word='CREW', schema_extra=PEOPLE,
    title='Team: Vishmayraj Zala and Kathan Patel | Anopticon',
    desc='Anopticon is built by Vishmayraj Zala, founder, and Kathan Patel, co-founder, from GTU-SET in Ahmedabad, Gujarat.',
    h1='Team', lede='Two founders from GTU-SET, Ahmedabad. We wrote the engine and the paper ourselves.',
    body=f'''
<section class="band band--white" id="vishmayraj-zala" aria-labelledby="vz-h">
  <div class="wrap duo">
    <div>
      <h2 id="vz-h" class="h2 reveal">Vishmayraj Zala</h2>
      <p class="lead reveal">Founder. Leads operations.</p>
    </div>
    <div class="reveal">
      <p>Builds real-time data systems. Google Summer of Code 2026 contributor with OSGeo. Corresponding author of our first paper.</p>
      <ul class="buttons">
        <li><a class="btn" href="https://github.com/Vishmayraj" rel="me">GitHub</a></li>
        <li><a class="btn" href="https://www.linkedin.com/in/vishmayraj-zala" rel="me">LinkedIn</a></li>
        <li><a class="btn" href="https://orcid.org/0009-0007-9796-9449" rel="me">ORCID</a></li>
        <li><a class="btn" href="mailto:{MAIL}">Email</a></li>
      </ul>
    </div>
  </div>
</section>

<section class="band band--black" id="kathan-patel" aria-labelledby="kp-h">
  <div class="wrap duo">
    <div>
      <h2 id="kp-h" class="h2 reveal">Kathan Patel</h2>
      <p class="lead reveal">Co-founder. Leads machine learning research.</p>
    </div>
    <div class="reveal">
      <p>Student researcher. Works on the data and on validating what the engine finds.</p>
      <ul class="buttons">
        <li><a class="btn btn--light" href="https://github.com/KathanPatel1310">GitHub</a></li>
        <li><a class="btn btn--light" href="https://www.linkedin.com/in/kathan-patel-0235a3354">LinkedIn</a></li>
      </ul>
    </div>
  </div>
</section>
'''))

# ------------------------------------------------------------------------------------------------------------ about
PAGES.append(dict(
    path='about/', crumbs=[('About', '/about/')], word='NAME',
    title='About Anopticon: what the name means',
    desc='Anopticon is the panopticon turned around: a watchtower the watched can look into. Why we chose the name, and how to say it.',
    h1='About', lede='The name, and why we picked it.',
    body='''
<section class="band band--white" aria-labelledby="name-h">
  <div class="wrap duo">
    <h2 id="name-h" class="h2 reveal">A watchtower with glass walls.</h2>
    <div class="prose reveal">
      <p>Bentham&rsquo;s panopticon is a prison with a tower in the middle: the guard sees every cell and no prisoner sees the guard. Take away the &ldquo;pan&rdquo; and you get Anopticon. We kept the tower and took out the secret. Whatever we conclude about a ship comes with the data and the method, so anyone can climb up and look.</p>
      <p>The word is older than the company. In 2009 a project in Venice used it to map the city&rsquo;s CCTV cameras. We are the maritime one.</p>
    </div>
  </div>
</section>

<section class="band band--black" aria-labelledby="say-h">
  <div class="wrap duo">
    <h2 id="say-h" class="h2 reveal">an-OP-ti-kon</h2>
    <p class="lead reveal">Four syllables, stress on the second. Founded in 2026, in Gujarat.</p>
  </div>
</section>
'''))

# ---------------------------------------------------------------------------------------------------------- contact
PAGES.append(dict(
    path='contact/', crumbs=[('Contact', '/contact/')], word='K',
    title='Contact Anopticon',
    desc='Write to Anopticon about pilots, research or press: vishmayraj@anopticon.com. Gujarat, India.',
    h1='Contact', lede='Flag K: I wish to communicate with you.',
    body=f'''
<section class="rows" aria-label="Contact details">
  <a class="row row--yellow" href="mailto:{MAIL}?subject=Anopticon"><span>vishmayraj@<wbr>anopticon.com</span><span class="arrow" aria-hidden="true">&rarr;</span></a>
  <a class="row" href="/team/#vishmayraj-zala"><span>Vishmayraj Zala, founder</span><span class="arrow" aria-hidden="true">&rarr;</span></a>
  <a class="row" href="/team/#kathan-patel"><span>Kathan Patel, co-founder</span><span class="arrow" aria-hidden="true">&rarr;</span></a>
  <div class="row"><span>Gujarat, India</span></div>
</section>
'''))

# ---------------------------------------------------------------------------------------------------------- shared
FONTS = 'https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;800&display=swap'


def nav(page):
    here = '/' + page['path']
    links = ''.join(f'<li><a href="{u}"{HERE if here.startswith(u) else ""}>{t}</a></li>' for u, t in NAV)
    cur = HERE if page['path'] == 'contact/' else ''
    return f'''<a class="skip" href="#main">Skip to content</a>
<nav class="nav{' nav--dark' if page.get('home') else ''}" aria-label="Main">
  <a class="nav__mark" href="/"><span class="nav__flags" data-hoist="AN" aria-hidden="true"></span>Anopticon</a>
  <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
  <ul class="nav__links" id="menu">{links}<li><a class="btn{' btn--light' if page.get('home') else ''}" href="/contact/"{cur}>Contact</a></li></ul>
</nav>
'''


def page_head(page):
    return f'''<header class="phead wrap">
  {hoist(page['word'], 'hoist hoist--page')}
  <h1 class="phead__h">{page['h1']}</h1>
  <p class="phead__lede">{page['lede']}</p>
</header>
'''


def faq_html(faq):
    items = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    return f'''
<section class="band band--grey" aria-labelledby="faq-h">
  <div class="wrap duo">
    <h2 id="faq-h" class="h2 reveal">Questions</h2>
    <div class="faq reveal">{items}</div>
  </div>
</section>

<section class="band band--white" aria-labelledby="src-h">
  <div class="wrap duo">
    <h2 id="src-h" class="h2 reveal">Sources</h2>
    <ul class="sources reveal">
      <li><a href="https://www.imo.org/en/OurWork/Safety/Pages/AIS.aspx">IMO: AIS transponders</a>, SOLAS chapter V carriage requirements</li>
      <li><a href="https://arxiv.org/abs/2602.16257">SeaSpoofFinder: potential GNSS spoofing event detection using AIS</a>, arXiv, 2026</li>
      <li><a href="https://insidegnss.com/?p=197021">LA/Long Beach VTIS records spoofing event in January 2026</a>, Inside GNSS</li>
      <li><a href="https://www.hellenicshippingnews.com/?p=1100977">Jamming and spoofing: responding to GNSS and AIS interference</a>, Hellenic Shipping News</li>
      <li><a href="/research/">Zala and Patel, ship physics under sparse AIS sampling</a>, 2026</li>
    </ul>
  </div>
</section>
'''


def footer(page):
    return f'''
<footer class="foot">
  <div class="wrap foot__k">
    <span class="chip chip--big" data-flag="K" aria-hidden="true"></span>
    <p class="foot__say"><b>Kilo.</b> I wish to communicate with you.</p>
    <a class="btn btn--yellow" href="mailto:{MAIL}?subject=Anopticon">{MAIL}</a>
  </div>
  <div class="wrap foot__cols">
    <p class="foot__what">{WHAT} AIS spoofing, GNSS jamming and forged positions, checked against what the ship can do.</p>
    <ul><li><a href="/ais-spoofing/">AIS spoofing</a></li><li><a href="/ledger/">Ledger</a></li><li><a href="/research/">Research</a></li></ul>
    <ul><li><a href="/projects/">Projects</a></li><li><a href="/team/">Team</a></li><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li></ul>
  </div>
  <p class="wrap foot__legal">&copy; {TODAY[:4]} Anopticon, Gujarat, India. Signal flags after the International Code of Signals. Pictures: Istanbul Painter (Louvre CA 823), W. H. Roscher (1890), after Bruegel (The Met); public domain.</p>
</footer>
<script src="/assets/flags.js" defer></script>
<script src="/assets/site.js" defer></script>
'''


def head(page):
    url = SITE + '/' + page['path']
    graph = list(page.get('schema', [ORG, WEBSITE])) + list(page.get('schema_extra', []))
    graph.append({'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': page['title'],
                  'description': page['desc'], 'isPartOf': {'@id': f'{SITE}/#site'},
                  'about': {'@id': f'{SITE}/#org'}, 'dateModified': TODAY, 'inLanguage': 'en'})
    if page['path']:
        graph.append(crumbs(page))
    if page.get('faq'):
        graph.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in page['faq']]})
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)
    t, d = html.escape(page['title']), html.escape(page['desc'])
    robots = page.get('robots', 'index, follow, max-image-preview:large')
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="{'#0A0A0A' if page.get('home') else '#FFFFFF'}">
<meta property="og:site_name" content="Anopticon">
<meta property="og:type" content="website">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Anopticon. Is that ship really there?">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{SITE}/assets/og.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">
{ld}
</script>
<script>document.documentElement.classList.add('js')</script>
</head>
<body class="{'home' if page.get('home') else 'inner'}">
'''


def render(page):
    body = page['body']
    if not page.get('home'):
        body = '<main id="main">\n' + page_head(page) + body + (faq_html(page['faq']) if page.get('faq') else '') + '</main>\n'
    return head(page) + nav(page) + body + footer(page) + '</body>\n</html>\n'


def build():
    for page in PAGES:
        out = OUT / page['path'] / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(page), encoding='utf-8', newline='\n')
        print('wrote', out.relative_to(ROOT))

    nf = dict(path='404/', word='N', h1='Not found', lede='Flag N: negative. Nothing at this address.',
              title='Not found | Anopticon', desc='Nothing at this address.', robots='noindex',
              body='<section class="band band--white"><p class="wrap"><a class="link" href="/">Back to the start</a></p></section>\n')
    (OUT / '404.html').write_text(render(nf), encoding='utf-8', newline='\n')
    print('wrote public/404.html')

    urls = ''.join(f'  <url><loc>{SITE}/{p["path"]}</loc><lastmod>{TODAY}</lastmod></url>\n' for p in PAGES)
    (OUT / 'sitemap.xml').write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n',
        encoding='utf-8', newline='\n')
    print('wrote public/sitemap.xml')


if __name__ == '__main__':
    build()
