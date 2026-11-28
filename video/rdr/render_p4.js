// PARTE 4 — La deuda + La tos (9:16)
require('./props_rdr.js');
init({ part: 4, from: 'capitulo 4 la deuda', to: 'de verdad lo tiene', after: 331 });
cues([
  ['s1', 'capitulo 4'], ['s2', 'para sobrevivir'], ['rapido', 'dinero rapido'], ['strauss', 'llamado strauss'], ['idea', 'una idea'],
  ['prestar', 'prestar dinero'], ['cobrar', 'a cobrar'], ['s3', 'tu eres el grande'], ['asusta', 'el que asusta'], ['preguntas', 'no hace preguntas'],
  ['s4', 'una de esas deudas'], ['downes', 'thomas downes'], ['palido', 'palido'], ['flaco', 'flaco'], ['temblando', 'temblando'],
  ['nodinero', 'no tiene el dinero'], ['enfermo', 'esta enfermo'], ['s5', 'no te importa'], ['trabajo', 'es trabajo'], ['golpeas', 'lo golpeas'],
  ['s6', 'y mientras esta en el suelo'], ['tose', 'te tose'], ['s7', 'te limpias'], ['caballo', 'a tu caballo'], ['tevas', 'y te vas'],
  ['s8', 'ese dia no te das cuenta'], ['ahi', 'pero ahi'], ['granja', 'en esa granja'], ['dolares', 'unos cuantos dolares'], ['final', 'empieza tu final'],
  ['s9', 'capitulo 5'], ['s10', 'la banda llega'], ['edificios', 'edificios enormes'], ['luces', 'luces'], ['tranvias', 'tranvias'], ['elegante', 'gente elegante'],
  ['denis', 'saint denis'], ['s11', 'y dutch tiene otro plan'], ['grande', 'el mas grande'], ['banco', 'robar el banco'],
  ['s12', 'sale peor'], ['policia', 'la policia'], ['vendio', 'alguien los vendio'], ['s13', 'y ahi'], ['hosea', 'matan a hosea'],
  ['zorro', 'ojos de zorro'], ['leer', 'te enseno a leer'], ['pensar', 'te enseno a pensar'],
  ['s14', 'huyen como pueden'], ['barco', 'en un barco'], ['naufraga', 'el barco naufraga'], ['isla', 'isla tropical'], ['revolucion', 'una revolucion'],
  ['guerra', 'una guerra ajena'], ['s15', 'cuando por fin vuelven'], ['seva', 'ya no se va'], ['pequeno', 'algo pequeno'], ['sangre', 'sangre'],
  ['aire', 'te falta el aire'], ['colina', 'una colina'], ['s16', 'vas a un doctor'], ['revisa', 'te revisa'], ['palabra', 'una sola palabra'],
  ['tb', 'tuberculosis'], ['cura', 'no hay cura'], ['medicina', 'no hay medicina'], ['meses', 'te quedan meses'],
  ['s17', 'y la enfermedad'], ['regalo', 'te la regalo'], ['s18', 'esa noche abres'], ['uno', 'numero uno'], ['plan', 'tiene un plan'],
  ['primera', 'por primera vez'], ['tiene', 'de verdad lo tiene'],
]);
function cough(x, t, t0, cx, cy) { if (t < t0) return; const R = rng(8); for (let i = 0; i < 16; i++) { const k = clamp((t - t0) * 1.6 - i * .02); if (k <= 0 || k >= 1) continue; const a = -0.5 + R() * 1.0, sp = 140 + R() * 220; x.fillStyle = `rgba(190,20,30,${1 - k})`; x.beginPath(); x.arc(cx + Math.cos(a) * sp * k, cy + Math.sin(a) * sp * k + 180 * k * k, 5 + R() * 7, 0, 7); x.fill(); } }

