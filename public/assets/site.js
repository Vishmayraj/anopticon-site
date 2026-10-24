// Anopticon: flags, the forged-flag hunt, hoist your name, prints that take their colour back, menu, entrances.
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const ICS = window.ICS || {};
  const MEANS = {
    A: 'Diver down; keep clear', B: 'Dangerous cargo', C: 'Yes', D: 'Keep clear; manoeuvring with difficulty',
    E: 'Altering course to starboard', F: 'Disabled; communicate with me', G: 'I require a pilot', H: 'Pilot on board',
    I: 'Altering course to port', J: 'On fire; keep clear', K: 'I wish to communicate with you', L: 'Stop instantly',
    M: 'Stopped, making no way', N: 'No', O: 'Man overboard', P: 'All aboard; about to sail', Q: 'Healthy; request pratique',
    R: 'No single-flag meaning', S: 'Engines going astern', T: 'Keep clear of me', U: 'You are running into danger',
    V: 'I require assistance', W: 'I require medical assistance', X: 'Stop and watch for my signals', Y: 'Dragging anchor',
    Z: 'I require a tug',
  };
  const LETTERS = Object.keys(ICS);

  requestAnimationFrame(() => document.body.classList.add('is-loaded'));

  function flag(letter, tag = 'span') {
    const f = ICS[letter];
    const el = document.createElement(tag);
    el.className = 'flag';
    if (!f) return el;
    el.dataset.letter = letter;
    el.dataset.say = `${letter} ${f.name}`;
    el.innerHTML = `<svg viewBox="${f.v}" preserveAspectRatio="none" aria-hidden="true">${f.s}</svg>`;
    return el;
  }
  function draw(host, word, tag) {
    host.replaceChildren();
    [...word.toUpperCase()].filter((c) => ICS[c]).forEach((c, i) => {
      const f = flag(c, tag);
      f.style.setProperty('--i', i);
      host.appendChild(f);
    });
  }

  // Every hoist on the page, plus single flags.
  document.querySelectorAll('[data-hoist]').forEach((h) => {
    if (h.hasAttribute('data-forge')) return;
    draw(h, h.dataset.hoist);
    if (!h.closest('.nav') && h.parentElement.closest('.phead')) h.querySelectorAll('.flag').forEach((f) => f.classList.add('flag--outline'));
  });
  document.querySelectorAll('[data-flag]').forEach((c) => {
    const f = flag(c.dataset.flag);
    c.replaceChildren(...f.childNodes);
  });

  // The hero: ANOPTICON in flags, one of them forged. Find it.
  const hero = document.querySelector('.hero__hoist[data-forge]');
  const say = document.getElementById('game');
  if (hero) {
    const word = hero.dataset.hoist;
    draw(hero, word, 'button');
    const flags = [...hero.querySelectorAll('.flag')];
    const at = Math.floor(Math.random() * flags.length);
    const real = flags[at].dataset.letter;
    // Forge it with a flag that is easy to mistake for nothing: any other letter.
    const pool = LETTERS.filter((l) => l !== real && !word.includes(l));
    const fake = pool[Math.floor(Math.random() * pool.length)];
    const forged = flag(fake, 'button');
    forged.style.setProperty('--i', at);
    forged.dataset.forged = real;
    flags[at].replaceWith(forged);
    let tries = 0, found = false;
    hero.querySelectorAll('.flag').forEach((f, i) => {
      f.type = 'button';
      f.setAttribute('aria-label', `Flag ${i + 1}: ${f.dataset.say}`);
      f.addEventListener('click', () => {
        if (found) return;
        tries++;
        if (f.dataset.forged) {
          found = true;
          f.classList.add('is-caught');
          const r = ICS[f.dataset.forged];
          say.innerHTML = `<b>Forged.</b> Flag ${i + 1} is ${fake} ${ICS[fake].name}, which means &ldquo;${MEANS[fake]}&rdquo;. The hoist says ${word}, so it should be ${f.dataset.forged} ${r.name}. Found in ${tries} ${tries === 1 ? 'try' : 'tries'}.`;
        } else {
          f.classList.remove('is-wrong'); void f.offsetWidth; f.classList.add('is-wrong');
          say.textContent = `${f.dataset.say} is real. It belongs in ${word}. Keep looking.`;
        }
      });
    });
    if (!reduce) hero.classList.add('hoisting');
  }

  // Hoist your name, then forge one flag.
  const own = document.getElementById('own');
  if (own) {
    const out = document.getElementById('own-hoist');
    const read = document.getElementById('own-read');
    const forgeBtn = document.getElementById('forge');
    const checkBtn = document.getElementById('check');
    let forgedAt = -1, truth = '';
    const clean = () => own.value.toUpperCase().replace(/[^A-Z]/g, '');
    const render = () => {
      truth = clean() || 'NEREUS';
      draw(out, truth);
      forgedAt = -1;
      read.innerHTML = `Reads <b>${truth}</b>.`;
      forgeBtn.disabled = false;
    };
    own.addEventListener('input', render);
    forgeBtn.addEventListener('click', () => {
      const flags = [...out.querySelectorAll('.flag')];
      if (!flags.length) return;
      if (forgedAt >= 0) render();
      forgedAt = Math.floor(Math.random() * flags.length);
      const was = flags[forgedAt].dataset.letter;
      const pool = LETTERS.filter((l) => l !== was);
      const fake = pool[Math.floor(Math.random() * pool.length)];
      const f = flag(fake);
      f.classList.add('is-forged');
      flags[forgedAt].replaceWith(f);
      const now = [...out.querySelectorAll('.flag')].map((x) => x.dataset.letter).join('');
      read.innerHTML = `Reads <b>${now}</b>. Does it?`;
    });
    checkBtn.addEventListener('click', () => {
      const f = out.querySelector('.is-forged');
      if (!f) { read.innerHTML = `Reads <b>${truth}</b>. Nothing forged yet.`; return; }
      f.classList.add('is-shown');
      read.innerHTML = `Flag ${forgedAt + 1} was forged: ${f.dataset.say}. You sent <b>${truth}</b>.`;
    });
    render();
  }

  // Prints: colour comes back under the pointer, or where a finger touches.
  document.querySelectorAll('[data-reveal]').forEach((fig) => {
    const frame = fig.querySelector('.print__frame');
    const set = (e) => {
      const b = frame.getBoundingClientRect();
      frame.style.setProperty('--x', `${e.clientX - b.left}px`);
      frame.style.setProperty('--y', `${e.clientY - b.top}px`);
    };
    frame.addEventListener('pointerenter', (e) => { set(e); fig.classList.add('is-looking'); });
    frame.addEventListener('pointermove', set);
    frame.addEventListener('pointerleave', () => fig.classList.remove('is-looking'));
    frame.addEventListener('pointerdown', (e) => { set(e); fig.classList.add('is-looking'); });
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
    s.querySelectorAll('.reveal').forEach((el, i) => el.style.setProperty('--d', `${Math.min(i, 6) * 80}ms`));
  });
  const io = new IntersectionObserver((es) => {
    for (const e of es) if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach((el) => io.observe(el));
})();
