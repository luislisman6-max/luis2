// PARTE 5 — Lo que dejas + El amanecer (final) (9:16)
require('./props_rdr.js');
init({ part: 5, from: 'capitulo 6 lo que dejas', to: 'cumpliste hasta el final somos familia', after: 455, last: true });
cues([
  ['s1', 'capitulo 6'], ['s2', 'una tarde'], ['monja', 'una monja'], ['s3', 'no sabes por que'], ['todo', 'le cuentas todo'],
  ['enfermo', 'que estas enfermo'], ['morir', 'que vas a morir'], ['miedo', 'que tienes miedo'], ['s4', 'y ella te dice'], ['tarde', 'no es tarde'],
  ['bueno', 'algo bueno'], ['s5', 'asi que lo intentas'], ['viuda', 'una viuda'], ['granja', 'en su granja'], ['devuelves', 'le devuelves dinero'],
  ['arruinaste', 'arruinaste'], ['perdon', 'le pides perdon'], ['downes', 'thomas downes'], ['liberas', 'liberas a gente'], ['presa', 'estar presa'],
  ['s6', 'no borras el pasado'], ['eliges', 'eliges'], ['s7', 'mientras tanto'], ['rompiendo', 'rompiendo por dentro'],
  ['s8', 'dutch ya no es'], ['callejon', 'aquel callejon'], ['paranoico', 'paranoico'], ['violento', 'violento'], ['perdido', 'perdido'],
  ['s9', 'y a su lado'], ['micah', 'micah bell'], ['susurra', 'le susurra'], ['escuchar', 'quiere escuchar'],
  ['s10', 'alguien le esta pasando'], ['ley', 'a la ley'], ['rata', 'es una rata'], ['sospechar', 'sospechar quien'],
  ['s11', 'entonces miras a john'], ['abigail', 'abigail'], ['jack', 'jack'], ['perdiste', 'perdiste hace mucho'],
  ['s12', 'y tomas la decision'], ['salir', 'tiene que salir de esta'], ['futuro', 'un futuro'], ['tuno', 'tu no'],
  ['s13', 'final'], ['s14', 'todo termina'], ['camino', 'viene en camino'], ['apunta', 'micah te apunta'], ['entre', 'esta dutch'],
  ['s15', 'le dices la verdad'], ['rata2', 'micah es la rata'], ['traiciono', 'traiciono a todos'],
  ['s16', 'dutch te mira'], ['miraMicah', 'mira a micah'], ['nada', 'no dice nada'], ['s17', 'simplemente se da la vuelta'], ['seva', 'y se va'],
  ['s18', 'el hombre que te saco'], ['disparar', 'ensero a disparar'.replace('ensero', 'enseno')], ['familia', 'eran familia'],
  ['s19', 'se va'], ['solo', 'te deja solo'], ['s20', 'ya no te quedan'], ['roca', 'te sientas'],
  ['s21', 'abajo'], ['ciervo', 'un ciervo'], ['sol', 'salir el sol'], ['s22', 'lo miras'], ['respiras', 'respiras'], ['vez', 'una vez mas'],
  ['s23', 'es el ultimo amanecer'], ['s24', 'arthur morgan'], ['anos', '1863 a 1899'], ['y36', 'anos'],
  ['s25', 'anos despues'], ['tumba', 'una tumba'], ['escribe', 'en ella escribe'], ['bien', 'bienaventurados'],
  ['s26', 'john sobrevive'], ['padre', 'con un padre'], ['s27', 'el oeste te va'], ['forajido', 'un forajido'], ['ladron', 'un ladron'],
  ['asesino', 'un asesino'], ['buscados', 'mas buscados'], ['s28', 'pero tu sabes'], ['plan', 'nunca tuvo un plan'],
  ['s29', 'al final de las dos'], ['verdad', 'solo una era verdad'], ['cumpliste', 'la unica que cumpliste'], ['somos', 'somos familia'],
]);
// Arthur sentado: se recorta de la cabeza a la cadera y se apoya en un banco o una roca
function seated(x, name, cx, seatY, h, o = {}) { const sh = 820; crop(x, name, 0, 60, 600, sh - 60, cx - h * 600 / (sh - 60) / 2, seatY - h, h * 600 / (sh - 60), h, o); }
function rock(x, cx, cy, s = 1) { x.save(); x.translate(cx, cy); x.scale(s, s); x.fillStyle = '#5a4a50'; x.strokeStyle = K; x.lineWidth = 6; x.beginPath(); x.moveTo(-260, 0); x.lineTo(-220, -120); x.lineTo(-60, -170); x.lineTo(160, -150); x.lineTo(260, -40); x.lineTo(250, 0); x.closePath(); x.fill(); x.stroke(); x.fillStyle = 'rgba(0,0,0,.2)'; x.beginPath(); x.moveTo(60, -160); x.lineTo(160, -150); x.lineTo(260, -40); x.lineTo(250, 0); x.lineTo(80, 0); x.closePath(); x.fill(); x.restore(); }
function mountain(x, t, k) { sunrise(x, t, k); x.fillStyle = '#3a2a34'; x.strokeStyle = K; x.lineWidth = 5; x.beginPath(); x.moveTo(0, 1350); x.quadraticCurveTo(400, 1250, 1080, 1300); x.lineTo(1080, H); x.lineTo(0, H); x.closePath(); x.fill(); x.stroke(); }

