// PARTE 3 — Diez dólares + Blackwater (9:16)
require('./props_rdr.js');
init({ part: 3, from: 'anos despues conoces', to: 'como siempre', after: 219 });
cues([
  ['eliza', 'llamada eliza'], ['s2', 'no es un gran romance'], ['s3', 'pero de esa relacion'], ['hijo', 'un hijo'], ['isaac', 'isaac'],
  ['s4', 'los visitas'], ['dinero', 'les llevas dinero'], ['juegas', 'juegas con el nino'], ['tevas', 'y luego te vas'], ['banda', 'con la banda'],
  ['s5', 'no es muy seguido'], ['nunca', 'nunca es suficiente'], ['s6', 'un dia'], ['granja', 'llegas a la granja'],
  ['s7', 'y lo unico que encuentras'], ['tumbas', 'dos tumbas'], ['s8', 'los asaltaron'], ['mataron', 'los mataron'],
  ['s9', 'por cuanto dinero'], ['d1', '10 dolares'], ['d2', '10 dolares'], ['s10', 'te quedas ahi parado'], ['palabra', 'una palabra'],
  ['nadie', 'se lo cuentas a nadie'], ['s11', 'capitulo 3'], ['s12', 'pasan los anos'], ['y1899', '1899'], ['cambiando', 'esta cambiando'],
  ['trenes', 'los trenes'], ['telegrafos', 'los telegrafos'], ['ciudades', 'las ciudades'], ['ley', 'la ley es cada vez'], ['fuerte', 'mas fuerte'],
  ['muriendo', 'se esta muriendo'], ['s13', 'dutch lo sabe'], ['plan', 'tiene un plan'], ['s14', 'un ultimo golpe'], ['blackwater', 'llamado blackwater'],
  ['barco', 'un barco lleno de dinero'], ['s15', 'suficiente para'], ['tierras', 'compre tierras'], ['siempre', 'para siempre'],
  ['s16', 'sale fatal'], ['s17', 'algo se descontrola'], ['disparos', 'hay disparos'], ['gritos', 'hay gritos'], ['muertos', 'hay muertos'],
  ['s18', 'mueren miembros'], ['inocentes', 'mueren inocentes'], ['s19', 'ahora todo el pais'], ['nombres', 'sus nombres'],
  ['arrestarlos', 'arrestarlos'], ['colgarlos', 'quiere colgarlos'], ['s20', 'la banda huye'], ['tormenta', 'tormenta de nieve'],
  ['caballos', 'caballos que se congelan'], ['comida', 'comida que se acaba'], ['amanecer', 'el siguiente amanecer'],
  ['s21', 'y en medio de todo eso'], ['desaparece', 'john desaparece'], ['s22', 'quien sale a buscarlo'], ['tu', 'tu'], ['claro', 'claro que tu'],
  ['s23', 'lo encuentras medio muerto'], ['lobos', 'por lobos'], ['s24', 'y lo cargas'], ['s25', 'esa noche'], ['depie', 'se pone de pie'],
  ['solo', 'solo necesito'], ['tengo', 'tengo un plan'], ['s26', 'y tu le crees'], ['como', 'como siempre'],
]);

