// Mil metros bajo el océano — render 16:9 procedural
const { createCanvas, GlobalFonts } = require('@napi-rs/canvas');
const fs = require('fs');
const path = require('path');
GlobalFonts.registerFromPath(path.join(__dirname, 'fonts/Anton.ttf'), 'Anton');
GlobalFonts.registerFromPath(path.join(__dirname, 'fonts/Fredoka.ttf'), 'Fredoka');

const W = 1920, H = 1080, FPS = 30;
const TOK = JSON.parse(fs.readFileSync(path.join(__dirname, '../work/tokens.json'), 'utf8'));
const VOICE_END = TOK[TOK.length - 1].e;
const DUR = VOICE_END + 2.0;

// ---------- utils ----------
const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const lerp = (a, b, k) => a + (b - a) * k;
const ss = (a, b, x) => { const k = clamp((x - a) / (b - a)); return k * k * (3 - 2 * k); };
const easeOutBack = k => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(k - 1, 3) + c1 * Math.pow(k - 1, 2); };
const easeOut = k => 1 - Math.pow(1 - k, 3);
function rng(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const norm = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]/g, '');
// window: in at a (dur d), out at b (dur d)
const win = (t, a, b, d = 0.25) => Math.min(ss(a, a + d, t), 1 - ss(b - d, b, t));
const fmt = n => String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, '.');

// ---------- cue lookup ----------
let cursor = 0;
function findPhrase(ph, from) {
  const p = ph.split(/\s+/).map(norm).filter(Boolean);
  for (let i = from; i < TOK.length; i++) {
    let ok = true;
    for (let j = 0; j < p.length; j++) if (!TOK[i + j] || TOK[i + j].n !== p[j]) { ok = false; break; }
    if (ok) return [i, i + p.length - 1];
  }
  throw new Error('Cue not found: ' + ph);
}
const C = {}, CE = {};
function cue(name, ph) { const [i, j] = findPhrase(ph, cursor); C[name] = TOK[i].s; CE[name] = TOK[j].e; cursor = i; }
[
  ['apagar', 'voy a apagar los focos de la cámara'], ['izq', 'fíjate a la izquierda'], ['destello', 'destello azul'],
  ['vuelta', 'da una vuelta completa'], ['desaparece', 'desaparece'], ['sol', 'la luz del sol'], ['quien', 'quién acaba'],
  ['medusa', 'una medusa'], ['atolla', 'se llama atolla'], ['onda', 'onda de luz'], ['explic', 'una de las explicaciones'],
  ['alarma', 'como una alarma'], ['imagina', 'imagina que un animal'], ['comer', 'intenta comérsela'], ['destella2', 'la medusa destella'],
  ['grande', 'mucho más grande'], ['atacando', 'la está atacando'], ['incomodo', 'un momento bastante'], ['boca', 'la boca llena'],
  ['focosOn', 'volvamos a encender'], ['seguir', 'vamos a seguir'], ['challenger', 'abismo challenger'], ['marianas', 'fosa de las marianas'],
  ['km1', 'ya llevamos un'], ['faltan10', 'todavía nos faltan casi'], ['antes', 'y antes de seguir'], ['vasito', 'vasito blanco'],
  ['espuma', 'vasos de espuma'], ['carita', 'le dibujamos una carita'], ['m2000', '2000 metros'], ['puntitos', 'puntitos blancos'],
  ['nevando', 'está nevando'], ['nieve', 'nieve marina'], ['acercate', 'acércate a uno'], ['plancton', 'restos diminutos'],
  ['particulas', 'partículas pegadas'], ['excrementos', 'excrementos'], ['yase', 'ya sé'], ['piensa', 'pero piensa'],
  ['superficie', 'cerca de la superficie'], ['organismos', 'organismos microscópicos'], ['ahoraAbajo', 'ahora mucho más abajo'],
  ['migajas', 'las migajas'], ['m4000', '4000 metros'], ['teacuerdas', 'te acuerdas del vaso'], ['buscaCarita', 'busca la carita'],
  ['cuesta', 'lo que cuesta reconocer'], ['juguete', 'cocina de juguete'], ['como', 'cómo puede encogerse'], ['material', 'mira de cerca el material'],
  ['huequitos', 'muchísimos huequitos'], ['presion', 'la presión comprime'], ['encoge', 'se encoge la pared'], ['dibujo', 'dibujo incluido'],
  ['oceanografos', 'los oceanógrafos'], ['miniatura', 'en miniatura'], ['recuerdo', 'el nuestro acaba'], ['m6000', '6000 metros'],
  ['adivinar', 'intenta adivinar'], ['mitad', 'ya pasamos la mitad'], ['zona', 'la zona más profunda'], ['gira2', 'gira la cámara'],
  ['suelo', 'ves el suelo'], ['tampoco', 'yo tampoco'], ['foco', 'el foco alcanza'], ['fondoKm', 'el fondo sigue'], ['apuesta', 'aquí viene una apuesta'],
  ['q8000', 'qué te imaginas'], ['dibujado', 'yo habría dibujado'], ['armadura', 'armadura'], ['miraEsto', 'pues mira esto'],
  ['camaraReal', 'una cámara real'], ['m8178', '8178 metros'], ['piel', 'tiene la piel'], ['cola', 'una cola'], ['pelicula', 'si lo hubieras'],
  ['nadando', 'y ahí estaba'], ['trampa', 'la trampa de mi pregunta'], ['gas', 'lo que se comprimió'], ['aguaPez', 'el cuerpo de ese pez'],
  ['aguaMenos', 'el agua se comprime'], ['adapt', 'vivir a esa presión'], ['coraza', 'pero llevar una coraza'], ['m9000', '9000 metros'],
  ['colocar', 'vamos a colocar'], ['everest', 'imagina el everest'], ['cima', 'pasaríamos junto'], ['dosKm', 'apenas algo más'],
  ['todo', 'todo lo que hemos visto'], ['faltan2', 'y ahora mismo'], ['titulo', 'qué vería una cámara'], ['m10000', '10000 metros'],
  ['durante', 'durante buena parte'], ['estaVez', 'esta vez'], ['clara', 'superficie clara'], ['aterrizar', 'aterrizar'],
  ['m10900', 'alrededor de'], ['fondo', 'hemos llegado al fondo'], ['demos', 'demos unos'], ['sedimento', 'hay sedimento'],
  ['ondulaciones', 'pequeñas ondulaciones'], ['vida', 'y si buscas vida'], ['anfipodos', 'anfípodos'], ['crustaceos', 'pequeños crustáceos'],
  ['investigadores', 'investigadores'], ['m10897', '10897 metros'], ['piensaCam', 'piensa en todo'], ['casa', 'para ese animalito'],
  ['copo', 'ahora volvamos a'], ['mota', 'allá arriba parecía'], ['comer2', 'quién se lo va'], ['km11', 'casi 11'], ['luzDia', 'parte de su comida'],
  ['duda', 'nos queda una última'], ['nosotros', 'nosotros tuvimos'], ['barco', 'cómo puede un barco'], ['oscuridad', 'en plena oscuridad'],
  ['metrosAgua', 'saber cuántos'], ['pista', 'la pista se puede'], ['proxima', 'esa será la próxima'],
].forEach(([n, p]) => cue(n, p));

// ---------- SFX events ----------
const SFX = [];
const sfx = (t, name, g = 1) => SFX.push({ t: +t.toFixed(3), name, g });

// ---------- depth timeline ----------
const DK = [[0, 1000], [C.antes, 1000], [C.m2000, 2000], [C.m4000, 4000], [C.m6000, 6000], [C.camaraReal, 6900], [C.m8178, 8178],
  [C.m9000, 9000], [C.m10000, 10000], [C.fondo, 10900], [DUR, 10900]];
function depthAt(t) {
  for (let i = 0; i < DK.length - 1; i++) if (t <= DK[i + 1][0]) return lerp(DK[i][1], DK[i + 1][1], (t - DK[i][0]) / (DK[i + 1][0] - DK[i][0]));
  return 10900;
}
const MILESTONES = [C.m2000, C.m4000, C.m6000, C.m8178, C.m9000, C.m10000, C.fondo];
MILESTONES.forEach(t => sfx(t, 'ping', 0.9));
const milestonePulse = t => { let p = 0; for (const m of MILESTONES) p = Math.max(p, t >= m ? 1 - ss(m, m + 0.8, t) : 0); return p; };
const cupScale = t => 1 - 0.6 * ss(1200, 4300, depthAt(t));

// ---------- drawing helpers ----------
function glow(x, c, b) { x.shadowColor = c; x.shadowBlur = b; }
function noGlow(x) { x.shadowBlur = 0; x.shadowColor = 'transparent'; }
function circle(x, cx, cy, r, fill) { x.beginPath(); x.arc(cx, cy, Math.max(0.01, r), 0, Math.PI * 2); x.fillStyle = fill; x.fill(); }
function text(x, s, px, py, size, color, o = {}) {
  x.save();
  x.font = `${o.weight || ''} ${size}px ${o.font || 'Anton'}`.trim();
  x.textAlign = o.align || 'center'; x.textBaseline = 'middle';
  if (o.alpha !== undefined) x.globalAlpha *= o.alpha;
  if (o.stroke) { x.lineJoin = 'round'; x.lineWidth = o.stroke; x.strokeStyle = o.strokeColor || '#000'; x.strokeText(s, px, py); }
  if (o.glow) glow(x, o.glow, o.glowBlur || 25);
  x.fillStyle = color; x.fillText(s, px, py);
  x.restore();
}
// pill label with pop-in
function label(x, t, a, b, s, px, py, o = {}) {
  if (t < a || t > b) return;
  const k = easeOutBack(clamp((t - a) / 0.35));
  const al = 1 - ss(b - 0.25, b, t);
  x.save(); x.translate(px, py); x.scale(k, k); x.globalAlpha *= al;
  const size = o.size || 42;
  x.font = `${size}px Anton`;
  const w = x.measureText(s).width + size * 1.1, h = size * 1.55;
  x.fillStyle = o.bg || 'rgba(4,18,38,0.82)';
  x.strokeStyle = o.color || '#5ff2ff'; x.lineWidth = 3;
  glow(x, o.color || '#5ff2ff', 18);
  roundRect(x, -w / 2, -h / 2, w, h, h / 2); x.fill(); x.stroke(); noGlow(x);
  text(x, s, 0, 2, size, o.textColor || '#fff');
  x.restore();
}
function roundRect(x, a, b, w, h, r) { x.beginPath(); x.moveTo(a + r, b); x.arcTo(a + w, b, a + w, b + h, r); x.arcTo(a + w, b + h, a, b + h, r); x.arcTo(a, b + h, a, b, r); x.arcTo(a, b, a + w, b, r); x.closePath(); }
function arrow(x, x1, y1, x2, y2, color, wdt = 6, p = 1) {
  const ex = lerp(x1, x2, p), ey = lerp(y1, y2, p);
  x.save(); x.strokeStyle = color; x.fillStyle = color; x.lineWidth = wdt; x.lineCap = 'round'; glow(x, color, 12);
  x.beginPath(); x.moveTo(x1, y1); x.lineTo(ex, ey); x.stroke();
  const ang = Math.atan2(y2 - y1, x2 - x1), hs = wdt * 3.2;
  x.beginPath(); x.moveTo(ex, ey); x.lineTo(ex - hs * Math.cos(ang - 0.5), ey - hs * Math.sin(ang - 0.5)); x.lineTo(ex - hs * Math.cos(ang + 0.5), ey - hs * Math.sin(ang + 0.5)); x.closePath(); x.fill();
  x.restore();
}
function ringHighlight(x, t, a, b, cx, cy, r, color = '#ffe14d') {
  if (t < a || t > b) return;
  const k = easeOutBack(clamp((t - a) / 0.35)), al = 1 - ss(b - 0.25, b, t);
  x.save(); x.globalAlpha *= al; x.strokeStyle = color; x.lineWidth = 6; x.setLineDash([18, 12]); x.lineDashOffset = -t * 40;
  glow(x, color, 16); x.beginPath(); x.arc(cx, cy, r * k, 0, Math.PI * 2); x.stroke(); x.restore();
}

