// PARTE 2 — La familia + Mary (9:16)
require('./props_rdr.js');
init({ part: 2, from: 'capitulo 1 la familia', to: 'esa decision el resto de tu vida', after: 99 });
cues([
  ['s1', 'capitulo 1'], ['s2', 'son dos hombres'], ['s3', 'uno es elegante'], ['bigote', 'bigote perfecto'], ['sermon', 'un sermon'],
  ['dutch', 'se llama dutch'], ['s4', 'el otro es mayor'], ['zorro', 'ojos de zorro'], ['hosea', 'se llama hosea'],
  ['s5', 'cualquier otro'], ['paliza', 'una paliza'], ['balazo', 'un balazo'], ['s6', 'ellos no'], ['rien', 'se rien'],
  ['comer', 'de comer'], ['s7', 'esa noche'], ['miedo', 'sin miedo'], ['s8', 'dutch te ensena a disparar'], ['disparar', 'disparar'],
  ['s9', 'hosea te ensena a mentir'], ['mentir', 'mentir'], ['gente', 'leer a la gente'], ['estafar', 'estafar con una sonrisa'],
  ['s10', 'y entre los dos'], ['leer', 'a leer y a escribir'], ['escribir', 'escribir'],
  ['s11', 'dutch habla de libertad'], ['libertad', 'libertad'], ['gobierno', 'gobierno corrupto'], ['ricos', 'robar a los ricos'], ['suyos', 'proteger a los suyos'],
  ['s12', 'y tu que nunca'], ['todo', 'te lo crees todo'],
  ['s13', 'y te grabas'], ['n1', 'numero 1'], ['plan', 'tiene un plan'], ['n2', 'numero 2'], ['familia', 'somos familia'],
  ['s14', 'con los anos'], ['pistoleros', 'pistoleros'], ['estafadores', 'estafadores'], ['perdida', 'gente perdida'],
  ['s15', 'y un dia'], ['flaco', 'flaco'], ['bocon', 'bocon'], ['desesperante', 'desesperante'], ['john', 'se llama john'],
  ['s16', 'te cae mal'], ['imprudente', 'imprudente'], ['terco', 'terco'], ['problemas', 'problemas'],
  ['s17', 'pero sin darte cuenta'], ['hermano', 'un hermano'], ['s18', 'recuerda ese nombre'], ['john2', 'john'], ['depender', 'depender de el'],
  ['s19', 'capitulo 2'], ['s20', 'te conviertes'], ['grande', 'grande'], ['fuerte', 'fuerte'], ['amigos', 'pocos amigos'],
  ['brazo', 'el brazo derecho'], ['sucio', 'trabajo sucio'], ['s21', 'pero hasta un forajido'], ['enamorarse', 'enamorarse'],
  ['mary', 'se llama mary'], ['buena', 'buena familia'], ['educada', 'educada'], ['preciosa', 'preciosa'], ['quiere', 'te quiere a ti'],
  ['s22', 'su papa no'], ['criminal', 'un criminal'], ['salvaje', 'un salvaje'], ['futuro', 'sin futuro'], ['razon', 'tiene razon'],
  ['s23', 'mary te lo pone'], ['ella', 'o ella'], ['banda', 'o la banda'], ['s24', 'y tu eliges'], ['eliges', 'la banda'],
  ['s25', 'vas a pensar'], ['vida', 'el resto de tu vida'],
]);

