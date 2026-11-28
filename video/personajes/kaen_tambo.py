"""Personajes originales KAEN (quema su vida, naranja) y TAMBO (pelea riendo, blanco).
Mismo estilo que dibujar.py (vector plano, contorno #111, cuerpo de bloques).
Uso: python3 kaen_tambo.py  -> SVG + PNG transparentes en esta carpeta."""
import os, json, subprocess, math
from dibujar import st, line, poly, rrect, circ, spikes, arm, leg, svg_wrap, K, OUT

CX = 300

# ---------------------------------------------------------------- caras
def face_head(cx, hy, skin, w=64):
    return (f'<path d="M{cx-w},{hy-40} Q{cx-w-4},{hy+46} {cx-34},{hy+80} L{cx},{hy+94} L{cx+34},{hy+80} '
            f'Q{cx+w+4},{hy+46} {cx+w},{hy-40} Q{cx},{hy-80} {cx-w},{hy-40} Z" {st(skin)}/>')

def ears(cx, hy, skin, w=64):
    return ''.join(f'<ellipse cx="{cx+s*(w+4)}" cy="{hy+10}" rx="12" ry="20" {st(skin, 5)}/>' for s in (-1, 1))

def eyes(cx, y, iris, sep=30, brow=True, glow=None):
    out = []
    for s in (-1, 1):
        x = cx + s * sep
        pts = [(x - 22 * s, y - 2), (x + 22 * s, y - 12), (x + 19 * s, y + 10), (x - 18 * s, y + 10)]
        out.append(poly(pts, glow or '#fff', 5))
        if not glow:
            out.append(f'<circle cx="{x+1*s}" cy="{y+1}" r="8.5" fill="{iris}"/><circle cx="{x+1*s}" cy="{y+1}" r="4" fill="{K}"/>'
                       f'<circle cx="{x-2*s}" cy="{y-3}" r="2.2" fill="#fff"/>')
        else:
            out.append(f'<circle cx="{x+1*s}" cy="{y+1}" r="7" fill="{iris}"/>')
        if brow:
            out.append(line([(x - 26 * s, y - 12), (x + 26 * s, y - 28)], K, 9))
    return ''.join(out)

def eyes_laugh(cx, y, sep=30):
    """ojos cerrados de risa (arcos ^ ^)"""
    return ''.join(f'<path d="M{cx+s*sep-20},{y+6} Q{cx+s*sep},{y-16} {cx+s*sep+20},{y+6}" fill="none" stroke="{K}" stroke-width="7" stroke-linecap="round"/>'
                   for s in (-1, 1))

def grin(cx, y, w=40, h=34):
    """sonrisa enorme abierta con dientes"""
    return (f'<path d="M{cx-w},{y} Q{cx},{y+6} {cx+w},{y} Q{cx+w*0.7},{y+h} {cx},{y+h+4} Q{cx-w*0.7},{y+h} {cx-w},{y} Z" {st("#c8283a", 5)}/>'
            f'<path d="M{cx-w+5},{y+3} Q{cx},{y+9} {cx+w-5},{y+3} L{cx+w-10},{y+12} Q{cx},{y+17} {cx-w+10},{y+12} Z" fill="#fff"/>'
            f'<ellipse cx="{cx}" cy="{y+h-6}" rx="{w*0.35}" ry="6" fill="#ff7a86"/>')

def nose(cx, hy, sh):
    return line([(cx - 3, hy + 40), (cx - 8, hy + 52), (cx + 2, hy + 54)], sh, 4)

# ---------------------------------------------------------------- KAEN
K_SKIN = '#f1b98c'; K_SH = '#cf8d5c'
K_RED = '#b8271f'; K_RED_SH = '#7e1712'; K_PANT = '#2b2b35'
FIRE = '#ff8a1e'; FIRE_SH = '#e0560c'; FIRE_LT = '#ffd23a'
K_SKIN_FIRE = '#ffb04a'; K_SH_FIRE = '#e06d12'

def bandage(sx, sy, side, ang, up_len, fo_len, w):
    return ''

