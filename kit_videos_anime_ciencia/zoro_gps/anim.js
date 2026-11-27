// ZORO Y EL GPS — motor + escenas + efectos + subtítulos (voz 1.2x, 78.0 s)
const END = 78.0;
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
const OZ = { ...ZORO, mid: zoroCoat(), over: swordsFront() };
const OZ_LOST = { ...ZORO, angry: false, lookX: -4, mouth: 'flat', mid: zoroCoat(), over: swordsFront() };
const OZ_AURA = { ...ZORO, behind: aura('#4fe07a', .4) + swordsBack(), mid: zoroCoat(), over: swordsFront() };
const OZ_HAKI = { ...ZORO, behind: aura('#2a0f3a', .85) + swordsBack(), mid: zoroCoat(), over: swordsFront(), iris: '#a01828' };
const OTU = { ...HOOD, calm: true, mouth: 'flat', lookY: 4, lookX: 2, over: phone };
const OTU_MAP = { ...HOOD, angry: true, mouth: 'grit', aura: '#ffd23a', auraOp: .3, over: mapPaper };
const OTU_WALK = { ...HOOD, angry: true, mouth: 'smirk' };
const OTU_OLD = { ...HOOD, headExtra: youHair.replace('#4a2f1e', '#c9c9d1'), calm: true, mouth: 'smile',
  over: `<path d="M268,410 L292,616" stroke="${OL}" stroke-width="13" stroke-linecap="round"/><path d="M268,410 L292,616" stroke="#8a5a2e" stroke-width="8" stroke-linecap="round"/><path d="M262,406 Q262,384 284,386" fill="none" stroke="${OL}" stroke-width="13" stroke-linecap="round"/><path d="M262,406 Q262,384 284,386" fill="none" stroke="#8a5a2e" stroke-width="8" stroke-linecap="round"/>` };
const OTAXI = { top: 'suit', topC: '#2e3a52', sleeve: 'long', bottom: '#23252e', shoes: '#16161c', skin: '#efc29c', hair: 'none', headExtra: capTaxi, iris: '#4a5a7a', mouth: 'smile',
  over: `<path d="M178,224 L200,262 L222,224" fill="#e9e6df" stroke="${OL}" stroke-width="2.6"/><path d="M196,236 L204,236 L206,300 L200,310 L194,300 Z" fill="#8e1f27" stroke="${OL}" stroke-width="2"/>` };

// caminar: balanceo + rebote + pasos
function walk(id, t0, t1, per = .3, vol = .3, tilt = 3) {
  let k = 0;
  for (let t = t0; t < t1 - .05; t += per, k++) {
    tl.to(RIGS[id], { r: k % 2 ? -tilt : tilt, duration: per / 2, ease: 'sine.inOut' }, t);
    ft(RIGS[id], { y: 0 }, { y: -10, duration: per / 2, ease: 'sine.out', yoyo: true, repeat: 1 }, t);
    if (vol) sfx(t + per * .45, 'step', vol);
  }
  tl.to(RIGS[id], { r: 0, duration: .15 }, t1 - .1);
}
// trazo que se dibuja (stroke-dashoffset)
function drawPath(sel, t, d, len = 3000) { ft(sel, { attr: { 'stroke-dasharray': len, 'stroke-dashoffset': len } }, { attr: { 'stroke-dashoffset': 0 }, duration: d, ease: 'power1.inOut' }, t); }

// ---------- utilería de este video
const QM = (x, y) => `<g font-family="Anton" fill="#ffd23a" stroke="${OLc}" stroke-width="8" paint-order="stroke">${TXT(x, y, 130, '?', '#ffd23a', 'Anton', `stroke="#000" stroke-width="10" paint-order="stroke" transform="rotate(14 ${x} ${y})"`)}${TXT(x + 90, y + 70, 90, '?', '#ffd23a', 'Anton', `stroke="#000" stroke-width="9" paint-order="stroke" transform="rotate(24 ${x + 90} ${y + 70})"`)}${TXT(x - 300, y + 30, 100, '?', '#ffd23a', 'Anton', `stroke="#000" stroke-width="9" paint-order="stroke" transform="rotate(-16 ${x - 300} ${y + 30})"`)}</g>`;
const CHECK = (x, y, r = 46) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#22b35a" stroke="#fff" stroke-width="8"/><path d="M${x - r * .5},${y} L${x - r * .1},${y + r * .4} L${x + r * .55},${y - r * .42}" fill="none" stroke="#fff" stroke-width="${r * .26}" stroke-linecap="round" stroke-linejoin="round"/>`;
const CROSS = (x, y, r = 46) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#e0283a" stroke="#fff" stroke-width="8"/><path d="M${x - r * .42},${y - r * .42} L${x + r * .42},${y + r * .42} M${x + r * .42},${y - r * .42} L${x - r * .42},${y + r * .42}" stroke="#fff" stroke-width="${r * .26}" stroke-linecap="round"/>`;
// carretera en perspectiva con la LÍNEA RECTA en el centro
function road(p) {
  let s = radBg('#2f6b45', '#06140c', '#8fffb4', '#000');
  s += `<rect y="880" width="1080" height="1040" fill="#173523"/>`;
  s += `<path d="M470,880 L610,880 L1240,1920 L-160,1920 Z" fill="#3b3f4c"/><path d="M470,880 L490,880 L-100,1920 L-160,1920 Z M590,880 L610,880 L1240,1920 L1180,1920 Z" fill="#e8e4da" opacity=".7"/>`;
  s += `<path id="${p}line" d="M534,880 L546,880 L566,1920 L514,1920 Z" fill="#ffd23f"/>`;
  for (let i = 0; i < 9; i++) s += `<circle cx="${R(40, 400).toFixed(0)}" cy="${R(900, 1200).toFixed(0)}" r="${R(30, 70).toFixed(0)}" fill="#1f4a2e" opacity=".9"/><circle cx="${R(700, 1060).toFixed(0)}" cy="${R(900, 1200).toFixed(0)}" r="${R(30, 70).toFixed(0)}" fill="#1f4a2e" opacity=".9"/>`;
  return s;
}
const ship = (x, y) => `<g transform="translate(${x},${y})"><path d="M-170,0 L170,0 L130,80 L-130,80 Z" fill="#8a5a2e" stroke="#000" stroke-width="7" stroke-linejoin="round"/><rect x="-170" y="-14" width="340" height="18" fill="#6a4220" stroke="#000" stroke-width="6"/>
  <line x1="0" y1="-14" x2="0" y2="-300" stroke="#000" stroke-width="16"/><line x1="0" y1="-14" x2="0" y2="-300" stroke="#a87444" stroke-width="9"/>
  <path d="M-110,-270 Q0,-250 110,-270 L120,-60 Q0,-40 -120,-60 Z" fill="#f4ead2" stroke="#000" stroke-width="6" stroke-linejoin="round"/><path d="M0,-300 L70,-316 L0,-330 Z" fill="#15121a" stroke="#000" stroke-width="4"/>
  ${[-110, -40, 30, 100].map(c => `<circle cx="${c}" cy="40" r="11" fill="#3a2410" stroke="#000" stroke-width="4"/>`).join('')}</g>`;