function calendarFlip(x, t, t0, cx, cy, labels) {
  const n = Math.min(labels.length - 1, Math.floor(Math.max(0, t - t0) / .18));
  x.save(); x.translate(cx, cy); x.fillStyle = '#fbf6ea'; x.strokeStyle = K; x.lineWidth = 6; rr(x, -170, -150, 340, 300, 16); x.fill(); x.stroke();
  x.fillStyle = '#c8202a'; rr(x, -170, -150, 340, 90, 16); x.fill(); x.stroke(); txt(x, labels[n], 0, -104, 60, { color: '#fff', font: 'Bebas', spacing: 4 });
  for (let r = 0; r < 3; r++) for (let c = 0; c < 5; c++) { x.strokeStyle = 'rgba(0,0,0,.3)'; x.lineWidth = 2; x.strokeRect(-140 + c * 56, -40 + r * 56, 50, 50); }
  x.restore();
}
function train(x, t, px, py, s = 1) {
  x.save(); x.translate(px, py); x.scale(s, s); x.strokeStyle = K; x.lineWidth = 6;
  x.fillStyle = '#2a2a2e'; x.fillRect(-300, -160, 260, 160); x.strokeRect(-300, -160, 260, 160); x.fillStyle = '#3a3a42'; x.fillRect(-40, -120, 220, 120); x.strokeRect(-40, -120, 220, 120);
  x.fillStyle = '#2a2a2e'; x.fillRect(100, -230, 50, 110); x.strokeRect(100, -230, 50, 110); x.fillStyle = '#c8202a'; x.fillRect(-300, -30, 480, 30); x.strokeRect(-300, -30, 480, 30);
  x.beginPath(); x.moveTo(180, 0); x.lineTo(240, 0); x.lineTo(180, -60); x.closePath(); x.fillStyle = '#5a5a60'; x.fill(); x.stroke();
  for (const a of [-240, -120, 40, 130]) { x.fillStyle = '#5a5a60'; x.beginPath(); x.arc(a, 10, 40, 0, 7); x.fill(); x.stroke(); }
  for (let k = 0; k < 4; k++) { const kk = (t * .8 + k * .25) % 1; x.fillStyle = `rgba(230,230,230,${.7 * (1 - kk)})`; x.beginPath(); x.arc(125 - kk * 200, -250 - kk * 160, 30 + kk * 50, 0, 7); x.fill(); }
  x.restore();
}
function star(x, cx, cy, s) { x.save(); x.translate(cx, cy); x.scale(s, s); x.fillStyle = '#e8c34a'; x.strokeStyle = K; x.lineWidth = 6; x.beginPath(); for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, r = i % 2 ? 50 : 120; x.lineTo(r * Math.cos(a), r * Math.sin(a)); } x.closePath(); x.fill(); x.stroke(); for (let i = 0; i < 5; i++) { const a = -Math.PI / 2 + i * 2 * Math.PI / 5; x.beginPath(); x.arc(120 * Math.cos(a), 120 * Math.sin(a), 14, 0, 7); x.fill(); x.stroke(); } txt(x, 'LEY', 0, 6, 50, { color: '#6a4a1a' }); x.restore(); }
function farm(x, t, dusk) {
  if (dusk) sunset(x, t, { sunY: 1150, top: '#3a2a4a' }); else campDay(x, t, { tents: false });
  x.strokeStyle = K; x.lineWidth = 6; x.fillStyle = '#a0683a'; x.fillRect(620, 820, 380, 360); x.strokeRect(620, 820, 380, 360);
  x.fillStyle = '#6a3a22'; x.beginPath(); x.moveTo(590, 830); x.lineTo(810, 660); x.lineTo(1030, 830); x.closePath(); x.fill(); x.stroke();
  x.fillStyle = dusk ? '#1a1410' : '#f2d27a'; x.fillRect(700, 900, 90, 90); x.strokeRect(700, 900, 90, 90); x.fillStyle = '#4a2a14'; x.fillRect(840, 1020, 100, 160); x.strokeRect(840, 1020, 100, 160);
  x.strokeStyle = '#6a4a2a'; x.lineWidth = 8; for (let px = 0; px < 600; px += 90) { x.beginPath(); x.moveTo(px, 1120); x.lineTo(px, 1220); x.stroke(); } x.beginPath(); x.moveTo(0, 1150); x.lineTo(600, 1150); x.moveTo(0, 1195); x.lineTo(600, 1195); x.stroke();
}

