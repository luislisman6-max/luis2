// VEGETA, EL RIVAL — motor + escenas + efectos + subtítulos (voz 90.96 s)
const END = 91.1;
const tl = gsap.timeline({ paused: true });
const SFX = []; window.SFX = SFX;
const sfx = (t, n, v = 1) => SFX.push([+t.toFixed(3), n, v]);
const root = document.getElementById('root'), ui = document.getElementById('ui');
let seed = 11; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
const R = (a, b) => a + (b - a) * rnd();
const ft = (el, a, b, t) => tl.fromTo(el, a, Object.assign({ immediateRender: false }, b), t);
const $ = id => document.getElementById(id);

// ---------- rigs
const RIGS = {};
function rig(id, ox, oy) { return (RIGS[id] = { x: 0, y: 0, r: 0, s: 1, ox, oy }); }
function applyRigs() {
  for (const k in RIGS) {
    const o = RIGS[k], el = $(k); if (!el) continue;
    el.setAttribute('transform', `translate(${(o.x + o.ox).toFixed(2)},${(o.y + o.oy).toFixed(2)}) rotate(${o.r.toFixed(2)}) scale(${o.s.toFixed(4)}) translate(${-o.ox},${-o.oy})`);
  }
}
// ---------- cámara
const CAM = { x: 0, y: 0, z: 1 }, SHK = { x: 0, y: 0 };
function applyCam() {
  $('camZ').setAttribute('transform', `translate(${CAM.x.toFixed(2)},${CAM.y.toFixed(2)}) scale(${CAM.z.toFixed(4)})`);
  $('camS').setAttribute('transform', `translate(${SHK.x.toFixed(2)},${SHK.y.toFixed(2)})`);
}
function cam(t, cx, cy, z, d = .5, ease = 'power2.inOut') {
  const v = { x: Math.min(0, Math.max(1080 - 1080 * z, 540 - cx * z)), y: Math.min(0, Math.max(1920 - 1920 * z, 960 - cy * z)), z };
  if (d === 0) tl.set(CAM, v, t); else tl.to(CAM, Object.assign(v, { duration: d, ease }), t);
}
function shake(t, d, a) {
  const n = Math.max(2, Math.round(d / .04));
  for (let i = 0; i < n; i++) { const k = 1 - i / n; tl.to(SHK, { x: R(-a, a) * k, y: R(-a, a) * k, duration: .04, ease: 'none' }, t + i * .04); }
  tl.to(SHK, { x: 0, y: 0, duration: .05 }, t + n * .04);
}
function flash(t, col = '#fff', o = .8, d = .3) { tl.set('#flash', { attr: { fill: col } }, t); ft('#flash', { opacity: o }, { opacity: 0, duration: d, ease: 'power2.out' }, t); }

// ---------- utilería
const OLc = '#15121a';
const TXT = (x, y, s, txt, col = '#fff', fam = 'Oswald', ex = '') => `<text x="${x}" y="${y}" font-family="${fam},Impact,sans-serif" font-weight="700" font-size="${s}" fill="${col}" text-anchor="middle" ${ex}>${txt}</text>`;
const STK = 'stroke="#000" stroke-width="8" paint-order="stroke" stroke-linejoin="round"';
function pg(id, cx, cy, inner, vis = false) { rig(id, cx, cy); return `<g id="${id}" ${vis ? '' : 'opacity="0"'}>${inner}</g>`; }
function popS(id, t, snd = 'pop', v = .5, d = .3) { if (snd) sfx(t, snd, v); tl.set('#' + id, { opacity: 1 }, t); ft(RIGS[id], { s: 0 }, { s: 1, duration: d, ease: 'back.out(2.4)' }, t); }
function hideS(id, t, d = .2) { tl.to('#' + id, { opacity: 0, duration: d }, t); }
function scene(id, t0, t1) { tl.set('#' + id, { opacity: 1 }, t0); tl.set('#' + id, { opacity: 0 }, t1); }
function cut(t) { sfx(t, 'whoosh', .45); flash(t, '#fff', .25, .18); }

// personaje: grupo rig con origen en los pies; poses = variantes; flip = mira a la izquierda
function actor(id, o, x, gy, s, poses = ['stand'], extra = '', flip = false) {
  const vs = poses.map((p, i) => `<g class="pv pv${i}" ${i ? 'opacity="0"' : ''}>${typeof o === 'function' ? o() : person(Object.assign({}, o, { pose: p }))}</g>`).join('');
  rig(id, x, gy);
  const tr = flip ? `translate(${x + 200 * s},${gy - 620 * s}) scale(${-s},${s})` : `translate(${x - 200 * s},${gy - 620 * s}) scale(${s})`;
  return `<g id="${id}"><g transform="${tr}">${vs}</g>${extra}</g>`;
}
function pose(id, i, t) { tl.set(`#${id} .pv`, { opacity: 0 }, t); tl.set(`#${id} .pv${i}`, { opacity: 1 }, t); }
const lp = (x, gy, s, lx, ly) => [x + (lx - 200) * s, gy - (620 - ly) * s];
function enter(id, t, dx, dur = .3, snd = 'whoosh') { if (snd) sfx(t, snd, .5); tl.set('#' + id, { opacity: 1 }, t); ft(RIGS[id], { x: dx }, { x: 0, duration: dur, ease: 'power3.out' }, t); }
function show(id, t) { tl.set('#' + id, { opacity: 1 }, t); }
function powerUp(id, t, col = '#ffe14d', snd = true) {
  if (snd) sfx(t, 'powerup', .9);
  flash(t, col, .7, .4); shake(t, .45, 18);
  ft(RIGS[id], { s: 1.12 }, { s: 1, duration: .45, ease: 'power3.out' }, t);
}
function auraPulse(id, t0, t1) { tl.to(`#${id} .aura`, { opacity: .55, duration: .3, yoyo: true, repeat: Math.max(1, Math.floor((t1 - t0) / .3) - 1), ease: 'sine.inOut' }, t0); }
function breathe(id, t0, t1, a = 6) { const n = Math.max(1, Math.floor((t1 - t0) / .8) - 1); tl.to(RIGS[id], { y: a, duration: .8, yoyo: true, repeat: n, ease: 'sine.inOut' }, t0); tl.to(RIGS[id], { y: 0, duration: .2 }, t1 - .2); }
// ciclo de carrera: alterna poses 0/1 con rebote y pasos
function runCycle(id, t0, t1, per = .17, stepVol = .3) {
  let k = 0;
  for (let t = t0; t < t1 - .01; t += per, k++) {
    pose(id, k % 2, t);
    ft(RIGS[id], { y: 0 }, { y: -14, duration: per / 2, ease: 'sine.out', yoyo: true, repeat: 1 }, t);
    if (stepVol && k % 2 === 0) sfx(t + per * .9, 'step', stepVol);
  }
}
// golpe rápido (pose 1) y vuelta a guardia
function strike(id, t, hold = .22, push = 30) {
  sfx(t - .06, 'swish', .5); pose(id, 1, t - .04);
  tl.to(RIGS[id], { x: push, duration: .07, ease: 'power2.out' }, t - .04);
  tl.to(RIGS[id], { x: 0, duration: .18, ease: 'power1.inOut' }, t + hold);
  pose(id, 0, t + hold);
}
function impactFx(id, x, y, col = '#fff') {
  let s = '';
  for (let i = 0; i < 14; i++) { const a = i / 14 * Math.PI * 2, r0 = 40, r1 = R(120, 200); s += `<line x1="${x + Math.cos(a) * r0}" y1="${y + Math.sin(a) * r0}" x2="${x + Math.cos(a) * r1}" y2="${y + Math.sin(a) * r1}" stroke="${col}" stroke-width="${R(6, 12).toFixed(0)}" stroke-linecap="round"/>`; }
  return pg(id, x, y, `<circle cx="${x}" cy="${y}" r="110" fill="url(#yelGlow)"/>${s}<circle cx="${x}" cy="${y}" r="34" fill="#fff"/>`);
}
function boom(id, t, snd = 'impact', v = .9) {
  sfx(t, snd, v); tl.set('#' + id, { opacity: 1 }, t);
  ft(RIGS[id], { s: .3, r: 0 }, { s: 1.15, r: 10, duration: .25, ease: 'power3.out' }, t);
  tl.to('#' + id, { opacity: 0, duration: .15 }, t + .22); shake(t, .25, 14);
}

