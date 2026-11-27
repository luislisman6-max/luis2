// BLACK FLASH — motor + escenas + efectos + subtítulos (voz 85.6 s)
const END = 85.6;
const tl = gsap.timeline({ paused: true });
const SFX = []; window.SFX = SFX;
const sfx = (t, n, v = 1) => SFX.push([+t.toFixed(3), n, v]);
const root = document.getElementById('root'), ui = document.getElementById('ui');
let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
const R = (a, b) => a + (b - a) * rnd();
const ft = (el, a, b, t) => tl.fromTo(el, a, Object.assign({ immediateRender: false }, b), t);
const $ = id => document.getElementById(id);

// ---------- rigs: transformaciones con origen fijo (aplicadas tras cada seek)
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
function tint(t, col, o, hold = .4) { tl.set('#tint', { attr: { fill: col } }, t); ft('#tint', { opacity: o }, { opacity: 0, duration: hold, ease: 'power1.in' }, t + .05); }

// ---------- utilería SVG
const OLc = '#15121a';
const TXT = (x, y, s, txt, col = '#fff', fam = 'Oswald', ex = '') => `<text x="${x}" y="${y}" font-family="${fam},Impact,sans-serif" font-weight="700" font-size="${s}" fill="${col}" text-anchor="middle" ${ex}>${txt}</text>`;
function pg(id, cx, cy, inner, vis = false) { rig(id, cx, cy); return `<g id="${id}" ${vis ? '' : 'opacity="0"'}>${inner}</g>`; }
function popS(id, t, snd = 'pop', v = .5, d = .3) { if (snd) sfx(t, snd, v); tl.set('#' + id, { opacity: 1 }, t); ft(RIGS[id], { s: 0 }, { s: 1, duration: d, ease: 'back.out(2.4)' }, t); }
function hideS(id, t, d = .2) { tl.to('#' + id, { opacity: 0, duration: d }, t); }
function scene(id, t0, t1) { tl.set('#' + id, { opacity: 1 }, t0); tl.set('#' + id, { opacity: 0 }, t1); }
function cut(t) { sfx(t, 'whoosh', .45); flash(t, '#fff', .25, .18); }

// personaje con variantes de pose; el grupo rig usa coordenadas de pantalla (pies = origen)
function actor(id, o, x, gy, s, poses = ['guard', 'punch'], extra = '') {
  const vs = poses.map((p, i) => `<g class="pv pv${i}" ${i ? 'opacity="0"' : ''}>${p === 'curse' ? curse() : person(Object.assign({}, o, { pose: p }))}</g>`).join('');
  rig(id, x, gy);
  return `<g id="${id}"><g transform="translate(${x - 200 * s},${gy - 620 * s}) scale(${s})">${vs}</g>${extra}</g>`;
}
function tintCopy(id, o, x, gy, s, pose, col) {
  return `<g id="${id}" opacity="0" filter="url(#fl_${col.slice(1)})"><g transform="translate(${x - 200 * s},${gy - 620 * s}) scale(${s})">${person(Object.assign({}, o, { pose }))}</g></g>`;
}
function pose(id, i, t) { tl.set(`#${id} .pv`, { opacity: 0 }, t); tl.set(`#${id} .pv${i}`, { opacity: 1 }, t); }
const lp = (x, gy, s, lx, ly) => [x + (lx - 200) * s, gy - (620 - ly) * s];

// saco de boxeo colgado (pivote = enganche de la cadena)
function bag(id, px, py, s = 1) {
  rig(id, px, py);
  let ch = '';
  for (let y = py; y < py + 360 * s; y += 24 * s) ch += `<ellipse cx="${px}" cy="${y + 12 * s}" rx="${6 * s}" ry="${11 * s}" fill="none" stroke="#9aa0a8" stroke-width="${4 * s}"/>`;
  const x0 = px - 85 * s, y0 = py + 370 * s, w = 170 * s, h = 640 * s;
  return `<g id="${id}">${ch}
    <path d="M${px - 60 * s},${y0 + 6 * s} L${px},${py + 340 * s} L${px + 60 * s},${y0 + 6 * s}" fill="none" stroke="#7d828a" stroke-width="${4 * s}"/>
    <rect x="${x0}" y="${y0}" width="${w}" height="${h}" rx="${30 * s}" fill="#c0222c" stroke="${OLc}" stroke-width="${5 * s}"/>
    <rect x="${x0 + w * .62}" y="${y0 + 6 * s}" width="${w * .34}" height="${h - 12 * s}" rx="${24 * s}" fill="#000" opacity=".22"/>
    <rect x="${x0 + w * .14}" y="${y0 + 20 * s}" width="${w * .1}" height="${h - 60 * s}" rx="${8 * s}" fill="#fff" opacity=".16"/>
    <ellipse cx="${px}" cy="${y0 + 8 * s}" rx="${w / 2 - 6 * s}" ry="${14 * s}" fill="#8e1820" stroke="${OLc}" stroke-width="${4 * s}"/>
    <rect x="${x0}" y="${y0 + 210 * s}" width="${w}" height="${70 * s}" fill="#121216"/>
    ${TXT(px, y0 + 258 * s, 40 * s, 'HEAVY', '#f2f2f2', 'Oswald', `letter-spacing="${3 * s}"`)}
    <rect x="${x0}" y="${y0}" width="${w}" height="${h}" rx="${30 * s}" fill="none" stroke="${OLc}" stroke-width="${5 * s}"/></g>`;
}
function bagHit(id, t, amt = -9) {
  tl.to(RIGS[id], { r: amt, duration: .12, ease: 'power2.out' }, t);
  tl.to(RIGS[id], { r: -amt * .45, duration: .45, ease: 'sine.inOut' }, t + .12);
  tl.to(RIGS[id], { r: 0, duration: .5, ease: 'sine.inOut' }, t + .57);
}
function bagFly(id, t) {
  sfx(t + .05, 'chain', .9);
  tl.to(RIGS[id], { r: -72, duration: .32, ease: 'power3.out' }, t);
  tl.to(RIGS[id], { r: 30, duration: .7, ease: 'sine.inOut' }, t + .32);
  tl.to(RIGS[id], { r: -12, duration: .6, ease: 'sine.inOut' }, t + 1.02);
  tl.to(RIGS[id], { r: 0, duration: .6, ease: 'sine.inOut' }, t + 1.62);
  sfx(t + 1.0, 'chain', .5);
}
// golpe: pose de puñetazo + pequeño avance del cuerpo
function punch(id, t, hold = .25, push = 18) {
  sfx(t - .08, 'swish', .55);
  pose(id, 1, t - .04);
  tl.to(RIGS[id], { x: push, duration: .08, ease: 'power2.out' }, t - .04);
  tl.to(RIGS[id], { x: 0, duration: .2, ease: 'power1.inOut' }, t + hold);
  pose(id, 0, t + hold);
}