// 1 — tarjeta de capítulo sobre el callejón (enlaza con la parte 1)
scene(0, (x, t) => {
  night(x, t, { moonX: 540, moonY: 330, mountains: false }); dim(x, .55);
  img(x, 'dutch', 380, 1600, 1100, { sil: '#06040a' }); img(x, 'hosea', 720, 1600, 1060, { sil: '#06040a' });
  [[352, 610], [408, 610], [693, 618], [747, 618]].forEach(([a, b]) => { x.fillStyle = '#ffe9a0'; x.beginPath(); x.ellipse(a, b, 8, 4, 0, 0, 7); x.fill(); });
  const k = fin(t, .1, .5); x.save(); x.globalAlpha = k;
  txt(x, 'CAPÍTULO 1', 540, 420, 56, { color: '#d1a646', font: 'Bebas', spacing: 10 });
  txt(x, 'LA FAMILIA', 540, 520, 150, { color: '#f4ead2', font: 'Bebas', spacing: 6, stroke: K, sw: 10, sc: lerp(1.1, 1, k) }); x.restore();
}, { nosubs: true });
sfx(0.05, 'stinger', .8);

// 2 — los dos hombres salen de la sombra
scene(C.s2, (x, t) => {
  night(x, t, { moonX: 540, moonY: 330, mountains: false });
  const lg = x.createRadialGradient(540, 700, 20, 540, 800, 800); lg.addColorStop(0, 'rgba(255,200,120,.45)'); lg.addColorStop(1, 'rgba(255,200,120,0)'); x.fillStyle = lg; x.fillRect(0, 0, W, H);
  const k = fin(t, C.s2 + .2, .6);
  shadowEllipse(x, 330, 1640, 200); shadowEllipse(x, 760, 1640, 200);
  img(x, 'dutch', 330, 1650, 1250, { sil: '#06040a' }); img(x, 'hosea', 760, 1650, 1200, { sil: '#06040a' });
  x.save(); x.globalAlpha = k; img(x, 'dutch', 330, 1650, 1250); img(x, 'hosea', 760, 1650, 1200); x.restore();
});
sfx(C.s2 + .2, 'shimmer', .5);

// 3 — Dutch de cerca
scene(C.s3, (x, t) => {
  campNight(x, t, { tents: false, fire: false });
  crop(x, 'dutch', 60, 100, 480, 700, -150, 520, 1380, 2013);
  label(x, t, w('bigote'), 'BIGOTE PERFECTO', 800, 640, { to: [620, 1130], bend: 80 });
  if (t > w('sermon')) { const k = pop(t, w('sermon')); x.save(); x.translate(230, 600); x.scale(k, k); x.fillStyle = '#fbf6ea'; x.strokeStyle = K; x.lineWidth = 5; rr(x, -150, -60, 300, 120, 40); x.fill(); x.stroke(); [-60, 0, 60].forEach((a, i) => { x.fillStyle = K; x.beginPath(); x.arc(a, 0, 12 + 4 * Math.sin(t * 8 + i), 0, 7); x.fill(); }); x.restore(); }
  bigText(x, t, w('dutch'), 'DUTCH VAN DER LINDE', 420, { size: 110 });
});
sfx(w('bigote'), 'pop', .7); sfx(w('sermon'), 'bell', .25); sfx(w('dutch'), 'stinger', .6);

// 4 — Hosea de cerca
scene(C.s4, (x, t) => {
  campNight(x, t, { tents: false, fire: false });
  crop(x, 'hosea', 60, 100, 480, 700, -150, 520, 1380, 2013);
  label(x, t, w('zorro'), 'OJOS DE ZORRO', 300, 640, { to: [440, 960], bend: -60 });
  bigText(x, t, w('hosea'), 'HOSEA MATTHEWS', 420, { size: 120 });
});
sfx(w('zorro'), 'pop', .7); sfx(w('hosea'), 'stinger', .6);