// 1 — capítulo 6
scene(0, (x, t) => { station(x, t); dim(x, .8); const k = fin(t, .1, .5); x.save(); x.globalAlpha = k; txt(x, 'CAPÍTULO 6', 540, 820, 56, { color: '#d1a646', font: 'Bebas', spacing: 10 }); txt(x, 'LO QUE DEJAS', 540, 930, 150, { color: '#f4ead2', font: 'Bebas', spacing: 6, stroke: K, sw: 10, sc: lerp(1.1, 1, k) }); x.restore(); }, { nosubs: true });
sfx(.05, 'stinger', .6);
// 2 — la estación, la monja
scene(C.s2, (x, t) => {
  station(x, t);
  seated(x, 'arthur', 360, 1520, 900); seated(x, 'monja', 760, 1520, 640, {});
  bench(x, 540, 1600, 1.3);
  label(x, t, w('monja'), 'UNA MONJA', 800, 760, { size: 52, to: [760, 900], bend: 40 });
});
sfx(C.s2, 'trainHorn', .35); sfx(w('monja'), 'pop', .7);
// 3 — le cuentas todo
scene(C.s3, (x, t) => {
  station(x, t); dim(x, .25);
  seated(x, 'arthur', 360, 1520, 900); seated(x, 'monja', 760, 1520, 640);
  bench(x, 540, 1600, 1.3);
  label(x, t, w('enfermo'), 'ESTOY ENFERMO', 540, 420, { size: 56 }); label(x, t, w('morir'), 'VOY A MORIR', 540, 560, { size: 56 }); label(x, t, w('miedo'), 'TENGO MIEDO', 540, 700, { size: 64 });
});
['enfermo', 'morir', 'miedo'].forEach(n => sfx(w(n), 'pop', .7));
// 4 — todavía no es tarde
scene(C.s4, (x, t) => {
  const g = x.createRadialGradient(540, 900, 50, 540, 900, 1200); g.addColorStop(0, '#fff4d0'); g.addColorStop(1, '#c87a4a'); x.fillStyle = g; x.fillRect(0, 0, W, H);
  embers(x, t, 40, '255,255,230');
  x.save(); x.translate(540, 1700); img(x, 'monja', 0, 0, 1350); x.restore();
  bubble(x, t, w('tarde'), 'TODAVÍA NO ES TARDE', 540, 380, { size: 62 });
  bubble(x, t, w('bueno'), 'PUEDES HACER ALGO BUENO', 540, 560, { size: 54, tail: 1 });
});
sfx(w('tarde'), 'shimmer', .6); sfx(w('bueno'), 'shimmerBig', .5);
// 5 — así que lo intentas: buenas acciones
scene(C.s5, (x, t) => {
  if (t < w('devuelves')) {
    campDay(x, t, { tents: false });
    x.strokeStyle = K; x.lineWidth = 6; x.fillStyle = '#a0683a'; x.fillRect(620, 820, 380, 360); x.strokeRect(620, 820, 380, 360);
    x.fillStyle = '#6a3a22'; x.beginPath(); x.moveTo(590, 830); x.lineTo(810, 660); x.lineTo(1030, 830); x.closePath(); x.fill(); x.stroke();
    img(x, 'arthur', 330, 1700, 1350); img(x, 'viuda', 760, 1700, 950);
    bigText(x, t, C.s5 + .05, 'LO INTENTAS', 380, { size: 140 });
    label(x, t, w('viuda'), 'UNA VIUDA', 800, 620, { size: 50 });
    if (t > w('granja')) { const k = pop(t, w('granja')); x.save(); x.translate(540, 1000); x.scale(k, k); x.fillStyle = '#3aa04a'; x.strokeStyle = K; x.lineWidth = 6; x.beginPath(); x.arc(0, 0, 70, 0, 7); x.fill(); x.stroke(); x.strokeStyle = '#fff'; x.lineWidth = 14; x.beginPath(); x.moveTo(-30, 0); x.lineTo(-6, 26); x.lineTo(34, -24); x.stroke(); x.restore(); }
  } else if (t < w('perdon')) {
    woodWall(x, .9); img(x, 'arthur', 330, 1700, 1350); img(x, 'abigail', 790, 1700, 950, {});
    const k = ss(w('devuelves'), w('devuelves') + .8, t); moneyBag(x, lerp(420, 700, k), 1100, .7);
    label(x, t, w('arruinaste'), 'LA FAMILIA QUE ARRUINASTE', 540, 420, { size: 50 });
  } else if (t < w('liberas')) {
    farmGray(x, t); img(x, 'arthur', 330, 1700, 1350); img(x, 'viuda', 790, 1700, 950);
    label(x, t, w('downes'), 'SRA. DOWNES', 800, 620, { size: 52 });
    bubble(x, t, w('perdon') + .2, 'PERDÓN', 380, 420, { size: 70 });
  } else {
    night(x, t, { mountains: false });
    x.fillStyle = '#4a4a50'; x.strokeStyle = K; x.lineWidth = 6; x.fillRect(140, 500, 800, 900); x.strokeRect(140, 500, 800, 900);
    const open = fin(t, w('liberas') + .2, .5);
    for (let i = 0; i < 8; i++) { const bx = 190 + i * 100; x.fillStyle = '#2a2a30'; x.save(); x.translate(bx, 500); x.rotate(i < 4 ? -open * .6 : open * .6); x.fillRect(-10, 0, 20, 900); x.restore(); }
    for (let i = 0; i < 3; i++) { const k = fin(t, w('presa') + i * .2, 1); img(x, 'downes', lerp(400 + i * 140, -300 + i * 1500, k), 1700, 900, { sil: '#1a1a20' }); }
    img(x, 'arthur', 830, 1720, 1300);
  }
});
sfx(C.s5 + .05, 'stinger', .4); sfx(w('granja'), 'ding', .6); sfx(w('devuelves'), 'cash', .6); sfx(w('perdon'), 'pop', .5); sfx(w('liberas'), 'jail', .7); sfx(w('presa'), 'steps', .5);
function farmGray(x, t) { campDay(x, t, { tents: false }); x.fillStyle = 'rgba(120,110,90,.35)'; x.fillRect(0, 0, W, H); x.strokeStyle = K; x.lineWidth = 6; x.fillStyle = '#8a6a4a'; x.fillRect(600, 760, 420, 440); x.strokeRect(600, 760, 420, 440); x.fillStyle = '#5a4030'; x.beginPath(); x.moveTo(570, 770); x.lineTo(810, 600); x.lineTo(1050, 770); x.closePath(); x.fill(); x.stroke(); }
// 6 — no borras el pasado, pero eliges
scene(C.s6, (x, t) => {
  woodWall(x, .7); wanted(x, t, 540, 860, 1.05, -.03, { reward: '$5,000' });
  if (t > w('eliges')) { dim(x, .55); bigText(x, t, w('eliges'), 'ELIGES', 900, { size: 240 }); }
});
sfx(w('eliges'), 'stinger', .8);
// 7 — la banda se rompe
scene(C.s7, (x, t) => {
  woodWall(x, .6);
  const crack = fin(t, w('rompiendo'), .5);
  const draw = (y) => { y.fillStyle = '#c9a46a'; y.fillRect(-170, -190, 340, 340); [['dutch', -90], ['arthur', 0], ['john', 90]].forEach(([n, dx]) => crop(y, n, 100, 80, 400, 900, dx - 90, -170, 180, 405, { filter: 'sepia(.7)' })); };
  x.save(); x.translate(-crack * 60, 0); x.rotate(-crack * .05); x.beginPath(); x.moveTo(0, 0); x.lineTo(540, 0); x.lineTo(500, 700); x.lineTo(560, 1000); x.lineTo(520, H); x.lineTo(0, H); x.clip(); polaroid(x, 540, 900, -.03, 1.9, draw, 'LA FAMILIA'); x.restore();
  x.save(); x.translate(crack * 60, 0); x.rotate(crack * .05); x.beginPath(); x.moveTo(540, 0); x.lineTo(W, 0); x.lineTo(W, H); x.lineTo(520, H); x.lineTo(560, 1000); x.lineTo(500, 700); x.clip(); polaroid(x, 540, 900, -.03, 1.9, draw, 'LA FAMILIA'); x.restore();
});
sfx(w('rompiendo'), 'rip', .8);
// 8 — Dutch ya no es el mismo
scene(C.s8, (x, t) => {
  campNight(x, t, { tents: false, fire: false }); x.fillStyle = 'rgba(90,0,0,.25)'; x.fillRect(0, 0, W, H);
  crop(x, 'dutch', 60, 100, 480, 700, -150, 520, 1380, 2013, { filter: `saturate(${1 - .6 * fin(t, w('paranoico'), 1)})` });
  stamp(x, t, w('paranoico'), 'PARANOICO', 270, 420, { size: 64 }); stamp(x, t, w('violento'), 'VIOLENTO', 800, 520, { size: 64, rot: .1 }); stamp(x, t, w('perdido'), 'PERDIDO', 300, 640, { size: 64, rot: -.05 });
}, { shake: () => w('violento') });
sfx(w('paranoico'), 'thunk'); sfx(w('violento'), 'thunk'); sfx(w('perdido'), 'thunk');
// 9 — Micah
scene(C.s9, (x, t) => {
  campNight(x, t, { fireX: 540, fireY: 1650, fireS: .7 });
  img(x, 'dutch', 360, 1700, 1250);
  const k = ss(C.s9, w('micah'), t); img(x, 'micah', lerp(1300, 760, k), 1700, 1220);
  bigText(x, t, w('micah'), 'MICAH BELL', 380, { size: 160, color: '#e8e0c8' });
  if (t > w('susurra')) for (let i = 0; i < 3; i++) { const a = fin(t, w('susurra') + i * .2, .3); x.strokeStyle = `rgba(255,255,255,${a})`; x.lineWidth = 6; x.beginPath(); x.arc(580, 560, 40 + i * 30, Math.PI * .8, Math.PI * 1.2); x.stroke(); }
});
sfx(w('micah'), 'stinger', .6); sfx(w('susurra'), 'whisper', .6);
// 10 — una rata
scene(C.s10, (x, t) => {
  woodWall(x, .6);
  [['dutch', 240, 520], ['john', 540, 520], ['micah', 840, 520], ['strauss', 390, 980], ['arthur', 690, 980]].forEach(([n, px, py], i) => {
    polaroid(x, px, py, (i % 2 ? .05 : -.05), .62, (y) => { y.fillStyle = '#8a7a5a'; y.fillRect(-170, -190, 340, 340); crop(y, n, 150, 90, 300, 330, -170, -190, 340, 374, { filter: 'sepia(.9)' }); }, '?');
  });
  if (t > w('sospechar')) { const k = fin(t, w('sospechar'), .5); x.strokeStyle = '#c8202a'; x.lineWidth = 12; x.beginPath(); x.ellipse(840, 520, 170, 200, 0, 0, 7 * k); x.stroke(); }
  const r = pop(t, w('rata')); if (r > 0) { x.save(); x.translate(540, 1180); x.scale(r, r); x.fillStyle = '#6a6a72'; x.strokeStyle = K; x.lineWidth = 6; x.beginPath(); x.ellipse(0, 0, 110, 60, 0, 0, 7); x.fill(); x.stroke(); x.beginPath(); x.ellipse(110, -20, 50, 36, .3, 0, 7); x.fill(); x.stroke(); x.beginPath(); x.arc(90, -60, 22, 0, 7); x.fill(); x.stroke(); x.fillStyle = K; x.beginPath(); x.arc(130, -26, 6, 0, 7); x.fill(); x.strokeStyle = '#d8a0a0'; x.lineWidth = 6; x.beginPath(); x.moveTo(-110, 0); x.quadraticCurveTo(-200, 40, -240, -20); x.stroke(); x.restore(); txt(x, 'RATA', 540, 1310, 90, { color: '#c8202a', font: 'Anton', stroke: K, sw: 10, sc: r }); }
});
sfx(w('ley'), 'camera', .5); sfx(w('rata'), 'squeak', .7); sfx(w('sospechar'), 'scribble', .6);
// 11 — John, Abigail y Jack
scene(C.s11, (x, t) => {
  campDay(x, t, { tents: false });
  img(x, 'john', 300, 1700, 1300);
  const a = pop(t, w('abigail')); if (a > 0) { x.save(); x.translate(640, 1700); x.scale(a, a); img(x, 'abigail', 0, 0, 1000); x.restore(); }
  const j = pop(t, w('jack')); if (j > 0) { x.save(); x.translate(900, 1720); x.scale(j, j); img(x, 'jack', 0, 0, 620); x.restore(); }
  label(x, t, w('abigail'), 'ABIGAIL', 640, 560, { size: 56 }); label(x, t, w('jack'), 'JACK', 900, 900, { size: 56 });
  if (t > w('perdiste')) { const k = pop(t, w('perdiste'), .4); heart(x, 640, 420, 1.6 * k); }
});
sfx(w('abigail'), 'pop', .8); sfx(w('jack'), 'pop', .8); sfx(w('perdiste'), 'shimmer', .5);
// 12 — la decisión
scene(C.s12, (x, t) => {
  sunset(x, t, { sunY: 1050 });
  const go = ss(w('salir'), w('tuno'), t);
  [['john', 700, 1150], ['abigail', 840, 900], ['jack', 960, 560]].forEach(([n, px, h]) => img(x, n, lerp(px, px + 600, go), 1700, h * lerp(1, .7, go)));
  img(x, 'arthur', 300, 1720, 1450);
  label(x, t, w('salir'), 'JOHN TIENE QUE SALIR', 540, 420, { size: 56 }); label(x, t, w('futuro'), 'ÉL SÍ TIENE FUTURO', 540, 560, { size: 56 });
  if (t > w('tuno')) { dim(x, .5); bigText(x, t, w('tuno'), 'TÚ NO', 900, { size: 260, color: '#c8202a' }); }
});
sfx(w('salir'), 'pop', .6); sfx(w('futuro'), 'pop', .6); sfx(w('tuno'), 'stinger', .9);
// 13 — Final: el amanecer
scene(C.s13, (x, t) => chapterCard(x, t, C.s13, 'FINAL', 'EL AMANECER'), { nosubs: true });
sfx(C.s13, 'boom', .7);
// 14 — la montaña: Micah apunta, Dutch en medio
scene(C.s14, (x, t) => {
  mountain(x, t, .15); dim(x, .2);
  const flash = Math.sin(t * 10) > 0; if (t > w('camino')) { x.fillStyle = flash ? 'rgba(220,40,40,.12)' : 'rgba(40,80,220,.12)'; x.fillRect(0, 0, W, H); label(x, t, w('camino'), 'LA LEY VIENE', 540, 420, { size: 56 }); }
  img(x, 'arthur', 220, 1720, 1300);
  img(x, 'micah', 870, 1720, 1250, { flip: true });
  if (t > w('apunta')) { x.save(); x.translate(720, 1080); x.fillStyle = '#2a2a2e'; x.strokeStyle = K; x.lineWidth = 5; x.fillRect(-120, -16, 120, 32); x.strokeRect(-120, -16, 120, 32); x.restore(); x.strokeStyle = 'rgba(255,60,60,.6)'; x.lineWidth = 3; x.setLineDash([12, 10]); x.beginPath(); x.moveTo(600, 1080); x.lineTo(280, 760); x.stroke(); x.setLineDash([]); }
  if (t > w('entre')) { const k = pop(t, w('entre')); x.save(); x.translate(540, 1720); x.scale(k, k); img(x, 'dutch', 0, 0, 1150); x.restore(); }
});
sfx(w('camino'), 'siren', .4); sfx(w('apunta'), 'gunCock', .9); sfx(w('entre'), 'stinger', .6);
// 15 — Micah es la rata
scene(C.s15, (x, t) => {
  mountain(x, t, .2); dim(x, .2);
  img(x, 'micah', 600, 1720, 1350, { flip: true });
  stamp(x, t, w('rata2'), 'LA RATA', 600, 520, { size: 110 });
  stamp(x, t, w('traiciono'), 'TRAIDOR', 600, 700, { size: 90, rot: .1 });
});
sfx(w('rata2'), 'thunk', 1.1); sfx(w('traiciono'), 'thunk');
// 16 — Dutch mira, no dice nada
scene(C.s16, (x, t) => {
  mountain(x, t, .25); dim(x, .25);
  crop(x, 'dutch', 60, 100, 480, 700, -150, 520, 1380, 2013);
  const look = t > w('miraMicah') ? 1 : -1; const ex = look * 10;
  x.fillStyle = '#1e130d'; [[448 + ex, 997], [632 + ex, 997]].forEach(([a, b]) => { x.beginPath(); x.arc(a, b, 13, 0, 7); x.fill(); });
  if (t > w('nada')) { dim(x, .4); bigText(x, t, w('nada'), '…', 520, { size: 260, color: '#fff' }); }
});
sfx(w('miraMicah'), 'tick', .6); sfx(w('nada'), 'silence', .1);
// 17 — se da la vuelta y se va
scene(C.s17, (x, t) => {
  mountain(x, t, .3);
  const k = ss(w('seva'), w('seva') + 2.5, t);
  img(x, 'dutch', lerp(540, 1300, k), 1720, 1250 * lerp(1, .8, k), { flip: true });
  img(x, 'arthur', 200, 1720, 1300);
});
sfx(w('seva'), 'steps', .6);
// 18 — recuerdos
scene(C.s18, (x, t) => {
  woodWall(x, .5); dim(x, .2);
  polaroid(x, 300, 600, -.08, .9 * Math.min(1, pop(t, C.s18)), (y) => { y.fillStyle = '#1a2340'; y.fillRect(-170, -190, 340, 340); img(y, 'dutch', -40, 150, 300, { sil: '#05060c' }); img(y, 'arthur_teen', 90, 150, 200, { sil: '#05060c' }); }, 'EL CALLEJÓN');
  polaroid(x, 780, 820, .07, .9 * Math.min(1, pop(t, w('disparar'))), (y) => { y.fillStyle = '#8aa65a'; y.fillRect(-170, -190, 340, 340); img(y, 'dutch', -50, 150, 320); img(y, 'arthur_teen', 80, 150, 220); }, 'DISPARAR');
  polaroid(x, 360, 1150, -.04, .9 * Math.min(1, pop(t, w('familia'))), (y) => { y.fillStyle = '#efe3c4'; y.fillRect(-170, -190, 340, 340); txt(y, 'SOMOS', 0, -40, 80, { color: '#2a1a0e', font: 'Bebas' }); txt(y, 'FAMILIA', 0, 50, 80, { color: '#2a1a0e', font: 'Bebas' }); }, 'LA REGLA 2');
});
sfx(C.s18, 'camera', .6); sfx(w('disparar'), 'camera', .6); sfx(w('familia'), 'camera', .6);
// 19 — te deja solo
scene(C.s19, (x, t) => { mountain(x, t, .3); img(x, 'arthur', 540, 1720, 1350); if (t > w('solo')) bigText(x, t, w('solo'), 'SOLO', 520, { size: 220, color: '#f4ead2' }); });
sfx(w('solo'), 'wind', .6);
// 20 — sin fuerzas, te sientas en la roca
scene(C.s20, (x, t) => {
  mountain(x, t, .35);
  const sit = fin(t, w('roca') - .4, .6);
  if (sit < 1) img(x, 'arthur', lerp(300, 540, sit), 1720, 1300, { rot: .08 * Math.sin(t * 3), alpha: 1 - sit });
  if (sit > 0) { x.save(); x.globalAlpha = sit; seated(x, 'arthur', 540, 1450, 950); x.restore(); }
  rock(x, 540, 1620, 1.3);
});
sfx(C.s20, 'breath', .6); sfx(w('roca') - .2, 'thud', .6);
// 21 — el valle, el ciervo, el sol
scene(C.s21, (x, t) => {
  const k = ss(C.s21, CE.sol, t); mountain(x, t, .35 + .65 * k);
  const d = fin(t, w('ciervo'), .8); deer(x, 870, 1330, .9, `rgba(30,16,24,${d})`);
  seated(x, 'arthur', 330, 1520, 820, { filter: `brightness(${.4 + .6 * k})` }); rock(x, 330, 1660, 1.1);
});
sfx(w('ciervo'), 'chime', .5); sfx(w('sol'), 'shimmerBig', .6);
// 22 — lo miras, respiras
scene(C.s22, (x, t) => {
  mountain(x, t, 1);
  crop(x, 'arthur', 60, 80, 480, 700, -150, 520, 1380, 2013, { filter: 'sepia(.2)' });
  const sun = x.createRadialGradient(540, 900, 50, 540, 900, 900); sun.addColorStop(0, 'rgba(255,230,180,.35)'); sun.addColorStop(1, 'rgba(255,230,180,0)'); x.fillStyle = sun; x.fillRect(0, 0, W, H);
});
sfx(w('respiras'), 'breath', .8); sfx(w('vez'), 'heartbeat', .5);
// 23 — el último amanecer
scene(C.s23, (x, t) => { mountain(x, t, 1); seated(x, 'arthur', 540, 1520, 900, { filter: 'brightness(.35)' }); rock(x, 540, 1660, 1.3); x.fillStyle = `rgba(255,248,230,${.8 * fin(t, C.s23 + .5, 2)})`; x.fillRect(0, 0, W, H); });
sfx(C.s23, 'shimmerDown', .6);
// 24 — Arthur Morgan 1863-1899, 36 años
scene(C.s24, (x, t) => {
  x.fillStyle = '#0b0807'; x.fillRect(0, 0, W, H);
  txt(x, 'ARTHUR MORGAN', 540, 760, 140, { color: '#f4ead2', font: 'Bebas', spacing: 10, alpha: fin(t, C.s24, .5) });
  if (t > w('anos')) txt(x, '1863 — 1899', 540, 900, 110, { color: '#d1a646', font: 'Bebas', spacing: 8, alpha: fin(t, C.anos, .5) });
  if (t > w('y36') - .5) bigText(x, t, w('y36') - .5, '36 AÑOS', 1080, { size: 150, color: '#f4ead2' });
}, { nosubs: true });
sfx(C.s24, 'bell', .7);
// 25 — la tumba y el epitafio
scene(C.s25, (x, t) => {
  mountain(x, t, .9);
  x.save(); x.translate(540, 1500); const k = pop(t, w('tumba'), .4); x.scale(k || .001, k || .001);
  x.fillStyle = '#8a8478'; x.strokeStyle = K; x.lineWidth = 7; x.beginPath(); x.moveTo(-340, 0); x.lineTo(-300, -500); x.quadraticCurveTo(0, -620, 300, -500); x.lineTo(340, 0); x.closePath(); x.fill(); x.stroke();
  x.fillStyle = '#6b4226'; x.fillRect(-24, -880, 48, 420); x.strokeRect(-24, -880, 48, 420); x.fillRect(-160, -780, 320, 44); x.strokeRect(-160, -780, 320, 44);
  txt(x, 'ARTHUR MORGAN', 0, -758, 34, { color: '#f4ead2', font: 'Bebas', spacing: 3 });
  x.fillStyle = '#9a6a3a'; rr(x, -240, -440, 480, 300, 10); x.fill(); x.stroke();
  const ep = ['BIENAVENTURADOS', 'LOS QUE TIENEN', 'HAMBRE Y SED', 'DE JUSTICIA']; const i0 = TOK.findIndex(k => k.s >= C.bien - .01);
  const tw = [TOK[i0].s, TOK[i0 + 2].s, TOK[i0 + 4].s, TOK[i0 + 7].s];
  ep.forEach((l, i) => { if (t >= tw[i]) txt(x, l, 0, -390 + i * 70, 50, { color: '#2a1a0e', font: 'Bebas', spacing: 2, alpha: fin(t, tw[i], .3) }); });
  for (let i = 0; i < 7; i++) { x.fillStyle = ['#e8485a', '#f2d27a', '#c8a0e0'][i % 3]; x.beginPath(); x.arc(-300 + i * 100, 10, 18, 0, 7); x.fill(); x.stroke(); }
  x.restore();
});
sfx(w('tumba'), 'thud', .6); sfx(w('bien'), 'shimmer', .5);
// 26 — John sobrevive, Jack crece con un padre
scene(C.s26, (x, t) => { sunset(x, t, { sunY: 1000 }); img(x, 'john', 420, 1700, 1350); img(x, 'jack', 760, 1720, 700); const k = pop(t, w('padre'), .4); if (k > 0) heart(x, 600, 560, 1.8 * k); bigText(x, t, C.s26 + .05, 'JOHN SOBREVIVE', 380, { size: 120 }); });
sfx(C.s26 + .05, 'stinger', .5); sfx(w('padre'), 'shimmer', .6);
// 27 — así te recordará el Oeste
scene(C.s27, (x, t) => {
  woodWall(x, .9); wanted(x, t, 540, 860, 1.12, -.02, { reward: '$5,000' });
  stamp(x, t, w('forajido'), 'FORAJIDO', 300, 420, { size: 70 }); stamp(x, t, w('ladron'), 'LADRÓN', 800, 700, { size: 70, rot: .1 });
  stamp(x, t, w('asesino'), 'ASESINO', 300, 1100, { size: 70, rot: -.05 }); stamp(x, t, w('buscados'), 'MÁS BUSCADO', 760, 1260, { size: 70, rot: .06 });
});
['forajido', 'ladron', 'asesino', 'buscados'].forEach(n => sfx(w(n), 'thunk'));
// 28 — Dutch nunca tuvo un plan
scene(C.s28, (x, t) => {
  woodWall(x, .7);
  x.save(); x.translate(540, 760); x.fillStyle = '#9a6a3a'; x.strokeStyle = K; x.lineWidth = 6; rr(x, -380, -240, 760, 460, 10); x.fill(); x.stroke();
  txt(x, 'PLANES DE DUTCH', 0, -160, 86, { color: '#f4ead2', font: 'Bebas', spacing: 4 });
  txt(x, 'PLANES QUE', 0, -20, 70, { color: '#f4ead2', font: 'Bebas' }); txt(x, 'FUNCIONARON:', 0, 60, 70, { color: '#f4ead2', font: 'Bebas' });
  if (t > w('plan')) txt(x, '0', 0, 160, 150, { color: '#c8202a', font: 'Anton', sc: pop(t, w('plan')) });
  x.restore();
});
sfx(w('plan'), 'thunk', 1);
// 29 — Somos familia
scene(C.s29, (x, t) => {
  notebook(x, t, [
    { s: 'DUTCH SIEMPRE TIENE UN PLAN', t: 0, strike: C.s29 + .3 },
    { s: 'SOMOS FAMILIA', t: 0, circle: w('cumpliste') },
  ], { portrait: 'dutch' });
  label(x, t, w('verdad'), 'SOLO UNA ERA VERDAD', 540, 1320, { size: 56 });
  if (t > w('somos')) { dim(x, .55); bigText(x, t, w('somos'), 'SOMOS FAMILIA', 900, { size: 170, color: '#f4ead2' }); }
});
sfx(C.s29 + .3, 'scribble', .6); sfx(w('verdad'), 'pop', .6); sfx(w('cumpliste'), 'scribble', .6); sfx(w('somos'), 'stinger', .9);

endCard(true);
run(['arthur', 'arthur_teen', 'dutch', 'john', 'micah', 'strauss', 'downes', 'monja', 'viuda', 'abigail', 'jack']);
