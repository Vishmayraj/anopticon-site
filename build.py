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

NAV = [('/projects/', 'Projects'), ('/ledger/', 'Ledger'), ('/research/', 'Research'), ('/partners/', 'Partners'),
       ('/about/', 'About'), ('/join/', 'Join us')]
HERE = ' aria-current="page"'


def crumbs(page):
    items = [('Anopticon', '/')] + page.get('crumbs', [])
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + u} for i, (n, u) in enumerate(items)]}


EXTRA_IMG = {
    'hero': ('/assets/img/wadsworth-dazzle-ships.jpg', 1280, 1600,
             'Painting of a ship in dry dock, its hull covered in clashing black, white and grey stripes, with workers below.',
             'Dazzle-ships in Drydock at Liverpool, Edward Wadsworth, 1919. Ships were painted like this to make an enemy misjudge their course.'),
    'ledger': ('/assets/img/vinckeboons-delaware-1639.jpg', 1600, 1124,
               'Hand-drawn sea chart of a bay and river with compass lines and a compass rose.',
               'Chart of the South River in New Netherland (Delaware Bay), Joan Vinckeboons, 1639. Public domain.'),
    'research': ('/assets/img/holbein-ambassadors.jpg', 1600, 1577,
                 'Two men in a green-curtained room, with a celestial globe, sundials and a quadrant on the table between them.',
                 'The Ambassadors, Hans Holbein the Younger, 1533. On the table, the instruments of knowing where you are. National Gallery, London.'),
    'primer': ('/assets/img/dourado-chart-1571.jpg', 1600, 1228,
               'Portuguese sea chart of the west coast of Africa, with compass roses, rhumb lines and flags.',
               'Chart of the West African coast, Fern&atilde;o Vaz Dourado, 1571. Public domain.'),
    'partners': ('/assets/img/darling-harbour-1900.jpg', 1024, 771,
                 'Black and white photograph of a busy harbour with sailing ships, wharves and a railway yard.',
                 'Darling Harbour, Sydney, about 1900. Kerry and Co., Powerhouse Museum. Public domain.'),
    'join': ('/assets/img/marconi-operator.jpg', 1600, 1170,
             'Black and white photograph of a wireless operator at his instruments in a ship radio room.',
             'Marconi operator aboard the liner Deutschland, early 1900s. Bain News Service, Library of Congress. Public domain.'),
    'about': ('/assets/img/eddystone-1703.jpg', 1110, 1600,
              'Engraving of an ornate wooden lighthouse on a rock, with ships sailing around it.',
              'Eddystone lighthouse, engraved by Henry Winstanley, its builder, before the storm of 1703 took it. Public domain.'),
}

# ---------------------------------------------------------------------------------------------------- pictures
# Every picture is public domain; credits.json in assets/img lists the source pages.
IMG = {
    'nereus': ('/assets/img/nereus-lekythos.jpg', 1600, 1285,
               "Black-figure painting on an oil jar: Heracles grips Nereus, who has a fish's tail and a lion springing from his back.",
               'Heracles and Nereus. Lekythos by the Istanbul Painter, about 590 BC. Louvre, CA 823.'),
    'argus': ('/assets/img/argus-vase.jpg', 1090, 430,
              'Line drawing from a Greek vase: Hermes strikes Argus, whose body is covered in eyes.',
              'Hermes kills Argus. Drawing after an Athenian red-figure vase, W. H. Roscher, 1890.'),
    'aether': ('/assets/img/aether-icarus.jpg', 1600, 1228,
               'Engraving of an armed three-masted ship under sail; in the sky, Icarus falls from the sun.',
               'Armed three-master with Daedalus and Icarus in the sky. After Pieter Bruegel the Elder, 1561&ndash;65. The Met.'),
}
IMG.update(EXTRA_IMG)


def pic(key, cls='print', lazy=True):
    src, w, h, alt, cap = IMG[key]
    lz = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return (f'<figure class="{cls} reveal"><img src="{src}" width="{w}" height="{h}" alt="{html.escape(alt)}"{lz} '
            f'decoding="async"><figcaption>{cap}</figcaption></figure>')


# -------------------------------------------------------------------------------------------------- the one case
PWNED = ('M40 270 L40 90 L160 90 L160 180 L40 180 L220 90 L250 270 L280 180 L310 270 L340 90 L400 270 L400 90 '
         'L520 270 L520 90 L700 90 L580 90 L580 270 L700 270 L580 180 L670 180 L760 90 L760 270 L850 270 L880 240 '
         'L880 120 L850 90 L760 90')
PWNED_ART = f'''<svg viewBox="0 0 920 360" role="img" aria-label="A ship's track that spells the word pwned">
  <path class="draw ink" d="{PWNED}" fill="none" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>
  <circle class="pop fillmk" data-at=".98" cx="760" cy="90" r="11"/>
  <text class="label" x="40" y="330">A ship that never existed, off Italy</text>
</svg>'''