// 5 — lo que cualquier otro habría hecho
scene(C.s5, (x, t) => {
  night(x, t, { moonX: 540, moonY: 330, mountains: false });
  shadowEllipse(x, 540, 1690, 200); img(x, 'arthur_teen', 540, 1700, 1000, { rot: Math.sin(t * 30) * (t > w('paliza') && t < w('paliza') + .3 ? .05 : 0) });
  const k1 = pop(t, w('paliza')); if (k1 > 0) { x.save(); x.translate(250, 700); x.scale(k1, k1); x.fillStyle = '#d9a07a'; x.strokeStyle = K; x.lineWidth = 7; rr(x, -90, -70, 180, 140, 40); x.fill(); x.stroke(); for (let i = 0; i < 3; i++) { x.beginPath(); x.moveTo(-60 + i * 50, -70); x.lineTo(-60 + i * 50, -10); x.stroke(); } x.restore(); stamp(x, t, w('paliza') + .05, 'PALIZA', 250, 880, { size: 60 }); }
  const k2 = pop(t, w('balazo')); if (k2 > 0) { bullet(x, 830, 760, .9 * k2, -.5); stamp(x, t, w('balazo') + .05, 'BALAZO', 830, 940, { size: 60, rot: .1 }); }
});
sfx(w('paliza'), 'punch', .9); sfx(w('balazo'), 'gunshot', .6);

// 6 — ellos se ríen y te ofrecen de comer
scene(C.s6, (x, t) => {
  campNight(x, t, { fireX: 540, fireY: 1560, fireS: .8 });
  const laugh = t > w('rien') ? Math.abs(Math.sin(t * 14)) * 10 : 0;
  img(x, 'dutch', 250, 1620 - laugh, 1150); img(x, 'hosea', 840, 1620 - laugh * .8, 1100);
  img(x, 'arthur_teen', 540, 1700, 700);
  if (t > w('rien')) { txt(x, 'JA', 250, 400 - laugh * 2, 90, { color: '#ffe08a', font: 'Anton', stroke: K, sw: 10, rot: -.2, sc: pop(t, w('rien')) }); txt(x, 'JA JA', 840, 420 - laugh * 2, 80, { color: '#ffe08a', font: 'Anton', stroke: K, sw: 10, rot: .15, sc: pop(t, w('rien') + .15) }); }
  const k = pop(t, w('comer')); if (k > 0) { x.save(); x.translate(700, 1180); x.scale(k, k); x.fillStyle = '#8a8a90'; x.strokeStyle = K; x.lineWidth = 6; x.beginPath(); x.ellipse(0, 0, 100, 30, 0, 0, Math.PI); x.lineTo(-100, 0); x.fill(); x.stroke(); x.fillStyle = '#8a4a2a'; x.beginPath(); x.ellipse(0, 0, 100, 22, 0, 0, 7); x.fill(); x.stroke(); smoke(x, t, 0, -20, .5); x.restore(); bread(x, 380, 1200, .6 * k, .2); }
});
sfx(w('rien'), 'laugh', .7); sfx(w('comer'), 'pop', .8);

// 7 — duermes sin miedo
scene(C.s7, (x, t) => {
  campNight(x, t, { fireX: 760, fireY: 1500, fireS: .9 });
  x.save(); x.translate(380, 1560); x.rotate(-Math.PI / 2); img(x, 'arthur_teen', 0, 260, 620); x.restore();
  x.fillStyle = '#8a3a3a'; x.strokeStyle = K; x.lineWidth = 6; rr(x, 140, 1470, 520, 120, 40); x.fill(); x.stroke();
  for (let i = 0; i < 3; i++) { const k = (t * .6 + i / 3) % 1; txt(x, 'Z', 300 + k * 120, 1300 - k * 240, 60 + k * 40, { color: '#fff', font: 'Anton', alpha: 1 - k, stroke: K, sw: 6 }); }
  bigText(x, t, w('miedo') - .1, 'SIN MIEDO', 450, { size: 130 });
});
sfx(C.s7, 'crackle', .4); sfx(w('miedo') - .1, 'shimmer', .5);

