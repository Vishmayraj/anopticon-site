// Anopticon: the sea of reports, the lens, and section entrances.
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  requestAnimationFrame(() => document.body.classList.add('is-loaded'));

  // Entrances: each section's parts arrive in order, once.
  document.querySelectorAll('section').forEach((s) => {
    s.querySelectorAll('.reveal').forEach((el, i) => el.style.setProperty('--d', `${Math.min(i, 6) * 80}ms`));
  });
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  document.querySelectorAll('.reveal, .proj').forEach((el) => io.observe(el));

  // The sea. An illustration, not data: ships move along lanes and broadcast reports. During an
  // incident some reports are pulled onto one impossible spot. Outside the lens every report looks
  // the same; inside it, the poisoned ones are tied back to where the ship really was.
  const canvas = document.getElementById('sea');
  if (!canvas) return;
  const hero = canvas.parentElement;
  const ctx = canvas.getContext('2d');
  const C = {
    ink2: '#181C23', paper: '#FAF9F5', mist: 'rgba(169,175,184,', signal: '#FF6A4D', ok: '#4CC38A',
  };
  const TRAIL = 9;

  let W = 0, H = 0, dpr = 1;
  let lanes = [], ships = [];
  let incident = null, nextIncident = 1.2;
  const lens = { x: 0, y: 0, tx: 0, ty: 0, r: 160, user: false };
  let t = 0;

  const rand = (a, b) => a + Math.random() * (b - a);

  function laneY(l, x) { return l.y0 + l.a * Math.sin(x * l.f + l.p) + l.tilt * (x - W / 2); }

  function build() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = hero.clientWidth; H = hero.clientHeight;
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    const narrow = W < 700;
    const nLanes = narrow ? 6 : 9;
    lanes = Array.from({ length: nLanes }, (_, i) => ({
      y0: H * (0.11 + (narrow ? 0.42 : 0.46) * (i + rand(0.1, 0.9)) / nLanes),
      a: rand(8, H * 0.045), f: rand(0.002, 0.006), p: rand(0, 6.28), tilt: rand(-0.08, 0.08),
    }));
    const perLane = narrow ? 6 : 9;
    ships = [];
    lanes.forEach((l) => {
      for (let k = 0; k < perLane; k++) {
        const dir = Math.random() < 0.5 ? 1 : -1;
        ships.push({
          l, dir, x: rand(-40, W + 40), off: rand(-7, 7),
          v: rand(14, 34) * (narrow ? 0.7 : 1),
          every: rand(0.45, 0.8), clock: rand(0, 0.8),
          reports: [], hit: false,
        });
      }
    });
    lens.r = Math.max(110, Math.min(180, W * 0.14));
    if (!lens.user) { lens.x = lens.tx = W * 0.62; lens.y = lens.ty = H * 0.34; }
  }

  function startIncident() {
    const cx = rand(W * 0.5, W * 0.86), cy = rand(H * 0.14, H * 0.4);
    incident = { cx, cy, age: 0, life: rand(6, 8) };
    ships.forEach((s) => { s.hit = Math.random() < 0.38; });
  }

  function step(dt) {
    t += dt;
    if (incident) {
      incident.age += dt;
      if (incident.age > incident.life) { incident = null; nextIncident = rand(2.5, 4); ships.forEach((s) => { s.hit = false; }); }
    } else if ((nextIncident -= dt) <= 0) startIncident();

    for (const s of ships) {
      s.x += s.dir * s.v * dt;
      if (s.x > W + 60) s.x = -60, s.reports = [];
      if (s.x < -60) s.x = W + 60, s.reports = [];
      s.clock += dt;
      if (s.clock >= s.every) {
        s.clock = 0;
        const tx = s.x, ty = laneY(s.l, s.x) + s.off;
        let rx = tx, ry = ty, bad = false;
        if (incident && s.hit) {
          const k = Math.min(1, incident.age / 1.4) * Math.min(1, (incident.life - incident.age) / 0.8);
          if (k > 0.05) {
            bad = true;
            rx = tx + (incident.cx + rand(-14, 14) - tx) * k;
            ry = ty + (incident.cy + rand(-14, 14) - ty) * k;
          }
        }
        s.reports.push({ rx, ry, tx, ty, bad });
        if (s.reports.length > TRAIL) s.reports.shift();
      }
    }

    if (!lens.user) {
      lens.tx = W * (0.62 + 0.22 * Math.sin(t * 0.17)) ;
      lens.ty = H * (0.36 + 0.16 * Math.sin(t * 0.23 + 1));
      if (incident && incident.age > 1.4) { lens.tx = lens.tx * 0.5 + incident.cx * 0.5; lens.ty = lens.ty * 0.5 + incident.cy * 0.5; }
    }
    const ease = 1 - Math.pow(0.0015, dt);
    lens.x += (lens.tx - lens.x) * ease;
    lens.y += (lens.ty - lens.y) * ease;
  }

  const inLens = (x, y) => (x - lens.x) ** 2 + (y - lens.y) ** 2 < lens.r * lens.r;

  function draw() {
    ctx.clearRect(0, 0, W, H);

    // What everyone sees: reports, all alike.
    ctx.lineWidth = 1;
    for (const s of ships) {
      const r = s.reports;
      if (r.length < 2) continue;
      ctx.strokeStyle = C.mist + '0.28)';
      ctx.beginPath(); ctx.moveTo(r[0].rx, r[0].ry);
      for (let i = 1; i < r.length; i++) ctx.lineTo(r[i].rx, r[i].ry);
      ctx.stroke();
      for (let i = 0; i < r.length; i++) {
        ctx.fillStyle = C.mist + (0.25 + 0.65 * i / r.length) + ')';
        ctx.fillRect(r[i].rx - 1.5, r[i].ry - 1.5, 3, 3);
      }
    }

    // What the lens sees.
    ctx.save();
    ctx.beginPath(); ctx.arc(lens.x, lens.y, lens.r, 0, Math.PI * 2);
    ctx.fillStyle = C.ink2; ctx.fill();
    ctx.clip();
    ctx.fillStyle = 'rgba(169,175,184,0.18)';
    for (let gx = Math.floor((lens.x - lens.r) / 24) * 24; gx < lens.x + lens.r; gx += 24)
      for (let gy = Math.floor((lens.y - lens.r) / 24) * 24; gy < lens.y + lens.r; gy += 24) ctx.fillRect(gx, gy, 1.5, 1.5);

    let bad = 0, checked = 0;
    for (const s of ships) {
      const r = s.reports;
      if (!r.length) continue;
      // The true track, solid.
      ctx.strokeStyle = 'rgba(250,249,245,0.55)'; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(r[0].tx, r[0].ty);
      for (let i = 1; i < r.length; i++) ctx.lineTo(r[i].tx, r[i].ty);
      ctx.stroke();
      for (const p of r) {
        const seen = inLens(p.rx, p.ry) || inLens(p.tx, p.ty);
        if (!seen) continue;
        checked++;
        if (p.bad) {
          bad++;
          ctx.strokeStyle = C.signal; ctx.lineWidth = 1.5; ctx.setLineDash([4, 4]);
          ctx.beginPath(); ctx.moveTo(p.rx, p.ry); ctx.lineTo(p.tx, p.ty); ctx.stroke();
          ctx.setLineDash([]);
          ctx.fillStyle = C.signal; ctx.beginPath(); ctx.arc(p.rx, p.ry, 3.5, 0, 6.283); ctx.fill();
          ctx.strokeStyle = C.paper; ctx.beginPath(); ctx.arc(p.tx, p.ty, 5, 0, 6.283); ctx.stroke();
        } else {
          ctx.fillStyle = C.ok; ctx.fillRect(p.tx - 2, p.ty - 2, 4, 4);
        }
      }
    }
    ctx.restore();

    // The ring and its count.
    ctx.strokeStyle = C.paper; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(lens.x, lens.y, lens.r, 0, Math.PI * 2); ctx.stroke();
    ctx.font = '500 13px "IBM Plex Mono", monospace';
    ctx.textBaseline = 'bottom';
    const label = `${checked} checked  ${bad} poisoned`;
    const lw = ctx.measureText(label).width;
    const lx = Math.max(8, Math.min(W - lw - 8, lens.x - lw / 2)), ly = lens.y - lens.r - 10;
    ctx.fillStyle = C.paper; ctx.fillText(`${checked} checked`, lx, ly);
    ctx.fillStyle = bad ? C.signal : C.mist + '0.8)';
    ctx.fillText(`${bad} poisoned`, lx + ctx.measureText(`${checked} checked  `).width, ly);
  }

  // Pointer: the lens follows a mouse; a tap moves it on touch screens.
  hero.addEventListener('pointermove', (e) => {
    if (e.pointerType !== 'mouse') return;
    const b = hero.getBoundingClientRect();
    lens.tx = e.clientX - b.left; lens.ty = e.clientY - b.top; lens.user = true;
    if (reduce) { lens.x = lens.tx; lens.y = lens.ty; draw(); }
  });
  hero.addEventListener('pointerleave', (e) => { if (e.pointerType === 'mouse') lens.user = false; });
  hero.addEventListener('pointerdown', (e) => {
    if (e.target.closest('a')) return;
    const b = hero.getBoundingClientRect();
    lens.tx = e.clientX - b.left; lens.ty = e.clientY - b.top; lens.user = true;
    if (reduce) { lens.x = lens.tx; lens.y = lens.ty; draw(); }
  });

  let raf = 0, last = 0, visible = true;
  function frame(now) {
    const dt = Math.min(0.05, (now - last) / 1000 || 0.016);
    last = now;
    step(dt); draw();
    raf = visible && !document.hidden ? requestAnimationFrame(frame) : 0;
  }
  const run = () => { if (!raf && !reduce) { last = performance.now(); raf = requestAnimationFrame(frame); } };

  build();
  if (reduce) {
    // One still frame, mid-incident, with the lens over the pile-up.
    for (let i = 0; i < 200; i++) step(0.05);
    startIncident();
    for (let i = 0; i < 60; i++) step(0.05);
    lens.x = incident.cx; lens.y = incident.cy;
    draw();
  } else run();

  new IntersectionObserver((es) => { visible = es[0].isIntersecting; if (visible) run(); }).observe(hero);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) run(); });
  let rt;
  addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => { build(); if (reduce) draw(); }, 150); });
})();
