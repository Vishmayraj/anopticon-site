"""Build anopticon.com into public/.

    python build.py

Pages are defined below. Every page gets the same head (title, description, canonical, Open Graph, JSON-LD), nav and
footer. Commit public/; Render serves it as it is.
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
WHAT = 'Anopticon tests what machines report against what the physical world allows.'

ORG = {
    '@type': 'Organization', '@id': f'{SITE}/#org', 'name': 'Anopticon', 'url': f'{SITE}/',
    'logo': {'@type': 'ImageObject', 'url': f'{SITE}/assets/icons/logo-512.png', 'width': 512, 'height': 512},
    'image': f'{SITE}/assets/og.png', 'email': MAIL,
    'description': ('Anopticon tests what machines report against what the physical world allows, and keeps independent '
                    'records anyone can check. It starts at sea: AIS spoofing, GNSS (GPS) jamming and falsified ship '
                    'positions, tested against what each ship can physically do and against independent sources. Then '
                    'navies and coast guards, then aircraft. Founded in 2026 in Gujarat, India.'),
    'disambiguatingDescription': ('The telemetry-integrity company at anopticon.com, starting with ship positions at sea. '
                                  'Not a general cybersecurity firm, and not the 2009 Venice CCTV-mapping project of the same name.'),
    'foundingDate': '2026', 'foundingLocation': {'@type': 'Place', 'name': 'Gujarat, India'},
    'knowsAbout': ['Telemetry integrity', 'AIS spoofing', 'GNSS jamming', 'GPS spoofing at sea', 'Automatic Identification System',
                   'Ship position verification', 'Maritime domain awareness', 'ADS-B'],
    'founder': [{'@id': f'{SITE}/team/#vishmayraj-zala'}, {'@id': f'{SITE}/team/#kathan-patel'}],
    'sameAs': ['https://github.com/Vishmayraj/anopticon-site'],
    'contactPoint': {'@type': 'ContactPoint', 'email': MAIL, 'contactType': 'sales', 'availableLanguage': 'English'},
}
WEBSITE = {'@type': 'WebSite', '@id': f'{SITE}/#site', 'url': f'{SITE}/', 'name': 'Anopticon',
           'alternateName': 'Anopticon, telemetry integrity', 'publisher': {'@id': f'{SITE}/#org'}, 'inLanguage': 'en'}
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

NAV = [('/ais-spoofing/', 'AIS spoofing'), ('/ledger/', 'Ledger'), ('/research/', 'Research'), ('/team/', 'Team'),
       ('/contact/', 'Contact')]
HERE = ' aria-current="page"'


def picture(src, w, h, alt, cap):
    return (f'<figure class="print reveal"><img src="{src}" width="{w}" height="{h}" alt="{html.escape(alt)}" '
            f'loading="lazy" decoding="async"><figcaption>{cap}</figcaption></figure>')


MYTH = {
    'home': ('/assets/img/hermes-vase.jpg', 1067, 1600, 'Black-figure vase: Hermes running, a ram on his shoulders.',
             'Hermes carried the messages of the gods. He was also the god of thieves.',
             'Hermes, black-figure oinochoe, Louvre F 159.'),
    'ais-spoofing/': ('/assets/img/ulysses-mast.jpg', 1000, 600, 'Painting: Ulysses tied to the mast of his ship, his crew rowing.',
                      'Ulysses had himself tied to the mast, so he could hear the Sirens and not steer for them.',
                      'Ulysses and the Sirens, Henri Lehmann, 1867, detail.'),
    'ledger/': ('/assets/img/cassandra.jpg', 843, 1056, 'Drawing: Cassandra raises her hand towards a burning city.',
                'Cassandra saw it coming and said so. We write it down.',
                'Cassandra before the burning city of Troy. Art Institute of Chicago.'),
    'research/': ('/assets/img/urania.jpg', 843, 1393, 'Engraving: Urania, muse of astronomy, holding a globe beside an armillary sphere.',
                  'Urania, the muse who measured the sky.',
                  'Urania, Johann Theodor de Bry, 1601. Art Institute of Chicago.'),
    'team/': ('/assets/img/argonauts.jpg', 1600, 642, 'Painted panel: scenes from the voyage of the Argonauts.',
              'Every crew starts small. The Argo had fifty.',
              'Scenes from the Story of the Argonauts, Biagio d&rsquo;Antonio, about 1465. The Met.'),
}


def myth(key):
    if key not in MYTH:
        return ''
    src, w, h, alt, line, cap = MYTH[key]
    return f'''
<section class="band myth" aria-label="Picture">
  <div class="wrap duo">
    <figure class="print reveal"><img src="{src}" width="{w}" height="{h}" alt="{html.escape(alt)}" loading="lazy" decoding="async"><figcaption>{cap}</figcaption></figure>
    <p class="lead reveal myth__line">{line}</p>
  </div>
</section>
'''


def crumbs(page):
    items = [('Anopticon', '/')] + page.get('crumbs', [])
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + u} for i, (n, u) in enumerate(items)]}


# ------------------------------------------------------------------------------------------------ the cases (home)
# Each drawing illustrates the case as reported; its lines draw themselves as you scroll.
PWNED = ('M40 270 L40 90 L160 90 L160 180 L40 180 L220 90 L250 270 L280 180 L310 270 L340 90 L400 270 L400 90 '
         'L520 270 L520 90 L700 90 L580 90 L580 270 L700 270 L580 180 L670 180 L760 90 L760 270 L850 270 L880 240 '
         'L880 120 L850 90 L760 90')


def la_art():
    out = []
    for k in range(7):
        y = 60 + k * 64
        x1 = 300 + k * 30
        jx, jy = 560 + (k * 47) % 220, 30 + ((k * 3) % 7) * 64
        out.append(f'  <path class="ink" d="M0 {y} L{x1} {y}" fill="none" stroke-width="5"/>\n'
                   f'  <path class="draw mk" d="M{x1} {y} L{jx} {jy}" fill="none" stroke-width="4"/>\n'
                   f'  <circle class="pop fillmk" data-at=".95" cx="{jx}" cy="{jy}" r="8"/>\n')
    return ('<svg viewBox="0 0 920 520" role="img" aria-label="Seven ship tracks in parallel lanes, each with a sudden jump">\n'
            + ''.join(out) + '  <text class="label" x="0" y="510">San Pedro Bay</text>\n</svg>')


ART = {
    'pwned': f'''<svg viewBox="0 0 920 360" role="img" aria-label="A ship's track that spells the word pwned">
  <path class="draw ink" d="{PWNED}" fill="none" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>
  <circle class="pop fillmk" data-at=".98" cx="760" cy="90" r="11"/>
  <text class="label" x="40" y="330">A fake ship, off Italy</text>
</svg>''',
    'reyes': '''<svg viewBox="0 0 920 520" role="img" aria-label="A coastline with a ship's track looping over the headland">
  <path class="land" d="M560 0 L920 0 L920 520 L640 520 C610 470 650 430 610 390 C570 350 520 380 500 340 C480 300 540 280 520 240 C500 200 440 210 450 170 C460 130 530 140 540 90 C548 50 520 30 560 0 Z"/>
  <path class="ink" d="M0 300 L300 300" fill="none" stroke-width="3" stroke-dasharray="6 8" style="opacity:.5"/>
  <path class="draw ink" d="M300 300 C300 200 470 170 560 210 C660 255 640 370 540 390 C430 410 300 380 300 300 Z" fill="none" stroke-width="7"/>
  <text class="label" x="0" y="285">from an oil terminal in Nigeria</text>
  <text class="label" x="640" y="160">Point Reyes</text>
</svg>''',
    'rings': '''<svg viewBox="0 0 920 560" role="img" aria-label="A river, and rings of reported positions on the land beside it">
  <path class="ink" d="M0 470 C180 430 300 500 460 460 C620 420 760 470 920 440" fill="none" stroke-width="44" style="opacity:.12"/>
  <path class="draw ink" d="M540 150 a60 60 0 1 0 120 0 a60 60 0 1 0 -120 0" fill="none" stroke-width="6" stroke-linecap="round"/>
  <path class="draw ink" d="M475 150 a125 125 0 1 0 250 0 a125 125 0 1 0 -250 0" fill="none" stroke-width="6" stroke-linecap="round"/>
  <path class="draw mk" d="M410 150 a190 190 0 1 0 380 0 a190 190 0 1 0 -380 0" fill="none" stroke-width="6" stroke-linecap="round"/>
  <text class="label" x="0" y="420">Huangpu river</text>
  <text class="label" x="760" y="40">east bank</text>
</svg>''',
    'la': la_art(),
    'lima': '''<svg viewBox="0 0 1000 500" role="img" aria-label="World map with a line from the Bosphorus to Lima, Peru">
  <path class="land" id="world" d=""/>
  <path class="draw ink" d="M580.5 136.1 Q 430 -20 286 283.4" fill="none" stroke-width="4"/>
  <circle class="fillfg" cx="580.5" cy="136.1" r="7"/>
  <circle class="pop fillfg" data-at=".97" cx="286" cy="283.4" r="11"/>
  <text class="label" x="596" y="128">Bosphorus</text>
  <text class="label" x="222" y="314">Lima</text>
</svg>''',
}

CASES = [
    ('pwned', 'white', 'October 2013. Off Italy.', 'A ship that never existed sailed the word &ldquo;pwned&rdquo;.',
     'Trend Micro researchers made it with a 700-euro radio. Public tracking maps showed it.',
     '<a href="https://www.technologyreview.com/2013/10/18/82918/ship-tracking-hack-makes-tankers-vanish-from-view/">MIT Technology Review</a>, 18 October 2013'),
    ('reyes', 'black', 'June 2019. Point Reyes, California.', 'A boat in Nigeria went round in circles over California.',
     'For two weeks, a crew boat in Nigeria broadcast a loop over Point Reyes. Part of it was on land.',
     '<a href="https://www.thelog.com/snw/ships-AIS-broadcasts-draw-GPS-crop-circles-thousands-of-miles-away-from-actual-locations/">The Log</a>, 28 August 2020'),
    ('rings', 'white', 'July 2019. Shanghai.', 'Rings on the riverbank.',
     'Ships near Shanghai showed up in rings on the bank of the Huangpu. Nobody has said who did it.',
     '<a href="https://www.technologyreview.com/2019/11/15/131940/ghost-ships-crop-circles-and-soft-gold-a-gps-mystery-in-shanghai/">MIT Technology Review</a>, 15 November 2019'),
    ('la', 'black', '29 January 2026. Los Angeles and Long Beach.', 'Seven ships jumped at once.',
     'During a GPS test, seven ships jumped across an area 100 miles wide. One went silent for nearly an hour.',
     '<a href="https://insidegnss.com/?p=197021">Inside GNSS</a>, 2026'),
    ('lima', 'orange', '10 October 2026. Lima, Peru.', 'Ships off Istanbul turned up in Peru.',
     'Forty-nine of them, in one 3&nbsp;km patch of inland Lima, 12,221&nbsp;km away. This one is ours.',
     '<a href="/ledger/">The entry in our ledger</a>'),
]


def case_html(c):
    key, tone, when, h, p, src = c
    return f'''<section class="case" data-tone="{tone}" aria-labelledby="case-{key}">
  <div class="wrap case__grid">
    <div>
      <p class="case__when reveal">{when}</p>
      <h2 class="case__h reveal" id="case-{key}">{h}</h2>
      <p class="case__p reveal">{p}</p>
      <p class="case__src reveal">{src}</p>
    </div>
    <div class="case__art" data-art>{ART[key]}</div>
  </div>
</section>
'''


PAGES = []

PAGES.append(dict(
    path='', home=True, tone='black',
    title='Anopticon | Telemetry integrity, starting at sea: AIS spoofing and GNSS jamming',
    desc=('Anopticon tests what machines report against what the physical world allows, starting with ships at sea. '
          'Real cases of AIS spoofing and GNSS jamming, from the 2013 "pwned" ship to the Lima pile-up of October 2026.'),
    schema=[ORG, WEBSITE] + PEOPLE,
    body=f'''<main id="main">
<header class="open wrap" data-tone="black">
  <h1 class="open__h">Ships that were not where they said.</h1>
  <div class="open__row">
    <p>{WHAT} We start with ships. Five times they were wrong:</p>
    <p class="open__count">2013 &middot; 2019 &middot; 2019 &middot; 2026 &middot; 2026</p>
  </div>
</header>
''' + myth('home') + ''.join(case_html(c) for c in CASES) + f'''
<section class="close" data-tone="black" aria-labelledby="close-h">
  <div class="wrap">
    <div class="close__grid">
      <h2 class="h2 reveal" id="close-h">Independent records of what actually happened.</h2>
      <div class="reveal">
        <p class="lead">Sea first, then navies, then the air. Send us the ship and the dates.</p>
        <p style="margin-top:24px"><a class="btn btn--solid" href="mailto:{MAIL}?subject=A%20ship%20to%20check">{MAIL}</a></p>
      </div>
    </div>
    <nav class="close__links" aria-label="More">
      <a href="/projects/"><span>Sea, then watch, then air</span><span>Projects</span></a>
      <a href="/ais-spoofing/"><span>How AIS spoofing works</span><span>Explainer</span></a>
      <a href="/ledger/"><span>The ledger</span><span>Our records</span></a>
      <a href="/research/"><span>Research</span><span>Paper, code, data</span></a>
      <a href="/team/"><span>Who we are</span><span>Two founders</span></a>
    </nav>
  </div>
</section>
</main>
'''))

FAQ = [
    ('What is AIS spoofing?',
     'A ship broadcasting a position or identity over AIS that is not real, because its satellite signal was faked or its messages were.'),
    ('What is the difference between GNSS jamming and spoofing?',
     'Jamming drowns the satellite signal, so positions freeze or vanish. Spoofing replaces it, so the ship reports the wrong place, confidently.'),
    ('Can AIS spoofing be detected?',
     'Often, from the data: speeds no hull can reach, or many ships in one impossible spot. Radar satellites can confirm the rest.'),
    ('Where does AIS spoofing happen?',
     'Regularly in the Baltic, the Black Sea, the eastern Mediterranean and the Gulf, and off ports such as Los Angeles in January 2026.'),
    ('What does Anopticon do?',
     'We test reported positions against what the ship can do and against other sources, and publish what we find with the data.'),
]

PAGES.append(dict(
    path='ais-spoofing/', crumbs=[('AIS spoofing', '/ais-spoofing/')],
    title='What is AIS spoofing? GNSS jamming explained | Anopticon',
    desc=('AIS spoofing and GNSS jamming explained: what they are, how they show up in ship-tracking data, how they are detected, '
          'and why false ship positions matter.'),
    h1='AIS spoofing', lede='How a ship ends up broadcasting a position it is not in, and how you can tell.', faq=FAQ,
    body='''
<section class="band" aria-labelledby="ais-h">
  <div class="wrap duo">
    <h2 id="ais-h" class="h2 reveal">What AIS is</h2>
    <div class="prose reveal">
      <p>Every few seconds a ship&rsquo;s AIS broadcasts its name, position and speed on open radio. The position comes from its satellite receiver, and nothing proves who sent it.</p>
    </div>
  </div>
</section>

<section class="band band--black" aria-labelledby="ways-h">
  <div class="wrap">
    <h2 id="ways-h" class="h2 reveal">Jamming, spoofing, forgery</h2>
    <dl class="ways">
      <div class="reveal"><dt>Jamming</dt><dd>Noise drowns the satellite signal. The receiver loses its fix and positions freeze, drift or vanish.</dd></div>
      <div class="reveal"><dt>Spoofing</dt><dd>A false signal replaces the real one. The receiver reports the wrong place, often many ships at once, often on land.</dd></div>
      <div class="reveal"><dt>Forgery</dt><dd>The messages themselves are made up or changed: a borrowed identity, a ship that does not exist, a track never sailed.</dd></div>
    </dl>
  </div>
</section>

<section class="band" aria-labelledby="tell-h">
  <div class="wrap duo">
    <h2 id="tell-h" class="h2 reveal">How to tell</h2>
    <div class="prose reveal">
      <p><b>The hull.</b> A report that needs more speed than the ship has did not happen.</p>
      <p><b>Other ships.</b> One ship jumping is a fault. Forty is interference.</p>
      <p><b>A second source.</b> Radar satellites see ships that do not broadcast.</p>
    </div>
  </div>
</section>
'''))

PAGES.append(dict(
    path='ledger/', crumbs=[('Ledger', '/ledger/')],
    title='AIS spoofing incidents: the Anopticon ledger',
    desc=('Interference events we have recorded in ship AIS data, with dates, ship counts, distances and reported speeds. '
          'Ships near Istanbul reported in Lima, Peru, 10 and 11 October 2026.'),
    h1='Ledger', lede='Events we have recorded ourselves. One entry each, and a note on what the data cannot show.',
    body='''
<section class="band" aria-labelledby="e1-h">
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
    <h2 id="stop-h" class="h2 reveal">What it does not show</h2>
    <p class="lead reveal">The positions were moved, not sailed, and the pattern fits interference with satellite navigation. The data alone does not say who or what did it.</p>
  </div>
</section>
'''))

PAGES.append(dict(
    path='projects/', crumbs=[('Projects', '/projects/')],
    title='Projects: Nereus, Argus and Aether | Anopticon',
    desc='One core, one domain at a time: Nereus for ships at sea, Argus for navies and coast guards, Aether for aircraft.',
    h1='Projects', lede='One core: test what a machine reports against what the physical world allows. One domain at a time.',
    body='''
<section class="band" aria-label="Projects">
  <div class="wrap close__links" style="margin-top:0">
    <a href="/projects/nereus/"><span>Nereus. Ships at sea.</span><span>Now</span></a>
    <a href="/projects/argus/"><span>Argus. Navies and coast guards.</span><span>Next</span></a>
    <a href="/projects/aether/"><span>Aether. Aircraft.</span><span>Later</span></a>
  </div>
</section>
'''))


OTHERS = [('nereus', 'Nereus', 'Ships at sea', 'Now'), ('argus', 'Argus', 'Navies and coast guards', 'Next'),
          ('aether', 'Aether', 'Aircraft', 'Later')]


def project(key, name, title, desc, lede, img, paras):
    return dict(
        path=f'projects/{key}/', crumbs=[('Projects', '/projects/'), (name, f'/projects/{key}/')],
        title=title, desc=desc, h1=name, lede=lede,
        body=f'''
<section class="band" aria-labelledby="{key}-h">
  <div class="wrap duo">
    {picture(*img)}
    <div class="prose reveal"><h2 id="{key}-h" class="sr-only">{name}</h2>{''.join(f'<p>{p}</p>' for p in paras)}</div>
  </div>
</section>

<section class="close" aria-label="Other projects">
  <div class="wrap close__links" style="margin-top:0">{''.join(f'<a href="/projects/{k}/"><span>{n}. {w}.</span><span>{t}</span></a>' for k, n, w, t in OTHERS if k != key)}
    <a href="/projects/"><span>All projects</span><span>Projects</span></a>
  </div>
</section>
''')


PAGES.append(project(
    'nereus', 'Nereus', 'Project Nereus: checking ship positions at sea | Anopticon',
    'Project Nereus is our work at sea: telling real ship positions from jammed, spoofed and forged ones.',
    'Ships at sea. What we are doing now.',
    ('/assets/img/nereus-lekythos.jpg', 1600, 1285,
     "Black-figure painting on an oil jar: Heracles grips Nereus, who has a fish's tail and a lion springing from his back.",
     'Heracles and Nereus. Lekythos by the Istanbul Painter, about 590 BC. Louvre, CA 823.'),
    ['In the Greek story, Nereus would answer any question if you could hold on to him while he changed shape. Heracles held on.',
     'Nereus is our work at sea: shipping, insurance and disputes, where someone needs to know where a ship actually was.']))
PAGES.append(project(
    'argus', 'Argus', 'Project Argus: for navies and coast guards | Anopticon',
    'Project Argus takes our ship-position checks to the navies and coast guards who watch the sea.',
    'Navies and coast guards. Next.',
    ('/assets/img/argus-vase.jpg', 1090, 430,
     'Line drawing from a Greek vase: Hermes strikes Argus, whose body is covered in eyes.',
     'Hermes kills Argus. Drawing after an Athenian red-figure vase, W. H. Roscher, 1890.'),
    ['Argus had a hundred eyes, and Hermes still got past him.',
     'Argus is for the people whose job is watching the sea, built on the same core as Nereus.']))
PAGES.append(project(
    'aether', 'Aether', 'Project Aether: position checks for aircraft | Anopticon',
    'Project Aether asks the same question of aircraft, which broadcast their positions too.',
    'Aircraft. Later.',
    ('/assets/img/aether-icarus.jpg', 1600, 1228,
     'Engraving of an armed three-masted ship under sail; in the sky, Icarus falls from the sun.',
     'Armed three-master with Daedalus and Icarus in the sky. After Pieter Bruegel the Elder, 1561&ndash;65. The Met.'),
    ['Aircraft broadcast where they are as well, and those broadcasts get jammed and spoofed in the same way.',
     'Aether is that work, once the sea is done properly.']))

PAGES.append(dict(
    path='research/', crumbs=[('Research', '/research/')], schema_extra=[PAPER],
    title='Research: ship physics under sparse AIS sampling | Anopticon',
    desc=('What sparse AIS reports let ship manoeuvring and resistance models predict, identify and bound, measured on 47.7 million '
          'reports from the Baltic and North Sea. Code and data on Zenodo.'),
    h1='Research', lede='The method is public, and so is the code behind every number.',
    body=f'''
<section class="band" aria-labelledby="p1-h">
  <div class="wrap duo">
    <div>
      <h2 id="p1-h" class="paper-title reveal">Ship manoeuvring and resistance models under sparse AIS sampling: what can be predicted, identified and bounded</h2>
      <p class="byline reveal">Vishmayraj Zala, Kathan Patel. Under review, 2026.</p>
      <p class="reveal"><a class="btn" href="{ZENODO}">Code and data on Zenodo</a></p>
    </div>
    <div class="prose reveal">
      <p>What can AIS reports, seconds to minutes apart, tell ship physics? We measured it on 47.7 million reports and ships the models had not seen.</p>
      <table class="data data--plain">
        <caption class="sr-only">Findings</caption>
        <tbody>
          <tr><th scope="row">Turns</th><td>On course changes of 45&deg; or more, standard turn models place the ship about 22% worse at the 95th percentile than simply averaging the two reports.</td></tr>
          <tr><th scope="row">Steering</th><td>A hull&rsquo;s steering constants can&rsquo;t be identified from AIS, because AIS carries no rudder angle.</td></tr>
          <tr><th scope="row">Speed</th><td>A Holtrop&ndash;Mennen speed screen is crossed by 4 of 8,472 ships up to Froude number 0.45, and by 181 of 199 above it.</td></tr>
          <tr><th scope="row">So</th><td>Between sparse reports, ship physics is good for bounds, not for filling in the gaps.</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
'''))

PAGES.append(dict(
    path='team/', crumbs=[('Team', '/team/')], schema_extra=PEOPLE,
    title='Team: Vishmayraj Zala and Kathan Patel | Anopticon',
    desc='Anopticon is Vishmayraj Zala, founder, and Kathan Patel, co-founder, from GTU-SET in Ahmedabad, Gujarat.',
    h1='Team', lede='Two founders from GTU-SET, Ahmedabad. We built the engine and wrote the paper ourselves.',
    body=f'''
<section class="band" id="vishmayraj-zala" aria-labelledby="vz-h">
  <div class="wrap duo">
    <div>
      <h2 id="vz-h" class="h2 reveal">Vishmayraj Zala</h2>
      <p class="lead reveal">Founder. Runs operations.</p>
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
      <p>Student researcher. Works on the data and on checking what the engine finds.</p>
      <ul class="buttons">
        <li><a class="btn" href="https://github.com/KathanPatel1310">GitHub</a></li>
        <li><a class="btn" href="https://www.linkedin.com/in/kathan-patel-0235a3354">LinkedIn</a></li>
      </ul>
    </div>
  </div>
</section>
'''))

PAGES.append(dict(
    path='about/', crumbs=[('About', '/about/')],
    title='About Anopticon: what we believe and what the name means',
    desc='When something does not make sense, ask why. What Anopticon believes, how it works, and why it is called Anopticon.',
    h1='About', lede='When something does not make sense, ask why.',
    body='''
<section class="band" aria-labelledby="name-h">
  <div class="wrap duo">
    <h2 id="name-h" class="h2 reveal">Why Anopticon</h2>
    <div class="prose reveal">
      <p>The panopticon is a prison where one hidden guard sees everyone. Take away the &ldquo;pan&rdquo;: the tower stays, but anyone can look inside.</p>
    </div>
  </div>
</section>

<section class="band band--black" aria-labelledby="how-h">
  <div class="wrap duo">
    <h2 id="how-h" class="h2 reveal">Question. Investigate. Verify.</h2>
    <div class="prose reveal">
      <p>Ships, aircraft and sensors all report where they are. More of those reports are wrong, and few people check.</p>
      <p>We test each report against what the world allows, and hand over the data so anyone can check us.</p>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="say-h">
  <div class="wrap duo">
    <h2 id="say-h" class="h2 reveal">an-OP-ti-kon</h2>
    <p class="lead reveal">Stress on the second syllable. Founded in 2026, in Gujarat. <a class="link" href="/projects/">Projects</a></p>
  </div>
</section>
'''))

PAGES.append(dict(
    path='contact/', crumbs=[('Contact', '/contact/')],
    title='Contact Anopticon',
    desc='Write to Anopticon about a ship to check, research or press: vishmayraj@anopticon.com. Gujarat, India.',
    h1='Contact', lede='A ship to check, a question, a story. Send the ship and the dates if you have them.',
    body=f'''
<section class="rows" aria-label="Contact details">
  <a class="row row--orange" href="mailto:{MAIL}?subject=Anopticon"><span>vishmayraj@<wbr>anopticon.com</span><span aria-hidden="true">&rarr;</span></a>
  <a class="row" href="/team/#vishmayraj-zala"><span>Vishmayraj Zala, founder</span><span aria-hidden="true">&rarr;</span></a>
  <a class="row" href="/team/#kathan-patel"><span>Kathan Patel, co-founder</span><span aria-hidden="true">&rarr;</span></a>
  <div class="row"><span>Gujarat, India</span></div>
</section>
'''))

# ---------------------------------------------------------------------------------------------------------- shared
FONTS = 'https://fonts.googleapis.com/css2?family=Martian+Mono:wght@400;600&family=Schibsted+Grotesk:wght@400;600;800&display=swap'


def nav(page):
    here = '/' + page['path']
    links = ''.join(f'<li><a href="{u}"{HERE if here.startswith(u) else ""}>{t}</a></li>' for u, t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<nav class="nav" aria-label="Main">
  <a class="nav__mark" href="/">Anopticon</a>
  <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
  <ul class="nav__links" id="menu">{links}</ul>
</nav>
'''


def page_head(page):
    return f'''<header class="phead wrap">
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

<section class="band" aria-labelledby="src-h">
  <div class="wrap duo">
    <h2 id="src-h" class="h2 reveal">Sources</h2>
    <ul class="sources reveal">
      <li><a href="https://www.imo.org/en/OurWork/Safety/Pages/AIS.aspx">IMO: AIS transponders</a>, SOLAS chapter V carriage requirements</li>
      <li><a href="https://www.technologyreview.com/2013/10/18/82918/ship-tracking-hack-makes-tankers-vanish-from-view/">Ship-tracking hack makes tankers vanish from view</a>, MIT Technology Review, 2013</li>
      <li><a href="https://arxiv.org/abs/2602.16257">SeaSpoofFinder: potential GNSS spoofing event detection using AIS</a>, arXiv, 2026</li>
      <li><a href="https://insidegnss.com/?p=197021">LA/Long Beach VTIS records spoofing event in January 2026</a>, Inside GNSS</li>
      <li><a href="/research/">Zala and Patel, ship physics under sparse AIS sampling</a>, 2026</li>
    </ul>
  </div>
</section>
'''


def footer(page):
    world = '<script src="/assets/world.js" defer></script>\n' if page.get('home') else ''
    return f'''
<footer class="foot">
  <div class="wrap foot__grid">
    <p class="foot__what">{WHAT} Ships at sea now; navies and coast guards next; aircraft after. <a href="mailto:{MAIL}">{MAIL}</a></p>
    <ul><li><a href="/ais-spoofing/">AIS spoofing</a></li><li><a href="/ledger/">Ledger</a></li><li><a href="/research/">Research</a></li></ul>
    <ul><li><a href="/projects/">Projects</a></li><li><a href="/team/">Team</a></li><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li></ul>
  </div>
  <p class="wrap foot__legal">&copy; {TODAY[:4]} Anopticon, Gujarat, India. Sources are linked on each page; pictures are public domain.</p>
</footer>
{world}<script src="/assets/site.js" defer></script>
'''


def head(page):
    url = SITE + '/' + page['path']
    graph = list(page.get('schema', [ORG, WEBSITE])) + list(page.get('schema_extra', []))
    graph.append({'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': page['title'], 'description': page['desc'],
                  'isPartOf': {'@id': f'{SITE}/#site'}, 'about': {'@id': f'{SITE}/#org'}, 'dateModified': TODAY, 'inLanguage': 'en'})
    if page['path']:
        graph.append(crumbs(page))
    if page.get('faq'):
        graph.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in page['faq']]})
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)
    t, d = html.escape(page['title']), html.escape(page['desc'])
    robots = page.get('robots', 'index, follow, max-image-preview:large')
    tone = page.get('tone', 'white')
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="{'#0A0A0A' if tone == 'black' else '#FFFFFF'}">
<meta property="og:site_name" content="Anopticon">
<meta property="og:type" content="website">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Anopticon. Ships that were not where they said.">
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
<body data-tone="{tone}">
'''


def render(page):
    body = page['body']
    if not page.get('home'):
        body = '<main id="main">\n' + page_head(page) + myth(page['path']) + body + (faq_html(page['faq']) if page.get('faq') else '') + '</main>\n'
    return head(page) + nav(page) + body + footer(page) + '</body>\n</html>\n'


def build():
    for page in PAGES:
        out = OUT / page['path'] / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(page), encoding='utf-8', newline='\n')
        print('wrote', out.relative_to(ROOT))
    nf = dict(path='404/', h1='Not here', lede='Nothing at this address. <a class="link" href="/">Back to the start</a>',
              title='Not found | Anopticon', desc='Nothing at this address.', robots='noindex', body='')
    (OUT / '404.html').write_text(render(nf), encoding='utf-8', newline='\n')
    print('wrote public/404.html')
    urls = ''.join(f'  <url><loc>{SITE}/{p["path"]}</loc><lastmod>{TODAY}</lastmod></url>\n' for p in PAGES)
    (OUT / 'sitemap.xml').write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n',
        encoding='utf-8', newline='\n')
    print('wrote public/sitemap.xml')


if __name__ == '__main__':
    build()
