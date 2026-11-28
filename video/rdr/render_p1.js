// ¿Y si nacieras como Arthur Morgan? — PARTE 1 (9:16, 1080x1920, 30 fps)
// Uso: node render_p1.js meta | still <t...> | frames <a> <b>
const { createCanvas, loadImage, GlobalFonts } = require('@napi-rs/canvas');
const fs = require('fs'), path = require('path');
GlobalFonts.registerFromPath(path.join(__dirname, 'fonts/Anton.ttf'), 'Anton');
GlobalFonts.registerFromPath(path.join(__dirname, 'fonts/BebasNeue.ttf'), 'Bebas');

const WORK = process.env.WORK;
const W = 1080, H = 1920, FPS = 30;
const ALL = JSON.parse(fs.readFileSync(path.join(WORK, 'tokens.json'), 'utf8'));
const PART_END_WORD = 'equivocadas';
const iEnd = ALL.findIndex(k => k.n === PART_END_WORD);
const TOK = ALL.slice(0, iEnd + 1);
const VOICE_END = TOK[TOK.length - 1].e;
const END_CARD = VOICE_END + 0.35;
const DUR = END_CARD + 3.0;

// ---------- utils
const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const lerp = (a, b, k) => a + (b - a) * k;
const ss = (a, b, x) => { const k = clamp((x - a) / (b - a)); return k * k * (3 - 2 * k); };
const easeOutBack = k => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(k - 1, 3) + c1 * Math.pow(k - 1, 2); };
const pop = (t, t0, d = 0.28) => t < t0 ? 0 : easeOutBack(clamp((t - t0) / d));
const fin = (t, t0, d = 0.3) => ss(t0, t0 + d, t);
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const norm = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]/g, '');

// ---------- cues (frase → tiempo exacto de la palabra)
let cursor = 0;
function findPhrase(ph) {
  const p = ph.split(/\s+/).map(norm).filter(Boolean);
  for (let i = cursor; i < TOK.length; i++) {
    let ok = true;
    for (let j = 0; j < p.length; j++) if (!TOK[i + j] || TOK[i + j].n !== p[j]) { ok = false; break; }
    if (ok) return [i, i + p.length - 1];
  }
  throw new Error('Cue no encontrado: ' + ph);
}
const C = {}, CE = {}, CW = {};   // inicio frase, fin frase, inicio de la ÚLTIMA palabra
function cue(name, ph) { const [i, j] = findPhrase(ph); C[name] = TOK[i].s; CE[name] = TOK[j].e; CW[name] = TOK[j].s; cursor = i; }
[
  ['buscado', 'el hombre mas buscado'], ['s2', 'vas a robar trenes'], ['bancos', 'vas a robar bancos'], ['pais', 'medio pais'],
  ['rastro', 'rastro'], ['s3', 'vas a cabalgar'], ['america', 'america'], ['matar1', 'vas a matar'], ['dosveces', 'dos veces'],
  ['s4', 'pero lo que'], ['matarAti', 'matar a ti'], ['bala', 'no sera una bala'],
  ['s5', 'esta es tu historia'], ['primer', 'el primer dia'], ['ultimo', 'hasta el ultimo'],
  ['s6', 'prologo'], ['s7', 'naces'], ['y1863', '1863'], ['cabana', 'cabana de madera'], ['humo', 'humo'],
  ['tierra', 'tierra mojada'], ['whisky', 'whisky barato'],
  ['s8', 'esa mujer'], ['mama', 'tu mama'], ['beatrice', 'se llama beatrice'], ['dulce', 'es dulce'], ['paciente', 'es paciente'],
  ['unico', 'lo unico bueno'],
  ['s9', 'no te va a durar'], ['muere', 'se muere'], ['cara', 'su cara'], ['foto', 'una foto vieja'], ['quiso', 'te quiso'],
  ['s10', 'y entonces te quedas'], ['papa', 'tu papa'], ['lyle', 'lyle morgan'], ['ladron', 'ladron'], ['violento', 'violento'],
  ['borracho', 'borracho'], ['casiNada', 'casi nada'], ['terminar', 'no quieres terminar'],
  ['s11', 'un dia la ley'], ['atrapa', 'lo atrapa'], ['morir1', 'lo ves morir'],
  ['s12', 'anos despues'], ['frase', 'lo vi morir'], ['pronto', 'lo bastante pronto'],
  ['s13', 'ahora tienes'], ['y14', '14 anos'], ['casa', 'no tienes casa'], ['familia', 'no tienes familia'], ['nada', 'no tienes nada'],
  ['s14', 'asi que haces'], ['robas', 'robas'], ['pan', 'robas pan'], ['monedas', 'robas monedas'], ['loque', 'lo que sea'],
  ['s15', 'hasta que una noche'], ['callejon', 'callejon oscuro'], ['equivocadas', 'personas equivocadas'],
].forEach(([n, p]) => cue(n, p));
const w = n => CW[n];   // momento exacto de la palabra clave

