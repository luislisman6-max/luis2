// Motor común de la serie «¿Y si nacieras como Arthur Morgan?» (9:16, 1080x1920, 30 fps)
// Cada parte (render_pN.js) llama a init(), define cues y escenas con los helpers globales y llama a run().
const { createCanvas, loadImage, GlobalFonts } = require('@napi-rs/canvas');
const fs = require('fs'), path = require('path');
GlobalFonts.registerFromPath(path.join(__dirname, 'fonts/Anton.ttf'), 'Anton');
GlobalFonts.registerFromPath(path.join(__dirname, 'fonts/BebasNeue.ttf'), 'Bebas');
const WORK = process.env.WORK;
const W = 1080, H = 1920, FPS = 30;
// ---------- utils
const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const lerp = (a, b, k) => a + (b - a) * k;
const ss = (a, b, x) => { const k = clamp((x - a) / (b - a)); return k * k * (3 - 2 * k); };
const easeOutBack = k => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(k - 1, 3) + c1 * Math.pow(k - 1, 2); };
const pop = (t, t0, d = 0.28) => t < t0 ? 0 : easeOutBack(clamp((t - t0) / d));
const fin = (t, t0, d = 0.3) => ss(t0, t0 + d, t);
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const norm = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]/g, '');

// ---------- estado de la parte
let ALL, TOK, T0, VOICE_END, END_CARD, DUR, VCUT, PART, TOTAL = 5;
const C = {}, CE = {}, CW = {};
let cursor = 0;
const SFX = [], SC = [], IMG = {};
const sfx = (t, name, g = 1) => SFX.push({ t: +t.toFixed(3), name, g });
const scene = (start, draw, o = {}) => SC.push({ start, draw, ...o });
const w = n => CW[n];
function phraseIdx(list, ph, from = 0) {
  const p = ph.split(/\s+/).map(norm).filter(Boolean);
  for (let i = from; i < list.length; i++) {
    let ok = true;
    for (let j = 0; j < p.length; j++) if (!list[i + j] || list[i + j].n !== p[j]) { ok = false; break; }
    if (ok) return [i, i + p.length - 1];
  }
  throw new Error('Frase no encontrada: ' + ph);
}
// init({part, from: 'capitulo 1 la familia', to: 'resto de tu vida', after: 100})  (after = segundo aprox. para buscar)
function init(o) {
  PART = o.part;
  ALL = JSON.parse(fs.readFileSync(path.join(WORK, 'tokens.json'), 'utf8'));
  const sIdx = ALL.findIndex(k => k.s >= (o.after || 0) - 0.5);
  const [i0] = phraseIdx(ALL, o.from, sIdx);
  const [, i1] = phraseIdx(ALL, o.to, i0);
  const prevEnd = i0 > 0 ? ALL[i0 - 1].e : 0;
  T0 = Math.max(prevEnd + 0.03, ALL[i0].s - 0.15);
  TOK = ALL.slice(i0, i1 + 1).map(k => ({ ...k, s: k.s - T0, e: k.e - T0 }));
  VOICE_END = TOK[TOK.length - 1].e;
  const nx = ALL[i1 + 1];
  VCUT = nx ? Math.min(nx.s - T0 - 0.06, VOICE_END + 0.4) : VOICE_END + 0.6;
  END_CARD = VOICE_END + 0.35; DUR = END_CARD + (o.last ? 4.0 : 3.0);
  Object.assign(global, { TOK, VOICE_END, END_CARD, DUR });
}
function cue(name, ph) { const [i, j] = phraseIdx(TOK, ph, cursor); C[name] = TOK[i].s; CE[name] = TOK[j].e; CW[name] = TOK[j].s; cursor = i; }
function cues(list) { list.forEach(([n, p]) => cue(n, p)); }
// ---------- dibujo básico
const K = '#1e130d';
function rr(x, a, b, ww, hh, r) { x.beginPath(); x.moveTo(a + r, b); x.arcTo(a + ww, b, a + ww, b + hh, r); x.arcTo(a + ww, b + hh, a, b + hh, r); x.arcTo(a, b + hh, a, b, r); x.arcTo(a, b, a + ww, b, r); x.closePath(); }
function txt(x, s, px, py, size, o = {}) {
  x.save(); x.translate(px, py); if (o.rot) x.rotate(o.rot); if (o.sc) x.scale(o.sc, o.sc);
  x.globalAlpha *= (o.alpha ?? 1);
  x.font = `${size}px ${o.font || 'Anton'}`; x.textAlign = o.align || 'center'; x.textBaseline = 'middle';
  if (o.spacing) x.letterSpacing = o.spacing + 'px';
  if (o.shadow) { x.shadowColor = 'rgba(0,0,0,.6)'; x.shadowBlur = o.shadow; x.shadowOffsetY = 4; }
  if (o.stroke) { x.lineJoin = 'round'; x.lineWidth = o.sw || 10; x.strokeStyle = o.stroke; x.strokeText(s, 0, 0); x.shadowBlur = 0; }
  x.fillStyle = o.color || '#fff'; x.fillText(s, 0, 0); x.restore();
}
function img(x, name, cx, footY, h, o = {}) {
  const im = IMG[name]; const s = h / im.height; const ww = im.width * s;
  x.save(); x.globalAlpha *= (o.alpha ?? 1);
  x.translate(cx, footY); if (o.rot) x.rotate(o.rot); if (o.flip) x.scale(-1, 1);
  if (o.sil) { // silueta: dibuja y rellena con un color
    const c = createCanvas(Math.ceil(ww), Math.ceil(h)), cx2 = c.getContext('2d');
    cx2.drawImage(im, 0, 0, ww, h); cx2.globalCompositeOperation = 'source-in'; cx2.fillStyle = o.sil; cx2.fillRect(0, 0, ww, h);
    x.drawImage(c, -ww / 2, -h);
  } else x.drawImage(im, -ww / 2, -h, ww, h);
  x.restore();
}
// recorte (crop en coordenadas del SVG original = px/3)
function crop(x, name, sx, sy, sw, sh, dx, dy, dw, dh, o = {}) {
  x.save(); x.globalAlpha *= (o.alpha ?? 1); if (o.filter) x.filter = o.filter;
  x.drawImage(IMG[name], sx * 3, sy * 3, sw * 3, sh * 3, dx, dy, dw, dh); x.restore();
}
function shadowEllipse(x, cx, cy, rx) { x.save(); x.fillStyle = 'rgba(0,0,0,.28)'; x.beginPath(); x.ellipse(cx, cy, rx, rx * 0.14, 0, 0, 7); x.fill(); x.restore(); }