PROJ = [('nereus', 'Nereus', 'Ships at sea', 'Now'), ('argus', 'Argus', 'Navies and coast guards', 'Next'),
        ('aether', 'Aether', 'Aircraft', 'Later')]


def rows(items):
    return '<nav class="close__links" aria-label="Pages">' + ''.join(
        f'<a href="{u}"><span>{a}</span><span>{b}</span></a>' for u, a, b in items) + '</nav>'


PAGES = []

# ------------------------------------------------------------------------------------------------------------ home
PAGES.append(dict(
    path='', home=True, tone='black',
    title='Anopticon | Independent records of what actually happened at sea',
    desc=('Anopticon tests what machines report against what the physical world allows, starting with ship positions at sea: '
          'AIS spoofing, GNSS jamming and falsified tracks, checked and kept as records anyone can verify.'),
    schema=[ORG, WEBSITE] + PEOPLE,
    body=f'''<main id="main">
<header class="open wrap" data-tone="black">
  <h1 class="open__h">Records of what actually happened.</h1>
  <div class="open__row">
    <p>{WHAT} We start at sea. Ships broadcast their own positions every few seconds, and those broadcasts are now jammed, spoofed and faked.</p>
    <p class="open__count"><a href="/partners/">Bring us a case</a></p>
  </div>
</header>

<section class="home-img" data-tone="black" aria-label="Picture">
  <div class="wrap">{pic('hero', 'print print--wide', lazy=False)}</div>
</section>

<section class="band" data-tone="white" aria-labelledby="do-h">
  <div class="wrap duo">
    <h2 class="h2 reveal" id="do-h">What we do</h2>
    <div class="prose reveal">
      <p>Every large ship reports its position over AIS, a radio system with no signature on its messages. The position comes from the ship&rsquo;s satellite receiver, and that receiver can be jammed or fooled. Ports, insurers, charterers, lawyers and navies all rely on those positions anyway.</p>
      <p>We check them. Each report is tested against what that ship can physically do, against the ships around it, and against independent sources such as radar satellites. What we find goes into a record, with the data and the method, so the other side can check it too.</p>
      <p>New to this? The <a href="/primer/">primer</a> explains how positions go wrong.</p>
    </div>
  </div>
</section>

<section class="band" data-tone="black" aria-labelledby="proj-h">
  <div class="wrap">
    <div class="duo">
      <h2 class="h2 reveal" id="proj-h">Projects</h2>
      <p class="lead reveal">One core, one domain at a time: sea first, then the people who watch it, then the air.</p>
    </div>
    {rows([(f'/projects/{k}/', f'{n}. {w}.', t) for k, n, w, t in PROJ])}
  </div>
</section>

<section class="band" data-tone="white" aria-labelledby="ledger-h">
  <div class="wrap duo">
    {pic('ledger')}
    <div>
      <h2 class="h2 reveal" id="ledger-h">The ledger</h2>
      <p class="lead reveal">On 10 October 2026, 49 ships near Istanbul reported themselves in inland Peru, 12,221&nbsp;km away. We found it, measured it and wrote it down.</p>
      <p class="reveal" style="margin-top:24px"><a class="link" href="/ledger/">Read the entry</a></p>
    </div>
  </div>
</section>

<section class="band" data-tone="orange" aria-labelledby="partners-h">
  <div class="wrap duo">
    <h2 class="h2 reveal" id="partners-h">Design partners</h2>
    <div class="reveal">
      <p class="lead">We are working with a small number of early partners on real cases: claims, disputes, charters. If a ship&rsquo;s position matters to you, we would like to look at it.</p>
      <p style="margin-top:24px"><a class="btn btn--solid" href="/partners/">How it works</a></p>
    </div>
  </div>
</section>

<section class="band" data-tone="white" aria-labelledby="research-h">
  <div class="wrap duo">
    <div>
      <h2 class="h2 reveal" id="research-h">Research</h2>
      <p class="lead reveal">Our first paper measures how far ship physics can be trusted between AIS reports, on 47.7 million real ones. The code is public.</p>
      <p class="reveal" style="margin-top:24px"><a class="link" href="/research/">The paper</a></p>
    </div>
    {pic('research')}
  </div>
</section>

<section class="close" data-tone="black" aria-labelledby="close-h">
  <div class="wrap">
    <div class="close__grid">
      <h2 class="h2 reveal" id="close-h">Two founders, in Gujarat.</h2>
      <div class="reveal">
        <p class="lead">We built the engine and wrote the paper ourselves, and we are looking for people who would rather check than assume.</p>
        <p style="margin-top:24px"><a class="btn btn--solid" href="mailto:{MAIL}">{MAIL}</a></p>
      </div>
    </div>
    {rows([('/about/', 'Why we exist', 'About'), ('/team/', 'Who we are', 'Team'), ('/join/', 'Work with us', 'Join us'), ('/contact/', 'Get in touch', 'Contact')])}
  </div>
</section>
</main>
'''))