const sea = `<rect y="1000" width="1080" height="430" fill="#1d5a8a"/>${Array.from({ length: 10 }, (_, i) => `<path d="M${-40 + i * 120},${1060 + (i % 3) * 110} q30,-18 60,0 t60,0" fill="none" stroke="#bfe6ff" stroke-width="6" opacity=".6"/>`).join('')}`;
function brain(id, cx, cy, s, crack = false) {
  const g = `<g transform="translate(${cx},${cy}) scale(${s})">
    <path d="M-260,40 C-290,-120 -150,-230 0,-222 C150,-232 292,-140 272,10 C300,92 232,172 140,160 C118,214 40,226 0,198 L-16,262 L-62,254 L-50,192 C-150,204 -252,152 -260,40 Z" fill="#f4a6bd" stroke="#000" stroke-width="9" stroke-linejoin="round"/>
    <path d="M150,-160 C232,-120 300,-40 250,70 C232,120 190,150 140,160 C200,90 214,-40 150,-160 Z" fill="#000" opacity=".12"/>
    <path d="M-200,-60 C-160,-120 -90,-80 -60,-130 M-30,-170 C10,-120 70,-150 100,-110 M140,-60 C190,-60 210,-10 230,0 M-220,60 C-170,40 -150,100 -100,80 M-60,-20 C-20,-60 40,-20 80,-50 M100,40 C150,30 170,90 210,80 M-160,140 C-120,110 -60,150 -30,130" fill="none" stroke="#c4587a" stroke-width="9" stroke-linecap="round"/>
    <g id="${id}hip"><path d="M-70,60 C-40,10 50,18 66,64 C80,108 34,132 10,110 C-8,94 14,76 32,86" fill="none" stroke="#ffb800" stroke-width="40" stroke-linecap="round" opacity=".45" filter="url(#blur8)"/>
      <path d="M-70,60 C-40,10 50,18 66,64 C80,108 34,132 10,110 C-8,94 14,76 32,86" fill="none" stroke="#000" stroke-width="30" stroke-linecap="round"/>
      <path d="M-70,60 C-40,10 50,18 66,64 C80,108 34,132 10,110 C-8,94 14,76 32,86" fill="none" stroke="#ffd23f" stroke-width="20" stroke-linecap="round"/></g>
    ${crack ? `<g id="${id}crk" opacity="0"><path d="M-120,-200 L-90,-120 L-130,-60 L-80,10 L-110,90 M90,-210 L60,-130 L110,-70 L70,0 L120,60 M-10,-90 L20,-30 L-20,30" fill="none" stroke="#e0283a" stroke-width="14" stroke-linejoin="round" stroke-linecap="round"/></g>` : ''}</g>`;
  return pg(id, cx, cy, g);
}
const cab = (x, y) => `<g transform="translate(${x},${y})"><path d="M-260,-40 Q-250,-150 -150,-170 L-110,-260 Q-60,-300 60,-300 Q130,-300 160,-250 L200,-170 Q270,-160 270,-80 L270,-10 L-260,-10 Z" fill="#17171e" stroke="#000" stroke-width="8" stroke-linejoin="round"/>
  <path d="M-96,-250 Q-60,-280 0,-280 L0,-180 L-130,-180 Z M20,-280 Q120,-280 148,-240 L176,-180 L20,-180 Z" fill="#9fd0ef" stroke="#000" stroke-width="6" stroke-linejoin="round"/>
  <rect x="-40" y="-336" width="90" height="38" rx="8" fill="#ffd23f" stroke="#000" stroke-width="6"/>${TXT(5, -306, 30, 'TAXI', '#000', 'Anton')}
  <rect x="210" y="-120" width="50" height="30" rx="8" fill="#fff6c4" stroke="#000" stroke-width="5"/><path d="M-250,-80 L270,-80" stroke="#444" stroke-width="5"/>
  ${[-150, 150].map(c => `<circle cx="${c}" cy="-10" r="62" fill="#111" stroke="#000" stroke-width="8"/><circle cx="${c}" cy="-10" r="28" fill="#9aa4b8" stroke="#000" stroke-width="5"/>`).join('')}</g>`;
const bigBen = `<g opacity=".95"><rect x="800" y="560" width="140" height="870" fill="#2a2450" stroke="#0a0820" stroke-width="6"/><path d="M790,560 L870,380 L950,560 Z" fill="#2a2450" stroke="#0a0820" stroke-width="6"/><line x1="870" y1="380" x2="870" y2="320" stroke="#2a2450" stroke-width="10"/>
  <circle cx="870" cy="650" r="54" fill="#f5e3a0" stroke="#0a0820" stroke-width="8"/><path d="M870,650 L870,612 M870,650 L898,660" stroke="#0a0820" stroke-width="7" stroke-linecap="round"/></g>`;
function bubble(x, y, w, h, inner) { return `<g><circle cx="${x - w * .2}" cy="${y + h * .62}" r="14" fill="#fff" stroke="#000" stroke-width="5"/><circle cx="${x - w * .28}" cy="${y + h * .8}" r="8" fill="#fff" stroke="#000" stroke-width="4"/><ellipse cx="${x}" cy="${y}" rx="${w / 2}" ry="${h / 2}" fill="#fff" stroke="#000" stroke-width="7"/>${inner}</g>`; }
const shop = (x, y) => `<g transform="translate(${x},${y})"><rect x="-70" y="-40" width="140" height="110" fill="#f4ead2" stroke="#000" stroke-width="6"/><path d="M-84,-40 L84,-40 L74,-90 L-74,-90 Z" fill="#e0283a" stroke="#000" stroke-width="6"/><path d="M-50,-90 L-56,-40 M-20,-90 L-20,-40 M20,-90 L20,-40 M50,-90 L56,-40" stroke="#fff" stroke-width="10"/><rect x="-24" y="10" width="48" height="60" fill="#8a5a2e" stroke="#000" stroke-width="5"/></g>`;
const bridge = (x, y) => `<g transform="translate(${x},${y})"><path d="M-110,40 L-110,-10 Q0,-90 110,-10 L110,40 L80,40 Q0,-30 -80,40 Z" fill="#c9ccd6" stroke="#000" stroke-width="6" stroke-linejoin="round"/><rect x="-124" y="-24" width="248" height="16" rx="6" fill="#8a8ea0" stroke="#000" stroke-width="5"/><path d="M-110,60 q20,-10 40,0 t40,0 t40,0 t40,0 t40,0" fill="none" stroke="#6fd3ff" stroke-width="7"/></g>`;
const corner = (x, y) => `<g transform="translate(${x},${y})"><rect x="-8" y="-100" width="16" height="170" fill="#9aa4b8" stroke="#000" stroke-width="5"/><rect x="-90" y="-110" width="120" height="40" rx="6" fill="#22b35a" stroke="#000" stroke-width="5"/><rect x="-20" y="-66" width="120" height="40" rx="6" fill="#2f74c8" stroke="#000" stroke-width="5"/><path d="M-60,-90 L0,-90 M10,-46 L70,-46" stroke="#fff" stroke-width="7" stroke-linecap="round"/></g>`;
const cloud = (x, y) => `<g transform="translate(${x},${y})"><path d="M-110,30 Q-130,-20 -80,-30 Q-70,-80 -10,-70 Q30,-110 70,-60 Q130,-60 120,0 Q140,40 90,40 L-80,40 Q-120,40 -110,30 Z" fill="#f4f6ff" stroke="#000" stroke-width="7" stroke-linejoin="round"/></g>`;
const house = (x, y) => `<g transform="translate(${x},${y})"><path d="M-90,0 L0,-80 L90,0 Z" fill="#e0283a" stroke="#000" stroke-width="7" stroke-linejoin="round"/><rect x="-70" y="0" width="140" height="100" fill="#f4ead2" stroke="#000" stroke-width="7"/><rect x="-20" y="40" width="40" height="60" fill="#8a5a2e" stroke="#000" stroke-width="5"/></g>`;
const flagTag = (x, y, txt, col) => `<g transform="translate(${x},${y})"><rect x="-120" y="-34" width="240" height="68" rx="14" fill="${col}" stroke="#000" stroke-width="6"/>${TXT(0, 18, 46, txt, '#fff', 'Anton')}</g>`;