// 1 — capítulo 4
scene(0, (x, t) => {
  woodWall(x, .5); dim(x, .3);
  for (let i = 0; i < 9; i++) coin(x, 120 + i * 105, 400 + ((t * 300 + i * 140) % 1300), .8, t * 6 + i);
  const k = fin(t, .1, .5); x.save(); x.globalAlpha = k;
  txt(x, 'CAPÍTULO 4', 540, 860, 56, { color: '#d1a646', font: 'Bebas', spacing: 10 });
  txt(x, 'LA DEUDA', 540, 970, 170, { color: '#f4ead2', font: 'Bebas', spacing: 6, stroke: K, sw: 10, sc: lerp(1.1, 1, k) }); x.restore();
}, { nosubs: true });
sfx(.05, 'stinger', .7); sfx(.2, 'coins', .4);
// 2 — Strauss y su idea
scene(C.s2, (x, t) => {
  campNight(x, t, { tents: false, fire: false });
  tent(x, 540, 1350, 2.4, true);
  x.fillStyle = '#6b4226'; x.strokeStyle = K; x.lineWidth = 6; x.fillRect(560, 1180, 380, 30); x.strokeRect(560, 1180, 380, 30);
  img(x, 'strauss', 380, 1660, 1150);
  label(x, t, w('strauss'), 'STRAUSS', 760, 560, { sub: 'PRESTAMISTA', to: [480, 640], bend: -40 });
  const k = pop(t, w('idea')); if (k > 0) { x.save(); x.translate(380, 360); x.scale(k, k); x.fillStyle = '#ffe08a'; x.strokeStyle = K; x.lineWidth = 6; x.beginPath(); x.arc(0, 0, 60, 0, 7); x.fill(); x.stroke(); x.fillStyle = '#9a9a9a'; x.fillRect(-26, 56, 52, 36); x.strokeRect(-26, 56, 52, 36); x.restore(); }
  if (t > w('prestar')) moneyBag(x, 820, 1100, .8 * pop(t, w('prestar')));
  if (t > w('cobrar')) { const k2 = fin(t, w('cobrar'), .4); x.strokeStyle = '#ffe08a'; x.lineWidth = 10; x.beginPath(); x.moveTo(820, 1000); x.lineTo(820 - 300 * k2, 900); x.stroke(); stamp(x, t, w('cobrar'), 'A COBRAR', 720, 820, { size: 64 }); }
});
sfx(w('strauss'), 'pop', .8); sfx(w('idea'), 'ding', .6); sfx(w('prestar'), 'cash', .6); sfx(w('cobrar'), 'thunk');
// 3 — tú eres el grande
scene(C.s3, (x, t) => {
  sunset(x, t, { sunY: 1150, top: '#2a1a2a' }); dim(x, .2);
  crop(x, 'arthur', 0, 60, 600, 900, -360, 300, 1800, 2700);
  stamp(x, t, C.s3 + .1, 'EL GRANDE', 540, 380, { size: 90 });
  stamp(x, t, w('asusta'), 'EL QUE ASUSTA', 540, 1180, { size: 72, rot: .06 });
  stamp(x, t, w('preguntas'), 'SIN PREGUNTAS', 540, 1320, { size: 72, rot: -.05 });
});
sfx(C.s3 + .1, 'thunk'); sfx(w('asusta'), 'thunk'); sfx(w('preguntas'), 'thunk');
// 4 — Thomas Downes
scene(C.s4, (x, t) => {
  campDay(x, t, { tents: false }); x.fillStyle = 'rgba(120,110,90,.35)'; x.fillRect(0, 0, W, H);
  x.strokeStyle = K; x.lineWidth = 6; x.fillStyle = '#8a6a4a'; x.fillRect(600, 760, 420, 440); x.strokeRect(600, 760, 420, 440);
  x.fillStyle = '#5a4030'; x.beginPath(); x.moveTo(570, 770); x.lineTo(810, 600); x.lineTo(1050, 770); x.closePath(); x.fill(); x.stroke();
  const shake = t > w('temblando') ? Math.sin(t * 60) * 4 : 0;
  img(x, 'downes', 430 + shake, 1700, 1300);
  bigText(x, t, w('downes'), 'THOMAS DOWNES', 360, { size: 130 });
  label(x, t, w('palido'), 'PÁLIDO', 820, 620, { size: 50 }); label(x, t, w('flaco'), 'FLACO', 860, 760, { size: 50 }); label(x, t, w('temblando'), 'TEMBLANDO', 820, 900, { size: 50 });
  if (t > w('nodinero')) { dim(x, .25); bubble(x, t, w('nodinero'), 'NO TENGO EL DINERO…', 600, 560, { size: 50 }); }
  bubble(x, t, w('enfermo'), 'ESTOY ENFERMO', 600, 720, { size: 56 });
});
sfx(w('downes'), 'stinger', .5); sfx(w('palido'), 'pop', .6); sfx(w('flaco'), 'pop', .6); sfx(w('temblando'), 'pop', .6); sfx(w('nodinero'), 'pop', .6); sfx(w('enfermo'), 'cough', .4);
// 5 — no te importa, lo golpeas
scene(C.s5, (x, t) => {
  campDay(x, t, { tents: false }); x.fillStyle = 'rgba(120,110,90,.35)'; x.fillRect(0, 0, W, H);
  const hit = w('golpeas'); const fall = fin(t, hit, .3);
  img(x, 'arthur', 340, 1720, 1400);
  x.save(); x.translate(790, 1720); x.rotate(fall * 1.2); img(x, 'downes', 0, 0, 1250); x.restore();
  stamp(x, t, w('trabajo'), 'ES TRABAJO', 540, 420, { size: 90 });
  if (t > hit && t < hit + .06) { x.fillStyle = 'rgba(255,255,255,.3)'; x.fillRect(0, 0, W, H); }
  if (t > hit) txt(x, '¡PAM!', 760, 700, 150, { color: '#ffe08a', font: 'Anton', stroke: K, sw: 14, rot: .2, sc: pop(t, hit), alpha: 1 - fin(t, hit + .8, .3) });
}, { shake: () => w('golpeas') });
sfx(w('trabajo'), 'thunk'); sfx(w('golpeas'), 'punch', 1);
// 6 — te tose en la cara (cámara lenta)
scene(C.s6, (x, t) => {
  x.fillStyle = '#2a2418'; x.fillRect(0, 0, W, H);
  x.save(); x.translate(540, 1250); x.rotate(-Math.PI / 2 + .2); crop(x, 'downes', 150, 150, 300, 300, -300, -300, 600, 600); x.restore();
  crop(x, 'arthur', 150, 100, 300, 330, 380, 200, 700, 770, { alpha: .95 });
  const c0 = w('tose'); if (t > c0) { const k = clamp((t - c0) / 1.2); for (let i = 0; i < 40; i++) { const R = rng(i + 1); const a = -1.1 + R() * .6; const d = k * (300 + R() * 500); x.fillStyle = `rgba(160,180,140,${.5 * (1 - k)})`; x.beginPath(); x.arc(560 + Math.cos(a) * d, 1150 + Math.sin(a) * d, 10 + R() * 30 * k, 0, 7); x.fill(); } }
  bigText(x, t, c0, 'COF COF', 380, { size: 120, color: '#cfe0b0' });
});
sfx(w('tose'), 'cough', 1);
// 7 — te limpias y te vas
scene(C.s7, (x, t) => {
  farm(x, t); const k = ss(w('caballo'), w('tevas') + 1.2, t);
  img(x, 'jinete', lerp(380, 1300, k), 1600 + Math.sin(t * 10) * 6 * (k > 0 ? 1 : 0), 760);
  img(x, 'downes', 900, 1700, 500, { alpha: 1 - k, rot: 1.2 });
});
sfx(C.s7, 'wipe', .5); sfx(w('caballo'), 'horse', .5); sfx(w('tevas'), 'gallop', .6);
function farm(x, t) {
  campDay(x, t, { tents: false }); x.fillStyle = 'rgba(120,110,90,.35)'; x.fillRect(0, 0, W, H);
  x.strokeStyle = K; x.lineWidth = 6; x.fillStyle = '#8a6a4a'; x.fillRect(600, 760, 420, 440); x.strokeRect(600, 760, 420, 440);
  x.fillStyle = '#5a4030'; x.beginPath(); x.moveTo(570, 770); x.lineTo(810, 600); x.lineTo(1050, 770); x.closePath(); x.fill(); x.stroke();
}
// 8 — ahí empieza tu final
scene(C.s8, (x, t) => {
  farm(x, t); const d = fin(t, w('final'), .8); dim(x, .3 + .6 * d);
  if (t > w('ahi')) { const k = fin(t, w('ahi'), .5); x.strokeStyle = '#c8202a'; x.lineWidth = 12; x.beginPath(); x.ellipse(810, 900, 300, 260, 0, 0, 7 * k); x.stroke(); }
  label(x, t, w('dolares'), 'POR UNOS DÓLARES', 540, 420, { size: 60 });
  bigText(x, t, w('final'), 'EMPIEZA TU FINAL', 1000, { size: 130, color: '#c8202a' });
});
sfx(w('ahi'), 'scribble', .5); sfx(w('dolares'), 'pop', .6); sfx(w('final'), 'stinger', .9);
// 9 — capítulo 5
scene(C.s9, (x, t) => chapterCard(x, t, C.s9, 'CAPÍTULO 5', 'LA TOS'), { nosubs: true });
sfx(C.s9, 'cough', .5);
// 10 — Saint Denis
scene(C.s10, (x, t) => {
  city(x, t);
  if (t > w('tranvias')) { const k = clamp((t - w('tranvias')) / 3); x.save(); x.translate(lerp(-300, 1300, k), 1420); x.fillStyle = '#3a6a4a'; x.strokeStyle = K; x.lineWidth = 6; rr(x, -200, -160, 400, 160, 14); x.fill(); x.stroke(); for (let i = 0; i < 4; i++) { x.fillStyle = '#ffd88a'; x.fillRect(-170 + i * 90, -130, 60, 60); } x.restore(); }
  label(x, t, w('edificios'), 'EDIFICIOS ENORMES', 540, 400, { size: 52 }); label(x, t, w('luces'), 'LUCES', 260, 560, { size: 52 });
  label(x, t, w('tranvias'), 'TRANVÍAS', 820, 560, { size: 52 }); label(x, t, w('elegante'), 'GENTE ELEGANTE', 540, 720, { size: 52 });
  bigText(x, t, w('denis'), 'SAINT DENIS', 1000, { size: 160 });
});
sfx(C.s10, 'city', .5); ['edificios', 'luces', 'tranvias', 'elegante'].forEach(n => sfx(w(n), 'pop', .6)); sfx(w('tranvias'), 'tramBell', .5); sfx(w('denis'), 'stinger', .6);
// 11 — robar el banco
scene(C.s11, (x, t) => {
  night(x, t, { mountains: false }); bankFront(x, t); dim(x, .25);
  img(x, 'dutch', 300, 1720, 1150); img(x, 'arthur', 760, 1720, 1250);
  stamp(x, t, w('banco'), 'EL GOLPE MÁS GRANDE', 540, 1000, { size: 72 });
});
sfx(w('grande'), 'riser', .5); sfx(w('banco'), 'thunk');
// 12 — sale peor: la policía
scene(C.s12, (x, t) => {
  night(x, t, { mountains: false }); bankFront(x, t); dim(x, .35);
  const flash = Math.sin(t * 12) > 0; x.fillStyle = flash ? 'rgba(220,40,40,.18)' : 'rgba(40,80,220,.18)'; x.fillRect(0, 0, W, H);
  for (let i = 0; i < 6; i++) { const k = pop(t, w('policia') + i * .08); if (k > 0) { x.save(); x.translate(110 + i * 172, 1700); x.scale(k, k); img(x, 'linton', 0, 0, 950, { sil: '#0a0a18' }); x.restore(); } }
  bigText(x, t, C.s12 + .1, 'PEOR QUE BLACKWATER', 420, { size: 100 });
  stamp(x, t, w('vendio'), 'ALGUIEN LOS VENDIÓ', 540, 640, { size: 70 });
});
sfx(C.s12 + .1, 'stinger', .6); sfx(w('policia'), 'whistle', .6); sfx(w('vendio'), 'thunk');
// 13 — matan a Hosea
scene(C.s13, (x, t) => {
  night(x, t, { mountains: false }); x.fillStyle = '#1a1418'; x.fillRect(0, 1300, W, H - 1300);
  const sh = w('hosea'); const fall = fin(t, sh + .1, .6);
  if (t < sh + .1) img(x, 'hosea', 540, 1700, 1300);
  else { x.save(); x.translate(540, 1700); x.rotate(fall * -1.4); img(x, 'hosea', 0, 0, 1300, { alpha: 1 - .3 * fall }); x.restore(); }
  muzzle(x, t, sh, 1000, 900, 1);
  if (t > sh + .9) { dim(x, .55); polaroid(x, 540, 900, -.04, 1.4, (y) => { y.fillStyle = '#8a7a5a'; y.fillRect(-170, -190, 340, 340); crop(y, 'hosea', 150, 90, 300, 330, -170, -190, 340, 374, { filter: 'sepia(1)' }); }, 'HOSEA'); }
  label(x, t, w('leer'), 'TE ENSEÑÓ A LEER', 540, 380, { size: 52 });
  label(x, t, w('pensar'), 'Y A PENSAR', 540, 500, { size: 52 });
}, { shake: () => w('hosea') });
sfx(w('hosea'), 'gunshot', 1); sfx(w('hosea') + .9, 'bell', .6);
// 14 — barco, naufragio, isla
scene(C.s14, (x, t) => {
  const nf = w('naufraga');
  if (t < w('isla') - .1) {
    night(x, t, { mountains: false }); water(x, t, 1200, '#14203a');
    const sink = fin(t, nf, 1.2);
    x.save(); x.translate(540, 1210 + sink * 500); x.rotate(sink * .5); ferry(x, t, 0, 0, .9); x.restore();
    if (t > nf) { const R = rng(3); x.strokeStyle = 'rgba(200,210,240,.4)'; x.lineWidth = 2; for (let i = 0; i < 160; i++) { const rx = R() * W, ry = ((t * 1200 + R() * 2000) % (H + 100)); x.beginPath(); x.moveTo(rx, ry); x.lineTo(rx - 10, ry + 40); x.stroke(); } }
    bigText(x, t, nf, 'NAUFRAGIO', 420, { size: 160 });
  } else {
    island(x, t);
    img(x, 'arthur', 360, 1720, 1150); img(x, 'dutch', 700, 1720, 1050);
    label(x, t, w('revolucion'), 'REVOLUCIÓN', 540, 420, { size: 64 });
    label(x, t, w('guerra'), 'UNA GUERRA AJENA', 540, 580, { size: 56 });
    if (t > w('guerra')) for (let i = 0; i < 5; i++) muzzle(x, t, w('guerra') + i * .3, 150 + i * 200, 1000, .6);
  }
});
sfx(w('barco'), 'waves', .5); sfx(w('naufraga'), 'thunder', .8); sfx(w('isla') - .1, 'whoosh', .6); sfx(w('isla'), 'seagull', .5); sfx(w('revolucion'), 'pop', .6); sfx(w('guerra'), 'gunfight', .5);
// 15 — la tos ya no se va
scene(C.s15, (x, t) => {
  night(x, t, { moonX: 760, moonY: 400 });
  const c1 = w('seva'), c2 = w('sangre');
  const jerk = (tt) => t > tt ? Math.sin((t - tt) * 30) * 10 * Math.exp(-(t - tt) * 4) : 0;
  img(x, 'arthur', 470, 1800 + jerk(c1) + jerk(c2), 1650, { rot: t > c2 ? .06 : 0 });
  cough(x, t, c2, 560, 560);
  label(x, t, w('pequeno'), 'ALGO PEQUEÑO', 820, 700, { size: 50 });
  if (t > w('sangre')) stamp(x, t, w('sangre'), 'SANGRE', 820, 880, { size: 70 });
  label(x, t, w('aire'), 'TE FALTA EL AIRE', 300, 1000, { size: 50 });
  label(x, t, w('colina'), 'TE CANSAS', 760, 1120, { size: 50 });
});
sfx(w('seva'), 'cough', .7); sfx(w('sangre'), 'cough', .9); sfx(w('aire'), 'breath', .6); sfx(w('pequeno'), 'pop', .5); sfx(w('colina'), 'pop', .5);
// 16 — el doctor: tuberculosis
scene(C.s16, (x, t) => {
  woodWall(x, .9);
  x.fillStyle = '#ece4d0'; x.strokeStyle = K; x.lineWidth = 6; x.fillRect(650, 300, 300, 380); x.strokeRect(650, 300, 300, 380);
  x.fillStyle = '#1a2a3a'; x.fillRect(680, 330, 240, 320); x.strokeStyle = '#cfe0ff'; x.lineWidth = 6; x.beginPath(); x.moveTo(800, 360); x.lineTo(800, 620); x.stroke();
  for (let i = 0; i < 5; i++) { x.beginPath(); x.ellipse(800, 400 + i * 45, 90 - i * 4, 18, 0, 0, Math.PI); x.stroke(); }
  if (t > w('tb')) { x.fillStyle = 'rgba(230,60,60,.6)'; x.beginPath(); x.arc(740, 470, 40, 0, 7); x.fill(); x.beginPath(); x.arc(860, 520, 30, 0, 7); x.fill(); }
  img(x, 'doctor', 310, 1700, 1250); img(x, 'arthur', 790, 1720, 1250);
  if (t > w('tb')) { dim(x, .5); bigText(x, t, w('tb'), 'TUBERCULOSIS', 900, { size: 150, color: '#ff5a5a' }); }
  stamp(x, t, w('cura'), 'SIN CURA', 540, 1080, { size: 70 }); stamp(x, t, w('medicina'), 'SIN MEDICINA', 540, 1200, { size: 70, rot: .06 });
  if (t > w('meses')) { x.save(); x.translate(540, 520); x.scale(pop(t, w('meses')), pop(t, w('meses'))); txt(x, 'TE QUEDAN MESES', 0, 0, 90, { color: '#fff', font: 'Anton', stroke: K, sw: 12 }); x.restore(); }
});
sfx(w('revisa'), 'heartbeat', .6); sfx(w('tb'), 'stinger', 1); sfx(w('cura'), 'thunk'); sfx(w('medicina'), 'thunk'); sfx(w('meses'), 'clock', .6);
// 17 — te la regaló el granjero
scene(C.s17, (x, t) => {
  woodWall(x, .6);
  polaroid(x, 540, 880, .05, 1.4 * Math.min(1, pop(t, C.s17 + .1, .3)), (y) => { y.fillStyle = '#8a7a5a'; y.fillRect(-170, -190, 340, 340); crop(y, 'downes', 150, 130, 300, 330, -170, -190, 340, 374, { filter: 'sepia(1)' }); }, 'THOMAS DOWNES');
  if (t > w('regalo')) { const k = fin(t, w('regalo'), .4); x.strokeStyle = '#c8202a'; x.lineWidth = 12; x.beginPath(); x.ellipse(540, 860, 290, 340, .05, 0, 7 * k); x.stroke(); label(x, t, w('regalo') + .3, 'EL GRANJERO QUE GOLPEASTE', 540, 380, { size: 50 }); }
});
sfx(C.s17 + .1, 'camera', .6); sfx(w('regalo'), 'scribble', .6);
// 18 — ¿de verdad lo tiene?
scene(C.s18, (x, t) => {
  const pi = TOK.findIndex(k => k.s >= C.plan - .01);
  notebook(x, t, [
    { s: 'DUTCH SIEMPRE TIENE UN PLAN', t: 0, strike: w('primera'), note: ['¿DE VERDAD?', w('tiene')] },
    { s: 'SOMOS FAMILIA', t: 0 },
  ], { portrait: 'dutch' });
  if (t > w('uno') && t < w('primera')) { const k = fin(t, w('uno'), .3); x.strokeStyle = '#ffe08a'; x.lineWidth = 10; x.globalAlpha = k; rr(x, 110, 610, 860, 120, 20); x.stroke(); x.globalAlpha = 1; }
});
sfx(C.s18, 'paper', .7); sfx(w('primera'), 'scribble', .7); sfx(w('tiene'), 'stinger', .8);

endCard(false);
run(['arthur', 'dutch', 'hosea', 'strauss', 'downes', 'doctor', 'linton', 'jinete']);