// ---------- SFX (cada animación registra su sonido en el mismo instante)
const SFX = [];
const sfx = (t, name, g = 1) => SFX.push({ t: +t.toFixed(3), name, g });

// ---------- assets
const IMG = {};
const NAMES = ['arthur', 'arthur_teen', 'baby', 'beatrice', 'jinete', 'lyle'];

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

// ---------- escenas
const SC = [];
const scene = (start, draw, o = {}) => SC.push({ start, draw, ...o });

// S1 — retrato al atardecer
scene(0, (x, t) => {
  sunset(x, t, { sunY: 980 });
  const k = ss(0, 4, t);
  crop(x, 'arthur', 60, 80, 480, 700, lerp(-120, -150, k), lerp(560, 530, k), lerp(1320, 1380, k), lerp(1925, 2013, k));
  const a = pop(t, w('buscado') - 0.05, 0.35);
  if (a > 0) {
    x.save(); x.translate(540, 400); x.scale(a, a);
    txt(x, 'ARTHUR', 0, -60, 150, { color: '#fff2d2', font: 'Bebas', spacing: 14, stroke: K, sw: 12, shadow: 16 });
    txt(x, 'MORGAN', 0, 70, 110, { color: '#ffcf6a', font: 'Bebas', spacing: 26, stroke: K, sw: 10, shadow: 16 });
    x.restore();
  }
});
sfx(0.02, 'whoosh', 0.7); sfx(w('buscado') - 0.05, 'stinger', 0.8);

// S2 — cartel de SE BUSCA
scene(C.s2, (x, t) => {
  woodWall(x);
  const many = fin(t, w('rastro'), 0.6);
  if (many > 0) { const R = rng(4); for (let i = 0; i < 9; i++) { const k = pop(t, w('rastro') + i * 0.06, 0.25); if (k > 0) wanted(x, t, 120 + R() * 840, 200 + R() * 1500, .42 * k, (R() - .5) * .5, {}); } }
  const sc = lerp(1.05, 1.12, ss(C.s2, C.s3, t));
  wanted(x, t, 540, 860, sc, -0.02, { lines: [['TRENES', w('s2')], ['BANCOS', w('bancos')], ['MEDIO PAÍS', w('pais')]], reward: t >= w('rastro') ? '$' + Math.round(lerp(0, 5000, fin(t, w('rastro'), 0.6))).toLocaleString('en') : '$ ???' });
});
sfx(w('s2'), 'thunk'); sfx(w('bancos'), 'thunk'); sfx(w('pais'), 'thunk');
sfx(w('rastro'), 'paper', 0.9); sfx(w('rastro') + 0.25, 'cash', 0.6);

// S3 — jinetes al atardecer + disparo
scene(C.s3, (x, t) => {
  sunset(x, t, { sunY: 1120 });
  const R = rng(11);
  for (let i = 0; i < 7; i++) { const dx = ((t - C.s3) * 60 + i * 150) % 1300 - 160; img(x, 'jinete', dx, 1260 + (i % 2) * 20, 230 + R() * 30, {}); }
  const bob = Math.sin(t * 10) * 6;
  img(x, 'jinete', 540 + Math.sin(t) * 10, 1420 + bob, 760);
  stamp(x, t, w('america'), 'MÁS BUSCADO', 540, 520, { size: 96 });
}, { endAt: () => C.matar1 });
sfx(C.s3, 'gallop', 0.8); sfx(w('america'), 'thunk', 1.1);
// S3b — Arthur desenfunda
scene(C.matar1, (x, t) => {
  sunset(x, t, { sunY: 1000 });
  shadowEllipse(x, 540, 1600, 260);
  img(x, 'arthur', 540, 1610, 1500);
  const bang = w('matar1');
  if (t >= bang && t < bang + 0.07) { x.fillStyle = 'rgba(255,240,200,.45)'; x.fillRect(0, 0, W, H); }
  if (t >= bang && t < bang + 0.5) { const k = (t - bang) / 0.5; x.save(); x.translate(400, 900); x.fillStyle = `rgba(255,220,120,${1 - k})`; x.beginPath(); for (let i = 0; i < 10; i++) { const a = i / 10 * 7, r = (i % 2 ? 50 : 130) * (1 + k); x.lineTo(r * Math.cos(a), r * Math.sin(a)); } x.fill(); x.restore(); }
}, { shake: () => w('matar1') });
sfx(w('matar1'), 'gunshot', 1.0);