// ---------- world: particles ----------
const PR = rng(7);
const PARTS = Array.from({ length: 260 }, () => ({ x: PR() * W, y: PR() * H, z: 0.25 + PR() * 1.0, ph: PR() * 6.28, sz: PR() }));
function drawOcean(x, t, o = {}) {
  const d = depthAt(t);
  const k = clamp((d - 1000) / 10000);
  const g = x.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, `rgb(${lerp(4, 1, k)},${lerp(22, 6, k)},${lerp(44, 16, k)})`);
  g.addColorStop(1, `rgb(${lerp(1, 0, k)},${lerp(8, 2, k)},${lerp(20, 8, k)})`);
  x.fillStyle = g; x.fillRect(0, 0, W, H);
  const L = o.lights === undefined ? 1 : o.lights;
  if (L > 0) {
    const rg = x.createRadialGradient(W * 0.5, H * 0.58, 50, W * 0.5, H * 0.58, 900);
    rg.addColorStop(0, `rgba(90,170,210,${0.22 * L})`); rg.addColorStop(0.5, `rgba(30,90,140,${0.10 * L})`); rg.addColorStop(1, 'rgba(0,0,0,0)');
    x.fillStyle = rg; x.fillRect(0, 0, W, H);
    // light beams
    x.save(); x.globalCompositeOperation = 'lighter';
    for (const sx of [-80, W + 80]) {
      const bg = x.createLinearGradient(sx, H, W / 2, H * 0.3);
      bg.addColorStop(0, `rgba(120,200,230,${0.10 * L})`); bg.addColorStop(1, 'rgba(120,200,230,0)');
      x.fillStyle = bg; x.beginPath(); x.moveTo(sx, H + 40); x.lineTo(W / 2 - 300, -50); x.lineTo(W / 2 + 300, -50); x.closePath(); x.fill();
    }
    x.restore();
  }
  // marine snow
  const density = o.density !== undefined ? o.density : (0.45 + 0.55 * ss(C.m2000 - 2, C.m2000 + 2, t));
  const speed = o.speed !== undefined ? o.speed : 38;
  const n = Math.floor(PARTS.length * density);
  for (let i = 0; i < n; i++) {
    const p = PARTS[i];
    const yy = ((p.y - t * speed * p.z) % (H + 40) + H + 40) % (H + 40) - 20;
    const xx = p.x + Math.sin(t * 0.6 + p.ph) * 12 * p.z;
    const dist = Math.hypot(xx - W / 2, yy - H * 0.58) / 900;
    const lit = Math.max(0.10, L * (1 - dist * 0.8));
    const r = (1 + p.sz * 2.6) * p.z;
    circle(x, xx, yy, r, `rgba(225,240,255,${clamp(lit * (0.35 + 0.6 * p.z))})`);
  }
}

// ---------- ROV + cup ----------
function drawROV(x, t, L = 1) {
  x.save();
  // frame edge bottom-left
  x.fillStyle = '#d98a1e'; x.strokeStyle = '#7a4a0c'; x.lineWidth = 4;
  x.beginPath(); x.moveTo(-20, H - 250); x.lineTo(150, H - 250); x.lineTo(330, H + 20); x.lineTo(-20, H + 20); x.closePath(); x.fill(); x.stroke();
  x.fillStyle = '#b06d12'; x.fillRect(-20, H - 262, 190, 22);
  for (let i = 0; i < 4; i++) circle(x, 20 + i * 40, H - 251, 5, '#4a2c06');
  // lamp
  const lg = x.createRadialGradient(250, H - 150, 4, 250, H - 150, 60);
  lg.addColorStop(0, `rgba(255,255,240,${0.2 + 0.8 * L})`); lg.addColorStop(1, 'rgba(255,255,220,0)');
  circle(x, 250, H - 150, 30, '#333');
  x.fillStyle = lg; x.beginPath(); x.arc(250, H - 150, 60, 0, 7); x.fill();
  x.restore();
}
// cup: bottom center at (cx,cy), height 220*s
function drawCup(x, cx, cy, s, face = 1, o = {}) {
  const h = 220 * s, wt = 170 * s, wb = 115 * s;
  x.save();
  if (o.alpha !== undefined) x.globalAlpha *= o.alpha;
  if (o.ghost) {
    x.setLineDash([14, 10]); x.strokeStyle = 'rgba(255,255,255,0.55)'; x.lineWidth = 4;
    x.beginPath(); x.moveTo(cx - wt / 2, cy - h); x.lineTo(cx + wt / 2, cy - h); x.lineTo(cx + wb / 2, cy); x.lineTo(cx - wb / 2, cy); x.closePath(); x.stroke();
    x.restore(); return;
  }
  const g = x.createLinearGradient(cx - wt / 2, 0, cx + wt / 2, 0);
  g.addColorStop(0, '#cfd8de'); g.addColorStop(0.35, '#ffffff'); g.addColorStop(1, '#b8c4cc');
  glow(x, 'rgba(160,230,255,0.6)', 20 * s + 6);
  x.fillStyle = g; x.beginPath(); x.moveTo(cx - wt / 2, cy - h); x.lineTo(cx + wt / 2, cy - h); x.lineTo(cx + wb / 2, cy); x.lineTo(cx - wb / 2, cy); x.closePath(); x.fill();
  noGlow(x);
  // foam texture
  const r = rng(3);
  for (let i = 0; i < 40; i++) { const yy = cy - r() * h, k = (cy - yy) / h, half = lerp(wb, wt, k) / 2; circle(x, cx + (r() * 2 - 1) * half * 0.9, yy, 2.2 * s + 0.4, 'rgba(150,165,175,0.35)'); }
  // rim
  x.fillStyle = '#eef3f6'; x.beginPath(); x.ellipse(cx, cy - h, wt / 2 + 6 * s, 14 * s, 0, 0, Math.PI * 2); x.fill();
  x.fillStyle = '#8da0ab'; x.beginPath(); x.ellipse(cx, cy - h, wt / 2 - 4 * s, 9 * s, 0, 0, Math.PI * 2); x.fill();
  // face
  if (face > 0) {
    x.strokeStyle = '#111'; x.fillStyle = '#111'; x.lineCap = 'round'; x.lineWidth = Math.max(1.5, 7 * s);
    const fy = cy - h * 0.55;
    if (face > 0.05) circle(x, cx - 28 * s, fy - 12 * s, 9 * s * clamp(face / 0.3), '#111');
    if (face > 0.3) circle(x, cx + 28 * s, fy - 12 * s, 9 * s * clamp((face - 0.3) / 0.3), '#111');
    if (face > 0.6) { const p = clamp((face - 0.6) / 0.4); x.beginPath(); x.arc(cx, fy + 2 * s, 34 * s, Math.PI * 0.15, Math.PI * (0.15 + 0.7 * p)); x.stroke(); }
  }
  x.restore();
}
function cupOnRov(x, t, face = 1) { const s = 0.62 * cupScale(t); drawCup(x, 95, H - 262, s, face); }

// ---------- depth gauge ----------
function drawGauge(x, t, al = 1) {
  if (al <= 0) return;
  const d = depthAt(t), top = 175, bot = 800, gx = 1825;
  x.save(); x.globalAlpha *= al;
  x.strokeStyle = 'rgba(120,230,255,0.55)'; x.lineWidth = 4; x.beginPath(); x.moveTo(gx, top); x.lineTo(gx, bot); x.stroke();
  for (let km = 0; km <= 11; km++) {
    const y = lerp(top, bot, km / 11);
    x.beginPath(); x.moveTo(gx - (km % 2 ? 8 : 16), y); x.lineTo(gx, y); x.stroke();
    if (km % 2 === 0 || km === 11) text(x, km + ' km', gx - 30, y, 22, 'rgba(180,235,255,0.75)', { align: 'right' });
  }
  const my = lerp(top, bot, d / 11000);
  // filled part
  x.strokeStyle = '#5ff2ff'; glow(x, '#5ff2ff', 14); x.lineWidth = 8; x.beginPath(); x.moveTo(gx, top); x.lineTo(gx, my); x.stroke();
  circle(x, gx, my, 13, '#ffe14d'); noGlow(x);
  // readout
  const pulse = milestonePulse(t);
  const sc = 1 + 0.25 * pulse;
  x.save(); x.translate(1760, 110); x.scale(sc, sc);
  x.fillStyle = 'rgba(3,14,30,0.85)'; x.strokeStyle = pulse > 0 ? '#ffe14d' : '#5ff2ff'; x.lineWidth = 3; glow(x, x.strokeStyle, 16 + 30 * pulse);
  roundRect(x, -135, -42, 270, 84, 18); x.fill(); x.stroke(); noGlow(x);
  text(x, fmt(Math.round(d / 10) * 10) + ' m', 0, 2, 54, pulse > 0 ? '#ffe14d' : '#ffffff', { glow: '#5ff2ff', glowBlur: 12 });
  x.restore();
  x.restore();
}