// rayo rojo radial del Black Flash
function bfx(id, x, y, Rr = 380, n = 13) {
  let b = '';
  for (let i = 0; i < n; i++) {
    const a = (i / n) * Math.PI * 2 + R(-.15, .15), L = Rr * R(.65, 1.1);
    let px = x + Math.cos(a) * 34, py = y + Math.sin(a) * 34, d = `M${px.toFixed(1)},${py.toFixed(1)}`;
    const steps = 7;
    for (let k = 1; k <= steps; k++) {
      const rr = 34 + (L - 34) * k / steps, j = k < steps ? R(-26, 26) : 0;
      px = x + Math.cos(a) * rr - Math.sin(a) * j; py = y + Math.sin(a) * rr + Math.cos(a) * j;
      d += ` L${px.toFixed(1)},${py.toFixed(1)}`;
      if (k === 3 || k === 5) { const a2 = a + R(-.7, .7); d += ` M${px.toFixed(1)},${py.toFixed(1)} l${(Math.cos(a2) * L * .22).toFixed(1)},${(Math.sin(a2) * L * .22).toFixed(1)} M${px.toFixed(1)},${py.toFixed(1)}`; }
    }
    b += `<path d="${d}" fill="none" stroke="#ff1f35" stroke-width="26" stroke-linecap="round" stroke-linejoin="round" opacity=".35" filter="url(#blur8)"/>
          <path d="${d}" fill="none" stroke="#ff2d40" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="${d}" fill="none" stroke="#0a0004" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>`;
  }
  return pg(id, x, y, `<circle cx="${x}" cy="${y}" r="${Rr * .75}" fill="url(#redGlow)"/>${b}
    <circle cx="${x}" cy="${y}" r="46" fill="#0a0004" stroke="#ff2d40" stroke-width="8"/><circle cx="${x}" cy="${y}" r="18" fill="#fff"/>`);
}
function sparks(id, x, y, n = 22) {
  let s = '';
  for (let i = 0; i < n; i++) {
    const r = R(7, 16);
    s += `<path class="sp" d="M${x},${y - r} L${x + r * .5},${y} L${x},${y + r} L${x - r * .5},${y} Z" fill="${i % 3 ? '#0a0004' : '#ff2d40'}" stroke="#ff4050" stroke-width="2"/>`;
  }
  return `<g id="${id}" opacity="0">${s}</g>`;
}
function burstSparks(id, t, dist = 380) {
  tl.set('#' + id, { opacity: 1 }, t);
  document.querySelectorAll(`#${id} .sp`).forEach((el, i, all) => {
    const a = i / all.length * Math.PI * 2 + R(-.2, .2), d = dist * R(.5, 1.1);
    ft(el, { x: 0, y: 0, opacity: 1 }, { x: Math.cos(a) * d, y: Math.sin(a) * d + 60, opacity: 0, duration: R(.6, 1.0), ease: 'power2.out' }, t);
  });
  tl.set('#' + id, { opacity: 0 }, t + 1.1);
}
// ¡BLACK FLASH! completo
function blackFlash(fx, t, o = {}) {
  sfx(t, 'bf', 1);
  tl.set('#' + fx, { opacity: 1 }, t);
  ft(RIGS[fx], { s: .15, r: 0 }, { s: 1, r: 8, duration: .2, ease: 'power4.out' }, t);
  tl.to(RIGS[fx], { s: 1.08, r: 12, duration: .7, ease: 'none' }, t + .2);
  tl.to('#' + fx, { opacity: .55, duration: .05, yoyo: true, repeat: 3 }, t + .22);
  tl.to('#' + fx, { opacity: 0, duration: .25 }, t + .7);
  flash(t, '#ff2d40', .55, .35); tint(t + .05, '#ff0a24', .3, .5); shake(t, .5, o.shake || 26);
  if (o.sparks) burstSparks(o.sparks, t + .02);
  if (o.kanji !== false) kanji(t + .02, t + (o.kdur || 1.2));
}

// ---------- interfaz (HTML)
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
function big(txt, t0, t1, col = '#ffd23f') {
  const d = addDiv('big', txt, `color:${col};text-shadow:${strokeShadow(10)}`);
  ft(d, { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: .16, ease: 'power4.in' }, t0);
  tl.to(d, { scale: 1.06, duration: Math.max(.1, t1 - t0 - .3), ease: 'none' }, t0 + .16);
  tl.to(d, { opacity: 0, duration: .14 }, t1 - .14);
  sfx(t0 + .12, 'slam', .7); shake(t0 + .16, .2, 12);
}
function kanji(t0, t1) {
  const d = addDiv('kanji', '黒閃');
  ft(d, { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: .14, ease: 'power3.out' }, t0);
  tl.to(d, { opacity: .6, duration: .04, yoyo: true, repeat: 3 }, t0 + .2);
  tl.to(d, { opacity: 0, duration: .2 }, t1 - .2);
}
let TITLE;
function title(t0, t1, snd = true) {
  const d = addDiv('title', 'BLACK FLASH');
  if (snd) sfx(t0, 'neon', .7);
  tl.set(d, { opacity: 1 }, t0);
  [.05, .1, .16, .22].forEach((k, i) => tl.set(d, { opacity: i % 2 ? 1 : .25 }, t0 + k));
  tl.set(d, { opacity: 1 }, t0 + .28);
  tl.set(d, { opacity: 0 }, t1);
  return d;
}
function badge(n, txt, t0, t1) { return popUI(addDiv('badge', `<b>${n}</b>${txt}`), t0, t1, 'pop', .6); }