// =============================================================== ESCENAS (markup)
let M = defs + `<g id="camS"><g id="camZ">`;
const GY = 1430;
// 1 y 17 · gancho / final en bucle: Zoro se sale de la línea recta + "tú" con el GPS
function hook(p) {
  return `<g id="${p}" opacity="0">${road(p)}${flr(540, GY + 4, 230)}
    ${actor(p + 'Z', OZ_LOST, 540, GY, 1.32, ['stand', 'scratch'])}
    ${pg(p + 'q', 760, 560, QM(820, 560))}
    <g id="${p}Tw" opacity="0">${flr(250, GY + 4, 170)}${actor(p + 'T', OTU, 250, GY, 1.05, ['phone'])}</g></g>`;
}
M += hook('s1');
// 2 · el espadachín más fuerte
M += `<g id="s2" opacity="0">${radBg('#2f7a46', '#06160d', '#9dffbd', '#06160d')}${flr(540, GY + 4, 250)}${actor('s2Z', OZ_AURA, 540, GY, 1.5, ['cross'])}
  ${pg('s2hat', 540, 560, `<ellipse cx="540" cy="600" rx="190" ry="48" fill="#f2c84b" stroke="#000" stroke-width="9"/><path d="M430,600 Q430,470 540,466 Q650,470 650,600 Z" fill="#f2c84b" stroke="#000" stroke-width="9"/><path d="M432,580 Q540,604 648,580 L650,604 Q540,628 430,604 Z" fill="#d8323a" stroke="#000" stroke-width="6"/>`)}</g>`;
// 3 · no encuentra ni su propio barco
M += `<g id="s3" opacity="0"><rect width="1080" height="1920" fill="#7ec6ee"/><circle cx="180" cy="300" r="80" fill="#fff4c0"/>${sea}${pg('s3ship', 820, 1000, ship(820, 1000), true)}
  <rect y="1300" width="1080" height="620" fill="#e0c28a"/><rect y="1430" width="1080" height="490" fill="#c9a66a"/>${flr(330, GY + 4, 200)}
  ${actor('s3Z', OZ_LOST, 330, GY, 1.3, ['stand', 'scratch'], '', true)}
  ${pg('s3arr', 820, 600, `<path d="M820,520 L820,640" stroke="#ffd23f" stroke-width="24" stroke-linecap="round" ${STK}/><path d="M770,600 L820,660 L870,600" fill="none" stroke="#ffd23f" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/>${TXT(820, 500, 64, 'SU BARCO', '#ffd23f', 'Anton', STK)}`)}
  ${pg('s3q', 330, 560, QM(380, 600))}</g>`;
// 4 · nos reímos… el chiste eres tú
const JA = [[220, 430, -12], [860, 520, 10], [600, 720, 8], [860, 900, -8]];
M += `<g id="s4" opacity="0">${radBg('#7a6a1a', '#1a1404', '#ffe27a', '#1a1404')}${flr(330, GY + 4, 190)}${flr(780, GY + 4, 170)}
  ${actor('s4Z', OZ_LOST, 330, GY, 1.2, ['stand', 'scratch'])}
  <g id="s4Tw" opacity="0">${actor('s4T', OTU, 780, GY, 1.12, ['phone'], '', true)}</g>
  ${JA.map(([x, y, r], i) => pg('s4j' + i, x, y, `<g transform="rotate(${r} ${x} ${y})">${TXT(x, y + 30, 96, 'JA JA', '#fff', 'Anton', 'stroke="#000" stroke-width="10" paint-order="stroke"')}</g>`)).join('')}
  ${pg('s4sci', 540, 560, `<circle cx="540" cy="560" r="150" fill="url(#yelGlow)" opacity=".6"/><path d="M500,440 L500,520 L430,650 Q420,680 450,680 L630,680 Q660,680 650,650 L580,520 L580,440 Z" fill="#d6f4ff" stroke="#000" stroke-width="8" stroke-linejoin="round"/><path d="M462,600 L618,600 L650,652 Q656,672 632,672 L448,672 Q424,672 430,652 Z" fill="#3fd17a"/><rect x="486" y="426" width="108" height="24" rx="8" fill="#9aa4b8" stroke="#000" stroke-width="6"/>`)}
  ${pg('s4fing', 780, 700, `<path d="M640,700 L900,700" stroke="#ff4152" stroke-width="26" stroke-linecap="round" ${STK}/><path d="M860,650 L920,700 L860,750" fill="none" stroke="#ff4152" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>`)}</g>`;
// 5 · Londres: taxistas y 25 000 calles
let streets = ''; for (let i = 0; i < 9; i++) streets += `<line x1="${60 + i * 120}" y1="360" x2="${60 + i * 120}" y2="1000" stroke="#ffd23f" stroke-width="4" opacity=".55"/>`; for (let i = 0; i < 6; i++) streets += `<line x1="40" y1="${380 + i * 120}" x2="1040" y2="${380 + i * 120}" stroke="#ffd23f" stroke-width="4" opacity=".55"/>`;
M += `<g id="s5" opacity="0">${nightBg()}${bigBen}<g id="s5map" opacity="0"><rect x="30" y="340" width="1020" height="680" rx="20" fill="#0b0f22" opacity=".85"/>${streets}</g>
  <rect y="1430" width="1080" height="490" fill="#14122e"/>${flr(250, GY + 4, 170)}${actor('s5D', OTAXI, 250, GY, 1.12, ['stand', 'point'])}
  <g id="s5cw">${pg('s5cab', 730, 1460, cab(730, 1460), true)}</g>
  ${pg('s5cnt', 540, 560, `<rect x="250" y="490" width="580" height="140" rx="22" fill="#ffd23f" stroke="#000" stroke-width="8"/><text id="s5num" x="540" y="590" font-family="Anton" font-size="96" text-anchor="middle" fill="#000">0</text>`)}</g>`;
// 6 · Maguire escanea el cerebro: hipocampo más grande
M += `<g id="s6" opacity="0"><rect width="1080" height="1920" fill="#0c1226"/><rect width="1080" height="1920" fill="url(#grid)" opacity=".7"/>
  ${brain('s6b', 540, 960, 1.45)}
  <g id="s6scan" opacity="0"><rect id="s6bar" x="120" y="560" width="22" height="820" fill="#6fd3ff" opacity=".85" filter="url(#glowB)"/></g>
  ${pg('s6arr', 760, 1180, `<path d="M900,1260 L700,1120" stroke="#ffd23f" stroke-width="22" stroke-linecap="round" ${STK}/><path d="M700,1180 L690,1112 L760,1110" fill="none" stroke="#ffd23f" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>`)}</g>`;