// 8 — Dutch te enseña a disparar
scene(C.s8, (x, t) => {
  campDay(x, t, { tents: false });
  x.fillStyle = '#8a5a30'; x.strokeStyle = K; x.lineWidth = 6; rr(x, 700, 1060, 300, 40, 6); x.fill(); x.stroke(); x.fillRect(720, 1100, 20, 140); x.fillRect(960, 1100, 20, 140);
  const b = w('disparar') + .05;
  [760, 850, 940].forEach((bx, i) => { const hit = t > b + i * .25; if (!hit) bottle(x, bx, 1062, .5); else { const k = clamp((t - b - i * .25) * 2); for (let j = 0; j < 6; j++) { x.fillStyle = '#8a5a1e'; x.beginPath(); x.arc(bx + Math.cos(j) * 120 * k, 1000 - 200 * k + 300 * k * k + j * 6, 8, 0, 7); x.fill(); } } });
  img(x, 'dutch', 220, 1650, 1150); img(x, 'arthur_teen', 470, 1700, 760);
  [0, 1, 2].forEach(i => muzzle(x, t, b + i * .25, 560, 1250, .7));
});
sfx(w('disparar') + .05, 'gunshot', .5); sfx(w('disparar') + .3, 'gunshot', .4); sfx(w('disparar') + .55, 'gunshot', .4);
sfx(w('disparar') + .1, 'glass', .6); sfx(w('disparar') + .35, 'glass', .5); sfx(w('disparar') + .6, 'glass', .5);

// 9 — Hosea te enseña a mentir
scene(C.s9, (x, t) => {
  woodWall(x, .8);
  img(x, 'hosea', 330, 1650, 1200); img(x, 'arthur_teen', 780, 1700, 800);
  label(x, t, w('mentir'), 'MENTIR', 800, 520, { size: 56 });
  label(x, t, w('gente'), 'LEER A LA GENTE', 760, 680, { size: 50 });
  label(x, t, w('estafar'), 'ESTAFAR SONRIENDO', 720, 840, { size: 50 });
  // cartas de truco
  const k = pop(t, w('mentir')); if (k > 0) [0, 1, 2].forEach(i => { x.save(); x.translate(560 + i * 40, 1150); x.rotate((i - 1) * .3 * k); x.fillStyle = '#fbf6ea'; x.strokeStyle = K; x.lineWidth = 5; rr(x, -50, -75, 100, 150, 10); x.fill(); x.stroke(); txt(x, ['A', 'K', 'Q'][i], 0, 0, 60, { color: i ? K : '#c8202a' }); x.restore(); });
});
sfx(w('mentir'), 'pop', .7); sfx(w('gente'), 'pop', .7); sfx(w('estafar'), 'pop', .7); sfx(w('mentir') + .1, 'cards', .6);

// 10 — a leer y a escribir (pizarra)
scene(C.s10, (x, t) => {
  campDay(x, t, { tents: false });
  chalkboard(x, t, [{ s: 'A B C', t: w('leer') }, { s: 'ARTHUR', t: w('escribir'), d: .6 }], 540, 640);
  img(x, 'hosea', 200, 1650, 1080); img(x, 'arthur_teen', 820, 1700, 760);
});
sfx(w('leer'), 'chalk', .7); sfx(w('escribir'), 'chalk', .7);

// 11 — el discurso de Dutch
scene(C.s11, (x, t) => {
  campNight(x, t, { fireX: 540, fireY: 1640, fireS: .8, tents: false });
  x.fillStyle = '#8a5a30'; x.strokeStyle = K; x.lineWidth = 6; x.fillRect(380, 1420, 320, 160); x.strokeRect(380, 1420, 320, 160);
  img(x, 'dutch', 540, 1430, 1150, { rot: Math.sin(t * 3) * .02 });
  bigText(x, t, w('libertad'), 'LIBERTAD', 360, { size: 170 });
  const g = pop(t, w('gobierno')); if (g > 0) { x.save(); x.translate(190, 700); x.scale(g, g); x.fillStyle = '#ece4d0'; x.strokeStyle = K; x.lineWidth = 6; x.beginPath(); x.arc(0, -40, 70, Math.PI, 0); x.fill(); x.stroke(); x.fillRect(-100, -40, 200, 120); x.strokeRect(-100, -40, 200, 120); for (let i = 0; i < 4; i++) x.strokeRect(-80 + i * 46, -30, 22, 100); x.restore(); redX(x, t, w('gobierno') + .2, 190, 700, 110); }
  const r = pop(t, w('ricos')); if (r > 0) { moneyBag(x, 890, 680, .9 * r); }
  const p2 = fin(t, w('suyos'), .5); if (p2 > 0) { x.strokeStyle = '#ffe08a'; x.lineWidth = 10; x.beginPath(); x.moveTo(820, 820); x.quadraticCurveTo(700, 980, 620, 980 * 1 + 60 * (1 - p2)); x.stroke(); heart(x, 880, 900, pop(t, w('suyos')) * 1.1); }
});
sfx(w('libertad'), 'stinger', .6); sfx(w('gobierno'), 'pop', .6); sfx(w('gobierno') + .2, 'buzz', .4); sfx(w('ricos'), 'cash', .6); sfx(w('suyos'), 'sparkle', .5);