// S4a — silueta tosiendo (la verdadera amenaza)
scene(C.s4, (x, t) => {
  night(x, t, { moonX: 700, moonY: 520 });
  const cough = w('matarAti');
  const jerk = t > cough ? Math.sin((t - cough) * 30) * 10 * Math.exp(-(t - cough) * 4) : 0;
  img(x, 'arthur', 470, 1800 + jerk, 1650, { sil: '#05070f', rot: t > cough ? 0.06 : 0 });
  if (t > cough) { const R = rng(8); for (let i = 0; i < 18; i++) { const k = clamp((t - cough) * 1.6 - i * .02); if (k <= 0) continue; const a = -0.6 + R() * 0.9, sp = 160 + R() * 260; x.fillStyle = `rgba(190,20,30,${1 - k})`; x.beginPath(); x.arc(560 + Math.cos(a) * sp * k, 520 + Math.sin(a) * sp * k + 200 * k * k, 6 + R() * 8, 0, 7); x.fill(); } }
}, { endAt: () => C.bala });
sfx(w('matarAti'), 'cough', 0.9);
// S4b — la bala cae bajo el foco + X
scene(C.bala, (x, t) => {
  x.fillStyle = '#050403'; x.fillRect(0, 0, W, H);
  const sp = x.createRadialGradient(540, 1150, 30, 540, 900, 700); sp.addColorStop(0, 'rgba(255,230,170,.55)'); sp.addColorStop(1, 'rgba(255,230,170,0)');
  x.fillStyle = sp; x.beginPath(); x.moveTo(440, 0); x.lineTo(640, 0); x.lineTo(900, 1250); x.lineTo(180, 1250); x.closePath(); x.fill();
  x.fillStyle = 'rgba(255,230,170,.3)'; x.beginPath(); x.ellipse(540, 1250, 360, 60, 0, 0, 7); x.fill();
  const land = C.bala + 0.55; const k = ss(C.bala, land, t);
  const y = lerp(-200, 1150, k * k); bullet(x, 540, y, 1.6, lerp(2.5, 0, k));
  redX(x, t, w('bala') + 0.05, 540, 1060, 260);
});
sfx(C.bala + 0.55, 'clink', 0.9); sfx(w('bala') + 0.05, 'buzz', 0.7);

// S5 — el libro se abre
scene(C.s5, (x, t) => {
  woodWall(x, 0.45);
  table(x, 540, 1320, 1100);
  candle(x, t, 930, 1320);
  const o = ss(C.s5 + 0.1, C.s5 + 0.7, t);
  x.save(); x.translate(540, 1010);
  x.fillStyle = '#5a2a18'; x.strokeStyle = K; x.lineWidth = 6; rr(x, -450, -330, 900, 640, 16); x.fill(); x.stroke();
  // página izquierda
  x.fillStyle = '#f2e6c8'; rr(x, -430, -310, 420, 600, 10); x.fill(); x.stroke();
  txt(x, 'LA VIDA DE', -220, -200, 54, { color: '#5a2a18', font: 'Bebas', spacing: 6 });
  txt(x, 'ARTHUR', -220, -110, 110, { color: '#3a1a0c', font: 'Bebas', spacing: 6 });
  txt(x, 'MORGAN', -220, -10, 110, { color: '#3a1a0c', font: 'Bebas', spacing: 6 });
  x.fillStyle = '#b8323b'; x.beginPath(); x.arc(-220, 150, 40, 0, 7); x.fill(); txt(x, 'A', -220, 154, 50, { color: '#f2e6c8' });
  // página derecha
  x.fillStyle = '#f2e6c8'; rr(x, 10, -310, 420, 600, 10); x.fill(); x.stroke();
  const a1 = pop(t, w('primer')), a2 = pop(t, w('ultimo'));
  if (a1 > 0) { x.save(); x.translate(220, -130); x.scale(a1, a1); txt(x, 'PRIMER DÍA', 0, -60, 44, { color: '#5a2a18', font: 'Bebas', spacing: 4 }); txt(x, '1863', 0, 10, 110, { color: '#3a1a0c', font: 'Bebas' }); x.restore(); }
  if (a2 > 0) { x.save(); x.translate(220, 130); x.scale(a2, a2); txt(x, 'ÚLTIMO DÍA', 0, -60, 44, { color: '#5a2a18', font: 'Bebas', spacing: 4 }); txt(x, '18??', 0, 10, 110, { color: '#b8323b', font: 'Bebas' }); x.restore(); }
  // tapa que gira al abrir
  if (o < 1) { x.save(); x.scale(1 - o * 2 < 0 ? -(o * 2 - 1) : 1 - o * 2, 1); x.fillStyle = '#6a3220'; rr(x, 0, -330, 450, 640, 16); x.fill(); x.stroke(); x.strokeStyle = '#d1a646'; x.lineWidth = 4; rr(x, 40, -280, 370, 540, 10); x.stroke(); x.restore(); }
  x.restore();
});
sfx(C.s5 + 0.1, 'pageflip', 0.9); sfx(w('primer'), 'pop', 0.7); sfx(w('ultimo'), 'pop', 0.7);