// 7 · mapa mental (cabeza que dibuja un mapa) + años al volante
M += `<g id="s7" opacity="0">${radBg('#2a4c8a', '#071226', '#7fdcff', '#071226')}
  <g id="s7head"><path d="M300,1300 L300,1180 Q190,1150 200,1000 Q180,980 210,940 Q200,600 540,580 Q860,590 860,900 Q870,1120 760,1180 L760,1300 Z" fill="#f2c8a0" stroke="#000" stroke-width="10" stroke-linejoin="round"/>
   <rect x="330" y="700" width="420" height="360" rx="30" fill="#f4ead2" stroke="#000" stroke-width="7"/>
   <path d="M330,820 L750,820 M330,940 L750,940 M470,700 L470,1060 M610,700 L610,1060" stroke="#c9b892" stroke-width="10"/>
   <path id="s7route" d="M370,1020 L370,880 L540,880 L540,760 L700,760" fill="none" stroke="#e0283a" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="3000" stroke-dashoffset="3000"/>
   <circle id="s7pin" cx="700" cy="760" r="20" fill="#e0283a" stroke="#000" stroke-width="5" opacity="0"/></g>
  <g id="s7chart" opacity="0"><rect x="100" y="560" width="880" height="780" rx="26" fill="#0b0f1e" stroke="#ffd23f" stroke-width="6"/>${TXT(540, 640, 52, 'AÑOS AL VOLANTE → HIPOCAMPO', '#ffd23f', 'Oswald')}
   <line x1="180" y1="1240" x2="900" y2="1240" stroke="#5a6a8a" stroke-width="6"/>
   ${[0, 1, 2].map(i => `<rect id="s7b${i}" x="${230 + i * 230}" y="${1240 - (180 + i * 200)}" width="160" height="${180 + i * 200}" fill="${['#6fd3ff', '#3fa8ff', '#ffd23f'][i]}" stroke="#000" stroke-width="6"/>${TXT(310 + i * 230, 1300, 40, ['5 AÑOS', '15 AÑOS', '30 AÑOS'][i], '#e8eef8')}`).join('')}
   ${pg('s7wheel', 860, 760, `<circle cx="860" cy="760" r="64" fill="none" stroke="#e8eef8" stroke-width="16"/><circle cx="860" cy="760" r="14" fill="#e8eef8"/><path d="M860,760 L860,700 M860,760 L808,792 M860,760 L912,792" stroke="#e8eef8" stroke-width="12"/>`, true)}</g></g>`;
// 8 · ¿y con GPS? estudio McGill, 3 años
M += `<g id="s8" opacity="0">${nightBg()}${flr(320, GY + 4, 190)}${actor('s8T', OTU, 320, GY, 1.25, ['phone'])}
  ${pg('s8ph', 790, 900, `<g transform="rotate(6 790 900)"><rect x="640" y="640" width="300" height="540" rx="40" fill="#1b1b22" stroke="#000" stroke-width="9"/><rect x="664" y="690" width="252" height="440" rx="12" fill="#e9eef4"/>
     <path d="M664,800 L916,760 M664,960 L916,1000 M740,690 L780,1130 M860,690 L830,1130" stroke="#c4ccd8" stroke-width="18"/><path d="M790,1110 L790,880 L860,820" fill="none" stroke="#2f9be6" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
     <path d="M760,1060 L790,990 L820,1060 L790,1046 Z" fill="#2f9be6" stroke="#000" stroke-width="5"/></g>`)}
  ${pg('s8cal', 790, 520, `<rect x="650" y="420" width="280" height="230" rx="18" fill="#fff" stroke="#000" stroke-width="8"/><rect x="650" y="420" width="280" height="64" rx="18" fill="#e0283a" stroke="#000" stroke-width="8"/>${TXT(790, 468, 40, 'AÑOS', '#fff', 'Anton')}
     ${[1, 2, 3].map(n => `<text class="s8y" id="s8y${n}" x="790" y="620" font-family="Anton" font-size="130" text-anchor="middle" fill="#15121a" opacity="0">${n}</text>`).join('')}`)}</g>`;
// 9 · más GPS = menos memoria espacial
M += `<g id="s9" opacity="0"><rect width="1080" height="1920" fill="#0c1226"/><rect width="1080" height="1920" fill="url(#grid)" opacity=".7"/>
  <g id="s9chart"><rect x="90" y="520" width="900" height="840" rx="26" fill="#0b0f1e" stroke="#ff4a5a" stroke-width="6"/>${TXT(540, 600, 52, 'MEMORIA ESPACIAL', '#ff6b78', 'Oswald')}
   <line x1="170" y1="1250" x2="920" y2="1250" stroke="#5a6a8a" stroke-width="6"/><line x1="170" y1="660" x2="170" y2="1250" stroke="#5a6a8a" stroke-width="6"/>${TXT(560, 1320, 40, 'USO DE GPS →', '#e8eef8')}
   <path id="s9line" d="M180,720 L340,770 L480,860 L620,940 L760,1080 L900,1200" fill="none" stroke="#ff2d40" stroke-width="18" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="3000" stroke-dashoffset="3000"/></g>
  ${pg('s9gps', 900, 1120, `<circle cx="900" cy="1120" r="62" fill="#2f9be6" stroke="#fff" stroke-width="8"/><path d="M876,1150 L900,1086 L924,1150 L900,1136 Z" fill="#fff"/>`)}</g>`;
// 10 · ¿por qué? sigues flechas → el hipocampo se apaga → solo obedeces
const ARR = [[540, 1640], [540, 1360], [600, 1150], [690, 990]];
M += `<g id="s10" opacity="0">${road('s10')}
  ${ARR.map(([x, y], i) => { const k = 1 - i * .2; return pg('s10a' + i, x, y, `<path d="M${x - 70 * k},${y + 40 * k} L${x},${y - 60 * k} L${x + 70 * k},${y + 40 * k} L${x},${y + 10 * k} Z" fill="#2f9be6" stroke="#fff" stroke-width="${8 * k}" stroke-linejoin="round"/>`); }).join('')}
  ${flr(400, GY + 4, 190)}${actor('s10T', OTU, 400, GY, 1.22, ['phone'])}
  ${pg('s10th', 700, 560, bubble(700, 560, 380, 300, `<g transform="translate(700,560) scale(.5)"><path d="M-260,40 C-290,-120 -150,-230 0,-222 C150,-232 292,-140 272,10 C300,92 232,172 140,160 C118,214 40,226 0,198 L-16,262 L-62,254 L-50,192 C-150,204 -252,152 -260,40 Z" fill="#f4a6bd" stroke="#000" stroke-width="12"/>
     <g id="s10hip"><path d="M-70,60 C-40,10 50,18 66,64 C80,108 34,132 10,110 C-8,94 14,76 32,86" fill="none" stroke="#000" stroke-width="40" stroke-linecap="round"/><path d="M-70,60 C-40,10 50,18 66,64 C80,108 34,132 10,110 C-8,94 14,76 32,86" fill="none" stroke="#ffd23f" stroke-width="28" stroke-linecap="round"/></g></g>`))}
  ${pg('s10off', 860, 430, `<rect x="790" y="390" width="140" height="80" rx="16" fill="#15121a" stroke="#ff4a5a" stroke-width="6"/>${TXT(860, 450, 52, 'OFF', '#ff4a5a', 'Anton')}`)}</g>`;
// 11 · lo oscuro: Alzheimer
M += `<g id="s11" opacity="0">${radBg('#4a0f1c', '#090205', '#ff3d5a', '#090205')}${brain('s11b', 540, 960, 1.4, true)}</g>`;
// 12 · Haki de reserva + para cuando seas viejo
let hakiBolts = ''; for (let i = 0; i < 6; i++) { let x = R(240, 840), y = R(560, 900), d = `M${x.toFixed(0)},${y.toFixed(0)}`; for (let k = 0; k < 5; k++) { x += R(-60, 60); y += R(40, 90); d += ` L${x.toFixed(0)},${y.toFixed(0)}`; } hakiBolts += `<path d="${d}" fill="none" stroke="#ff2d5a" stroke-width="7" stroke-linejoin="round" filter="url(#glowB)"/>`; }
M += `<g id="s12" opacity="0">${radBg('#2a0f3a', '#050208', '#c070ff', '#050208')}<g id="s12bolt" opacity="0">${hakiBolts}</g>${flr(540, GY + 4, 250)}
  <g id="s12Zw">${actor('s12Z', OZ_HAKI, 540, GY, 1.45, ['cross'])}</g>
  <g id="s12Ow" opacity="0">${flr(820, GY + 4, 160)}${actor('s12O', OTU_OLD, 820, GY, 1.0, ['stand'])}</g></g>`;