def flame_cloak(cx, top, bot, half_top, half_bot):
    """manto de llamas planas sobre el cuerpo (Modo Brasa)"""
    pts = [(cx - half_top, top)]
    n = 7
    for i in range(n + 1):
        x = cx - half_bot - 30 + i * (2 * half_bot + 60) / n
        pts.append((x, bot + (60 if i % 2 else 10)))
    pts.append((cx + half_top, top))
    pts = [(cx - half_top, top)] + pts[1:-1][::1] + [(cx + half_top, top)]
    return poly(pts, FIRE, 6)

def kaen_hair(cx, hy, col, shd, fire=False):
    g = []
    # moño atado arriba (o llama si está en Modo Brasa)
    if fire:
        g.append(spikes(cx, hy - 30, [(-60, 170, 26), (-30, 215, 30), (0, 250, 32), (30, 215, 30), (60, 170, 26),
                                       (-90, 120, 22), (90, 120, 22)], col, shd))
    else:
        g.append(f'<ellipse cx="{cx}" cy="{hy-92}" rx="34" ry="30" {st(col)}/>')
        g.append(rrect(cx - 22, hy - 72, 44, 18, 6, K_RED, sw=5))
        g.append(spikes(cx, hy - 20, [(-70, 110, 20), (70, 110, 20), (-95, 95, 18), (95, 95, 18)], col, shd))
    # casquete con mechones laterales largos
    cap = [(cx - 72, hy + 40), (cx - 76, hy - 40), (cx - 40, hy - 76), (cx, hy - 82), (cx + 40, hy - 76), (cx + 76, hy - 40),
           (cx + 72, hy + 40), (cx + 58, hy - 6), (cx + 44, hy - 18), (cx + 20, hy - 30), (cx - 10, hy - 24), (cx - 34, hy - 10),
           (cx - 50, hy - 20), (cx - 58, hy - 4)]
    g.append(poly(cap, col))
    g.append(poly([(cx + 30, hy - 70), (cx + 68, hy - 40), (cx + 66, hy + 10), (cx + 46, hy - 30)], shd, 0))
    return ''.join(g)

def kaen_upper(cx, form, skin, sh, torso_top, torso_bot, punch=0, kneel=False):
    g = []
    fire = form == 'brasa'
    shoulder_w = 112
    # brazos con vendas
    for s in (-1, 1):
        p = s == punch
        g.append(arm(s, cx + s * (shoulder_w + 6), torso_top + 30, skin, ang=86 if p else (6 if kneel else 18),
                     up_len=118, fo_len=112, w=60, band='#f2ede2', band_stripe=K_SH if not fire else FIRE_SH,
                     sleeve=K_RED if not fire else FIRE, flex=0 if p else -6))
    # cuello
    g.append(rrect(cx - 30, torso_top - 62, 60, 76, 10, skin))
    # torso: túnica roja cruzada
    tw_top, tw_bot = shoulder_w + 8, 92
    body = [(cx - tw_top, torso_top), (cx + tw_top, torso_top), (cx + tw_bot, torso_bot), (cx - tw_bot, torso_bot)]
    g.append(poly(body, K_RED if not fire else FIRE))
    # escote en V con piel + sello
    g.append(poly([(cx - 52, torso_top), (cx + 52, torso_top), (cx, torso_top + 120)], skin))
    g.append(line([(cx - 40, torso_top + 40), (cx, torso_top + 58), (cx + 40, torso_top + 40)], sh, 5))
    # sello en el pecho: rombo con llama (brilla en Modo Brasa, se apaga al final)
    seal_col = {'base': '#f6c33a', 'brasa': '#fff6c0', 'apagado': '#6b5a4a'}[form]
    sy = torso_top + 76
    g.append(poly([(cx, sy - 24), (cx + 18, sy), (cx, sy + 24), (cx - 18, sy)], seal_col, 5))
    g.append(f'<path d="M{cx},{sy+12} Q{cx-9},{sy+2} {cx},{sy-12} Q{cx+9},{sy+2} {cx},{sy+12} Z" fill="{K_RED if form!="brasa" else FIRE_SH}"/>')
    # solapa cruzada
    g.append(line([(cx - 52, torso_top), (cx + 8, torso_top + 130)], K_RED_SH if not fire else FIRE_SH, 8))
    # fajín negro con nudo
    g.append(rrect(cx - 100, torso_bot - 30, 200, 34, 8, '#1b1b22', sw=6))
    g.append(poly([(cx + 40, torso_bot - 8), (cx + 72, torso_bot + 46), (cx + 56, torso_bot + 50), (cx + 30, torso_bot)], '#1b1b22', 5))
    # hombros
    for s in (-1, 1):
        g.append(circ(cx + s * (shoulder_w + 2), torso_top + 30, 44, K_RED if not fire else FIRE))
        g.append(f'<path d="M{cx+s*(shoulder_w-30)},{torso_top+6} Q{cx+s*(shoulder_w+10)},{torso_top-6} {cx+s*(shoulder_w+34)},{torso_top+22}" '
                 f'fill="none" stroke="#fff" stroke-opacity=".45" stroke-width="7" stroke-linecap="round"/>')
    return ''.join(g)