// 12 — te lo crees todo
scene(C.s12, (x, t) => {
  campNight(x, t, { tents: false, fire: false });
  crop(x, 'arthur_teen', 60, 80, 380, 560, -60, 480, 1200, 1768);
  const k = fin(t, w('todo') - .3, .6);
  [[396, 1004], [676, 1004]].forEach(([a, b]) => { x.fillStyle = `rgba(255,240,170,${.8 * k})`; x.shadowColor = '#ffe08a'; x.shadowBlur = 40 * k; x.beginPath(); x.arc(a, b, 16 + 10 * k, 0, 7); x.fill(); x.shadowBlur = 0; });
  embers(x, t, 50, '255,230,150');
});
sfx(w('todo') - .3, 'shimmerBig', .6);

// 13 — las dos reglas (libreta)
scene(C.s13, (x, t) => {
  const plan = TOK.findIndex(k => k.s >= C.plan - .01), fam = TOK.findIndex(k => k.s >= C.familia - .01);
  notebook(x, t, [
    { s: 'DUTCH SIEMPRE TIENE UN PLAN', t: w('n1'), wt: [TOK[plan - 2].s, TOK[plan - 1].s, TOK[plan].s, TOK[plan + 1].s, TOK[plan + 2].s, TOK[plan + 2].s] },
    { s: 'SOMOS FAMILIA', t: w('n2'), wt: [TOK[fam].s, TOK[fam + 1].s] },
  ], { portrait: 'dutch' });
});
sfx(C.s13, 'paper', .7); sfx(w('n1'), 'scribbleLong', .45); sfx(w('n2'), 'scribbleLong', .45);

// 14 — la banda crece
scene(C.s14, (x, t) => {
  campDay(x, t);
  const crew = [['micah', 180, w('pistoleros')], ['john', 400, w('pistoleros') + .15], ['strauss', 640, w('estafadores')], ['hosea', 860, w('estafadores') + .15], ['downes', 300, w('perdida')], ['linton', 760, w('perdida') + .15]];
  crew.forEach(([n, cx, t0], i) => { const k = pop(t, t0); if (k <= 0) return; x.save(); x.translate(cx, 1500 + (i >= 4 ? 140 : 0)); x.scale(k, k); img(x, n, 0, 0, i >= 4 ? 900 : 1000, { sil: i >= 4 ? '#3a2a20' : undefined }); x.restore(); });
  label(x, t, w('pistoleros'), 'PISTOLEROS', 300, 420, { size: 50 });
  label(x, t, w('estafadores'), 'ESTAFADORES', 760, 360, { size: 50 });
  label(x, t, w('perdida'), 'GENTE PERDIDA', 540, 560, { size: 50 });
});
['pistoleros', 'estafadores', 'perdida'].forEach(n => { sfx(w(n), 'pop', .7); sfx(w(n) + .15, 'pop', .5); });