// ---------- creatures ----------
function drawAtolla(x, cx, cy, s, t, body = 1, ring = 0, ringSpeed = 1) {
  x.save(); x.translate(cx, cy); x.scale(s, s);
  const pulse = Math.sin(t * 2.2) * 0.05;
  if (body > 0) {
    x.globalAlpha = body;
    // tentacles
    x.strokeStyle = 'rgba(150,30,50,0.8)'; x.lineWidth = 4;
    for (let i = 0; i < 18; i++) {
      const a = -0.9 + 1.8 * i / 17, bx = Math.sin(a) * 150;
      x.beginPath(); x.moveTo(bx, 10); x.quadraticCurveTo(bx * 1.15 + Math.sin(t * 1.5 + i) * 10, 70, bx * 1.2 + Math.sin(t * 1.3 + i) * 18, 120); x.stroke();
    }
    // long trailing tentacle
    x.lineWidth = 5; x.beginPath(); x.moveTo(30, 10);
    for (let k = 1; k <= 12; k++) x.lineTo(30 + Math.sin(t * 1.2 + k * 0.5) * 25 * k / 12 + k * 6, 10 + k * 40);
    x.stroke();
    // bell
    const g = x.createRadialGradient(0, -40, 10, 0, -10, 190);
    g.addColorStop(0, '#d0384e'); g.addColorStop(0.6, '#7a1328'); g.addColorStop(1, '#3a0612');
    x.fillStyle = g; x.beginPath(); x.ellipse(0, 0, 175 * (1 + pulse), 95 * (1 - pulse), 0, Math.PI, 0); x.quadraticCurveTo(0, 40, -175 * (1 + pulse), 0); x.fill();
    x.strokeStyle = 'rgba(255,120,140,0.35)'; x.lineWidth = 3; x.beginPath(); x.ellipse(0, -10, 95, 50, 0, Math.PI, 0); x.stroke();
    x.globalAlpha = 1;
  }
  if (ring > 0) {
    // ring of light spinning around the bell rim
    const head = t * 5.5 * ringSpeed;
    x.globalCompositeOperation = 'lighter';
    for (let i = 0; i < 40; i++) {
      const a = (i / 40) * Math.PI * 2;
      let dd = ((head - a) % (Math.PI * 2) + Math.PI * 2) % (Math.PI * 2);
      const tr = Math.exp(-dd * 1.4);
      const px = Math.cos(a) * 180, py = Math.sin(a) * 60 + 5;
      glow(x, '#3fb8ff', 30);
      circle(x, px, py, 6 + 14 * tr, `rgba(${80 + 120 * tr},${200 + 55 * tr},255,${ring * (0.12 + 0.88 * tr)})`);
    }
    noGlow(x);
    x.globalCompositeOperation = 'source-over';
  }
  x.restore();
}
function drawFish(x, cx, cy, s, t, mouth = 0, dir = -1, o = {}) {
  x.save(); x.translate(cx, cy); x.scale(s * dir, s);
  const wig = Math.sin(t * 9) * 0.25;
  x.fillStyle = o.color || '#c79a3a';
  // tail
  x.save(); x.translate(-90, 0); x.rotate(wig); x.beginPath(); x.moveTo(0, 0); x.lineTo(-60, -45); x.lineTo(-50, 0); x.lineTo(-60, 45); x.closePath(); x.fill(); x.restore();
  // body
  x.beginPath(); x.ellipse(0, 0, 105, 55, 0, 0, Math.PI * 2); x.fill();
  x.fillStyle = 'rgba(255,255,255,0.18)'; x.beginPath(); x.ellipse(10, 18, 70, 22, 0, 0, Math.PI * 2); x.fill();
  // fin
  x.fillStyle = o.fin || '#9a6f22'; x.beginPath(); x.moveTo(-20, -50); x.lineTo(10, -85); x.lineTo(40, -48); x.fill();
  // mouth
  x.fillStyle = '#1a0d00'; x.beginPath(); x.moveTo(100, 5); x.lineTo(70, 5 - 30 * mouth); x.lineTo(70, 5 + 30 * mouth); x.closePath(); x.fill();
  // eye
  circle(x, 55, -18, 16 * (o.eyeBig || 1), '#fff'); circle(x, 60, -18, 8 * (o.eyeBig || 1), '#000');
  if (o.sweat) { x.fillStyle = '#7fd6ff'; x.beginPath(); x.moveTo(20, -75); x.quadraticCurveTo(35, -50, 20, -45); x.quadraticCurveTo(5, -50, 20, -75); x.fill(); }
  x.restore();
}
function drawBigEye(x, cx, cy, r, open) {
  if (open <= 0) return;
  x.save(); x.translate(cx, cy);
  glow(x, '#ff5a3c', 60 * open);
  x.fillStyle = `rgba(255,200,80,${open})`; x.beginPath(); x.ellipse(0, 0, r, r * 0.62 * open, 0, 0, Math.PI * 2); x.fill();
  noGlow(x);
  x.fillStyle = '#000'; x.beginPath(); x.ellipse(-r * 0.1, 0, r * 0.18, r * 0.55 * open, 0, 0, Math.PI * 2); x.fill();
  x.restore();
}
function drawSnailfish(x, cx, cy, s, t, dir = -1) {
  x.save(); x.translate(cx, cy); x.scale(s * dir, s);
  const g = x.createLinearGradient(0, -90, 0, 90); g.addColorStop(0, '#f3d6d8'); g.addColorStop(1, '#d7a9b0');
  x.fillStyle = g; glow(x, 'rgba(255,220,230,0.4)', 30);
  // tadpole: big head, tapering tail with wave
  x.beginPath(); x.moveTo(130, 0);
  x.bezierCurveTo(130, -95, 20, -100, -20, -60);
  const N = 14; const pts = [];
  for (let i = 0; i <= N; i++) { const k = i / N; const px = -20 - k * 330, w = lerp(60, 3, Math.pow(k, 0.8)), off = Math.sin(t * 6 - k * 5) * 26 * k; pts.push([px, off, w]); }
  for (const [px, off, w] of pts) x.lineTo(px, off - w);
  for (let i = pts.length - 1; i >= 0; i--) { const [px, off, w] = pts[i]; x.lineTo(px, off + w); }
  x.lineTo(-20, 60); x.bezierCurveTo(20, 100, 130, 95, 130, 0); x.closePath(); x.fill(); noGlow(x);
  // translucency stripes
  x.strokeStyle = 'rgba(255,255,255,0.35)'; x.lineWidth = 3;
  for (let i = 0; i < 6; i++) { x.beginPath(); x.moveTo(-40 - i * 40, -45 + i * 6); x.lineTo(-40 - i * 40, 45 - i * 6); x.stroke(); }
  circle(x, 85, -22, 11, '#2b1a20'); circle(x, 88, -25, 3.5, '#fff');
  x.strokeStyle = '#a07078'; x.lineWidth = 3; x.beginPath(); x.arc(105, 22, 18, 0.2, 1.2); x.stroke();
  // pectoral fin
  x.fillStyle = 'rgba(240,200,205,0.7)'; x.beginPath(); x.ellipse(30, 55, 45, 18, 0.5 + Math.sin(t * 4) * 0.2, 0, Math.PI * 2); x.fill();
  x.restore();
}
function drawAmphipod(x, cx, cy, s, t, ph = 0, dir = 1) {
  x.save(); x.translate(cx, cy); x.scale(s * dir, s);
  const bob = Math.sin(t * 8 + ph) * 2;
  x.translate(0, bob);
  x.strokeStyle = '#e9b8a8'; x.lineWidth = 2.5;
  for (let i = 0; i < 7; i++) { const lx = -45 + i * 14, k = Math.sin(t * 14 + i + ph) * 6; x.beginPath(); x.moveTo(lx, 8); x.lineTo(lx + k, 30); x.stroke(); }
  x.beginPath(); x.moveTo(52, -10); x.quadraticCurveTo(85, -40, 105 + Math.sin(t * 3 + ph) * 6, -30); x.stroke();
  x.beginPath(); x.moveTo(52, -6); x.quadraticCurveTo(90, -20, 110, -8); x.stroke();
  for (let i = 0; i < 9; i++) {
    const a = Math.PI * (1.05 - i * 0.1), px = Math.cos(a) * 55, py = -Math.sin(a) * 28 + 10;
    x.fillStyle = i % 2 ? '#f6d2c4' : '#efc0ae'; x.beginPath(); x.ellipse(px, py, 11, 16, -a + Math.PI / 2, 0, Math.PI * 2); x.fill();
  }
  circle(x, 52, -6, 4, '#222');
  x.restore();
}

// ---------- subtitles ----------
const GROUPS = [];
{
  let g = null;
  for (let i = 0; i < TOK.length; i++) {
    const k = TOK[i];
    if (!g) g = { w: [], s: k.s };
    g.w.push(i);
    const chars = g.w.reduce((a, j) => a + TOK[j].t.length + 1, 0);
    const next = TOK[i + 1];
    const endP = /[.,?!:;]$/.test(k.t);
    const gap = next ? next.s - k.e : 9;
    if (g.w.length >= 3 || chars > 17 || endP || gap > 0.3 || !next) { g.e = k.e; GROUPS.push(g); g = null; }
  }
  for (let i = 0; i < GROUPS.length; i++) { const nx = GROUPS[i + 1]; GROUPS[i].end = nx ? Math.min(nx.s, GROUPS[i].e + 0.45) : GROUPS[i].e + 0.8; }
}
function drawSubs(x, t, hidden) {
  if (hidden) return;
  const g = GROUPS.find(g => t >= g.s && t < g.end);
  if (!g) return;
  const size = 66;
  x.save();
  x.font = `${size}px Anton`;
  const parts = g.w.map(j => ({ s: TOK[j].t.toUpperCase().replace(/[.,;:]$/, ''), j }));
  const sp = 20;
  const widths = parts.map(p => x.measureText(p.s).width);
  const total = widths.reduce((a, b) => a + b, 0) + sp * (parts.length - 1);
  const k = easeOutBack(clamp((t - g.s) / 0.12));
  const cy = 985;
  x.translate(W / 2, cy); x.scale(0.85 + 0.15 * k, 0.85 + 0.15 * k);
  let px = -total / 2;
  parts.forEach((p, i) => {
    const tk = TOK[p.j];
    const active = t >= tk.s && t < (TOK[p.j + 1] && g.w.includes(p.j + 1) ? TOK[p.j + 1].s : g.end);
    const done = t >= tk.s;
    x.save();
    const cx = px + widths[i] / 2;
    x.translate(cx, 0);
    if (active) { const a = easeOutBack(clamp((t - tk.s) / 0.1)); x.scale(1 + 0.1 * a, 1 + 0.1 * a); }
    x.lineJoin = 'round'; x.lineWidth = 12; x.strokeStyle = '#000';
    x.shadowColor = 'rgba(0,0,0,0.8)'; x.shadowBlur = 14; x.shadowOffsetY = 4;
    x.textAlign = 'center'; x.textBaseline = 'middle';
    x.strokeText(p.s, 0, 0);
    x.shadowBlur = 0; x.shadowOffsetY = 0;
    x.fillStyle = active ? '#ffe14d' : (done ? '#ffffff' : 'rgba(255,255,255,0.92)');
    x.fillText(p.s, 0, 0);
    x.restore();
    px += widths[i] + sp;
  });
  x.restore();
}

// ---------- scenes ----------
const SC = [];
const scene = (start, draw, o = {}) => SC.push({ start, draw, ...o });

// A: 1000 m darkness + Atolla
scene(0, (x, t) => {
  const offT = CE.apagar - 0.15;
  let L = t < offT ? 0.55 : 0;
  if (t >= offT && t < offT + 0.3) L = (Math.floor((t - offT) * 20) % 2) ? 0.4 : 0;
  drawOcean(x, t, { lights: L, density: 0.45, speed: 10 });
  // sunlight that no longer arrives
  const sl = win(t, C.sol - 0.1, C.quien, 0.4);
  if (sl > 0) {
    x.save(); x.globalCompositeOperation = 'lighter';
    for (let i = 0; i < 6; i++) {
      const bx = 300 + i * 260 + Math.sin(t + i) * 20, len = 520 * (1 - ss(C.sol, C.sol + 1.6, t) * 0.7);
      const g = x.createLinearGradient(bx, 0, bx, len); g.addColorStop(0, `rgba(255,240,180,${0.35 * sl})`); g.addColorStop(1, 'rgba(255,240,180,0)');
      x.fillStyle = g; x.beginPath(); x.moveTo(bx - 40, 0); x.lineTo(bx + 40, 0); x.lineTo(bx + 90, len); x.lineTo(bx - 10, len); x.fill();
    }
    x.restore();
    label(x, t, C.sol, C.quien, 'LA LUZ DEL SOL NO LLEGA', W / 2, 640, { color: '#ffd36a' });
  }
  // jelly position
  const jx = lerp(470, 760, ss(C.medusa, C.medusa + 1.5, t)) - 160 * ss(C.imagina, C.imagina + 1, t) + 0;
  const jy = 470 + Math.sin(t * 0.7) * 12;
  const body = 0.05 + 0.95 * ss(C.medusa - 0.1, C.medusa + 0.5, t);
  let ring = win(t, C.destello, CE.desaparece + 0.2, 0.15);
  ring = Math.max(ring, win(t, C.onda, C.explic + 0.4, 0.2), win(t, C.destella2, C.grande + 0.8, 0.1) * 1.0);
  const spd = t > C.destella2 ? 1.8 : 1;
  drawAtolla(x, jx, jy, 0.9, t, body, ring, spd);
  if (t > C.destella2 && t < C.destella2 + 0.5) { // flash burst
    const k = (t - C.destella2) / 0.5; x.save(); x.globalCompositeOperation = 'lighter';
    const rg = x.createRadialGradient(jx, jy, 10, jx, jy, 900 * k + 50); rg.addColorStop(0, `rgba(80,190,255,${0.6 * (1 - k)})`); rg.addColorStop(1, 'rgba(0,0,0,0)');
    x.fillStyle = rg; x.fillRect(0, 0, W, H); x.restore();
  }
  ringHighlight(x, t, C.izq, C.destello + 0.2, 470, 470, 240, '#5ff2ff');
  if (t > C.quien - 0.1 && t < C.medusa + 0.2) text(x, '?', 470, 470, 220 * easeOutBack(clamp((t - C.quien + 0.1) / 0.3)), '#5ff2ff', { glow: '#5ff2ff', glowBlur: 40, alpha: 1 - ss(C.medusa - 0.1, C.medusa + 0.2, t) });
  label(x, t, C.atolla, C.explic, 'ATOLLA', jx, jy - 200, { color: '#ff6b81', size: 52 });
  // alarm
  if (t > C.alarma - 0.1 && t < C.imagina) {
    const k = (t - C.alarma) * 2.5;
    for (let i = 0; i < 3; i++) { const kk = (k + i / 3) % 1; x.save(); x.strokeStyle = `rgba(255,80,80,${(1 - kk) * 0.9})`; x.lineWidth = 6; glow(x, '#ff4040', 20); x.beginPath(); x.arc(jx, jy, 150 + kk * 260, 0, Math.PI * 2); x.stroke(); x.restore(); }
    label(x, t, C.alarma, C.imagina, '¿UNA ALARMA?', jx, jy + 270, { color: '#ff5a5a', size: 50 });
  }
  // predator fish
  if (t > C.imagina) {
    const fx = lerp(W + 200, jx + 260, easeOut(clamp((t - C.imagina) / 1.6)));
    const fy = jy + 40;
    const mouth = t > C.comer && t < C.destella2 ? 0.5 + 0.5 * Math.abs(Math.sin((t - C.comer) * 6)) : (t > C.boca ? 0.25 : 0.1);
    // spotlight on fish when big creature sees it
    if (t > C.atacando - 0.2) {
      const al = ss(C.atacando - 0.2, C.atacando + 0.3, t);
      const rg = x.createRadialGradient(fx, fy, 20, fx, fy, 260); rg.addColorStop(0, `rgba(255,240,180,${0.35 * al})`); rg.addColorStop(1, 'rgba(0,0,0,0)');
      x.fillStyle = rg; x.fillRect(0, 0, W, H);
    }
    const shake = t > C.grande && t < C.boca + 1.5 ? Math.sin(t * 60) * 3 : 0;
    drawFish(x, fx + shake, fy, 0.9, t, mouth, -1, { sweat: t > C.incomodo, eyeBig: t > C.grande ? 1.35 : 1 });
    if (t > C.boca) { // tentacle bit in mouth
      x.save(); x.strokeStyle = 'rgba(150,30,50,0.9)'; x.lineWidth = 6; x.beginPath(); x.moveTo(fx - 90, fy + 5); x.quadraticCurveTo(fx - 130, fy + 40, fx - 150, fy + 20); x.stroke(); x.restore();
    }
    drawBigEye(x, 1480, 300, 150, ss(C.grande, C.grande + 0.5, t));
    if (t > C.grande) drawBigEye(x, 1180, 250, 120, ss(C.grande + 0.15, C.grande + 0.65, t));
    label(x, t, C.boca, C.focosOn, 'MOMENTO INCÓMODO', fx, fy - 170, { color: '#ffe14d' });
  }
  drawROV(x, t, L);
  cupOnRov(x, t, 0);
}, { gauge: 1 });
sfx(CE.apagar - 0.15, 'off', 1);
sfx(C.destello, 'shimmer', 1); sfx(C.sol, 'whoosh', 0.5); sfx(C.quien, 'pop', 0.7); sfx(C.medusa, 'shimmer', 0.6); sfx(C.atolla, 'pop', 0.8);
sfx(C.onda, 'shimmer', 0.8); sfx(C.alarma, 'alarm', 0.6); sfx(C.imagina, 'whoosh', 0.7); sfx(C.comer + 0.3, 'chomp', 0.9);
sfx(C.destella2, 'shimmerBig', 1); sfx(C.grande, 'boom', 1); sfx(C.atacando, 'stinger', 0.6); sfx(C.boca, 'gulp', 0.9);