# ----------------------------------------------------------------------------------------------------------- about
PAGES.append(dict(
    path='about/', crumbs=[('About', '/about/')], tone='black',
    title='About Anopticon: why we exist and what the name means',
    desc=('In 2013 a ship that never existed sailed the word "pwned" across public tracking maps. Why Anopticon exists, '
          'how we work, and what the name means.'),
    h1='About', lede='When something does not make sense, ask why.',
    body=f'''
<section class="case" data-tone="white" aria-labelledby="case-pwned">
  <div class="wrap case__grid">
    <div>
      <p class="case__when reveal">October 2013. Off Italy.</p>
      <h2 class="case__h reveal" id="case-pwned">A ship that never existed sailed the word &ldquo;pwned&rdquo;.</h2>
      <p class="case__p reveal">Researchers at Trend Micro built it with a 700-euro AIS radio and a laptop near a port, and public tracking maps showed it. In the same tests a real tugboat left the Mississippi and turned up on a lake in Dallas. Nobody had to break into anything. AIS simply believes what it hears.</p>
      <p class="case__src reveal"><a href="https://www.technologyreview.com/2013/10/18/82918/ship-tracking-hack-makes-tankers-vanish-from-view/">MIT Technology Review</a>, 18 October 2013</p>
    </div>
    <div class="case__art" data-art>{PWNED_ART}</div>
  </div>
</section>

<section class="band" data-tone="black" aria-labelledby="why-h">
  <div class="wrap duo">
    <h2 id="why-h" class="h2 reveal">Why we exist</h2>
    <div class="prose reveal">
      <p>Thirteen years later the trick is ordinary. Ships near Istanbul report themselves in Peru. Ships in Shanghai appear in rings on dry land. Whole sea areas lose their satellite signal. Each of those false positions ends up in a port log, an insurance file, a sanctions screen or a court bundle.</p>
      <p>Machines now report where they are all the time: ships, aircraft, vehicles, sensors. Almost nobody checks them independently. That is the job we picked.</p>
    </div>
  </div>
</section>

<section class="band" data-tone="white" aria-labelledby="how-h">
  <div class="wrap duo">
    <h2 id="how-h" class="h2 reveal">Question. Investigate. Verify.</h2>
    <div class="prose reveal">
      <p><b>Question.</b> Start with the report that does not fit: the impossible speed, the ship on land, the crowd in one spot.</p>
      <p><b>Investigate.</b> Test it against what the physical world allows, compare independent sources, and measure how unusual the pattern really is.</p>
      <p><b>Verify.</b> Write down what the evidence supports and where it stops, and hand over the data so anyone can rerun it. When we are wrong, the correction goes where the claim was.</p>
    </div>
  </div>
</section>

<section class="band" data-tone="black" aria-labelledby="name-h">
  <div class="wrap duo">
    {pic('about')}
    <div>
      <h2 id="name-h" class="h2 reveal">The name</h2>
      <div class="prose reveal" style="margin-top:24px">
        <p>Bentham&rsquo;s panopticon is a prison with a tower in the middle: the guard sees every cell and no prisoner sees the guard. Take the &ldquo;pan&rdquo; away and you have Anopticon. We kept the tower and took out the secret.</p>
        <p>Say it an-OP-ti-kon. The word is older than us; a 2009 project in Venice used it to map the city&rsquo;s CCTV cameras. We are the maritime one, founded in 2026 in Gujarat.</p>
      </div>
    </div>
  </div>
</section>

<section class="close" data-tone="white" aria-label="More">
  <div class="wrap">{rows([('/team/', 'Who we are', 'Team'), ('/projects/', 'What we are building', 'Projects'), ('/join/', 'Work with us', 'Join us')])}</div>
</section>
'''))

# ---------------------------------------------------------------------------------------------------------- primer
FAQ = [
    ('What is AIS spoofing?',
     'A ship broadcasting a position, identity or movement over the Automatic Identification System that is not real. It happens '
     'when the ship\'s satellite-navigation receiver is fed a false signal, or when the AIS messages themselves are forged.'),
    ('What is the difference between GNSS jamming and spoofing?',
     'Jamming drowns the satellite signal, so the receiver loses its fix and positions freeze, drift or disappear. Spoofing replaces '
     'the signal with a false one, so the receiver reports the wrong place with full confidence. Mild jamming can look like spoofing in the data.'),
    ('Can AIS spoofing be detected?',
     'A lot of it can be flagged from the data: a report that needs a speed no hull can reach, or many ships reporting the same '
     'impossible spot. AIS alone rarely shows who did it. Radar satellites can confirm where a ship really was.'),
    ('Where does it happen?',
     'Interference is reported regularly in the Baltic, the Black Sea, the eastern Mediterranean and the Gulf, and has been recorded '
     'off major ports elsewhere, including Los Angeles and Long Beach in January 2026.'),
    ('Why does it matter outside navigation?',
     'Because ship positions are evidence. They decide demurrage and laytime, whether a ship entered a sanctioned area, whether a claim '
     'for a collision or a grounding holds up, and what a voyage is worth. A false position carries into every one of those.'),
]