// ---------- interfaz HTML
function addDiv(cls, html, style = '') { const d = document.createElement('div'); d.className = cls; d.innerHTML = html; if (style) d.setAttribute('style', style); ui.appendChild(d); return d; }
function strokeShadow(r, col = '#000') {
  const s = []; for (let a = 0; a < 360; a += 22.5) s.push(`${(Math.cos(a * Math.PI / 180) * r).toFixed(1)}px ${(Math.sin(a * Math.PI / 180) * r).toFixed(1)}px 0 ${col}`);
  return s.join(',') + `,0 ${r + 4}px ${r + 8}px rgba(0,0,0,.6)`;
}
function popUI(d, t0, t1, snd = 'pop', v = .45) {
  if (snd) sfx(t0, snd, v);
  ft(d, { opacity: 0, scale: .6 }, { opacity: 1, scale: 1, duration: .22, ease: 'back.out(2.6)' }, t0);
  if (t1 != null) tl.to(d, { opacity: 0, duration: .15 }, t1 - .15);
  return d;
}
const pill = (txt, t0, t1, col = '', snd = 'pop') => popUI(addDiv('pill ' + col, `<span>${txt}</span>`), t0, t1, snd);
const lab = (txt, t0, t1, col = '', snd = 'pop') => popUI(addDiv('lab ' + col, `<span>${txt}</span>`), t0, t1, snd);
function big(txt, t0, t1, col = '#ffd23f', size = 190, top = 300) {
  const d = addDiv('big', txt, `color:${col};font-size:${size}px;top:${top}px;text-shadow:${strokeShadow(10)}`);
  ft(d, { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .16, ease: 'power4.in' }, t0);
  tl.to(d, { scale: 1.06, duration: Math.max(.1, t1 - t0 - .3), ease: 'none' }, t0 + .16);
  tl.to(d, { opacity: 0, duration: .14 }, t1 - .14);
  sfx(t0 + .12, 'slam', .7); shake(t0 + .16, .2, 12);
  return d;
}
function stamp(txt, t0, t1, col = '#ff3346', top = 360) {
  const d = addDiv('stamp', `<span style="color:${col};border-color:${col}">${txt}</span>`);
  d.style.top = top + 'px'; popUI(d, t0, t1, 'slam', .8); shake(t0 + .05, .2, 12); return d;
}
function badge(n, txt, t0, t1) { return popUI(addDiv('badge', `<b>${n}</b>${txt}`), t0, t1, 'pop', .6); }

// ---------- defs y fondos
const defs = `<defs>
<filter id="blur8" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="blur20" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="20"/></filter>
<filter id="glowB" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="clipR"><rect x="214" y="-100" width="300" height="400"/></clipPath>
<pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M60,0 L0,0 L0,60" fill="none" stroke="#1f2a44" stroke-width="2"/></pattern>
<radialGradient id="floorSh"><stop offset="0" stop-color="#000" stop-opacity=".6"/><stop offset="1" stop-opacity="0"/></radialGradient>
<radialGradient id="yelGlow"><stop offset="0" stop-color="#fff3b0" stop-opacity=".95"/><stop offset="1" stop-color="#ffb800" stop-opacity="0"/></radialGradient>
<radialGradient id="purGlow"><stop offset="0" stop-color="#e48bff" stop-opacity=".9"/><stop offset="1" stop-color="#7a1fa0" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx="50%" cy="48%" r="75%"><stop offset=".6" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5b8fd6"/><stop offset=".7" stop-color="#f2b46a"/><stop offset="1" stop-color="#f7d08a"/></linearGradient>
<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0a22"/><stop offset="1" stop-color="#24204e"/></linearGradient>
<linearGradient id="stadium" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0f1a3a"/><stop offset="1" stop-color="#28407a"/></linearGradient>
</defs>`;
let GID = 0;
function radBg(c0, c1, line, floor = '#000') {
  const id = 'rg' + (GID++);
  let s = `<defs><radialGradient id="${id}" cx="50%" cy="45%" r="75%"><stop offset="0" stop-color="${c0}"/><stop offset="1" stop-color="${c1}"/></radialGradient></defs><rect width="1080" height="1920" fill="url(#${id})"/>`;
  for (let i = 0; i < 44; i++) { const a = i / 44 * Math.PI * 2 + R(-.05, .05), r0 = R(300, 460); s += `<line x1="${(540 + Math.cos(a) * r0).toFixed(0)}" y1="${(860 + Math.sin(a) * r0).toFixed(0)}" x2="${(540 + Math.cos(a) * 1500).toFixed(0)}" y2="${(860 + Math.sin(a) * 1500).toFixed(0)}" stroke="${line}" stroke-width="${R(2, 6).toFixed(1)}" opacity="${R(.2, .5).toFixed(2)}"/>`; }
  return s + `<rect y="1430" width="1080" height="490" fill="${floor}" opacity=".55"/><rect y="1428" width="1080" height="6" fill="#000" opacity=".5"/>`;
}
function wasteland() {
  let s = `<rect width="1080" height="1920" fill="url(#sky)"/><circle cx="820" cy="420" r="90" fill="#fff4d0" opacity=".8"/>`;
  s += `<path d="M0,1100 L80,980 L60,820 L190,800 L210,1000 L330,1060 L420,900 L560,880 L600,1080 L760,1040 L800,760 L960,740 L990,1000 L1080,1020 L1080,1430 L0,1430 Z" fill="#c9824e" stroke="#7a4424" stroke-width="5"/>`;
  s += `<path d="M60,820 L190,800 L196,860 L66,880 Z M800,760 L960,740 L966,800 L806,820 Z" fill="#e0a06a"/>`;
  s += `<rect y="1300" width="1080" height="620" fill="#d89a5e"/><rect y="1430" width="1080" height="490" fill="#b97a44"/>`;
  for (let i = 0; i < 14; i++) s += `<ellipse cx="${R(0, 1080).toFixed(0)}" cy="${R(1460, 1880).toFixed(0)}" rx="${R(20, 60).toFixed(0)}" ry="${R(6, 14).toFixed(0)}" fill="#8f5a2e" opacity=".5"/>`;
  return s;
}
function nightBg() {
  let s = `<rect width="1080" height="1920" fill="url(#night)"/>`;
  for (let i = 0; i < 40; i++) s += `<circle cx="${R(0, 1080).toFixed(0)}" cy="${R(0, 700).toFixed(0)}" r="${R(1, 2.6).toFixed(1)}" fill="#fff" opacity="${R(.3, .8).toFixed(2)}"/>`;
  let x = -20;
  while (x < 1100) {
    const w = R(90, 170), h = R(300, 700), y = 1430 - h;
    s += `<rect x="${x.toFixed(0)}" y="${y.toFixed(0)}" width="${w.toFixed(0)}" height="${h.toFixed(0)}" fill="#15123a" stroke="#0a0820" stroke-width="4"/>`;
    for (let wy = y + 30; wy < 1400; wy += 50) for (let wx = x + 16; wx < x + w - 26; wx += 38) if (rnd() > .6) s += `<rect x="${wx.toFixed(0)}" y="${wy.toFixed(0)}" width="18" height="24" fill="#f5c84c" opacity=".5"/>`;
    x += w + R(4, 18);
  }
  return s + `<rect y="1430" width="1080" height="490" fill="#0d0b22"/>`;
}
// pista de atletismo en perspectiva (líneas que corren hacia la cámara)
function track(p) {
  let s = `<rect width="1080" height="1920" fill="url(#stadium)"/>`;
  // gradas con público
  s += `<rect y="420" width="1080" height="420" fill="#1b2546"/>`;
  for (let r = 0; r < 9; r++) for (let c = 0; c < 30; c++) s += `<circle cx="${(c * 37 + (r % 2) * 18 + R(-4, 4)).toFixed(0)}" cy="${(450 + r * 44).toFixed(0)}" r="13" fill="${['#e0583c', '#f2c94c', '#5fb0ff', '#e8e4da', '#8f6bd8'][Math.floor(R(0, 5))]}" opacity=".55"/>`;
  s += `<rect y="836" width="1080" height="14" fill="#e8e4da"/>`;
  for (let i = 0; i < 5; i++) s += `<circle cx="${120 + i * 210}" cy="250" r="34" fill="#fff8d0" opacity=".9"/><circle cx="${120 + i * 210}" cy="250" r="90" fill="#fff8d0" opacity=".12"/>`;
  // pista
  s += `<path d="M380,850 L700,850 L1300,1920 L-220,1920 Z" fill="#c0482f"/><rect y="850" width="1080" height="1070" fill="#3d8a4a" opacity="0"/>`;
  s += `<path d="M0,850 L380,850 L-220,1920 L0,1920 Z M700,850 L1080,850 L1080,1920 L1300,1920 Z" fill="#2f7a3e"/>`;
  for (const k of [0, .25, .5, .75, 1]) { const x0 = 380 + 320 * k, x1 = -220 + 1520 * k; s += `<line x1="${x0}" y1="850" x2="${x1}" y2="1920" stroke="#f4efe2" stroke-width="5"/>`; }
  // marcas que se acercan (animadas)
  let m = '';
  for (let i = 0; i < 7; i++) m += `<rect class="tm" x="0" y="0" width="1080" height="10" fill="#f4efe2" opacity=".55"/>`;
  return s + `<g id="${p}marks">${m}</g>`;
}
function trackRun(p, t0, t1) {
  // las marcas horizontales bajan en perspectiva para dar sensación de velocidad
  document.querySelectorAll(`#${p}marks .tm`).forEach((el, i) => {
    const per = .9, off = i / 7 * per;
    for (let t = t0 - off; t < t1; t += per) {
      if (t + per < t0) continue;
      ft(el, { attr: { y: 850, height: 3 }, opacity: .2 }, { attr: { y: 1920, height: 30 }, opacity: .7, duration: per, ease: 'power2.in' }, Math.max(0, t));
    }
  });
}
const flr = (x, y, rx = 200) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="26" fill="url(#floorSh)"/>`;
function speedLines(id, col = '#fff') {
  let s = ''; for (let i = 0; i < 26; i++) { const y = R(300, 1400), x = R(-100, 900), w = R(200, 520); s += `<rect class="sl" x="${x.toFixed(0)}" y="${y.toFixed(0)}" width="${w.toFixed(0)}" height="${R(4, 10).toFixed(0)}" rx="4" fill="${col}" opacity="${R(.3, .7).toFixed(2)}"/>`; }
  return `<g id="${id}" opacity="0">${s}</g>`;
}
function zoomLines(t0, t1, id) { tl.set('#' + id, { opacity: 1 }, t0); ft(`#${id} .sl`, { x: 300 }, { x: -700, duration: t1 - t0, ease: 'none' }, t0); tl.set('#' + id, { opacity: 0 }, t1); }