// ---------- defs y fondos
const defs = `<defs>
<filter id="blur8" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="blur20" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="20"/></filter>
<filter id="glowB" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="fl_ff2d40"><feFlood flood-color="#ff2d40"/><feComposite in2="SourceAlpha" operator="in"/></filter>
<filter id="fl_3aa8ff"><feFlood flood-color="#3aa8ff"/><feComposite in2="SourceAlpha" operator="in"/></filter>
<pattern id="brick" width="140" height="64" patternUnits="userSpaceOnUse"><rect width="140" height="64" fill="#3d2c26"/><rect x="2" y="2" width="136" height="28" fill="#47332b"/><rect x="-68" y="34" width="136" height="28" fill="#43302a"/><rect x="72" y="34" width="136" height="28" fill="#4a352d"/></pattern>
<pattern id="mesh" width="46" height="46" patternUnits="userSpaceOnUse"><path d="M0,23 L23,0 L46,23 L23,46 Z" fill="none" stroke="#7d8594" stroke-width="3"/></pattern>
<pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M60,0 L0,0 L0,60" fill="none" stroke="#1f2a44" stroke-width="2"/></pattern>
<linearGradient id="spot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff1c8" stop-opacity=".32"/><stop offset="1" stop-color="#fff1c8" stop-opacity=".02"/></linearGradient>
<radialGradient id="spotFloor"><stop offset="0" stop-color="#fff1c8" stop-opacity=".28"/><stop offset="1" stop-color="#fff1c8" stop-opacity="0"/></radialGradient>
<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d0820"/><stop offset="1" stop-color="#2d1650"/></linearGradient>
<radialGradient id="redBg" cx="50%" cy="42%" r="70%"><stop offset="0" stop-color="#6a0a16"/><stop offset=".6" stop-color="#2a040b"/><stop offset="1" stop-color="#0c0204"/></radialGradient>
<radialGradient id="redGlow"><stop offset="0" stop-color="#ff3346" stop-opacity=".75"/><stop offset="1" stop-color="#ff0022" stop-opacity="0"/></radialGradient>
<radialGradient id="auraBlue"><stop offset="0" stop-color="#e8fbff"/><stop offset=".35" stop-color="#5fd0ff" stop-opacity=".9"/><stop offset="1" stop-color="#2a6cff" stop-opacity="0"/></radialGradient>
<radialGradient id="floorSh"><stop offset="0" stop-color="#000" stop-opacity=".6"/><stop offset="1" stop-opacity="0"/></radialGradient>
<radialGradient id="yelGlow"><stop offset="0" stop-color="#ffe27a" stop-opacity=".9"/><stop offset="1" stop-color="#ffb800" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx="50%" cy="48%" r="75%"><stop offset=".6" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>
</defs>`;
const DUST = Array.from({ length: 34 }, () => [R(260, 840), R(80, 1350), R(1.5, 3.5), R(.15, .5)]);
function gym(extra = '') {
  let s = `<rect width="1080" height="1920" fill="#17110f"/><rect width="1080" height="1260" fill="url(#brick)"/>
  <rect width="1080" height="1260" fill="#000" opacity=".35"/>
  <rect x="70" y="330" width="170" height="230" fill="#c8ad45" opacity=".85" stroke="#000" stroke-width="4"/>${TXT(155, 400, 52, 'FIGHT', '#3a3010', 'Oswald')}<rect x="100" y="430" width="110" height="10" fill="#3a3010" opacity=".6"/><rect x="100" y="455" width="80" height="10" fill="#3a3010" opacity=".6"/>
  <rect x="880" y="300" width="170" height="230" fill="#c9484a" opacity=".85" stroke="#000" stroke-width="4"/>${TXT(965, 370, 52, 'NIGHT', '#3a0a0a', 'Oswald')}<rect x="910" y="400" width="110" height="10" fill="#3a0a0a" opacity=".6"/>
  <rect x="20" y="880" width="26" height="440" fill="#2a2a30" stroke="#000" stroke-width="4"/><rect x="1034" y="880" width="26" height="440" fill="#2a2a30" stroke="#000" stroke-width="4"/>`;
  [[960, '#c92a35'], [1040, '#e9e6df'], [1120, '#c92a35']].forEach(([y, c]) => s += `<rect x="0" y="${y - 9}" width="1080" height="18" fill="${c}" stroke="#000" stroke-width="3"/>`);
  s += `<rect y="1260" width="1080" height="660" fill="#1d1613"/>`;
  for (let i = 0; i < 9; i++) s += `<line x1="${-400 + i * 235}" y1="1920" x2="${300 + i * 60}" y2="1260" stroke="#000" stroke-width="3" opacity=".35"/>`;
  s += `<rect y="1255" width="1080" height="10" fill="#000" opacity=".5"/>
  <polygon points="420,0 660,0 1010,1440 70,1440" fill="url(#spot)"/><ellipse cx="540" cy="1440" rx="470" ry="90" fill="url(#spotFloor)"/>`;
  s += DUST.map(([x, y, r, o]) => `<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${r.toFixed(1)}" fill="#fff6dc" opacity="${o.toFixed(2)}"/>`).join('');
  return s + extra;
}
function nightBg() {
  let s = `<rect width="1080" height="1920" fill="url(#night)"/><circle cx="820" cy="330" r="170" fill="#e8e0ff" opacity=".18" filter="url(#blur20)"/><circle cx="820" cy="330" r="74" fill="#f1ecff"/>`;
  for (let i = 0; i < 40; i++) s += `<circle cx="${R(0, 1080).toFixed(0)}" cy="${R(0, 800).toFixed(0)}" r="${R(1, 2.6).toFixed(1)}" fill="#fff" opacity="${R(.3, .8).toFixed(2)}"/>`;
  let x = -20;
  while (x < 1100) {
    const w = R(110, 190), h = R(260, 520), y = 1430 - h;
    s += `<rect x="${x.toFixed(0)}" y="${y.toFixed(0)}" width="${w.toFixed(0)}" height="${h.toFixed(0)}" fill="#160d2a" stroke="#0a0614" stroke-width="4"/>`;
    for (let wy = y + 30; wy < 1400; wy += 56) for (let wx = x + 20; wx < x + w - 30; wx += 44) if (rnd() > .62) s += `<rect x="${wx.toFixed(0)}" y="${wy.toFixed(0)}" width="20" height="26" fill="#f5c84c" opacity=".55"/>`;
    x += w + R(4, 20);
  }
  return s + `<rect y="1430" width="1080" height="490" fill="#0d0819"/><rect y="1426" width="1080" height="8" fill="#000" opacity=".6"/>`;
}
function redBg() {
  let s = `<rect width="1080" height="1920" fill="url(#redBg)"/>`;
  for (let i = 0; i < 46; i++) { const a = i / 46 * Math.PI * 2 + R(-.05, .05), r0 = R(260, 420); s += `<line x1="${(540 + Math.cos(a) * r0).toFixed(0)}" y1="${(820 + Math.sin(a) * r0).toFixed(0)}" x2="${(540 + Math.cos(a) * 1500).toFixed(0)}" y2="${(820 + Math.sin(a) * 1500).toFixed(0)}" stroke="#ff2d40" stroke-width="${R(2, 6).toFixed(1)}" opacity="${R(.25, .6).toFixed(2)}"/>`; }
  return s + `<rect y="1430" width="1080" height="490" fill="#0c0204" opacity=".85"/><ellipse cx="540" cy="1432" rx="300" ry="34" fill="url(#floorSh)"/>`;
}
const fsh = (x, y, rx = 200) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="26" fill="url(#floorSh)"/>`;

// ---------- personajes
const OBOX = { skin: '#b67b52', hair: 'short', hairC: '#1f1b22', top: 'tank', topC: '#34373f', bottom: '#202127', band: '#d8323a', gloves: 'wrap', wrapC: '#d8323a', shoes: '#26262c', sole: '#bdbab3', angry: true };
const OYUJI = { skin: '#f2d0b4', hair: 'yuji', hairC: '#f18aa5', eyes: 'anime', iris: '#a5652a', marks: true, smirk: true, top: 'uniform', topC: '#1d2336', hood: '#c8323c', bottom: '#1a1f30', pants: true, shoes: '#d0313a', sole: '#f2efe6', aura: true, brow: '#4a2f36' };
const OKAR = { skin: '#a8714a', hair: 'short', hairC: '#1b181d', top: 'gi', topC: '#eeece6', bottom: '#eeece6', pants: true, shoes: 'barefoot' };
const OGYM = { skin: '#c48a5c', hair: 'buzz', hairC: '#3a2a22', top: 'tee', topC: '#2f74c8', bottom: '#1f2026', shoes: '#e8e6e0', sole: '#9c9a94' };
const OMMA = { skin: '#9a6440', hair: 'buzz', hairC: '#151317', top: 'none', bottom: '#c62a33', band: '#111', gloves: 'mma', shoes: 'barefoot', angry: true };
// posiciones comunes del gimnasio
const BX = 380, BG = 1430, BS = 1.55, BAGX = 768, BAGY = 150;
const CONTACT = [BX + (396 - 200) * BS + 22, BG - (620 - 230) * BS];   // puño extendido

// =============================================================== ESCENAS (markup)
let M = defs + `<g id="camS"><g id="camZ">`;
// 1 · Yuji en fondo rojo (también se reutiliza para el final en bucle)
function yujiSolo(p) {
  return `<g id="${p}" opacity="0">${redBg()}${actor(p + 'Y', OYUJI, 540, 1430, 1.8, ['stand'])}${bfx(p + 'fx', ...lp(540, 1430, 1.8, 262, 404), 190, 9)}</g>`;
}
M += yujiSolo('s1');
// 2/3 · gimnasio con el boxeador
function gymScene(p, o = {}) {
  return `<g id="${p}" opacity="0">${gym()}${fsh(BX, BG + 4, 240)}${actor(p + 'B', OBOX, BX, BG, BS)}${bag(p + 'bag', BAGX, BAGY)}
  ${o.trail ? `<path id="${p}trail" d="M${BX + 60},${BG - 640} Q${BX + 200},${BG - 700} ${CONTACT[0] - 10},${CONTACT[1]}" fill="none" stroke="#ffd23f" stroke-width="8" stroke-dasharray="4 18" stroke-linecap="round" opacity="0"/>
    <circle id="${p}trailDot" cx="${CONTACT[0] - 10}" cy="${CONTACT[1]}" r="16" fill="#ffd23f" opacity="0"/>` : ''}
  ${bfx(p + 'fx', ...CONTACT, 420)}${sparks(p + 'sp', ...CONTACT)}${o.extra || ''}</g>`;
}
M += gymScene('s2', { trail: true });
// 4/5 · Yuji contra la maldición (noche)
const YX = 330, YG = 1430, YS = 1.4, CX = 810, CS = 1.15;
const YCON = [YX + (396 - 200) * YS + 40, YG - (620 - 230) * YS];
let cracks = '';
for (let i = 0; i < 7; i++) {
  let x = YCON[0], y = YCON[1], d = `M${x},${y}`; const a = i / 7 * Math.PI * 2 + .3;
  for (let k = 0; k < 6; k++) { x += Math.cos(a) * 150 + R(-50, 50); y += Math.sin(a) * 150 + R(-50, 50); d += ` L${x.toFixed(0)},${y.toFixed(0)}`; }
  cracks += `<path d="${d}" fill="none" stroke="#fff" stroke-width="6" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" class="ck"/><path d="${d}" fill="none" stroke="#ff2d40" stroke-width="2" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" class="ck"/>`;
}
M += `<g id="s4" opacity="0">${nightBg()}${fsh(YX, YG, 200)}${fsh(CX, YG, 230)}
  ${actor('s4C', {}, CX, YG, CS, ['curse'])}${actor('s4Y', OYUJI, YX, YG, YS, ['stand', 'punch'])}
  <g id="s4ck">${cracks}</g>${bfx('s4fx', ...YCON, 460)}${bfx('s4fx2', ...YCON, 300, 9)}${sparks('s4sp', ...YCON, 30)}
  <g id="s4hud" opacity="0" transform="translate(0,40)"><rect x="110" y="1650" width="860" height="170" rx="18" fill="#0b0816" opacity=".85" stroke="#3a2d5a" stroke-width="3"/>
    ${TXT(175, 1695, 30, 'PUÑO', '#fff')}${TXT(905, 1695, 30, 'IMPACTO', '#ff4a5a')}
    <line x1="170" y1="1722" x2="900" y2="1722" stroke="#4b4470" stroke-width="4"/><line x1="170" y1="1772" x2="900" y2="1772" stroke="#4b4470" stroke-width="4"/>
    <rect id="s4imp" x="896" y="1700" width="8" height="96" fill="#ff2d40"/>
    <rect id="s4mF" x="158" y="1708" width="26" height="28" rx="5" fill="#fff"/><circle id="s4mE" cx="171" cy="1772" r="14" fill="#5fd0ff" filter="url(#glowB)"/>
    ${TXT(260, 1810, 26, 'ENERGÍA MALDITA', '#5fd0ff')}</g>
  ${pg('s4time', 760, 1290, `<rect x="610" y="1256" width="300" height="70" rx="12" fill="#1a1406" stroke="#ffd23f" stroke-width="4"/>${TXT(760, 1306, 46, '0.000001 s', '#ffd23f')}`)}
</g>`;
// 6 · no es fuerza, es timing
M += `<g id="s6" opacity="0"><rect width="1080" height="1920" fill="#0c0b14"/><rect width="1080" height="1920" fill="url(#grid)"/>
  ${pg('s6dum', 290, 820, `<rect x="150" y="790" width="280" height="60" rx="14" fill="#8a8f99" stroke="#000" stroke-width="6"/>
     <rect x="120" y="690" width="70" height="260" rx="16" fill="#3b3f48" stroke="#000" stroke-width="6"/><rect x="390" y="690" width="70" height="260" rx="16" fill="#3b3f48" stroke="#000" stroke-width="6"/>
     ${TXT(290, 1080, 72, 'FUERZA', '#fff', 'Anton')}`)}
  ${pg('s6x', 290, 820, `<path d="M150,680 L430,960 M430,680 L150,960" stroke="#ff2d40" stroke-width="34" stroke-linecap="round"/>`)}
  ${pg('s6clk', 790, 820, `<circle cx="790" cy="820" r="185" fill="url(#yelGlow)" opacity=".5"/><rect x="760" y="590" width="60" height="50" rx="10" fill="#ddd" stroke="#000" stroke-width="6"/>
     <circle cx="790" cy="820" r="160" fill="#f6f3ea" stroke="#000" stroke-width="10"/>${[...Array(12)].map((_, i) => { const a = i / 12 * Math.PI * 2; return `<line x1="${790 + Math.cos(a) * 128}" y1="${820 + Math.sin(a) * 128}" x2="${790 + Math.cos(a) * 146}" y2="${820 + Math.sin(a) * 146}" stroke="#000" stroke-width="6"/>`; }).join('')}
     ${pg('s6hand', 790, 820, `<line x1="790" y1="820" x2="790" y2="690" stroke="#e0283a" stroke-width="10" stroke-linecap="round"/><circle cx="790" cy="820" r="14" fill="#000"/>`, true)}
     ${TXT(790, 1080, 72, 'TIMING', '#ffd23f', 'Anton')}`)}
  ${pg('s6ok', 900, 690, `<circle cx="900" cy="690" r="62" fill="#22b35a" stroke="#fff" stroke-width="8"/><path d="M868,690 L892,716 L936,664" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>`)}
</g>`;
// 7 · tu puño funciona igual
M += gymScene('s7', { extra: bfx('s7fx', ...lp(BX, BG, BS, 238, 200), 150, 9) });
// 8/9 · estudio de Londres (pantalla dividida)
function panel(y0, h) { return `<rect x="30" y="${y0}" width="1020" height="${h}" rx="18" fill="#2f3a4c" stroke="#121620" stroke-width="6"/><circle cx="70" cy="${y0 + 36}" r="11" fill="#ff3346"/><circle cx="1010" cy="${y0 + 36}" r="11" fill="#ff3346"/><rect x="30" y="${y0 + h - 70}" width="1020" height="70" rx="0" fill="#1f2734"/>`; }
const KX = 330, KG1 = 810, KG2 = 1410, KS = .82;
function pad(id, x, gy) { rig(id, x, gy - 240); return `<g id="${id}"><rect x="${x}" y="${gy - 390}" width="44" height="220" rx="12" fill="#1d2129" stroke="#000" stroke-width="5"/><rect x="${x + 14}" y="${gy - 170}" width="14" height="170" fill="#3a404c" stroke="#000" stroke-width="4"/></g>`; }
const PADX = KX + 52;
function ring(id, x, y) { return pg(id, x, y, `<circle cx="${x}" cy="${y}" r="50" fill="none" stroke="#fff" stroke-width="7"/><circle cx="${x}" cy="${y}" r="22" fill="#fff" opacity=".6"/>`); }
function bar(id, x, y, w, col, lbl) { return `${TXT(x + 210, y - 18, 32, lbl, '#cfd6e4')}<rect x="${x}" y="${y}" width="420" height="44" rx="10" fill="#151a24" stroke="#000" stroke-width="4"/><rect id="${id}" x="${x + 4}" y="${y + 4}" width="0" height="36" rx="7" fill="${col}"/>`; }
M += `<g id="s8" opacity="0"><rect width="1080" height="1920" fill="#232b39"/>${panel(220, 610)}${panel(830, 610)}
  <g id="s8top" opacity="0">${pad('s8p1', PADX, KG1)}${actor('s8K', OKAR, KX, KG1, KS, ['guard'])}${TXT(790, 400, 50, 'CINTURONES NEGROS', '#ffd23f')}${bar('s8b1', 580, 490, 0, '#ffd23f', 'FUERZA DEL GOLPE')}${ring('s8r1', PADX, KG1 - 300)}</g>
  <g id="s8bot" opacity="0">${pad('s8p2', PADX, KG2)}${actor('s8G', OGYM, KX, KG2, KS, ['guard'])}${TXT(790, 940, 50, 'GENTE DEL GYM', '#fff')}${bar('s8b2', 580, 1040, 0, '#e8eef8', 'FUERZA DEL GOLPE')}${ring('s8r2', PADX, KG2 - 300)}</g>
  ${pg('s8cm', PADX - 18, KG1 - 340, `<path d="M${PADX - 40},${KG1 - 330} L${PADX - 40},${KG1 - 350} M${PADX - 40},${KG1 - 340} L${PADX},${KG1 - 340} M${PADX},${KG1 - 330} L${PADX},${KG1 - 350}" stroke="#ffd23f" stroke-width="5"/>${TXT(PADX - 20, KG1 - 360, 30, '5 CM', '#ffd23f')}`)}
  ${pg('s8pct', 860, 640, TXT(860, 680, 120, '+50%', '#ffd23f', 'Anton', `stroke="#000" stroke-width="6" paint-order="stroke"`))}
  ${pg('s8mus', 540, 830, `<rect x="140" y="640" width="800" height="380" rx="22" fill="#0e121b" stroke="#fff" stroke-width="5"/>${TXT(540, 715, 54, 'FUERZA MUSCULAR', '#fff')}
     ${TXT(250, 800, 32, 'NEGROS', '#ffd23f', 'Oswald', 'text-anchor="start"')}<rect x="400" y="772" width="460" height="40" rx="9" fill="#ffd23f"/>
     ${TXT(250, 880, 32, 'GYM', '#e8eef8', 'Oswald', 'text-anchor="start"')}<rect x="400" y="852" width="460" height="40" rx="9" fill="#e8eef8"/>
     ${TXT(540, 975, 56, '= IGUAL', '#22d36a', 'Anton')}`)}
</g>`;
// 10 · curvas de velocidad hombro / muñeca
function gauss(baseY, peakX, h, w) { let d = ''; for (let x = 150; x <= 930; x += 6) { const y = baseY - h * Math.exp(-((x - peakX) ** 2) / (2 * w * w)); d += (d ? ' L' : 'M') + x + ',' + y.toFixed(1); } return d; }
function graph(y0, ttl, col, sP, wP) {
  const base = y0 + 410;
  return `<rect x="70" y="${y0}" width="940" height="490" rx="18" fill="#0f1730" stroke="#2c3e6e" stroke-width="4"/>${TXT(540, y0 + 62, 46, ttl, col)}
  <line x1="150" y1="${base}" x2="930" y2="${base}" stroke="#4a5a88" stroke-width="4"/><line x1="150" y1="${base}" x2="150" y2="${y0 + 100}" stroke="#4a5a88" stroke-width="4"/>
  ${TXT(200, y0 + 460, 26, 'HOMBRO', '#5fd0ff')}${TXT(330, y0 + 460, 26, 'MUÑECA', '#ff4a5a')}${TXT(860, y0 + 460, 26, 'VELOCIDAD', '#7b8ab8')}
  <path class="cs" d="${gauss(base, sP, 250, 62)}" fill="none" stroke="#5fd0ff" stroke-width="8" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" filter="url(#glowB)"/>
  <path class="cw" d="${gauss(base, wP, 300, 62)}" fill="none" stroke="#ff4a5a" stroke-width="8" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" filter="url(#glowB)"/>`;
}
M += `<g id="s10" opacity="0"><rect width="1080" height="1920" fill="#070b18"/><rect width="1080" height="1920" fill="url(#grid)" opacity=".6"/>
  <g id="s10a">${graph(330, 'CINTURÓN NEGRO', '#ffd23f', 640, 640)}</g><g id="s10b">${graph(900, 'GENTE DEL GYM', '#e8eef8', 500, 790)}</g>
  ${pg('s10ok', 640, 380, `<line x1="640" y1="390" x2="640" y2="740" stroke="#22d36a" stroke-width="5" stroke-dasharray="14 10"/><rect x="470" y="352" width="340" height="56" rx="12" fill="#0a2a16" stroke="#22d36a" stroke-width="4"/>${TXT(640, 394, 36, 'SINCRONIZADOS ✔', '#22d36a')}`)}
  ${pg('s10no', 645, 960, `<line x1="500" y1="980" x2="500" y2="1310" stroke="#ff4a5a" stroke-width="5" stroke-dasharray="14 10"/><line x1="790" y1="980" x2="790" y2="1310" stroke="#ff4a5a" stroke-width="5" stroke-dasharray="14 10"/><rect x="475" y="922" width="340" height="56" rx="12" fill="#2a0a0e" stroke="#ff4a5a" stroke-width="4"/>${TXT(645, 964, 36, 'DESFASADOS ✘', '#ff4a5a')}`)}
</g>`;
// 11 · cerebelo
const BRAIN = 'M230,860 C190,690 320,530 470,555 C545,460 715,470 775,555 C905,560 955,710 900,820 C925,905 850,985 760,965 C700,1025 600,1015 560,970 C475,1015 350,1000 310,945 C245,945 220,905 230,860 Z';
const GYRI = ['M330,700 C380,660 430,720 480,680', 'M520,600 C560,640 610,590 650,630', 'M700,620 C740,680 800,640 830,700', 'M300,820 C360,780 400,850 460,810', 'M500,740 C540,700 600,760 640,720', 'M680,760 C720,800 780,760 840,800', 'M380,900 C430,860 480,930 540,890', 'M600,860 C640,900 690,860 720,900'];
const CBX = 735, CBY = 1010;
const WIRES = [[CBX, CBY, 420, 690], [CBX, CBY, 580, 620], [CBX, CBY, 780, 650], [CBX, CBY, 360, 860], [CBX, CBY, 560, 800], [CBX, CBY, 850, 790]];
M += `<g id="s11" opacity="0"><rect width="1080" height="1920" fill="#070816"/><rect width="1080" height="1920" fill="url(#grid)" opacity=".5"/>
  <g id="s11br" filter="url(#glowB)"><path d="${BRAIN}" fill="#0f1b3a" stroke="#6fb8ff" stroke-width="7"/>${GYRI.map(d => `<path d="${d}" fill="none" stroke="#6fb8ff" stroke-width="5" opacity=".75" stroke-linecap="round"/>`).join('')}
    <path d="M610,975 C620,1050 600,1110 585,1170" fill="none" stroke="#6fb8ff" stroke-width="22" stroke-linecap="round" opacity=".7"/></g>
  <g id="s11w" opacity="0">${WIRES.map(([a, b, c, d]) => `<path class="wr" d="M${a},${b} Q${(a + c) / 2 + 60},${(b + d) / 2 + 40} ${c},${d}" fill="none" stroke="#ffd23f" stroke-width="5" stroke-dasharray="16 14" stroke-linecap="round" filter="url(#glowB)"/>`).join('')}</g>
  ${pg('s11cb', CBX, CBY, `<ellipse cx="${CBX}" cy="${CBY}" rx="170" ry="110" fill="url(#yelGlow)"/><ellipse cx="${CBX}" cy="${CBY}" rx="112" ry="62" fill="#f2c94c" stroke="#7a5a00" stroke-width="5"/>${[-30, -10, 10, 30].map(o => `<path d="M${CBX - 95},${CBY + o} Q${CBX},${CBY + o - 18} ${CBX + 95},${CBY + o}" fill="none" stroke="#a07a10" stroke-width="4"/>`).join('')}`)}
  ${pg('s11lb', 560, 1230, `<line x1="${CBX - 60}" y1="${CBY + 55}" x2="470" y2="1200" stroke="#ffd23f" stroke-width="5"/><rect x="250" y="1196" width="440" height="76" rx="14" fill="#1a1406" stroke="#ffd23f" stroke-width="5"/>${TXT(470, 1250, 46, 'CEREBELO', '#ffd23f')}`)}
</g>`;
// 12-14 · peleador de MMA con sensores
const SENS = [[156, 262], [244, 262], [132, 300], [268, 300], [176, 360], [224, 360]].map(([a, b]) => lp(BX, BG, BS, a, b));
const sensM = SENS.map(([x, y], i) => pg('sn' + i, x, y, `<circle cx="${x}" cy="${y}" r="26" fill="#36d3e6" opacity=".35"/><rect x="${x - 13}" y="${y - 13}" width="26" height="26" rx="5" fill="#e9f4f7" stroke="#000" stroke-width="3"/><circle cx="${x}" cy="${y}" r="6" fill="#36d3e6"/>`)).join('');
function cage() {
  return `<rect width="1080" height="1920" fill="#101218"/><rect y="560" width="1080" height="720" fill="url(#mesh)" opacity=".35"/>
  <rect x="0" y="540" width="1080" height="22" fill="#2a2d36"/><rect x="40" y="600" width="40" height="160" rx="8" fill="#c62a33"/><rect x="1000" y="600" width="40" height="160" rx="8" fill="#c62a33"/>
  <rect y="1280" width="1080" height="640" fill="#1b1d24"/><rect y="1276" width="1080" height="8" fill="#000" opacity=".6"/>
  <polygon points="420,0 660,0 1010,1440 70,1440" fill="url(#spot)" opacity=".7"/><ellipse cx="540" cy="1440" rx="470" ry="90" fill="url(#spotFloor)"/>
  <ellipse cx="540" cy="1700" rx="420" ry="80" fill="#c62a33" opacity=".22"/>`;
}
const SIGY = 400, SIG = (() => { let d = 'M100,' + SIGY; for (let x = 104; x <= 980; x += 4) { let y = SIGY + R(-3, 3); if (Math.abs(x - 330) < 46) y = SIGY + Math.sin(x * .9) * 95 * Math.exp(-((x - 330) ** 2) / 500); if (Math.abs(x - 830) < 50) y = SIGY + Math.sin(x * .9) * 110 * Math.exp(-((x - 830) ** 2) / 600); d += ` L${x},${y.toFixed(1)}`; } return d; })();
M += `<g id="s12" opacity="0">${cage()}${fsh(BX, BG + 4, 240)}${actor('s12F', OMMA, BX, BG, BS, ['guard', 'punch'], tintCopy('s12tR', OMMA, BX, BG, BS, 'guard', '#ff2d40') + tintCopy('s12tB', OMMA, BX, BG, BS, 'guard', '#3aa8ff') + tintCopy('s12tR2', OMMA, BX, BG, BS, 'punch', '#ff2d40') + sensM)}
  ${bag('s12bag', BAGX, BAGY)}${bfx('s12fx', ...CONTACT, 440)}${sparks('s12sp', ...CONTACT, 26)}
  <g id="s12hud" opacity="0"><rect x="60" y="230" width="960" height="290" rx="18" fill="#05070d" opacity=".88" stroke="#1d4a5a" stroke-width="4"/>${TXT(190, 280, 30, 'SEÑAL MUSCULAR', '#36d3e6')}
    <clipPath id="sigClip"><rect id="sigR" x="90" y="240" width="0" height="270"/></clipPath>
    <path d="${SIG}" fill="none" stroke="#36d3e6" stroke-width="5" clip-path="url(#sigClip)" filter="url(#glowB)"/>
    ${pg('sg1', 330, 470, `<circle cx="330" cy="${SIGY}" r="40" fill="none" stroke="#fff" stroke-width="4" stroke-dasharray="8 8"/>${TXT(330, 480, 40, '1', '#fff', 'Anton')}`)}
    ${pg('sg2', 830, 470, `<circle cx="830" cy="${SIGY}" r="40" fill="none" stroke="#fff" stroke-width="4" stroke-dasharray="8 8"/>${TXT(830, 480, 40, '2', '#fff', 'Anton')}`)}
    ${pg('sgT', 330, 300, TXT(330, 315, 34, 'TENSO', '#ff4a5a'))}${pg('sgL', 580, 300, TXT(580, 315, 34, 'SUELTO', '#6fd3ff'))}${pg('sgS', 830, 300, TXT(830, 315, 34, 'APRIETA', '#ff4a5a'))}
  </g>
  ${pg('s12arr', 830, 590, `<path d="M830,610 L830,530" stroke="#ff2d40" stroke-width="10" stroke-linecap="round"/><path d="M806,552 L830,522 L854,552" fill="none" stroke="#ff2d40" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><rect x="630" y="612" width="400" height="70" rx="14" fill="#2a040b" stroke="#ff2d40" stroke-width="5"/>${TXT(830, 662, 44, 'TU BLACK FLASH', '#ff4a5a')}`)}
</g>`;
// 15-17 · los 3 pasos
const FOOT = lp(BX, BG, BS, 160, 610), HIP = lp(BX, BG, BS, 200, 440);
M += gymScene('s15', { extra:
  pg('s15ft', FOOT[0], FOOT[1], `<path d="M${FOOT[0] - 110},${FOOT[1] + 50} Q${FOOT[0] - 20},${FOOT[1] + 90} ${FOOT[0] + 80},${FOOT[1] + 40}" fill="none" stroke="#ffd23f" stroke-width="12" stroke-linecap="round"/><path d="M${FOOT[0] + 50},${FOOT[1] + 22} L${FOOT[0] + 86},${FOOT[1] + 38} L${FOOT[0] + 60},${FOOT[1] + 70}" fill="none" stroke="#ffd23f" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>`) +
  `<g id="s15hip" opacity="0"><path d="M${HIP[0] - 150},${HIP[1]} A150,46 0 1,0 ${HIP[0] + 150},${HIP[1] + 2}" fill="none" stroke="#ffd23f" stroke-width="12" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" id="s15hipP"/><path d="M${HIP[0] + 128},${HIP[1] - 28} L${HIP[0] + 152},${HIP[1] + 4} L${HIP[0] + 116},${HIP[1] + 18}" fill="none" stroke="#ffd23f" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></g>` +
  pg('s15ret', BAGX + 70, CONTACT[1], `<circle cx="${BAGX + 70}" cy="${CONTACT[1]}" r="58" fill="none" stroke="#ffd23f" stroke-width="7"/><circle cx="${BAGX + 70}" cy="${CONTACT[1]}" r="10" fill="#ffd23f"/>${[0, 1, 2, 3].map(i => { const a = i * Math.PI / 2; return `<line x1="${BAGX + 70 + Math.cos(a) * 40}" y1="${CONTACT[1] + Math.sin(a) * 40}" x2="${BAGX + 70 + Math.cos(a) * 80}" y2="${CONTACT[1] + Math.sin(a) * 80}" stroke="#ffd23f" stroke-width="7"/>`; }).join('')}<rect x="${BAGX - 60}" y="${CONTACT[1] - 150}" width="260" height="56" rx="10" fill="#1a1406" stroke="#ffd23f" stroke-width="4"/>${TXT(BAGX + 70, CONTACT[1] - 110, 36, 'APUNTA AQUÍ', '#ffd23f')}`) +
  pg('s15x', CONTACT[0] + 30, CONTACT[1], `<path d="M${CONTACT[0]},${CONTACT[1] - 30} l60,60 M${CONTACT[0] + 60},${CONTACT[1] - 30} l-60,60" stroke="#ff2d40" stroke-width="14" stroke-linecap="round"/>`) });