// B: lights on, route, cup
scene(C.focosOn, (x, t) => {
  const onT = C.focosOn + 0.3;
  let L = t < onT ? 0 : 1; if (t >= onT && t < onT + 0.25) L = (Math.floor((t - onT) * 24) % 2) ? 1 : 0.2;
  drawOcean(x, t, { lights: L });
  // map panel
  const mp = win(t, C.challenger - 0.3, C.km1 + 0.3, 0.35);
  if (mp > 0) {
    x.save(); x.globalAlpha = mp; x.translate(lerp(-500, 0, easeOut(mp)), 0);
    x.fillStyle = 'rgba(2,14,32,0.88)'; x.strokeStyle = '#5ff2ff'; x.lineWidth = 3; roundRect(x, 520, 170, 880, 560, 30); x.fill(); x.stroke();
    text(x, 'OCÉANO PACÍFICO', 960, 225, 40, '#7fdcff');
    // islands / trench arc
    x.strokeStyle = 'rgba(95,242,255,0.35)'; x.lineWidth = 3;
    for (let i = 0; i < 5; i++) { x.beginPath(); x.arc(1180, 380, 220 + i * 25, Math.PI * 0.55, Math.PI * 1.05); x.stroke(); }
    x.strokeStyle = '#1d6fa8'; x.lineWidth = 26; x.lineCap = 'round'; x.beginPath(); x.arc(1180, 380, 270, Math.PI * 0.56, Math.PI * 1.04); x.stroke();
    x.fillStyle = '#c9a86a'; [[900, 300], [925, 360], [940, 420], [960, 480]].forEach(([a, b]) => { x.beginPath(); x.ellipse(a, b, 14, 9, 0.6, 0, 7); x.fill(); });
    const pin = easeOutBack(clamp((t - C.challenger) / 0.4));
    const pxp = 1180 + 270 * Math.cos(Math.PI * 0.78), pyp = 380 + 270 * Math.sin(Math.PI * 0.78);
    x.save(); x.translate(pxp, pyp); x.scale(pin, pin); glow(x, '#ff4d6d', 25); circle(x, 0, -30, 22, '#ff4d6d'); x.beginPath(); x.moveTo(-14, -20); x.lineTo(0, 5); x.lineTo(14, -20); x.fill(); circle(x, 0, -30, 8, '#fff'); x.restore();
    text(x, 'ABISMO CHALLENGER', pxp + 20, pyp + 55, 34, '#fff', { alpha: pin, align: 'left' });
    if (t > C.marianas) text(x, 'FOSA DE LAS MARIANAS', 960, 680, 44, '#ffe14d', { alpha: ss(C.marianas, C.marianas + 0.3, t), glow: '#ffb000', glowBlur: 14 });
    x.restore();
  }
  label(x, t, C.km1, C.antes, '1 KM BAJADO · FALTAN ~10', W / 2, 420, { color: '#5ff2ff', size: 46 });
  // cup presentation
  const cp = win(t, C.vasito - 0.2, C.m2000 + 0.2, 0.45);
  const s = lerp(0.62, 1.7, easeOut(cp)), cx = lerp(95, 760, easeOut(cp)), cy = lerp(H - 262, 760, easeOut(cp));
  drawROV(x, t, L);
  const face = ss(C.carita + 0.2, C.carita + 1.6, t);
  if (cp > 0.01) drawCup(x, cx, cy, s, face); else cupOnRov(x, t, face);
  ringHighlight(x, t, C.vasito, C.espuma, 760, 760 - 190, 260);
  label(x, t, C.espuma, C.carita + 0.3, 'VASO DE ESPUMA · CASI NO PESA', 1180, 520, { color: '#ffffff' });
  if (t > C.carita && t < C.carita + 1.8) { // marker
    const k = clamp((t - C.carita - 0.2) / 1.4); const mx = 760 + Math.cos(k * 9) * 30, my = 760 - 220 + Math.sin(k * 7) * 20;
    x.save(); x.translate(mx + 40, my - 60); x.rotate(0.6); x.fillStyle = '#222'; x.fillRect(-10, -80, 20, 90); x.fillStyle = '#e33'; x.fillRect(-10, -95, 20, 18); x.restore();
  }
  label(x, t, C.carita + 1.4, C.m2000, '¡RECUÉRDALO!', 1120, 560, { color: '#ffe14d', size: 50 });
}, { gauge: 1 });
sfx(C.focosOn + 0.3, 'on', 1); sfx(C.challenger - 0.3, 'whoosh', 0.7); sfx(C.challenger, 'pop', 0.8); sfx(C.marianas, 'pop', 0.6);
sfx(C.km1 + 0.2, 'whoosh', 0.5); sfx(C.vasito - 0.2, 'whoosh', 0.7); sfx(C.vasito, 'pop', 0.6); sfx(C.espuma, 'pop', 0.6);
sfx(C.carita + 0.2, 'scribble', 0.9); sfx(C.carita + 1.4, 'sparkle', 0.7);

// C: 2000 m marine snow
scene(C.m2000, (x, t) => {
  const heavy = ss(C.nevando - 0.5, C.nevando + 1, t);
  drawOcean(x, t, { speed: lerp(38, 22, heavy), density: 1 });
  if (t > C.puntitos) {
    const p = [PARTS[3], PARTS[11], PARTS[25]];
    p.forEach((pp, i) => {
      const yy = ((pp.y - t * lerp(38, 22, heavy) * pp.z) % (H + 40) + H + 40) % (H + 40) - 20;
      const xx = pp.x + Math.sin(t * 0.6 + pp.ph) * 12 * pp.z;
      ringHighlight(x, t, C.puntitos + i * 0.25, C.nevando, xx, yy, 40, '#5ff2ff');
    });
  }
  if (t > C.nieve) {
    const k = easeOutBack(clamp((t - C.nieve) / 0.45));
    x.save(); x.translate(W / 2, 430); x.scale(k, k);
    text(x, 'NIEVE MARINA', 0, 0, 150, '#ffffff', { glow: '#7fe8ff', glowBlur: 40, stroke: 10, strokeColor: 'rgba(0,20,40,0.8)' });
    x.restore();
  }
  drawROV(x, t); cupOnRov(x, t);
}, { gauge: 1 });
sfx(C.puntitos, 'pop', 0.5); sfx(C.puntitos + 0.25, 'pop', 0.4); sfx(C.puntitos + 0.5, 'pop', 0.4); sfx(C.nevando, 'sparkle', 0.5); sfx(C.nieve, 'stinger', 0.8);

// D: inside a flake + sun-to-depth food chain
scene(C.acercate, (x, t) => {
  drawOcean(x, t, { speed: 15, density: 1 });
  const split = ss(C.piensa + 0.1, C.piensa + 0.8, t);
  if (split < 1) {
    x.save(); x.globalAlpha = 1 - split;
    const zk = easeOut(clamp((t - C.acercate) / 0.8)), R = 360 * zk;
    const shake = t > C.yase && t < C.yase + 0.5 ? Math.sin(t * 70) * 6 : 0;
    const cx = W / 2 - 120 + shake, cy = 470;
    x.save(); x.beginPath(); x.arc(cx, cy, R, 0, Math.PI * 2); x.clip();
    const bg = x.createRadialGradient(cx, cy, 10, cx, cy, R); bg.addColorStop(0, '#16405e'); bg.addColorStop(1, '#071a2e'); x.fillStyle = bg; x.fillRect(cx - R, cy - R, R * 2, R * 2);
    // fluffy aggregate
    const r = rng(11); for (let i = 0; i < 70; i++) { const a = r() * 6.28, d = Math.pow(r(), 0.6) * 220; circle(x, cx + Math.cos(a) * d, cy + Math.sin(a) * d * 0.8, 10 + r() * 26, 'rgba(220,235,245,0.10)'); }
    const pk = ss(C.plancton, C.plancton + 0.4, t), pa = ss(C.particulas, C.particulas + 0.4, t), ex = ss(C.excrementos, C.excrementos + 0.4, t);
    // plankton bits
    for (let i = 0; i < 6; i++) { const a = i * 1.05 + 0.3, d = 140; x.save(); x.translate(cx + Math.cos(a) * d, cy + Math.sin(a) * d * 0.7); x.rotate(a + t * 0.3); x.scale(pk, pk); x.strokeStyle = '#7dffb0'; x.lineWidth = 4; glow(x, '#3dff8a', 14); x.beginPath(); x.ellipse(0, 0, 26, 12, 0, 0, 7); x.stroke(); x.beginPath(); x.moveTo(-26, 0); x.lineTo(26, 0); x.stroke(); x.restore(); }
    // stuck particles
    for (let i = 0; i < 14; i++) { const a = i * 0.45, d = 60 + (i % 3) * 30; circle(x, cx + Math.cos(a) * d, cy + Math.sin(a) * d * 0.7, 8 * pa, '#d8c8a0'); }
    // pellets
    for (let i = 0; i < 3; i++) { const px = cx - 60 + i * 60, py = cy + 120 - i * 15; x.save(); x.translate(px, py); x.scale(ex, ex); x.fillStyle = '#6b4a2a'; x.beginPath(); x.ellipse(0, 0, 26, 12, 0.3, 0, 7); x.fill(); x.restore();
      if (ex > 0.5) { x.strokeStyle = 'rgba(160,200,90,0.7)'; x.lineWidth = 3; for (let k = 0; k < 2; k++) { x.beginPath(); x.moveTo(px - 8 + k * 14, py - 25); x.bezierCurveTo(px - 18 + k * 14, py - 40 - Math.sin(t * 5) * 5, px + 2 + k * 14, py - 55, px - 8 + k * 14, py - 70); x.stroke(); } } }
    x.restore();
    x.strokeStyle = '#bfefff'; x.lineWidth = 10; glow(x, '#5ff2ff', 20); x.beginPath(); x.arc(cx, cy, R, 0, 7); x.stroke(); noGlow(x);
    x.save(); x.translate(cx + R * 0.72, cy + R * 0.72); x.rotate(0.8); x.fillStyle = '#9cb4c4'; roundRect(x, -18, 0, 36, 180 * zk, 14); x.fill(); x.restore();
    label(x, t, C.plancton, C.piensa + 0.5, 'PLANCTON', cx + 470, cy - 200, { color: '#3dff8a' });
    label(x, t, C.particulas, C.piensa + 0.5, 'PARTÍCULAS', cx + 470, cy - 70, { color: '#e8d8a8' });
    label(x, t, C.excrementos, C.piensa + 0.5, 'EXCREMENTOS', cx + 470, cy + 60, { color: '#c08a4a' });
    label(x, t, C.yase, C.piensa + 0.5, 'YA SÉ...', cx + 470, cy + 190, { color: '#ff8fa3' });
    x.restore();
  }
  if (split > 0) {
    x.save(); x.globalAlpha = split;
    // top: sunny surface
    const sg = x.createLinearGradient(0, 0, 0, H / 2); sg.addColorStop(0, '#3fa9d8'); sg.addColorStop(1, '#0d4a78'); x.fillStyle = sg; x.fillRect(0, 0, W, H / 2);
    const sunK = ss(C.superficie, C.superficie + 0.6, t);
    glow(x, '#ffe680', 80); circle(x, 300, 110 - 40 * (1 - sunK), 70, '#ffe680'); noGlow(x);
    x.strokeStyle = 'rgba(255,255,255,0.4)'; x.lineWidth = 3; x.beginPath(); for (let i = 0; i <= 40; i++) { const xx = i * 48; x.lineTo(xx, 30 + Math.sin(i * 0.8 + t * 2) * 6); } x.stroke();
    const gk = ss(C.organismos, C.organismos + 2.5, t);
    const r = rng(21); for (let i = 0; i < 50; i++) { const px = 500 + r() * 1350, py = 90 + r() * 400; circle(x, px, py, (4 + r() * 6) * gk, '#5dff8f'); }
    label(x, t, C.organismos, C.ahoraAbajo + 0.3, 'CRECEN CON LUZ DEL SOL', 1150, 120, { color: '#5dff8f' });
    // bottom: darkness
    const dg = x.createLinearGradient(0, H / 2, 0, H); dg.addColorStop(0, '#04122a'); dg.addColorStop(1, '#000208'); x.fillStyle = dg; x.fillRect(0, H / 2, W, H / 2);
    x.fillStyle = 'rgba(255,255,255,0.8)'; x.fillRect(0, H / 2 - 2, W, 4);
    // crumbs falling
    const fall = ss(C.ahoraAbajo - 0.5, C.migajas + 1.5, t);
    for (let i = 0; i < 12; i++) { const px = 700 + (i % 4) * 70 + Math.sin(i) * 30, py = lerp(380, 820, clamp(fall * 1.3 - i * 0.03)); if (py < 820) circle(x, px, py, 6, '#e8f0d8'); }
    // deep fish
    const df = ss(C.ahoraAbajo, C.ahoraAbajo + 1, t);
    drawFish(x, lerp(W + 200, 1080, df), 830, 1.0, t, t > C.migajas ? 0.5 + 0.5 * Math.abs(Math.sin(t * 7)) : 0.2, -1, { color: '#5a3a6a', fin: '#3a2448', eyeBig: 1.4 });
    label(x, t, C.migajas, C.m4000, 'MIGAJAS DEL DESAYUNO', 1450, 700, { color: '#ffe14d' });
    arrow(x, 760, 470, 760, 640, '#ffe14d', 6, ss(C.ahoraAbajo, C.ahoraAbajo + 0.6, t));
    x.restore();
  }
}, { gauge: 1, gaugeFn: t => 1 - ss(C.piensa + 0.1, C.piensa + 0.6, t), subsY: 0 });
sfx(C.acercate, 'whoosh', 0.8); sfx(C.plancton, 'pop', 0.6); sfx(C.particulas, 'pop', 0.6); sfx(C.excrementos, 'squish', 0.9); sfx(C.yase, 'boing', 0.7);
sfx(C.piensa + 0.1, 'whoosh', 0.8); sfx(C.superficie, 'sparkle', 0.7); sfx(C.organismos, 'bubbles', 0.5); sfx(C.ahoraAbajo, 'whoosh', 0.5); sfx(C.migajas, 'munch', 0.9);