def kaen_head(cx, hy, form, skin, sh, bow=False):
    g = []
    fire = form == 'brasa'
    hair = (FIRE_LT, FIRE) if fire else ('#1c1a22', '#3c3848')
    if form == 'apagado':
        hair = ('#2a2630', '#4a4552')
    g.append(face_head(cx, hy, skin))
    g.append(ears(cx, hy, skin))
    if fire:
        # marcas de llama en mejillas
        for s in (-1, 1):
            g.append(poly([(cx + s * 40, hy + 46), (cx + s * 60, hy + 34), (cx + s * 54, hy + 52)], FIRE_SH, 0))
        g.append(eyes(cx, hy + 26, '#ff4b1a', glow='#fff2a8'))
        g.append(f'<path d="M{cx-30},{hy+66} L{cx+30},{hy+64} L{cx+24},{hy+80} L{cx-24},{hy+80} Z" {st("#7a1410", 5)}/>')
        g.append(line([(cx - 26, hy + 69), (cx + 26, hy + 67)], '#fff', 5))
    elif form == 'apagado':
        # ojos medio cerrados, agotado
        for s in (-1, 1):
            x = cx + s * 30
            g.append(f'<path d="M{x-20},{hy+30} Q{x},{hy+40} {x+20},{hy+30}" fill="none" stroke="{K}" stroke-width="6" stroke-linecap="round"/>')
            g.append(line([(x - 22 * s, hy + 14), (x + 22 * s, hy + 10)], K, 7))
        g.append(line([(cx - 14, hy + 72), (cx + 14, hy + 74)], K, 5))
        # sudor y tierra
        g.append(f'<path d="M{cx+58},{hy-6} q8,14 0,20 q-8,-6 0,-20 Z" fill="#8fd3ff" stroke="{K}" stroke-width="3"/>')
        g.append(line([(cx - 50, hy + 54), (cx - 34, hy + 58)], sh, 4))
    else:
        g.append(eyes(cx, hy + 26, '#c47a12'))
        g.append(line([(cx - 18, hy + 70), (cx + 18, hy + 66)], K, 6))
    g.append(nose(cx, hy, sh))
    g.append(kaen_hair(cx, hy, *hair, fire=fire))
    return ''.join(g)

def kaen(form='base', punch=0):
    fire = form == 'brasa'
    skin, sh = (K_SKIN_FIRE, K_SH_FIRE) if fire else (K_SKIN, K_SH)
    g = []
    torso_top, torso_bot = 365, 585
    if fire:  # llamas de fondo detrás del cuerpo
        g.append(spikes(CX, 520, [(a, 380 + (40 if i % 2 else 0), 70) for i, a in enumerate(range(-120, 121, 24))], FIRE, FIRE_SH))
    for s in (-1, 1):
        g.append(leg(s, CX + s * 52, 610, K_PANT if not fire else FIRE_SH, '#f4f4f6', K_RED if not fire else FIRE, L=240, w=82))
    g.append(kaen_upper(CX, form, skin, sh, torso_top, torso_bot, punch))
    g.append(kaen_head(CX, 250, form, skin, sh))
    return svg_wrap(''.join(g))

