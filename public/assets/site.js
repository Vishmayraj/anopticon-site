// Anopticon: page colour follows the section on screen; case drawings draw with the scroll; menu; entrances.
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const body = document.body;

  // Colour: the section filling most of the screen sets the page tone.
  const toneOf = (el) => el.dataset.tone || (el.classList.contains('band--black') ? 'black' : 'white');
  const toned = [...document.querySelectorAll('main > section, main > header, main > article')];
  if (toned.length) {
    const seen = new Map();
    const pick = () => {
      let best = null, area = 0;
      for (const [el, r] of seen) if (r > area) { area = r; best = el; }
      if (best) body.dataset.tone = toneOf(best);
    };
    const io = new IntersectionObserver((es) => { for (const e of es) seen.set(e.target, e.intersectionRatio * e.boundingClientRect.height); pick(); },
      { threshold: [0, .15, .3, .45, .6, .75, .9, 1] });
    toned.forEach((el) => io.observe(el));
  }

  // Drawings: each line knows its length; the scroll decides how much of it is drawn.
  const arts = [...document.querySelectorAll('[data-art]')];
  arts.forEach((a) => a.querySelectorAll('.draw').forEach((p) => {
    try { p.style.setProperty('--len', Math.ceil(p.getTotalLength()) + 1); } catch (e) { /* not drawable */ }
  }));
  function progress() {
    const vh = innerHeight;
    for (const a of arts) {
      const r = a.getBoundingClientRect();
      // 0 when the drawing's top reaches the bottom of the screen, 1 when its middle reaches the upper third
      const p = reduce ? 1 : Math.max(0, Math.min(1, (vh - r.top) / (vh * 0.66 + r.height * 0.5)));
      a.style.setProperty('--p', p.toFixed(3));
      a.querySelectorAll('.pop').forEach((d) => d.style.setProperty('--on', p >= +(d.dataset.at || 0.9) ? 1 : 0));
    }
  }
  if (arts.length) {
    let queued = false;
    const tick = () => { if (!queued) { queued = true; requestAnimationFrame(() => { queued = false; progress(); }); } };
    addEventListener('scroll', tick, { passive: true });
    addEventListener('resize', tick);
    progress();
  }

  // The world map for the Lima case arrives after the text.
  addEventListener('load', () => {
    const w = document.getElementById('world');
    if (w && window.WORLD) w.setAttribute('d', window.WORLD);
  });

  // Menu on narrow screens.
  const nav = document.querySelector('.nav');
  const toggle = nav && nav.querySelector('.nav__toggle');
  if (toggle) {
    const open = (on) => {
      nav.classList.toggle('is-open', on);
      toggle.setAttribute('aria-expanded', String(on));
      toggle.textContent = on ? 'Close' : 'Menu';
      document.body.style.overflow = on ? 'hidden' : '';
    };
    toggle.addEventListener('click', () => open(!nav.classList.contains('is-open')));
    nav.querySelectorAll('.nav__links a').forEach((a) => a.addEventListener('click', () => open(false)));
    addEventListener('keydown', (e) => { if (e.key === 'Escape') open(false); });
  }

  // Entrances.
  document.querySelectorAll('section, header').forEach((s) => {
    s.querySelectorAll('.reveal').forEach((el, i) => el.style.setProperty('--d', `${Math.min(i, 5) * 70}ms`));
  });
  const ro = new IntersectionObserver((es) => {
    for (const e of es) if (e.isIntersecting) { e.target.classList.add('is-in'); ro.unobserve(e.target); }
  }, { rootMargin: '0px 0px -6% 0px', threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach((el) => ro.observe(el));
})();