// E: 4000 m tiny cup + foam physics
scene(C.m4000, (x, t) => {
  drawOcean(x, t);
  drawROV(x, t);
  const zoom = win(t, C.teacuerdas - 0.2, C.material + 0.1, 0.4);
  const s0 = 0.62 * cupScale(t);
  if (zoom > 0.01) {
    const s = lerp(s0, 1.7 * cupScale(t), easeOut(zoom)), cx = lerp(95, 820, easeOut(zoom)), cy = lerp(H - 262, 780, easeOut(zoom));
    if (t > C.cuesta) drawCup(x, 820, 780, 1.7, 0, { ghost: true, alpha: ss(C.cuesta, C.cuesta + 0.4, t) * zoom });
    drawCup(x, cx, cy, s, 1);
    ringHighlight(x, t, C.buscaCarita, C.cuesta, 820, 780 - 1.7 * cupScale(t) * 120, 90);
    label(x, t, CE.buscaCarita, C.cuesta, '¡AHÍ SIGUE!', 1150, 520, { color: '#ffe14d' });
    label(x, t, C.cuesta + 0.3, C.material, 'ANTES', 820, 780 - 1.7 * 220 - 50, { color: '#ffffff', size: 34 });
    label(x, t, C.juguete, C.material, '¡TAMAÑO JUGUETE!', 1250, 600, { color: '#ff8fa3', size: 50 });
    if (t > C.como && t < C.material + 0.1) { arrow(x, 820, 380, 820, 780 - 1.7 * cupScale(t) * 220 + 10, '#5ff2ff', 7, ss(C.como + 0.8, C.como + 1.4, t)); label(x, t, C.como, C.material, '¿Y SI EL AGUA ENTRA?', 1250, 760, { color: '#5ff2ff', size: 40 }); }
  } else cupOnRov(x, t);
  // foam cross-section
  const fs_ = win(t, C.material, C.oceanografos, 0.4);
  if (fs_ > 0) {
    x.save(); x.globalAlpha = fs_;
    const cx = W / 2 - 80, cy = 470, R = 340;
    x.fillStyle = 'rgba(2,12,28,0.6)'; x.fillRect(0, 0, W, H);
    x.save(); x.beginPath(); x.arc(cx, cy, R, 0, 7); x.clip();
    x.fillStyle = '#e8eef2'; x.fillRect(cx - R, cy - R, 2 * R, 2 * R);
    const comp = ss(C.presion, C.presion + 2.2, t);
    const wall = ss(C.encoge, C.encoge + 1.2, t);
    x.save(); x.translate(cx, cy); x.scale(1 - 0.45 * wall, 1 - 0.45 * wall);
    const r = rng(5);
    for (let i = 0; i < 46; i++) {
      const bx = (r() * 2 - 1) * R, by = (r() * 2 - 1) * R, br = (18 + r() * 26) * (1 - 0.6 * comp);
      x.fillStyle = 'rgba(170,215,240,0.85)'; x.strokeStyle = '#7aa8c4'; x.lineWidth = 3; x.beginPath(); x.arc(bx, by, br, 0, 7); x.fill(); x.stroke();
    }
    x.restore();
    x.restore();
    x.strokeStyle = '#bfefff'; x.lineWidth = 10; glow(x, '#5ff2ff', 20); x.beginPath(); x.arc(cx, cy, R, 0, 7); x.stroke(); noGlow(x);
    label(x, t, C.huequitos, C.oceanografos, 'HUEQUITOS CON GAS', cx, cy - R - 10, { color: '#5ff2ff' });
    if (t > C.presion) for (let i = 0; i < 8; i++) {
      const a = i * Math.PI / 4, p = ss(C.presion, C.presion + 0.6, t), pul = Math.sin(t * 6) * 12;
      arrow(x, cx + Math.cos(a) * (R + 170 + pul), cy + Math.sin(a) * (R + 170 + pul), cx + Math.cos(a) * (R + 30), cy + Math.sin(a) * (R + 30), '#ff5a5a', 9, p);
    }
    label(x, t, C.presion, C.oceanografos, 'PRESIÓN', cx + R + 300, cy, { color: '#ff5a5a', size: 50 });
    label(x, t, C.dibujo, C.oceanografos, 'DIBUJO INCLUIDO', cx, cy + R + 10, { color: '#ffe14d' });
    if (t > C.encoge) { drawCup(x, 1500, 900, lerp(0.9, 0.5, wall), 1); }
    x.restore();
  }
}, { gauge: 1 });
sfx(C.teacuerdas - 0.2, 'whoosh', 0.7); sfx(C.buscaCarita, 'pop', 0.6); sfx(CE.buscaCarita, 'sparkle', 0.5); sfx(C.cuesta, 'shrink', 0.9); sfx(C.juguete, 'boing', 0.6);
sfx(C.como, 'pop', 0.5); sfx(C.material, 'whoosh', 0.8); sfx(C.huequitos, 'bubbles', 0.7); sfx(C.presion, 'creak', 1); sfx(C.encoge, 'shrink', 1); sfx(C.dibujo, 'pop', 0.6);

// F: before/after souvenirs
scene(C.oceanografos, (x, t) => {
  drawOcean(x, t);
  x.fillStyle = 'rgba(2,12,28,0.55)'; x.fillRect(0, 0, W, H);
  const a = easeOutBack(clamp((t - C.oceanografos) / 0.5));
  drawCup(x, 620, 760, 1.6 * a, 1);
  const b = ss(C.miniatura - 0.6, C.miniatura + 0.3, t);
  drawCup(x, 1250, 760, lerp(1.6, 0.6, b) * a, 1);
  text(x, 'ANTES', 620, 860, 56, '#fff', { alpha: a });
  text(x, 'DESPUÉS', 1250, 860, 56, '#ffe14d', { alpha: a });
  arrow(x, 830, 620, 1080, 620, '#5ff2ff', 8, ss(C.oceanografos + 0.5, C.oceanografos + 1.2, t));
  label(x, t, C.oceanografos + 0.6, C.recuerdo, 'EXPERIMENTO REAL', W / 2, 200, { color: '#5ff2ff' });
  if (t > C.recuerdo) {
    label(x, t, C.recuerdo, C.m6000, 'EL RECUERDO MÁS PEQUEÑO', W / 2, 200, { color: '#ffe14d', size: 50 });
    const r = rng(9); for (let i = 0; i < 10; i++) { const k = ((t - C.recuerdo) * 0.8 + r()) % 1; x.save(); x.globalAlpha = 1 - k; text(x, '✦', 1250 + (r() * 2 - 1) * 160, 700 - k * 200, 30 + r() * 20, '#ffe14d', { glow: '#ffe14d' }); x.restore(); }
  }
}, { gauge: 1 });
sfx(C.oceanografos, 'whoosh', 0.8); sfx(C.oceanografos + 0.6, 'pop', 0.6); sfx(C.miniatura - 0.6, 'shrink', 0.9); sfx(C.recuerdo, 'sparkle', 0.8);

// G: 6000 m halfway, tilt down
scene(C.m6000, (x, t) => {
  const tilt = ss(C.gira2, C.gira2 + 1.0, t);
  drawOcean(x, t, { speed: 38 + 400 * Math.sin(tilt * Math.PI) });
  const bp = win(t, C.adivinar, C.gira2, 0.3);
  if (bp > 0) {
    x.save(); x.globalAlpha = bp;
    const x0 = 360, x1 = 1560, y = 520;
    x.strokeStyle = 'rgba(255,255,255,0.3)'; x.lineWidth = 26; x.lineCap = 'round'; x.beginPath(); x.moveTo(x0, y); x.lineTo(x1, y); x.stroke();
    const p = lerp(0, 6 / 11, ss(C.adivinar + 0.3, C.adivinar + 1.5, t));
    x.strokeStyle = '#5ff2ff'; glow(x, '#5ff2ff', 20); x.beginPath(); x.moveTo(x0, y); x.lineTo(lerp(x0, x1, p), y); x.stroke(); noGlow(x);
    text(x, '0 KM', x0, y + 60, 34, '#fff'); text(x, '11 KM', x1, y + 60, 34, '#fff');
    x.strokeStyle = '#ffe14d'; x.lineWidth = 4; x.setLineDash([10, 8]); x.beginPath(); x.moveTo((x0 + x1) / 2, y - 60); x.lineTo((x0 + x1) / 2, y + 40); x.stroke(); x.setLineDash([]);
    if (t > C.mitad) label(x, t, C.mitad, C.gira2, '¡PASAMOS LA MITAD!', (x0 + x1) / 2, y - 110, { color: '#ffe14d', size: 48 });
    else text(x, '?', lerp(x0, x1, p), y - 80, 70, '#5ff2ff', { glow: '#5ff2ff' });
    label(x, t, C.zona, C.gira2, 'ZONA MÁS PROFUNDA: DENTRO DE LAS FOSAS', W / 2, 700, { color: '#5ff2ff', size: 40 });
    x.restore();
  }
  if (t > C.suelo) {
    label(x, t, C.suelo, C.foco, '¿SUELO?', W / 2, 520, { color: '#ffffff', size: 56 });
    label(x, t, C.tampoco, C.foco + 0.3, 'NADA', W / 2, 640, { color: '#ff5a5a', size: 46 });
    if (t > C.fondoKm) { const p = ss(C.fondoKm, C.fondoKm + 0.6, t); arrow(x, W / 2, 500, W / 2, 820, '#ffe14d', 9, p); label(x, t, C.fondoKm + 0.2, C.apuesta, 'FONDO: A VARIOS KM', W / 2, 430, { color: '#ffe14d', size: 48 }); }
  }
  drawROV(x, t); cupOnRov(x, t);
}, { gauge: 1 });
sfx(C.adivinar, 'whoosh', 0.6); sfx(C.adivinar + 0.3, 'riser', 0.6); sfx(C.mitad, 'sparkle', 0.8); sfx(C.zona, 'pop', 0.5); sfx(C.gira2, 'whoosh', 1);
sfx(C.suelo, 'pop', 0.6); sfx(C.tampoco, 'boing', 0.5); sfx(C.fondoKm, 'whooshDown', 0.8);