def kaen_kneel():
    """Kaen de rodillas, llama apagada (final)."""
    form = 'apagado'
    skin, sh = K_SKIN, K_SH
    g = []
    dy = 170  # todo el cuerpo baja
    # pierna atrás: muslo vertical hasta la rodilla en el suelo, espinilla hacia atrás
    g.append(rrect(CX - 210, 838, 190, 70, 16, K_PANT))                       # espinilla en el suelo
    g.append(f'<path d="M{CX-206},{840} L{CX-206},{906} L{CX-262},{906} L{CX-236},{846} Z" {st("#f4f4f6")}/>')  # bota
    g.append(rrect(CX - 92, 735, 86, 170, 16, K_PANT))                        # muslo atrás
    # pierna delante: muslo horizontal, rodilla arriba, espinilla vertical
    g.append(rrect(CX - 10, 732, 200, 82, 18, K_PANT))
    g.append(rrect(CX + 108, 738, 82, 140, 16, K_PANT))
    g.append(f'<path d="M{CX+102},{866} L{CX+196},{866} L{CX+222},{912} L{CX+102},{912} Z" {st("#f4f4f6")}/>')
    g.append(rrect(CX + 100, 872, 104, 16, 4, K_RED, sw=5))
    # torso inclinado hacia delante
    g.append(f'<g transform="translate(0,{dy}) rotate(10 {CX} 585)">')
    g.append(kaen_upper(CX, form, skin, sh, 365, 585, punch=0, kneel=True))
    g.append(f'<g transform="rotate(14 {CX} 330)">{kaen_head(CX, 250, form, skin, sh)}</g>')
    g.append('</g>')
    # humo que sale del sello
    for i, (x, y, r) in enumerate([(CX + 70, 560, 18), (CX + 100, 520, 24), (CX + 140, 470, 30)]):
        g.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#8a8494" opacity="{0.55-i*0.12}"/>')
    return svg_wrap(''.join(g))

# ---------------------------------------------------------------- TAMBO
T_SKIN = '#e9a978'; T_SH = '#c47f4d'
T_VEST = '#1f8f8a'; T_VEST_SH = '#146560'; T_SHORT = '#8a5a2b'; T_SHORT_SH = '#5f3c1a'
SCARF = '#ffcf3a'
WHITE = '#fbfbff'; WHITE_SH = '#cfd3e6'

def cloud_puffs(pts, fill=WHITE, r=26, sw=6):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{rr if rr else r}" {st(fill, sw)}/>' for x, y, rr in pts)

def tambo_hair(cx, hy, form):
    g = []
    if form == 'tambor':
        # pelo blanco de nubes: anillo de bolas esponjosas
        puffs = []
        for i in range(11):
            a = math.radians(168 + i * 20.4)
            R = 96 + (18 if i % 2 else 0)
            puffs.append((cx + R * math.cos(a) * 1.08, hy - 20 + R * math.sin(a), 36 if i % 2 else 30))
        g.append(cloud_puffs(puffs))
        g.append(f'<ellipse cx="{cx}" cy="{hy-50}" rx="86" ry="44" {st(WHITE)}/>')
        # flequillo de nubes (por encima de las cejas)
        g.append(cloud_puffs([(cx - 50, hy - 14, 20), (cx - 18, hy - 22, 22), (cx + 18, hy - 22, 22), (cx + 52, hy - 14, 20)]))
        for x, y in [(cx - 60, hy - 60), (cx + 30, hy - 74)]:
            g.append(f'<path d="M{x},{y} q14,-12 28,0" fill="none" stroke="{WHITE_SH}" stroke-width="6" stroke-linecap="round"/>')
    elif form == 'anciano':
        col, shd = '#d8d8dc', '#a9a9b2'
        cap = [(cx - 74, hy + 40), (cx - 78, hy - 30), (cx - 50, hy - 70), (cx, hy - 78), (cx + 50, hy - 70), (cx + 78, hy - 30), (cx + 74, hy + 40),
               (cx + 60, hy + 6), (cx + 50, hy - 26), (cx + 30, hy - 14), (cx + 10, hy - 34), (cx - 14, hy - 16), (cx - 36, hy - 32), (cx - 54, hy - 6), (cx - 62, hy + 8)]
        g.append(spikes(cx, hy - 10, [(-110, 110, 16), (110, 110, 16), (-80, 120, 18), (80, 120, 18)], col, shd))
        g.append(poly(cap, col))
        g.append(poly([(cx + 30, hy - 66), (cx + 70, hy - 30), (cx + 60, hy + 6), (cx + 50, hy - 26)], shd, 0))
    else:
        col, shd = '#1a1820', '#3a3646'
        # pelo revuelto: picos cortos irregulares
        g.append(spikes(cx, hy - 10, [(-105, 120, 18), (-80, 135, 20), (-50, 128, 20), (-20, 140, 20), (12, 132, 20), (42, 142, 20),
                                      (72, 128, 20), (100, 118, 18)], col, shd))
        cap = [(cx - 72, hy + 30), (cx - 78, hy - 30), (cx - 46, hy - 74), (cx, hy - 82), (cx + 46, hy - 74), (cx + 78, hy - 30), (cx + 72, hy + 30),
               (cx + 60, hy - 4), (cx + 52, hy - 30), (cx + 30, hy - 10), (cx + 18, hy - 36), (cx - 2, hy - 12), (cx - 20, hy - 34),
               (cx - 40, hy - 8), (cx - 52, hy - 30), (cx - 62, hy + 2)]
        g.append(poly(cap, col))
        g.append(poly([(cx + 30, hy - 70), (cx + 70, hy - 34), (cx + 60, hy - 4), (cx + 52, hy - 30)], shd, 0))
    return ''.join(g)