PAGES.append(dict(
    path='primer/', crumbs=[('Primer', '/primer/')],
    title='AIS spoofing and GNSS jamming: a primer | Anopticon',
    desc=('What AIS is, how ship positions go wrong through GNSS jamming, spoofing and forgery, how it shows up in the data, '
          'and how it can be detected.'),
    h1='Primer', lede='What AIS is, how a ship ends up broadcasting a position it is not in, and how you can tell.', faq=FAQ,
    body=f'''
<section class="band" aria-labelledby="ais-h">
  <div class="wrap duo">
    <h2 id="ais-h" class="h2 reveal">What AIS is</h2>
    <div class="prose reveal">
      <p>AIS, the Automatic Identification System, is a radio transponder. Every few seconds it broadcasts the ship&rsquo;s identity, position, course and speed on two VHF channels, 161.975 and 162.025&nbsp;MHz, that any receiver can hear: other ships, shore stations, satellites, and the websites that turn it all into a map.</p>
      <p>Under the SOLAS convention it is carried by ships of 300 gross tonnage and upwards on international voyages, by cargo ships of 500 gross tonnage and upwards, and by all passenger ships. A ship under way sends a position every 2 to 10 seconds; at anchor, every three minutes.</p>
      <p>The position comes from the ship&rsquo;s own satellite-navigation receiver, usually GPS. AIS repeats whatever that receiver believes, and nothing in the message proves who sent it.</p>
    </div>
  </div>
</section>

<section class="band band--black" aria-labelledby="ways-h">
  <div class="wrap">
    <h2 id="ways-h" class="h2 reveal">Jamming, spoofing, forgery</h2>
    <dl class="ways">
      <div class="reveal"><dt>Jamming</dt><dd>Noise drowns the satellite signal. The receiver loses its fix and positions freeze, drift or vanish. Jamming is cheap and is often a side effect of military activity nearby.</dd></div>
      <div class="reveal"><dt>Spoofing</dt><dd>A false satellite signal replaces the real one. The receiver reports the wrong place with full confidence, often many ships at once, often on land.</dd></div>
      <div class="reveal"><dt>Forgery</dt><dd>The AIS messages themselves are made up or changed: a borrowed identity, a ship that does not exist, a track that was never sailed, a transponder switched off.</dd></div>
    </dl>
  </div>
</section>

<section class="band" aria-labelledby="look-h">
  <div class="wrap duo">
    {pic('primer')}
    <div>
      <h2 id="look-h" class="h2 reveal">What it looks like</h2>
      <div class="prose reveal" style="margin-top:24px">
        <p>A ship that covers a continent between two reports. Dozens of ships stacked on one point inland. Tracks that loop in perfect circles over a headland. A ship that goes silent for an hour and comes back somewhere it could not have reached.</p>
        <p>One ship doing this is usually a faulty receiver. Many ships doing it in the same place at the same time is interference.</p>
      </div>
    </div>
  </div>
</section>

<section class="band band--grey" aria-labelledby="tell-h">
  <div class="wrap duo">
    <h2 id="tell-h" class="h2 reveal">How to tell</h2>
    <div class="prose reveal">
      <p><b>The hull.</b> A ship has a length, an engine and a top speed. A report that needs more than that did not happen as reported. Our <a href="/research/">research</a> measures how far ship physics holds between sparse reports.</p>
      <p><b>Other ships.</b> One ship jumping is a fault. Forty jumping to the same place is a pattern, and the pattern often says what kind of interference it was.</p>
      <p><b>A second source.</b> Radar satellites see ships whether or not they broadcast. Where an image exists for the right place and time, it settles where the ship was.</p>
    </div>
  </div>
</section>
'''))

# ---------------------------------------------------------------------------------------------------------- ledger
HOURS = [('12:00', 2), ('13:00', 1), ('14:00', 1), ('15:00', 4), ('16:00', 17), ('17:00', 36), ('18:00', 22)]
hours_rows = ''.join(f'<tr><th scope="row">{h}</th><td><span class="bar" style="--v:{v / 36:.3f}"></span></td><td>{v}</td></tr>' for h, v in HOURS)