// H: the bet — sketch of armored fish
scene(C.apuesta, (x, t) => {
  drawOcean(x, t, { speed: 20 });
  x.fillStyle = 'rgba(0,0,0,0.45)'; x.fillRect(0, 0, W, H);
  const k = easeOutBack(clamp((t - C.apuesta) / 0.5));
  x.save(); x.translate(W / 2, 480); x.rotate(-0.03); x.scale(k, k);
  x.fillStyle = '#f4ecd8'; x.shadowColor = 'rgba(0,0,0,0.6)'; x.shadowBlur = 40; x.fillRect(-620, -340, 1240, 680); noGlow(x);
  x.strokeStyle = 'rgba(120,150,200,0.35)'; x.lineWidth = 2; for (let i = 0; i < 12; i++) { x.beginPath(); x.moveTo(-620, -300 + i * 55); x.lineTo(620, -300 + i * 55); x.stroke(); }
  text(x, '¿QUÉ NADA A 8.000 m?', 0, -270, 54, '#2a3a5a', { alpha: ss(C.q8000, C.q8000 + 0.3, t) });
  const p = ss(C.dibujado, C.armadura + 0.3, t);
  x.strokeStyle = '#333'; x.lineWidth = 7; x.lineCap = 'round'; x.lineJoin = 'round'; x.setLineDash([Math.max(0.001, 4200 * p), 9000]); if (p <= 0.002) x.strokeStyle = 'rgba(0,0,0,0)';
  x.beginPath();
  x.moveTo(-360, 0); x.lineTo(-250, -150); x.lineTo(150, -170); x.lineTo(320, -40); x.lineTo(320, 40); x.lineTo(150, 170); x.lineTo(-250, 150); x.closePath();
  x.moveTo(-360, 0); x.lineTo(-500, -120); x.lineTo(-470, 0); x.lineTo(-500, 120); x.closePath();
  for (let i = 0; i < 4; i++) { x.moveTo(-200 + i * 100, -160); x.lineTo(-170 + i * 100, 160); }
  x.moveTo(-250, -150); x.lineTo(-200, -230); x.lineTo(-120, -160); x.moveTo(0, -165); x.lineTo(60, -240); x.lineTo(120, -168);
  x.stroke(); x.setLineDash([]);
  if (p > 0.7) { circle(x, 230, -40, 22, '#333'); circle(x, 236, -44, 7, '#fff'); x.lineWidth = 6; x.beginPath(); x.moveTo(260, 60); x.lineTo(320, 40); x.stroke(); }
  if (t > C.armadura) { const a = ss(C.armadura, C.armadura + 0.3, t); x.globalAlpha = a; x.fillStyle = 'rgba(120,120,140,0.25)'; x.fillRect(-250, -160, 400, 320); x.globalAlpha = 1; }
  text(x, 'PLACAS GRUESAS = ARMADURA', 0, 260, 44, '#7a2a2a', { alpha: ss(C.armadura, C.armadura + 0.3, t) });
  // red X
  if (t > C.miraEsto - 0.05) {
    const xp = ss(C.miraEsto - 0.05, C.miraEsto + 0.25, t);
    x.strokeStyle = '#e02424'; x.lineWidth = 26; glow(x, '#ff3030', 20);
    x.beginPath(); x.moveTo(-420, -260); x.lineTo(lerp(-420, 420, clamp(xp * 2)), lerp(-260, 260, clamp(xp * 2))); x.stroke();
    if (xp > 0.5) { x.beginPath(); x.moveTo(420, -260); x.lineTo(lerp(420, -420, clamp(xp * 2 - 1)), lerp(-260, 260, clamp(xp * 2 - 1))); x.stroke(); }
    noGlow(x);
  }
  x.restore();
  // pencil
  if (t > C.dibujado && t < C.armadura + 0.4) { const pp = ss(C.dibujado, C.armadura + 0.3, t); const px = W / 2 + Math.cos(pp * 30) * 300, py = 480 + Math.sin(pp * 23) * 150; x.save(); x.translate(px + 30, py - 70); x.rotate(0.5); x.fillStyle = '#f2b632'; x.fillRect(-12, -120, 24, 120); x.fillStyle = '#333'; x.beginPath(); x.moveTo(-12, 0); x.lineTo(12, 0); x.lineTo(0, 26); x.fill(); x.restore(); }
}, { gauge: 0 });
sfx(C.apuesta, 'whoosh', 0.8); sfx(C.apuesta + 0.1, 'paper', 0.8); sfx(C.dibujado, 'scribbleLong', 0.9); sfx(C.armadura, 'clank', 0.7); sfx(C.miraEsto - 0.05, 'swipe', 1); sfx(C.miraEsto + 0.15, 'swipe', 0.9);

// I: real camera — snailfish 8178 m
scene(C.miraEsto + 0.5, (x, t) => {
  drawOcean(x, t);
  const fx = lerp(W + 400, 900, easeOut(clamp((t - C.camaraReal - 0.6) / 2.5))) - 120 * ss(C.nadando, C.nadando + 2.5, t);
  const fy = 520 + Math.sin(t * 0.8) * 25;
  drawSnailfish(x, fx, fy, 1.2, t);
  // REC frame
  const rec = ss(C.camaraReal, C.camaraReal + 0.3, t);
  if (rec > 0) {
    x.save(); x.globalAlpha = rec; x.strokeStyle = '#fff'; x.lineWidth = 6;
    const m = 60; const c = 70;
    [[m, m, 1, 1], [W - 300, m, -1, 1], [m, H - 200, 1, -1], [W - 300, H - 200, -1, -1]].forEach(([a, b, sx, sy]) => { x.beginPath(); x.moveTo(a, b + c * sy); x.lineTo(a, b); x.lineTo(a + c * sx, b); x.stroke(); });
    if (Math.floor(t * 2) % 2 === 0) circle(x, 110, 115, 14, '#ff2a2a');
    text(x, 'REC', 175, 117, 40, '#fff');
    text(x, 'RECREACIÓN', 120, 170, 26, 'rgba(255,255,255,0.7)', { align: 'left' });
    x.restore();
  }
  label(x, t, C.m8178, C.piel, 'PEZ CARACOL · 8.178 m', 900, 300, { color: '#ffb3c1', size: 50 });
  if (t > C.piel) { label(x, t, C.piel, C.cola, 'PIEL CLARA · CUERPO BLANDO', 900, 300, { color: '#ffffff' }); ringHighlight(x, t, C.piel, C.cola, fx - 60, fy, 170, '#ffffff'); }
  if (t > C.cola) { label(x, t, C.cola, C.pelicula, 'COLA DE RENACUAJO', fx - 380, fy - 190, { color: '#ffe14d' }); arrow(x, fx - 380, fy - 140, fx - 300, fy - 30, '#ffe14d', 6, ss(C.cola, C.cola + 0.4, t)); }
  if (t > C.pelicula) {
    const k = easeOutBack(clamp((t - C.pelicula) / 0.4)), al = 1 - ss(C.nadando - 0.3, C.nadando, t);
    x.save(); x.globalAlpha = al; x.translate(1450, 280); x.scale(k, k);
    x.fillStyle = '#222'; x.fillRect(-120, -40, 240, 150); x.save(); x.translate(-120, -40); x.rotate(-0.25 * (1 - ss(C.pelicula + 0.5, C.pelicula + 0.7, t))); x.fillStyle = '#222'; x.fillRect(0, -40, 240, 40);
    x.fillStyle = '#fff'; for (let i = 0; i < 5; i++) { x.beginPath(); x.moveTo(i * 50 + 10, -40); x.lineTo(i * 50 + 35, -40); x.lineTo(i * 50 + 25, 0); x.lineTo(i * 50, 0); x.fill(); } x.restore();
    text(x, '¿MÁS INTIMIDANTE?', 0, 40, 34, '#fff'); x.restore();
  }
  label(x, t, C.nadando, C.trampa, 'Y AHÍ ESTABA, NADANDO', 900, 300, { color: '#5ff2ff' });
  drawROV(x, t); cupOnRov(x, t);
}, { gauge: 1 });
sfx(C.miraEsto + 0.5, 'whoosh', 0.7); sfx(C.camaraReal, 'rec', 0.8); sfx(C.camaraReal + 0.6, 'swim', 0.7); sfx(C.m8178, 'pop', 0.7); sfx(C.piel, 'pop', 0.5);
sfx(C.cola, 'pop', 0.5); sfx(C.pelicula + 0.5, 'clap', 0.9); sfx(C.nadando, 'swim', 0.6);

// J: gas vs water
scene(C.trampa, (x, t) => {
  drawOcean(x, t, { speed: 20 });
  x.fillStyle = 'rgba(2,10,24,0.7)'; x.fillRect(0, 0, W, H);
  const a = easeOutBack(clamp((t - C.trampa) / 0.5));
  const jars = [[560, 'GAS', '#ff8f5a'], [1260, 'AGUA', '#5ff2ff']];
  const pr = ss(C.gas + 0.3, C.gas + 2.0, t), pr2 = ss(C.aguaMenos, C.aguaMenos + 1.8, t);
  jars.forEach(([cx, name, col], i) => {
    x.save(); x.translate(cx, 520); x.scale(a, a);
    x.strokeStyle = 'rgba(220,240,255,0.8)'; x.lineWidth = 6; roundRect(x, -200, -230, 400, 460, 40); x.stroke();
    x.fillStyle = 'rgba(40,110,170,0.25)'; roundRect(x, -200, -230, 400, 460, 40); x.fill();
    if (i === 0) { const r = 130 * (1 - 0.65 * pr); glow(x, col, 30); circle(x, 0, 0, r, 'rgba(255,170,120,0.85)'); noGlow(x); }
    else { const s = 220 * (1 - 0.04 * pr2); x.fillStyle = 'rgba(95,200,255,0.75)'; glow(x, col, 30); x.fillRect(-s / 2, -s / 2, s, s); noGlow(x); if (t > C.aguaPez) { x.globalAlpha = ss(C.aguaPez, C.aguaPez + 0.4, t); drawSnailfish(x, 40, 0, 0.35, t); x.globalAlpha = 1; } }
    text(x, name, 0, 300, 64, col, { glow: col, glowBlur: 15 });
    if ((i === 0 && t > C.gas) || (i === 1 && t > C.aguaMenos)) for (let k = 0; k < 4; k++) { const ang = k * Math.PI / 2 + Math.PI / 4, pul = Math.sin(t * 6) * 8; arrow(x, Math.cos(ang) * (330 + pul), Math.sin(ang) * (330 + pul), Math.cos(ang) * 235, Math.sin(ang) * 235, '#ff5a5a', 8, 1); }
    x.restore();
  });
  label(x, t, C.gas + 1.5, C.adapt, 'SE COMPRIME MUCHO', 560, 170, { color: '#ff8f5a' });
  label(x, t, C.aguaMenos + 1.2, C.adapt, 'CASI NO CAMBIA', 1260, 170, { color: '#5ff2ff' });
  label(x, t, C.adapt, C.m9000, 'ADAPTACIONES EXTRAORDINARIAS', W / 2, 170, { color: '#ffe14d', size: 46 });
  label(x, t, C.coraza, C.m9000, '✗  CORAZA NO ERA LA RESPUESTA', W / 2, 850, { color: '#ff5a5a', size: 44 });
}, { gauge: 0 });
sfx(C.trampa, 'whoosh', 0.8); sfx(C.gas + 0.3, 'creak', 0.9); sfx(C.gas + 1.5, 'pop', 0.5); sfx(C.aguaPez, 'bubbles', 0.5); sfx(C.aguaMenos, 'thunk', 0.6);
sfx(C.adapt, 'sparkle', 0.6); sfx(C.coraza, 'buzz', 0.7);

