// Utilería y escenarios para las partes 2-5 (mismo estilo: plano, contorno café oscuro).
require('./lib_rdr.js');

// ---------- campamento
function campfire(x, t, cx, cy, s = 1) {
  x.save(); x.translate(cx, cy); x.scale(s, s);
  const gl = x.createRadialGradient(0, -40, 10, 0, -40, 520); gl.addColorStop(0, `rgba(255,160,60,${.45 + .05 * Math.sin(t * 9)})`); gl.addColorStop(1, 'rgba(255,160,60,0)');
  x.fillStyle = gl; x.fillRect(-560, -560, 1120, 1000);
  x.strokeStyle = K; x.lineWidth = 6;
  x.fillStyle = '#6b4226'; [[-70, -14, .3], [70, -14, -.3]].forEach(([a, b, r]) => { x.save(); x.translate(a, b); x.rotate(r); rr(x, -80, -14, 160, 28, 12); x.fill(); x.stroke(); x.restore(); });
  x.fillStyle = '#7a7470'; for (let i = 0; i < 7; i++) { const a = Math.PI + i / 6 * Math.PI; x.beginPath(); x.ellipse(Math.cos(a) * 110, 10 + Math.sin(a) * -10, 26, 18, 0, 0, 7); x.fill(); x.stroke(); }
  for (let i = 0; i < 3; i++) {
    const fx = -40 + i * 40, fh = 130 + 30 * Math.sin(t * 10 + i * 2);
    const fg = x.createLinearGradient(0, -fh, 0, 0); fg.addColorStop(0, '#ffe27a'); fg.addColorStop(1, '#ff6a1f');
    x.fillStyle = fg; x.beginPath(); x.moveTo(fx - 34, -6); x.quadraticCurveTo(fx - 30, -fh * .6, fx + 6 * Math.sin(t * 7 + i), -fh); x.quadraticCurveTo(fx + 34, -fh * .5, fx + 34, -6); x.fill();
  }
  const R = rng(4); for (let i = 0; i < 8; i++) { const k = (t * .5 + R()) % 1; x.fillStyle = `rgba(255,200,100,${1 - k})`; x.beginPath(); x.arc(R() * 80 - 40 + Math.sin(k * 8) * 20, -80 - k * 300, 3, 0, 7); x.fill(); }
  x.restore();
}
function tent(x, cx, cy, s = 1, lit = false) {
  x.save(); x.translate(cx, cy); x.scale(s, s); x.strokeStyle = K; x.lineWidth = 6;
  x.fillStyle = '#e2d6b8'; x.beginPath(); x.moveTo(-200, 0); x.lineTo(0, -260); x.lineTo(200, 0); x.closePath(); x.fill(); x.stroke();
  x.fillStyle = lit ? '#f2b45a' : '#3a2a1a'; x.beginPath(); x.moveTo(-60, 0); x.lineTo(0, -170); x.lineTo(60, 0); x.closePath(); x.fill(); x.stroke();
  x.fillStyle = 'rgba(0,0,0,.18)'; x.beginPath(); x.moveTo(0, -260); x.lineTo(200, 0); x.lineTo(60, 0); x.closePath(); x.fill();
  x.restore();
}
function wagon(x, cx, cy, s = 1) {
  x.save(); x.translate(cx, cy); x.scale(s, s); x.strokeStyle = K; x.lineWidth = 6;
  x.fillStyle = '#f0e6cc'; x.beginPath(); x.moveTo(-230, -110); x.bezierCurveTo(-230, -330, 230, -330, 230, -110); x.closePath(); x.fill(); x.stroke();
  for (const a of [-120, 0, 120]) { x.beginPath(); x.moveTo(a, -110); x.quadraticCurveTo(a * 1.05, -260, a * .9, -280); x.stroke(); }
  x.fillStyle = '#8a5a30'; rr(x, -250, -120, 500, 80, 6); x.fill(); x.stroke();
  for (const a of [-160, 160]) { x.fillStyle = '#6b4226'; x.beginPath(); x.arc(a, -20, 64, 0, 7); x.fill(); x.stroke(); x.fillStyle = '#c98a4a'; x.beginPath(); x.arc(a, -20, 16, 0, 7); x.fill(); x.stroke(); for (let i = 0; i < 8; i++) { x.beginPath(); x.moveTo(a, -20); x.lineTo(a + 60 * Math.cos(i * .785), -20 + 60 * Math.sin(i * .785)); x.stroke(); } }
  x.restore();
}
function campNight(x, t, o = {}) {
  night(x, t, { moonX: o.moonX ?? 820, moonY: 360 });
  // pinos
  x.fillStyle = '#0e1a2c'; x.strokeStyle = '#050a14'; x.lineWidth = 3;
  [60, 180, 300, 860, 980, 1060].forEach((px, i) => { const h = 260 + (i % 3) * 60; x.beginPath(); x.moveTo(px, 1260 - h); x.lineTo(px - 80, 1260); x.lineTo(px + 80, 1260); x.closePath(); x.fill(); x.stroke(); });
  x.fillStyle = '#2a2016'; x.fillRect(0, 1250, W, H - 1250);
  if (o.tents !== false) { tent(x, 200, 1300, .9, true); tent(x, 900, 1290, .8); }
  if (o.wagon) wagon(x, 760, 1300, .8);
  if (o.fire !== false) campfire(x, t, o.fireX ?? 540, o.fireY ?? 1520, o.fireS ?? 1);
}
function campDay(x, t, o = {}) {
  const g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#6fa6d8'); g.addColorStop(.6, '#c8e0ee'); x.fillStyle = g; x.fillRect(0, 0, W, H);
  x.fillStyle = '#fff'; [[200, 300, 1], [800, 220, .8]].forEach(([a, b, s]) => { x.beginPath(); x.ellipse(a + Math.sin(t * .2) * 30, b, 160 * s, 50 * s, 0, 0, 7); x.ellipse(a + 60 * s, b - 30 * s, 90 * s, 50 * s, 0, 0, 7); x.fill(); });
  x.fillStyle = '#7a8aa0'; x.strokeStyle = K; x.lineWidth = 4; x.beginPath(); x.moveTo(0, 1100); [[200, 900], [380, 1020], [600, 860], [820, 1000], [1080, 900]].forEach(p => x.lineTo(...p)); x.lineTo(1080, 1300); x.lineTo(0, 1300); x.closePath(); x.fill(); x.stroke();
  x.fillStyle = '#8aa65a'; x.fillRect(0, 1180, W, H - 1180); x.strokeRect(-10, 1180, W + 20, 4);
  x.fillStyle = '#7a9450'; const R = rng(3); for (let i = 0; i < 30; i++) { const gx = R() * W, gy = 1220 + R() * 650; x.beginPath(); x.moveTo(gx, gy); x.lineTo(gx - 8, gy - 24); x.lineTo(gx + 2, gy - 10); x.lineTo(gx + 10, gy - 26); x.lineTo(gx + 12, gy); x.fill(); }
  if (o.tents !== false) { tent(x, 150, 1250, .8); wagon(x, 880, 1250, .75); }
}
// ---------- libreta «COSAS QUE RECORDAR» (objeto recurrente)
function notebook(x, t, items, o = {}) {
  woodWall(x, .6);
  paperRect(x, 540, 900, 920, 1000, -0.015, '#efe3c4');
  x.save(); x.translate(540, 900); x.rotate(-0.015);
  x.strokeStyle = 'rgba(90,120,160,.35)'; x.lineWidth = 3; for (let y = -300; y <= 440; y += 90) { x.beginPath(); x.moveTo(-420, y); x.lineTo(420, y); x.stroke(); }
  x.strokeStyle = 'rgba(190,60,60,.5)'; x.beginPath(); x.moveTo(-360, -480); x.lineTo(-360, 480); x.stroke();
  txt(x, 'COSAS QUE RECORDAR', -330, -390, 84, { color: '#2a1a0e', font: 'Bebas', align: 'left', spacing: 3 });
  x.fillStyle = '#2a1a0e'; x.fillRect(-330, -340, 560, 5);
  items.forEach((it, i) => {
    const y = -230 + i * 140; if (t < it.t) return;
    const words = it.s.split(' '); const n = it.wt ? it.wt.filter(tt => t >= tt).length : words.length;
    const fs = it.s.length > 20 ? 62 : 74;
    txt(x, `${i + 1}.`, -340, y, 74, { color: '#2a1a0e', font: 'Bebas', align: 'left' });
    txt(x, words.slice(0, Math.max(1, n)).join(' '), -270, y, fs, { color: it.color || '#2a1a0e', font: 'Bebas', align: 'left', spacing: 2 });
    if (it.strike && t >= it.strike) { x.font = fs + 'px Bebas'; x.letterSpacing = '2px'; const tw = x.measureText(it.s).width; const k = fin(t, it.strike, .35); x.strokeStyle = '#c8202a'; x.lineWidth = 9; x.lineCap = 'round'; x.beginPath(); x.moveTo(-275, y + 4); x.lineTo(-275 + (tw + 20) * k, y - 2); x.stroke(); x.letterSpacing = '0px'; }
    if (it.note && t >= it.note[1]) txt(x, it.note[0], 300, y + 70, 64, { color: '#c8202a', font: 'Anton', rot: -0.08, sc: pop(t, it.note[1]) });
    if (it.circle && t >= it.circle) { const k = fin(t, it.circle, .5); x.strokeStyle = '#c8202a'; x.lineWidth = 8; x.beginPath(); x.ellipse(-40, y, 360, 70, -0.02, 0, 7 * k); x.stroke(); }
  });
  if (o.portrait) { x.save(); x.translate(360, -470); x.strokeStyle = '#2a1a0e'; x.lineWidth = 3; crop(x, o.portrait, 170, 110, 260, 280, -70, -80, 140, 150, { filter: 'grayscale(1) contrast(1.3)', alpha: .8 }); x.restore(); }
  x.restore();
}
// ---------- pizarra
function chalkboard(x, t, lines, cx = 540, cy = 640) {
  x.save(); x.translate(cx, cy); x.strokeStyle = K; x.lineWidth = 8;
  x.fillStyle = '#6b4226'; rr(x, -380, -250, 760, 500, 14); x.fill(); x.stroke();
  x.fillStyle = '#2f4a3a'; rr(x, -350, -220, 700, 440, 8); x.fill();
  x.fillRect(-300, 250, 20, 300); x.fillRect(280, 250, 20, 300);
  lines.forEach((l, i) => { if (t >= l.t) { const s = l.s; const n = Math.ceil(s.length * fin(t, l.t, l.d || .5)); txt(x, s.slice(0, n), -300, -140 + i * 110, l.size || 84, { color: '#f2f2ea', font: 'Bebas', align: 'left', spacing: 6 }); } });
  x.restore();
}
// ---------- nieve
function snow(x, t, o = {}) {
  const g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, o.night ? '#1a2540' : '#8a9ab0'); g.addColorStop(1, o.night ? '#3a4a66' : '#d8e0ea'); x.fillStyle = g; x.fillRect(0, 0, W, H);
  x.fillStyle = o.night ? '#4a5a78' : '#a8b4c4'; x.strokeStyle = K; x.lineWidth = 4;
  x.beginPath(); x.moveTo(0, 1000); [[180, 760], [360, 900], [560, 700], [760, 880], [940, 740], [1080, 860]].forEach(p => x.lineTo(...p)); x.lineTo(1080, 1300); x.lineTo(0, 1300); x.closePath(); x.fill(); x.stroke();
  x.fillStyle = '#f4f6fa'; [[180, 760], [560, 700], [940, 740]].forEach(([a, b]) => { x.beginPath(); x.moveTo(a, b); x.lineTo(a - 50, b + 60); x.lineTo(a + 50, b + 60); x.closePath(); x.fill(); });
  x.fillStyle = '#1e3a2e'; [80, 240, 820, 1000].forEach((px, i) => { const h = 300 + (i % 2) * 80; for (let k = 0; k < 3; k++) { x.beginPath(); x.moveTo(px, 1260 - h + k * 70); x.lineTo(px - 90 + k * 10, 1260 - h + 140 + k * 90); x.lineTo(px + 90 - k * 10, 1260 - h + 140 + k * 90); x.closePath(); x.fill(); x.stroke(); } });
  x.fillStyle = o.night ? '#c8d2e4' : '#f4f6fa'; x.beginPath(); x.moveTo(0, 1240); x.quadraticCurveTo(540, 1180, 1080, 1240); x.lineTo(1080, H); x.lineTo(0, H); x.closePath(); x.fill(); x.stroke();
  const R = rng(12), n = o.storm ? 260 : 120;
  for (let i = 0; i < n; i++) { const sx = R() * W, sp = 80 + R() * 160, ph = R() * 50; const yy = (t * sp + ph * 40) % (H + 40); const xx = (sx + (o.storm ? t * 260 : Math.sin(t + ph) * 30)) % W; x.fillStyle = 'rgba(255,255,255,.85)'; x.beginPath(); x.arc(xx, yy, 2 + R() * 4, 0, 7); x.fill(); }
}
function wolf(x, cx, cy, s = 1, flip = false, eyes = 1) {
  x.save(); x.translate(cx, cy); x.scale(flip ? -s : s, s); x.fillStyle = '#1a1e28';
  x.beginPath(); x.moveTo(-160, 0); x.lineTo(-150, -70); x.quadraticCurveTo(-200, -100, -230, -60); x.quadraticCurveTo(-200, -110, -140, -110); x.lineTo(60, -120); x.lineTo(110, -170); x.lineTo(120, -210); x.lineTo(140, -180); x.lineTo(160, -200); x.lineTo(168, -170); x.quadraticCurveTo(230, -150, 240, -120); x.lineTo(180, -110); x.lineTo(130, -90); x.lineTo(110, 0); x.lineTo(90, 0); x.lineTo(80, -70); x.lineTo(-90, -70); x.lineTo(-110, 0); x.closePath(); x.fill();
  if (eyes) { x.fillStyle = `rgba(255,220,90,${eyes})`; x.shadowColor = '#ffd24a'; x.shadowBlur = 14; x.beginPath(); x.ellipse(170, -160, 8, 4, .2, 0, 7); x.fill(); x.shadowBlur = 0; }
  x.restore();
}
// ---------- barco de vapor / ferry
function ferry(x, t, cx, cy, s = 1) {
  x.save(); x.translate(cx, cy + Math.sin(t * 2) * 6); x.scale(s, s); x.strokeStyle = K; x.lineWidth = 6;
  x.fillStyle = '#e8e0cc'; x.beginPath(); x.moveTo(-380, 0); x.lineTo(380, 0); x.lineTo(330, 90); x.lineTo(-340, 90); x.closePath(); x.fill(); x.stroke();
  x.fillStyle = '#8a2a2a'; x.fillRect(-340, 60, 670, 30); x.strokeRect(-340, 60, 670, 30);
  x.fillStyle = '#f4ecd8'; x.fillRect(-280, -160, 520, 160); x.strokeRect(-280, -160, 520, 160);
  for (let i = 0; i < 7; i++) { x.fillStyle = '#2a3a5a'; x.fillRect(-250 + i * 70, -120, 40, 50); x.strokeRect(-250 + i * 70, -120, 40, 50); }
  x.fillStyle = '#e8e0cc'; x.fillRect(-180, -260, 300, 100); x.strokeRect(-180, -260, 300, 100);
  for (const a of [-120, 40]) { x.fillStyle = '#2a2a2a'; x.fillRect(a, -420, 40, 160); x.strokeRect(a, -420, 40, 160); x.fillStyle = 'rgba(80,80,80,.5)'; for (let k = 0; k < 4; k++) { const kk = (t * .4 + k * .25) % 1; x.beginPath(); x.arc(a + 20 + kk * 120, -440 - kk * 200, 20 + kk * 40, 0, 7); x.fill(); } }
  x.restore();
}
function water(x, t, y0, col = '#2a4a6a') {
  x.fillStyle = col; x.fillRect(0, y0, W, H - y0);
  x.strokeStyle = 'rgba(255,255,255,.25)'; x.lineWidth = 4;
  for (let r = 0; r < 10; r++) { const yy = y0 + 30 + r * 70; x.beginPath(); for (let px = 0; px <= W; px += 20) x.lineTo(px, yy + Math.sin(px * .02 + t * 2 + r) * 8); x.stroke(); }
}
// ---------- ciudad de noche (Saint Denis)
function city(x, t) {
  night(x, t, { moonX: 860, moonY: 300, mountains: false });
  const R = rng(21);
  for (let layer = 0; layer < 2; layer++) {
    for (let i = 0; i < 14; i++) {
      const bw = 90 + R() * 90, bh = (layer ? 420 : 620) + R() * 360, bx = i * 85 - 40 + layer * 40, by = 1300 - bh;
      x.fillStyle = layer ? '#1e2238' : '#2c304c'; x.strokeStyle = '#0a0c18'; x.lineWidth = 3; x.fillRect(bx, by, bw, bh); x.strokeRect(bx, by, bw, bh);
      for (let wy = by + 30; wy < 1280; wy += 60) for (let wx = bx + 16; wx < bx + bw - 20; wx += 34) if (R() > .45) { x.fillStyle = `rgba(255,214,120,${.6 + .4 * Math.sin(t * 2 + wx + wy)})`; x.fillRect(wx, wy, 16, 26); }
    }
  }
  x.fillStyle = '#14121c'; x.fillRect(0, 1300, W, H - 1300);
  for (let i = 0; i < 5; i++) { const lx = 100 + i * 220; x.fillStyle = '#0a0a10'; x.fillRect(lx, 1060, 10, 240); const g = x.createRadialGradient(lx + 5, 1060, 5, lx + 5, 1060, 160); g.addColorStop(0, 'rgba(255,210,120,.6)'); g.addColorStop(1, 'rgba(255,210,120,0)'); x.fillStyle = g; x.fillRect(lx - 160, 900, 330, 330); x.fillStyle = '#ffd88a'; x.beginPath(); x.arc(lx + 5, 1056, 12, 0, 7); x.fill(); }
}
function bankFront(x, t) {
  x.fillStyle = '#d8ccb0'; x.strokeStyle = K; x.lineWidth = 6; x.fillRect(90, 420, 900, 900); x.strokeRect(90, 420, 900, 900);
  x.fillStyle = '#c4b694'; x.beginPath(); x.moveTo(60, 430); x.lineTo(540, 230); x.lineTo(1020, 430); x.closePath(); x.fill(); x.stroke();
  txt(x, 'BANCO', 540, 360, 90, { color: '#3a2a1a', font: 'Bebas', spacing: 12 });
  for (let i = 0; i < 5; i++) { x.fillStyle = '#ece4d0'; x.fillRect(130 + i * 180, 470, 60, 820); x.strokeRect(130 + i * 180, 470, 60, 820); }
  x.fillStyle = '#3a2a1a'; x.fillRect(450, 980, 180, 340); x.strokeRect(450, 980, 180, 340);
  x.fillStyle = '#6a6a6a'; x.fillRect(0, 1320, W, H - 1320);
}
// ---------- isla tropical
function island(x, t) {
  const g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#3aa0d8'); g.addColorStop(.55, '#a8dcf0'); x.fillStyle = g; x.fillRect(0, 0, W, H);
  x.fillStyle = '#fff4c8'; x.beginPath(); x.arc(820, 300, 90, 0, 7); x.fill();
  water(x, t, 1000, '#1e8aa8');
  x.fillStyle = '#ecd8a0'; x.strokeStyle = K; x.lineWidth = 5; x.beginPath(); x.moveTo(0, 1200); x.quadraticCurveTo(540, 1080, 1080, 1220); x.lineTo(1080, H); x.lineTo(0, H); x.closePath(); x.fill(); x.stroke();
  [[160, 1240, 1], [930, 1260, -1]].forEach(([px, py, s]) => {
    x.strokeStyle = K; x.lineWidth = 5; x.fillStyle = '#8a6a3a';
    x.beginPath(); x.moveTo(px - 20, py); x.quadraticCurveTo(px + s * 60, py - 300, px + s * 30, py - 560); x.lineTo(px + s * 60, py - 560); x.quadraticCurveTo(px + s * 90, py - 300, px + 20, py); x.closePath(); x.fill(); x.stroke();
    x.fillStyle = '#3a8a3a'; for (let i = 0; i < 6; i++) { const a = -Math.PI / 2 + (i - 2.5) * .55 + Math.sin(t * 1.5 + i) * .05; x.save(); x.translate(px + s * 45, py - 560); x.rotate(a); x.beginPath(); x.moveTo(0, 0); x.quadraticCurveTo(130, -50, 260, 30); x.quadraticCurveTo(130, 10, 0, 0); x.fill(); x.stroke(); x.restore(); }
  });
}
// ---------- estación de tren
function station(x, t) {
  sunset(x, t, { sunY: 1000, top: '#4a2a5a' });
  x.strokeStyle = K; x.lineWidth = 6;
  x.fillStyle = '#c99a4a'; x.fillRect(80, 700, 600, 520); x.strokeRect(80, 700, 600, 520);
  x.fillStyle = '#7a3a2a'; x.beginPath(); x.moveTo(40, 710); x.lineTo(380, 560); x.lineTo(720, 710); x.closePath(); x.fill(); x.stroke();
  x.fillStyle = '#ece4d0'; x.fillRect(240, 740, 280, 80); x.strokeRect(240, 740, 280, 80); txt(x, 'ESTACIÓN', 380, 782, 56, { color: '#3a2412', font: 'Bebas', spacing: 6 });
  for (let i = 0; i < 3; i++) { x.fillStyle = '#2a3a5a'; x.fillRect(130 + i * 190, 880, 110, 150); x.strokeRect(130 + i * 190, 880, 110, 150); }
  x.fillStyle = '#5a5a60'; x.fillRect(0, 1220, W, 40); x.fillStyle = '#3a3a40'; x.fillRect(0, 1260, W, H - 1260);
  x.fillStyle = '#8a8a90'; x.fillRect(0, 1300, W, 12); x.fillRect(0, 1360, W, 12);
}
function bench(x, cx, cy, s = 1) { x.save(); x.translate(cx, cy); x.scale(s, s); x.fillStyle = '#7a4a2a'; x.strokeStyle = K; x.lineWidth = 6; rr(x, -280, -40, 560, 34, 6); x.fill(); x.stroke(); rr(x, -280, -130, 560, 30, 6); x.fill(); x.stroke(); x.fillStyle = '#2a2a2a'; [-250, 250].forEach(a => { x.fillRect(a - 10, -130, 20, 230); }); x.restore(); }
// ---------- tumbas y cruces
function grave(x, cx, cy, s = 1, txtLabel = '') {
  x.save(); x.translate(cx, cy); x.scale(s, s); x.strokeStyle = K; x.lineWidth = 6;
  x.fillStyle = '#5a3a22'; x.beginPath(); x.ellipse(0, 20, 150, 36, 0, 0, 7); x.fill(); x.stroke();
  x.fillStyle = '#8a5a30'; x.fillRect(-14, -260, 28, 280); x.strokeRect(-14, -260, 28, 280); x.fillRect(-90, -200, 180, 28); x.strokeRect(-90, -200, 180, 28);
  if (txtLabel) txt(x, txtLabel, 0, -186, 30, { color: '#f4ead2', font: 'Bebas' });
  x.restore();
}
function deer(x, cx, cy, s = 1, col = '#1a1014') {
  x.save(); x.translate(cx, cy); x.scale(s, s); x.fillStyle = col; x.strokeStyle = col; x.lineCap = 'round';
  x.beginPath(); x.ellipse(0, -110, 110, 45, 0, 0, 7); x.fill();
  x.lineWidth = 16; [[-80, -90, -90, 0], [-50, -90, -40, 0], [60, -90, 70, 0], [90, -90, 100, 0]].forEach(([a, b, c, d]) => { x.beginPath(); x.moveTo(a, b); x.lineTo(c, d); x.stroke(); });
  x.beginPath(); x.moveTo(80, -130); x.lineTo(110, -230); x.lineTo(150, -230); x.lineTo(120, -120); x.fill();
  x.beginPath(); x.ellipse(140, -240, 40, 22, .3, 0, 7); x.fill();
  x.lineWidth = 7; [[120, -260, 90, -340], [100, -300, 70, -320], [140, -262, 170, -340], [160, -300, 190, -320]].forEach(([a, b, c, d]) => { x.beginPath(); x.moveTo(a, b); x.lineTo(c, d); x.stroke(); });
  x.restore();
}
function sunrise(x, t, k) { // k: 0 noche → 1 amanecer
  const g = x.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, `rgb(${lerp(20, 120, k)},${lerp(24, 110, k)},${lerp(60, 170, k)})`); g.addColorStop(.5, `rgb(${lerp(60, 240, k)},${lerp(50, 170, k)},${lerp(90, 150, k)})`); g.addColorStop(.7, `rgb(${lerp(80, 255, k)},${lerp(60, 214, k)},${lerp(90, 150, k)})`);
  x.fillStyle = g; x.fillRect(0, 0, W, H);
  const sy = lerp(1300, 1020, k); const sg = x.createRadialGradient(540, sy, 30, 540, sy, 500); sg.addColorStop(0, `rgba(255,240,200,${k})`); sg.addColorStop(1, 'rgba(255,220,160,0)'); x.fillStyle = sg; x.fillRect(0, 0, W, H);
  x.fillStyle = `rgba(255,246,220,${k})`; x.beginPath(); x.arc(540, sy, 110, 0, 7); x.fill();
  x.fillStyle = '#5a4060'; x.strokeStyle = K; x.lineWidth = 4; x.beginPath(); x.moveTo(0, 1150); [[150, 980], [300, 1080], [480, 940], [640, 1060], [820, 960], [1080, 1100]].forEach(p => x.lineTo(...p)); x.lineTo(1080, 1300); x.lineTo(0, 1300); x.closePath(); x.fill(); x.stroke();
  x.fillStyle = '#e8d8e0'; [[480, 940], [820, 960]].forEach(([a, b]) => { x.beginPath(); x.moveTo(a, b); x.lineTo(a - 40, b + 50); x.lineTo(a + 40, b + 50); x.closePath(); x.fill(); });
  x.fillStyle = '#2a1a24'; x.beginPath(); x.moveTo(0, 1240); x.quadraticCurveTo(540, 1200, 1080, 1250); x.lineTo(1080, H); x.lineTo(0, H); x.closePath(); x.fill();
}
// ---------- otros
function muzzle(x, t, t0, px, py, sc = 1) { if (t < t0 || t > t0 + .25) return; const k = (t - t0) / .25; x.save(); x.translate(px, py); x.scale(sc, sc); x.fillStyle = `rgba(255,220,120,${1 - k})`; x.beginPath(); for (let i = 0; i < 12; i++) { const a = i / 12 * 7, r = (i % 2 ? 30 : 90) * (1 + k * .5); x.lineTo(r * Math.cos(a), r * Math.sin(a)); } x.fill(); x.restore(); }
function bubble(x, t, t0, s, px, py, o = {}) { const k = pop(t, t0); if (k <= 0) return; x.save(); x.translate(px, py); x.scale(k, k); x.font = `${o.size || 52}px Anton`; const tw = x.measureText(s).width; const ww = tw + 60, hh = (o.size || 52) + 46; x.fillStyle = '#fbf6ea'; x.strokeStyle = K; x.lineWidth = 5; rr(x, -ww / 2, -hh / 2, ww, hh, 30); x.fill(); x.stroke(); x.beginPath(); x.moveTo((o.tail || -1) * 20, hh / 2 - 3); x.lineTo((o.tail || -1) * 60, hh / 2 + 40); x.lineTo((o.tail || -1) * -10, hh / 2 - 3); x.fill(); x.stroke(); txt(x, s, 0, 2, o.size || 52, { color: K }); x.restore(); }
function bigText(x, t, t0, s, py, o = {}) { const k = pop(t, t0, .35); if (k <= 0) return; x.save(); x.translate(540, py); x.scale(k, k); txt(x, s, 0, 0, o.size || 150, { color: o.color || '#ffe08a', font: o.font || 'Bebas', stroke: K, sw: 14, spacing: o.spacing ?? 4, shadow: 16 }); x.restore(); }
function dim(x, a) { x.fillStyle = `rgba(0,0,0,${a})`; x.fillRect(0, 0, W, H); }
function moneyBag(x, cx, cy, s = 1) { x.save(); x.translate(cx, cy); x.scale(s, s); x.fillStyle = '#c9a46a'; x.strokeStyle = K; x.lineWidth = 6; x.beginPath(); x.moveTo(-40, -120); x.lineTo(40, -120); x.lineTo(30, -90); x.quadraticCurveTo(130, -40, 110, 60); x.quadraticCurveTo(0, 110, -110, 60); x.quadraticCurveTo(-130, -40, -30, -90); x.closePath(); x.fill(); x.stroke(); txt(x, '$', 0, 10, 110, { color: '#6a4a1a' }); x.restore(); }
function crossX(x, t, t0, cx, cy, r) { redX(x, t, t0, cx, cy, r); }

Object.assign(global, { campfire, tent, wagon, campNight, campDay, notebook, chalkboard, snow, wolf, ferry, water, city, bankFront, island, station, bench, grave, deer, sunrise, muzzle, bubble, bigText, dim, moneyBag, crossX });