PAGES.append(dict(
    path='ledger/', crumbs=[('Ledger', '/ledger/')],
    title='AIS spoofing incidents: the Anopticon ledger',
    desc=('Interference events we have recorded in ship AIS data, with dates, ship counts, distances and reported speeds. '
          'Ships near Istanbul reported in Lima, Peru, 10 and 11 October 2026.'),
    h1='Ledger', lede='Events we have found and recorded ourselves. One entry each, the numbers behind it, and what the data cannot show.',
    body=f'''
<section class="band" aria-labelledby="e1-h">
  <article class="wrap">
    <div class="duo">
      <div>
        <h2 id="e1-h" class="h2 reveal">Lima, 10 October 2026</h2>
        <p class="lead reveal" style="margin-top:24px">Ships in the Bosphorus and the western Black Sea broadcast positions inside one 3&nbsp;km patch of inland Lima, Peru, on the far side of the planet.</p>
      </div>
      {pic('ledger')}
    </div>
    <table class="data reveal">
      <caption class="sr-only">Lima event, 10 October 2026</caption>
      <tbody>
        <tr><th scope="row">Ships</th><td>49</td><td>247 reports, 41 with names</td></tr>
        <tr><th scope="row">Window</th><td>12:00&ndash;18:34</td><td>UTC</td></tr>
        <tr class="is-false"><th scope="row">Reported at</th><td>Inland Lima</td><td>12.04&deg; S, 77.05&deg; W</td></tr>
        <tr><th scope="row">Really near</th><td>The Bosphorus</td><td>41.56&deg; N, 28.98&deg; E</td></tr>
        <tr><th scope="row">Apart</th><td>12,221 km</td><td>median, per ship</td></tr>
        <tr><th scope="row">Spread</th><td>965 m</td><td>median from the centre of the patch</td></tr>
        <tr><th scope="row">Reported speed</th><td>94.9 kn</td><td>median; fastest 102.0</td></tr>
      </tbody>
    </table>
    <h3 class="sub reveal">Ships in the patch, by hour (UTC)</h3>
    <table class="hours reveal"><caption class="sr-only">Ships per hour</caption><tbody>{hours_rows}</tbody></table>
  </article>
</section>

<section class="band band--grey" aria-labelledby="e2-h">
  <article class="wrap">
    <h2 id="e2-h" class="h2 reveal">Lima, 11 October 2026</h2>
    <p class="lead reveal measure" style="margin-top:24px">The same patch, the next morning, shorter.</p>
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

<section class="band" aria-labelledby="how-h">
  <div class="wrap duo">
    <h2 id="how-h" class="h2 reveal">How we found it</h2>
    <div class="prose reveal">
      <p>No single report gave it away. What stood out was many ships, with no earlier history in the area, arriving in one small patch over a few hours, most of them last seen on the other side of the world. We cluster reports like that into one event, check every ship against its own earlier track, and keep the reports as they were received.</p>
    </div>
  </div>
</section>

<section class="band band--black" aria-labelledby="stop-h">
  <div class="wrap duo">
    <h2 id="stop-h" class="h2 reveal">What it does not show</h2>
    <p class="lead reveal">The positions were moved, not sailed, and the pattern fits interference with satellite navigation. The data alone does not say who or what did it, and we do not guess.</p>
  </div>
</section>
'''))


# -------------------------------------------------------------------------------------------------------- projects
PAGES.append(dict(
    path='projects/', crumbs=[('Projects', '/projects/')],
    title='Projects: Nereus, Argus and Aether | Anopticon',
    desc='One core, one domain at a time: Nereus for ships at sea, Argus for navies and coast guards, Aether for aircraft.',
    h1='Projects', lede='One core: test what a machine reports against what the physical world allows. One domain at a time, each one only when the last has earned it.',
    body='\n'.join(f'''
<section class="band{' band--grey' if i % 2 else ''}" aria-labelledby="p-{k}">
  <div class="wrap duo">
    {pic(k)}
    <div>
      <p class="case__when reveal">{t}</p>
      <h2 class="h2 reveal" id="p-{k}" style="margin-top:14px">{n}</h2>
      <p class="lead reveal" style="margin-top:20px">{w}.</p>
      <p class="reveal" style="margin-top:24px"><a class="link" href="/projects/{k}/">About {n}</a></p>
    </div>
  </div>
</section>''' for i, (k, n, w, t) in enumerate(PROJ))))