// 15 — Dutch trae a John
scene(C.s15, (x, t) => {
  campDay(x, t);
  img(x, 'dutch', 330, 1650, 1200); img(x, 'john_teen', 760, 1700, 800);
  stamp(x, t, w('flaco'), 'FLACO', 840, 560, { size: 60, rot: .08 });
  stamp(x, t, w('bocon'), 'BOCÓN', 840, 700, { size: 60, rot: -.06 });
  stamp(x, t, w('desesperante'), 'DESESPERANTE', 760, 840, { size: 56, rot: .05 });
  bigText(x, t, w('john'), 'JOHN MARSTON', 380, { size: 140 });
});
sfx(w('flaco'), 'thunk'); sfx(w('bocon'), 'thunk'); sfx(w('desesperante'), 'thunk'); sfx(w('john'), 'stinger', .6);

// 16 — te cae mal
scene(C.s16, (x, t) => {
  campDay(x, t, { tents: false });
  img(x, 'arthur_teen', 300, 1700, 980); img(x, 'john_teen', 790, 1700 - Math.abs(Math.sin(t * 9)) * 14, 900);
  const a = pop(t, C.s16 + .2); if (a > 0) { x.save(); x.translate(380, 700); x.scale(a, a); x.strokeStyle = '#e0242f'; x.lineWidth = 12; x.lineCap = 'round'; for (let i = 0; i < 4; i++) { x.rotate(Math.PI / 2); x.beginPath(); x.moveTo(14, 14); x.quadraticCurveTo(40, 10, 44, 40); x.stroke(); } x.restore(); }
  stamp(x, t, w('imprudente'), 'IMPRUDENTE', 760, 520, { size: 58 });
  stamp(x, t, w('terco'), 'TERCO', 760, 660, { size: 58, rot: .1 });
  stamp(x, t, w('problemas'), 'PROBLEMAS', 760, 800, { size: 58, rot: -.04 });
});
sfx(C.s16 + .2, 'anger', .6); sfx(w('imprudente'), 'thunk'); sfx(w('terco'), 'thunk'); sfx(w('problemas'), 'thunk');

// 17 — como a un hermano
scene(C.s17, (x, t) => {
  campNight(x, t, { fireX: 540, fireY: 1600, fireS: .7 });
  img(x, 'arthur_teen', 390, 1700, 950); img(x, 'john_teen', 690, 1700, 880, { flip: true });
  const k = pop(t, w('hermano'), .4); if (k > 0) heart(x, 540, 620 - (t - w('hermano')) * 20, 2.2 * k);
  bigText(x, t, w('hermano'), 'HERMANO', 400, { size: 140 });
});
sfx(w('hermano'), 'shimmer', .6);

// 18 — recuerda ese nombre
scene(C.s18, (x, t) => {
  woodWall(x, .7);
  polaroid(x, 540, 880, -.05, 1.6 * Math.min(1, pop(t, C.s18, .3)), (y) => { y.fillStyle = '#8a7a5a'; y.fillRect(-170, -190, 340, 340); crop(y, 'john', 150, 90, 300, 330, -170, -190, 340, 374, { filter: 'sepia(.8)' }); }, 'JOHN');
  if (t > w('john2')) { const k = fin(t, w('john2'), .4); x.strokeStyle = '#c8202a'; x.lineWidth = 12; x.beginPath(); x.ellipse(540, 1190, 220, 90, -.05, 0, 7 * k); x.stroke(); }
  label(x, t, w('depender'), 'RECUERDA ESTO', 540, 380, { size: 64 });
});
sfx(C.s18, 'camera', .6); sfx(w('john2'), 'scribble', .5); sfx(w('depender'), 'stinger', .6);

// 19 — capítulo 2
scene(C.s19, (x, t) => chapterCard(x, t, C.s19, 'CAPÍTULO 2', 'LO QUE PIERDES'), { nosubs: true });
sfx(C.s19, 'boom', .6);