// ---------- personajes (mismas opciones que la hoja de personajes)
const OG = { ...GI, top: 'goku', emblem: '悟', skin: GSKIN, hair: 'goku', hairC: '#17151a', hairHi: '#6c6a80', iris: '#1d1c22', mouth: 'smile' };
const OG_SSJ = { ...GI, top: 'goku', emblem: '亀', skin: GSKIN, hair: 'ssj', hairC: '#ffd23a', hairHi: '#fff6c4', brow: '#e0a91c', iris: '#18a39a', angry: true, mouth: 'grit', aura: '#ffd84a' };
const OG_DIOS = { ...GI, top: 'goku', emblem: '悟', skin: '#f3c9a2', hair: 'goku', hairScale: .9, hairC: '#d6283f', hairHi: '#ff8a9a', brow: '#b81f33', iris: '#c4283a', calm: true, aura: '#ff3d5a', auraOp: .4 };
const OG_BLUE = { ...GI, top: 'goku', emblem: '悟', skin: GSKIN, hair: 'ssj', hairC: '#39b6f2', hairHi: '#c9f0ff', brow: '#1f8fd0', iris: '#2a7fd8', angry: true, mouth: 'smirk', aura: '#3fc3ff' };
const OG_UI = { ...GI, top: 'bare', topC: GSKIN, abs: true, sleeve: 'none', skin: GSKIN, hair: 'ui', hairC: '#dfe3ee', hairHi: '#ffffff', brow: '#aab3c6', iris: '#b9c3d6', noPupil: true, calm: true, aura: '#cfd8ff', auraOp: .35 };
const OV = { ...SAIYAN, armor: '#e6b43a', pads: '#e6b43a', skin: GSKIN, hair: 'vegeta', hairC: '#17151a', hairHi: '#6c6a80', iris: '#1d1c22', angry: true, mouth: 'smirk' };
const OV_SSJ = { ...OV, hairC: '#ffd23a', hairHi: '#fff6c4', brow: '#e0a91c', iris: '#18a39a', aura: '#ffd84a', auraOp: .4 };
const OV_BLUE = { ...SAIYAN, armor: '#e6b43a', skin: GSKIN, hair: 'vegeta', hairC: '#39b6f2', hairHi: '#c9f0ff', brow: '#1f8fd0', iris: '#2a7fd8', angry: true, mouth: 'grit', aura: '#3fc3ff' };
const OV_MAJIN = { ...SAIYAN, sleeve: 'none', skin: GSKIN, hair: 'vegeta', hairC: '#ffd23a', hairHi: '#fff6c4', brow: '#e0a91c', iris: '#18a39a', angry: true, veins: true, majinM: true, mouth: 'smirk', aura: '#ffd84a', auraOp: .4 };
const OWHIS = { topC: '#6e1d2c', bottom: '#6e1d2c', robe: '#17151c', sleeve: 'long', cuff: '#17151c', skin: '#a8c3e8', shoes: '#f4f2ec', hair: 'none', iris: '#7b4fc0', calm: true, mouth: 'smile', lips: '#7b4fc0', ring: '#2f9be6', headExtra: whisHair, over: whisStaff };
const OTU = { top: 'tank', topC: '#d8323a', bottom: '#b67b52', bare: true, shorts: '#1f2026', skin: '#b67b52', hair: 'none', headExtra: `<path d="M153,144 Q148,84 200,82 Q252,84 247,144 Q240,112 200,110 Q160,112 153,144 Z" fill="#1f1b22" stroke="${OL}" stroke-width="3"/>`, iris: '#1d1c22', bib: '07', shoes: '#f4f2ec', sole: '#d8323a', angry: true, mouth: 'grit' };
const ORIV = { top: 'tank', topC: '#2f74c8', bottom: '#e0b48a', bare: true, shorts: '#1f2026', skin: '#e0b48a', hair: 'none', headExtra: `<path d="M152,146 Q144,76 200,74 Q258,76 248,146 Q246,108 228,100 L222,118 L210,98 L196,118 L186,98 L174,116 Q156,112 152,146 Z" fill="#5a3a22" stroke="${OL}" stroke-width="3"/>`, iris: '#1d1c22', bib: '23', shoes: '#f4f2ec', sole: '#2f74c8', angry: true, mouth: 'smirk' };

// =============================================================== ESCENAS (markup)
let M = defs + `<g id="camS"><g id="camZ">`;
const GY = 1430;
// 1 y 16 · gancho / final en bucle: Goku Ultra Instinto + entra Vegeta
function hook(p) {
  return `<g id="${p}" opacity="0">${radBg('#3a3f6e', '#0b0c1c', '#cfd8ff', '#05060f')}${flr(540, GY + 4, 260)}
    ${actor(p + 'G', OG_UI, 540, GY, 1.62, ['stand'])}
    <g id="${p}Vw" opacity="0">${actor(p + 'V', OV, 800, GY, 1.38, ['cross'])}</g></g>`;
}
M += hook('s1');
// sello "LA CIENCIA" (matraz)
M += pg('s1sci', 540, 560, `<circle cx="540" cy="560" r="150" fill="url(#yelGlow)" opacity=".6"/><path d="M500,440 L500,520 L430,650 Q420,680 450,680 L630,680 Q660,680 650,650 L580,520 L580,440 Z" fill="#d6f4ff" stroke="#000" stroke-width="8" stroke-linejoin="round"/><path d="M462,600 L618,600 L650,652 Q656,672 632,672 L448,672 Q424,672 430,652 Z" fill="#3fd17a"/><rect x="486" y="426" width="108" height="24" rx="8" fill="#9aa4b8" stroke="#000" stroke-width="6"/><circle cx="520" cy="630" r="10" fill="#fff" opacity=".8"/><circle cx="560" cy="648" r="7" fill="#fff" opacity=".8"/>`);
// 2 · Vegeta lo alcanza, Goku sube de nivel
M += `<g id="s2" opacity="0">${wasteland()}${flr(330, GY + 4)}${flr(780, GY + 4)}
  ${actor('s2V', OV, 780, GY, 1.25, ['stand', 'guard'], '', true)}
  ${actor('s2G', OG, 330, GY, 1.3, ['stand'])}${actor('s2G2', OG_SSJ, 330, GY, 1.3, ['guard'])}
  ${speedLines('s2sl')}
  ${pg('s2up', 330, 470, `<path d="M330,560 L330,420" stroke="#ffd23f" stroke-width="20" stroke-linecap="round"/><path d="M280,470 L330,410 L380,470" fill="none" stroke="#ffd23f" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>`)}</g>`;
