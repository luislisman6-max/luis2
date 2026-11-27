// Motor de personajes "Black Flash" — vector plano, contorno fino oscuro, sombra suave.
// Coordenadas locales: caja 400x660, centro x=200, pies en y≈620.
const OL = '#15121a';
const sh = (c, a = 0.22) => `fill="${OL}" fill-opacity="${a}"`;

function limb(pts, w, color, out = 5) {
  const d = 'M' + pts.map(p => p.join(',')).join(' L');
  return `<path d="${d}" fill="none" stroke="${OL}" stroke-width="${w + out}" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="${d}" fill="none" stroke="${color}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
}
const ln = (pts, w, color) => `<path d="M${pts.map(p => p.join(',')).join(' L')}" fill="none" stroke="${color}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;

// ---------- cabeza ----------
function head(o) {
  const cx = 200, cy = 150;
  let s = '';
  // orejas
  s += `<ellipse cx="${cx - 44}" cy="${cy + 6}" rx="9" ry="13" fill="${o.skin}" stroke="${OL}" stroke-width="3"/>
        <ellipse cx="${cx + 44}" cy="${cy + 6}" rx="9" ry="13" fill="${o.skin}" stroke="${OL}" stroke-width="3"/>`;
  // cara (mandíbula más angulosa)
  s += `<path d="M${cx - 44},${cy - 20} Q${cx - 46},${cy + 30} ${cx - 30},${cy + 48} Q${cx - 14},${cy + 62} ${cx},${cy + 63} Q${cx + 14},${cy + 62} ${cx + 30},${cy + 48} Q${cx + 46},${cy + 30} ${cx + 44},${cy - 20} Q${cx + 40},${cy - 58} ${cx},${cy - 60} Q${cx - 40},${cy - 58} ${cx - 44},${cy - 20} Z" fill="${o.skin}" stroke="${OL}" stroke-width="3.2"/>`;
  // sombra lateral cara
  s += `<path d="M${cx + 44},${cy - 20} Q${cx + 46},${cy + 30} ${cx + 30},${cy + 48} Q${cx + 14},${cy + 62} ${cx},${cy + 63} Q${cx + 24},${cy + 40} ${cx + 30},${cy} Z" ${sh(0, 0.16)}/>`;
  // ojos
  const ey = cy + 8, ex = 18;
  if (o.eyes === 'anime') {
    for (const k of [-1, 1]) {
      const x = cx + k * ex;
      s += `<path d="M${x - 12},${ey - 2} Q${x},${ey - 11} ${x + 12},${ey - 3} L${x + 11},${ey + 6} Q${x},${ey + 10} ${x - 11},${ey + 6} Z" fill="#fff" stroke="${OL}" stroke-width="2"/>
            <ellipse cx="${x + k * 1}" cy="${ey + 1}" rx="6" ry="7.5" fill="${o.iris}"/>
            <ellipse cx="${x + k * 1}" cy="${ey + 2}" rx="3" ry="4" fill="${OL}"/>
            <circle cx="${x + k * 1 - 2}" cy="${ey - 2}" r="1.8" fill="#fff"/>
            <path d="M${x - 13},${ey - 4} Q${x},${ey - 14} ${x + 13},${ey - 5}" fill="none" stroke="${OL}" stroke-width="3.4" stroke-linecap="round"/>`;
      // marcas bajo los ojos (Yuji)
      if (o.marks) s += `<path d="M${x - 8 * k + (k < 0 ? -2 : 2)},${ey + 13} l${k * 8},2" stroke="${OL}" stroke-width="2.2" stroke-linecap="round"/>`;
    }
  } else {
    for (const k of [-1, 1]) {
      const x = cx + k * ex;
      s += `<ellipse cx="${x}" cy="${ey + 1}" rx="5" ry="6" fill="${OL}"/><circle cx="${x - 1.5}" cy="${ey - 1}" r="1.5" fill="#fff"/>`;
    }
  }
  // cejas
  for (const k of [-1, 1]) {
    const x = cx + k * ex;
    s += `<path d="M${x - k * 12},${ey - 16 + (o.angry ? 4 : 0)} Q${x},${ey - 22} ${x + k * 12},${ey - 17 - (o.angry ? 2 : 0)}" fill="none" stroke="${o.brow || OL}" stroke-width="5" stroke-linecap="round"/>`;
  }
  // nariz y boca
  s += `<path d="M${cx + 2},${ey + 12} Q${cx + 7},${ey + 22} ${cx},${ey + 25}" fill="none" stroke="${OL}" stroke-opacity=".55" stroke-width="2.4" stroke-linecap="round"/>`;
  s += o.smirk
    ? `<path d="M${cx - 12},${ey + 38} Q${cx + 2},${ey + 42} ${cx + 14},${ey + 33}" fill="none" stroke="${OL}" stroke-width="3" stroke-linecap="round"/>`
    : `<path d="M${cx - 11},${ey + 38} Q${cx},${ey + 36} ${cx + 11},${ey + 38}" fill="none" stroke="${OL}" stroke-width="3" stroke-linecap="round"/>`;
  s += hair(o, cx, cy);
  return s;
}

function hair(o, cx, cy) {
  if (o.hair === 'none') return '';
  if (o.hair === 'short') {
    return `<path d="M${cx - 47},${cy - 6} Q${cx - 52},${cy - 66} ${cx - 4},${cy - 70} Q${cx + 48},${cy - 70} ${cx + 48},${cy - 8} Q${cx + 40},${cy - 30} ${cx + 30},${cy - 36} Q${cx},${cy - 26} ${cx - 26},${cy - 34} Q${cx - 40},${cy - 26} ${cx - 47},${cy - 6} Z" fill="${o.hairC}" stroke="${OL}" stroke-width="3"/>
            <path d="M${cx - 20},${cy - 58} Q${cx + 6},${cy - 66} ${cx + 26},${cy - 54}" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="5" stroke-linecap="round"/>`;
  }
  if (o.hair === 'buzz') {
    return `<path d="M${cx - 45},${cy - 4} Q${cx - 50},${cy - 64} ${cx},${cy - 66} Q${cx + 50},${cy - 64} ${cx + 45},${cy - 4} Q${cx + 40},${cy - 34} ${cx},${cy - 38} Q${cx - 40},${cy - 34} ${cx - 45},${cy - 4} Z" fill="${o.hairC}" stroke="${OL}" stroke-width="3"/>`;
  }
  if (o.hair === 'yuji') {
    let s = '';
    // undercut oscuro en sienes
    s += `<path d="M154,146 Q150,120 160,106 L170,110 Q161,124 162,146 Z" fill="#3f2a30" stroke="${OL}" stroke-width="2.4"/>
          <path d="M246,146 Q250,120 240,106 L230,110 Q239,124 238,146 Z" fill="#3f2a30" stroke="${OL}" stroke-width="2.4"/>`;
    const d = 'M158,126 L140,108 L160,102 L136,76 L166,82 L152,48 L180,68 L184,32 L200,60 L214,24 L222,60 L242,34 L242,70 L268,56 L252,90 L272,94 L248,110 L244,126 Q238,120 232,116 L226,136 L214,116 L205,142 L194,116 L182,134 L176,116 Q166,118 158,126 Z';
    s += `<g transform="translate(0,28) scale(1,0.78)">`;
    s += `<path d="${d}" fill="${o.hairC}" stroke="${OL}" stroke-width="3" stroke-linejoin="round"/>`;
    // sombras del pelo
    s += `<path d="M222,60 L242,34 L242,70 L268,56 L252,90 L272,94 L248,110 L244,126 Q238,120 232,116 L236,92 Z" fill="#c9557a" fill-opacity=".6"/>
          <path d="M176,116 L182,134 L194,116 L205,142 L214,116 L226,136 L232,116 Q206,104 176,116 Z" fill="#c9557a" fill-opacity=".45"/>`;
    // brillos
    s += `<path d="M178,74 L184,48 M200,70 L212,40 M166,92 L156,66" stroke="#ffd3df" stroke-width="4" stroke-linecap="round" opacity=".85"/></g>`;
    return s;
  }
  return '';
}

// ---------- cuerpo ----------
function person(o) {
  const C = 200;
  let back = '', front = '', s0;
  const pose = o.pose || 'guard';
  const legW = o.pants ? 38 : 30;
  // piernas
  const L = [[182, 440], [168, 525], [160, 598]], R = [[218, 440], [232, 525], [240, 598]];
  const legC = o.pants ? o.bottom : o.skin;
  back += limb(L, legW, legC) + limb(R, legW, legC);
  if (o.pants) back += ln([[176, 455], [168, 525], [162, 592]], 9, OL).replace('stroke-width="9"', 'stroke-width="9" stroke-opacity=".18"');
  // zapatos
  for (const [x, k] of [[160, -1], [240, 1]]) {
    const fill = o.shoes === 'barefoot' ? o.skin : o.shoes;
    s0 = `M${x - 20 - (k < 0 ? 8 : 0)},608 Q${x - 22 - (k < 0 ? 8 : 0)},623 ${x - 6},623 L${x + 8},623 Q${x + 22 + (k > 0 ? 8 : 0)},623 ${x + 20 + (k > 0 ? 8 : 0)},608 Q${x + 12},590 ${x},590 Q${x - 12},590 ${x - 20 - (k < 0 ? 8 : 0)},608 Z`;
    back += `<path d="${s0}" fill="${fill}" stroke="${OL}" stroke-width="3"/>`;
    if (o.shoes !== 'barefoot') back += `<path d="M${x - 22 - (k < 0 ? 6 : 0)},618 L${x + 22 + (k > 0 ? 6 : 0)},618" stroke="${o.sole || '#e9e6df'}" stroke-width="5" stroke-linecap="round"/>`;
  }
  // parte de abajo
  if (o.top === 'gi') {
    back += `<path d="M156,420 L244,420 L250,470 L206,476 L200,450 L194,476 L150,470 Z" fill="${o.bottom}" stroke="${OL}" stroke-width="3" stroke-linejoin="round"/>`;
  } else if (!o.pants) {
    back += `<path d="M156,415 L244,415 L256,500 Q230,508 206,502 L200,470 L194,502 Q170,508 144,500 Z" fill="${o.bottom}" stroke="${OL}" stroke-width="3" stroke-linejoin="round"/>
             <path d="M156,428 L244,428" stroke="${o.band || OL}" stroke-width="7" opacity=".6"/>
             <path d="M226,430 L240,500" stroke="#fff" stroke-opacity=".12" stroke-width="10"/>`;
  } else {
    back += `<path d="M158,415 L242,415 L246,470 L154,470 Z" fill="${o.bottom}" stroke="${OL}" stroke-width="3"/>`;
  }
  // torso
  const torso = `M146,232 Q200,214 254,232 Q262,300 246,360 Q240,400 242,440 L158,440 Q160,400 154,360 Q138,300 146,232 Z`;
  const topC = o.top === 'none' ? o.skin : o.topC;
  back += `<rect x="186" y="196" width="28" height="34" fill="${o.skin}" stroke="${OL}" stroke-width="3"/>`;
  back += `<path d="${torso}" fill="${topC}" stroke="${OL}" stroke-width="3.2"/>`;
  back += `<path d="M232,232 Q262,300 246,360 Q240,400 242,440 L222,440 Q232,360 232,232 Z" ${sh(0, 0.18)}/>`;
  if (o.top === 'tank') {
    back += `<path d="M146,232 Q160,236 172,226 Q176,262 154,284 Z M254,232 Q240,236 228,226 Q224,262 246,284 Z" fill="${o.skin}" stroke="${OL}" stroke-width="2.6"/>
             <path d="M178,222 Q200,248 222,222" fill="${o.skin}" stroke="${OL}" stroke-width="2.6"/>`;
  }
  if (o.top === 'none') {
    back += `<path d="M168,262 Q186,276 198,262 M202,262 Q214,276 232,262" fill="none" stroke="${OL}" stroke-opacity=".35" stroke-width="3" stroke-linecap="round"/>
             <path d="M200,290 L200,380 M182,320 L218,320 M184,350 L216,350" stroke="${OL}" stroke-opacity=".2" stroke-width="2.6" stroke-linecap="round"/>`;
  }
  if (o.top === 'tee') {
    back += `<path d="M178,222 Q200,240 222,222" fill="none" stroke="${OL}" stroke-width="3"/>`;
  }
  if (o.top === 'gi') {
    back += `<path d="M176,224 L208,330 L224,224" fill="none" stroke="${OL}" stroke-width="3"/>
             <path d="M178,224 L206,312" stroke="#d5d2c8" stroke-width="8"/>
             <path d="M152,404 L248,404 L248,424 L152,424 Z" fill="#1b1a1f" stroke="${OL}" stroke-width="2.6"/>
             <path d="M204,424 L194,470 L206,470 L212,424 M212,424 L226,466 L236,462 L220,424" fill="#1b1a1f" stroke="${OL}" stroke-width="2.4"/>`;
  }
  if (o.top === 'uniform') {
    // uniforme de la escuela: cuello alto, cremallera, capucha roja
    back += `<path d="M150,228 Q140,200 172,196 Q200,206 228,196 Q260,200 250,228 Q230,214 200,222 Q170,214 150,228 Z" fill="${o.hood}" stroke="${OL}" stroke-width="3"/>
             <path d="M170,200 Q200,190 230,200 L232,236 Q200,246 168,236 Z" fill="${o.topC}" stroke="${OL}" stroke-width="3"/>
             <path d="M200,240 L200,440" stroke="${OL}" stroke-opacity=".5" stroke-width="2.4"/>
             <path d="M160,430 L240,430" stroke="${OL}" stroke-opacity=".4" stroke-width="3"/>
             <circle cx="216" cy="220" r="7" fill="#e8c24a" stroke="${OL}" stroke-width="2"/>
             <path d="M216,220 m-3,0 a3,3 0 1,1 3,3" fill="none" stroke="#8a6a12" stroke-width="1.6"/>
             <path d="M152,286 Q170,296 186,290" fill="none" stroke="#fff" stroke-opacity=".08" stroke-width="6"/>`;
  }
  // brazos
  let LA, RA, fistL, fistR;
  if (pose === 'guard') {
    LA = [[150, 240], [146, 326], [170, 200]]; RA = [[250, 240], [254, 326], [230, 200]];
  } else if (pose === 'punch') {
    LA = [[150, 240], [146, 326], [170, 200]]; RA = [[250, 240], [324, 236], [396, 230]];
  } else if (pose === 'punchL') {
    LA = [[150, 240], [76, 236], [4, 230]]; RA = [[250, 240], [254, 326], [230, 200]];
  } else {
    LA = [[150, 240], [134, 330], [140, 404]]; RA = [[250, 240], [266, 330], [262, 404]];
  }
  fistL = LA[2]; fistR = RA[2];
  const armW = o.top === 'none' || o.top === 'tank' ? 28 : 32;
  const sleeveC = { tee: o.topC, gi: o.topC, uniform: o.topC }[o.top];
  const armSeg = (A) => {
    let s = limb(A, armW, o.skin);
    if (sleeveC && o.top !== 'tee') s = limb(A, armW + 6, sleeveC);
    if (o.top === 'tee') s += limb([A[0], [(A[0][0] + A[1][0]) / 2, (A[0][1] + A[1][1]) / 2]], armW + 8, sleeveC);
    return s;
  };
  front += armSeg(LA) + armSeg(RA);
  // puños
  for (const [x, y] of [fistL, fistR]) {
    if (o.gloves === 'wrap') {
      front += `<rect x="${x - 17}" y="${y - 19}" width="34" height="36" rx="12" fill="${o.skin}" stroke="${OL}" stroke-width="3"/>
                <path d="M${x - 16},${y - 6} L${x + 16},${y - 10} M${x - 16},${y + 4} L${x + 16},${y} M${x - 16},${y + 13} L${x + 16},${y + 9}" stroke="${o.wrapC}" stroke-width="6"/>
                <rect x="${x - 17}" y="${y - 19}" width="34" height="36" rx="12" fill="none" stroke="${OL}" stroke-width="3"/>`;
    } else if (o.gloves === 'mma') {
      front += `<rect x="${x - 18}" y="${y - 20}" width="36" height="34" rx="13" fill="#1d1c22" stroke="${OL}" stroke-width="3"/>
                <rect x="${x - 16}" y="${y + 12}" width="32" height="10" rx="3" fill="#2c2b33" stroke="${OL}" stroke-width="2.4"/>
                <path d="M${x - 10},${y - 12} Q${x},${y - 16} ${x + 10},${y - 12}" stroke="#fff" stroke-opacity=".25" stroke-width="3" fill="none"/>`;
    } else {
      if (o.aura) front += `<circle class="aura" cx="${x}" cy="${y}" r="36" fill="url(#auraBlue)"/>`;
      front += `<rect x="${x - 16}" y="${y - 17}" width="32" height="32" rx="12" fill="${o.skin}" stroke="${OL}" stroke-width="3"/>
                <path d="M${x - 8},${y - 16} L${x - 8},${y - 6} M${x},${y - 17} L${x},${y - 6} M${x + 8},${y - 16} L${x + 8},${y - 6}" stroke="${OL}" stroke-opacity=".4" stroke-width="2"/>`;
      if (o.aura) front += `<path d="M${x - 14},${y - 4} q6,-10 12,-2 q6,-12 14,0" fill="none" stroke="#bfe9ff" stroke-width="3" stroke-linecap="round"/>`;
    }
  }
  // sensores (MMA)
  if (o.sensors) {
    for (const [x, y] of [[156, 262], [244, 262], [132, 300], [268, 300], [176, 360], [224, 360]])
      front += `<rect x="${x - 7}" y="${y - 7}" width="14" height="14" rx="3" fill="#e9f4f7" stroke="${OL}" stroke-width="2"/><circle cx="${x}" cy="${y}" r="3" fill="#36d3e6"/>`;
  }
  return back + head(o) + front;
}

// ---------- maldición ----------
function curse() {
  let s = '';
  // tentáculos
  s += limb([[150, 470], [120, 540], [140, 612]], 34, '#5b437c') + limb([[250, 470], [282, 545], [262, 614]], 34, '#5b437c');
  s += limb([[100, 330], [36, 380], [44, 470]], 30, '#5b437c') + limb([[300, 320], [366, 366], [362, 452]], 30, '#5b437c');
  // cuerpo blob
  const body = 'M200,130 Q262,118 300,170 Q340,230 318,320 Q306,400 330,470 Q300,520 200,510 Q100,520 72,468 Q96,400 84,322 Q62,230 104,170 Q140,124 200,130 Z';
  s += `<path d="${body}" fill="#6e5394" stroke="${OL}" stroke-width="3.5"/>`;
  s += `<path d="M300,170 Q340,230 318,320 Q306,400 330,470 Q300,520 250,514 Q300,420 290,300 Q288,220 300,170 Z" ${sh(0, 0.22)}/>`;
  s += `<path d="M130,180 Q160,150 200,150" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="10" stroke-linecap="round"/>`;
  // ojos
  for (const [x, y, r] of [[160, 210, 15], [222, 196, 18], [272, 236, 13], [128, 262, 11], [200, 262, 12], [250, 292, 10], [156, 316, 9]]) {
    s += `<circle cx="${x}" cy="${y}" r="${r}" fill="#f6d33c" stroke="${OL}" stroke-width="2.6"/><circle cx="${x + 1}" cy="${y + 1}" r="${r * 0.42}" fill="${OL}"/><circle cx="${x - r * 0.3}" cy="${y - r * 0.35}" r="${r * 0.18}" fill="#fff"/>`;
  }
  // boca con dientes
  s += `<path d="M120,372 Q200,410 284,368 Q262,430 200,436 Q138,430 120,372 Z" fill="#1a0f22" stroke="${OL}" stroke-width="3"/>`;
  let t = 'M126,378';
  for (let i = 0; i < 12; i++) { const x = 130 + i * 13; t += ` L${x + 6},${396 + (i % 2)} L${x + 13},${382 + Math.sin(i / 11 * Math.PI) * 10}`; }
  s += `<path d="${t}" fill="#f4efe2" stroke="${OL}" stroke-width="1.6" stroke-linejoin="round"/>`;
  return s;
}

const CHARS = [
  { id: 'boxeador', name: 'EL BOXEADOR', sub: 'protagonista · gimnasio', svg: () => person({ skin: '#b67b52', hair: 'short', hairC: '#1f1b22', top: 'tank', topC: '#34373f', bottom: '#202127', band: '#d8323a', gloves: 'wrap', wrapC: '#d8323a', shoes: '#26262c', sole: '#bdbab3', angry: true }) },
  { id: 'yuji', name: 'YUJI ITADORI', sub: 'fan art · energía maldita', svg: () => person({ pose: 'stand', skin: '#f2d0b4', hair: 'yuji', hairC: '#f18aa5', eyes: 'anime', iris: '#a5652a', marks: true, smirk: true, top: 'uniform', topC: '#1d2336', hood: '#c8323c', bottom: '#1a1f30', pants: true, shoes: '#d0313a', sole: '#f2efe6', aura: true, brow: '#4a2f36' }) },
  { id: 'maldicion', name: 'LA MALDICIÓN', sub: 'espíritu maldito', svg: curse },
  { id: 'karateka', name: 'CINTURÓN NEGRO', sub: 'karateka · estudio de Londres', svg: () => person({ skin: '#a8714a', hair: 'short', hairC: '#1b181d', top: 'gi', topC: '#eeece6', bottom: '#eeece6', pants: true, shoes: 'barefoot' }) },
  { id: 'gym', name: 'CHICO DEL GYM', sub: 'principiante · estudio de Londres', svg: () => person({ skin: '#c48a5c', hair: 'buzz', hairC: '#3a2a22', top: 'tee', topC: '#2f74c8', bottom: '#1f2026', shoes: '#e8e6e0', sole: '#9c9a94' }) },
  { id: 'mma', name: 'PELEADOR MMA', sub: 'élite · sensores musculares', svg: () => person({ skin: '#9a6440', hair: 'buzz', hairC: '#151317', top: 'none', bottom: '#c62a33', band: '#111', gloves: 'mma', shoes: 'barefoot', sensors: true, angry: true }) },
];