// 13 · mi opinión: Zoro no es tonto, sigue intentando
M += `<g id="s13" opacity="0">${radBg('#1f6a3c', '#04120a', '#7dffa8', '#04120a')}${flr(540, GY + 4, 250)}
  ${actor('s13Z', OZ_AURA, 540, GY, 1.45, ['cross', 'stand'])}</g>`;
// 14 · ¿cómo entrenas tu orientación? (brújula)
M += `<g id="s14" opacity="0">${radBg('#5a3a1a', '#120a04', '#ffd23f', '#120a04')}${flr(330, GY + 4, 200)}${actor('s14T', OTU_MAP, 330, GY, 1.25, ['point'])}
  ${pg('s14cmp', 790, 760, `<circle cx="790" cy="760" r="190" fill="url(#yelGlow)" opacity=".5"/><circle cx="790" cy="760" r="150" fill="#f4ead2" stroke="#000" stroke-width="12"/><circle cx="790" cy="760" r="120" fill="none" stroke="#c9b892" stroke-width="5"/>
    ${TXT(790, 650, 48, 'N', '#e0283a', 'Anton')}${TXT(790, 905, 40, 'S', '#15121a', 'Anton')}${TXT(905, 775, 40, 'E', '#15121a', 'Anton')}${TXT(675, 775, 40, 'O', '#15121a', 'Anton')}
    ${pg('s14ndl', 790, 760, `<path d="M790,660 L816,760 L790,860 L764,760 Z" fill="#e0283a" stroke="#000" stroke-width="6"/><path d="M790,760 L816,760 L790,860 L764,760 Z" fill="#e8eef8" stroke="#000" stroke-width="6"/><circle cx="790" cy="760" r="14" fill="#15121a"/>`, true)}`)}</g>`;
// 15 · paso 1: mira el mapa 30 s y arma la ruta en tu cabeza
M += `<g id="s15" opacity="0">${radBg('#2a4c8a', '#071226', '#7fdcff', '#071226')}${flr(300, GY + 4, 190)}${actor('s15T', OTU_WALK, 300, GY, 1.15, ['stand', 'point'])}
  ${pg('s15map', 720, 860, `<g transform="rotate(-4 720 860)"><path d="M500,620 L640,650 L790,610 L940,640 L940,1100 L790,1070 L640,1110 L500,1080 Z" fill="#f4ead2" stroke="#000" stroke-width="8" stroke-linejoin="round"/>
     <path d="M640,650 L640,1110 M790,610 L790,1070" stroke="#000" stroke-opacity=".2" stroke-width="5"/><path d="M520,780 L920,760 M520,930 L920,940 M580,640 L560,1090 M860,630 L880,1080" stroke="#c9b892" stroke-width="16"/>
     <path id="s15route" d="M560,1040 L560,930 L700,930 L700,770 L860,770" fill="none" stroke="#e0283a" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="3000" stroke-dashoffset="3000"/></g>`)}
  ${pg('s15clk', 330, 560, `<circle cx="330" cy="580" r="120" fill="#f6f3ea" stroke="#000" stroke-width="10"/><rect x="305" y="430" width="50" height="36" rx="8" fill="#ddd" stroke="#000" stroke-width="6"/><text id="s15num" x="330" y="612" font-family="Anton" font-size="96" text-anchor="middle" fill="#e0283a">0</text>${TXT(330, 660, 30, 'SEG', '#15121a', 'Anton')}`)}
  ${pg('s15th', 330, 560, bubble(330, 560, 400, 280, `<g transform="translate(330,560) scale(.62)"><rect x="-210" y="-160" width="420" height="320" rx="20" fill="#f4ead2" stroke="#000" stroke-width="8"/><path d="M-170,130 L-170,20 L-10,20 L-10,-100 L170,-100" fill="none" stroke="#e0283a" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/><circle cx="170" cy="-100" r="22" fill="#e0283a" stroke="#000" stroke-width="6"/></g>`))}</g>`;
// 16 · paso 2: tres puntos fijos (tienda, puente, esquina) — nubes no
M += `<g id="s16" opacity="0"><rect width="1080" height="1920" fill="#1d3a2a"/><rect width="1080" height="1920" fill="url(#grid)" opacity=".35"/>
  <path d="M120,1300 L120,1000 L460,1000 L460,700 L900,700" fill="none" stroke="#3b3f4c" stroke-width="90" stroke-linejoin="round"/><path id="s16route" d="M120,1300 L120,1000 L460,1000 L460,700 L900,700" fill="none" stroke="#ffd23f" stroke-width="12" stroke-dasharray="26 18"/>
  ${pg('s16a', 250, 900, shop(250, 900))}${pg('s16ac', 330, 820, CHECK(330, 820, 40))}
  ${pg('s16b', 640, 1120, bridge(640, 1120))}${pg('s16bc', 740, 1070, CHECK(740, 1070, 40))}
  ${pg('s16c', 870, 600, corner(870, 600))}${pg('s16cc', 960, 520, CHECK(960, 520, 40))}
  ${pg('s16d', 300, 560, cloud(300, 560))}${pg('s16dx', 400, 520, CROSS(400, 520, 40))}
  ${flr(930, GY + 4, 150)}<g id="s16Zw" opacity="0">${actor('s16Z', OZ_LOST, 930, GY, .95, ['scratch'], '', true)}</g></g>`;