// 3 · escalera de transformaciones
const STEP = i => ({ x: 20 + i * 240, y: 1520 - i * 225 });
let stairs = '';
for (let i = 0; i < 4; i++) { const { x, y } = STEP(i); stairs += `<rect x="${x}" y="${y}" width="262" height="${1920 - y}" fill="${['#3a2f6b', '#46397f', '#524393', '#5e4da7'][i]}" stroke="#120d2a" stroke-width="6"/><rect x="${x}" y="${y}" width="262" height="18" fill="#fff" opacity=".18"/>`; }
const GFORMS = [OG_SSJ, OG_DIOS, OG_BLUE, OG_UI], GNAMES = ['SUPER SAIYAJIN', 'DIOS', 'BLUE', 'ULTRA INSTINTO'], GCOL = ['#ffd23a', '#ff4a5a', '#39b6f2', '#e6ebf5'];
M += `<g id="s3" opacity="0">${radBg('#4a3a8a', '#120c2a', '#ffd23f', '#120c2a')}${stairs}
  ${GFORMS.map((o, i) => { const { x, y } = STEP(i); return `<g id="s3g${i}w" opacity="0">${actor('s3g' + i, o, x + 132, y, .74, [i % 2 ? 'stand' : 'guard'])}</g>`; }).join('')}
  ${[OV, OV_BLUE, OV_BLUE].map((o, i) => { const { x, y } = STEP(i); return `<g id="s3v${i}w" opacity="0">${actor('s3v' + i, o, x + 96, y, .68, ['guard'])}</g>`; }).join('')}
  ${pg('s3loop', 540, 900, `<path d="M380,760 A200,200 0 1,1 380,1040" fill="none" stroke="#ffd23f" stroke-width="18" stroke-linecap="round"/><path d="M340,1000 L380,1046 L420,1004" fill="none" stroke="#ffd23f" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>`)}
</g>`;
// 4 · cara a cara: RIVALIDAD
let bolt = '';
for (let i = 0; i < 3; i++) { let y = 560 + i * 18, d = `M540,${y}`; for (let k = 1; k <= 8; k++) { y += 100; d += ` L${(540 + R(-50, 50)).toFixed(0)},${y}`; } bolt += `<path d="${d}" fill="none" stroke="${i ? '#7fdcff' : '#fff'}" stroke-width="${i ? 6 : 12}" stroke-linejoin="round" filter="url(#glowB)"/>`; }
M += `<g id="s4" opacity="0"><rect width="540" height="1920" fill="#e8742a"/><rect x="540" width="540" height="1920" fill="#22346f"/>${radBg('#ffffff00', '#00000088', '#fff', '#000').replace('<rect width="1080" height="1920"', '<rect width="1080" height="1920" opacity=".55"')}
  ${actor('s4G', OG, 290, GY, 1.32, ['guard'])}${actor('s4V', OV, 800, GY, 1.32, ['guard'], '', true)}
  <g id="s4b" opacity="0">${bolt}</g>${pg('s4vs', 540, 1000, `<circle cx="540" cy="1000" r="92" fill="#ffd23f" stroke="#000" stroke-width="10"/>${TXT(540, 1036, 100, 'VS', '#000', 'Anton')}`)}</g>`;
// 5 · universidad de Nueva York
M += `<g id="s5" opacity="0">${nightBg()}
  <g id="s5uni"><path d="M240,760 L540,600 L840,760 Z" fill="#d9d2c0" stroke="#000" stroke-width="8" stroke-linejoin="round"/><rect x="250" y="760" width="580" height="40" fill="#cfc8b4" stroke="#000" stroke-width="7"/>
   ${[0, 1, 2, 3, 4, 5].map(i => `<rect x="${280 + i * 92}" y="800" width="46" height="500" fill="#ebe5d6" stroke="#000" stroke-width="6"/>`).join('')}<rect x="230" y="1300" width="620" height="60" fill="#cfc8b4" stroke="#000" stroke-width="7"/><rect x="200" y="1360" width="680" height="70" fill="#bdb5a0" stroke="#000" stroke-width="7"/>
   ${TXT(540, 730, 46, 'UNIVERSIDAD', '#3a3426', 'Oswald')}<rect x="500" y="660" width="80" height="12" fill="#3a3426" opacity=".3"/></g>
  ${pg('s5clip', 820, 1040, `<g transform="rotate(8 820 1040)"><rect x="680" y="840" width="280" height="380" rx="16" fill="#8a5a2e" stroke="#000" stroke-width="8"/><rect x="705" y="880" width="230" height="320" fill="#fbf7ea" stroke="#000" stroke-width="5"/><rect x="770" y="824" width="100" height="40" rx="8" fill="#b8bcc6" stroke="#000" stroke-width="6"/>
     <polyline points="725,1160 770,1110 810,1130 850,1050 905,980" fill="none" stroke="#e0283a" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>${[0, 1, 2].map(i => `<rect x="725" y="${910 + i * 34}" width="${170 - i * 30}" height="10" rx="5" fill="#9aa"/>`).join('')}</g>`)}
  ${pg('s5ok', 940, 860, `<circle cx="940" cy="860" r="56" fill="#22b35a" stroke="#fff" stroke-width="8"/><path d="M912,860 L934,884 L972,836" fill="none" stroke="#fff" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>`)}</g>`;
// 6 · miles de resultados
const NAMES = ['M. GARCÍA', 'J. SMITH', 'A. ROSSI', 'L. CHEN', 'K. MÜLLER', 'P. SILVA', 'T. KIM', 'R. DIAZ', 'S. COHEN', 'E. NAKA'];
M += `<g id="s6" opacity="0">${track('s6')}<rect width="1080" height="1920" fill="#000" opacity=".45"/>
  <g id="s6tab"><rect x="90" y="400" width="900" height="900" rx="24" fill="#0c1226" stroke="#5fb0ff" stroke-width="5"/>${TXT(540, 470, 48, 'RESULTADOS · CARRERAS', '#5fb0ff')}
   <clipPath id="s6clip"><rect x="110" y="500" width="860" height="780"/></clipPath><g clip-path="url(#s6clip)"><g id="s6rows">
   ${Array.from({ length: 40 }, (_, i) => `<g><rect x="120" y="${510 + i * 78}" width="840" height="64" rx="10" fill="${i % 2 ? '#141c36' : '#18213f'}"/>${TXT(190, 553 + i * 78, 32, String(i + 1).padStart(2, '0'), '#7b8ab8')}${TXT(420, 553 + i * 78, 32, NAMES[i % 10], '#e8eef8')}${TXT(800, 553 + i * 78, 32, `${4 + (i % 3)}:${String(10 + (i * 7) % 50).padStart(2, '0')} /KM`, '#ffd23f')}</g>`).join('')}</g></g></g>
  ${pg('s6cnt', 540, 1380, `<rect x="300" y="1330" width="480" height="96" rx="18" fill="#ffd23f" stroke="#000" stroke-width="6"/><text id="s6num" x="540" y="1402" font-family="Anton" font-size="68" text-anchor="middle" fill="#000">0</text>`)}</g>`;
// 7 · la carrera con el rival
const TX = 540, TS = 1.25;
M += `<g id="s7" opacity="0">${track('s7')}${speedLines('s7sl')}${flr(TX, GY + 6, 220)}
  <g id="s7Rw" opacity="0">${flr(820, GY + 6, 200)}${actor('s7R', ORIV, 820, GY, TS, ['run2', 'run'])}</g>
  ${actor('s7T', OTU, TX, GY, TS, ['run', 'run2'])}
  ${pg('s7tag', 820, 560, `<path d="M820,640 L800,606 L840,606 Z" fill="#2f74c8" stroke="#000" stroke-width="5"/><rect x="700" y="520" width="240" height="90" rx="16" fill="#2f74c8" stroke="#000" stroke-width="6"/>${TXT(820, 584, 56, 'RIVAL', '#fff', 'Anton')}`)}
  ${pg('s7ring', 820, 1000, `<ellipse cx="820" cy="1000" rx="250" ry="470" fill="none" stroke="#ffd23f" stroke-width="12" stroke-dasharray="30 18"/>`)}
  ${pg('s7clk', 230, 640, `<circle cx="230" cy="640" r="110" fill="#f6f3ea" stroke="#000" stroke-width="10"/><rect x="205" y="500" width="50" height="36" rx="8" fill="#ddd" stroke="#000" stroke-width="6"/>${pg('s7hand', 230, 640, `<line x1="230" y1="640" x2="230" y2="555" stroke="#e0283a" stroke-width="10" stroke-linecap="round"/><circle cx="230" cy="640" r="12" fill="#000"/>`, true)}`)}
</g>`;
// 8 · no peleas por una medalla, peleas por tu orgullo
M += `<g id="s8" opacity="0">${radBg('#2a3c7a', '#070a1c', '#ffd23f', '#070a1c')}
  ${pg('s8med', 540, 860, `<path d="M440,520 L500,760 L560,760 L500,520 Z" fill="#d8323a" stroke="#000" stroke-width="7"/><path d="M640,520 L580,760 L520,760 L580,520 Z" fill="#2f74c8" stroke="#000" stroke-width="7"/><circle cx="540" cy="900" r="170" fill="url(#yelGlow)" opacity=".6"/><circle cx="540" cy="900" r="130" fill="#f2c13a" stroke="#000" stroke-width="10"/><circle cx="540" cy="900" r="92" fill="none" stroke="#b8860b" stroke-width="8"/>${TXT(540, 945, 120, '1', '#8a5a00', 'Anton')}`)}
  ${pg('s8x', 540, 860, `<path d="M380,700 L700,1060 M700,700 L380,1060" stroke="#ff2d40" stroke-width="46" stroke-linecap="round" ${STK}/>`)}</g>`;