def tambo_head(cx, hy, form):
    skin, sh = (T_SKIN, T_SH)
    g = []
    if form == 'tambor':
        skin, sh = '#f2c9a4', '#d29a6c'
    g.append(face_head(cx, hy, skin, 66))
    g.append(ears(cx, hy, skin, 66))
    if form == 'tambor':
        g.append(eyes_laugh(cx, hy + 28))
        g.append(grin(cx, hy + 52, 46, 40))
        # mejillas
        for s in (-1, 1):
            g.append(f'<ellipse cx="{cx+s*44}" cy="{hy+48}" rx="12" ry="7" fill="#ff8f8f" opacity=".7"/>')
    elif form == 'anciano':
        for s in (-1, 1):
            x = cx + s * 30
            g.append(f'<path d="M{x-18},{hy+30} Q{x},{hy+18} {x+18},{hy+30}" fill="none" stroke="{K}" stroke-width="6" stroke-linecap="round"/>')
            g.append(line([(x - 16, hy + 40), (x + 14, hy + 42)], sh, 3))     # ojeras
            g.append(line([(cx + s * 56, hy + 20), (cx + s * 50, hy + 60)], sh, 4))  # mejillas hundidas
        g.append(line([(cx - 40, hy - 4), (cx + 40, hy - 4)], sh, 3))          # arrugas de frente
        g.append(line([(cx - 30, hy + 6), (cx + 30, hy + 6)], sh, 3))
        g.append(grin(cx, hy + 58, 34, 26))
    else:
        g.append(eyes(cx, hy + 26, '#3a2415', brow=False))
        for s in (-1, 1):
            g.append(line([(cx + s * 52, hy + 4), (cx + s * 12, hy + 2)], K, 8))   # cejas rectas, gesto confiado
        g.append(grin(cx, hy + 56, 40, 30))
        g.append(line([(cx + 40, hy + 60), (cx + 52, hy + 50)], sh, 4))            # tirita en mejilla
        g.append(rrect(cx + 34, hy + 48, 26, 14, 4, '#f6e3c4', rot=-30, cx=cx + 47, cy=hy + 55, sw=4))
    g.append(nose(cx, hy, sh))
    g.append(tambo_hair(cx, hy, form))
    return ''.join(g)

def big_fist(x, y, s, col):
    """puño gigante (para el golpe final), centrado en x,y."""
    return (rrect(x - 110 * s, y - 100 * s, 220 * s, 200 * s, 70 * s, col, sw=9) +
            ''.join(line([(x + 60 * s, y - 70 * s + i * 50 * s), (x + 100 * s, y - 70 * s + i * 50 * s)], K, 7) for i in range(4)) +
            line([(x - 40 * s, y - 100 * s), (x - 40 * s, y - 40 * s)], K, 7))