// 18 · final en bucle
M += yujiSolo('s18');
M += `</g></g><rect id="tint" width="1080" height="1920" fill="#ff0a24" opacity="0"/><rect width="1080" height="1920" fill="url(#vig)"/><rect id="flash" width="1080" height="1920" fill="#fff" opacity="0"/>`;
root.innerHTML = M;

// =============================================================== LÍNEA DE TIEMPO
const aura = (p, t0, t1) => tl.to(`#${p} .aura`, { opacity: .45, duration: .35, yoyo: true, repeat: Math.max(1, Math.floor((t1 - t0) / .35) - 1), ease: 'sine.inOut' }, t0);
function breathe(id, t0, t1, a = 6) { const n = Math.max(1, Math.floor((t1 - t0) / .8) - 1); tl.to(RIGS[id], { y: a, duration: .8, yoyo: true, repeat: n, ease: 'sine.inOut' }, t0); tl.to(RIGS[id], { y: 0, duration: .2 }, t1 - .2); }

// --- 1 · 0.00–4.76 · "En Jujutsu Kaisen dicen que nadie puede lanzar un Black Flash a propósito"
scene('s1', 0, 4.76);
cam(0, 540, 960, 1.0, 0); cam(0, 540, 880, 1.14, 4.7, 'sine.inOut');
title(0, 14.95);
aura('s1Y', 0, 4.7); breathe('s1Y', 0, 4.7, 5);
sfx(2.04, 'thump', .6); shake(2.04, .15, 6);
blackFlash('s1fx', 3.12, { kanji: false, shake: 10 });
const p1 = pill('¿A PROPÓSITO?', 3.66, 4.76);
popUI(addDiv('stamp', '<span>IMPOSIBLE</span>'), 4.0, 4.76, 'slam', .8); shake(4.05, .2, 12);