M += `<g id="s9" opacity="0">${radBg('#3a4ea0', '#0a0f2a', '#ffd23f', '#0a0f2a')}${flr(540, GY + 4, 240)}${actor('s9V', OV, 540, GY, 1.5, ['cross'])}
  ${pg('s9crown', 540, 400, `<path d="M440,450 L450,340 L500,400 L540,320 L580,400 L630,340 L640,450 Z" fill="#ffd23f" stroke="#000" stroke-width="8" stroke-linejoin="round"/><circle cx="540" cy="410" r="14" fill="#e0283a" stroke="#000" stroke-width="4"/>`)}</g>`;
// 10 · lado oscuro y trampa
M += `<g id="s10" opacity="0">${radBg('#3a1050', '#08020f', '#a040ff', '#08020f')}
  ${pg('s10warn', 540, 820, `<path d="M540,560 L780,980 L300,980 Z" fill="#ffd23f" stroke="#000" stroke-width="14" stroke-linejoin="round"/>${TXT(540, 930, 280, '!', '#000', 'Anton')}`)}
  ${pg('s10chart', 540, 670, `<g transform="translate(0,-90)"><rect x="160" y="420" width="760" height="560" rx="24" fill="#120820" stroke="#a040ff" stroke-width="5"/>${TXT(540, 490, 44, 'GANAS DE HACER TRAMPA', '#e48bff')}
     <line x1="230" y1="920" x2="850" y2="920" stroke="#5a3a7a" stroke-width="5"/>
     <rect x="290" y="760" width="180" height="160" fill="#6f5a8a" stroke="#000" stroke-width="5"/>${TXT(380, 960, 32, 'SIN RIVAL', '#cbb8e8')}
     <rect id="s10bar" x="610" y="540" width="180" height="380" fill="#ff2d40" stroke="#000" stroke-width="5"/>${TXT(700, 960, 32, 'CON RIVAL', '#ff6b78')}</g>`)}
  ${flr(330, GY + 4)}${flr(750, GY + 4)}<g id="s10rw" opacity="0">${actor('s10T', OTU, 330, GY, .95, ['stand'])}${actor('s10R', ORIV, 750, GY, .95, ['stand'], '', true)}</g></g>`;
// 11 · Babidi controla a Vegeta
let rings = ''; for (let i = 0; i < 5; i++) rings += `<ellipse class="mr" cx="0" cy="0" rx="${40 + i * 6}" ry="${16 + i * 3}" fill="none" stroke="#e48bff" stroke-width="7" opacity="0"/>`;
M += `<g id="s11" opacity="0">${radBg('#3a1a5a', '#0c0418', '#b040ff', '#0c0418')}${flr(250, GY + 4, 160)}${flr(580, GY + 4, 230)}${flr(910, GY + 4, 160)}
  <g id="s11bw" opacity="0">${actor('s11B', babidi, 240, GY, .82)}</g>
  ${actor('s11V', OV, 580, GY, 1.38, ['cross'])}${actor('s11M', OV_MAJIN, 580, GY, 1.38, ['guard'])}
  <g id="s11gw" opacity="0">${actor('s11G', OG, 910, GY, .95, ['guard'], '', true)}</g>
  <g id="s11rings">${rings}</g>
  ${pg('s11m', 580, 700, `<circle cx="580" cy="700" r="260" fill="url(#purGlow)"/>`)}</g>`;
// 12 · ¿cómo usas a tu propio Vegeta sin volverte Majin?
M += `<g id="s12" opacity="0"><rect width="540" height="1920" fill="#1b2a5e"/><rect x="540" width="540" height="1920" fill="#3a1050"/><rect x="532" width="16" height="1920" fill="#000"/>
  ${flr(280, GY + 4, 180)}${flr(800, GY + 4, 180)}${actor('s12V', OV, 280, GY, 1.12, ['cross'])}${actor('s12M', OV_MAJIN, 800, GY, 1.12, ['guard'])}
  ${pg('s12ok', 280, 560, `<circle cx="280" cy="560" r="80" fill="#22b35a" stroke="#fff" stroke-width="10"/><path d="M240,560 L270,594 L326,530" fill="none" stroke="#fff" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>`)}
  ${pg('s12no', 800, 560, `<circle cx="800" cy="560" r="80" fill="#e0283a" stroke="#fff" stroke-width="10"/><path d="M760,520 L840,600 M840,520 L760,600" stroke="#fff" stroke-width="18" stroke-linecap="round"/>`)}</g>`;
// 13 · paso 1: alguien de tu nivel + marcador
function score(id, a, b) { return pg(id, 540, 560, `<rect x="320" y="490" width="440" height="140" rx="22" fill="#0b0f1e" stroke="#fff" stroke-width="6"/>${TXT(430, 590, 92, a, '#ff4a5a', 'Anton')}${TXT(540, 584, 70, '-', '#fff', 'Anton')}${TXT(650, 590, 92, b, '#5fb0ff', 'Anton')}`); }
M += `<g id="s13" opacity="0">${track('s13')}<rect width="1080" height="1920" fill="#000" opacity=".25"/>${flr(310, GY + 4)}${flr(770, GY + 4)}
  ${actor('s13T', OTU, 310, GY, 1.15, ['stand', 'up'])}${actor('s13R', ORIV, 770, GY, 1.15, ['stand', 'up'], '', true)}
  ${pg('s13eq', 540, 760, `<line x1="200" y1="740" x2="880" y2="740" stroke="#ffd23f" stroke-width="10" stroke-dasharray="26 16"/><rect x="470" y="690" width="140" height="100" rx="18" fill="#ffd23f" stroke="#000" stroke-width="6"/>${TXT(540, 770, 90, '=', '#000', 'Anton')}`)}
  ${score('s13s0', '0', '1')}${score('s13s1', '1', '1')}</g>`;
// 14 · paso 2: compite contra sus números
M += `<g id="s14" opacity="0"><rect width="1080" height="1920" fill="#0c1226"/><rect width="1080" height="1920" fill="url(#grid)" opacity=".7"/>${flr(300, GY + 4)}${flr(790, GY + 4)}
  ${actor('s14T', OTU, 300, GY, 1.0, ['stand'])}${actor('s14R', ORIV, 790, GY, 1.0, ['stand'], '', true)}
  <g id="s14pan" opacity="0"><rect x="80" y="400" width="920" height="380" rx="24" fill="#0b0f1e" stroke="#5fb0ff" stroke-width="5"/>
   ${TXT(200, 520, 42, 'RIVAL', '#5fb0ff', 'Anton')}<rect x="290" y="480" width="560" height="56" rx="12" fill="#2f74c8"/>${TXT(920, 522, 38, '4:55', '#5fb0ff', 'Anton')}
   ${TXT(200, 660, 42, 'TÚ', '#ff4a5a', 'Anton')}<rect x="290" y="620" width="560" height="56" rx="12" fill="#1a2238"/><rect id="s14bar" x="290" y="620" width="400" height="56" rx="12" fill="#d8323a"/>${TXT(920, 662, 38, '5:03', '#ff4a5a', 'Anton')}
   <line id="s14line" x1="850" y1="450" x2="850" y2="700" stroke="#ffd23f" stroke-width="8" stroke-dasharray="16 10" opacity="0"/></g>
  ${pg('s14flag', 850, 410, `<line x1="850" y1="460" x2="850" y2="330" stroke="#fff" stroke-width="8"/><path d="M850,330 L940,355 L850,380 Z" fill="#ffd23f" stroke="#000" stroke-width="5"/>${TXT(850, 315, 40, 'META', '#ffd23f', 'Anton', STK)}`)}
  ${pg('s14x', 790, 1050, `<path d="M680,900 L900,1180 M900,900 L680,1180" stroke="#ff2d40" stroke-width="32" stroke-linecap="round" ${STK}/>`)}</g>`;
