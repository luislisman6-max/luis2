// Motor de personajes "Vegeta, el rival" — mismo estilo que Black Flash (vector plano, contorno fino, sombra suave).
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
  s += `<path d="M168,70 L180,44 M196,52 L204,20 M226,62 L238,38" stroke="${o.hairHi || '#fff'}" stroke-width="4.5" stroke-linecap="round" opacity=".55"/>`;
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
    // ojo anguloso estilo Toriyama
    const top = o.angry ? `M${x - 12},${ey - 1 - (k > 0 ? 3 : 0)} L${x + 12},${ey - 1 - (k < 0 ? 3 : 0)}` : `M${x - 12},${ey - 2} Q${x},${ey - 10} ${x + 12},${ey - 2}`;
    s += `<path d="${top} L${x + 11},${ey + 6} Q${x},${ey + 9} ${x - 11},${ey + 6} Z" fill="#fff" stroke="${OL}" stroke-width="2"/>
          <ellipse cx="${x + k * 1}" cy="${ey + 2}" rx="${o.calm ? 5 : 5.5}" ry="6.5" fill="${o.iris}"/>
          ${o.noPupil ? '' : `<ellipse cx="${x + k * 1}" cy="${ey + 3}" rx="2.6" ry="3.4" fill="${OL}"/>`}
          <circle cx="${x + k * 1 - 2}" cy="${ey}" r="1.6" fill="#fff"/>
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
  // brazos
  let LA, RA;
  if (pose === 'guard') { LA = [[150, 240], [140, 330], [176, 268]]; RA = [[250, 240], [262, 326], [244, 236]]; }
  else if (pose === 'punch') { LA = [[150, 240], [140, 330], [176, 268]]; RA = [[250, 240], [322, 236], [396, 230]]; }
  else if (pose === 'run') { LA = [[150, 240], [126, 300], [160, 252]]; RA = [[250, 240], [272, 320], [292, 372]]; }
  else if (pose === 'run2') { RA = [[250, 240], [274, 300], [240, 252]]; LA = [[150, 240], [128, 320], [108, 372]]; }
  else if (pose === 'up') { LA = [[150, 240], [126, 160], [118, 80]]; RA = [[250, 240], [272, 330], [262, 404]]; }
  else if (pose === 'cross') { LA = [[150, 242], [132, 318], [232, 300]]; RA = [[250, 242], [268, 320], [168, 310]]; }
  else { LA = [[150, 240], [134, 330], [140, 404]]; RA = [[250, 240], [266, 330], [262, 404]]; }
  const armW = o.bare ? 28 : 32;
  const armSeg = (A) => {
    let s = limb(A, armW, o.sleeve === 'long' ? o.topC : o.skin);
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

const CHARS = [
  { id: 'goku_base', name: 'GOKU', sub: 'base · el que persigue', bg: '#1d3b2a', svg: () => person({ ...GI, top: 'goku', emblem: '悟', skin: GSKIN, hair: 'goku', hairC: '#17151a', hairHi: '#6c6a80', iris: '#1d1c22', mouth: 'smile' }) },
  { id: 'goku_ssj', name: 'SUPER SAIYAJIN', sub: 'Goku · nivel 1', bg: '#3a3010', svg: () => person({ ...GI, top: 'goku', emblem: '亀', pose: 'guard', skin: GSKIN, hair: 'ssj', hairC: '#ffd23a', hairHi: '#fff6c4', brow: '#e0a91c', iris: '#18a39a', angry: true, mouth: 'grit', aura: '#ffd84a' }) },
  { id: 'goku_dios', name: 'SSJ DIOS', sub: 'Goku · nivel dios', bg: '#3a1020', svg: () => person({ ...GI, top: 'goku', emblem: '悟', skin: '#f3c9a2', hair: 'goku', hairScale: .9, hairC: '#d6283f', hairHi: '#ff8a9a', brow: '#b81f33', iris: '#c4283a', calm: true, aura: '#ff3d5a', auraOp: .4 }) },
  { id: 'goku_blue', name: 'SSJ BLUE', sub: 'Goku · dios + saiyajin', bg: '#0f2a46', svg: () => person({ ...GI, top: 'goku', emblem: '悟', pose: 'guard', skin: GSKIN, hair: 'ssj', hairC: '#39b6f2', hairHi: '#c9f0ff', brow: '#1f8fd0', iris: '#2a7fd8', angry: true, mouth: 'smirk', aura: '#3fc3ff' }) },
  { id: 'goku_ui', name: 'ULTRA INSTINTO', sub: 'Goku · dominado', bg: '#1c1f33', svg: () => person({ ...GI, top: 'bare', topC: GSKIN, bare: false, abs: true, sleeve: 'none', skin: GSKIN, hair: 'ui', hairC: '#dfe3ee', hairHi: '#ffffff', brow: '#aab3c6', iris: '#b9c3d6', noPupil: true, calm: true, aura: '#cfd8ff', auraOp: .35 }) },
  { id: 'vegeta', name: 'VEGETA', sub: 'el rival · príncipe saiyajin', bg: '#151c3a', svg: () => person({ ...SAIYAN, pose: 'cross', armor: '#e6b43a', pads: '#e6b43a', skin: GSKIN, hair: 'vegeta', hairC: '#17151a', hairHi: '#6c6a80', iris: '#1d1c22', angry: true, mouth: 'smirk' }) },
  { id: 'vegeta_blue', name: 'VEGETA BLUE', sub: 'siempre lo alcanza', bg: '#0f2a46', svg: () => person({ ...SAIYAN, pose: 'guard', armor: '#e6b43a', skin: GSKIN, hair: 'vegeta', hairC: '#39b6f2', hairHi: '#c9f0ff', brow: '#1f8fd0', iris: '#2a7fd8', angry: true, mouth: 'grit', aura: '#3fc3ff' }) },
  { id: 'majin_vegeta', name: 'MAJIN VEGETA', sub: 'el lado oscuro del rival', bg: '#2a0f2a', svg: () => person({ ...SAIYAN, sleeve: 'none', bare: false, skin: GSKIN, hair: 'vegeta', hairC: '#ffd23a', hairHi: '#fff6c4', brow: '#e0a91c', iris: '#18a39a', angry: true, veins: true, majinM: true, mouth: 'smirk', aura: '#ffd84a', auraOp: .4, behind: `<path d="M120,200 L40,150 L90,260 L20,300 L110,330 Z M280,200 L360,150 L310,260 L380,300 L290,330 Z" fill="#7a1f6b" fill-opacity=".5"/>` }) },
  { id: 'babidi', name: 'BABIDI', sub: 'el mago que lo controló', bg: '#1f1330', svg: babidi },
  { id: 'whis', name: 'WHIS', sub: 'el maestro de los dos', bg: '#1b2440', svg: () => person({ topC: '#6e1d2c', bottom: '#6e1d2c', robe: '#17151c', sleeve: 'long', cuff: '#17151c', skin: '#a8c3e8', shoes: '#f4f2ec', hair: 'none', iris: '#7b4fc0', calm: true, mouth: 'smile', lips: '#7b4fc0', ring: '#2f9be6', headExtra: whisHair, over: whisStaff }) },
  { id: 'corredor', name: 'TÚ', sub: 'corredor · estudio de rivalidad', bg: '#2a1616', svg: () => person({ top: 'tank', topC: '#d8323a', bottom: '#b67b52', bare: true, shorts: '#1f2026', skin: '#b67b52', hair: 'none', headExtra: `<path d="M153,144 Q148,84 200,82 Q252,84 247,144 Q240,112 200,110 Q160,112 153,144 Z" fill="#1f1b22" stroke="${OL}" stroke-width="3"/>`, iris: '#1d1c22', bib: '07', shoes: '#f4f2ec', sole: '#d8323a', angry: true, mouth: 'grit' }) },
  { id: 'rival', name: 'TU RIVAL', sub: 'corredor · 5 s/km más rápido', bg: '#141c2e', svg: () => person({ top: 'tank', topC: '#2f74c8', bottom: '#e0b48a', bare: true, shorts: '#1f2026', skin: '#e0b48a', hair: 'none', headExtra: `<path d="M152,146 Q144,76 200,74 Q258,76 248,146 Q246,108 228,100 L222,118 L210,98 L196,118 L186,98 L174,116 Q156,112 152,146 Z" fill="#5a3a22" stroke="${OL}" stroke-width="3"/>`, iris: '#1d1c22', bib: '23', shoes: '#f4f2ec', sole: '#2f74c8', angry: true, mouth: 'smirk' }) },
];