// etiqueta blanca con flecha (como el video de referencia)
function label(x, t, t0, s, px, py, o = {}) {
  const k = pop(t, t0); if (k <= 0) return;
  x.save(); x.translate(px, py); x.scale(k, k);
  x.font = `${o.size || 46}px Anton`; const tw = x.measureText(s).width; const ww = tw + 50, hh = (o.size || 46) + 34;
  x.rotate(o.rot || -0.03);
  x.fillStyle = 'rgba(0,0,0,.35)'; rr(x, -ww / 2 + 6, -hh / 2 + 8, ww, hh, 14); x.fill();
  x.fillStyle = '#fbf6ea'; x.strokeStyle = K; x.lineWidth = 5; rr(x, -ww / 2, -hh / 2, ww, hh, 14); x.fill(); x.stroke();
  txt(x, s, 0, 2, o.size || 46, { color: K });
  if (o.sub) txt(x, o.sub, 0, hh / 2 + 22, 30, { color: '#fbf6ea', font: 'Bebas', stroke: K, sw: 6, spacing: 2 });
  x.restore();
  if (o.to) { // flecha curva dibujándose
    const a = fin(t, t0 + 0.1, 0.3); if (a <= 0) return;
    const [tx, ty] = o.to; const sx = px + (tx > px ? 1 : -1) * 40, sy = py + 40;
    const mx = (sx + tx) / 2 + (o.bend || 60), my = (sy + ty) / 2;
    x.save(); x.strokeStyle = '#fbf6ea'; x.lineWidth = 7; x.lineCap = 'round';
    x.shadowColor = 'rgba(0,0,0,.5)'; x.shadowBlur = 6;
    x.beginPath(); const N = 24;
    for (let i = 0; i <= N * a; i++) { const u = i / N; const bx = (1 - u) * (1 - u) * sx + 2 * (1 - u) * u * mx + u * u * tx, by = (1 - u) * (1 - u) * sy + 2 * (1 - u) * u * my + u * u * ty; i ? x.lineTo(bx, by) : x.moveTo(bx, by); }
    x.stroke();
    if (a >= 1) { const ang = Math.atan2(ty - my, tx - mx); x.beginPath(); x.moveTo(tx, ty); x.lineTo(tx - 26 * Math.cos(ang - .5), ty - 26 * Math.sin(ang - .5)); x.moveTo(tx, ty); x.lineTo(tx - 26 * Math.cos(ang + .5), ty - 26 * Math.sin(ang + .5)); x.stroke(); }
    x.restore();
  }
}
// sello que cae de golpe
function stamp(x, t, t0, s, px, py, o = {}) {
  if (t < t0) return; const k = clamp((t - t0) / 0.16); const sc = lerp(2.6, 1, k * k);
  x.save(); x.translate(px, py); x.rotate(o.rot ?? -0.12); x.scale(sc, sc); x.globalAlpha *= lerp(0, 0.95, k);
  const size = o.size || 70; x.font = `${size}px Anton`; const tw = x.measureText(s).width;
  x.strokeStyle = o.color || '#c8202a'; x.lineWidth = 8; rr(x, -tw / 2 - 26, -size / 2 - 16, tw + 52, size + 32, 10); x.stroke();
  txt(x, s, 0, 3, size, { color: o.color || '#c8202a' });
  x.restore();
}
function redX(x, t, t0, cx, cy, r) {
  const a = fin(t, t0, 0.12), b = fin(t, t0 + 0.08, 0.12); if (a <= 0) return;
  x.save(); x.strokeStyle = '#e0242f'; x.lineWidth = r * 0.22; x.lineCap = 'round'; x.shadowColor = 'rgba(0,0,0,.5)'; x.shadowBlur = 10;
  x.beginPath(); x.moveTo(cx - r, cy - r); x.lineTo(cx - r + 2 * r * a, cy - r + 2 * r * a); x.stroke();
  if (b > 0) { x.beginPath(); x.moveTo(cx + r, cy - r); x.lineTo(cx + r - 2 * r * b, cy - r + 2 * r * b); x.stroke(); }
  x.restore();
}
function embers(x, t, n = 40, col = '255,210,140') {
  const R = rng(3);
  for (let i = 0; i < n; i++) {
    const bx = R() * W, sp = 20 + R() * 40, ph = R() * 100, sz = 2 + R() * 4;
    const y = H - ((t * sp + ph * 20) % (H + 100)); const xx = bx + Math.sin(t * 0.8 + ph) * 30;
    x.fillStyle = `rgba(${col},${0.25 + 0.5 * Math.abs(Math.sin(t * 2 + ph))})`; x.beginPath(); x.arc(xx, y, sz, 0, 7); x.fill();
  }
}