def tambo(form='base', punch=0, stretch=False, giant=False):
    tam = form == 'tambor'; old = form == 'anciano'
    skin, sh = ('#f2c9a4', '#d29a6c') if tam else (T_SKIN, T_SH)
    vest, vest_sh = (WHITE, WHITE_SH) if tam else (T_VEST, T_VEST_SH)
    short, short_sh = (WHITE, WHITE_SH) if tam else (T_SHORT, T_SHORT_SH)
    if old:
        vest, short = '#5f7a78', '#6f5a44'
    g = []
    cx = CX
    torso_top, torso_bot = (385, 585) if old else (370, 585)
    shoulder_w = 84 if old else 104
    hip = 44 if old else 50
    # piernas: pantalón corto + pierna desnuda + sandalia blanca
    for s in (-1, 1):
        lw = 58 if old else 74
        g.append(f'<g transform="rotate({4*s} {cx+s*hip} 600)">')
        g.append(rrect(cx + s * hip - lw / 2 + 4, 640, lw - 8, 210, 14, skin))
        g.append(f'<path d="M{cx+s*hip-lw/2-6},{845} L{cx+s*hip+lw/2+6},{845} L{cx+s*hip+lw/2+6+(14 if s>0 else 0)},{905} '
                 f'L{cx+s*hip-lw/2-6-(14 if s<0 else 0)},{905} Z" {st("#f4f4f6")}/>')
        g.append(line([(cx + s * hip - 14, 846), (cx + s * hip + 6, 870)], K, 5))
        g.append(rrect(cx + s * hip - (lw / 2 + 10), 590, lw + 20, 110, 12, short))  # pernera
        g.append(rrect(cx + s * hip - (lw / 2 + 14), 680, lw + 28, 26, 8, short_sh if not tam else WHITE_SH, sw=5))  # dobladillo
        g.append('</g>')
    # brazos
    for s in (-1, 1):
        p = s == punch
        fo = 260 if (p and stretch) else (100 if old else 110)
        if p and giant:
            continue
        if p and stretch:
            # brazo de goma estirado
            g.append(arm(s, cx + s * (shoulder_w + 6), torso_top + 28, skin, ang=88, up_len=110, fo_len=fo, w=40 if old else 54,
                         band=None, flex=0))
            # líneas de estiramiento
            for i in range(3):
                xx = cx + s * (shoulder_w + 150 + i * 70)
                g.append(line([(xx, torso_top + 6), (xx, torso_top + 50)], sh, 4))
        else:
            g.append(arm(s, cx + s * (shoulder_w + 6), torso_top + 28, skin, ang=86 if p else 16, up_len=104 if old else 114,
                         fo_len=fo, w=40 if old else 58, band=None, flex=0 if p else -8))
    # puño gigante (Forma Tambor)
    if giant:
        g.append(rrect(cx - 330, torso_top + 4, 330 - shoulder_w + 10, 54, 26, skin))
        g.append(big_fist(cx - 330, torso_top + 30, 1.2, skin))
    # cuello
    g.append(rrect(cx - (24 if old else 30), torso_top - 60, 48 if old else 60, 72, 10, skin))
    # torso desnudo
    tw_top, tw_bot = shoulder_w + 6, (68 if old else 86)
    g.append(poly([(cx - tw_top, torso_top), (cx + tw_top, torso_top), (cx + tw_bot, torso_bot), (cx - tw_bot, torso_bot)], skin))
    if old:
        for i in range(4):  # costillas
            yy = torso_top + 50 + i * 26
            g.append(line([(cx - 50 + i * 3, yy), (cx - 18, yy + 8)], sh, 4))
            g.append(line([(cx + 50 - i * 3, yy), (cx + 18, yy + 8)], sh, 4))
    else:
        g.append(line([(cx - 80, torso_top + 66), (cx - 40, torso_top + 88), (cx, torso_top + 76), (cx + 40, torso_top + 88), (cx + 80, torso_top + 66)], sh, 6))
        g.append(line([(cx, torso_top + 80), (cx, torso_bot - 15)], sh, 5))
        for i, yy in enumerate((torso_top + 124, torso_top + 156, torso_top + 186)):
            g.append(line([(cx - 34 + i * 3, yy), (cx + 34 - i * 3, yy)], sh, 5))
    # chaleco abierto (sin mangas)
    for s in (-1, 1):
        g.append(poly([(cx + s * tw_top, torso_top), (cx + s * 44, torso_top), (cx + s * 56, torso_bot - 4), (cx + s * tw_bot, torso_bot - 4)], vest))
        g.append(line([(cx + s * (tw_top - 18), torso_top + 30), (cx + s * (tw_bot - 6), torso_bot - 20)], vest_sh, 5))
        if tam:  # ribete de nubes en el chaleco
            g.append(cloud_puffs([(cx + s * 50, torso_bot - 10 - i * 46, 16) for i in range(4)], WHITE, sw=5))
    # cinturón de cuerda
    g.append(rrect(cx - tw_bot - 6, torso_bot - 24, 2 * tw_bot + 12, 28, 10, '#d9b878' if not tam else WHITE_SH, sw=5))
    g.append(line([(cx - 10, torso_bot - 10), (cx - 26, torso_bot + 44)], K, 5))
    g.append(line([(cx + 4, torso_bot - 10), (cx + 14, torso_bot + 40)], K, 5))
    # pañuelo al cuello
    g.append(poly([(cx - 46, torso_top - 8), (cx + 46, torso_top - 8), (cx + 30, torso_top + 22), (cx - 30, torso_top + 22)], SCARF if not tam else WHITE, 6))
    g.append(poly([(cx + 24, torso_top + 14), (cx + 52, torso_top + 66), (cx + 30, torso_top + 70), (cx + 12, torso_top + 20)], SCARF if not tam else WHITE, 5))
    # hombros
    for s in (-1, 1):
        g.append(circ(cx + s * (shoulder_w + 2), torso_top + 28, 30 if old else 40, vest))
    # tambor en el pecho (Forma Tambor): corazón-tambor brillante
    if tam:
        y = torso_top + 104
        g.append(f'<ellipse cx="{cx}" cy="{y}" rx="30" ry="22" {st("#ff6b6b", 5)}/>')
        g.append(f'<ellipse cx="{cx}" cy="{y-6}" rx="30" ry="10" {st("#ffd1d1", 4)}/>')
        for s in (-1, 1):
            g.append(line([(cx + s * 26, y - 2), (cx + s * 18, y + 18)], K, 4))
    # cabeza
    hy = 262 if old else 248
    g.append(tambo_head(cx, hy, form))
    body = ''.join(g)
    if old:  # encorvado
        body = f'<g transform="rotate(4 {cx} 900)">{body}</g>'
    return svg_wrap(body)