// 17 · paso 3: una vez por semana, calle nueva sin GPS
M += `<g id="s17" opacity="0">${nightBg()}
  ${pg('s17cal', 270, 560, `<rect x="90" y="440" width="360" height="260" rx="18" fill="#fff" stroke="#000" stroke-width="8"/><rect x="90" y="440" width="360" height="66" rx="18" fill="#2f74c8" stroke="#000" stroke-width="8"/>${TXT(270, 490, 40, 'SEMANA', '#fff', 'Anton')}
     ${['L', 'M', 'X', 'J', 'V', 'S', 'D'].map((d, i) => `${TXT(122 + i * 49, 570, 34, d, '#15121a', 'Anton')}<rect x="${102 + i * 49}" y="590" width="40" height="40" rx="8" fill="#e8eef8" stroke="#000" stroke-width="4"/>`).join('')}
     <path id="s17chk" d="M402,610 L414,624 L436,596" fill="none" stroke="#22b35a" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" opacity="0"/>`)}
  ${pg('s17sign', 820, 620, `<rect x="808" y="620" width="24" height="320" fill="#9aa4b8" stroke="#000" stroke-width="5"/><path d="M640,540 L960,540 L1010,600 L960,660 L640,660 Z" fill="#22b35a" stroke="#000" stroke-width="7" stroke-linejoin="round"/>${TXT(815, 620, 52, 'CALLE NUEVA', '#fff', 'Anton')}`)}
  ${pg('s17house', 930, 1250, house(930, 1250))}
  ${flr(420, GY + 4, 180)}${actor('s17T', OTU_WALK, 420, GY, 1.15, ['stand'])}
  ${pg('s17ph', 220, 900, `<g transform="translate(-340,0)"><rect x="500" y="800" width="120" height="200" rx="18" fill="#1b1b22" stroke="#000" stroke-width="7"/><rect x="512" y="820" width="96" height="160" rx="6" fill="#2f9be6"/><path d="M540,950 L560,850 L580,950 L560,936 Z" fill="#fff"/>${CROSS(600, 820, 44)}</g>`)}</g>`;
// 18 · etiqueta a tu Zoro (el que se pierde buscando el baño)
M += `<g id="s18" opacity="0">${radBg('#1f6a3c', '#04120a', '#ffd23f', '#04120a')}${flr(380, GY + 4, 200)}
  ${actor('s18Z', OZ_LOST, 380, GY, 1.25, ['stand', 'scratch'], '', true)}
  ${pg('s18tag', 540, 520, `<rect x="140" y="440" width="800" height="160" rx="80" fill="#fff" stroke="#000" stroke-width="8"/><circle cx="240" cy="520" r="58" fill="#e0283a" stroke="#000" stroke-width="6"/>${TXT(240, 548, 80, '@', '#fff', 'Anton')}${TXT(590, 548, 72, 'TU_ZORO', '#15121a', 'Anton')}`)}
  ${pg('s18arr', 540, 700, `<path d="M540,640 L540,760" stroke="#ffd23f" stroke-width="22" stroke-linecap="round"/><path d="M490,720 L540,775 L590,720" fill="none" stroke="#ffd23f" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>`)}
  ${pg('s18wc', 860, 1000, `<rect x="760" y="820" width="200" height="420" rx="10" fill="#8a5a2e" stroke="#000" stroke-width="8"/><circle cx="930" cy="1040" r="12" fill="#f2c13a" stroke="#000" stroke-width="4"/><rect x="790" y="860" width="140" height="80" rx="10" fill="#2f74c8" stroke="#000" stroke-width="6"/>${TXT(860, 918, 56, 'WC', '#fff', 'Anton')}`)}
  ${pg('s18q', 420, 760, QM(520, 760))}</g>`;
M += hook('s19');
M += `</g></g><rect width="1080" height="1920" fill="url(#vig)"/><rect id="flash" width="1080" height="1920" fill="#fff" opacity="0"/>`;
root.innerHTML = M;

// =============================================================== LÍNEA DE TIEMPO
// --- 1 · 0–3.54 · gancho (se repite al final para el bucle)
function hookTL(p, t0, tLinea, tY, tTu, endT) {
  scene(p, t0, endT);
  cam(t0, 540, 1000, 1.14, 0); cam(t0 + .02, 540, 960, 1.0, Math.max(.4, tY - t0), 'sine.inOut');
  // Zoro camina por la línea recta… y se sale
  walk(p + 'Z', t0, tY + .3, .3, .3, 3);
  tl.to(RIGS[p + 'Z'], { x: 250, duration: tY + .3 - t0, ease: 'power1.in' }, t0);
  big('LÍNEA RECTA', tLinea, tY + .02, '#ffd23f', 160);
  popS(p + 'q', tY, 'blip', .6); pose(p + 'Z', 1, tY);
  tl.to(RIGS[p + 'q'], { r: 6, duration: .25, yoyo: true, repeat: 5, ease: 'sine.inOut' }, tY + .2);
  // y tú vas por el mismo camino
  show(p + 'Tw', tTu); enter(p + 'T', tTu, -500, .35);
  walk(p + 'T', tTu + .35, endT, .32, .25, 2);
  tl.to(RIGS[p + 'T'], { x: 60, duration: endT - tTu, ease: 'none' }, tTu + .35);
  lab('Y TÚ… IGUAL', tTu + .1, endT, 'r');
  flash(tTu + .05, '#ff6b78', .25, .2);
}
hookTL('s1', 0, 1.12, 1.96, 2.2, 3.54);

// --- 2 · 3.54–6.02 · el espadachín más fuerte
cut(3.54); scene('s2', 3.54, 6.02);
cam(3.54, 540, 1000, 1.18, 0); cam(3.56, 540, 960, 1.0, .5, 'power2.out');
sfx(3.56, 'aura', .5); auraPulse('s2Z', 3.54, 6.02); breathe('s2Z', 3.54, 6.0, 5);
sfx(4.28, 'metal', .5); flash(4.28, '#bfffd2', .35, .2);
big('EL MÁS FUERTE', 4.7, 5.34, '#7dffa8', 150);
popS('s2hat', 5.34, 'pop', .6); tl.to(RIGS.s2hat, { r: 8, duration: .2, yoyo: true, repeat: 1 }, 5.5);
pill('SOMBRERO DE PAJA', 5.34, 6.02, 'y', null);

// --- 3 · 6.02–8.2 · ni su propio barco
cut(6.02); scene('s3', 6.02, 8.2);
cam(6.02, 540, 960, 1.0, 0);
walk('s3Z', 6.02, 6.9, .3, .3, 3); tl.to(RIGS.s3Z, { x: -120, duration: .9, ease: 'power1.out' }, 6.02);
sfx(6.3, 'splash', .25);
popS('s3arr', 6.68, 'pop', .6); tl.to(RIGS.s3arr, { y: 18, duration: .22, yoyo: true, repeat: 5 }, 6.9);
pose('s3Z', 1, 7.2); popS('s3q', 7.2, 'blip', .6);
lab('NI SU PROPIO BARCO', 7.2, 8.2, 'y', null);
tl.to(RIGS.s3ship, { y: 10, duration: .5, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 6.02);

// --- 4 · 8.2–11.74 · nos reímos… el chiste eres tú
cut(8.2); scene('s4', 8.2, 11.74);
cam(8.2, 540, 960, 1.0, 0); breathe('s4Z', 8.2, 9.4, 4);
JA.forEach((_, i) => { popS('s4j' + i, 8.3 + i * .2, 'pop', .45); tl.to(RIGS['s4j' + i], { y: -14, duration: .12, yoyo: true, repeat: 5 }, 8.5 + i * .2); hideS('s4j' + i, 9.5); });
pose('s4Z', 1, 8.4);
popS('s4sci', 9.68, 'glint', .7); hideS('s4sci', 10.4, .15);
show('s4Tw', 10.38); enter('s4T', 10.38, 500, .3);
popS('s4fing', 10.74, null); tl.to(RIGS.s4fing, { x: 20, duration: .15, yoyo: true, repeat: 3 }, 10.9);
cam(10.74, 780, 1050, 1.2, .3, 'power3.out');
stamp('EL CHISTE ERES TÚ', 10.74, 11.74, '#ff3346', 330);

// --- 5 · 11.74–16.04 · Londres, taxistas, 25 000 calles
cut(11.74); scene('s5', 11.74, 16.04);
cam(11.74, 540, 900, 1.12, 0); cam(11.76, 540, 960, 1.0, 1.0, 'sine.inOut');
pill('LONDRES', 11.86, 13.4, 'b');
ft(RIGS.s5cab, { x: 700 }, { x: 0, duration: .5, ease: 'power3.out' }, 12.6); sfx(12.6, 'whoosh', .6); sfx(13.0, 'horn', .45);
pose('s5D', 1, 13.06); breathe('s5D', 11.74, 13.0, 4);
tl.to('#s5map', { opacity: 1, duration: .3 }, 13.42); sfx(13.42, 'shimmer', .4);
popS('s5cnt', 13.82, 'pop', .6);
const CNT = { v: 0 };
ft(CNT, { v: 0 }, { v: 25000, duration: 1.0, ease: 'power2.out', onUpdate: () => { $('s5num').textContent = Math.round(CNT.v).toLocaleString('es-ES').replace(/\./g, ' '); } }, 14.18);
for (let t = 14.18; t < 15.2; t += .08) sfx(t, 'tick', .25);
sfx(15.2, 'ding', .7); ft(RIGS.s5cnt, { s: 1.15 }, { s: 1, duration: .25 }, 15.2);
lab('CALLES DE MEMORIA', 14.82, 16.04, 'y', null);

// --- 6 · 16.04–20.98 · Maguire escanea el cerebro → hipocampo más grande
cut(16.04); scene('s6', 16.04, 20.98);
cam(16.04, 540, 960, 1.0, 0);
popS('s6b', 16.1, 'pop', .6);
pill('NEUROCIENTÍFICA', 16.26, 16.9, 'b', null);
pill('ELEANOR MAGUIRE · UCL', 16.92, 18.7, 'b');
show('s6scan', 17.84); ft('#s6bar', { attr: { x: 120 } }, { attr: { x: 940 }, duration: .8, ease: 'power1.inOut' }, 17.84); sfx(17.84, 'riser', .5); sfx(17.84, 'blip', .5);
tl.set('#s6scan', { opacity: 0 }, 18.7);
big('MÁS GRANDE', 19.6, 20.98, '#ffd23f', 160);
ft('#s6bhip', { scale: 1, transformOrigin: '50% 50%' }, { scale: 1.45, duration: .45, ease: 'back.out(2.5)' }, 20.26); sfx(20.26, 'powerup', .5); flash(20.26, '#ffd23f', .3, .25);
popS('s6arr', 20.3, null);
lab('HIPOCAMPO', 20.26, 20.98, 'y', null);

// --- 7 · 20.98–24.78 · el mapa mental + años al volante
cut(20.98); scene('s7', 20.98, 24.78);
cam(20.98, 540, 960, 1.0, 0);
pill('TU MAPA MENTAL', 21.06, 22.78, 'y');
ft('#s7route', { attr: { 'stroke-dashoffset': 3000 } }, { attr: { 'stroke-dashoffset': 2120 }, duration: .9, ease: 'power1.inOut' }, 21.36); sfx(21.36, 'swish', .5);
tl.set('#s7pin', { opacity: 1 }, 22.26); sfx(22.26, 'ding', .5);
tl.set('#s7head', { opacity: 0 }, 22.78); tl.set('#s7chart', { opacity: 1 }, 22.78); sfx(22.78, 'whoosh', .5);
[0, 1, 2].forEach((i, k) => { const t = [23.16, 23.52, 24.22][k]; const h = 180 + i * 200; ft('#s7b' + i, { attr: { y: 1240, height: 0 } }, { attr: { y: 1240 - h, height: h }, duration: .35, ease: 'back.out(1.6)' }, t); sfx(t, 'blip', .55); });
tl.set('#s7b0', { attr: { height: 0, y: 1240 } }, 22.78); tl.set('#s7b1', { attr: { height: 0, y: 1240 } }, 22.78); tl.set('#s7b2', { attr: { height: 0, y: 1240 } }, 22.78);
tl.to(RIGS.s7wheel, { r: 360, duration: 1.8, ease: 'power1.inOut' }, 22.9);
big('MÁS GRANDE ↑', 24.22, 24.78, '#ffd23f', 130, 330);

// --- 8 · 24.78–30.24 · ¿y con GPS? McGill, 3 años
cut(24.78); scene('s8', 24.78, 30.24);
cam(24.78, 540, 960, 1.0, 0); breathe('s8T', 24.78, 30.2, 4);
popS('s8ph', 25.66, 'blip', .7); tl.to(RIGS.s8ph, { r: -3, duration: .3, yoyo: true, repeat: 3 }, 25.9);
pill('¿Y CON GPS?', 25.44, 26.78, 'r');
pill('UNIVERSIDAD McGILL', 26.78, 28.56, 'b');
hideS('s8ph', 28.9, .15);
popS('s8cal', 28.98, 'pop', .6);
[[1, 29.18], [2, 29.5], [3, 29.8]].forEach(([n, t]) => { tl.set('.s8y', { opacity: 0 }, t); tl.set('#s8y' + n, { opacity: 1 }, t); sfx(t, 'tick', .6); ft(RIGS.s8cal, { s: 1.1 }, { s: 1, duration: .2 }, t); });
lab('3 AÑOS SIGUIENDO CONDUCTORES', 28.56, 30.24, 'y', null);

// --- 9 · 30.24–33.66 · más GPS = menos memoria
cut(30.24); scene('s9', 30.24, 33.66);
cam(30.24, 540, 960, 1.0, 0);
pill('LOS QUE MÁS USABAN GPS', 30.34, 32.0, 'r');
drawPath('#s9line', 31.0, 1.2); sfx(31.0, 'reverse', .45);
popS('s9gps', 32.0, 'buzz', .5);
big('MEMORIA ↓', 32.36, 33.66, '#ff4a5a', 160);
shake(32.5, .25, 10);

// --- 10 · 33.66–39.64 · ¿por qué? flechas → hipocampo OFF → solo obedeces
cut(33.66); scene('s10', 33.66, 39.64);
cam(33.66, 540, 960, 1.0, 0);
big('¿POR QUÉ?', 33.66, 34.4, '#ffffff', 170);
ARR.forEach((_, i) => popS('s10a' + i, 34.7 + i * .14, 'blip', .5));
ARR.forEach((_, i) => tl.to(RIGS['s10a' + i], { y: -14, duration: .2, yoyo: true, repeat: 9 }, 35.3 + i * .05));
walk('s10T', 34.5, 39.6, .34, .22, 2);
pill('SIGUES LAS FLECHAS', 34.98, 35.76, 'b', null);
popS('s10th', 35.76, 'pop', .6);
tl.to('#s10hip', { opacity: .12, duration: .35 }, 36.48); sfx(36.48, 'switch', .9); sfx(36.52, 'reverse', .35);
popS('s10off', 36.7, 'buzz', .5);
lab('NO DECIDES NADA', 37.32, 38.36, 'r');
hideS('s10th', 38.2, .15); hideS('s10off', 38.2, .15);
stamp('SOLO OBEDECES', 38.38, 39.64, '#6fd3ff', 400);

// --- 11 · 39.64–44.0 · lo oscuro: Alzheimer
cut(39.64); scene('s11', 39.64, 44.0);
cam(39.64, 540, 960, 1.0, 0); cam(39.66, 540, 960, 1.08, 4.2, 'none');
big('LO OSCURO', 40.12, 41.0, '#ff4a5a', 170); sfx(40.12, 'rumble', .6);
popS('s11b', 41.0, null);
tl.to('#s11bhip', { opacity: .3, duration: .2, yoyo: true, repeat: 5 }, 41.2);
sfx(41.14, 'heartbeat', .55);
tl.set('#s11bcrk', { opacity: 1 }, 42.7); sfx(42.7, 'crack', .8); shake(42.72, .3, 16); flash(42.7, '#ff2d40', .4, .25);
big('ALZHEIMER', 43.08, 44.0, '#ff2d40', 170, 280); sfx(43.08, 'stinger', .5);

// --- 12 · 44.0–47.82 · Haki de reserva + cuando seas viejo
cut(44.0); scene('s12', 44.0, 47.82);
cam(44.0, 540, 900, 1.15, 0); cam(44.02, 540, 960, 1.0, .6, 'power2.out');
sfx(44.02, 'aura', .55); auraPulse('s12Z', 44.0, 46.0); breathe('s12Z', 44.0, 46.0, 4);
pill('UN BUEN MAPA MENTAL', 44.18, 45.2, 'y', null);
show('s12bolt', 45.24); tl.to('#s12bolt', { opacity: .2, duration: .06, yoyo: true, repeat: 9 }, 45.3); sfx(45.24, 'zap', .6);
big('HAKI DE RESERVA', 45.24, 46.2, '#c070ff', 130); flash(45.24, '#7a1fa0', .4, .3);
tl.to(RIGS.s12Z, { x: -230, s: .85, duration: .35, ease: 'power3.out' }, 46.2);
show('s12Ow', 46.2); enter('s12O', 46.2, 400, .35);
walk('s12O', 46.6, 47.8, .4, .2, 2);
lab('PARA CUANDO SEAS VIEJO', 46.36, 47.82, 'b');

// --- 13 · 47.82–53.12 · mi opinión: no es tonto
cut(47.82); scene('s13', 47.82, 53.12);
cam(47.82, 540, 960, 1.0, 0); auraPulse('s13Z', 47.82, 53.12); breathe('s13Z', 47.82, 50.2, 4);
pill('MI OPINIÓN', 47.82, 49.0, 'y');
big('NO ES TONTO', 49.18, 50.2, '#7dffa8', 160); sfx(49.3, 'metal', .45);
pose('s13Z', 1, 50.2);
sfx(50.8, 'swish', .4);
walk('s13Z', 50.8, 52.9, .3, .3, 3); tl.to(RIGS.s13Z, { x: -160, duration: 1.0, ease: 'sine.inOut' }, 50.8); tl.to(RIGS.s13Z, { x: 180, duration: 1.1, ease: 'sine.inOut' }, 51.8);
lab('SIGUE INTENTANDO', 50.8, 53.12, 'y');

// --- 14 · 53.12–55.88 · ¿cómo entrenas tu orientación?
cut(53.12); scene('s14', 53.12, 55.88);
cam(53.12, 540, 960, 1.0, 0); auraPulse('s14T', 53.12, 55.88); breathe('s14T', 53.12, 55.8, 4);
popS('s14cmp', 53.4, 'glint', .7);
tl.fromTo(RIGS.s14ndl, { r: 0 }, { r: 1080 + 20, duration: 1.6, ease: 'power3.out', immediateRender: false }, 54.0); sfx(54.0, 'swish', .5);
pill('¿CÓMO ENTRENAS TU ORIENTACIÓN?', 54.0, 55.88, 'y', null);
sfx(54.82, 'ding', .6);

// --- 15 · 55.88–60.86 · paso 1
cut(55.88); scene('s15', 55.88, 60.86);
cam(55.88, 540, 960, 1.0, 0); breathe('s15T', 55.88, 60.8, 4);
badge('1', 'Mira el mapa', 55.88, 60.86);
popS('s15map', 57.7, 'pop', .7); sfx(57.7, 'swish', .4);
popS('s15clk', 58.12, null);
const C30 = { v: 0 };
ft(C30, { v: 0 }, { v: 30, duration: .7, ease: 'none', onUpdate: () => { $('s15num').textContent = Math.round(C30.v); } }, 58.12);
for (let t = 58.14; t < 58.84; t += .07) sfx(t, 'tick', .3);
sfx(58.86, 'ding', .6); hideS('s15clk', 59.2, .15);
drawPath('#s15route', 59.26, .9); sfx(59.26, 'swish', .45);
pose('s15T', 1, 59.4);
popS('s15th', 59.9, 'pop', .6);
lab('ARMA LA RUTA EN TU CABEZA', 59.26, 60.86, 'y', null);

// --- 16 · 60.86–67.14 · paso 2
cut(60.86); scene('s16', 60.86, 67.14);
cam(60.86, 540, 960, 1.0, 0);
badge('2', '3 puntos fijos', 60.86, 67.14);
tl.fromTo('#s16route', { attr: { 'stroke-dashoffset': 0 } }, { attr: { 'stroke-dashoffset': -440 }, duration: 6.2, ease: 'none', immediateRender: false }, 60.86);
popS('s16a', 64.12, 'pop', .6); popS('s16ac', 64.3, 'ding', .6);
popS('s16b', 64.66, 'pop', .6); popS('s16bc', 64.84, 'ding', .6);
popS('s16c', 65.22, 'pop', .6); popS('s16cc', 65.4, 'ding', .6);
lab('TIENDA · PUENTE · ESQUINA', 64.12, 65.84, 'b', null);
popS('s16d', 65.84, 'swish', .5); tl.to(RIGS.s16d, { x: 120, duration: 1.2, ease: 'sine.inOut' }, 65.9);
popS('s16dx', 66.2, 'buzz', .55);
lab('QUE NO SE MUEVAN', 65.84, 66.6, 'r', null);
show('s16Zw', 66.6); ft(RIGS.s16Z, { x: 400 }, { x: 0, duration: .3, ease: 'power3.out' }, 66.6); sfx(66.6, 'whoosh', .5);
lab('¡ZORO!', 66.6, 67.14, 'y', null);

// --- 17 · 67.14–70.98 · paso 3
cut(67.14); scene('s17', 67.14, 70.98);
cam(67.14, 540, 960, 1.0, 0);
badge('3', 'Calle nueva, sin GPS', 67.14, 70.98);
popS('s17cal', 67.74, 'pop', .6);
tl.set('#s17chk', { opacity: 1 }, 68.1); sfx(68.1, 'ding', .6);
popS('s17sign', 68.7, 'pop', .6);
walk('s17T', 68.7, 70.9, .3, .3, 3); tl.to(RIGS.s17T, { x: 170, duration: 2.2, ease: 'none' }, 68.7);
popS('s17house', 68.92, 'pop', .5);
popS('s17ph', 70.06, 'buzz', .6); tl.to(RIGS.s17ph, { x: 10, duration: .05, yoyo: true, repeat: 5 }, 70.2);

// --- 18 · 70.98–74.24 · etiqueta a tu Zoro
cut(70.98); scene('s18', 70.98, 74.24);
cam(70.98, 540, 960, 1.0, 0); breathe('s18Z', 70.98, 72.8, 4);
popS('s18tag', 71.0, 'pop', .8); tl.to(RIGS.s18tag, { s: 1.06, duration: .3, yoyo: true, repeat: 3 }, 71.3);
popS('s18arr', 71.52, 'blip', .6); tl.to(RIGS.s18arr, { y: 20, duration: .25, yoyo: true, repeat: 3 }, 71.7);
hideS('s18arr', 72.9, .15);
popS('s18wc', 72.98, 'pop', .6);
pose('s18Z', 1, 72.98); popS('s18q', 73.18, 'blip', .6);
walk('s18Z', 73.2, 74.2, .3, .25, 3); tl.to(RIGS.s18Z, { x: -200, duration: 1.0, ease: 'none' }, 73.2);
lab('SE PIERDE BUSCANDO EL BAÑO', 72.04, 74.24, 'y', null);

// --- 19 · 74.24–END · vuelve al inicio (bucle)
cut(74.24);
hookTL('s19', 74.24, 75.44, 75.98, 76.36, END + 1);

// =============================================================== SUBTÍTULOS
(function subs() {
  const RED = /^(pierde|chiste|oscuro|alzheimer|apaga|obedeces|perdieron|nada|tonto|sin|ataca|gps)$/i;
  const YEL = /^(zoro|recta|línea|25 000|hipocampo|grande|mapa|mental|tres|30|segundos|1|2|3|haki|fuerte|espadachín|ciencia|memoria|espacial|calle|nueva|camino|ruta)$/i;
  const BLU = /^(londres|taxistas|maguire|eleanor|cerebro|mcgill|universidad|tienda|puente|esquina|orientación|etiqueta|flechas|reserva|barco|sombrero|paja|semana|neurocientífica|conductores)$/i;
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
