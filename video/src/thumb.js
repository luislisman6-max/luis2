// Miniatura 16:9 — "Mil metros bajo el océano"
const { createCanvas } = require('@napi-rs/canvas');
const fs = require('fs');
const R = require('./render.js');
const { drawCup, drawAmphipod, drawAtolla, drawSnailfish, circle, glow, noGlow, rng } = R;
const W = 1920, H = 1080;
const c = createCanvas(W, H), x = c.getContext('2d');

// --- background: lit water (top-left) diving into abyss (bottom-right)
const bg = x.createLinearGradient(0, 0, W * 0.75, H * 1.1);
bg.addColorStop(0, '#1f8fd0'); bg.addColorStop(0.28, '#0b4f86'); bg.addColorStop(0.55, '#06203f'); bg.addColorStop(1, '#010409');
x.fillStyle = bg; x.fillRect(0, 0, W, H);
// god rays from top-left
x.save(); x.globalCompositeOperation = 'lighter';
for (let i = 0; i < 7; i++) {
  const a = 0.25 + i * 0.09;
  const g = x.createLinearGradient(0, 0, Math.cos(a) * 1300, Math.sin(a) * 1300);
  g.addColorStop(0, 'rgba(190,235,255,0.22)'); g.addColorStop(1, 'rgba(190,235,255,0)');
  x.fillStyle = g; x.beginPath(); x.moveTo(-50, -50); x.lineTo(Math.cos(a - 0.025) * 1600, Math.sin(a - 0.025) * 1600); x.lineTo(Math.cos(a + 0.025) * 1600, Math.sin(a + 0.025) * 1600); x.closePath(); x.fill();
}
x.restore();
// marine snow
const r = rng(12);
for (let i = 0; i < 220; i++) { const px = r() * W, py = r() * H, s = r(); circle(x, px, py, 1 + s * 3.5, `rgba(230,245,255,${0.15 + 0.45 * s})`); }

// --- deep right side: seafloor under spotlight
// spotlight cone from above
x.save(); x.globalCompositeOperation = 'lighter';
const cone = x.createLinearGradient(1500, 250, 1500, 1000); cone.addColorStop(0, 'rgba(200,235,255,0)'); cone.addColorStop(1, 'rgba(200,235,255,0.16)');
x.fillStyle = cone; x.beginPath(); x.moveTo(1440, 250); x.lineTo(1560, 250); x.lineTo(1900, 1000); x.lineTo(1100, 1000); x.closePath(); x.fill();
x.restore();
const fl = x.createLinearGradient(0, 820, 0, H); fl.addColorStop(0, '#3a3226'); fl.addColorStop(1, '#a8946e');
x.fillStyle = fl; x.beginPath(); x.moveTo(1040, H); x.bezierCurveTo(1200, 850, 1500, 830, W, 840); x.lineTo(W, H); x.closePath(); x.fill();
const sp = x.createRadialGradient(1500, 880, 20, 1500, 880, 520); sp.addColorStop(0, 'rgba(255,248,220,0.55)'); sp.addColorStop(0.5, 'rgba(160,200,230,0.12)'); sp.addColorStop(1, 'rgba(0,0,0,0)');
x.fillStyle = sp; x.fillRect(900, 300, W, H);

// deep creatures (atmosphere)
x.save(); x.globalAlpha = 0.9; drawAtolla(x, 1700, 210, 0.55, 1.3, 0.85, 1, 1); x.restore();
x.save(); x.globalAlpha = 0.55; drawSnailfish(x, 1180, 560, 0.55, 2.1, 1); x.restore();

// --- BIG cup (left, surface)
const bx = 430, by = 900, bs = 2.55;
x.save(); glow(x, 'rgba(120,220,255,0.9)', 60); drawCup(x, bx, by, bs, 0); noGlow(x); x.restore();
drawCup(x, bx, by, bs, 0);
// happy face
{
  const fy = by - 220 * bs * 0.55;
  x.fillStyle = '#111'; x.strokeStyle = '#111'; x.lineCap = 'round';
  circle(x, bx - 26 * bs, fy - 14 * bs, 9 * bs, '#111'); circle(x, bx + 26 * bs, fy - 14 * bs, 9 * bs, '#111');
  circle(x, bx - 23 * bs, fy - 17 * bs, 3 * bs, '#fff'); circle(x, bx + 29 * bs, fy - 17 * bs, 3 * bs, '#fff');
  x.lineWidth = 7 * bs; x.beginPath(); x.arc(bx, fy + 2 * bs, 30 * bs, 0.15 * Math.PI, 0.85 * Math.PI); x.stroke();
  circle(x, bx - 44 * bs, fy + 8 * bs, 8 * bs, 'rgba(255,120,140,0.45)'); circle(x, bx + 44 * bs, fy + 8 * bs, 8 * bs, 'rgba(255,120,140,0.45)');
}