// --- 2/3 · 4.76–15.0 · la ciencia dice que se equivocan · el saco casi sale volando
cut(4.76); scene('s2', 4.76, 15.0);
cam(4.76, 540, 960, 1.0, 0);
pill('LA CIENCIA DICE QUE SÍ', 4.94, 9.0, 'y');
sfx(5.82, 'crack', .8); shake(5.82, .25, 14); flash(5.82, '#fff', .35, .2);
cam(6.9, 400, 720, 1.65, .45); sfx(6.9, 'swish', .45);
cam(8.3, 540, 960, 1.0, .5);
breathe('s2B', 4.76, 9.0, 5);
const CN = [[9.06, '97'], [9.6, '98'], [10.1, '99'], [10.74, '100']];
CN.forEach(([t, n], i) => {
  const d = addDiv('cnt', `<span>× ${n}</span>`);
  tl.set(d, { opacity: 1 }, t + .06); tl.set(d, { opacity: 0 }, i < 3 ? CN[i + 1][0] + .06 : 13.6);
  if (i < 3) { punch('s2B', t, .2); sfx(t + .02, 'bag', .8); bagHit('s2bag', t + .02, -7); sfx(t + .06, 'tick', .4); }
});
ft(RIGS.s2B, { r: 0 }, { r: -3, duration: .8, ease: 'sine.inOut' }, 10.74);
lab('UN GOLPE SUELTO', 10.74, 13.6, 'b');
tl.set('#s2trail', { opacity: 1 }, 10.9); ft('#s2trail', { attr: { 'stroke-dashoffset': 200 } }, { attr: { 'stroke-dashoffset': 0 }, duration: 1.2, ease: 'none' }, 10.9);
ft('#s2trailDot', { opacity: 0 }, { opacity: 1, duration: .1 }, 11.4); sfx(11.4, 'blip', .4);
tl.to(['#s2trail', '#s2trailDot'], { opacity: 0, duration: .1 }, 12.2);
cam(11.4, 600, 900, 1.2, .8, 'power1.inOut');
tl.to(RIGS.s2B, { r: 0, duration: .1 }, 12.2);
punch('s2B', 12.3, .45, 26); blackFlash('s2fx', 12.32, { sparks: 's2sp', kdur: 1.3 }); bagFly('s2bag', 12.32);
cam(12.32, 600, 900, 1.0, .35, 'power3.out');
lab('¡ESO FUE UNO!', 13.7, 15.0, 'r', 'slam');
cam(13.7, 540, 900, 1.12, 1.2, 'sine.inOut');