// 15 · paso 3: pregúntale cómo lo hizo (podio)
M += `<g id="s15" opacity="0">${radBg('#2f3f6e', '#0b1022', '#ffd23f', '#0b1022')}
  <rect x="560" y="1150" width="340" height="770" fill="#e8c24a" stroke="#000" stroke-width="8"/>${TXT(730, 1300, 140, '1', '#8a5a00', 'Anton')}
  <rect x="180" y="1300" width="340" height="620" fill="#c9ccd6" stroke="#000" stroke-width="8"/>${TXT(350, 1450, 140, '2', '#6a6e7a', 'Anton')}
  ${actor('s15R', ORIV, 730, 1150, .9, ['stand', 'up'], '', true)}${actor('s15T', OTU, 350, 1300, .9, ['stand'])}
  ${pg('s15tro', 730, 470, `<path d="M670,380 L790,380 L780,470 Q730,520 680,470 Z" fill="#ffd23f" stroke="#000" stroke-width="7"/><path d="M670,400 Q630,400 640,440 Q650,470 685,468 M790,400 Q830,400 820,440 Q810,470 775,468" fill="none" stroke="#000" stroke-width="7"/><rect x="715" y="505" width="30" height="40" fill="#ffd23f" stroke="#000" stroke-width="6"/><rect x="690" y="540" width="80" height="22" rx="6" fill="#b8860b" stroke="#000" stroke-width="6"/>`)}
  ${pg('s15q', 330, 600, `<path d="M140,500 Q140,440 200,440 L470,440 Q530,440 530,500 L530,610 Q530,670 470,670 L330,670 L290,730 L290,670 L200,670 Q140,670 140,610 Z" fill="#fff" stroke="#000" stroke-width="7"/>${TXT(335, 540, 44, '¿CÓMO', '#15121a', 'Anton')}${TXT(335, 610, 44, 'LO HICISTE?', '#15121a', 'Anton')}`)}
  ${pg('s15bulb', 860, 640, `<circle cx="860" cy="640" r="90" fill="url(#yelGlow)"/><circle cx="860" cy="620" r="50" fill="#ffe66a" stroke="#000" stroke-width="7"/><rect x="838" y="664" width="44" height="34" rx="6" fill="#b8bcc6" stroke="#000" stroke-width="6"/>`)}</g>`;
// 16 · Goku y Vegeta entrenando juntos con Whis
M += `<g id="s16" opacity="0">${radBg('#2a4c8a', '#071226', '#7fdcff', '#071226')}${flr(540, 1250, 150)}
  <g id="s16ww" opacity="0">${actor('s16W', OWHIS, 540, 1250, .78, ['stand'])}</g>${flr(300, GY + 4)}${flr(780, GY + 4)}
  ${actor('s16G', OG_BLUE, 290, GY, 1.12, ['guard', 'punch'])}${actor('s16V', OV_BLUE, 790, GY, 1.12, ['guard', 'punch'], '', true)}
  ${impactFx('s16i1', 540, 1000, '#bff0ff')}${impactFx('s16i2', 540, 1010, '#bff0ff')}${impactFx('s16i3', 540, 990, '#bff0ff')}</g>`;
// 17 · etiqueta a tu Vegeta
M += `<g id="s17" opacity="0">${radBg('#26387a', '#080c1e', '#ffd23f', '#080c1e')}${speedLines('s17sl', '#ffb27a')}${flr(700, GY + 4, 230)}
  ${actor('s17V', OV, 720, GY, 1.32, ['cross'])}
  <g id="s17tw" opacity="0">${actor('s17T', OTU, 270, GY, 1.1, ['run', 'run2'])}</g>
  ${pg('s17tag', 540, 520, `<rect x="140" y="440" width="800" height="160" rx="80" fill="#fff" stroke="#000" stroke-width="8"/><circle cx="240" cy="520" r="58" fill="#e0283a" stroke="#000" stroke-width="6"/>${TXT(240, 548, 80, '@', '#fff', 'Anton')}${TXT(590, 548, 72, 'TU_VEGETA', '#15121a', 'Anton')}`)}
  ${pg('s17arr', 540, 700, `<path d="M540,640 L540,760" stroke="#ffd23f" stroke-width="22" stroke-linecap="round"/><path d="M490,720 L540,775 L590,720" fill="none" stroke="#ffd23f" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>`)}</g>`;
M += hook('s18');
M += `</g></g><rect width="1080" height="1920" fill="url(#vig)"/><rect id="flash" width="1080" height="1920" fill="#fff" opacity="0"/>`;
root.innerHTML = M;

// =============================================================== LÍNEA DE TIEMPO
// --- 1 · 0–5.88 · gancho
function hookTL(p, t0, uiT, vegT, endT, first) {
  scene(p, t0, endT);
  cam(t0, 540, 860, 1.12, 0); cam(t0 + .02, 540, 960, 1.0, Math.max(.3, vegT - t0 - .1), 'sine.inOut');
  auraPulse(p + 'G', t0, endT); breathe(p + 'G', t0, vegT, 5);
  sfx(t0 + .02, 'aura', .55);
  big('ULTRA INSTINTO', uiT, vegT, '#e9eefc', 132);
  sfx(uiT, 'shimmer', .5);
  // entra Vegeta: Goku se hace a un lado
  tl.to(RIGS[p + 'G'], { x: -230, duration: .3, ease: 'power3.out' }, vegT);
  show(p + 'Vw', vegT); enter(p + 'V', vegT, 700, .28); sfx(vegT + .22, 'slam', .9); shake(vegT + .24, .3, 18); flash(vegT + .22, '#7fb0ff', .35, .25);
  if (first) breathe(p + 'V', vegT + .4, endT, 4);
}
hookTL('s1', 0, 1.66, 2.48, 5.88, true);
pill('NO LO DIGO YO…', 3.3, 4.5, '', 'pop');
popS('s1sci', 4.52, 'glint', .7); pill('LO DICE LA CIENCIA', 4.52, 5.88, 'y', null);
hideS('s1sci', 5.7, .15);

// --- 2 · 5.88–10.24 · Vegeta lo alcanza → Goku sube de nivel
cut(5.88); scene('s2', 5.88, 10.24);
cam(5.88, 540, 960, 1.0, 0);
pill('PIÉNSALO', 5.88, 6.66, 'y');
breathe('s2G', 5.88, 8.6, 5); breathe('s2V', 5.88, 7.0, 4);
// Vegeta corre a alcanzarlo
pose('s2V', 1, 7.0); zoomLines(7.0, 7.7, 's2sl'); sfx(7.0, 'whoosh', .7);
ft(RIGS.s2V, { x: 0 }, { x: -200, duration: .6, ease: 'power2.inOut' }, 7.05);
lab('LO ALCANZA', 7.64, 8.7, 'b'); sfx(7.66, 'thud', .6); shake(7.66, .15, 8);
// Goku se transforma
tl.set('#s2G', { opacity: 0 }, 8.7); tl.set('#s2G2', { opacity: 0 }, 0); tl.set('#s2G2', { opacity: 1 }, 8.7);
powerUp('s2G2', 8.7, '#ffe14d'); auraPulse('s2G2', 8.7, 10.24);
cam(8.7, 400, 900, 1.2, .3, 'power3.out');
popS('s2up', 9.34, 'blip', .6); tl.to(RIGS.s2up, { y: -40, duration: .5, ease: 'power2.out' }, 9.4);
lab('GOKU SUBE DE NIVEL', 9.34, 10.24, 'y', null);

// --- 3 · 10.24–16.08 · escalera de transformaciones
cut(10.24); scene('s3', 10.24, 16.08);
cam(10.24, 300, 1300, 1.25, 0);
const GT = [10.24, 11.48, 12.26, 12.94];
GT.forEach((t, i) => {
  if (i) tl.set(`#s3g${i - 1}w`, { opacity: 0 }, t);
  show(`s3g${i}w`, t); ft(RIGS['s3g' + i], { y: -120, s: .7 }, { y: 0, s: 1, duration: .25, ease: 'back.out(2)' }, t);
  sfx(t, 'powerup', .55); flash(t, GCOL[i], .35, .25);
  auraPulse('s3g' + i, t, 16.08);
  if (i) { show(`s3v${i - 1}w`, t); if (i > 1) tl.set(`#s3v${i - 2}w`, { opacity: 0 }, t); ft(RIGS['s3v' + (i - 1)], { x: -160 }, { x: 0, duration: .25, ease: 'power2.out' }, t + .1); sfx(t + .1, 'swish', .4); }
});
cam(11.48, 520, 1100, 1.15, .4); cam(12.26, 700, 940, 1.1, .35); cam(12.94, 540, 960, 1.0, .5);
pill('UNO PERSIGUE AL OTRO', 14.16, 16.08, 'y', null);

// --- 4 · 16.08–18.22 · RIVALIDAD
cut(16.08); scene('s4', 16.08, 18.22);
cam(16.08, 540, 960, 1.0, 0); cam(16.1, 540, 1000, 1.1, 2.0, 'sine.inOut');
enter('s4G', 16.08, -500, .3, null); enter('s4V', 16.08, 500, .3, null);
breathe('s4G', 16.4, 18.2, 4); breathe('s4V', 16.4, 18.2, 4);
popS('s4vs', 16.52, 'zap', .7);
show('s4b', 16.9); tl.to('#s4b', { opacity: .3, duration: .05, yoyo: true, repeat: 7 }, 16.9); sfx(16.9, 'zap', .5);
big('RIVALIDAD', 17.34, 18.22, '#ff4a5a', 170);

