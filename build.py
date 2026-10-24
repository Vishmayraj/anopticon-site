"""Build anopticon.com into public/.

    python build.py

Pages are defined below. Every page opens on a full-screen painting and gets the same head (title, description,
canonical, Open Graph, JSON-LD), nav and footer. Commit public/; Render serves it as it is.
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

# What Anopticon is, in one sentence. Used in every footer, the schema and llms.txt.
WHAT = 'Anopticon tests what machines report against what the physical world allows, using data that already exists.'

ORG = {
    '@type': 'Organization', '@id': f'{SITE}/#org', 'name': 'Anopticon', 'url': f'{SITE}/',
    'logo': {'@type': 'ImageObject', 'url': f'{SITE}/assets/icons/logo-512.png', 'width': 512, 'height': 512},
    'image': f'{SITE}/assets/og.png', 'email': MAIL, 'slogan': 'Built on what is already there.',
    'description': ('Anopticon tests what machines report against what the physical world allows. It uses data that '
                    'already exists, such as public AIS ship broadcasts, satellite radar, weather records and physics, and '
                    'no custom sensors or surveillance hardware. It starts with ship positions at sea (AIS spoofing, GNSS '
                    'jamming, forged tracks), then navies and coast guards, then aircraft. Founded in 2026 in Gujarat, India.'),
    'disambiguatingDescription': ('The company at anopticon.com that checks machine-reported positions using open and '
                                  'existing data. Not a cybersecurity firm, not a hardware or surveillance company, and not '
                                  'the 2009 Venice CCTV-mapping project of the same name.'),
    'foundingDate': '2026', 'foundingLocation': {'@type': 'Place', 'name': 'Gujarat, India'},
    'knowsAbout': ['Telemetry integrity', 'Open data', 'AIS spoofing', 'GNSS jamming', 'GPS spoofing at sea',
                   'Automatic Identification System', 'Satellite radar', 'Ship position verification', 'ADS-B'],
    'founder': [{'@id': f'{SITE}/team/#vishmayraj-zala'}, {'@id': f'{SITE}/team/#kathan-patel'}],
    'sameAs': ['https://github.com/Vishmayraj/anopticon-site'],
    'contactPoint': {'@type': 'ContactPoint', 'email': MAIL, 'contactType': 'sales', 'availableLanguage': 'English'},
}
WEBSITE = {'@type': 'WebSite', '@id': f'{SITE}/#site', 'url': f'{SITE}/', 'name': 'Anopticon',
           'alternateName': 'Anopticon, built on what is already there', 'publisher': {'@id': f'{SITE}/#org'},
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

NAV = [('/projects/', 'Projects'), ('/ledger/', 'Ledger'), ('/research/', 'Research'), ('/team/', 'Team'),
       ('/questions/', 'Questions'), ('/contact/', 'Contact')]
HERE = ' aria-current="page"'

# ------------------------------------------------------------------------------------------------- the paintings
# key: (widths available as webp, the jpg fallback width, alt text, credit, focal point desktop, focal point phone)
BG = {
    'home': ((960, 1600, 2560), 1600, 'Painting: Ulysses tied to the mast of his ship while the Sirens, women with the bodies of birds, swoop around it.',
             'Ulysses and the Sirens, John William Waterhouse, 1891', '62% 40%', '63% 45%'),
    'projects': ((960, 1600, 2560), 1600, 'Engraving: a heavily armed sailing ship at sea; in the sky, Icarus falls from the sun.',
                 'Armed three-master with Daedalus and Icarus in the sky, after Pieter Bruegel the Elder, 1561&ndash;65', '50% 55%', '42% 50%'),
    'nereus': ((960, 1600), 1600, "Black-figure vase painting: Heracles grips Nereus, who has a fish's tail and a lion springing from his back.",
               'Heracles and Nereus, lekythos by the Istanbul Painter, about 590 BC, Louvre CA 823', '55% 55%', '58% 50%'),
    'argus': ((960, 1600, 2560), 1600, 'Painting: Mercury creeps up on Argus, who has fallen asleep against a rock, a cow behind them.',
              'Mercury and Argus, Diego Vel&aacute;zquez, 1659, Museo del Prado', '50% 50%', '30% 50%'),
    'aether': ((960, 1600), 1600, 'Engraving detail: Icarus falls out of the sun while Daedalus flies on.',
               'Detail, after Pieter Bruegel the Elder, 1561&ndash;65', '50% 35%', '50% 30%'),
    'ledger': ((960, 1600, 2560), 1600, 'Ink drawing: Cassandra raises her hand towards a burning city.',
               'Cassandra before the burning city of Troy, Art Institute of Chicago', '50% 40%', '30% 45%'),
    'research': ((960, 1600), 1600, 'Engraving: Urania, muse of astronomy, holding a globe beside an armillary sphere.',
                 'Urania, Johann Theodor de Bry, 1601, Art Institute of Chicago', '50% 30%', '50% 30%'),
    'team': ((960, 1600, 2560), 1600, 'Painted panel: scenes from the voyage of the Argonauts, with their ship at harbour.',
             'Scenes from the Story of the Argonauts, Biagio d&rsquo;Antonio, about 1465, The Met', '40% 50%', '12% 50%'),
    'questions': ((960, 1600, 2560), 1600, 'Black-figure vase: Hermes running, a ram on his shoulders.',
                  'Hermes, black-figure oinochoe, Louvre F 159', '50% 45%', '50% 45%'),
    'about': ((960,), 960, 'Line drawing from a Greek vase: Hermes strikes Argus, whose body is covered in eyes.',
              'Hermes kills Argus, after an Athenian red-figure vase, W. H. Roscher, 1890', '50% 50%', '45% 50%'),
}
BG['contact'] = BG['home']


def hero(key, h1, line, home=False, extra=''):
    widths, fb, alt, cred, pos, posm = BG[key]
    name = 'home' if key == 'contact' else key
    srcset = ', '.join(f'/assets/bg/{name}-{w}.webp {w}w' for w in widths)
    cls = 'hero hero--home' if home else 'hero'
    return f'''<header class="{cls}" style="--pos:{pos};--pos-m:{posm}">
  <picture><source type="image/webp" srcset="{srcset}" sizes="100vw"><img src="/assets/bg/{name}-{fb}.jpg" alt="{html.escape(alt)}" fetchpriority="high" decoding="async"></picture>
  <div class="hero__text wrap">
    <h1 class="hero__h">{h1}</h1>
    <p class="hero__line">{line}</p>{extra}
  </div>
  <p class="hero__credit">{cred}</p>
</header>
'''


def crumbs(page):
    items = [('Anopticon', '/')] + page.get('crumbs', [])
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + u} for i, (n, u) in enumerate(items)]}


def rows(items, cls='rows'):
    return f'<nav class="{cls}" aria-label="Pages">' + ''.join(
        f'<a href="{u}"><span>{a}</span><span>{b}</span></a>' for u, a, b in items) + '</nav>'


PWNED = ('M40 270 L40 90 L160 90 L160 180 L40 180 L220 90 L250 270 L280 180 L310 270 L340 90 L400 270 L400 90 '
         'L520 270 L520 90 L700 90 L580 90 L580 270 L700 270 L580 180 L670 180 L760 90 L760 270 L850 270 L880 240 '
         'L880 120 L850 90 L760 90')

PROJ = [('nereus', 'Nereus', 'Ships at sea', 'Now'), ('argus', 'Argus', 'Navies and coast guards', 'Next'),
        ('aether', 'Aether', 'Aircraft', 'Later')]

PAGES = []

# ------------------------------------------------------------------------------------------------------------ home
PAGES.append(dict(
    path='', bg='home', home=True,
    title='Anopticon | Built on what is already there',
    desc=('Anopticon tests what machines report against what the physical world allows, using data that already exists. '
          'No custom hardware. Ship positions first, then navies and coast guards, then aircraft.'),
    schema=[ORG, WEBSITE] + PEOPLE,
    h1='Anopticon', line='Built on what is already there.',
    extra=rows([(u, t, '') for u, t in NAV], 'rows rows--home'),
    body=''))

# -------------------------------------------------------------------------------------------------------- projects
PAGES.append(dict(
    path='projects/', bg='projects', crumbs=[('Projects', '/projects/')],
    title='Projects: Nereus, Argus and Aether | Anopticon',
    desc='One test, one domain at a time: Nereus for ships at sea, Argus for navies and coast guards, Aether for aircraft.',
    h1='Projects', line='One test, one domain at a time.',
    body=f'<section class="band"><div class="wrap">{rows([(f"/projects/{k}/", f"{n}. {w}.", t) for k, n, w, t in PROJ])}</div></section>\n'))


def project(key, title, desc, line, blocks):
    k, n, w, t = next(p for p in PROJ if p[0] == key)
    others = [(f'/projects/{a}/', f'{b}. {c}.', d) for a, b, c, d in PROJ if a != key] + [('/projects/', 'All projects', '')]
    body = '<section class="band"><div class="wrap">' + ''.join(
        f'<div class="pair reveal"><h2>{h}</h2><p>{p}</p></div>' for h, p in blocks) + '</div></section>\n'
    body += f'<section class="band band--end"><div class="wrap">{rows(others)}</div></section>\n'
    return dict(path=f'projects/{key}/', bg=key, crumbs=[('Projects', '/projects/'), (n, f'/projects/{key}/')],
                title=title, desc=desc, h1=n, line=line, body=body)


PAGES.append(project(
    'nereus', 'Project Nereus: ship positions at sea | Anopticon',
    'Project Nereus checks ship positions at sea against what each hull can do and what radar satellites saw.',
    'Ships at sea. Running now.',
    [('The story', 'Nereus answered any question truthfully, if you could hold on while he changed shape.'),
     ('What it checks', 'AIS positions, against what the hull could have done and what radar satellites saw.'),
     ('For', 'Charterers, owners, insurers, lawyers. Anyone who has to know where a ship really was.')]))
PAGES.append(project(
    'argus', 'Project Argus: for navies and coast guards | Anopticon',
    'Project Argus finds ships that go dark, meet at sea or borrow an identity, from radar and radio already in orbit.',
    'Navies and coast guards. Next.',
    [('The story', 'Argus had a hundred eyes. Mercury put every one of them to sleep.'),
     ('What it checks', 'Ships that go dark, meet at sea or borrow an identity, from radar and radio already in orbit.')]))
PAGES.append(project(
    'aether', 'Project Aether: for aircraft | Anopticon',
    'Project Aether asks the same question of aircraft, which broadcast their positions and get jammed and spoofed too.',
    'Aircraft. Later.',
    [('The story', 'Icarus trusted the wings he was given, and flew too close to the sun.'),
     ('What it checks', 'Aircraft broadcast where they are as well, and get jammed and spoofed the same way.')]))

# ---------------------------------------------------------------------------------------------------------- ledger
PAGES.append(dict(
    path='ledger/', bg='ledger', crumbs=[('Ledger', '/ledger/')],
    title='Ledger: GNSS interference events in ship data | Anopticon',
    desc=('Interference events recorded in ship AIS data, with dates, ship counts, distances and reported speeds. Ships near '
          'Istanbul reported in Lima, Peru, 10 and 11 October 2026.'),
    h1='Ledger', line='Interference, written down.',
    body='''
<section class="band" aria-labelledby="e1-h">
  <article class="wrap">
    <h2 id="e1-h" class="h2 reveal">Lima, 10 October 2026</h2>
    <p class="lead reveal">Ships in the Bosphorus reported positions in one 3&nbsp;km patch of inland Peru.</p>
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
<section class="band" aria-labelledby="e2-h">
  <article class="wrap">
    <h2 id="e2-h" class="h2 reveal">Lima, 11 October 2026</h2>
    <p class="lead reveal">The same patch, the next morning.</p>
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
<section class="band band--end" aria-labelledby="stop-h">
  <div class="wrap pair reveal"><h2 id="stop-h">Where it stops</h2><p>Moved, not sailed. The pattern fits satellite-navigation interference; the data alone does not say who did it.</p></div>
</section>
'''))

# -------------------------------------------------------------------------------------------------------- research
PAGES.append(dict(
    path='research/', bg='research', crumbs=[('Research', '/research/')], schema_extra=[PAPER],
    title='Research: ship physics under sparse AIS sampling | Anopticon',
    desc=('What sparse AIS reports let ship manoeuvring and resistance models predict, identify and bound, measured on 47.7 '
          'million reports from the Baltic and North Sea. Code and data on Zenodo.'),
    h1='Research', line='How far ship physics holds between two AIS reports.',
    body=f'''
<section class="band" aria-labelledby="p1-h">
  <div class="wrap">
    <h2 id="p1-h" class="paper-title reveal">Ship manoeuvring and resistance models under sparse AIS sampling: what can be predicted, identified and bounded</h2>
    <p class="byline reveal">Vishmayraj Zala, Kathan Patel. Under review, 2026. 47,739,929 reports, Baltic and North Sea.</p>
    <table class="data data--plain reveal">
      <caption class="sr-only">Findings</caption>
      <tbody>
        <tr><th scope="row">Turns</th><td>On sharp turns, textbook models place the ship about 22% worse than averaging the two reports.</td></tr>
        <tr><th scope="row">Steering</th><td>A hull&rsquo;s steering constants cannot be read from AIS. It carries no rudder angle.</td></tr>
        <tr><th scope="row">Speed</th><td>4 of 8,472 ships cross a Holtrop&ndash;Mennen speed screen up to Froude number 0.45.</td></tr>
        <tr><th scope="row">So</th><td>Between sparse reports, physics is good for bounds, not for filling gaps.</td></tr>
      </tbody>
    </table>
    <p class="reveal" style="margin-top:32px"><a class="btn" href="{ZENODO}">Code and data on Zenodo</a></p>
  </div>
</section>
'''))

# ------------------------------------------------------------------------------------------------------------ team
PAGES.append(dict(
    path='team/', bg='team', crumbs=[('Team', '/team/')], schema_extra=PEOPLE,
    title='Team: Vishmayraj Zala and Kathan Patel | Anopticon',
    desc='Anopticon was founded by Vishmayraj Zala and Kathan Patel, from GTU-SET in Ahmedabad, Gujarat.',
    h1='Team', line='Two founders. Gujarat, India.',
    body=f'''
<section class="band" id="vishmayraj-zala" aria-labelledby="vz-h">
  <div class="wrap person reveal">
    <h2 id="vz-h">Vishmayraj Zala</h2>
    <p>Founder. Real-time data systems; Google Summer of Code 2026 with OSGeo; author of the engine and the first paper.</p>
    <ul class="buttons">
      <li><a class="btn" href="https://github.com/Vishmayraj" rel="me">GitHub</a></li>
      <li><a class="btn" href="https://www.linkedin.com/in/vishmayraj-zala" rel="me">LinkedIn</a></li>
      <li><a class="btn" href="https://orcid.org/0009-0007-9796-9449" rel="me">ORCID</a></li>
      <li><a class="btn" href="mailto:{MAIL}">Email</a></li>
    </ul>
  </div>
</section>
<section class="band band--end" id="kathan-patel" aria-labelledby="kp-h">
  <div class="wrap person reveal">
    <h2 id="kp-h">Kathan Patel</h2>
    <p>Co-founder. Machine learning research; the data, and checking what the engine finds.</p>
    <ul class="buttons">
      <li><a class="btn" href="https://github.com/KathanPatel1310">GitHub</a></li>
      <li><a class="btn" href="https://www.linkedin.com/in/kathan-patel-0235a3354">LinkedIn</a></li>
    </ul>
  </div>
</section>
'''))

# ------------------------------------------------------------------------------------------------------- questions
QUESTIONS = [
    ('What is Anopticon?',
     'A company that checks what machines report about where they are against what the physical world allows. Ships first.'),
    ('What data does it use?',
     'Data that already exists: public AIS ship broadcasts, satellite radar and imagery, weather and sea-state records, and ship physics.'),
    ('Does it use its own sensors or hardware?',
     'No. Nothing is installed on ships and nothing new is launched. It reads what is already out there.'),
    ('What does it check first?',
     'Ship positions at sea: AIS reports that were jammed, spoofed or forged, and the tracks built from them.'),
    ('What is AIS spoofing?',
     'A ship broadcasting a position or identity that is not real, because its satellite signal was faked or its messages were.'),
    ('What is the difference between GNSS jamming and spoofing?',
     'Jamming drowns the satellite signal, so positions freeze or vanish. Spoofing replaces it, so the ship reports the wrong place.'),
    ('Can it be detected?',
     'Often, from the data alone: speeds no hull can reach, or many ships in one impossible spot. Radar satellites settle the rest.'),
    ('Who is it for?',
     'Anyone who has to rely on where a ship was: charterers, owners, insurers, claims handlers, lawyers, port operators.'),
    ('What comes after ships?',
     'Navies and coast guards, then aircraft, which broadcast their positions the same way.'),
    ('Where is Anopticon based?',
     'Gujarat, India. Founded in 2026 by Vishmayraj Zala and Kathan Patel.'),
    ('What does the name mean?',
     'The panopticon is a prison where one hidden guard sees everyone. Anopticon is the same tower with the walls taken away.'),
    ('How do I get in touch?',
     'Email vishmayraj@anopticon.com, with the ship and the dates if there is a case.'),
]

PAGES.append(dict(
    path='questions/', bg='questions', crumbs=[('Questions', '/questions/')], faq=QUESTIONS,
    title='Questions: what Anopticon is, AIS spoofing and GNSS jamming | Anopticon',
    desc=('Short answers: what Anopticon is, what data it uses (no custom hardware), what AIS spoofing and GNSS jamming are, '
          'and how they are detected.'),
    h1='Questions', line='The short answers.',
    body='<section class="band"><div class="wrap"><dl class="qa">' + ''.join(
        f'<div class="reveal"><dt>{q}</dt><dd>{a}</dd></div>' for q, a in QUESTIONS) + '''</dl></div></section>
<section class="band band--end" aria-labelledby="src-h">
  <div class="wrap pair"><h2 id="src-h">Sources</h2>
    <ul class="sources">
      <li><a href="https://www.imo.org/en/OurWork/Safety/Pages/AIS.aspx">IMO: AIS transponders</a></li>
      <li><a href="https://www.technologyreview.com/2013/10/18/82918/ship-tracking-hack-makes-tankers-vanish-from-view/">Ship-tracking hack makes tankers vanish from view</a>, MIT Technology Review, 2013</li>
      <li><a href="https://arxiv.org/abs/2602.16257">SeaSpoofFinder</a>, arXiv, 2026</li>
      <li><a href="https://insidegnss.com/?p=197021">LA/Long Beach spoofing event, January 2026</a>, Inside GNSS</li>
    </ul>
  </div>
</section>
'''))

# ----------------------------------------------------------------------------------------------------------- about
PAGES.append(dict(
    path='about/', bg='about', crumbs=[('About', '/about/')],
    title='About Anopticon: the name, and a ship that never existed',
    desc='Anopticon is the panopticon with the walls taken away. And in 2013 a ship that never existed sailed the word "pwned".',
    h1='About', line='The panopticon, with the walls taken away.',
    body=f'''
<section class="band" aria-labelledby="pw-h">
  <div class="wrap">
    <div class="pair reveal"><h2 id="pw-h">October 2013</h2><p>A ship that never existed sailed the word &ldquo;pwned&rdquo; off Italy. Public tracking maps showed it. <a href="https://www.technologyreview.com/2013/10/18/82918/ship-tracking-hack-makes-tankers-vanish-from-view/">Source</a></p></div>
    <div class="art" data-art>
      <svg viewBox="0 0 920 360" role="img" aria-label="A ship's track that spells the word pwned">
        <path class="draw ink" d="{PWNED}" fill="none" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>
        <circle class="pop fillmk" data-at=".98" cx="760" cy="90" r="11"/>
      </svg>
    </div>
  </div>
</section>
<section class="band band--end" aria-labelledby="m-h">
  <div class="wrap">
    <h2 id="m-h" class="sr-only">Method</h2>
    {rows([('#', 'Question.', ''), ('#', 'Investigate.', ''), ('#', 'Verify.', '')], 'rows rows--static')}
    <p class="lead reveal" style="margin-top:40px">Say it an-OP-ti-kon. Founded in 2026, in Gujarat.</p>
  </div>
</section>
'''))

# --------------------------------------------------------------------------------------------------------- contact
PAGES.append(dict(
    path='contact/', bg='contact', crumbs=[('Contact', '/contact/')],
    title='Contact Anopticon',
    desc='Write to Anopticon about a ship to check, research or press: vishmayraj@anopticon.com. Gujarat, India.',
    h1='Contact', line='The ship and the dates, if there is a case.',
    body=f'<section class="band band--end"><div class="wrap">{rows([(f"mailto:{MAIL}?subject=Anopticon", MAIL, "Email"), ("/team/", "Vishmayraj Zala and Kathan Patel", "Team"), ("/questions/", "Gujarat, India", "")])}</div></section>\n'))

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


def footer(page):
    return f'''
<footer class="foot">
  <div class="wrap foot__grid">
    <p class="foot__what">{WHAT} <a href="mailto:{MAIL}">{MAIL}</a></p>
    <ul>{''.join(f'<li><a href="{u}">{t}</a></li>' for u, t in NAV)}<li><a href="/about/">About</a></li></ul>
  </div>
  <p class="wrap foot__legal">&copy; {TODAY[:4]} Anopticon, Gujarat, India. Paintings and drawings are public domain.</p>
</footer>
<script src="/assets/site.js" defer></script>
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
    pre = ''
    if page.get('bg'):
        name = 'home' if page['bg'] == 'contact' else page['bg']
        widths = BG[page['bg']][0]
        pre = (f'<link rel="preload" as="image" type="image/webp" imagesrcset="'
               + ', '.join(f'/assets/bg/{name}-{w}.webp {w}w' for w in widths) + '" imagesizes="100vw">\n')
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0A0A0A">
<meta property="og:site_name" content="Anopticon">
<meta property="og:type" content="website">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Anopticon. Built on what is already there.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{SITE}/assets/og.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
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
    top = hero(page['bg'], page['h1'], page['line'], page.get('home'), page.get('extra', '')) if page.get('bg') else (
        f'<header class="phead wrap"><h1 class="hero__h">{page["h1"]}</h1><p class="hero__line">{page["line"]}</p></header>\n')
    return head(page) + nav(page) + '<main id="main">\n' + top + page['body'] + '</main>\n' + footer(page) + '</body>\n</html>\n'


def build():
    for page in PAGES:
        out = OUT / page['path'] / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(page), encoding='utf-8', newline='\n')
        print('wrote', out.relative_to(ROOT))
    nf = dict(path='404/', h1='Not here', line='Nothing at this address. <a class="link" href="/">Back to the start</a>',
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