// S6 — tarjeta de capítulo
scene(C.s6, (x, t) => chapterCard(x, t, C.s6, 'PRÓLOGO', 'EL NIÑO MÁS SALVAJE'), { nosubs: true });
sfx(C.s6, 'boom', 0.6);

// S7 — la cabaña, naces
scene(C.s7, (x, t) => {
  cabin(x, t);
  smoke(x, t, 160, 380, 1.4, fin(t, w('humo'), 0.4));
  table(x, 860, 1080, 300);
  const kb = pop(t, w('whisky')); if (kb > 0) bottle(x, 860, 1084, 0.9 * kb);
  const km = pop(t, w('tierra'));
  if (km > 0) { x.save(); x.translate(820, 1560); x.scale(km, km); x.fillStyle = '#3a2412'; x.strokeStyle = K; x.lineWidth = 5; x.beginPath(); x.ellipse(0, 0, 150, 40, 0, 0, 7); x.fill(); x.stroke(); x.fillStyle = 'rgba(150,180,220,.4)'; x.beginPath(); x.ellipse(-30, -6, 70, 14, 0, 0, 7); x.fill(); x.restore(); }
  cradle(x, 540, 1170, t * 2);
  img(x, 'baby', 540, 1140, 330);
  const y = pop(t, w('y1863'), 0.35);
  if (y > 0) { x.save(); x.translate(540, 430); x.scale(y, y); txt(x, '1863', 0, 0, 220, { color: '#ffe08a', font: 'Bebas', stroke: K, sw: 14, shadow: 20 }); x.restore(); }
  label(x, t, w('cabana') - 0.1, 'TÚ, 0 AÑOS', 300, 690, { to: [470, 870], bend: -80 });
  label(x, t, w('humo'), 'HUMO', 170, 230, { size: 40 });
  label(x, t, w('whisky'), 'WHISKY BARATO', 800, 760, { size: 40, to: [850, 880], bend: 40 });
});
sfx(C.s7, 'crackle', 0.35); sfx(w('y1863'), 'pop', 0.9); sfx(w('cabana') - 0.1, 'pop', 0.7); sfx(w('humo'), 'puff', 0.6);
sfx(w('tierra'), 'squish', 0.5); sfx(w('whisky'), 'clink', 0.8);

// S8 — Beatrice
scene(C.s8, (x, t) => {
  cabin(x, t);
  shadowEllipse(x, 540, 1600, 230);
  const sway = Math.sin(t * 1.6) * 0.02;
  img(x, 'beatrice', 540, 1610, 1220, { rot: sway });
  label(x, t, w('beatrice'), 'BEATRICE', 820, 560, { sub: 'TU MAMÁ', to: [660, 640], bend: 50 });
  [[w('dulce'), 300, 760], [w('paciente'), 780, 900], [w('unico'), 330, 1040]].forEach(([t0, hx, hy]) => { const k = pop(t, t0); if (k > 0) heart(x, hx, hy - (t - t0) * 20, 1.3 * k); });
  const gl = fin(t, w('unico'), 0.5); if (gl > 0) { const g = x.createRadialGradient(540, 1000, 50, 540, 1000, 700); g.addColorStop(0, `rgba(255,230,160,${.3 * gl})`); g.addColorStop(1, 'rgba(255,230,160,0)'); x.fillStyle = g; x.fillRect(0, 0, W, H); }
});
sfx(w('mama'), 'pop', 0.5); sfx(w('beatrice'), 'pop', 0.8); sfx(w('dulce'), 'sparkle', 0.5); sfx(w('paciente'), 'sparkle', 0.5); sfx(w('unico'), 'shimmer', 0.5);