def project(i, title, desc, lede, sections):
    k, n, w, t = PROJ[i]
    prev_, next_ = PROJ[i - 1], PROJ[(i + 1) % len(PROJ)]
    secs = ''.join(f'''
<section class="band{' band--grey' if j % 2 else ''}" aria-labelledby="{k}-{j}">
  <div class="wrap duo">
    <h2 id="{k}-{j}" class="h2 reveal">{h}</h2>
    <div class="prose reveal">{''.join(f'<p>{p}</p>' for p in ps)}</div>
  </div>
</section>''' for j, (h, ps) in enumerate(sections))
    return dict(
        path=f'projects/{k}/', crumbs=[('Projects', '/projects/'), (n, f'/projects/{k}/')],
        title=title, desc=desc, h1=n, lede=lede,
        body=f'''
<section class="band" aria-label="Picture"><div class="wrap">{pic(k, 'print print--wide', lazy=False)}</div></section>
{secs}
<section class="close" aria-label="Other projects">
  <div class="wrap">{rows([(f'/projects/{prev_[0]}/', f'{prev_[1]}. {prev_[2]}.', 'Previous'), (f'/projects/{next_[0]}/', f'{next_[1]}. {next_[2]}.', 'Next'), ('/projects/', 'All projects', 'Projects')])}</div>
</section>
''')


PAGES.append(project(
    0, 'Project Nereus: independent records of ship positions at sea | Anopticon',
    'Project Nereus is our work at sea: telling real ship positions from jammed, spoofed and forged ones, and keeping records anyone can check.',
    'Ships at sea. What we are building now.',
    [('The story', ['In the Greek story, Nereus, the old man of the sea, would answer any question truthfully if you could hold on to him while he changed shape: a lion, a serpent, water. Heracles held on.',
                    'Ship data changes shape the same way, and the job is to hold on until it tells you what happened.']),
     ('What it does', ['We read AIS from several networks, keep every report as it was received, and test each one against a calibrated model of what that ship could have done since its last report.',
                       'Where many ships go wrong in one place, we open a single event and describe it: where they were, where they said they were, when, and how far apart. Every finding goes into a record with the reports behind it and a script that recomputes the numbers.']),
     ('Who it is for', ['People who need to know where a ship really was and may have to prove it to someone else: charterers and owners in a dispute, claims handlers and P&amp;I correspondents, admiralty lawyers and the experts they hire.',
                        'We are working with a few <a href="/partners/">design partners</a> on real cases now.']),
     ('Where it stands', ['Working today: live scoring of AIS against ship physics, clustering of area events like Lima, and records whose numbers anyone can rerun.',
                          'Still to come: our own receivers at chokepoints, trusted timestamps on the archive, and purchased radar imagery for disputed cases.'])]))
PAGES.append(project(
    1, 'Project Argus: position checks for navies and coast guards | Anopticon',
    'Project Argus takes our ship-position checks to the navies and coast guards whose job is to watch the sea.',
    'Navies and coast guards. Next, once the sea work has earned it.',
    [('The story', ['Argus Panoptes had a hundred eyes and never closed them all. Hermes lulled every one of them to sleep anyway.',
                    'Watching everything is not the same as knowing what is true.']),
     ('What it would do', ['Find ships that go dark, ships that meet at sea without saying so, and ships whose identity does not match their hull, by putting AIS next to radar satellites and radio.',
                           'Built on the same core as Nereus, with the same rule: say what the evidence supports and where it stops.']),
     ('Where it stands', ['A radar-first scan that looks for ships AIS does not explain already runs in test. Argus starts properly after Nereus has paying customers and a published method with its error rates.'])]))
PAGES.append(project(
    2, 'Project Aether: position checks for aircraft | Anopticon',
    'Project Aether asks the same question of aircraft, which broadcast their positions too, and whose positions are jammed and spoofed in the same way.',
    'Aircraft. Later.',
    [('The story', ['Aether is the bright upper air of the Greek sky. In Bruegel&rsquo;s engraving a warship holds its course while Icarus falls out of the sky above it.']),
     ('What it would do', ['Aircraft broadcast where they are over ADS-B, and those positions are hit by the same jamming and spoofing as ships. The method that finds many ships reporting one impossible place applies to aircraft almost unchanged.']),
     ('Where it stands', ['An intention, not a product. It comes after the sea and the navies, and only if the core has proved it carries over.'])]))

# -------------------------------------------------------------------------------------------------------- research
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
      <p>On shore you only see a ship through its AIS reports, seconds to minutes apart. Textbook ship physics describes continuous motion. We measured what survives the gap: what those reports let the models predict, what they let you work out about a particular hull, and what they let you rule out.</p>
      <p>The data: 47,739,929 reports from four networks over eleven days in the Baltic and North Sea, tested on ships the models had not seen.</p>
    </div>
  </div>
</section>