// --- 4/5 · 15.0–26.04 · el anime: puño + energía maldita, ×2.5, chispas negras
cut(15.0); scene('s4', 15.0, 26.04);
cam(15.0, 540, 960, 1.0, 0); cam(15.0, 540, 1000, 1.08, 5.0, 'sine.inOut');
pill('YUJI ITADORI', 15.0, 20.1, 'r');
aura('s4Y', 15.0, 21.2); breathe('s4Y', 15.0, 21.0, 5); breathe('s4C', 15.0, 21.0, 9);
tl.set('#s4hud', { opacity: 1 }, 15.2); sfx(15.2, 'blip', .5);
ft('#s4mF', { x: 0 }, { x: 726, duration: 1.68, ease: 'power1.in' }, 15.94); sfx(15.94, 'whoosh', .35);
ft('#s4mE', { x: 0 }, { x: 726, duration: 1.22, ease: 'power2.in' }, 16.4); sfx(16.4, 'shimmer', .4);
sfx(17.62, 'ding', .7); flash(17.62, '#5fd0ff', .25, .25);
ft('#s4imp', { attr: { width: 8 } }, { attr: { width: 20 }, duration: .12, yoyo: true, repeat: 1 }, 17.62);
popS('s4time', 18.66, 'tick', .8);
tl.to(['#s4hud', '#s4time'], { opacity: 0, duration: .2 }, 20.0);
sfx(20.16, 'riser', .8); cam(20.16, 560, 960, 1.28, 1.0, 'power2.in');
punch('s4Y', 21.26, 1.6, 40); blackFlash('s4fx', 21.28, { kdur: 1.25 });
cam(21.28, 560, 960, 1.0, .35, 'power3.out');
tl.to(RIGS.s4C, { x: 150, r: 14, duration: .3, ease: 'power3.out' }, 21.28); tl.to(RIGS.s4C, { x: 110, r: 4, duration: 1.2, ease: 'sine.inOut' }, 21.6);
big('×2.5', 22.56, 23.85);
sfx(23.92, 'glass', .9); shake(23.92, .3, 16);
document.querySelectorAll('#s4ck .ck').forEach(el => ft(el, { attr: { 'stroke-dashoffset': 1 } }, { attr: { 'stroke-dashoffset': 0 }, duration: .3, ease: 'power2.out' }, 23.92));
blackFlash('s4fx2', 24.94, { kanji: false, sparks: 's4sp', shake: 18 }); sfx(24.94, 'zap', .7);
tl.to('#s4ck', { opacity: 0, duration: .5 }, 25.4);