// --- 5 · 18.22–22.24 · universidad
cut(18.22); scene('s5', 18.22, 22.24);
cam(18.22, 540, 1000, 1.15, 0); cam(18.24, 540, 960, 1.0, 3.9, 'sine.inOut');
pill('UNIVERSIDAD DE NUEVA YORK', 19.18, 22.24, 'b');
popS('s5clip', 20.44, 'pop', .6);
popS('s5ok', 20.72, 'ding', .6);
tl.to(RIGS.s5clip, { r: -3, duration: .4, yoyo: true, repeat: 2 }, 20.8);
lab('EN LA VIDA REAL', 21.16, 22.24, 'y');

// --- 6 · 22.24–25.0 · miles de resultados
cut(22.24); scene('s6', 22.24, 25.0);
cam(22.24, 540, 960, 1.0, 0);
ft('#s6rows', { y: 0 }, { y: -2300, duration: 2.7, ease: 'power1.in' }, 22.3);
for (let t = 22.4; t < 24.9; t += .12) sfx(t, 'tick', .25);
const CNT = { v: 0 };
popS('s6cnt', 22.8, 'pop', .5);
ft(CNT, { v: 0 }, { v: 1000, duration: 1.7, ease: 'power2.out', onUpdate: () => { $('s6num').textContent = Math.round(CNT.v).toLocaleString('es') + (CNT.v > 999 ? '+' : ''); } }, 22.8);
pill('MILES DE CORREDORES', 23.28, 25.0, 'y');

// --- 7 · 25.0–38.54 · la carrera: el rival al lado
cut(25.0); scene('s7', 25.0, 38.54);
cam(25.0, 540, 1000, 1.08, 0);
trackRun('s7', 25.0, 38.54);
runCycle('s7T', 25.0, 38.54, .19, .25);
show('s7Rw', 26.12); ft(RIGS.s7R, { x: 400 }, { x: 0, duration: .4, ease: 'power3.out' }, 26.12); sfx(26.12, 'whoosh', .6);
runCycle('s7R', 26.12, 38.54, .19, 0);
tl.to(RIGS.s7T, { x: -170, duration: .4, ease: 'power2.out' }, 26.12);
popS('s7tag', 26.4, 'pop', .6); hideS('s7tag', 27.9, .15);
pill('SU RIVAL EN LA CARRERA', 26.12, 27.96, 'b', null);
// más rápido
cam(27.96, 680, 1050, 1.0, .3); zoomLines(27.96, 31.7, 's7sl'); sfx(27.96, 'riser', .6);
popS('s7clk', 28.72, 'tick', .7);
tl.to(RIGS.s7hand, { r: 720, duration: 2.4, ease: 'power2.out' }, 28.72);
big('−5 SEG / KM', 28.96, 31.7, '#ffd23f', 150);
pill('MÁS RÁPIDO', 29.82, 31.7, 'y', null);
hideS('s7clk', 31.6, .15);
pill('MISMAS PIERNAS ✔', 31.78, 33.1, '', 'ding');
pill('MISMO ENTRENAMIENTO ✔', 33.16, 34.8, '', 'ding');
// lo único que cambió: quién estaba a su lado
cam(34.88, 760, 1000, 1.15, .6);
popS('s7ring', 36.26, 'glint', .7); tl.to(RIGS.s7ring, { s: 1.06, duration: .3, yoyo: true, repeat: 3 }, 36.5);
lab('QUIÉN ESTABA A SU LADO', 36.26, 37.78, 'y', null);
hideS('s7ring', 37.7, .1);
big('¿POR QUÉ?', 37.78, 38.54, '#ffffff', 170);
cam(37.78, 540, 1000, 1.08, .3);

// --- 8 · 38.54–42.8 · no peleas por una medalla, peleas por tu orgullo
cut(38.54); scene('s8', 38.54, 42.8);
cam(38.54, 540, 960, 1.0, 0);
pill('CONTRA UN RIVAL…', 38.74, 40.3, '');
popS('s8med', 38.9, 'ding', .6); tl.to(RIGS.s8med, { r: 6, duration: .35, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 39.2);
ft(RIGS.s8med, { s: 1 }, { s: 1.15, duration: .15, yoyo: true, repeat: 1 }, 40.36); sfx(40.36, 'glint', .6);
pill('NO PELEAS POR UNA MEDALLA', 40.36, 41.9, 'b', null);
popS('s8x', 41.34, 'slam', .8); shake(41.36, .2, 12);
tl.to(['#s8med', '#s8x'], { opacity: .25, duration: .2 }, 41.92);
big('ORGULLO', 41.92, 42.8, '#ff4a5a', 200, 700);

// --- 9 · 42.8–44.82 · el príncipe de los saiyajin
cut(42.8); scene('s9', 42.8, 44.82);
cam(42.8, 540, 900, 1.15, 0); cam(42.82, 540, 960, 1.0, 1.9, 'sine.inOut');
breathe('s9V', 42.8, 44.8, 4);
popS('s9crown', 43.34, 'glint', .8); tl.to(RIGS.s9crown, { y: -14, duration: .5, yoyo: true, repeat: 2, ease: 'sine.inOut' }, 43.7);
pill('EL PRÍNCIPE SAIYAJIN', 43.34, 44.82, 'y', null);

// --- 10 · 44.82–53.5 · el lado oscuro: trampa
cut(44.82); scene('s10', 44.82, 53.5);
cam(44.82, 540, 960, 1.0, 0);
popS('s10warn', 45.0, 'slam', .8); shake(45.05, .2, 10);
tl.to(RIGS.s10warn, { r: 4, duration: .1, yoyo: true, repeat: 5 }, 45.3);
pill('¡CUIDADO!', 45.0, 47.0, 'r', null);
hideS('s10warn', 47.0, .15);
big('LADO OSCURO', 47.1, 47.92, '#c070ff', 150);
sfx(47.1, 'rumble', .6);
popS('s10chart', 47.92, 'pop', .6);
pill('OTRO ESTUDIO', 47.92, 49.6, 'b', null);
show('s10rw', 49.62); ft(RIGS.s10T, { x: -300 }, { x: 0, duration: .3, ease: 'power3.out' }, 49.62); ft(RIGS.s10R, { x: 300 }, { x: 0, duration: .3, ease: 'power3.out' }, 49.7); sfx(49.62, 'whoosh', .5);
pill('FRENTE A SU RIVAL', 49.62, 51.5, 'r', null);
ft('#s10bar', { attr: { y: 900, height: 20 } }, { attr: { y: 540, height: 380 }, duration: .7, ease: 'power2.out' }, 51.52); sfx(51.52, 'riser', .5);
stamp('TRAMPA ↑', 52.68, 53.5, '#ff3346', 560);

// --- 11 · 53.5–60.0 · Babidi controla a Vegeta → Majin Vegeta
cut(53.5); scene('s11', 53.5, 60.0);
cam(53.5, 580, 960, 1.1, 0); cam(53.52, 540, 960, 1.0, 1.9, 'sine.inOut');
tl.set('#s11M', { opacity: 0 }, 0);
breathe('s11V', 53.5, 58.5, 4);
pill('COMO VEGETA', 53.82, 55.5, 'y');
show('s11bw', 55.52); ft(RIGS.s11B, { y: 80, s: .4 }, { y: 0, s: 1, duration: .35, ease: 'back.out(2)' }, 55.52); sfx(55.52, 'magic', .7);
pill('BABIDI', 55.52, 57.0, 'r', null);
// ondas de control desde el dedo de Babidi hasta Vegeta
const FING = [240 + (340 - 200) * .82 * 1.05, GY - (620 - 266) * .82 * 1.05];
document.querySelectorAll('#s11rings .mr').forEach((el, i) => {
  for (let k = 0; k < 3; k++) {
    const t = 55.96 + k * .55 + i * .11;
    ft(el, { attr: { cx: FING[0], cy: FING[1] }, opacity: .9 }, { attr: { cx: 580, cy: 780 }, opacity: 0, duration: .55, ease: 'power1.in' }, t);
  }
});
sfx(55.96, 'magic', .6); tl.to(RIGS.s11V, { r: -3, duration: .12, yoyo: true, repeat: 7 }, 56.1);
show('s11gw', 57.04); ft(RIGS.s11G, { x: 300 }, { x: 0, duration: .3, ease: 'power3.out' }, 57.04); sfx(57.04, 'whoosh', .5);
pill('SOLO PARA PELEAR CONTRA GOKU', 57.04, 58.5, '', null);
// transformación
tl.set('#s11V', { opacity: 0 }, 58.62); tl.set('#s11M', { opacity: 1 }, 58.62);
powerUp('s11M', 58.62, '#c070ff'); auraPulse('s11M', 58.62, 60.0);
popS('s11m', 58.62, null); tl.to('#s11m', { opacity: 0, duration: .6 }, 59.0);
cam(58.62, 580, 820, 1.3, .3, 'power3.out'); cam(59.4, 580, 960, 1.0, .5);
big('MAJIN VEGETA', 58.62, 60.0, '#ffd23f', 140);
sfx(58.98, 'stinger', .6);

// --- 12 · 60.0–63.94 · ¿cómo usas a tu propio Vegeta?
cut(60.0); scene('s12', 60.0, 63.94);
cam(60.0, 540, 960, 1.0, 0);
breathe('s12V', 60.0, 63.9, 4); breathe('s12M', 60.0, 63.9, 5); auraPulse('s12M', 60.0, 63.94);
pill('¿CÓMO LO USAS?', 60.92, 63.94, 'y');
popS('s12ok', 61.96, 'ding', .7);
popS('s12no', 62.98, 'buzz', .6); tl.to(RIGS.s12no, { x: 10, duration: .05, yoyo: true, repeat: 5 }, 63.1);

// --- 13 · 63.94–68.96 · paso 1
cut(63.94); scene('s13', 63.94, 68.96);
cam(63.94, 540, 960, 1.0, 0);
badge('1', 'Alguien de tu nivel', 63.94, 68.96);
breathe('s13T', 63.94, 66.9, 4); breathe('s13R', 63.94, 66.9, 4);
popS('s13eq', 65.56, 'pop', .6); tl.to(RIGS.s13eq, { s: 1.08, duration: .25, yoyo: true, repeat: 1 }, 65.9);
hideS('s13eq', 66.4, .15);
popS('s13s0', 67.02, 'ding', .6); pose('s13R', 1, 67.02); pose('s13R', 0, 67.9);
tl.set('#s13s0', { opacity: 0 }, 68.06); popS('s13s1', 68.06, 'ding', .7); pose('s13T', 1, 68.06);
lab('PAREJOS', 67.02, 68.96, 'y', null);

// --- 14 · 68.96–74.84 · paso 2
cut(68.96); scene('s14', 68.96, 74.84);
cam(68.96, 540, 960, 1.0, 0);
badge('2', 'Compite contra sus números', 68.96, 74.84);
breathe('s14T', 68.96, 74.8, 4); breathe('s14R', 68.96, 71.4, 4);
ft('#s14pan', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, ease: 'back.out(2)' }, 70.48); sfx(70.48, 'pop', .6);
ft('#s14bar', { attr: { width: 0 } }, { attr: { width: 400 }, duration: .5, ease: 'power2.out' }, 70.7); sfx(70.7, 'blip', .5);
popS('s14x', 71.46, 'buzz', .6); hideS('s14x', 72.6, .15);
lab('NO CONTRA ÉL', 71.46, 72.8, 'r', null);
tl.set('#s14line', { opacity: 1 }, 72.82); sfx(72.82, 'glint', .6); tl.to('#s14line', { opacity: .3, duration: .15, yoyo: true, repeat: 3 }, 72.9);
popS('s14flag', 74.02, 'ding', .7);
ft('#s14bar', { attr: { width: 400 } }, { attr: { width: 560 }, duration: .6, ease: 'power2.inOut' }, 74.02); sfx(74.02, 'riser', .4);
lab('TU PRÓXIMA META', 74.02, 74.84, 'y', null);