// ---------- fondos
function sunset(x, t, o = {}) {
  const g = x.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, o.top || '#3c2452'); g.addColorStop(0.38, '#a8445a'); g.addColorStop(0.58, '#e3763f'); g.addColorStop(0.72, '#f6b25a');
  x.fillStyle = g; x.fillRect(0, 0, W, H);
  const sy = o.sunY ?? 1080, sx = o.sunX ?? 540;
  x.save(); x.globalAlpha = 0.18; x.translate(sx, sy); x.rotate(t * 0.03);
  for (let i = 0; i < 12; i++) { x.rotate(Math.PI / 6); x.fillStyle = '#fff2c4'; x.beginPath(); x.moveTo(0, 0); x.lineTo(-60, -1600); x.lineTo(60, -1600); x.fill(); }
  x.restore();
  const sg = x.createRadialGradient(sx, sy, 40, sx, sy, 380); sg.addColorStop(0, 'rgba(255,246,210,1)'); sg.addColorStop(0.3, 'rgba(255,226,150,.7)'); sg.addColorStop(1, 'rgba(255,200,120,0)');
  x.fillStyle = sg; x.fillRect(0, 0, W, H);
  x.fillStyle = '#fff4d2'; x.beginPath(); x.arc(sx, sy, 120, 0, 7); x.fill();
  // montañas
  x.strokeStyle = K; x.lineWidth = 4;
  x.fillStyle = '#8e4757'; x.beginPath(); x.moveTo(0, 1180); [[120, 1030], [230, 1090], [380, 940], [520, 1080], [640, 1010], [780, 1100], [900, 960], [1080, 1090]].forEach(p => x.lineTo(...p)); x.lineTo(1080, 1400); x.lineTo(0, 1400); x.closePath(); x.fill(); x.stroke();
  x.fillStyle = '#f3d6d0'; [[380, 940, 34], [900, 960, 30]].forEach(([a, b, r]) => { x.beginPath(); x.moveTo(a, b); x.lineTo(a - r, b + r * 1.3); x.lineTo(a - r * .3, b + r); x.lineTo(a + r * .2, b + r * 1.4); x.lineTo(a + r, b + r * 1.2); x.closePath(); x.fill(); });
  x.fillStyle = '#6e3036'; x.beginPath(); x.moveTo(0, 1250); x.quadraticCurveTo(540, 1200, 1080, 1240); x.lineTo(1080, H); x.lineTo(0, H); x.closePath(); x.fill(); x.stroke();
  x.fillStyle = '#542328'; x.fillRect(0, 1420, W, H - 1420);
  const R = rng(9); x.strokeStyle = '#8a4a3a'; x.lineWidth = 3;
  for (let i = 0; i < 26; i++) { const gx = R() * W, gy = 1280 + R() * 600; for (let k = -2; k <= 2; k++) { x.beginPath(); x.moveTo(gx + k * 6, gy); x.lineTo(gx + k * 12, gy - 20 - R() * 14); x.stroke(); } }
  embers(x, t, 30);
}
function night(x, t, o = {}) {
  const g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#070b1e'); g.addColorStop(0.6, '#16264a'); g.addColorStop(1, '#0b1226');
  x.fillStyle = g; x.fillRect(0, 0, W, H);
  const R = rng(5); for (let i = 0; i < 90; i++) { const a = 0.3 + 0.6 * Math.abs(Math.sin(t * 1.5 + i)); x.fillStyle = `rgba(255,255,255,${a})`; x.beginPath(); x.arc(R() * W, R() * 1100, R() * 2.4 + .5, 0, 7); x.fill(); }
  const mx = o.moonX ?? 760, my = o.moonY ?? 420;
  const mg = x.createRadialGradient(mx, my, 60, mx, my, 360); mg.addColorStop(0, 'rgba(220,230,255,.45)'); mg.addColorStop(1, 'rgba(220,230,255,0)'); x.fillStyle = mg; x.fillRect(0, 0, W, H);
  x.fillStyle = '#f1f0e4'; x.beginPath(); x.arc(mx, my, 90, 0, 7); x.fill();
  x.fillStyle = '#dcdacb'; [[-30, -20, 16], [26, 18, 12], [10, -40, 8]].forEach(([a, b, r]) => { x.beginPath(); x.arc(mx + a, my + b, r, 0, 7); x.fill(); });
  if (o.mountains !== false) {
    x.fillStyle = '#1b2545'; x.strokeStyle = '#0a0f20'; x.lineWidth = 4;
    x.beginPath(); x.moveTo(0, 1250); [[160, 1080], [300, 1170], [480, 1000], [660, 1160], [820, 1040], [1080, 1180]].forEach(p => x.lineTo(...p)); x.lineTo(1080, H); x.lineTo(0, H); x.closePath(); x.fill(); x.stroke();
    x.fillStyle = '#10182f'; x.fillRect(0, 1400, W, H - 1400);
  }
}
function woodWall(x, tone = 1) {
  x.fillStyle = `rgb(${Math.round(120 * tone)},${Math.round(70 * tone)},${Math.round(38 * tone)})`; x.fillRect(0, 0, W, H);
  for (let y = 0, i = 0; y < H; y += 92, i++) {
    x.fillStyle = i % 2 ? 'rgba(0,0,0,.08)' : 'rgba(255,200,150,.04)'; x.fillRect(0, y, W, 92);
    x.fillStyle = 'rgba(30,15,8,.75)'; x.fillRect(0, y, W, 5);
    const R = rng(i + 1); x.strokeStyle = 'rgba(40,20,10,.25)'; x.lineWidth = 2;
    for (let k = 0; k < 3; k++) { const a = R() * W; x.beginPath(); x.moveTo(a, y + 20 + R() * 50); x.lineTo(a + 120 + R() * 200, y + 25 + R() * 50); x.stroke(); }
  }
  const vg = x.createRadialGradient(W / 2, H * .42, 100, W / 2, H * .45, 1100); vg.addColorStop(0, 'rgba(255,190,110,.22)'); vg.addColorStop(1, 'rgba(0,0,0,.5)');
  x.fillStyle = vg; x.fillRect(0, 0, W, H);
}
function cabin(x, t, o = {}) {
  woodWall(x, o.dark ? 0.55 : 1);
  // ventana de noche con cortinas
  x.save(); x.translate(760, 360);
  x.fillStyle = '#1e2c55'; x.strokeStyle = K; x.lineWidth = 8; x.fillRect(-120, -110, 240, 220); x.strokeRect(-120, -110, 240, 220);
  x.fillStyle = '#f1f0e4'; x.beginPath(); x.arc(50, -50, 26, 0, 7); x.fill();
  x.beginPath(); x.moveTo(0, -110); x.lineTo(0, 110); x.moveTo(-120, 0); x.lineTo(120, 0); x.stroke();
  x.fillStyle = '#b8323b'; [[-150, -1], [150, 1]].forEach(([a, s]) => { x.beginPath(); x.moveTo(a - 30 * s, -130); x.lineTo(a + 40 * s, -130); x.quadraticCurveTo(a + 10 * s, 0, a + 30 * s, 130); x.lineTo(a - 30 * s, 130); x.closePath(); x.fill(); x.stroke(); });
  x.restore();
  // chimenea de piedra con fuego
  x.save(); x.translate(170, 980);
  x.fillStyle = '#7a7470'; x.strokeStyle = K; x.lineWidth = 5; x.fillRect(-170, -560, 300, 560); x.strokeRect(-170, -560, 300, 560);
  const R = rng(2); for (let r = 0; r < 14; r++) for (let c = 0; c < 4; c++) { x.fillStyle = R() > .5 ? '#8e8883' : '#6c6662'; rr(x, -165 + c * 74 + (r % 2) * 30, -555 + r * 40, 66, 34, 10); x.fill(); x.stroke(); }
  x.fillStyle = '#1a0f0a'; x.beginPath(); x.moveTo(-110, 0); x.lineTo(-110, -190); x.quadraticCurveTo(-10, -260, 90, -190); x.lineTo(90, 0); x.fill();
  const fl = o.fireOut ? 0 : 1;
  if (fl) for (let i = 0; i < 3; i++) {
    const fx = -60 + i * 50, fh = 120 + 30 * Math.sin(t * 9 + i * 2);
    const fg = x.createLinearGradient(0, -fh, 0, 0); fg.addColorStop(0, '#ffe27a'); fg.addColorStop(1, '#ff6a1f');
    x.fillStyle = fg; x.beginPath(); x.moveTo(fx - 34, -10); x.quadraticCurveTo(fx - 30, -fh * .6, fx + 6 * Math.sin(t * 7 + i), -fh); x.quadraticCurveTo(fx + 34, -fh * .5, fx + 34, -10); x.fill();
  }
  x.restore();
  if (fl) { const fg = x.createRadialGradient(150, 900, 20, 150, 900, 700); fg.addColorStop(0, `rgba(255,150,60,${0.28 + 0.05 * Math.sin(t * 8)})`); fg.addColorStop(1, 'rgba(255,150,60,0)'); x.fillStyle = fg; x.fillRect(0, 0, W, H); }
  // piso y alfombra
  x.fillStyle = o.dark ? '#3a2214' : '#5e3820'; x.fillRect(0, 1240, W, H - 1240);
  x.fillStyle = 'rgba(0,0,0,.25)'; for (let y = 1240; y < H; y += 70) x.fillRect(0, y, W, 4);
  x.save(); x.translate(560, 1430); x.scale(1, .28);
  ['#b8323b', '#e2b04a', '#3d6a8a', '#e9dfc9', '#b8323b'].forEach((c, i) => { x.fillStyle = c; x.strokeStyle = K; x.lineWidth = 6; x.beginPath(); x.arc(0, 0, 420 - i * 70, 0, 7); x.fill(); x.stroke(); });
  x.restore();
  if (o.dark) { x.fillStyle = 'rgba(5,8,25,.45)'; x.fillRect(0, 0, W, H); }
}
function cradle(x, cx, cy, rock) {
  x.save(); x.translate(cx, cy); x.rotate(Math.sin(rock) * 0.05);
  x.strokeStyle = K; x.lineWidth = 7;
  x.fillStyle = '#a0683a'; x.beginPath(); x.moveTo(-260, 40); x.quadraticCurveTo(0, 140, 260, 40); x.lineTo(240, 70); x.quadraticCurveTo(0, 170, -240, 70); x.closePath(); x.fill(); x.stroke();
  x.fillStyle = '#b97a44'; rr(x, -220, -150, 440, 200, 20); x.fill(); x.stroke();
  x.fillStyle = 'rgba(0,0,0,.2)'; x.fillRect(80, -146, 136, 192);
  x.fillStyle = '#e2b04a'; x.beginPath(); x.moveTo(-30, -60); x.lineTo(30, -60); x.lineTo(0, -10); x.closePath(); x.fill(); x.stroke();
  x.restore();
}
function table(x, cx, cy, ww) {
  x.fillStyle = '#6b4226'; x.strokeStyle = K; x.lineWidth = 6; rr(x, cx - ww / 2, cy, ww, 40, 8); x.fill(); x.stroke();
  x.fillRect(cx - ww / 2 + 30, cy + 40, 26, 300); x.strokeRect(cx - ww / 2 + 30, cy + 40, 26, 300);
  x.fillRect(cx + ww / 2 - 56, cy + 40, 26, 300); x.strokeRect(cx + ww / 2 - 56, cy + 40, 26, 300);
}
function candle(x, t, cx, cy, out = 0) {
  x.fillStyle = '#efe6cf'; x.strokeStyle = K; x.lineWidth = 4; rr(x, cx - 20, cy - 110, 40, 110, 6); x.fill(); x.stroke();
  x.fillStyle = '#c9b88c'; x.beginPath(); x.ellipse(cx, cy, 40, 12, 0, 0, 7); x.fill(); x.stroke();
  if (out < 1) {
    const a = 1 - out; const fh = 46 + 5 * Math.sin(t * 13);
    const gl = x.createRadialGradient(cx, cy - 140, 5, cx, cy - 140, 320); gl.addColorStop(0, `rgba(255,200,110,${.45 * a})`); gl.addColorStop(1, 'rgba(255,200,110,0)'); x.fillStyle = gl; x.fillRect(cx - 330, cy - 470, 660, 660);
    x.globalAlpha = a; x.fillStyle = '#ffd36a'; x.beginPath(); x.moveTo(cx - 12, cy - 112); x.quadraticCurveTo(cx - 14, cy - 140, cx + 2 * Math.sin(t * 9), cy - 112 - fh); x.quadraticCurveTo(cx + 16, cy - 140, cx + 12, cy - 112); x.fill(); x.globalAlpha = 1;
  } else { // humito de vela apagada
    const k = clamp(out - 1); x.strokeStyle = `rgba(200,200,200,${0.5 * (1 - k)})`; x.lineWidth = 4; x.beginPath();
    for (let i = 0; i < 20; i++) { const yy = cy - 112 - i * 9 - k * 60; x.lineTo(cx + Math.sin(i * .6 + t * 3) * 10, yy); } x.stroke();
  }
}
function paperRect(x, cx, cy, ww, hh, rot = 0, col = '#ecd9ad') {
  x.save(); x.translate(cx, cy); x.rotate(rot);
  x.fillStyle = 'rgba(0,0,0,.35)'; x.fillRect(-ww / 2 + 10, -hh / 2 + 14, ww, hh);
  x.fillStyle = col; x.strokeStyle = '#6b4a2a'; x.lineWidth = 4;
  x.beginPath(); x.moveTo(-ww / 2, -hh / 2); x.lineTo(ww / 2, -hh / 2 + 6); x.lineTo(ww / 2 - 4, hh / 2); x.lineTo(-ww / 2 + 6, hh / 2 - 4); x.closePath(); x.fill(); x.stroke();
  const g = x.createRadialGradient(0, 0, ww * .2, 0, 0, ww * .75); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(110,70,20,.35)'); x.fillStyle = g; x.fill();
  x.restore();
}
function wanted(x, t, cx, cy, sc, rot, o = {}) {
  x.save(); x.translate(cx, cy); x.rotate(rot); x.scale(sc, sc);
  paperRect(x, 0, 0, 560, 780);
  x.fillStyle = '#9a8a6a'; x.beginPath(); x.arc(0, -372, 10, 0, 7); x.fill();
  txt(x, 'SE BUSCA', 0, -300, 104, { color: '#3a2412', font: 'Anton' });
  x.fillStyle = '#d8c393'; x.strokeStyle = '#3a2412'; x.lineWidth = 5; x.fillRect(-150, -230, 300, 250); x.strokeRect(-150, -230, 300, 250);
  crop(x, o.who || 'arthur', 150, 90, 300, 260, -146, -226, 292, 242, { filter: 'sepia(1) contrast(1.1)' });
  txt(x, o.name || 'ARTHUR MORGAN', 0, 60, 54, { color: '#3a2412', font: 'Bebas', spacing: 3 });
  x.fillStyle = '#3a2412'; x.fillRect(-200, 92, 400, 4);
  if (o.lines) o.lines.forEach((l, i) => { const k = pop(t, l[1], 0.22); if (k > 0) { x.save(); x.translate(-150, 140 + i * 64); x.scale(k, k); txt(x, '●', 0, 0, 26, { color: '#b8323b' }); txt(x, l[0], 30, 2, 50, { color: '#3a2412', align: 'left', font: 'Bebas', spacing: 2 }); x.restore(); } });
  if (o.reward) txt(x, o.reward, 0, 345, 54, { color: '#b8323b', font: 'Anton' });
  x.restore();
}
function polaroid(x, cx, cy, rot, sc, draw, cap) {
  x.save(); x.translate(cx, cy); x.rotate(rot); x.scale(sc, sc);
  x.fillStyle = 'rgba(0,0,0,.4)'; x.fillRect(-190, -210, 400, 470);
  x.fillStyle = '#f4efe3'; x.strokeStyle = K; x.lineWidth = 5; x.fillRect(-200, -220, 400, 470); x.strokeRect(-200, -220, 400, 470);
  x.save(); x.beginPath(); x.rect(-170, -190, 340, 340); x.clip(); draw(x); x.restore();
  x.strokeRect(-170, -190, 340, 340);
  if (cap) txt(x, cap, 0, 200, 46, { color: K, font: 'Bebas', spacing: 3 });
  x.restore();
}
function bullet(x, cx, cy, sc, rot) {
  x.save(); x.translate(cx, cy); x.rotate(rot); x.scale(sc, sc); x.strokeStyle = K; x.lineWidth = 4;
  const g = x.createLinearGradient(-40, 0, 40, 0); g.addColorStop(0, '#8a6a2a'); g.addColorStop(.4, '#f2d27a'); g.addColorStop(1, '#8a6a2a');
  x.fillStyle = g; rr(x, -36, -40, 72, 150, 6); x.fill(); x.stroke();
  const g2 = x.createLinearGradient(-40, 0, 40, 0); g2.addColorStop(0, '#6a4a3a'); g2.addColorStop(.45, '#d8a47a'); g2.addColorStop(1, '#6a4a3a');
  x.fillStyle = g2; x.beginPath(); x.moveTo(-34, -40); x.quadraticCurveTo(-34, -130, 0, -150); x.quadraticCurveTo(34, -130, 34, -40); x.closePath(); x.fill(); x.stroke();
  x.fillStyle = '#b59544'; rr(x, -40, 100, 80, 16, 4); x.fill(); x.stroke();
  x.restore();
}
function iconHouse(x, cx, cy, s) { x.save(); x.translate(cx, cy); x.scale(s, s); x.fillStyle = '#c98a4a'; x.strokeStyle = K; x.lineWidth = 8; x.fillRect(-90, -20, 180, 140); x.strokeRect(-90, -20, 180, 140); x.fillStyle = '#8a3a2a'; x.beginPath(); x.moveTo(-120, -10); x.lineTo(0, -120); x.lineTo(120, -10); x.closePath(); x.fill(); x.stroke(); x.fillStyle = '#5a3a20'; x.fillRect(-26, 40, 52, 80); x.strokeRect(-26, 40, 52, 80); x.restore(); }
function iconFamily(x, cx, cy, s) { x.save(); x.translate(cx, cy); x.scale(s, s); x.strokeStyle = K; x.lineWidth = 7; [[-70, 0, 1, '#6f6386'], [70, 0, 1, '#5d5640'], [0, 40, .7, '#c9b38a']].forEach(([a, b, k, c]) => { x.fillStyle = c; x.beginPath(); x.ellipse(a, b + 70 * k, 52 * k, 70 * k, 0, Math.PI, 0); x.lineTo(a + 52 * k, b + 120 * k); x.lineTo(a - 52 * k, b + 120 * k); x.closePath(); x.fill(); x.stroke(); x.fillStyle = '#d9a07a'; x.beginPath(); x.arc(a, b - 20 * k, 40 * k, 0, 7); x.fill(); x.stroke(); }); x.restore(); }
function iconPockets(x, cx, cy, s) { x.save(); x.translate(cx, cy); x.scale(s, s); x.fillStyle = '#5e5040'; x.strokeStyle = K; x.lineWidth = 8; x.fillRect(-120, -60, 240, 120); x.strokeRect(-120, -60, 240, 120); x.fillStyle = '#e6dcc5'; [-1, 1].forEach(k => { x.beginPath(); x.moveTo(k * 60 - 40, 50); x.lineTo(k * 60 + 40, 50); x.lineTo(k * 60 + 30, 130); x.quadraticCurveTo(k * 60, 150, k * 60 - 30, 130); x.closePath(); x.fill(); x.stroke(); }); x.restore(); }
function bread(x, cx, cy, s, r = 0) { x.save(); x.translate(cx, cy); x.rotate(r); x.scale(s, s); x.fillStyle = '#d8964a'; x.strokeStyle = K; x.lineWidth = 7; x.beginPath(); x.ellipse(0, 0, 130, 60, 0, 0, 7); x.fill(); x.stroke(); x.strokeStyle = '#f2c57e'; x.lineWidth = 8; for (let i = -1; i <= 1; i++) { x.beginPath(); x.moveTo(i * 50 - 20, -30); x.lineTo(i * 50 + 20, 20); x.stroke(); } x.restore(); }
function coin(x, cx, cy, s, spin) { x.save(); x.translate(cx, cy); x.scale(s * Math.max(.15, Math.abs(Math.cos(spin))), s); x.fillStyle = '#e8c34a'; x.strokeStyle = K; x.lineWidth = 6; x.beginPath(); x.arc(0, 0, 50, 0, 7); x.fill(); x.stroke(); txt(x, '$', 0, 4, 60, { color: '#a8822a' }); x.restore(); }
function bottle(x, cx, cy, s, r = 0) { x.save(); x.translate(cx, cy); x.rotate(r); x.scale(s, s); x.fillStyle = '#8a5a1e'; x.strokeStyle = K; x.lineWidth = 6; x.beginPath(); x.moveTo(-40, 0); x.lineTo(-40, -150); x.quadraticCurveTo(-40, -190, -16, -200); x.lineTo(-16, -250); x.lineTo(16, -250); x.lineTo(16, -200); x.quadraticCurveTo(40, -190, 40, -150); x.lineTo(40, 0); x.closePath(); x.fill(); x.stroke(); x.fillStyle = '#efe2c0'; x.fillRect(-36, -120, 72, 70); x.strokeRect(-36, -120, 72, 70); txt(x, 'XXX', 0, -84, 34, { color: '#5a2a10' }); x.fillStyle = 'rgba(255,255,255,.35)'; x.fillRect(-28, -190, 10, 60); x.restore(); }
function heart(x, cx, cy, s, a = 1) { x.save(); x.translate(cx, cy); x.scale(s, s); x.globalAlpha *= a; x.fillStyle = '#e8485a'; x.strokeStyle = K; x.lineWidth = 6; x.beginPath(); x.moveTo(0, 30); x.bezierCurveTo(-60, -10, -40, -60, 0, -30); x.bezierCurveTo(40, -60, 60, -10, 0, 30); x.fill(); x.stroke(); x.restore(); }
function smoke(x, t, cx, cy, s, a = 1) { for (let i = 0; i < 4; i++) { const k = ((t * .4 + i * .25) % 1); x.fillStyle = `rgba(200,200,200,${a * .35 * (1 - k)})`; x.beginPath(); x.arc(cx + Math.sin(k * 6 + i) * 30 * s, cy - k * 260 * s, (30 + k * 60) * s, 0, 7); x.fill(); } }
function chapterCard(x, t, t0, small, big) {
  x.fillStyle = '#0b0807'; x.fillRect(0, 0, W, H);
  const k = fin(t, t0, 0.5);
  x.save(); x.globalAlpha = k;
  x.strokeStyle = '#d1a646'; x.lineWidth = 4; x.beginPath(); x.arc(540, 820, 34, 0, 7); x.stroke();
  for (let i = 0; i < 6; i++) { const a = i * Math.PI / 3 + t * .3; x.beginPath(); x.arc(540 + 18 * Math.cos(a), 820 + 18 * Math.sin(a), 7, 0, 7); x.stroke(); }
  txt(x, small, 540, 910, 44, { color: '#d1a646', font: 'Bebas', spacing: 10 });
  txt(x, big, 540, 1010, 110, { color: '#f4ead2', font: 'Bebas', spacing: 4, sc: lerp(1.08, 1, k) });
  x.restore();
}