// S9 — se muere: retrato que se desvanece, foto vieja
scene(C.s9, (x, t) => {
  const dark = fin(t, C.s9, 0.8);
  woodWall(x, lerp(0.8, 0.4, dark));
  table(x, 540, 1300, 900);
  const fade = fin(t, w('cara'), 1.2);
  // retrato ovalado
  x.save(); x.translate(470, 900);
  x.fillStyle = '#8a5a2a'; x.strokeStyle = K; x.lineWidth = 8; x.beginPath(); x.ellipse(0, 0, 250, 320, 0, 0, 7); x.fill(); x.stroke();
  x.fillStyle = '#efe2c0'; x.beginPath(); x.ellipse(0, 0, 210, 280, 0, 0, 7); x.fill(); x.stroke();
  x.save(); x.beginPath(); x.ellipse(0, 0, 210, 280, 0, 0, 7); x.clip();
  crop(x, 'beatrice', 120, 60, 260, 380, -210, -280, 420, 600, { alpha: 1 - fade * 0.85, filter: `sepia(.5) blur(${Math.round(fade * 14)}px)` });
  x.restore(); x.restore();
  candle(x, t, 870, 1300, fin(t, w('muere'), 0.25) * 1 + (t > w('muere') + 0.25 ? fin(t, w('muere') + 0.25, 1.2) : 0));
  const pk = pop(t, w('foto'), 0.35);
  if (pk > 0) polaroid(x, 640, 1180, 0.12, 0.95 * pk, (y) => { y.fillStyle = '#c9b48a'; y.fillRect(-170, -190, 340, 340); crop(y, 'beatrice', 90, 0, 320, 620, -150, -190, 300, 580, { filter: 'sepia(1) contrast(.9) brightness(1.05)' }); }, '');
  const hk = pop(t, w('quiso'), 0.4); if (hk > 0) heart(x, 790, 1000 - (t - w('quiso')) * 30, 1.2 * hk, 1 - fin(t, w('quiso') + 1, 0.8));
});
sfx(C.s9, 'bell', 0.6); sfx(w('muere'), 'blow', 0.7); sfx(w('cara'), 'shimmerDown', 0.4); sfx(w('foto'), 'paper', 0.8); sfx(w('quiso'), 'sparkle', 0.4);

// S10 — Lyle
scene(C.s10, (x, t) => {
  cabin(x, t, { dark: true });
  shadowEllipse(x, 520, 1640, 240);
  const sway = Math.sin(t * 2.2) * 0.035;
  x.save(); x.translate(520, 1650); x.rotate(sway); x.translate(-520, -1650);
  img(x, 'lyle', 520, 1650, 1450); x.restore();
  label(x, t, w('lyle'), 'LYLE MORGAN', 800, 400, { sub: 'TU PAPÁ', to: [610, 470], bend: -40 });
  stamp(x, t, w('ladron'), 'LADRÓN', 220, 760, { size: 64, rot: -0.15 });
  stamp(x, t, w('violento'), 'VIOLENTO', 860, 880, { size: 64, rot: 0.1 });
  stamp(x, t, w('borracho'), 'BORRACHO', 240, 1020, { size: 64, rot: -0.06 });
  if (t > w('terminar')) { x.fillStyle = `rgba(0,0,0,${.35 * fin(t, w('terminar'), .3)})`; x.fillRect(0, 0, W, H); redX(x, t, w('terminar'), 520, 900, 330); }
});
sfx(w('lyle'), 'pop', 0.8); sfx(w('ladron'), 'thunk'); sfx(w('violento'), 'thunk'); sfx(w('borracho'), 'thunk'); sfx(w('borracho') + 0.2, 'hiccup', 0.6);
sfx(w('terminar'), 'buzz', 0.7);

// S11 — la ley lo atrapa y lo ves morir
scene(C.s11, (x, t) => {
  const m = w('morir1');
  if (t < m - 0.15) {
    woodWall(x, 0.8);
    polaroid(x, 540, 900, -0.06, 1.5 * Math.min(1, pop(t, C.s11, 0.3)), (y) => { y.fillStyle = '#8a7a5a'; y.fillRect(-170, -190, 340, 340); crop(y, 'lyle', 130, 90, 340, 360, -170, -190, 340, 360, { filter: 'sepia(1)' }); for (let i = -150; i <= 150; i += 60) { y.fillStyle = 'rgba(20,20,20,.85)'; y.fillRect(i, -190, 14, 340); } }, 'CAPTURADO');
    stamp(x, t, w('atrapa'), 'LA LEY', 540, 1420, { size: 90 });
  } else {
    sunset(x, t, { sunY: 1120, top: '#2a1838' });
    x.fillStyle = 'rgba(20,10,30,.45)'; x.fillRect(0, 0, W, H);
    // horca a lo lejos (solo la estructura)
    x.fillStyle = '#120a10'; x.fillRect(560, 820, 22, 420); x.fillRect(560, 820, 240, 20); x.fillRect(760, 840, 6, 120);
    x.fillRect(460, 1160, 440, 22); x.fillRect(480, 1180, 16, 70); x.fillRect(860, 1180, 16, 70);
    x.strokeStyle = '#120a10'; x.lineWidth = 6; x.beginPath(); x.ellipse(763, 975, 18, 24, 0, 0, 7); x.stroke();
    img(x, 'arthur_teen', 260, 1780, 900, { sil: '#0d0710' });
  }
});
sfx(C.s11 + 0.05, 'camera', 0.6); sfx(w('atrapa'), 'thunk');
sfx(w('morir1') - 0.15, 'bell', 0.8); sfx(w('morir1') - 0.15, 'wind', 0.5);