<section class="band band--grey" aria-labelledby="f-h">
  <div class="wrap">
    <h2 id="f-h" class="h2 reveal">What we found</h2>
    <table class="data data--plain reveal">
      <caption class="sr-only">Findings</caption>
      <tbody>
        <tr><th scope="row">Turns</th><td>On course changes of 45&deg; or more, standard turn models place the ship about 22% worse at the 95th percentile than simply averaging the two reports.</td></tr>
        <tr><th scope="row">Steering</th><td>A hull&rsquo;s steering constants can&rsquo;t be identified from AIS, because AIS carries no rudder angle. Fitting them anyway makes predictions worse.</td></tr>
        <tr><th scope="row">Speed</th><td>A Holtrop&ndash;Mennen speed screen is crossed by 4 of 8,472 ships up to Froude number 0.45, and by 181 of 199 above it, most of them fast passenger craft.</td></tr>
        <tr><th scope="row">So</th><td>Between sparse reports, ship physics is good for bounds, not for filling in the gaps. That is exactly what a check needs.</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section class="band" aria-labelledby="why-h">
  <div class="wrap duo">
    {pic('research')}
    <div>
      <h2 id="why-h" class="h2 reveal">Why it matters to us</h2>
      <div class="prose reveal" style="margin-top:24px">
        <p>Every check we run asks whether a ship could have done what its reports say. The answer is only as good as the physics behind it, so we measured where that physics holds and where it does not before relying on it.</p>
        <p>Next: a method note on our own detector, with its error rates on real data.</p>
      </div>
    </div>
  </div>
</section>
'''))

# ------------------------------------------------------------------------------------------------------------ team
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
      <p>Builds real-time data systems. Google Summer of Code 2026 contributor with OSGeo, on the istSOS4 project. Wrote the Anopticon engine and is the corresponding author of our first paper.</p>
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
      <p>Student researcher. Works on the data and on checking what the engine finds, and co-authored our first paper.</p>
      <ul class="buttons">
        <li><a class="btn" href="https://github.com/KathanPatel1310">GitHub</a></li>
        <li><a class="btn" href="https://www.linkedin.com/in/kathan-patel-0235a3354">LinkedIn</a></li>
      </ul>
    </div>
  </div>
</section>

<section class="close" aria-label="More">
  <div class="wrap">{rows([('/join/', 'We are looking for people', 'Join us'), ('/about/', 'Why we exist', 'About')])}</div>
</section>
'''))

# -------------------------------------------------------------------------------------------------------- partners
PAGES.append(dict(
    path='partners/', crumbs=[('Design partners', '/partners/')],
    title='Design partners: bring us a real case | Anopticon',
    desc=('Anopticon is working with three to five early design partners on real cases where a ship\'s position matters: '
          'claims, disputes and charters. What you get, what we ask, and how to start.'),
    h1='Design partners', lede='We are working with three to five early partners on real cases. If a ship&rsquo;s position matters to your work, this is how it goes.',
    body=f'''
<section class="band" aria-labelledby="who-h">
  <div class="wrap duo">
    <h2 id="who-h" class="h2 reveal">Who it is for</h2>
    <div class="prose reveal">
      <p>Charterers and owners with a disputed voyage. Claims handlers and P&amp;I correspondents. Admiralty lawyers and the experts they instruct. Anyone who has had to argue about where a ship was, and wished the data could be checked by both sides.</p>
    </div>
  </div>
</section>

<section class="band band--black" aria-labelledby="get-h">
  <div class="wrap">
    <h2 id="get-h" class="h2 reveal">What you get, what we ask</h2>
    <dl class="ways">
      <div class="reveal"><dt>Your cases, looked at</dt><dd>We work up to three of your real cases into records: what the positions show, what they cannot show, and the data behind both.</dd></div>
      <div class="reveal"><dt>A say in the product</dt><dd>You tell us what a record has to contain to be useful in your work, and we build that, not what we imagined.</dd></div>
      <div class="reveal"><dt>What we ask</dt><dd>Real cases under NDA, a small fee per case that is credited in full if you carry on with us, and the outcome of each case once it closes.</dd></div>
    </dl>
  </div>
</section>

<section class="band" aria-labelledby="ind-h">
  <div class="wrap duo">
    {pic('partners')}
    <div>
      <h2 id="ind-h" class="h2 reveal">One thing to know</h2>
      <div class="prose reveal" style="margin-top:24px">
        <p>We are independent. Our fee never depends on the outcome, and a record says what the data shows even when that hurts the side that asked for it. That is the only way a record is worth showing to the other side.</p>
        <p>Everything is covered by a written agreement on scope, data rights, confidentiality and liability before any work starts.</p>
      </div>
    </div>
  </div>
</section>

<section class="band" data-tone="orange" aria-labelledby="start-h">
  <div class="wrap duo">
    <h2 id="start-h" class="h2 reveal">How to start</h2>
    <div class="reveal">
      <p class="lead">Send us the ship (name or MMSI), the dates, and one line on what is in dispute. We will reply with whether the data can say anything useful.</p>
      <p style="margin-top:24px"><a class="btn btn--solid" href="mailto:{MAIL}?subject=Design%20partner%3A%20a%20case">Send a case</a></p>
    </div>
  </div>
</section>
'''))