// ---------- cierre «CONTINUARÁ» (o final de la serie)
function endCard(last) {
  scene(END_CARD, (x, t) => {
    x.fillStyle = '#0b0807'; x.fillRect(0, 0, W, H);
    const a = pop(t, END_CARD + 0.1, 0.4), b = pop(t, END_CARD + 0.7, 0.35);
    if (last) {
      if (a > 0) txt(x, 'FIN', 540, 800, 200 * a, { color: '#f4ead2', font: 'Bebas', spacing: 20 });
      if (b > 0) txt(x, '¿DE QUIÉN QUIERES LA PRÓXIMA VIDA?', 540, 1000, 58 * b, { color: '#d1a646', font: 'Bebas', spacing: 3 });
      if (b > 0) txt(x, 'COMÉNTALO Y SÍGUEME', 540, 1090, 64, { color: '#fff', font: 'Anton', alpha: fin(t, END_CARD + 1.2, 0.4) });
      return;
    }
    if (a > 0) txt(x, 'CONTINUARÁ…', 540, 820, 130 * a, { color: '#f4ead2', font: 'Bebas', spacing: 8 });
    if (b > 0) { x.save(); x.translate(540, 1010); x.scale(b, b); x.fillStyle = '#c8202a'; x.strokeStyle = K; x.lineWidth = 6; rr(x, -300, -70, 600, 140, 24); x.fill(); x.stroke(); txt(x, 'PARTE ' + (PART + 1), -40, 4, 90, { color: '#fff' }); x.fillStyle = '#fff'; x.beginPath(); x.moveTo(150, -36); x.lineTo(214, 0); x.lineTo(150, 36); x.closePath(); x.fill(); x.restore(); }
    if (b > 0) txt(x, 'SÍGUEME PARA NO PERDÉRTELA', 540, 1160, 52, { color: '#d1a646', font: 'Bebas', spacing: 4, alpha: fin(t, END_CARD + 1.0, 0.4) });
  }, { nosubs: true });
  sfx(END_CARD + 0.1, last ? 'bell' : 'boom', 0.6); sfx(END_CARD + 0.7, 'pop', 0.9);
}
// ---------- subtítulos (Anton, palabra activa en amarillo, zona baja-media que no tapa la acción)
const GROUPS = [];
function buildGroups() {
  let g = null;
  for (let i = 0; i < TOK.length; i++) {
    const k = TOK[i]; if (!g) g = { w: [], s: k.s }; g.w.push(i);
    const chars = g.w.reduce((a, j) => a + TOK[j].t.length + 1, 0);
    const nx = TOK[i + 1]; const endP = /[.,?!:;…]$/.test(k.t); const gap = nx ? nx.s - k.e : 9;
    if (g.w.length >= 3 || chars > 15 || endP || gap > 0.3 || !nx) { g.e = k.e; GROUPS.push(g); g = null; }
  }
  GROUPS.forEach((g, i) => { const nx = GROUPS[i + 1]; g.end = nx ? Math.min(nx.s, g.e + 0.4) : g.e + 0.6; });
}
const SUB_Y = 1450;
function drawSubs(x, t) {
  const g = GROUPS.find(g => t >= g.s && t < g.end); if (!g) return;
  const size = 92; x.save(); x.font = `${size}px Anton`;
  const parts = g.w.map(j => ({ s: TOK[j].t.toUpperCase().replace(/[.,;:…]+$/, ''), j }));
  const sp = 22; const widths = parts.map(p => x.measureText(p.s).width);
  let total = widths.reduce((a, b) => a + b, 0) + sp * (parts.length - 1);
  const maxW = 960, sc = Math.min(1, maxW / total);
  const k = easeOutBack(clamp((t - g.s) / 0.12));
  x.translate(W / 2, SUB_Y); x.scale(sc * (0.88 + 0.12 * k), sc * (0.88 + 0.12 * k));
  let px = -total / 2;
  parts.forEach((p, i) => {
    const tk = TOK[p.j]; const nxt = g.w.includes(p.j + 1) ? TOK[p.j + 1].s : g.end;
    const active = t >= tk.s && t < nxt;
    x.save(); x.translate(px + widths[i] / 2, 0);
    if (active) { const a = easeOutBack(clamp((t - tk.s) / 0.1)); x.scale(1 + 0.1 * a, 1 + 0.1 * a); }
    x.lineJoin = 'round'; x.lineWidth = 16; x.strokeStyle = '#000'; x.shadowColor = 'rgba(0,0,0,.85)'; x.shadowBlur = 18; x.shadowOffsetY = 6;
    x.textAlign = 'center'; x.textBaseline = 'middle'; x.strokeText(p.s, 0, 0);
    x.shadowBlur = 0; x.shadowOffsetY = 0; x.fillStyle = active ? '#ffd23f' : '#ffffff'; x.fillText(p.s, 0, 0);
    x.restore(); px += widths[i] + sp;
  });
  x.restore();
}