// S12 — el diario (cada palabra aparece cuando se dice)
const DIARY = (() => { const i0 = TOK.findIndex(k => k.s === C.frase); return Array.from({ length: 9 }, (_, j) => TOK[i0 + j].s); })();
scene(C.s12, (x, t) => {
  woodWall(x, 0.55);
  paperRect(x, 540, 960, 900, 1100, -0.02, '#efe3c4');
  x.save(); x.translate(540, 960); x.rotate(-0.02);
  x.strokeStyle = 'rgba(90,120,160,.35)'; x.lineWidth = 3; for (let y = -400; y <= 460; y += 80) { x.beginPath(); x.moveTo(-400, y); x.lineTo(400, y); x.stroke(); }
  txt(x, 'Años después…', -380, -440, 50, { color: '#6b4a2a', font: 'Bebas', align: 'left', spacing: 3 });
  const lines = [['"LO', 'VI', 'MORIR.'], ['Y', 'NO', 'LLEGÓ'], ['LO', 'BASTANTE'], ['PRONTO."']];
  let wi = 0; const t1 = CE.pronto;
  lines.forEach((l, i) => { const vis = l.filter((_, j) => t >= DIARY[wi + j]); wi += l.length; if (vis.length) txt(x, vis.join(' '), -380, -240 + i * 150, 120, { color: '#2a1a0e', font: 'Bebas', align: 'left', spacing: 4, rot: -0.01 }); });
  if (t > t1 + 0.1) txt(x, '— A. M.', 330, 420, 64, { color: '#5a2a18', font: 'Bebas', align: 'right', alpha: fin(t, t1 + 0.1, 0.3) });
  x.restore();
});
sfx(C.frase, 'scribbleLong', 0.6);

// S13 — 14 años, sin nada
scene(C.s13, (x, t) => {
  sunset(x, t, { top: '#4a3050', sunY: 1150 });
  x.fillStyle = 'rgba(30,20,40,.25)'; x.fillRect(0, 0, W, H);
  shadowEllipse(x, 540, 1690, 200);
  img(x, 'arthur_teen', 540, 1700, 1080);
  const y = pop(t, w('y14'), 0.35);
  if (y > 0) { x.save(); x.translate(540, 420); x.scale(y, y); txt(x, 'UNOS 14 AÑOS', 0, 0, 120, { color: '#ffe08a', font: 'Bebas', stroke: K, sw: 12, spacing: 4, shadow: 16 }); x.restore(); }
  [[w('casa'), iconHouse, 200], [w('familia'), iconFamily, 540], [w('nada'), iconPockets, 880]].forEach(([t0, f, ix]) => {
    const k = pop(t, t0); if (k <= 0) return;
    x.save(); x.fillStyle = 'rgba(251,246,234,.92)'; x.strokeStyle = K; x.lineWidth = 6; x.beginPath(); x.arc(ix, 640, 130 * k, 0, 7); x.fill(); x.stroke(); x.restore();
    f(x, ix, 640, 0.8 * k); redX(x, t, t0 + 0.25, ix, 640, 95);
  });
});
sfx(w('y14'), 'pop', 0.9);
['casa', 'familia', 'nada'].forEach(n => { sfx(w(n), 'pop', 0.7); sfx(w(n) + 0.25, 'buzz', 0.45); });