# ------------------------------------------------------------------------------------------------------------ join
PAGES.append(dict(
    path='join/', crumbs=[('Join us', '/join/')],
    title='Join Anopticon: careers',
    desc=('Work at Anopticon on ship positions, GNSS interference and independent records. Who we are looking for, how we work, '
          'and how to apply by email.'),
    h1='Join us', lede='We are two people. The next few will shape what this becomes.',
    body=f'''
<section class="band" aria-labelledby="look-h">
  <div class="wrap duo">
    <h2 id="look-h" class="h2 reveal">Who we are looking for</h2>
    <div class="prose reveal">
      <p>People who notice when something does not add up, and go and find out why instead of rounding it off. People who would rather say &ldquo;the data stops here&rdquo; than make something up to fill the gap.</p>
      <p>We do not have job titles yet. These are the kinds of people we want to hear from.</p>
    </div>
  </div>
</section>

<section class="band band--black" aria-labelledby="kinds-h">
  <div class="wrap">
    <h2 id="kinds-h" class="h2 reveal">The kinds of work</h2>
    <dl class="ways">
      <div class="reveal"><dt>From the sea</dt><dd>Master mariners, navigating officers, VTS operators, surveyors, claims and P&amp;I people. You know what a real track looks like and what a dispute really turns on.</dd></div>
      <div class="reveal"><dt>From the signal</dt><dd>GNSS and radio engineers, SAR and remote-sensing people, anyone who has decoded AIS or ADS-B for fun.</dd></div>
      <div class="reveal"><dt>From the data</dt><dd>Engineers who build pipelines that keep the raw truth, statisticians who measure their own error, and naval architects who know what a hull can and cannot do.</dd></div>
    </dl>
  </div>
</section>

<section class="band" aria-labelledby="how-h">
  <div class="wrap duo">
    {pic('join')}
    <div>
      <h2 id="how-h" class="h2 reveal">How we work</h2>
      <div class="prose reveal" style="margin-top:24px">
        <p>Small, in Gujarat, and in the open: our methods are published and our code is checked by people outside the company. We write down what we got wrong and fix it where people will see it.</p>
        <p>It is early. That means real ownership and real uncertainty, and we will be straight with you about both.</p>
      </div>
    </div>
  </div>
</section>

<section class="band" data-tone="orange" aria-labelledby="apply-h">
  <div class="wrap duo">
    <h2 id="apply-h" class="h2 reveal">How to apply</h2>
    <div class="reveal">
      <p class="lead">Email your CV and a few lines on something you found that did not add up, and what you did about it. No cover letter needed.</p>
      <p style="margin-top:24px"><a class="btn btn--solid" href="mailto:{MAIL}?subject=Joining%20Anopticon">Send your CV</a></p>
    </div>
  </div>
</section>
'''))

# --------------------------------------------------------------------------------------------------------- contact
PAGES.append(dict(
    path='contact/', crumbs=[('Contact', '/contact/')],
    title='Contact Anopticon',
    desc='Write to Anopticon about a ship to check, a partnership, a job, research or press: vishmayraj@anopticon.com. Gujarat, India.',
    h1='Contact', lede='A ship to check, a question, a story or a CV. One address for all of it.',
    body=f'''
<section class="rows" aria-label="Contact details">
  <a class="row row--orange" href="mailto:{MAIL}?subject=Anopticon"><span>vishmayraj@<wbr>anopticon.com</span><span aria-hidden="true">&rarr;</span></a>
  <a class="row" href="/partners/"><span>A case to look at</span><span aria-hidden="true">&rarr;</span></a>
  <a class="row" href="/join/"><span>Working with us</span><span aria-hidden="true">&rarr;</span></a>
  <a class="row" href="/team/"><span>Vishmayraj Zala and Kathan Patel</span><span aria-hidden="true">&rarr;</span></a>
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
    <ul><li><a href="/projects/">Projects</a></li><li><a href="/ledger/">Ledger</a></li><li><a href="/research/">Research</a></li><li><a href="/primer/">Primer</a></li></ul>
    <ul><li><a href="/partners/">Design partners</a></li><li><a href="/about/">About</a></li><li><a href="/team/">Team</a></li><li><a href="/join/">Join us</a></li><li><a href="/contact/">Contact</a></li></ul>
  </div>
  <p class="wrap foot__legal">&copy; {TODAY[:4]} Anopticon, Gujarat, India. All pictures are public domain and credited where they appear.</p>
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
        body = '<main id="main">\n' + page_head(page) + body + (faq_html(page['faq']) if page.get('faq') else '') + '</main>\n'
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