// 1 — Eliza
scene(0, (x, t) => {
  woodWall(x, .9);
  x.fillStyle = '#6b4226'; x.strokeStyle = K; x.lineWidth = 6; x.fillRect(0, 1200, W, 120); x.strokeRect(-10, 1200, W + 20, 120);
  for (let i = 0; i < 4; i++) bottle(x, 120 + i * 90, 1204, .55);
  img(x, 'eliza', 620, 1700, 1250);
  bigText(x, t, .05, 'AÑOS DESPUÉS', 360, { size: 120 });
  label(x, t, w('eliza'), 'ELIZA', 860, 620, { sub: 'CAMARERA', to: [720, 700], bend: 40 });
});
sfx(.05, 'whoosh', .7); sfx(w('eliza'), 'pop', .8);
// 2 — no es un gran romance
scene(C.s2, (x, t) => {
  woodWall(x, .9); img(x, 'arthur', 340, 1700, 1400); img(x, 'eliza', 790, 1700, 1050);
  const k = pop(t, C.s2 + .2), d = fin(t, C.s2 + .8, .4); if (k > 0) heart(x, 560, 620, (1.2 - .7 * d) * k, 1 - .5 * d);
});
sfx(C.s2 + .2, 'pop', .6); sfx(C.s2 + .8, 'deflate', .5);
// 3 — Isaac
scene(C.s3, (x, t) => {
  const g = x.createRadialGradient(540, 1000, 50, 540, 1000, 1100); g.addColorStop(0, '#fff2c8'); g.addColorStop(1, '#e0a050'); x.fillStyle = g; x.fillRect(0, 0, W, H);
  embers(x, t, 40, '255,255,220');
  img(x, 'arthur', 200, 1700, 1250, { alpha: .95 }); img(x, 'eliza', 880, 1700, 950, { alpha: .95 });
  const k = pop(t, w('hijo'), .45); if (k > 0) { x.save(); x.translate(540, 1650); x.scale(k, k); img(x, 'isaac', 0, 0, 900); x.restore(); }
  bigText(x, t, w('isaac'), 'ISAAC', 420, { size: 190 });
});
sfx(w('hijo'), 'shimmerBig', .6); sfx(w('isaac'), 'stinger', .5);
// 4 — visitas
scene(C.s4, (x, t) => {
  farm(x, t, false);
  const leave = fin(t, w('tevas'), 1.2);
  img(x, 'eliza', 640, 1700, 950);
  const j = t > w('juegas') ? Math.abs(Math.sin((t - w('juegas')) * 9)) * 60 : 0;
  img(x, 'isaac', 840, 1720 - j, 600);
  if (leave < 1) img(x, 'arthur', lerp(300, -200, leave), 1700, 1350);
  const m = pop(t, w('dinero')); if (m > 0 && leave < .3) moneyBag(x, 470, 1250, .7 * m);
  if (t > w('banda')) bigText(x, t, w('banda'), 'OTRA VEZ…', 420, { size: 120 });
});
sfx(w('dinero'), 'cash', .6); sfx(w('juegas'), 'laugh', .4); sfx(w('tevas'), 'gallop', .6);
// 5 — nunca es suficiente
scene(C.s5, (x, t) => {
  woodWall(x, .7); calendarFlip(x, t, C.s5, 540, 820, ['ENERO', 'MARZO', 'MAYO', 'JULIO', 'SEPT', 'NOV', 'ENERO']);
  const k = pop(t, w('nunca')); if (k > 0) { stamp(x, t, w('nunca'), 'NUNCA ES SUFICIENTE', 540, 1200, { size: 70 }); }
});
sfx(C.s5, 'pageflip', .6); sfx(C.s5 + .5, 'pageflip', .5); sfx(w('nunca'), 'thunk');
// 6 — llegas a la granja
scene(C.s6, (x, t) => {
  farm(x, t, true); dim(x, .15);
  const k = ss(C.s6, w('granja') + .4, t);
  img(x, 'jinete', lerp(-300, 330, k), 1520 + Math.sin(t * 10) * 5 * (1 - k), 620);
  bigText(x, t, C.s6 + .4, 'MESES DESPUÉS', 380, { size: 110, color: '#f4ead2' });
});
sfx(C.s6, 'gallop', .6); sfx(w('granja'), 'wind', .5);
// 7 — dos tumbas
scene(C.s7, (x, t) => {
  const g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#4a4a58'); g.addColorStop(1, '#8a8478'); x.fillStyle = g; x.fillRect(0, 0, W, H);
  farm(x, t, true); x.fillStyle = 'rgba(40,40,60,.55)'; x.fillRect(0, 0, W, H);
  const k1 = pop(t, w('tumbas')), k2 = pop(t, w('tumbas') + .2);
  if (k1 > 0) grave(x, 380, 1420, 1.5 * k1, 'ELIZA'); if (k2 > 0) grave(x, 740, 1440, 1.1 * k2, 'ISAAC');
});
sfx(w('tumbas'), 'bell', .8);
// 8 — los asaltaron, los mataron
scene(C.s8, (x, t) => {
  x.fillStyle = '#1a0808'; x.fillRect(0, 0, W, H);
  stamp(x, t, C.s8 + .05, 'ASALTADOS', 540, 760, { size: 110 }); stamp(x, t, w('mataron'), 'ASESINADOS', 540, 1000, { size: 110, rot: .08 });
  if (t > w('mataron') && t < w('mataron') + .1) { x.fillStyle = 'rgba(200,20,30,.5)'; x.fillRect(0, 0, W, H); }
}, { shake: () => w('mataron') });
sfx(C.s8 + .05, 'thunk', 1); sfx(w('mataron'), 'gunshot', .5);
// 9 — diez dólares
scene(C.s9, (x, t) => {
  x.fillStyle = '#0d0907'; x.fillRect(0, 0, W, H);
  const sp = x.createRadialGradient(540, 900, 30, 540, 900, 600); sp.addColorStop(0, 'rgba(255,230,170,.35)'); sp.addColorStop(1, 'rgba(0,0,0,0)'); x.fillStyle = sp; x.fillRect(0, 0, W, H);
  if (t > w('d1')) { const z = t > w('d2') ? 1.35 : 1; const k = pop(t, t > w('d2') ? w('d2') : w('d1'), .3); x.save(); x.translate(540, 880); x.scale(k * z, k * z); txt(x, '$10', 0, 0, 360, { color: '#e8c34a', font: 'Anton', stroke: K, sw: 18, shadow: 30 }); x.restore(); }
  else bigText(x, t, C.s9 + .1, '¿POR CUÁNTO?', 880, { size: 140, color: '#f4ead2' });
  if (t > w('d1')) coin(x, 540, lerp(200, 1250, clamp((t - w('d1')) * 1.3)), .9, t * 9);
});
sfx(w('d1'), 'coins', .6); sfx(w('d2'), 'boom', .6);
// 10 — parado frente a dos cruces
scene(C.s10, (x, t) => {
  const g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#2a2a38'); g.addColorStop(1, '#5a5448'); x.fillStyle = g; x.fillRect(0, 0, W, H);
  x.fillStyle = '#3a3a30'; x.fillRect(0, 1250, W, H - 1250);
  grave(x, 700, 1380, 1.1, 'ELIZA'); grave(x, 920, 1400, .8, 'ISAAC');
  img(x, 'arthur', 330, 1750, 1450, { sil: '#120e10' });
  const R = rng(6); x.strokeStyle = 'rgba(180,190,220,.35)'; x.lineWidth = 2; for (let i = 0; i < 120; i++) { const rx = R() * W, ry = ((t * 900 + R() * 2000) % (H + 100)); x.beginPath(); x.moveTo(rx, ry); x.lineTo(rx - 8, ry + 40); x.stroke(); }
  if (t > w('nadie')) { const k = fin(t, w('nadie'), .4); x.save(); x.globalAlpha = k; txt(x, 'NUNCA SE LO CONTÓ', 540, 420, 90, { color: '#f4ead2', font: 'Bebas', spacing: 4 }); txt(x, 'A NADIE', 540, 520, 120, { color: '#c8202a', font: 'Bebas', spacing: 8 }); x.restore(); }
});
sfx(C.s10, 'rain', .5); sfx(w('nadie'), 'boom', .4);
// 11 — capítulo 3
scene(C.s11, (x, t) => chapterCard(x, t, C.s11, 'CAPÍTULO 3', 'BLACKWATER'), { nosubs: true });
sfx(C.s11, 'boom', .6);
// 12 — 1899, el mundo cambia
scene(C.s12, (x, t) => {
  sunset(x, t, { sunY: 1100 });
  const yr = Math.round(lerp(1885, 1899, ss(C.s12, w('y1899'), t)));
  x.save(); x.translate(540, 520); const k = t >= w('y1899') ? 1 + .15 * Math.exp(-(t - w('y1899')) * 8) : 1; x.scale(k, k); txt(x, String(yr), 0, 0, 260, { color: '#ffe08a', font: 'Bebas', stroke: K, sw: 16, shadow: 20 }); x.restore();
  if (t > w('trenes')) train(x, t, lerp(1400, -500, clamp((t - w('trenes')) / 3.5)), 1300, 1.2);
  const tg = pop(t, w('telegrafos')); if (tg > 0) for (let i = 0; i < 3; i++) { x.save(); x.translate(150 + i * 140, 1250); x.scale(tg, tg); x.fillStyle = '#5a3a20'; x.strokeStyle = K; x.lineWidth = 4; x.fillRect(-8, -400, 16, 400); x.fillRect(-60, -380, 120, 14); x.restore(); }
  const cy = pop(t, w('ciudades')); if (cy > 0) { x.save(); x.translate(830, 1250); x.scale(cy, cy); [[-150, 260], [-70, 380], [10, 300], [90, 420], [170, 280]].forEach(([a, h]) => { x.fillStyle = '#4a4a5a'; x.strokeStyle = K; x.lineWidth = 4; x.fillRect(a - 40, -h, 80, h); x.strokeRect(a - 40, -h, 80, h); }); x.restore(); }
});
sfx(w('y1899'), 'stinger', .5); sfx(w('trenes'), 'trainHorn', .5); sfx(w('telegrafos'), 'telegraph', .5); sfx(w('ciudades'), 'pop', .6);
// 13 — la ley más fuerte, el oeste muere
scene(C.ley, (x, t) => {
  sunset(x, t, { sunY: 1180, top: '#2a1a2a' });
  dim(x, .45 * fin(t, w('muriendo'), 1));
  const k = pop(t, w('fuerte'), .35); if (k > 0) star(x, 540, 700, 1.8 * k);
  if (t > w('muriendo')) { const tx = lerp(-100, 1200, clamp((t - w('muriendo')) / 2.5)); x.save(); x.translate(tx, 1380); x.rotate(t * 5); x.strokeStyle = '#8a6a3a'; x.lineWidth = 5; for (let i = 0; i < 10; i++) { x.beginPath(); x.arc(0, 0, 30 + i * 4, i, i + 3); x.stroke(); } x.restore(); }
});
sfx(w('fuerte'), 'thunk', 1); sfx(w('muriendo'), 'wind', .6);
// 14 — Dutch tiene un plan
scene(C.s13, (x, t) => {
  woodWall(x, .7);
  x.save(); x.translate(540, 620); x.strokeStyle = '#d8ccb0'; x.lineWidth = 4; x.beginPath(); x.moveTo(-160, -200); x.lineTo(0, -260); x.lineTo(160, -200); x.stroke();
  x.fillStyle = '#9a6a3a'; x.strokeStyle = K; x.lineWidth = 6; rr(x, -330, -200, 660, 380, 10); x.fill(); x.stroke(); for (let i = 1; i < 3; i++) { x.beginPath(); x.moveTo(-330, -200 + i * 127); x.lineTo(330, -200 + i * 127); x.stroke(); }
  txt(x, 'PLANES DE DUTCH', 0, -136, 76, { color: '#f4ead2', font: 'Bebas', spacing: 4 });
  const n = t > w('plan') ? 1 : 0; txt(x, n ? 'PLAN Nº 1.000' : '…', 0, -8, 70, { color: '#f4ead2', font: 'Bebas', sc: n ? pop(t, w('plan')) : 1 });
  txt(x, 'PLANES QUE FUNCIONARON: 0', 0, 116, 50, { color: '#f4ead2', font: 'Bebas' }); x.restore();
  img(x, 'dutch', 540, 1720, 900);
});
sfx(w('plan'), 'pop', .8);
// 15 — Blackwater: el barco del dinero
scene(C.s14, (x, t) => {
  sunset(x, t, { sunY: 900 }); water(x, t, 1150, '#3a4a6a');
  ferry(x, t, 560, 1180, 1.05);
  bigText(x, t, w('blackwater'), 'BLACKWATER', 360, { size: 170 });
  const k = pop(t, w('barco')); if (k > 0) [380, 560, 740].forEach((bx, i) => moneyBag(x, bx, 890 - i % 2 * 20, .55 * pop(t, w('barco') + i * .1)));
});
sfx(w('blackwater'), 'stinger', .6); sfx(w('barco'), 'cash', .6); sfx(C.s14, 'waves', .4);
// 16 — el sueño de retirarse
scene(C.s15, (x, t) => {
  campDay(x, t, { tents: false });
  const fade = fin(t, w('siempre'), .6);
  x.save(); x.globalAlpha = 1 - fade;
  const k = pop(t, w('tierras')); if (k > 0) { x.save(); x.translate(540, 1150); x.scale(k, k); x.fillStyle = '#a0683a'; x.strokeStyle = K; x.lineWidth = 6; x.fillRect(-180, -200, 360, 200); x.strokeRect(-180, -200, 360, 200); x.fillStyle = '#6a3a22'; x.beginPath(); x.moveTo(-210, -190); x.lineTo(0, -350); x.lineTo(210, -190); x.closePath(); x.fill(); x.stroke(); x.restore(); }
  img(x, 'dutch', 220, 1700, 1000); img(x, 'arthur', 450, 1700, 1080); img(x, 'hosea', 680, 1700, 980); img(x, 'john', 880, 1700, 1040);
  x.restore();
  bigText(x, t, C.s15 + .1, 'RETIRARSE', 420, { size: 150 });
});
sfx(w('tierras'), 'pop', .7); sfx(w('siempre'), 'shimmerDown', .6);
// 17 — sale fatal
scene(C.s16, (x, t) => { x.fillStyle = '#c8202a'; x.fillRect(0, 0, W, H); stamp(x, t, C.s16, 'SALE FATAL', 540, 900, { size: 160, color: '#fff' }); }, { shake: () => C.s16, nosubs: true });
sfx(C.s16, 'stinger', 1);
// 18 — disparos, gritos, muertos
scene(C.s17, (x, t) => {
  night(x, t, { moonX: 860, moonY: 300, mountains: false }); water(x, t, 1250, '#14203a');
  ferry(x, t, 540, 1260, 1.05); dim(x, .3);
  const R = rng(31); for (let i = 0; i < 14; i++) { const tt = w('disparos') + R() * 3.2; muzzle(x, t, tt, 200 + R() * 680, 900 + R() * 300, .5 + R() * .4); }
  [['DISPAROS', w('disparos'), 420], ['GRITOS', w('gritos'), 560], ['MUERTOS', w('muertos'), 700]].forEach(([s, t0, y]) => { const k = pop(t, t0); if (k > 0) { x.save(); x.translate(540, y); x.scale(k, k); txt(x, s, 0, 0, 120, { color: '#ffe08a', font: 'Anton', stroke: K, sw: 12 }); x.restore(); } });
}, { shake: () => w('disparos') });
sfx(w('disparos'), 'gunfight', .8); sfx(w('gritos'), 'scream', .4); sfx(w('muertos'), 'boom', .6);
// 19 — mueren miembros e inocentes
scene(C.s18, (x, t) => {
  const g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#2a1a1a'); g.addColorStop(1, '#5a3a2a'); x.fillStyle = g; x.fillRect(0, 0, W, H);
  x.fillStyle = '#3a2a1a'; x.fillRect(0, 1300, W, H - 1300);
  for (let i = 0; i < 6; i++) { const t0 = (i < 3 ? C.s18 : w('inocentes')) + (i % 3) * .15; const k = pop(t, t0); if (k > 0) grave(x, 150 + i * 156, 1420 + (i % 2) * 40, .75 * k); }
  label(x, t, C.s18 + .1, 'LA BANDA', 300, 700, { size: 56 }); label(x, t, w('inocentes'), 'INOCENTES', 780, 760, { size: 56 });
});
sfx(C.s18 + .1, 'bell', .5); sfx(w('inocentes'), 'bell', .5);
// 20 — todos saben sus nombres
scene(C.s19, (x, t) => {
  woodWall(x, .9);
  [['dutch', 'DUTCH', 290, 560, -.06], ['arthur', 'ARTHUR', 790, 600, .05], ['hosea', 'HOSEA', 290, 1180, .04], ['john', 'JOHN', 790, 1200, -.05]].forEach(([who, nm, cx, cy, r], i) => {
    const k = pop(t, C.s19 + .15 + i * .18); if (k > 0) wanted(x, t, cx, cy, .62 * k, r, { who, name: nm, reward: '$ ????' });
  });
  if (t > w('arrestarlos')) { dim(x, .5); stamp(x, t, w('arrestarlos'), 'ARRESTARLOS', 540, 760, { size: 90 }); redX(x, t, w('arrestarlos') + .25, 540, 760, 200); }
  if (t > w('colgarlos')) { dim(x, .4); stamp(x, t, w('colgarlos'), 'COLGARLOS', 540, 1060, { size: 120 }); }
});
[0, 1, 2, 3].forEach(i => sfx(C.s19 + .15 + i * .18, 'thunk', .7)); sfx(w('arrestarlos') + .25, 'buzz', .5); sfx(w('colgarlos'), 'boom', .7);
// 21 — huyen a la nieve
scene(C.s20, (x, t) => {
  snow(x, t, { storm: t > w('tormenta') });
  for (let i = 0; i < 4; i++) { const px = ((t - C.s20) * 70 + i * 260) % 1400 - 200; img(x, 'jinete', px, 1350 + (i % 2) * 30, 360, { sil: '#2a3040' }); }
  bigText(x, t, w('tormenta'), 'TORMENTA', 420, { size: 160, color: '#eef4ff' });
});
sfx(C.s20, 'gallop', .5); sfx(w('tormenta'), 'blizzard', .7);
// 22 — caballos, comida, amanecer
scene(C.caballos, (x, t) => {
  snow(x, t, { storm: true, night: true });
  campfire(x, t, 540, 1600, .5);
  [['CABALLOS CONGELADOS', w('caballos'), 460], ['SIN COMIDA', w('comida'), 620], ['¿VERÁN EL AMANECER?', w('amanecer'), 780]].forEach(([s, t0, y]) => label(x, t, t0, s, 540, y, { size: 54 }));
  img(x, 'hosea', 330, 1620, 900, { sil: '#1a2030' }); img(x, 'dutch', 760, 1620, 950, { sil: '#1a2030' });
});
sfx(w('caballos'), 'pop', .6); sfx(w('comida'), 'pop', .6); sfx(w('amanecer'), 'pop', .6);
// 23 — John desaparece
scene(C.s21, (x, t) => {
  snow(x, t, { storm: true });
  for (let i = 0; i < 9; i++) { const k = fin(t, C.s21 + i * .12, .1); x.fillStyle = `rgba(120,130,150,${.6 * k})`; x.beginPath(); x.ellipse(300 + i * 70 + (i % 2) * 20, 1700 - i * 50, 14, 22, .3, 0, 7); x.fill(); }
  label(x, t, w('desaparece'), '¿JOHN?', 760, 1100, { size: 70, to: [880, 1300], bend: 60 });
});
sfx(C.s21, 'steps', .5); sfx(w('desaparece'), 'pop', .7);
// 24 — ¿quién sale a buscarlo? tú
scene(C.s22, (x, t) => {
  snow(x, t, { storm: true });
  img(x, 'arthur', 540, 1750, 1500);
  if (t > w('tu')) bigText(x, t, w('tu'), 'TÚ', 500, { size: 300 });
});
sfx(w('tu'), 'stinger', .7);
// 25 — medio muerto, lobos
scene(C.s23, (x, t) => {
  snow(x, t, { night: true });
  x.save(); x.translate(540, 1280); x.rotate(-Math.PI / 2); img(x, 'john', 0, 300, 640); x.restore();
  const k = fin(t, w('lobos') - .2, .5);
  wolf(x, 170, 1330, 1.2, false, k); wolf(x, 930, 1300, 1.1, true, k); wolf(x, 800, 1080, .7, true, k);
  label(x, t, C.s23 + .2, 'MEDIO MUERTO', 540, 520, { size: 60 });
});
sfx(w('lobos') - .2, 'growl', .7); sfx(w('lobos') + .3, 'howl', .5);
// 26 — lo cargas de vuelta
scene(C.s24, (x, t) => {
  snow(x, t, {});
  const k = ss(C.s24, C.s25, t);
  x.save(); x.translate(lerp(220, 760, k), 0);
  x.save(); x.translate(0, 820); x.rotate(-Math.PI / 2 + .1); img(x, 'john', 0, 160, 620); x.restore();
  img(x, 'arthur', 0, 1750 + Math.abs(Math.sin(t * 6)) * 10, 1350); x.restore();
});
sfx(C.s24, 'snowSteps', .6);
// 27 — el discurso de Dutch en la fogata
scene(C.s25, (x, t) => {
  campNight(x, t, { fireX: 540, fireY: 1660, fireS: .8 });
  img(x, 'dutch', 540, 1560 - (t > w('depie') ? 0 : 60), 1250);
  bubble(x, t, w('solo'), 'SOLO UN POCO MÁS DE DINERO…', 540, 400, { size: 50 });
  bubble(x, t, w('tengo'), '¡TENGO UN PLAN!', 540, 560, { size: 66 });
});
sfx(w('depie'), 'whoosh', .5); sfx(w('solo'), 'pop', .6); sfx(w('tengo'), 'pop', .8);
// 28 — y tú le crees
scene(C.s26, (x, t) => {
  campNight(x, t, { tents: false, fire: false });
  crop(x, 'arthur', 60, 80, 480, 700, -150, 520, 1380, 2013);
  if (t > w('como')) bigText(x, t, w('como'), 'COMO SIEMPRE', 420, { size: 140 });
});
sfx(w('como'), 'bell', .4);

endCard(false);
run(['arthur', 'dutch', 'hosea', 'john', 'eliza', 'isaac', 'jinete']);