// K: Everest in the trench
scene(C.m9000, (x, t) => {
  x.fillStyle = '#020b18'; x.fillRect(0, 0, W, H);
  const top = 120, bot = 960, z = d => lerp(top, bot, d / 11000);
  // water
  const g = x.createLinearGradient(0, top, 0, bot); g.addColorStop(0, '#1a6ea8'); g.addColorStop(0.3, '#0a3560'); g.addColorStop(1, '#010814'); x.fillStyle = g;
  x.beginPath(); x.moveTo(0, top); x.lineTo(W, top); x.lineTo(W, z(6000)); x.lineTo(1500, z(6000)); x.lineTo(1250, bot); x.lineTo(650, bot); x.lineTo(420, z(6000)); x.lineTo(0, z(6000)); x.closePath(); x.fill();
  // seabed
  x.fillStyle = '#3a2e22'; x.beginPath(); x.moveTo(0, z(6000)); x.lineTo(420, z(6000)); x.lineTo(650, bot); x.lineTo(1250, bot); x.lineTo(1500, z(6000)); x.lineTo(W, z(6000)); x.lineTo(W, H); x.lineTo(0, H); x.closePath(); x.fill();
  x.strokeStyle = '#7fdcff'; x.lineWidth = 4; x.beginPath(); for (let i = 0; i <= 40; i++) x.lineTo(i * 48, top + Math.sin(i * 0.7 + t * 2) * 5); x.stroke();
  text(x, 'SUPERFICIE', 140, top - 40, 32, '#7fdcff');
  // ship
  x.fillStyle = '#ddd'; x.beginPath(); x.moveTo(820, top - 5); x.lineTo(1100, top - 5); x.lineTo(1070, top + 25); x.lineTo(850, top + 25); x.fill(); x.fillRect(900, top - 45, 90, 40);
  // Everest
  const ev = ss(C.everest, C.everest + 1.2, t);
  const peakD = 10935 - 8849;
  x.save(); x.beginPath(); x.rect(0, 0, W, bot); x.clip();
  x.translate(0, (1 - ev) * 900);
  const eg = x.createLinearGradient(0, z(peakD), 0, bot); eg.addColorStop(0, '#ffffff'); eg.addColorStop(0.12, '#c8d2dc'); eg.addColorStop(0.2, '#6b7b8a'); eg.addColorStop(1, '#3a4652');
  x.fillStyle = eg; x.beginPath(); x.moveTo(680, bot); x.lineTo(820, z(5500)); x.lineTo(880, z(4200)); x.lineTo(930, z(peakD)); x.lineTo(1000, z(3600)); x.lineTo(1080, z(5200)); x.lineTo(1220, bot); x.closePath(); x.fill();
  x.restore();
  label(x, t, C.everest + 0.6, C.cima, 'EVEREST', 950, 700, { color: '#ffffff', size: 50 });
  // summit line
  if (t > C.cima) {
    const p = ss(C.cima, C.cima + 0.8, t);
    x.strokeStyle = '#ffe14d'; x.lineWidth = 4; x.setLineDash([16, 12]); x.beginPath(); x.moveTo(0, z(peakD)); x.lineTo(W * p, z(peakD)); x.stroke(); x.setLineDash([]);
    label(x, t, C.dosKm, DUR, 'CIMA ≈ 2 KM BAJO EL AGUA', 380, z(peakD) - 50, { color: '#ffe14d', size: 38 });
  }
  if (t > C.todo) { x.fillStyle = `rgba(95,242,255,${0.12 * ss(C.todo, C.todo + 0.5, t)})`; x.fillRect(0, z(peakD), W, bot - z(peakD)); label(x, t, C.todo + 0.3, DUR, 'TODO EL VIAJE: DEBAJO DE LA CUMBRE', 1480, z(4500), { color: '#5ff2ff', size: 32 }); }
  // camera marker
  const cy = z(depthAt(t)), cx = 1270 - (z(depthAt(t)) - z(6000)) * 0.1 + 60;
  x.strokeStyle = 'rgba(255,255,255,0.5)'; x.lineWidth = 2; x.beginPath(); x.moveTo(cx, top); x.lineTo(cx, cy); x.stroke();
  glow(x, '#ffe14d', 20); x.fillStyle = '#d98a1e'; roundRect(x, cx - 26, cy - 18, 52, 36, 8); x.fill(); circle(x, cx + 26, cy, 8, '#fff8d0'); noGlow(x);
  if (t > C.faltan2) {
    const p = ss(C.faltan2, C.faltan2 + 0.6, t);
    x.strokeStyle = '#ff8fa3'; x.lineWidth = 5; x.beginPath(); x.moveTo(cx + 70, cy); x.lineTo(cx + 90, cy); x.lineTo(cx + 90, lerp(cy, bot, p)); x.lineTo(cx + 70, lerp(cy, bot, p)); x.stroke();
    label(x, t, C.faltan2 + 0.3, DUR, '≈ 2 KM', cx + 200, (cy + bot) / 2, { color: '#ff8fa3', size: 40 });
  }
  label(x, t, C.colocar, C.everest, 'ALGO CONOCIDO PARA COMPARAR', W / 2, 300, { color: '#ffffff', size: 40 });
}, { gauge: 1 });
sfx(C.colocar, 'whoosh', 0.8); sfx(C.everest, 'rumble', 1); sfx(C.everest + 0.6, 'pop', 0.6); sfx(C.cima, 'riser', 0.6); sfx(C.dosKm, 'pop', 0.6); sfx(C.todo + 0.3, 'pop', 0.5); sfx(C.faltan2, 'whooshDown', 0.6);

// L: title card
scene(C.titulo, (x, t) => {
  x.fillStyle = '#000'; x.fillRect(0, 0, W, H);
  drawOcean(x, t, { lights: 0.3, speed: 15, density: 0.6 });
  x.fillStyle = 'rgba(0,0,0,0.55)'; x.fillRect(0, 0, W, H);
  const lines = ['¿QUÉ VERÍA UNA CÁMARA', 'AL BAJAR AL LUGAR', 'MÁS PROFUNDO DEL OCÉANO?'];
  // reveal words in sync
  const [i0] = findPhrase('qué vería una cámara', 0);
  let wi = 0;
  lines.forEach((ln, li) => {
    const words = ln.split(' ');
    x.font = '110px Anton'; const sp = 26;
    const ws = words.map(w => x.measureText(w).width); const tot = ws.reduce((a, b) => a + b, 0) + sp * (words.length - 1);
    let px = W / 2 - tot / 2;
    words.forEach((w, k) => {
      const tk = TOK[i0 + wi]; wi++;
      const kk = easeOutBack(clamp((t - tk.s + 0.05) / 0.25));
      x.save(); x.translate(px + ws[k] / 2, 330 + li * 150); x.scale(kk, kk);
      text(x, w, 0, 0, 110, li === 2 ? '#ffe14d' : '#fff', { stroke: 10, strokeColor: '#000', glow: li === 2 ? '#ffb000' : '#5ff2ff', glowBlur: 30 });
      x.restore(); px += ws[k] + sp;
    });
  });
}, { gauge: 0, nosubs: true });
sfx(C.titulo, 'stinger', 1);

// M: 10000 m looking down, floor appears
scene(C.m10000 - 0.1, (x, t) => {
  drawOcean(x, t, { lights: 0.6, density: 0 });
  const t0 = C.m10000;
  const floorK = ss(C.estaVez, C.clara + 1.5, t);
  // floor disc in center
  if (floorK > 0) {
    const R = lerp(60, 1300, floorK * floorK);
    const fg = x.createRadialGradient(W / 2, H / 2, 10, W / 2, H / 2, R);
    fg.addColorStop(0, `rgba(205,190,160,${0.9 * floorK})`); fg.addColorStop(0.6, `rgba(130,118,95,${0.6 * floorK})`); fg.addColorStop(1, 'rgba(0,0,0,0)');
    x.fillStyle = fg; x.fillRect(0, 0, W, H);
  }
  // particles falling away (perspective)
  const r = rng(77);
  for (let i = 0; i < 160; i++) {
    const px = (r() * 2 - 1) * 1600, py = (r() * 2 - 1) * 900, ph = r();
    let z = 1 + (((t - t0) * 0.35 + ph) % 1) * 7;
    const floorZ = lerp(30, 7.2, floorK);
    const landed = z >= floorZ - 0.05;
    z = Math.min(z, floorZ);
    const sx = W / 2 + px / z, sy = H / 2 + py / z, sr = 9 / z + 1;
    const al = landed ? 0.9 : clamp(1.2 - z / 8);
    circle(x, sx, sy, sr, `rgba(235,245,255,${al})`);
    if (landed && t > C.aterrizar) circle(x, sx, sy, sr * 2.5, 'rgba(220,210,180,0.25)');
  }
  label(x, t, C.durante, C.estaVez, 'CAEN... Y SE PIERDEN', W / 2, 220, { color: '#ffffff' });
  label(x, t, C.clara, C.m10900, '¡UNA SUPERFICIE CLARA!', W / 2, 220, { color: '#ffe14d', size: 50 });
  label(x, t, C.aterrizar, C.m10900 + 0.5, 'ATERRIZAN', W / 2, 330, { color: '#5ff2ff' });
}, { gauge: 1 });
sfx(C.m10000 - 0.1, 'whoosh', 0.7); sfx(C.durante, 'pop', 0.4); sfx(C.estaVez, 'riser', 0.8); sfx(C.clara, 'sparkle', 0.7); sfx(C.aterrizar, 'puff', 0.7);

// N + O: the bottom
const floorScene = (x, t) => {
  const land = C.fondo;
  const shake = t > land && t < land + 0.6 ? (1 - (t - land) / 0.6) * 14 * Math.sin(t * 80) : 0;
  const settle = 1 - easeOut(clamp((t - C.m10900 + 0.2) / (land - C.m10900 + 0.2)));
  x.save(); x.translate(0, shake - settle * 250);
  drawOcean(x, t, { density: 0.4, speed: -6 });
  // floor plane with perspective
  const hz = 430;
  const fg = x.createLinearGradient(0, hz, 0, H + 260); fg.addColorStop(0, '#2a2620'); fg.addColorStop(0.35, '#7a6c56'); fg.addColorStop(1, '#c9b892');
  x.fillStyle = fg; x.fillRect(0, hz, W, H + 300);
  const lg = x.createRadialGradient(W / 2, H * 0.8, 50, W / 2, H * 0.8, 900); lg.addColorStop(0, 'rgba(255,250,230,0.35)'); lg.addColorStop(1, 'rgba(0,0,0,0)'); x.fillStyle = lg; x.fillRect(0, hz, W, H + 300);
  // ripples
  const rip = ss(C.ondulaciones, C.ondulaciones + 0.6, t);
  for (let i = 0; i < 18; i++) {
    const k = i / 18, y = hz + Math.pow(k, 1.8) * 760;
    x.strokeStyle = `rgba(60,50,38,${0.25 + 0.35 * k + 0.3 * rip * Math.sin(t * 3 - i) ** 2})`; x.lineWidth = 2 + 5 * k;
    x.beginPath(); for (let j = 0; j <= 40; j++) { const xx = j * 48; x.lineTo(xx, y + Math.sin(j * 0.6 + i * 1.3) * (4 + 14 * k)); } x.stroke();
  }
  // dust puff on landing
  if (t > land && t < land + 2.5) { const k = (t - land) / 2.5; for (let i = 0; i < 18; i++) { const a = Math.PI + (i / 17) * Math.PI; circle(x, W / 2 + Math.cos(a) * 700 * k, H - 40 + Math.sin(a) * 160 * k, 60 + 120 * k, `rgba(200,185,150,${0.35 * (1 - k)})`); } }
  x.restore();
  label(x, t, C.fondo, C.demos + 0.5, '¡TOCAMOS FONDO!', W / 2, 260, { color: '#ffe14d', size: 60 });
  label(x, t, C.sedimento, C.vida, 'SEDIMENTO FINO', W / 2, 260, { color: '#e8d8a8' });
  label(x, t, C.ondulaciones, C.vida, 'ONDULACIONES DE LAS CORRIENTES', W / 2, 370, { color: '#5ff2ff', size: 38 });
};
const amphis = (x, t, eatT) => {
  const ap = ss(C.anfipodos - 0.6, C.anfipodos + 0.6, t);
  if (ap <= 0) return;
  const list = [[700, 760, 1.3, 0, 1], [1150, 820, 1.6, 1.2, -1], [950, 640, 0.9, 2.5, 1], [1400, 700, 1.0, 3.3, -1], [520, 880, 1.2, 4.1, 1]];
  list.forEach(([ax, ay, s, ph, dir], i) => {
    let px = ax + Math.sin(t * 0.6 + ph) * 40 + (1 - ap) * 500 * dir * -1;
    let py = ay;
    if (eatT && i === 1) { const k = ss(eatT - 1.2, eatT, t); px = lerp(px, 1000, k); py = lerp(py, 780, k); }
    x.save(); x.globalAlpha = ap; drawAmphipod(x, px, py, s, t, ph, dir); x.restore();
  });
};
scene(C.m10900, (x, t) => {
  floorScene(x, t);
  amphis(x, t);
  label(x, t, C.anfipodos, C.investigadores, 'ANFÍPODOS', 700, 600, { color: '#ffb3a1', size: 50 });
  label(x, t, C.crustaceos, C.investigadores, 'PARIENTES DE LOS CAMARONES', 1250, 560, { color: '#ffffff', size: 36 });
  label(x, t, C.investigadores, C.piensaCam, 'RECOGIDOS A 10.897 m', W / 2, 260, { color: '#5ff2ff', size: 50 });
  if (t > C.casa) { const k = easeOutBack(clamp((t - C.casa - 0.4) / 0.4)); x.save(); x.translate(1150, 690); x.scale(k, k); x.fillStyle = '#ffe14d'; glow(x, '#ffb000', 20); x.beginPath(); x.moveTo(-40, 0); x.lineTo(0, -40); x.lineTo(40, 0); x.closePath(); x.fill(); x.fillRect(-30, 0, 60, 45); noGlow(x); x.fillStyle = '#5a3a10'; x.fillRect(-10, 15, 20, 30); x.restore(); label(x, t, C.casa + 0.4, C.copo, 'SU CASA', 1150, 590, { color: '#ffe14d' }); }
}, { gauge: 1 });
sfx(C.m10900, 'whooshDown', 0.8); sfx(C.fondo, 'thud', 1); sfx(C.fondo + 0.05, 'puff', 0.8); sfx(C.sedimento, 'pop', 0.5); sfx(C.ondulaciones, 'sand', 0.6);
sfx(C.anfipodos - 0.6, 'skitter', 0.8); sfx(C.anfipodos, 'pop', 0.6); sfx(C.crustaceos, 'pop', 0.5); sfx(C.investigadores, 'pop', 0.6); sfx(C.casa + 0.4, 'sparkle', 0.7);