// ---------- render
let canvas, ctx;
const sceneAt = t => { let s = SC[0]; for (const c of SC) if (t >= c.start) s = c; return s; };
const PR = rng(77); const GRAIN = Array.from({ length: 900 }, () => [PR() * W, PR() * H, PR()]);
function renderFrame(t) {
  const sc = sceneAt(t);
  ctx.save();
  const since = t - sc.start; const hit = 0.07 * Math.exp(-since * 9);
  const z = 1 + hit + 0.012 * since;
  let sx = 0, sy = 0; if (sc.shake) { const s0 = sc.shake(); if (t > s0 && t < s0 + 0.45) { const a = 22 * (1 - (t - s0) / 0.45); sx = Math.sin(t * 90) * a; sy = Math.cos(t * 77) * a; } }
  ctx.translate(W / 2 + sx, H / 2 + sy); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
  sc.draw(ctx, t); ctx.restore();
  ctx.save(); GRAIN.forEach(([gx, gy, r], i) => { const v = (Math.sin(t * 40 + i) + 1) / 2; ctx.fillStyle = `rgba(255,255,255,${0.035 * v})`; ctx.fillRect((gx + t * 300 * r) % W, (gy + t * 170) % H, 2, 2); }); ctx.restore();
  const vg = ctx.createRadialGradient(W / 2, H / 2, H * 0.32, W / 2, H / 2, H * 0.72); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,.5)'); ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
  if (t < END_CARD) { ctx.save(); ctx.globalAlpha = 0.9; ctx.fillStyle = 'rgba(10,6,4,.55)'; rr(ctx, 44, 160, 230, 58, 29); ctx.fill(); txt(ctx, `PARTE ${PART} / ${TOTAL}`, 159, 191, 36, { color: '#f4ead2', font: 'Bebas', spacing: 4 }); ctx.restore(); }
  if (!sc.nosubs) drawSubs(ctx, t);
  const fade = Math.min(ss(0, 0.25, t), 1 - ss(DUR - 0.5, DUR, t)); if (fade < 1) { ctx.fillStyle = `rgba(0,0,0,${1 - fade})`; ctx.fillRect(0, 0, W, H); }
}
async function run(names) {
  SC.sort((a, b) => a.start - b.start);
  SC.slice(1).forEach(s => { if (!SFX.some(e => Math.abs(e.t - s.start) < 0.12 && /whoosh|boom|stinger/.test(e.name))) sfx(s.start, 'whoosh', 0.45); });
  buildGroups();
  canvas = createCanvas(W, H); ctx = canvas.getContext('2d');
  for (const n of names) IMG[n] = await loadImage(path.join(__dirname, 'assets', n + '.png'));
  const mode = process.argv[2];
  if (mode === 'meta') {
    fs.writeFileSync(path.join(WORK, 'sfx.json'), JSON.stringify({ dur: DUR, events: SFX.filter(e => e.g > 0 && e.t >= 0).sort((a, b) => a.t - b.t) }, null, 1));
    console.log('DUR', DUR.toFixed(2), 'frames', Math.ceil(DUR * FPS), 'sfx', SFX.length, 'scenes', SC.length);
    console.log('VCUT', VCUT.toFixed(3)); console.log('VSTART', T0.toFixed(3));
    Object.entries(C).forEach(([k, v]) => console.log(k.padEnd(12), v.toFixed(2), CW[k].toFixed(2)));
  } else if (mode === 'still') {
    for (const ts of process.argv.slice(3)) { renderFrame(+ts); fs.writeFileSync(path.join(WORK, `still_${ts}.png`), canvas.toBuffer('image/png')); }
  } else if (mode === 'frames') {
    const a = +process.argv[3], b = Math.min(+process.argv[4], Math.ceil(DUR * FPS));
    for (let f = a; f < b; f++) {
      renderFrame(f / FPS); const buf = ctx.getImageData(0, 0, W, H).data;
      if (!process.stdout.write(Buffer.from(buf.buffer, buf.byteOffset, buf.byteLength))) await new Promise(r => process.stdout.once('drain', r));
    }
  }
}

Object.assign(global, { createCanvas, W, H, FPS, clamp, lerp, ss, easeOutBack, pop, fin, rng, norm, C, CE, CW, sfx, scene, w, init, cue, cues, run, endCard, SC, SFX, IMG,
  K, rr, txt, img, crop, shadowEllipse, label, stamp, redX, embers, sunset, night, woodWall, cabin, cradle, table, candle, paperRect, wanted, polaroid,
  bullet, iconHouse, iconFamily, iconPockets, bread, coin, bottle, heart, smoke, chapterCard });