CHARS = {
    'kaen': lambda: kaen('base'),
    'kaen_golpe': lambda: kaen('base', 1),
    'kaen_brasa': lambda: kaen('brasa'),
    'kaen_brasa_golpe': lambda: kaen('brasa', 1),
    'kaen_rodillas': kaen_kneel,
    'tambo': lambda: tambo('base'),
    'tambo_golpe': lambda: tambo('base', -1),
    'tambo_tambor': lambda: tambo('tambor'),
    'tambo_tambor_estirado': lambda: tambo('tambor', -1, stretch=True),
    'tambo_tambor_gigante': lambda: tambo('tambor', -1, giant=True),
    'tambo_anciano': lambda: tambo('anciano'),
}

if __name__ == '__main__':
    for name, fn in CHARS.items():
        open(os.path.join(OUT, name + '.svg'), 'w').write(fn())
    js = """const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1000,height:1000},deviceScaleFactor:2});
for(const n of %s){await p.setContent('<html><body style="margin:0;background:transparent">'+fs.readFileSync('%s/'+n+'.svg','utf8')+'</body></html>');
await p.locator('svg').screenshot({path:'%s/'+n+'.png',omitBackground:true});console.log('ok',n);}await b.close();})();""" % (json.dumps(list(CHARS)), OUT, OUT)
    subprocess.run(['node', '-e', js], check=True)