// S14 — robas
scene(C.s14, (x, t) => {
  x.fillStyle = '#d9a24a'; x.fillRect(0, 0, W, H);
  // calle del pueblo
  sunset(x, t, { top: '#4a3050', sunY: 1300 });
  x.fillStyle = '#7a5232'; x.strokeStyle = K; x.lineWidth = 6;
  [[-40, 760, 360, 620, 'TIENDA'], [720, 820, 400, 560, 'BANCO']].forEach(([a, b, ww, hh, s]) => { x.fillStyle = '#8a5e3a'; x.fillRect(a, b, ww, hh); x.strokeRect(a, b, ww, hh); x.fillStyle = '#e9dfc9'; x.fillRect(a + 40, b + 40, ww - 80, 80); x.strokeRect(a + 40, b + 40, ww - 80, 80); txt(x, s, a + ww / 2, b + 82, 56, { color: '#3a2412', font: 'Bebas', spacing: 6 }); x.fillStyle = '#3a2412'; x.fillRect(a + ww / 2 - 60, b + hh - 220, 120, 220); });
  x.fillStyle = '#a77b4a'; x.fillRect(0, 1380, W, H - 1380);
  const run = Math.sin(t * 14) * 8;
  shadowEllipse(x, 540, 1690, 200);
  img(x, 'arthur_teen', 540, 1700 + Math.abs(run), 1040);
  const items = [[w('pan'), (k, tt) => bread(x, 230, lerp(900, 760, k), 1.1 * k, -0.2)],
  [w('monedas'), (k, tt) => { for (let i = 0; i < 5; i++) coin(x, 760 + i * 50, 860 - i * 40 - k * 60, 0.9 * k, tt * 8 + i); }],
  [w('loque'), (k) => { bottle(x, 220, 1400, .7 * k, -.4); x.save(); x.translate(880, 1300); x.scale(k, k); x.fillStyle = '#d8b24a'; x.strokeStyle = K; x.lineWidth = 6; x.beginPath(); x.arc(0, 0, 70, 0, 7); x.fill(); x.stroke(); x.fillStyle = '#f4efe3'; x.beginPath(); x.arc(0, 0, 52, 0, 7); x.fill(); x.stroke(); x.beginPath(); x.moveTo(0, 0); x.lineTo(0, -38); x.moveTo(0, 0); x.lineTo(26, 10); x.stroke(); x.fillStyle = '#d8b24a'; x.fillRect(-12, -96, 24, 26); x.strokeRect(-12, -96, 24, 26); x.restore(); }]];
  items.forEach(([t0, f]) => { const k = pop(t, t0); if (k > 0) f(k, t); });
  if (t >= w('robas') && t < w('robas') + 0.6) stamp(x, t, w('robas'), '¡ROBAS!', 540, 420, { size: 120, rot: -0.08 });
});
sfx(w('robas'), 'thunk', 1.0); sfx(w('pan'), 'pop', 0.8); sfx(w('monedas'), 'coins', 0.8); sfx(w('loque'), 'pop', 0.7); sfx(w('loque') + 0.15, 'clink', 0.5);

// S15 — callejón: las personas equivocadas
scene(C.s15, (x, t) => {
  night(x, t, { moonX: 540, moonY: 330, mountains: false });
  // paredes de ladrillo en perspectiva
  [[0, 1], [W, -1]].forEach(([bx, s]) => {
    x.fillStyle = '#3a2428'; x.strokeStyle = '#120a0c'; x.lineWidth = 4;
    x.beginPath(); x.moveTo(bx, 0); x.lineTo(bx + s * 360, 520); x.lineTo(bx + s * 360, 1500); x.lineTo(bx, H); x.closePath(); x.fill(); x.stroke();
    x.strokeStyle = 'rgba(0,0,0,.35)'; x.lineWidth = 3; for (let i = 1; i < 18; i++) { const y0 = i * 110, y1 = 520 + i * 55; x.beginPath(); x.moveTo(bx, y0); x.lineTo(bx + s * 360, y1); x.stroke(); }
  });
  x.fillStyle = '#1a1418'; x.beginPath(); x.moveTo(0, H); x.lineTo(360, 1500); x.lineTo(720, 1500); x.lineTo(W, H); x.closePath(); x.fill();
  // farol
  const lg = x.createRadialGradient(760, 760, 10, 760, 760, 420); lg.addColorStop(0, 'rgba(255,200,120,.5)'); lg.addColorStop(1, 'rgba(255,200,120,0)'); x.fillStyle = lg; x.fillRect(0, 0, W, H);
  x.fillStyle = '#ffd88a'; x.strokeStyle = K; x.lineWidth = 5; rr(x, 735, 720, 50, 70, 8); x.fill(); x.stroke();
  // niño que se acerca a escondidas
  const sneak = ss(C.s15, w('equivocadas'), t);
  img(x, 'arthur_teen', lerp(180, 330, sneak), 1720, 700, { sil: '#07050a' });
  // los dos hombres
  const turn = w('equivocadas');
  const k = fin(t, turn - 0.4, 0.3);
  x.save(); x.globalAlpha = k;
  img(x, 'arthur', 660, 1560, 1100, { sil: '#06040a' });
  img(x, 'lyle', 880, 1560, 1060, { sil: '#06040a', flip: true });
  x.restore();
  if (t > turn) { const e = fin(t, turn, 0.15); [[640, 600], [670, 600], [865, 610], [895, 610]].forEach(([ex, ey]) => { x.fillStyle = `rgba(255,240,180,${e})`; x.shadowColor = '#ffd36a'; x.shadowBlur = 20; x.beginPath(); x.ellipse(ex, ey, 9, 4, 0, 0, 7); x.fill(); }); x.shadowBlur = 0; }
}, { shake: () => w('equivocadas') });
sfx(C.s15, 'wind', 0.5); sfx(w('callejon'), 'steps', 0.6); sfx(w('equivocadas'), 'stinger', 1.0); sfx(w('equivocadas') + 0.05, 'gunCock', 0.7);

