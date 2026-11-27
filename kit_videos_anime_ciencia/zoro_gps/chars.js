// Motor de personajes "Zoro y el GPS" (basado en "Vegeta, el rival") — mismo estilo que Black Flash (vector plano, contorno fino, sombra suave).
// Caja local 400x660, centro x=200, pies en y≈620.
const OL = '#15121a';
const fsh = (a = 0.22) => `fill="${OL}" fill-opacity="${a}"`;
const lerp = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];

function limb(pts, w, color, out = 5) {
  const d = 'M' + pts.map(p => p.join(',')).join(' L');
  return `<path d="${d}" fill="none" stroke="${OL}" stroke-width="${w + out}" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="${d}" fill="none" stroke="${color}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
}
const ln = (pts, w, color, op = 1) => `<path d="M${pts.map(p => p.join(',')).join(' L')}" fill="none" stroke="${color}" stroke-opacity="${op}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;

// ---------- peinados ----------
const HAIR = {
  // Goku base: picos a los lados y arriba + flequillo de 5 mechones
  goku: 'M156,150 L148,126 L108,138 L138,106 L92,94 L136,82 L108,46 L156,62 L152,16 L186,50 L204,6 L218,48 L254,20 L248,64 L294,54 L262,90 L306,104 L262,114 L288,140 L248,132 L244,150 L244,124 L232,104 L224,128 L212,100 L198,132 L186,100 L174,126 L166,104 L156,128 Z',
  // Super Saiyajin: todo hacia arriba, mechón al centro
  ssj: 'M156,148 L144,118 L114,110 L138,94 L106,62 L148,70 L136,20 L174,56 L198,-6 L216,52 L252,14 L248,68 L290,56 L264,96 L294,112 L258,120 L244,148 L244,122 L230,96 L218,118 L206,92 L194,130 L188,96 L174,116 L164,98 L156,124 Z',
  // Ultra Instinto: picos rectos hacia arriba, más ordenado
  ui: 'M156,150 L146,120 L118,118 L140,100 L112,74 L150,78 L138,34 L176,62 L196,4 L214,60 L252,30 L246,78 L286,72 L262,102 L288,118 L256,122 L244,150 L244,124 L232,102 L220,124 L208,98 L196,126 L184,100 L172,122 L164,102 L156,126 Z',
  // Vegeta: flama alta con entrada en "M" (widow's peak)
  vegeta: 'M158,148 L150,104 L134,84 L150,82 L136,40 L160,58 L160,8 L182,40 L198,-22 L216,38 L238,6 L240,56 L264,38 L252,84 L268,86 L250,104 L242,148 L240,118 Q226,100 210,98 L200,118 L190,98 Q174,100 160,118 Z',
};
function hair(o, cx, cy) {
  const H = HAIR[o.hair];
  if (!H) return '';
  let s = '';
  const g = o.hairScale ? `<g transform="translate(200,100) scale(${o.hairScale}) translate(-200,-100)">` : '<g>';
  s += g + `<path d="${H}" fill="${o.hairC}" stroke="${OL}" stroke-width="3.2" stroke-linejoin="round"/>`;
  // sombra derecha del pelo y brillos
  s += `<path d="${H}" fill="${OL}" fill-opacity=".16" clip-path="url(#clipR)"/>`;
  s += `<path d="${o.hairHiD || 'M168,70 L180,44 M196,52 L204,20 M226,62 L238,38'}" stroke="${o.hairHi || '#fff'}" stroke-width="4.5" stroke-linecap="round" opacity=".55"/>`;
  s += '</g>';
  return s;
}

// ---------- cabeza ----------
function head(o) {
  const cx = 200, cy = 150;
  let s = '';
  s += `<ellipse cx="${cx - 44}" cy="${cy + 6}" rx="9" ry="13" fill="${o.skin}" stroke="${OL}" stroke-width="3"/>
        <ellipse cx="${cx + 44}" cy="${cy + 6}" rx="9" ry="13" fill="${o.skin}" stroke="${OL}" stroke-width="3"/>`;
  s += `<path d="M${cx - 44},${cy - 20} Q${cx - 46},${cy + 30} ${cx - 30},${cy + 48} Q${cx - 14},${cy + 62} ${cx},${cy + 63} Q${cx + 14},${cy + 62} ${cx + 30},${cy + 48} Q${cx + 46},${cy + 30} ${cx + 44},${cy - 20} Q${cx + 40},${cy - 58} ${cx},${cy - 60} Q${cx - 40},${cy - 58} ${cx - 44},${cy - 20} Z" fill="${o.skin}" stroke="${OL}" stroke-width="3.2"/>`;
  s += `<path d="M${cx + 44},${cy - 20} Q${cx + 46},${cy + 30} ${cx + 30},${cy + 48} Q${cx + 14},${cy + 62} ${cx},${cy + 63} Q${cx + 24},${cy + 40} ${cx + 30},${cy} Z" ${fsh(0.16)}/>`;
  const ey = cy + 8, ex = 18;
  for (const k of [-1, 1]) {
    const x = cx + k * ex;
    if (o.scarEye && k > 0) {
      s += `<path d="M${x - 12},${ey + 1} Q${x},${ey + 6} ${x + 12},${ey + 1}" fill="none" stroke="${OL}" stroke-width="3.4" stroke-linecap="round"/>
            <path d="M${x + 3},${ey - 24} L${x - 1},${ey + 22}" stroke="#9b4b3c" stroke-width="3.6" stroke-linecap="round"/>
            <path d="M${x - 4},${ey - 14} L${x + 7},${ey - 13} M${x - 5},${ey + 12} L${x + 5},${ey + 13}" stroke="#9b4b3c" stroke-width="2" stroke-linecap="round"/>`;
      continue;
    }
    // ojo anguloso estilo Toriyama
    const top = o.angry ? `M${x - 12},${ey - 1 - (k > 0 ? 3 : 0)} L${x + 12},${ey - 1 - (k < 0 ? 3 : 0)}` : `M${x - 12},${ey - 2} Q${x},${ey - 10} ${x + 12},${ey - 2}`;
    s += `<path d="${top} L${x + 11},${ey + 6} Q${x},${ey + 9} ${x - 11},${ey + 6} Z" fill="#fff" stroke="${OL}" stroke-width="2"/>
          <ellipse cx="${x + k * 1 + (o.lookX || 0)}" cy="${ey + 2 + (o.lookY || 0)}" rx="${o.calm ? 5 : 5.5}" ry="6.5" fill="${o.iris}"/>
          ${o.noPupil ? '' : `<ellipse cx="${x + k * 1 + (o.lookX || 0)}" cy="${ey + 3 + (o.lookY || 0)}" rx="2.6" ry="3.4" fill="${OL}"/>`}
          <circle cx="${x + k * 1 - 2 + (o.lookX || 0)}" cy="${ey + (o.lookY || 0)}" r="1.6" fill="#fff"/>
          <path d="${top}" fill="none" stroke="${OL}" stroke-width="3.4" stroke-linecap="round"/>`;
    if (o.veins) s += `<path d="M${x + k * 14},${ey + 2} l${k * 6},6 M${x - 8},${ey + 12} q${k * 6},4 ${k * 14},2" fill="none" stroke="${OL}" stroke-opacity=".5" stroke-width="2" stroke-linecap="round"/>`;
  }
  // cejas
  for (const k of [-1, 1]) {
    const x = cx + k * ex;
    const inner = o.angry ? ey - 8 : ey - 16, outer = o.angry ? ey - 20 : ey - 17;
    s += `<path d="M${x - k * 12},${inner} Q${x},${ey - 19} ${x + k * 13},${outer}" fill="none" stroke="${o.brow || OL}" stroke-width="5" stroke-linecap="round"/>`;
  }
  if (o.majinM) s += `<path d="M190,130 L190,118 L200,126 L210,118 L210,130" fill="none" stroke="${OL}" stroke-width="3.4" stroke-linejoin="round"/>`;
  s += `<path d="M${cx + 2},${ey + 12} Q${cx + 7},${ey + 22} ${cx},${ey + 25}" fill="none" stroke="${OL}" stroke-opacity=".55" stroke-width="2.4" stroke-linecap="round"/>`;
  if (o.mouth === 'smile') s += `<path d="M${cx - 13},${ey + 34} Q${cx},${ey + 46} ${cx + 13},${ey + 34}" fill="#fff" stroke="${OL}" stroke-width="3" stroke-linecap="round"/>`;
  else if (o.mouth === 'smirk') s += `<path d="M${cx - 12},${ey + 38} Q${cx + 2},${ey + 41} ${cx + 15},${ey + 31}" fill="none" stroke="${OL}" stroke-width="3" stroke-linecap="round"/>`;
  else if (o.mouth === 'grit') s += `<path d="M${cx - 14},${ey + 33} L${cx + 14},${ey + 33} L${cx + 12},${ey + 42} L${cx - 12},${ey + 42} Z" fill="#fff" stroke="${OL}" stroke-width="2.6"/><path d="M${cx - 14},${ey + 37.5} L${cx + 14},${ey + 37.5}" stroke="${OL}" stroke-width="1.6"/>`;
  else s += `<path d="M${cx - 10},${ey + 38} Q${cx},${ey + 36} ${cx + 10},${ey + 38}" fill="none" stroke="${OL}" stroke-width="3" stroke-linecap="round"/>`;
  if (o.lips) s += `<path d="M${cx - 9},${ey + 37} Q${cx},${ey + 42} ${cx + 9},${ey + 37}" fill="none" stroke="${o.lips}" stroke-width="3" stroke-linecap="round"/>`;
  s += hair(o, cx, cy);
  if (o.headExtra) s += o.headExtra;
  return s;
}

// ---------- aura (detrás) ----------
function aura(c, op = 0.55) {
  const d = 'M200,-30 L232,60 L282,10 L286,120 L340,90 L318,220 L364,230 L322,360 L350,470 L300,470 L310,600 L200,560 L90,600 L100,470 L50,470 L78,360 L36,230 L82,220 L60,90 L114,120 L118,10 L168,60 Z';
  return `<g class="aura"><path d="${d}" fill="${c}" fill-opacity="${op}"/><path d="${d}" fill="none" stroke="${c}" stroke-opacity=".9" stroke-width="5" stroke-linejoin="round" transform="translate(200,300) scale(.86) translate(-200,-300)" fill-opacity="0"/></g>`;
}

// ---------- cuerpo ----------
function person(o) {
  let back = '', front = '';
  const pose = o.pose || 'stand';
  if (o.aura) back += aura(o.aura, o.auraOp);
  const legW = 38;
  let L = [[182, 440], [168, 525], [160, 598]], R = [[218, 440], [232, 525], [240, 598]];
  if (pose === 'run') { L = [[182, 440], [170, 525], [160, 598]]; R = [[218, 440], [250, 492], [238, 556]]; }
  if (pose === 'run2') { R = [[218, 440], [230, 525], [240, 598]]; L = [[182, 440], [150, 492], [162, 556]]; }
  back += limb(L, o.bare ? 30 : legW, o.bottom) + limb(R, o.bare ? 30 : legW, o.bottom);
  back += ln([[176, 455], [168, 525], [162, 570]], 9, OL, .16);
  // botas
  if (o.boots) {
    for (const leg of [L, R]) back += limb([lerp(leg[1], leg[2], .45), leg[2]], legW + 6, o.boots);
    if (o.bootTie) for (const leg of [L, R]) { const p = lerp(leg[1], leg[2], .5); back += `<path d="M${p[0] - 22},${p[1]} L${p[0] + 22},${p[1] - 2}" stroke="${o.bootTie}" stroke-width="5"/>`; }
  }
  for (const [x, k, leg] of [[160, -1, L], [240, 1, R]]) {
    const a = k < 0 ? 8 : 0, b = k > 0 ? 8 : 0;
    back += `<g transform="translate(${leg[2][0] - x},${leg[2][1] - 598})">`;
    const d = `M${x - 20 - a},608 Q${x - 22 - a},623 ${x - 6},623 L${x + 8},623 Q${x + 22 + b},623 ${x + 20 + b},608 Q${x + 12},588 ${x},588 Q${x - 12},588 ${x - 20 - a},608 Z`;
    back += `<path d="${d}" fill="${o.shoes}" stroke="${OL}" stroke-width="3"/>`;
    if (o.toe) back += `<path d="M${x - 20 - a},610 Q${x - 22 - a},623 ${x - 6},623 L${x + 8},623 Q${x + 22 + b},623 ${x + 20 + b},610 Z" fill="${o.toe}" stroke="${OL}" stroke-width="2.6"/>`;
    if (o.sole) back += `<path d="M${x - 22 - a + 6},619 L${x + 22 + b - 6},619" stroke="${o.sole}" stroke-width="5" stroke-linecap="round"/>`;
    back += '</g>';
  }
  // cadera
  back += `<path d="M156,415 L244,415 L250,472 L206,478 L200,452 L194,478 L150,472 Z" fill="${o.bottom}" stroke="${OL}" stroke-width="3" stroke-linejoin="round"/>`;
  if (o.shorts) back += `<path d="M154,415 L246,415 L258,500 Q230,508 206,502 L200,470 L194,502 Q170,508 142,500 Z" fill="${o.shorts}" stroke="${OL}" stroke-width="3" stroke-linejoin="round"/><path d="M226,430 L240,500" stroke="#fff" stroke-opacity=".14" stroke-width="10"/>`;
  // torso
  const torso = `M146,232 Q200,214 254,232 Q262,300 246,360 Q240,400 242,440 L158,440 Q160,400 154,360 Q138,300 146,232 Z`;
  back += `<rect x="186" y="196" width="28" height="34" fill="${o.skin}" stroke="${OL}" stroke-width="3"/>`;
  back += `<path d="${torso}" fill="${o.topC}" stroke="${OL}" stroke-width="3.2"/>`;
  back += `<path d="M232,232 Q262,300 246,360 Q240,400 242,440 L222,440 Q232,360 232,232 Z" ${fsh(0.18)}/>`;
  if (o.abs) back += `<path d="M168,262 Q186,276 198,262 M202,262 Q214,276 232,262" fill="none" stroke="${OL}" stroke-opacity=".35" stroke-width="3" stroke-linecap="round"/><path d="M200,290 L200,384 M182,318 L218,318 M184,346 L216,346 M186,372 L214,372" stroke="${OL}" stroke-opacity=".22" stroke-width="2.6" stroke-linecap="round"/>`;
  if (o.top === 'goku') {
    back += `<path d="M172,222 L200,300 L228,222 Q200,232 172,222 Z" fill="${o.under}" stroke="${OL}" stroke-width="3" stroke-linejoin="round"/>
             <path d="M172,222 L200,300 L228,222" fill="none" stroke="${OL}" stroke-width="3"/>`;
    if (o.emblem) back += `<circle cx="226" cy="268" r="15" fill="#fbf6ea" stroke="${OL}" stroke-width="2.6"/><text x="226" y="275.5" font-size="19" font-weight="900" text-anchor="middle" fill="${OL}" font-family="'Yu Gothic','MS Gothic',sans-serif">${o.emblem}</text>`;
  }
  if (o.top === 'tank') {
    back += `<path d="M146,232 Q160,236 172,226 Q176,262 154,284 Z M254,232 Q240,236 228,226 Q224,262 246,284 Z" fill="${o.skin}" stroke="${OL}" stroke-width="2.6"/>
             <path d="M178,222 Q200,248 222,222" fill="${o.skin}" stroke="${OL}" stroke-width="2.6"/>`;
  }
  if (o.bib) back += `<rect x="170" y="300" width="60" height="46" rx="4" fill="#f7f5ef" stroke="${OL}" stroke-width="2.6"/><text x="200" y="334" font-size="28" text-anchor="middle" fill="${OL}" font-family="Anton">${o.bib}</text><circle cx="175" cy="305" r="2" fill="${OL}"/><circle cx="225" cy="305" r="2" fill="${OL}"/>`;
  if (o.top === 'suit') { // traje saiyajin con cuello
    back += `<path d="M176,222 Q200,234 224,222" fill="none" stroke="${OL}" stroke-width="3"/>`;
  }
  if (o.armor) { // armadura saiyajin
    back += `<path d="M150,236 Q200,222 250,236 L248,300 Q246,330 236,342 Q200,352 164,342 Q154,330 152,300 Z" fill="#f4f2ec" stroke="${OL}" stroke-width="3"/>
             <path d="M164,250 Q200,240 236,250 M200,258 L200,336" fill="none" stroke="${OL}" stroke-opacity=".25" stroke-width="3"/>
             <path d="M236,250 L248,300 Q246,330 236,342 L222,346 Q240,300 236,250 Z" ${fsh(0.12)}/>
             <path d="M158,346 L242,346 L248,410 L152,410 Z" fill="${o.armor}" stroke="${OL}" stroke-width="3"/>
             <path d="M156,368 L244,368 M154,390 L246,390 M200,346 L200,410" stroke="${OL}" stroke-opacity=".45" stroke-width="2.4"/>`;
  }
  // cinturón
  if (o.belt) {
    back += `<path d="M152,404 L248,404 L248,426 L152,426 Z" fill="${o.belt}" stroke="${OL}" stroke-width="2.6"/>
             <path d="M196,426 L186,476 L198,476 L206,426 M206,426 L222,470 L232,464 L216,426" fill="${o.belt}" stroke="${OL}" stroke-width="2.4"/>`;
  }
  if (o.robe) { // túnica larga (Whis)
    back += `<path d="M150,400 L250,400 L282,606 Q200,618 118,606 Z" fill="${o.topC}" stroke="${OL}" stroke-width="3.2" stroke-linejoin="round"/>
             <path d="M236,410 L268,604 L240,608 Z" ${fsh(0.16)}/>
             <path d="M176,230 L224,230 L220,420 L180,420 Z" fill="${o.robe}" stroke="${OL}" stroke-width="2.6"/>
             <path d="M200,276 L212,296 L200,316 L188,296 Z" fill="#f29b2c" stroke="${OL}" stroke-width="2.4"/>
             <path d="M180,420 L220,420 L230,604 L170,604 Z" fill="${o.robe}" stroke="${OL}" stroke-width="2.6"/>
`;
  }
  back += (o.mid || '');
  // brazos
  let LA, RA;
  if (pose === 'guard') { LA = [[150, 240], [140, 330], [176, 268]]; RA = [[250, 240], [262, 326], [244, 236]]; }
  else if (pose === 'punch') { LA = [[150, 240], [140, 330], [176, 268]]; RA = [[250, 240], [322, 236], [396, 230]]; }
  else if (pose === 'run') { LA = [[150, 240], [126, 300], [160, 252]]; RA = [[250, 240], [272, 320], [292, 372]]; }
  else if (pose === 'run2') { RA = [[250, 240], [274, 300], [240, 252]]; LA = [[150, 240], [128, 320], [108, 372]]; }
  else if (pose === 'up') { LA = [[150, 240], [126, 160], [118, 80]]; RA = [[250, 240], [272, 330], [262, 404]]; }
  else if (pose === 'phone') { LA = [[150, 240], [134, 330], [140, 404]]; RA = [[250, 240], [266, 322], [222, 286]]; }
  else if (pose === 'point') { LA = [[150, 240], [134, 330], [140, 404]]; RA = [[250, 240], [304, 206], [356, 172]]; }
  else if (pose === 'scratch') { LA = [[150, 240], [134, 330], [140, 404]]; RA = [[250, 240], [292, 190], [240, 112]]; }
  else if (pose === 'cross') { LA = [[150, 242], [132, 318], [232, 300]]; RA = [[250, 242], [268, 320], [168, 310]]; }
  else { LA = [[150, 240], [134, 330], [140, 404]]; RA = [[250, 240], [266, 330], [262, 404]]; }
  const armW = o.bare ? 28 : 32;
  const armSeg = (A) => {
    let s = limb(A, armW, o.sleeve === 'long' ? (o.sleeveC || o.topC) : o.skin);
    if (o.bandR && A === RA) { { const P = lerp(A[0], A[1], .46), Q = lerp(A[0], A[1], .58), dx = A[1][0] - A[0][0], dy = A[1][1] - A[0][1], L = Math.hypot(dx, dy), nx = -dy / L * (armW / 2 + 3), ny = dx / L * (armW / 2 + 3);
      s += `<path d="M${P[0] + nx},${P[1] + ny} L${Q[0] + nx},${Q[1] + ny} L${Q[0] - nx},${Q[1] - ny} L${P[0] - nx},${P[1] - ny} Z" fill="${o.bandR}" stroke="${OL}" stroke-width="3" stroke-linejoin="round"/>`; } s += `<path d="M${lerp(A[0], A[1], .5).join(',')} l14,10 m-14,-10 l18,-2" stroke="${OL}" stroke-width="7" stroke-linecap="round"/><path d="M${lerp(A[0], A[1], .5).join(',')} l14,10 m-14,-10 l18,-2" stroke="${o.bandR}" stroke-width="3.5" stroke-linecap="round"/>`; }
    if (o.sleeve === 'short') s += limb([A[0], lerp(A[0], A[1], .45)], armW + 8, o.under || o.topC);
    if (o.cuff) s += pose === 'cross' ? limb([lerp(A[1], A[2], .72), lerp(A[1], A[2], .88)], armW + 7, o.cuff) : limb([lerp(A[1], A[2], .5), lerp(A[1], A[2], .8)], armW + 7, o.cuff);
    return s;
  };
  front += armSeg(LA) + armSeg(RA);
  if (o.pads) for (const k of [-1, 1]) front += `<path d="M${200 + k * 34},228 Q${200 + k * 70},218 ${200 + k * 78},250 Q${200 + k * 60},262 ${200 + k * 36},252 Z" fill="${o.pads}" stroke="${OL}" stroke-width="3"/>`;
  for (const [x, y] of [LA[2], RA[2]]) {
    front += `<rect x="${x - 16}" y="${y - 17}" width="32" height="32" rx="12" fill="${o.glove || o.skin}" stroke="${OL}" stroke-width="3"/>
              <path d="M${x - 8},${y - 16} L${x - 8},${y - 6} M${x},${y - 17} L${x},${y - 6} M${x + 8},${y - 16} L${x + 8},${y - 6}" stroke="${OL}" stroke-opacity=".4" stroke-width="2"/>`;
  }
  if (o.ring) back += `<ellipse cx="200" cy="214" rx="58" ry="16" fill="none" stroke="${OL}" stroke-width="15"/><ellipse cx="200" cy="214" rx="58" ry="16" fill="none" stroke="${o.ring}" stroke-width="10"/>`;
  return (o.behind || '') + back + head(o) + front + (o.over || '');
}

// ---------- Babidi (bajito, cabezón) ----------
function babidi() {
  let s = '';
  const skin = '#d9c98a', suit = '#2f2a5c', OLs = `stroke="${OL}"`;
  s += `<g transform="translate(200,620) scale(1.05) translate(-200,-620)">`;
  // capa
  s += `<path d="M150,330 Q120,470 116,610 L284,610 Q280,470 250,330 Z" fill="#1d1838" ${OLs} stroke-width="3"/>`;
  // piernas y zapatos
  s += limb([[184, 520], [178, 598]], 26, suit) + limb([[216, 520], [222, 598]], 26, suit);
  for (const x of [176, 224]) s += `<path d="M${x - 18},612 Q${x - 18},596 ${x},594 Q${x + 18},596 ${x + 20},612 Z" fill="#7a5a2e" ${OLs} stroke-width="3"/>`;
  // cuerpo panzón
  s += `<path d="M158,340 Q140,430 160,520 L240,520 Q260,430 242,340 Q200,326 158,340 Z" fill="${suit}" ${OLs} stroke-width="3.2"/>`;
  s += `<path d="M226,340 Q258,430 240,520 L220,520 Q240,430 226,340 Z" ${fsh(.2)}/>`;
  s += `<path d="M168,340 Q200,368 232,340 L226,330 Q200,344 174,330 Z" fill="#e7dfc8" ${OLs} stroke-width="2.6"/>`;
  s += `<path d="M160,452 L240,452" stroke="#8a7bd0" stroke-width="6"/>`;
  // brazos (uno señalando)
  s += limb([[160, 352], [128, 410], [118, 452]], 22, suit);
  s += limb([[240, 352], [276, 330], [312, 300]], 22, suit);
  s += `<circle cx="116" cy="460" r="13" fill="${skin}" ${OLs} stroke-width="3"/>`;
  s += `<rect x="300" y="286" width="26" height="26" rx="9" fill="${skin}" ${OLs} stroke-width="3" transform="rotate(-35 313 299)"/>`;
  s += `<path d="M318,290 L340,268" stroke="${OL}" stroke-width="12" stroke-linecap="round"/><path d="M318,290 L340,268" stroke="${skin}" stroke-width="7" stroke-linecap="round"/>`;
  // cabeza grande y arrugada, orejas puntiagudas
  s += `<path d="M118,190 L60,150 L118,232 Z M282,190 L340,150 L282,232 Z" fill="${skin}" ${OLs} stroke-width="3" stroke-linejoin="round"/>`;
  s += `<path d="M120,200 Q112,110 200,96 Q288,110 280,200 Q284,290 236,332 Q200,348 164,332 Q116,290 120,200 Z" fill="${skin}" ${OLs} stroke-width="3.4"/>`;
  s += `<path d="M280,200 Q284,290 236,332 Q200,348 182,340 Q256,300 262,190 Q262,140 240,112 Q284,140 280,200 Z" ${fsh(.15)}/>`;
  // arrugas de la frente y la M
  s += `<path d="M150,150 Q200,138 250,150 M156,168 Q200,158 244,168" fill="none" stroke="${OL}" stroke-opacity=".35" stroke-width="2.6"/>`;
  s += `<path d="M184,196 L184,176 L200,190 L216,176 L216,196" fill="none" stroke="${OL}" stroke-width="4" stroke-linejoin="round"/>`;
  // ojos grandes con bolsas
  for (const k of [-1, 1]) {
    const x = 200 + k * 34;
    s += `<ellipse cx="${x}" cy="232" rx="20" ry="17" fill="#fff" ${OLs} stroke-width="2.6"/><circle cx="${x + k * 2}" cy="234" r="8" fill="${OL}"/><circle cx="${x + k * 2 - 3}" cy="230" r="2.4" fill="#fff"/>
          <path d="M${x - 20},226 Q${x},212 ${x + 20},226" fill="${skin}" ${OLs} stroke-width="2.6"/>
          <path d="M${x - 16},256 Q${x},266 ${x + 16},256" fill="none" stroke="${OL}" stroke-opacity=".4" stroke-width="2.4"/>`;
  }
  s += `<path d="M196,248 Q206,266 194,274" fill="none" stroke="${OL}" stroke-opacity=".55" stroke-width="2.6"/>`;
  // sonrisa malvada
  s += `<path d="M160,288 Q200,322 244,284 Q236,308 200,314 Q170,310 160,288 Z" fill="#3a1820" ${OLs} stroke-width="2.6"/><path d="M168,294 Q200,310 236,292 L232,300 Q200,312 172,302 Z" fill="#f7f2e4"/>`;
  s += `</g>`;
  return s;
}

// ---------- Whis: bastón ----------
const whisStaff = `<path d="M300,120 L300,616" stroke="${OL}" stroke-width="11" stroke-linecap="round"/><path d="M300,120 L300,616" stroke="#cfd6e4" stroke-width="6" stroke-linecap="round"/>
  <circle cx="300" cy="84" r="26" fill="#7fe0d6" fill-opacity=".85" stroke="${OL}" stroke-width="3"/><circle cx="292" cy="76" r="7" fill="#fff" opacity=".7"/>
  <path d="M286,118 L314,118 L310,128 L290,128 Z" fill="#e6c24a" stroke="${OL}" stroke-width="2.4"/>`;
const whisHair = `<path d="M166,104 Q156,40 178,-6 Q196,-40 222,-26 Q248,-6 240,56 Q238,88 234,104 Q200,90 166,104 Z" fill="#f4f3f8" stroke="${OL}" stroke-width="3.2"/>
  <path d="M222,-26 Q248,-6 240,56 Q238,88 234,104 Q222,98 214,96 Q232,40 222,-26 Z" ${fsh(.12)}/>
  <path d="M184,60 Q186,20 200,-4" stroke="#fff" stroke-width="5" stroke-linecap="round" fill="none"/>`;

// Paletas
const GI = { topC: '#f26b1d', bottom: '#f26b1d', under: '#1f3c8f', belt: '#2d47b8', boots: '#1f3c8f', shoes: '#1f3c8f', bootTie: '#d8323a', cuff: '#1f3c8f', sleeve: 'short' };
const SAIYAN = { topC: '#24346f', bottom: '#24346f', sleeve: 'long', top: 'suit', glove: '#f4f2ec', cuff: '#f4f2ec', boots: '#f4f2ec', shoes: '#f4f2ec', toe: '#e6b43a' };
const GSKIN = '#f6cfa6';

// =================== ZORO Y EL GPS ===================
// Referencia: Roronoa Zoro post-timeskip — pelo verde corto, ojo izquierdo cerrado con cicatriz vertical,
// 3 aretes dorados en la oreja izquierda, abrigo largo verde oscuro abierto, faja roja anudada, cicatriz diagonal
// en el pecho (hombro izq. -> cadera der.), pañuelo negro en el brazo izquierdo, pantalón oscuro, botas negras,
// 3 katanas en la cadera izquierda: Wado Ichimonji (blanca), Sandai Kitetsu (roja), Enma (negra, mango morado).
const ZSKIN = '#e8b88b', ZCOAT = '#2f5b3c', ZCOAT_D = '#24482f', ZSASH = '#c3262f';
const zoroHair = 'M153,142 Q146,100 166,86 L166,72 L180,80 L186,64 L198,76 L208,60 L216,76 L230,66 L232,84 Q256,98 247,142 L241,124 Q236,110 226,112 L220,100 L210,110 L200,98 L190,110 L180,100 L172,112 Q162,112 159,124 Z';
HAIR.zoro = zoroHair;
const zoroEarrings = [0, 1, 2].map(i => `<path d="M${248 + i * 1.5},${150 + i * 7} q5,2 5,7 q-1,5 -5,4" fill="none" stroke="${OL}" stroke-width="4.4"/><path d="M${248 + i * 1.5},${150 + i * 7} q5,2 5,7 q-1,5 -5,4" fill="none" stroke="#f2c23a" stroke-width="2.4"/>`).join('');
// abrigo: paneles superiores abiertos + faja + falda del abrigo
function zoroCoat(sash = true) {
  const up = (k) => { const X = x => k < 0 ? x : 400 - x; // espejo
    return `<path d="M${X(144)},230 Q${X(160)},222 ${X(180)},224 L${X(166)},404 L${X(150)},404 Q${X(140)},330 ${X(144)},230 Z" fill="${ZCOAT}" stroke="${OL}" stroke-width="3" stroke-linejoin="round"/>`; };
  let s = up(-1) + up(1);
  s += `<path d="M234,224 Q256,232 256,300 L250,404 L234,404 Z" ${fsh(0.2)}/>`;
  // cuello levantado detrás de la nuca
  s += `<path d="M164,226 Q160,206 172,198 L182,224 Z M236,226 Q240,206 228,198 L218,224 Z" fill="${ZCOAT_D}" stroke="${OL}" stroke-width="2.6" stroke-linejoin="round"/>`;
  // cicatriz del pecho con puntadas
  s += `<path d="M228,244 Q206,320 176,392" fill="none" stroke="#a9604c" stroke-width="4" stroke-linecap="round"/>`;
  for (let i = 1; i < 8; i++) { const t = i / 8, x = 228 - 52 * t - 6 * t * t, y = 244 + 148 * t; s += `<path d="M${x - 6},${y - 3} L${x + 6},${y + 3}" stroke="#a9604c" stroke-width="2" stroke-linecap="round"/>`; }
  // falda del abrigo (debajo de la faja)
  s += `<path d="M150,420 L250,420 L272,566 L208,570 L200,500 L192,570 L128,566 Z" fill="${ZCOAT}" stroke="${OL}" stroke-width="3" stroke-linejoin="round"/>
        <path d="M232,422 L272,566 L240,568 Z" ${fsh(0.2)}/>`;
  if (sash) s += `<path d="M150,398 L250,398 L252,428 L148,428 Z" fill="${ZSASH}" stroke="${OL}" stroke-width="2.8" stroke-linejoin="round"/>
        <path d="M150,410 L250,410" stroke="#fff" stroke-opacity=".18" stroke-width="5"/>
        <path d="M160,414 Q148,436 140,486 L156,488 Q160,446 170,426 Z M168,414 Q170,440 168,474 L182,472 Q182,440 176,420 Z" fill="${ZSASH}" stroke="${OL}" stroke-width="2.6" stroke-linejoin="round"/>
        <ellipse cx="166" cy="413" rx="13" ry="11" fill="${ZSASH}" stroke="${OL}" stroke-width="2.6"/>`;
  return s;
}
// 3 katanas en la cadera izquierda: vainas (detrás) y mangos (delante)
const SWORDS = [
  { sh: '#f1efe8', hd: '#f6f4ee', wrap: '#1c1a22', ts: '#e2b23a' },   // Wado Ichimonji
  { sh: '#8e1f27', hd: '#b8323a', wrap: '#2a1416', ts: '#3a3a44' },   // Sandai Kitetsu
  { sh: '#1c1a22', hd: '#6a3d8c', wrap: '#1c1a22', ts: '#e2b23a' },   // Enma
];
const SA = [[236, 424], [245, 421], [254, 424]], SH = [[210, 366], [226, 362], [244, 364]];
function swordsBack() {
  return SWORDS.map((w, i) => { const a = SA[i], b = [316 + i * 16, 600 - i * 8];
    return limb([a, b], 11, w.sh, 5); }).join('');
}
function swordsFront() {
  return SWORDS.map((w, i) => { const a = SA[i], h = SH[i];
    return limb([a, h], 12, w.hd, 5) +
      `<path d="M${lerp(a, h, .25).join(',')} L${lerp(a, h, .35).join(',')} M${lerp(a, h, .5).join(',')} L${lerp(a, h, .6).join(',')} M${lerp(a, h, .75).join(',')} L${lerp(a, h, .85).join(',')}" stroke="${w.wrap}" stroke-width="9" stroke-opacity=".8"/>` +
      `<ellipse cx="${a[0]}" cy="${a[1]}" rx="12" ry="7" transform="rotate(-55 ${a[0]} ${a[1]})" fill="${w.ts}" stroke="${OL}" stroke-width="2.4"/>`; }).join('');
}
const ZORO = { skin: ZSKIN, hair: 'zoro', hairC: '#57ad52', hairHi: '#c4ecb4', hairHiD: 'M176,96 L182,84 M200,90 L206,76 M222,94 L228,82',
  brow: '#2c4a2a', iris: '#2a2a30', angry: true, scarEye: true, mouth: 'smirk',
  top: 'bare', topC: ZSKIN, abs: true, sleeve: 'long', sleeveC: ZCOAT, bandR: '#17151c',
  bottom: '#2b2d36', boots: '#1b1b22', shoes: '#1b1b22', headExtra: zoroEarrings, behind: swordsBack() };
const qMarks = `<g font-family="Anton" font-size="64" fill="#ffd23a" stroke="${OL}" stroke-width="3" paint-order="stroke"><text x="268" y="70" transform="rotate(14 268 70)">?</text><text x="306" y="120" font-size="44" transform="rotate(24 306 120)">?</text><text x="98" y="86" font-size="48" transform="rotate(-16 98 86)">?</text></g>
  <path d="M146,118 q-8,14 0,20 q8,-6 0,-20 Z" fill="#8fd3ff" stroke="${OL}" stroke-width="2"/>`;
const capTaxi = `<path d="M150,128 Q150,84 200,82 Q252,84 252,122 Q236,112 200,112 Q166,112 150,128 Z" fill="#3a3a44" stroke="${OL}" stroke-width="3"/>
  <path d="M150,126 Q196,108 262,124 Q266,134 252,134 Q200,122 152,136 Z" fill="#2a2a32" stroke="${OL}" stroke-width="2.6"/>
  <path d="M158,104 Q200,92 240,104" stroke="#fff" stroke-opacity=".18" stroke-width="5" fill="none"/>
  <path d="M154,140 L154,168 M246,140 L246,168" stroke="#7a7a80" stroke-width="7" stroke-linecap="round"/>`;
const youHair = `<path d="M152,146 Q144,76 200,74 Q258,76 248,146 Q246,108 228,100 L222,118 L210,98 L196,118 L186,98 L174,116 Q156,112 152,146 Z" fill="#4a2f1e" stroke="${OL}" stroke-width="3"/>`;
const phone = `<g transform="rotate(-8 214 262)"><rect x="196" y="232" width="36" height="62" rx="6" fill="#1b1b22" stroke="${OL}" stroke-width="3"/><rect x="200" y="238" width="28" height="48" rx="3" fill="#2f9be6"/>
  <path d="M206,278 L214,252 L222,278 L214,272 Z" fill="#fff"/><path d="M200,262 L228,262" stroke="#9ee0ff" stroke-width="2" opacity=".7"/></g>`;
const mapPaper = `<g transform="rotate(-12 110 300)"><path d="M70,250 L104,258 L138,248 L160,256 L160,340 L138,332 L104,342 L70,334 Z" fill="#f4ead2" stroke="${OL}" stroke-width="3" stroke-linejoin="round"/>
  <path d="M104,258 L104,342 M138,248 L138,332" stroke="${OL}" stroke-opacity=".25" stroke-width="2"/><path d="M80,320 Q100,290 120,300 T150,268" fill="none" stroke="#d8323a" stroke-width="3.5" stroke-dasharray="6 5"/><circle cx="150" cy="268" r="5" fill="#d8323a"/></g>`;
const HOOD = { top: 'suit', topC: '#5b4bc4', sleeve: 'long', bottom: '#2c3550', shoes: '#f4f2ec', sole: '#5b4bc4', skin: '#f2c8a0', hair: 'none', headExtra: youHair, iris: '#3a2a20' };

const CHARS = [
  { id: 'zoro', name: 'RORONOA ZORO', sub: 'el espadachín · cazador de piratas', bg: '#14301f', svg: () => person({ ...ZORO, mid: zoroCoat(), over: swordsFront() }) },
  { id: 'zoro_cross', name: 'ZORO · AURA', sub: '"no es tonto": mi opinión', bg: '#0f2a1c', svg: () => person({ ...ZORO, pose: 'cross', mouth: 'smirk', behind: aura('#4fe07a', .4) + swordsBack(), mid: zoroCoat(), over: swordsFront() }) },
  { id: 'zoro_lost', name: 'ZORO PERDIDO', sub: 'se pierde hasta en línea recta', bg: '#2b2a12', svg: () => person({ ...ZORO, pose: 'scratch', angry: false, lookX: -4, mouth: 'flat', mid: zoroCoat(), over: swordsFront() + qMarks }) },
  { id: 'taxista', name: 'TAXISTA DE LONDRES', sub: '25 000 calles en la cabeza', bg: '#1a1d2c', svg: () => person({ top: 'suit', topC: '#2e3a52', sleeve: 'long', bottom: '#23252e', shoes: '#16161c', skin: '#efc29c', hair: 'none', headExtra: capTaxi, iris: '#4a5a7a', mouth: 'smile', pose: 'point', over: `<path d="M178,224 L200,262 L222,224" fill="#e9e6df" stroke="${OL}" stroke-width="2.6"/><path d="M196,236 L204,236 L206,300 L200,310 L194,300 Z" fill="#8e1f27" stroke="${OL}" stroke-width="2"/>` }) },
  { id: 'tu_gps', name: 'TÚ CON GPS', sub: 'solo obedeces las flechas', bg: '#10243a', svg: () => person({ ...HOOD, pose: 'phone', lookY: 4, lookX: 2, calm: true, mouth: 'flat', over: phone }) },
  { id: 'tu_mapa', name: 'TÚ SIN GPS', sub: 'mapa mental activado', bg: '#2a1830', svg: () => person({ ...HOOD, pose: 'point', angry: true, mouth: 'grit', aura: '#ffd23a', auraOp: .3, over: mapPaper }) },
];