// --- 15 · 74.84–79.4 · paso 3
cut(74.84); scene('s15', 74.84, 79.4);
cam(74.84, 540, 960, 1.0, 0);
badge('3', 'Pregúntale cómo lo hizo', 74.84, 79.4);
breathe('s15T', 74.84, 77.6, 4);
popS('s15tro', 76.0, 'ding', .8); pose('s15R', 1, 76.0);
tl.to(RIGS.s15T, { x: -12, duration: .08, yoyo: true, repeat: 5 }, 76.7); sfx(76.7, 'thud', .4);
popS('s15q', 77.76, 'pop', .7);
popS('s15bulb', 78.7, 'glint', .7);

// --- 16 · 79.4–83.32 · entrenando juntos con Whis
cut(79.4); scene('s16', 79.4, 83.32);
cam(79.4, 540, 1000, 1.12, 0); cam(79.42, 540, 960, 1.0, 1.6, 'sine.inOut');
auraPulse('s16G', 79.4, 83.32); auraPulse('s16V', 79.4, 83.32);
show('s16ww', 79.54); ft(RIGS.s16W, { y: 60 }, { y: 0, duration: .4, ease: 'power2.out' }, 79.54); sfx(79.54, 'shimmer', .5);
pill('GOKU Y VEGETA', 80.28, 81.8, 'y');
strike('s16G', 81.28, .2, 60); boom('s16i1', 81.3);
strike('s16V', 81.9, .2, -60); boom('s16i2', 81.92);
strike('s16G', 82.44, .3, 60); boom('s16i3', 82.46, 'impact', 1);

// --- 17 · 83.32–86.82 · etiqueta a tu Vegeta
cut(83.32); scene('s17', 83.32, 86.82);
cam(83.32, 540, 960, 1.0, 0);
breathe('s17V', 83.32, 86.8, 4);
popS('s17tag', 83.74, 'pop', .8); tl.to(RIGS.s17tag, { s: 1.06, duration: .3, yoyo: true, repeat: 3 }, 84.1);
popS('s17arr', 84.38, 'blip', .6); tl.to(RIGS.s17arr, { y: 20, duration: .25, yoyo: true, repeat: 5 }, 84.6);
// tú vas por él
show('s17tw', 85.22); ft(RIGS.s17T, { x: -450 }, { x: 0, duration: .5, ease: 'power3.out' }, 85.22);
runCycle('s17T', 85.22, 86.82, .16, .3); zoomLines(85.22, 86.82, 's17sl');
lab('YA VOY POR TI', 85.8, 86.82, 'r');
tl.to(RIGS.s17V, { r: -2, duration: .2 }, 85.96);

// --- 18 · 86.82–END · vuelve al inicio (bucle)
cut(86.82);
hookTL('s18', 86.82, 88.86, 90.1, END + 1, false);

// =============================================================== SUBTÍTULOS
(function subs() {
  const RED = /^(rival|rivalidad|vegeta|majin|trampa|oscuro|orgullo|babidi|cuidado|controlara|gane|escondas)$/i;
  const YEL = /^(goku|ultra|instinto|saiyajin|super|cinco|segundos|kilómetro|ciencia|nivel|1|2|3|meta|marca|números|juntos|miles|medalla|príncipe|dios)$/i;
  const BLU = /^(blue|real|piernas|entrenamiento|nueva|york|universidad|corredores|etiqueta)$/i;
  const W = window.WORDS, chunks = []; let cur = [];
  W.forEach((w, i) => {
    cur.push(w); const nx = W[i + 1];
    if (!nx || cur.length >= 3 || cur.reduce((a, x) => a + x.w.length, 0) + nx.w.length > 20 || /[,.?!]$/.test(w.w) || nx.s - w.e > .35) { chunks.push(cur); cur = []; }
  });
  const shd = strokeShadow(7);
  chunks.forEach((c, k) => {
    const t0 = c[0].s, nx = chunks[k + 1], t1 = Math.min(nx ? nx[0].s : END, c[c.length - 1].e + .45);
    const d = addDiv('sub', c.map(w => `<span>${w.w.replace(/[,.]$/, '')}</span>`).join(' '), `text-shadow:${shd}`);
    ft(d, { opacity: 1, scale: .82, y: 14 }, { scale: 1, y: 0, duration: .1, ease: 'back.out(3)' }, t0);
    tl.set(d, { opacity: 0 }, t1);
    const sp = d.querySelectorAll('span');
    c.forEach((w, i) => {
      const k2 = w.w.replace(/[¿?,.!]/g, '');
      const col = RED.test(k2) ? '#ff4152' : YEL.test(k2) ? '#ffd23f' : BLU.test(k2) ? '#6fd3ff' : '#ffffff';
      tl.set(sp[i], { color: col, scale: 1 }, t0);
      tl.fromTo(sp[i], { scale: 1.16 }, { scale: 1, duration: .14, immediateRender: false }, w.s);
    });
  });
})();

// =============================================================== control externo
tl.set({}, {}, END);
window.DURATION = END;
window.seek = t => { tl.seek(t, false); applyCam(); applyRigs(); return true; };
window.ready = document.fonts.ready.then(() => true);
tl.seek(0); applyCam(); applyRigs();