// --- tiny cup (right, on the floor) with shocked face
const tx = 1500, ty = 905, ts = 0.55;
drawCup(x, tx, ty, ts, 0);
{
  const fy = ty - 220 * ts * 0.55;
  x.strokeStyle = '#111'; x.lineWidth = 3;
  circle(x, tx - 26 * ts, fy - 14 * ts, 11 * ts, '#111'); circle(x, tx + 26 * ts, fy - 14 * ts, 11 * ts, '#111');
  x.fillStyle = '#111'; x.beginPath(); x.ellipse(tx, fy + 22 * ts, 12 * ts, 18 * ts, 0, 0, Math.PI * 2); x.fill();
  x.lineWidth = 4; x.lineCap = 'round';
  x.beginPath(); x.moveTo(tx - 42 * ts, fy - 34 * ts); x.lineTo(tx - 14 * ts, fy - 44 * ts); x.stroke();
  x.beginPath(); x.moveTo(tx + 42 * ts, fy - 34 * ts); x.lineTo(tx + 14 * ts, fy - 44 * ts); x.stroke();
}
// sweat drop
x.fillStyle = '#8fe0ff'; x.beginPath(); x.moveTo(tx + 50, ty - 120); x.quadraticCurveTo(tx + 62, ty - 98, tx + 50, ty - 92); x.quadraticCurveTo(tx + 38, ty - 98, tx + 50, ty - 120); x.fill();
// pressure arrows
for (let i = 0; i < 8; i++) {
  const a = i * Math.PI / 4 + Math.PI / 8, r0 = 210, r1 = 105;
  const cx = tx, cy = ty - 45;
  R.arrow(x, cx + Math.cos(a) * r0, cy + Math.sin(a) * r0 * 0.85, cx + Math.cos(a) * r1, cy + Math.sin(a) * r1 * 0.85, '#ff3b3b', 10, 1);
}
// amphipod for scale (looks huge next to the cup)
drawAmphipod(x, 1745, 905, 1.25, 0.7, 0.3, -1);
// ghost of original size around tiny cup
x.save(); x.globalAlpha = 0.55; drawCup(x, tx, ty, 1.15, 0, { ghost: true }); x.restore();

// --- descent arrow (curved, dashed glow) from big cup to tiny cup
x.save();
x.strokeStyle = '#ffe14d'; x.lineWidth = 16; x.lineCap = 'round'; x.setLineDash([2, 34]);
glow(x, '#ffb000', 25);
x.beginPath(); x.moveTo(720, 300); x.bezierCurveTo(1000, 230, 1300, 380, 1440, 640); x.stroke();
x.setLineDash([]);
// arrow head
x.fillStyle = '#ffe14d'; x.save(); x.translate(1450, 665); x.rotate(1.15);
x.beginPath(); x.moveTo(38, 0); x.lineTo(-22, -34); x.lineTo(-22, 34); x.closePath(); x.fill(); x.restore();
noGlow(x); x.restore();

// --- headline "11 KM"
x.save();
x.translate(1060, 205); x.rotate(-0.06);
x.font = '300px Anton'; x.textAlign = 'center'; x.textBaseline = 'middle';
x.lineJoin = 'round';
x.shadowColor = 'rgba(0,0,0,0.85)'; x.shadowBlur = 40; x.shadowOffsetY = 14;
x.lineWidth = 34; x.strokeStyle = '#000'; x.strokeText('11 KM', 0, 0);
x.shadowBlur = 0; x.shadowOffsetY = 0;
const tg = x.createLinearGradient(0, -130, 0, 130); tg.addColorStop(0, '#fff6a8'); tg.addColorStop(0.5, '#ffe14d'); tg.addColorStop(1, '#ffab00');
x.fillStyle = tg; x.fillText('11 KM', 0, 0);
x.restore();
// small tag: "ABAJO"
x.save(); x.translate(1060, 395); x.rotate(-0.06);
x.font = '78px Anton'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.lineJoin = 'round';
const tw = x.measureText('BAJO EL MAR').width + 70;
x.fillStyle = '#ff3b3b'; x.shadowColor = 'rgba(0,0,0,0.6)'; x.shadowBlur = 20; R.roundRect(x, -tw / 2, -55, tw, 110, 18); x.fill();
x.shadowBlur = 0; x.fillStyle = '#fff'; x.fillText('BAJO EL MAR', 0, 4);
x.restore();

// --- depth tags
function tag(t, px, py, col) {
  x.save(); x.font = '46px Anton'; x.textAlign = 'center'; x.textBaseline = 'middle';
  const w = x.measureText(t).width + 50; x.fillStyle = 'rgba(3,14,30,0.85)'; x.strokeStyle = col; x.lineWidth = 4; glow(x, col, 18);
  R.roundRect(x, px - w / 2, py - 36, w, 72, 36); x.fill(); x.stroke(); noGlow(x); x.fillStyle = '#fff'; x.fillText(t, px, py + 2); x.restore();
}
tag('0 m', 430, 200, '#5ff2ff');
tag('10.900 m', 1500, 1015, '#ffe14d');
// --- vignette + punchy contrast edge
const vg = x.createRadialGradient(W / 2, H / 2, H * 0.4, W / 2, H / 2, H * 1.05); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,0.6)');
x.fillStyle = vg; x.fillRect(0, 0, W, H);

fs.writeFileSync(process.argv[2] || 'thumb.png', c.toBuffer('image/png'));
console.log('ok');