// S16 — CONTINUARÁ
scene(END_CARD, (x, t) => {
  x.fillStyle = '#0b0807'; x.fillRect(0, 0, W, H);
  const a = pop(t, END_CARD + 0.1, 0.4), b = pop(t, END_CARD + 0.7, 0.35);
  if (a > 0) txt(x, 'CONTINUARÁ…', 540, 820, 130 * a, { color: '#f4ead2', font: 'Bebas', spacing: 8 });
  if (b > 0) { x.save(); x.translate(540, 1010); x.scale(b, b); x.fillStyle = '#c8202a'; x.strokeStyle = K; x.lineWidth = 6; rr(x, -300, -70, 600, 140, 24); x.fill(); x.stroke(); txt(x, 'PARTE 2', -40, 4, 90, { color: '#fff' }); x.fillStyle = '#fff'; x.beginPath(); x.moveTo(150, -36); x.lineTo(214, 0); x.lineTo(150, 36); x.closePath(); x.fill(); x.restore(); }
  if (b > 0) txt(x, 'SÍGUEME PARA NO PERDÉRTELA', 540, 1160, 52, { color: '#d1a646', font: 'Bebas', spacing: 4, alpha: fin(t, END_CARD + 1.0, 0.4) });
}, { nosubs: true });
sfx(END_CARD + 0.1, 'boom', 0.6); sfx(END_CARD + 0.7, 'pop', 0.9);

SC.sort((a, b) => a.start - b.start);
// whoosh en cada corte
SC.slice(1).forEach(s => { if (!SFX.some(e => Math.abs(e.t - s.start) < 0.12 && /whoosh|boom|stinger/.test(e.name))) sfx(s.start, 'whoosh', 0.45); });

// ---------- subtítulos (Anton, palabra activa en amarillo, zona baja-media que no tapa la acción)
const GROUPS = [];
{
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
const sceneAt = t => { let s = SC[0]; for (const c of SC) if (t >= c.start) s = c; return s; };
const canvas = createCanvas(W, H), ctx = canvas.getContext('2d');
const PR = rng(77); const GRAIN = Array.from({ length: 900 }, () => [PR() * W, PR() * H, PR()]);
function renderFrame(t) {
  const sc = sceneAt(t);
  ctx.save();
  // cámara: golpe de zoom en el corte + zoom lento + temblor
  const since = t - sc.start; const hit = 0.07 * Math.exp(-since * 9);
  const z = 1 + hit + 0.012 * since;
  let sx = 0, sy = 0; if (sc.shake) { const s0 = sc.shake(); if (t > s0 && t < s0 + 0.45) { const a = 22 * (1 - (t - s0) / 0.45); sx = Math.sin(t * 90) * a; sy = Math.cos(t * 77) * a; } }
  ctx.translate(W / 2 + sx, H / 2 + sy); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
  sc.draw(ctx, t); ctx.restore();
  // grano + viñeta
  ctx.save(); GRAIN.forEach(([gx, gy, r], i) => { const v = (Math.sin(t * 40 + i) + 1) / 2; ctx.fillStyle = `rgba(255,255,255,${0.035 * v})`; ctx.fillRect((gx + t * 300 * r) % W, (gy + t * 170) % H, 2, 2); }); ctx.restore();
  const vg = ctx.createRadialGradient(W / 2, H / 2, H * 0.32, W / 2, H / 2, H * 0.72); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,.5)'); ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
  // etiqueta de parte (pequeña, arriba, no estorba)
  if (t < END_CARD) { ctx.save(); ctx.globalAlpha = 0.9; ctx.fillStyle = 'rgba(10,6,4,.55)'; rr(ctx, 44, 160, 230, 58, 29); ctx.fill(); txt(ctx, 'PARTE 1 / 5', 159, 191, 36, { color: '#f4ead2', font: 'Bebas', spacing: 4 }); ctx.restore(); }
  if (!sc.nosubs) drawSubs(ctx, t);
  const fade = Math.min(ss(0, 0.25, t), 1 - ss(DUR - 0.5, DUR, t)); if (fade < 1) { ctx.fillStyle = `rgba(0,0,0,${1 - fade})`; ctx.fillRect(0, 0, W, H); }
}

(async () => {
  for (const n of NAMES) IMG[n] = await loadImage(path.join(__dirname, 'assets', n + '.png'));
  const mode = process.argv[2];
  if (mode === 'meta') {
    fs.writeFileSync(path.join(WORK, 'sfx.json'), JSON.stringify({ dur: DUR, events: SFX.filter(e => e.g > 0).sort((a, b) => a.t - b.t) }, null, 1));
    const nx = ALL[iEnd + 1]; const VCUT = nx ? Math.min(nx.s - 0.06, VOICE_END + 0.4) : VOICE_END + 0.4;
    console.log('DUR', DUR.toFixed(2), 'frames', Math.ceil(DUR * FPS), 'sfx', SFX.length, 'scenes', SC.length);
    console.log('VCUT', VCUT.toFixed(3));
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
})();