// 20 — te conviertes en un hombre grande
scene(C.s20, (x, t) => {
  sunset(x, t, { sunY: 1050 });
  const grow = fin(t, w('grande') - .15, .3);
  if (grow < 1) img(x, 'arthur_teen', 540, 1700, lerp(1000, 1300, grow), { alpha: 1 - grow });
  shadowEllipse(x, 540, 1690, 240); x.save(); x.globalAlpha = grow; img(x, 'arthur', 540, 1700, 1450); x.restore();
  stamp(x, t, w('grande'), 'GRANDE', 230, 560, { size: 64, rot: -.1 });
  stamp(x, t, w('fuerte'), 'FUERTE', 850, 640, { size: 64, rot: .08 });
  stamp(x, t, w('amigos'), 'POCOS AMIGOS', 540, 400, { size: 70 });
  if (t > w('brazo')) { dim(x, .2); label(x, t, w('brazo'), 'EL BRAZO DERECHO', 540, 560, { size: 56 }); }
  if (t > w('sucio')) { moneyBag(x, 880, 1100, pop(t, w('sucio'))); for (let i = 0; i < 6; i++) { x.fillStyle = '#5a3a1a'; x.beginPath(); x.arc(380 + i * 50, 900 + (i % 2) * 40, 14 * pop(t, w('sucio')), 0, 7); x.fill(); } }
}, { shake: () => w('grande') });
sfx(w('grande') - .15, 'riser', .5); sfx(w('grande'), 'thunk'); sfx(w('fuerte'), 'thunk'); sfx(w('amigos'), 'thunk'); sfx(w('brazo'), 'pop', .7); sfx(w('sucio'), 'squish', .6);

// 21 — Mary
scene(C.s21, (x, t) => {
  const g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#f6c6b8'); g.addColorStop(1, '#e88a8a'); x.fillStyle = g; x.fillRect(0, 0, W, H);
  for (let i = 0; i < 14; i++) heart(x, (i * 173) % W, (H - ((t * 80 + i * 230) % (H + 200))), .8, .35);
  const k = pop(t, w('mary') - .05, .4); x.save(); x.translate(540, 1700); x.scale(k || .001, k || .001); img(x, 'mary', 0, 0, 1300); x.restore();
  bigText(x, t, w('mary'), 'MARY LINTON', 380, { size: 150, color: '#fff2f2' });
  label(x, t, w('buena'), 'BUENA FAMILIA', 230, 760, { size: 46 });
  label(x, t, w('educada'), 'EDUCADA', 860, 900, { size: 46 });
  label(x, t, w('preciosa'), 'PRECIOSA', 230, 1040, { size: 46 });
});
sfx(w('enamorarse'), 'sparkle', .6); sfx(w('mary') - .05, 'shimmer', .6); sfx(w('buena'), 'pop', .6); sfx(w('educada'), 'pop', .6); sfx(w('preciosa'), 'pop', .6);
scene(C.quiere - .05, (x, t) => {
  sunset(x, t, { sunY: 1050 });
  img(x, 'arthur', 360, 1700, 1400); img(x, 'mary', 760, 1700, 1050);
  const k = pop(t, w('quiere'), .4); if (k > 0) heart(x, 560, 640 + Math.sin(t * 4) * 10, 2.4 * k);
});
sfx(w('quiere'), 'heartbeat', .6);