scene(C.copo, (x, t) => {
  floorScene(x, t);
  const eatT = C.comer2 + 0.6;
  // flake falling to the floor
  const fy = lerp(-40, 780, ss(C.copo, C.mota + 1.2, t));
  if (t < eatT + 0.1) { glow(x, '#ffffff', 20); circle(x, 1000, fy, 14, '#f4f8ff'); noGlow(x); ringHighlight(x, t, C.copo + 0.2, C.comer2, 1000, fy, 50, '#5ff2ff'); }
  amphis(x, t, eatT);
  if (t > eatT && t < eatT + 1) text(x, 'ÑAM', 1000, 680 - (t - eatT) * 60, 54, '#ffe14d', { stroke: 8, alpha: 1 - (t - eatT) });
  label(x, t, C.mota, C.comer2, 'ARRIBA: UNA MOTA MOLESTA', W / 2, 260, { color: '#ffffff', size: 42 });
  label(x, t, C.comer2, C.km11, '¿QUIÉN SE LO COME?', W / 2, 260, { color: '#ffe14d', size: 48 });
  // sun -> floor line
  if (t > C.km11) {
    const p = ss(C.km11, C.km11 + 1.2, t);
    x.save(); glow(x, '#ffe680', 50); circle(x, 150, 120, 55 * easeOutBack(clamp((t - C.km11) / 0.4)), '#ffe680'); noGlow(x);
    x.strokeStyle = '#ffe14d'; x.lineWidth = 6; x.setLineDash([16, 12]); x.lineDashOffset = -t * 60; x.beginPath(); x.moveTo(150, 180); x.lineTo(150, lerp(180, 900, p)); x.stroke(); x.setLineDash([]);
    text(x, '≈ 11 KM', 210, 520, 56, '#ffe14d', { align: 'left', stroke: 8, alpha: p });
    if (t > C.luzDia) { const k = ss(C.luzDia, C.luzDia + 2.5, t); glow(x, '#fff', 20); circle(x, 150, lerp(180, 880, k), 12, '#ffffff'); noGlow(x); label(x, t, C.luzDia + 0.4, C.duda, 'SU COMIDA EMPEZÓ BAJO EL SOL', W / 2 + 120, 260, { color: '#ffe680', size: 42 }); }
    x.restore();
  }
}, { gauge: 1 });
sfx(C.copo, 'whoosh', 0.6); sfx(C.mota, 'pop', 0.5); sfx(C.comer2, 'pop', 0.6); sfx(C.comer2 + 0.6, 'munch', 1); sfx(C.km11, 'sparkle', 0.7); sfx(C.luzDia, 'whooshDown', 0.6);

// P: next mystery — ship and sonar
scene(C.duda, (x, t) => {
  const sky = x.createLinearGradient(0, 0, 0, 300); sky.addColorStop(0, '#040a1c'); sky.addColorStop(1, '#0d1f3e'); x.fillStyle = sky; x.fillRect(0, 0, W, 300);
  const r = rng(4); for (let i = 0; i < 80; i++) circle(x, r() * W, r() * 260, r() * 1.8 + 0.3, `rgba(255,255,255,${0.3 + 0.5 * Math.abs(Math.sin(t * 2 + i))})`);
  const sea = x.createLinearGradient(0, 300, 0, H); sea.addColorStop(0, '#0a2a4a'); sea.addColorStop(1, '#000205'); x.fillStyle = sea; x.fillRect(0, 300, W, H);
  x.strokeStyle = '#3a7ab0'; x.lineWidth = 3; x.beginPath(); for (let i = 0; i <= 40; i++) x.lineTo(i * 48, 300 + Math.sin(i * 0.7 + t * 2) * 6); x.stroke();
  const bob = Math.sin(t * 1.5) * 5;
  x.save(); x.translate(W / 2, 300 + bob); x.rotate(Math.sin(t * 1.2) * 0.02);
  x.fillStyle = '#e8e8e8'; x.beginPath(); x.moveTo(-230, -10); x.lineTo(230, -10); x.lineTo(190, 45); x.lineTo(-200, 45); x.closePath(); x.fill();
  x.fillStyle = '#c33'; x.fillRect(-200, 25, 390, 14);
  x.fillStyle = '#f4f4f4'; x.fillRect(-80, -80, 150, 70); x.fillStyle = '#ffe680'; for (let i = 0; i < 4; i++) x.fillRect(-65 + i * 35, -65, 20, 18);
  x.fillStyle = '#ddd'; x.fillRect(100, -130, 8, 120); circle(x, 104, -135, 8, (Math.floor(t * 2) % 2) ? '#ff3030' : '#661010');
  x.restore();
  label(x, t, C.nosotros, C.barco, 'NOSOTROS: BAJAMOS HASTA VERLO', W / 2, 150, { color: '#ffffff', size: 40 });
  if (t > C.oscuridad) { const k = ss(C.oscuridad, C.oscuridad + 0.8, t); text(x, '?', W / 2, 760, 260 * k, 'rgba(95,242,255,0.25)', { glow: '#5ff2ff', glowBlur: 30 }); }
  label(x, t, C.metrosAgua, C.pista, '¿CUÁNTOS METROS HAY DEBAJO?', W / 2, 150, { color: '#ffe14d', size: 46 });
  if (t > C.pista) {
    for (let i = 0; i < 3; i++) {
      const k = (((t - C.pista) * 0.7 - i * 0.33) % 1 + 1) % 1; if (t - C.pista < i * 0.47) continue;
      x.save(); x.strokeStyle = `rgba(95,242,255,${1 - k})`; x.lineWidth = 6; glow(x, '#5ff2ff', 20);
      x.beginPath(); x.arc(W / 2, 345, 60 + k * 700, Math.PI * 0.2, Math.PI * 0.8); x.stroke(); x.restore();
    }
    label(x, t, C.pista + 0.3, C.proxima, 'LA PISTA SE ESCUCHA', W / 2, 150, { color: '#5ff2ff', size: 46 });
  }
  if (t > C.proxima) {
    const k = easeOutBack(clamp((t - C.proxima) / 0.5));
    x.fillStyle = `rgba(0,0,0,${0.55 * clamp((t - C.proxima) / 0.5)})`; x.fillRect(0, 0, W, H);
    x.save(); x.translate(W / 2, 470); x.scale(k, k);
    text(x, 'PRÓXIMA EXPEDICIÓN', 0, -80, 70, '#5ff2ff', { glow: '#5ff2ff', glowBlur: 25 });
    text(x, 'LA DUDA ANIMADA', 0, 40, 130, '#ffe14d', { stroke: 12, strokeColor: '#000', glow: '#ffb000', glowBlur: 35 });
    x.restore();
    drawCup(x, W / 2 - 560, 640, 0.5, 1, { alpha: ss(C.proxima + 0.3, C.proxima + 0.8, t) });
  }
}, { gauge: 0 });
sfx(C.duda, 'whoosh', 0.9); sfx(C.duda + 0.2, 'waves', 0.5); sfx(C.nosotros, 'pop', 0.5); sfx(C.oscuridad, 'boom', 0.5); sfx(C.metrosAgua, 'pop', 0.6);
sfx(C.pista, 'sonar', 1); sfx(C.pista + 1.43, 'sonar', 0.7); sfx(C.proxima, 'stinger', 0.9); sfx(C.proxima + 0.4, 'sparkle', 0.8);

SC.sort((a, b) => a.start - b.start);
const sceneAt = t => { let s = SC[0], i = 0; SC.forEach((c, k) => { if (t >= c.start) { s = c; i = k; } }); return [s, i]; };
SFX.push(...SC.slice(1).filter(s => !SFX.some(e => Math.abs(e.t - s.start) < 0.35 && /whoosh/.test(e.name))).map(s => ({ t: +s.start.toFixed(3), name: 'whoosh', g: 0.5 })));

// ---------- frame ----------
const canvas = createCanvas(W, H), ctx = canvas.getContext('2d');
const prev = createCanvas(W, H), pctx = prev.getContext('2d');
const XF = 0.35;
function gaugeAlpha(sc, t) { return sc.gaugeFn ? sc.gaugeFn(t) : (sc.gauge || 0); }
function renderFrame(t) {
  const [sc, i] = sceneAt(t);
  ctx.save(); ctx.globalAlpha = 1; sc.draw(ctx, t); ctx.restore();
  let ga = gaugeAlpha(sc, t);
  if (i > 0 && t - sc.start < XF) {
    const k = (t - sc.start) / XF, ps = SC[i - 1];
    pctx.save(); pctx.globalAlpha = 1; ps.draw(pctx, t); pctx.restore();
    ctx.save(); ctx.globalAlpha = 1 - ss(0, 1, k); ctx.drawImage(prev, 0, 0); ctx.restore();
    ga = lerp(gaugeAlpha(ps, t), ga, ss(0, 1, k));
  }
  drawGauge(ctx, t, ga);
  // vignette
  const vg = ctx.createRadialGradient(W / 2, H / 2, H * 0.45, W / 2, H / 2, H * 1.05); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,0.55)');
  ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
  drawSubs(ctx, t, sc.nosubs && t < C.m10000 - 0.1);
  // fade in/out
  const fade = Math.min(ss(0, 0.6, t), 1 - ss(DUR - 0.8, DUR, t));
  if (fade < 1) { ctx.fillStyle = `rgba(0,0,0,${1 - fade})`; ctx.fillRect(0, 0, W, H); }
}

// ---------- main ----------
const mode = process.argv[2];
if (mode === 'meta') {
  fs.writeFileSync(path.join(__dirname, '../work/sfx.json'), JSON.stringify({ dur: DUR, events: SFX.sort((a, b) => a.t - b.t) }, null, 1));
  console.log('DUR', DUR, 'frames', Math.ceil(DUR * FPS), 'sfx', SFX.length, 'scenes', SC.length);
} else if (mode === 'still') {
  for (const ts of process.argv.slice(3)) { renderFrame(+ts); fs.writeFileSync(path.join(__dirname, `../work/still_${ts}.png`), canvas.toBuffer('image/png')); }
} else if (mode === 'frames') {
  const a = +process.argv[3], b = +process.argv[4];
  (async () => {
    for (let f = a; f < b; f++) {
      renderFrame(f / FPS);
      const buf = ctx.getImageData(0, 0, W, H).data;
      if (!process.stdout.write(Buffer.from(buf.buffer, buf.byteOffset, buf.byteLength))) await new Promise(r => process.stdout.once('drain', r));
    }
  })();
}
module.exports = { C };