// --- 6 · 26.04–28.78 · no es más fuerza, es timing perfecto
cut(26.04); scene('s6', 26.04, 28.78);
cam(26.04, 540, 960, 1.0, 0);
popS('s6dum', 26.04, 'thud', .7); popS('s6x', 26.46, 'slam', .8); shake(26.5, .15, 8);
popS('s6clk', 26.94, 'pop', .6);
ft(RIGS.s6hand, { r: 0 }, { r: 720, duration: .85, ease: 'power2.inOut' }, 26.94);
for (let t = 26.94; t < 27.8; t += .14) sfx(t, 'tick', .5);
popS('s6ok', 27.8, 'ding', .8); cam(27.8, 790, 860, 1.25, .4);

// --- 7 · 28.78–32.0 · en la vida real pasa lo mismo
cut(28.78); scene('s7', 28.78, 32.0);
cam(28.78, 540, 960, 1.0, 0); breathe('s7B', 28.78, 32.0, 5);
pill('TU PUÑO = BLACK FLASH', 29.24, 32.0, 'r');
cam(30.16, 440, 800, 1.75, .6); sfx(30.16, 'swish', .45);
blackFlash('s7fx', 31.0, { kanji: false, shake: 8 });

// --- 8/9 · 32.0–45.1 · Imperial College: 5 cm, +50 %, mismos músculos
cut(32.0); scene('s8', 32.0, 45.1);
cam(32.0, 540, 960, 1.0, 0);
pill('IMPERIAL COLLEGE · LONDRES', 32.32, 45.1, 'y');
ft('#s8top', { opacity: 0, x: -200 }, { opacity: 1, x: 0, duration: .3, ease: 'power3.out' }, 33.34); sfx(33.34, 'whoosh', .4);
ft('#s8bot', { opacity: 0, x: -200 }, { opacity: 1, x: 0, duration: .3, ease: 'power3.out' }, 35.1); sfx(35.1, 'whoosh', .4);
breathe('s8K', 33.6, 45, 3); breathe('s8G', 35.4, 45, 3);
function jab(a, padId, ringId, t, v = 1) {
  sfx(t, 'hit', v);
  tl.to(RIGS[a], { x: 18, duration: .06, ease: 'power3.out' }, t - .04); tl.to(RIGS[a], { x: 0, duration: .22, ease: 'power1.inOut' }, t + .1);
  tl.to(RIGS[padId], { x: 10 * v, duration: .06 }, t); tl.to(RIGS[padId], { x: 0, duration: .3, ease: 'elastic.out(1,.4)' }, t + .06);
  tl.set('#' + ringId, { opacity: 1 }, t); ft(RIGS[ringId], { s: .3 }, { s: 1.4, duration: .35, ease: 'power2.out' }, t); tl.to('#' + ringId, { opacity: 0, duration: .2 }, t + .2);
}
jab('s8K', 's8p1', 's8r1', 36.72, 1); jab('s8G', 's8p2', 's8r2', 36.82, .6);
cam(37.74, 420, 560, 2.0, .45); popS('s8cm', 37.9, 'tick', .8);
cam(39.3, 540, 960, 1.0, .5);
jab('s8K', 's8p1', 's8r1', 40.5, 1); jab('s8G', 's8p2', 's8r2', 40.56, .6);
ft('#s8b1', { attr: { width: 0 } }, { attr: { width: 412 }, duration: .5, ease: 'power2.out' }, 40.5);
ft('#s8b2', { attr: { width: 0 } }, { attr: { width: 270 }, duration: .5, ease: 'power2.out' }, 40.56);
popS('s8pct', 41.06, 'slam', .8); shake(41.1, .2, 10);
popS('s8mus', 43.3, 'pop', .6); sfx(43.9, 'ding', .6);
hideS('s8pct', 43.2);

// --- 10 · 45.1–51.34 · energía maldita = timing; hombro y muñeca al mismo tiempo
cut(45.1); scene('s10', 45.1, 51.34);
cam(45.1, 540, 960, 1.0, 0);
pill('ENERGÍA MALDITA = TIMING', 45.32, 51.34, 'b');
ft('#s10a', { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: .3 }, 46.78); ft('#s10b', { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: .3 }, 46.92); sfx(46.78, 'whoosh', .35);
document.querySelectorAll('#s10 .cs').forEach(el => ft(el, { attr: { 'stroke-dashoffset': 1 } }, { attr: { 'stroke-dashoffset': 0 }, duration: .6, ease: 'power1.inOut' }, 48.14));
document.querySelectorAll('#s10 .cw').forEach(el => ft(el, { attr: { 'stroke-dashoffset': 1 } }, { attr: { 'stroke-dashoffset': 0 }, duration: .6, ease: 'power1.inOut' }, 48.68));
sfx(48.14, 'shimmer', .45); sfx(48.68, 'shimmer', .45);
popS('s10ok', 50.28, 'ding', .9); popS('s10no', 50.5, 'blip', .6);

// --- 11 · 51.34–55.18 · el cerebelo, el reloj del cerebro, cableado distinto
cut(51.34); scene('s11', 51.34, 55.18);
cam(51.34, 540, 900, 1.0, 0); cam(51.34, 600, 900, 1.15, 3.8, 'sine.inOut');
popS('s11cb', 51.64, 'glint', .8); popS('s11lb', 51.9, 'pop', .5);
tl.to(RIGS.s11cb, { s: 1.08, duration: .25, yoyo: true, repeat: 9, ease: 'sine.inOut' }, 52.2);
pill('EL RELOJ DEL CEREBRO', 52.58, 55.18, 'y');
for (let t = 52.58; t < 54.0; t += .3) sfx(t, 'tick', .55);
tl.set('#s11w', { opacity: 1 }, 54.14); sfx(54.14, 'zap', .6); sfx(54.2, 'shimmer', .5);
document.querySelectorAll('#s11w .wr').forEach(el => ft(el, { attr: { 'stroke-dashoffset': 0 } }, { attr: { 'stroke-dashoffset': -150 }, duration: 1.0, ease: 'none' }, 54.14));