// 22 — el papá de Mary
scene(C.s22, (x, t) => {
  sunset(x, t, { sunY: 1100 });
  x.fillStyle = '#ece4d4'; x.strokeStyle = K; x.lineWidth = 6; x.fillRect(420, 300, 700, 1100); x.strokeRect(420, 300, 700, 1100);
  for (let y = 340; y < 1400; y += 50) { x.strokeStyle = 'rgba(0,0,0,.15)'; x.beginPath(); x.moveTo(420, y); x.lineTo(1120, y); x.stroke(); }
  x.fillStyle = '#c99a4a'; x.strokeStyle = K; x.fillRect(560, 600, 380, 800); x.strokeRect(560, 600, 380, 800);
  img(x, 'linton', 750, 1440, 1100);
  img(x, 'arthur', 220, 1700, 1400);
  label(x, t, C.s22, 'SU PADRE', 940, 520, { size: 50, to: [800, 640], bend: 40 });
  stamp(x, t, w('criminal'), 'CRIMINAL', 760, 860, { size: 62 });
  stamp(x, t, w('salvaje'), 'SALVAJE', 760, 1000, { size: 62, rot: .1 });
  stamp(x, t, w('futuro'), 'SIN FUTURO', 760, 1140, { size: 62, rot: -.05 });
  if (t > w('razon')) { dim(x, .3 * fin(t, w('razon'), .3)); bigText(x, t, w('razon'), 'TIENE RAZÓN', 420, { size: 140 }); }
});
sfx(C.s22, 'door', .6); sfx(w('criminal'), 'thunk'); sfx(w('salvaje'), 'thunk'); sfx(w('futuro'), 'thunk'); sfx(w('razon'), 'boom', .4);

// 23 — o ella o la banda (pantalla dividida)
scene(C.s23, (x, t) => {
  x.save(); x.beginPath(); x.rect(0, 0, W / 2, H); x.clip();
  const g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#f6c6b8'); g.addColorStop(1, '#d87a7a'); x.fillStyle = g; x.fillRect(0, 0, W, H);
  img(x, 'mary', 270, 1600, 1000);
  if (t > w('eliges')) { const k = fin(t, w('eliges'), .5); dim(x, .6 * k); }
  x.restore();
  x.save(); x.beginPath(); x.rect(W / 2, 0, W / 2, H); x.clip();
  campNight(x, t, { fireX: 810, fireY: 1500, fireS: .6, tents: false });
  img(x, 'dutch', 760, 1600, 1050); img(x, 'hosea', 930, 1600, 980);
  x.restore();
  x.fillStyle = K; x.fillRect(W / 2 - 4, 0, 8, H);
  const o = pop(t, w('ella')); if (o > 0) { x.save(); x.translate(540, 820); x.scale(o, o); x.fillStyle = '#c8202a'; x.strokeStyle = K; x.lineWidth = 8; x.beginPath(); x.arc(0, 0, 90, 0, 7); x.fill(); x.stroke(); txt(x, 'O', 0, 6, 120, { color: '#fff' }); x.restore(); }
  label(x, t, w('ella'), 'ELLA', 270, 420, { size: 64 }); label(x, t, w('banda'), 'LA BANDA', 810, 420, { size: 64 });
  if (t > w('eliges')) { const k = fin(t, w('eliges'), .4); x.strokeStyle = '#ffe08a'; x.lineWidth = 14; rr(x, W / 2 + 20, 340, W / 2 - 40, 1300, 30); x.globalAlpha = k; x.stroke(); x.globalAlpha = 1; }
});
sfx(w('ella'), 'pop', .8); sfx(w('banda'), 'pop', .8); sfx(w('eliges'), 'heartbreak', .7);

// 25 — el resto de tu vida
scene(C.s25, (x, t) => {
  night(x, t, { moonX: 800, moonY: 380 });
  img(x, 'arthur', 380, 1700, 1400, { alpha: 1 });
  polaroid(x, 760, 1050, .12, .8, (y) => { y.fillStyle = '#c9b48a'; y.fillRect(-170, -190, 340, 340); crop(y, 'mary', 90, 0, 320, 620, -150, -190, 300, 580, { filter: 'sepia(1)' }); }, 'MARY');
  dim(x, .25 * fin(t, w('vida'), .8));
});
sfx(C.s25, 'wind', .4); sfx(w('vida'), 'bell', .5);

endCard(false);
run(['arthur', 'arthur_teen', 'dutch', 'hosea', 'john', 'john_teen', 'micah', 'strauss', 'downes', 'linton', 'mary']);