// --- 12-14 · 55.18–70.7 · MMA: sensores, dos disparos, tenso / suelto / apretón
cut(55.18); scene('s12', 55.18, 70.7);
cam(55.18, 540, 960, 1.0, 0); breathe('s12F', 55.18, 62.3, 5);
cam(56.4, 380, 1000, 1.4, .5);
SENS.forEach((_, i) => popS('sn' + i, 56.6 + i * .1, 'blip', .5));
lab('PELEADORES ÉLITE DE MMA', 57.28, 62.4, 'r');
cam(59.4, 540, 960, 1.0, .5);
tl.set('#s12hud', { opacity: 1 }, 59.54); sfx(59.54, 'blip', .5);
ft('#sigR', { attr: { width: 0 } }, { attr: { width: 180 }, duration: .4, ease: 'none' }, 59.54);
popS('sg1', 61.42, 'blip', .6); popS('sg2', 61.6, 'blip', .6);
hideS('sg1', 62.4, .15); hideS('sg2', 62.4, .15);
// tenso
ft('#sigR', { attr: { width: 180 } }, { attr: { width: 340 }, duration: .45, ease: 'none' }, 62.46); popS('sgT', 62.46, 'zap', .55);
ft('#s12tR', { opacity: 0 }, { opacity: .5, duration: .15 }, 62.46); tl.to('#s12tR', { opacity: 0, duration: .2 }, 63.9);
tl.to(RIGS.s12F, { y: 10, duration: .2 }, 62.46);
lab('TENSO', 62.46, 64.0, 'r');
// suelto (viaje del golpe)
ft('#sigR', { attr: { width: 340 } }, { attr: { width: 660 }, duration: 1.6, ease: 'none' }, 64.08); popS('sgL', 64.08, 'whoosh', .4);
ft('#s12tB', { opacity: 0 }, { opacity: .45, duration: .15 }, 64.08); tl.to('#s12tB', { opacity: 0, duration: .2 }, 65.4);
tl.to(RIGS.s12F, { y: 0, x: 16, duration: 1.4, ease: 'sine.inOut' }, 64.08);
lab('SUELTO', 64.08, 65.5, 'b');
// apretón en el impacto
ft('#sigR', { attr: { width: 660 } }, { attr: { width: 900 }, duration: .5, ease: 'none' }, 65.54); popS('sgS', 66.0, 'zap', .6);
lab('APRIETA', 66.0, 67.95, 'r');
tl.to(RIGS.s12F, { x: 0, duration: .1 }, 66.8);
punch('s12F', 67.0, .4, 24); sfx(67.06, 'impact', .9); sfx(67.06, 'bag', .9); bagHit('s12bag', 67.06, -16); shake(67.06, .25, 12);
ft('#s12tR2', { opacity: 0 }, { opacity: .5, duration: .08 }, 67.0); tl.to('#s12tR2', { opacity: 0, duration: .25 }, 67.35);
// ese apretón es tu black flash
title(68.04, 70.7);
popS('s12arr', 68.22, 'pop', .6);
punch('s12F', 69.58, .5, 26); blackFlash('s12fx', 69.6, { sparks: 's12sp', kdur: 1.05 }); bagFly('s12bag', 69.6);
tl.to('#s12hud', { opacity: 0, duration: .15 }, 69.55); hideS('s12arr', 69.55, .15);

// --- 15-17 · 70.7–82.26 · los 3 pasos
cut(70.7); scene('s15', 70.7, 82.26);
cam(70.7, 540, 960, 1.0, 0); breathe('s15B', 70.7, 72.3, 5);
badge('1', 'Empuja y gira la cadera', 70.7, 74.42);
popS('s15ft', 72.1, 'pop', .6); tl.to(RIGS.s15B, { r: 2, duration: .25, ease: 'power2.out' }, 72.36); sfx(72.36, 'thump', .5);
tl.set('#s15hip', { opacity: 1 }, 72.94); ft('#s15hipP', { attr: { 'stroke-dashoffset': 1 } }, { attr: { 'stroke-dashoffset': 0 }, duration: .45, ease: 'power2.out' }, 72.94); sfx(72.94, 'swish', .7);
tl.to(RIGS.s15B, { r: -3, x: 20, duration: .4, ease: 'power2.out' }, 72.94);
lab('CADERA PRIMERO', 73.26, 74.42, 'y');
tl.to(['#s15hip', '#s15ft'], { opacity: 0, duration: .2 }, 74.2); tl.to(RIGS.s15B, { r: 0, x: 0, duration: .3 }, 74.3);
// paso 2
badge('2', 'Quédate suelto', 74.42, 77.56);
const mt = addDiv('meter', '<i>TENSIÓN</i><span class="box"><span class="fill"></span></span>');
popUI(mt, 74.6, 77.5, 'pop', .4);
const fill = mt.querySelector('.fill');
tl.to(RIGS.s15B, { x: -12, duration: .6, yoyo: true, repeat: 2, ease: 'sine.inOut' }, 74.6);
ft(fill, { width: '15%', backgroundColor: '#3aa8ff' }, { width: '100%', backgroundColor: '#ff2d40', duration: .18, ease: 'power2.out' }, 76.36);
sfx(76.36, 'zap', .6); punch('s15B', 76.5, .22); sfx(76.52, 'bag', .9); bagHit('s15bag', 76.52, -10);
// paso 3
badge('3', 'Aprieta y atraviesa', 77.56, 82.26);
popS('s15ret', 77.9, 'glint', .7);
lab('APRIETA AL CONTACTO', 78.46, 79.6, 'r');
cam(78.4, 600, 900, 1.15, .5);
punch('s15B', 78.92, .5, 28); blackFlash('s15fx', 78.94, { sparks: 's15sp', kdur: 1.1 }); bagFly('s15bag', 78.94);
cam(78.94, 540, 960, 1.0, .35, 'power3.out');
tl.to(RIGS.s15ret, { s: 1.25, duration: .2, yoyo: true, repeat: 3 }, 80.14); sfx(80.14, 'blip', .5);
lab('A TRAVÉS DEL SACO', 79.64, 82.26, 'y');
hideS('s15ret', 81.1, .15); popS('s15x', 81.22, 'blip', .6); hideS('s15x', 82.1, .1);

// --- 18 · 82.26–85.6 · "...y la próxima vez que alguien te diga que esto es solo anime…" (vuelve al inicio)
cut(82.26); scene('s18', 82.26, END + 1);
cam(82.26, 540, 880, 1.14, 0); cam(82.3, 540, 960, 1.0, END - 82.4, 'sine.inOut');
aura('s18Y', 82.26, END); breathe('s18Y', 82.26, END, 5);
title(82.26, END + 1, true);
pill('¿SOLO ANIME?', 84.58, 85.45, 'r');
sfx(84.84, 'zap', .5);

// =============================================================== SUBTÍTULOS
(function subs() {
  const RED = /^(black|flash|impacto|aprieta|apretón|golpe|chispas|maldita|energía|chocar|arrancas|cadena|equivocan|nadie|tensos|disparan)$/i;
  const YEL = /^(2\.5|50%|5|1|2|3|millonésima|timing|perfecto|cerebelo|reloj|dos|veces|mma|londres|cinturones|negros|hombro|muñeca|cadera|primero|ciencia|propósito|karate|sensores|centímetros)$/i;
  const BLU = /^(sueltos|suelto|sin|esforzarte|quédate|viaje|anime|tú|real)$/i;
  const W = window.WORDS, chunks = []; let cur = [];
  W.forEach((w, i) => {
    cur.push(w); const nx = W[i + 1];
    const pair = nx && /^black$/i.test(w.w) && /^flash/i.test(nx.w);
    if (!nx || (!pair && (cur.length >= 3 || /[,.?!]$/.test(w.w) || nx.s - w.e > .35))) { chunks.push(cur); cur = []; }
  });
  const shd = strokeShadow(7);
  chunks.forEach((c, k) => {
    const t0 = c[0].s, nx = chunks[k + 1], t1 = Math.min(nx ? nx[0].s : END, c[c.length - 1].e + .45);
    const d = addDiv('sub', c.map(w => `<span>${w.w.replace(/[,.]$/, '')}</span>`).join(' '), `text-shadow:${shd}`);
    ft(d, { opacity: 1, scale: .82, y: 14 }, { scale: 1, y: 0, duration: .1, ease: 'back.out(3)' }, t0);
    tl.set(d, { opacity: 0 }, t1);
    const sp = d.querySelectorAll('span');
    c.forEach((w, i) => {
      const k2 = w.w.replace(/[¿?,.!]/g, '').replace(/\.$/, '');
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
