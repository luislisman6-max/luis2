"""Personajes originales KAEN (quema su vida, naranja) y TAMBO (pelea riendo, cian).
Mismo estilo que dibujar.py: vector plano, contorno negro grueso, cuerpo de bloques.
Uso: python3 dibujar_kaen_tambo.py"""
import os, json, subprocess, math
from dibujar import K, st, line, poly, rrect, circ, arm, leg, spikes, svg_wrap, OUT

CX, HY, TT, TB = 300, 250, 365, 585   # centro, cabeza, torso arriba/abajo

def head(skin, cx=CX, hy=HY):
    return (f'<path d="M{cx-62},{hy-40} Q{cx-66},{hy+50} {cx-36},{hy+82} L{cx},{hy+96} L{cx+36},{hy+82} '
            f'Q{cx+66},{hy+50} {cx+62},{hy-40} Q{cx},{hy-78} {cx-62},{hy-40} Z" {st(skin)}/>'
            + ''.join(f'<ellipse cx="{cx+s*66}" cy="{hy+12}" rx="12" ry="20" {st(skin, 5)}/>' for s in (-1, 1)))

def nose(sh, cx=CX, hy=HY):
    return line([(cx - 4, hy + 40), (cx - 8, hy + 52), (cx + 2, hy + 54)], sh, 4)

def flame(x, y, w, h, fill, inner=None, lean=0, sw=5):
    """llama en forma de gota con punta curvada; (x,y) = base centro"""
    t = (x + lean, y - h)
    d = (f'M{x-w},{y} C{x-w*1.1},{y-h*.45} {t[0]-w*.4},{y-h*.6} {t[0]},{t[1]} '
         f'C{t[0]+w*.2},{y-h*.55} {x+w*1.15},{y-h*.4} {x+w},{y} Q{x},{y+w*.5} {x-w},{y} Z')
    out = f'<path d="{d}" fill="{fill}" stroke="{K}" stroke-width="{sw}" stroke-linejoin="round"/>'
    if inner:
        out += flame(x, y - h * .05, w * .5, h * .55, inner, None, lean * .5, 0)
    return out

def sleep_eyes(cx=CX, y=HY + 30, sep=30):
    return ''.join(line([(cx + s * sep - 20, y), (cx + s * sep + 20, y + 4)], K, 6) for s in (-1, 1))

def laugh_eyes(cx=CX, y=HY + 30, sep=30):
    return ''.join(f'<path d="M{cx+s*sep-20},{y+6} Q{cx+s*sep},{y-16} {cx+s*sep+20},{y+6}" fill="none" stroke="{K}" '
                   f'stroke-width="8" stroke-linecap="round"/>' for s in (-1, 1))

def round_eyes(cx=CX, y=HY + 28, sep=30, iris='#2b1c14'):
    out = []
    for s in (-1, 1):
        x = cx + s * sep
        out.append(f'<ellipse cx="{x}" cy="{y}" rx="16" ry="19" {st("#fff", 5)}/>')
        out.append(f'<circle cx="{x+3*s}" cy="{y+2}" r="9" fill="{iris}"/><circle cx="{x+6*s}" cy="{y-3}" r="3.5" fill="#fff"/>')
        out.append(line([(x - 18 * s, y - 30), (x + 18 * s, y - 34)], K, 7))   # ceja alta, relajada
    return ''.join(out)

def fierce_eyes(cx=CX, y=HY + 28, sep=30, iris='#ff8a1f', slit=True):
    out = []
    for s in (-1, 1):
        x = cx + s * sep
        pts = [(x - 24 * s, y - 4), (x + 24 * s, y - 14), (x + 20 * s, y + 10), (x - 20 * s, y + 10)]
        out.append(poly(pts, '#fff', 5))
        out.append(f'<circle cx="{x+2*s}" cy="{y+1}" r="9" fill="{iris}"/>')
        out.append(f'<ellipse cx="{x+2*s}" cy="{y+1}" rx="{2.5 if slit else 4}" ry="7" fill="{K}"/>')
        out.append(line([(x - 30 * s, y - 14), (x + 28 * s, y - 30)], K, 9))
    return ''.join(out)

def grin(cx=CX, y=HY + 56, w=40, big=True):
    h = 40 if big else 26
    return (f'<path d="M{cx-w},{y} Q{cx},{y+6} {cx+w},{y} Q{cx+w*.7},{y+h} {cx},{y+h} Q{cx-w*.7},{y+h} {cx-w},{y} Z" {st("#c8283a", 5)}/>'
            f'<path d="M{cx-w+5},{y+2} Q{cx},{y+8} {cx+w-5},{y+2} L{cx+w-9},{y+11} Q{cx},{y+16} {cx-w+9},{y+11} Z" fill="#fff"/>'
            f'<path d="M{cx-w*.35},{y+h-6} Q{cx},{y+h-20} {cx+w*.35},{y+h-6}" fill="#ff7a88"/>')

def fist_big(x, y, s, fill):
    """puño gigante (Tambo). (x,y) = centro, s = escala"""
    w, h = 230 * s, 190 * s
    out = [rrect(x - w / 2, y - h / 2, w, h, 60 * s, fill)]
    for i in range(1, 4):
        xx = x - w / 2 + i * w / 4
        out.append(line([(xx, y - h / 2 + 18 * s), (xx, y - h / 2 + 70 * s)], K, 6))
    out.append(f'<path d="M{x-w/2+20*s},{y+h/2-40*s} Q{x},{y+h/2-10*s} {x+w/2-20*s},{y+h/2-40*s}" fill="none" stroke="#c9cde4" stroke-width="10" stroke-linecap="round"/>')
    return ''.join(out)

# ================================================================= KAEN
K_SKIN, K_SH = '#e8b48c', '#c08562'
K_HAIR, K_HAIR_SH = '#5a1616', '#3a0c0c'
K_TUNIC, K_SASH, K_PANTS = '#211c26', '#c4262e', '#3a3442'
BANDAGE, BANDAGE_SH = '#efe6cf', '#bdae8a'
ORANGE, ORANGE2, YELLOW = '#ff7a1a', '#ffa72e', '#ffe14a'

def seal(cx, y, glow, r=26):
    out = [circ(cx, y, r, glow if glow else '#3a2a2a', 5)]
    c = '#fff6c8' if glow else '#8a5a4a'
    out.append(flame(cx, y + 12, 9, 30, c, None, 2, 0))
    for a in range(0, 360, 60):
        ra = math.radians(a)
        out.append(line([(cx + math.cos(ra) * (r + 6), y + math.sin(ra) * (r + 6)), (cx + math.cos(ra) * (r + 16), y + math.sin(ra) * (r + 16))], glow or '#8a5a4a', 4))
    return ''.join(out)

def kaen(form='base', punch=0):
    """form: base | brasa | rodillas"""
    brasa = form in ('brasa', 'rodillas')
    kneel = form == 'rodillas'
    g = []
    dy = 175 if kneel else 0
    body = []
    # ---- aura de llamas pegada al cuerpo (solo brasa activa)
    if form == 'brasa':
        for i, (x, h, w, l) in enumerate([(150, 330, 70, -30), (210, 420, 80, -10), (300, 470, 90, 0), (390, 420, 80, 10), (450, 330, 70, 30),
                                          (110, 230, 55, -40), (490, 230, 55, 40)]):
            g.append(flame(x, 620, w, h, ORANGE, ORANGE2, l, 0).replace('fill="' + ORANGE + '"', f'fill="{ORANGE}" opacity=".85"'))
    # ---- pelo de atrás: coleta
    hair_c, hair_sh = (ORANGE, '#d9500e') if brasa and not kneel else (K_HAIR, K_HAIR_SH)
    if kneel:
        hair_c, hair_sh = '#7a2a18', '#4a1408'   # llama apagada: pelo ceniza-rojizo
    if form == 'brasa':
        for a, h, w in [(-50, 170, 36), (-20, 210, 40), (10, 230, 42), (40, 200, 38), (65, 150, 30)]:
            x = CX + math.sin(math.radians(a)) * 40
            g.append(flame(x, HY - 30, w, h, ORANGE, YELLOW, a * 1.2))
    else:
        pony = (f'<path d="M{CX+20},{HY-80} Q{CX+70},{HY-150} {CX+20},{HY-190} Q{CX+110},{HY-150} {CX+60},{HY-70} Z" {st(hair_c)}/>'
                + rrect(CX + 6, HY - 96, 40, 22, 6, K_SASH, rot=-30, sw=5))
    # ---- piernas
    if kneel:
        for sd in (-1, 1):
            body.append(f'<ellipse cx="{CX+sd*62}" cy="900" rx="70" ry="12" fill="#000" opacity=".25"/>')
            body.append(rrect(CX + sd * 62 - 46, 748, 92, 150, 16, K_PANTS))
            body.append(rrect(CX + sd * 62 - 50, 862, 100, 34, 12, BANDAGE, sw=5))
            body.append(poly([(CX + sd * 62 - 40, 896), (CX + sd * 62 + 40, 896), (CX + sd * 62 + 30, 912), (CX + sd * 62 - 30, 912)], K_TUNIC, 5))
    else:
        for s in (-1, 1):
            body.append(leg(s, CX + s * 56, 640, K_PANTS, K_TUNIC, BANDAGE, L=210, w=86))
    up = [] if form == 'brasa' else [pony]
    # ---- brazos
    skin = K_SKIN
    for s in (-1, 1):
        p = s == punch
        if kneel:
            # brazos caídos, puño apoyado en el suelo (izq)
            up.append(arm(s, CX + s * 128, TT + 30, skin, ang=8 if s < 0 else 22, up_len=118, fo_len=112, w=60,
                          band=BANDAGE, band_stripe=BANDAGE_SH, flex=-2))
        else:
            up.append(arm(s, CX + s * 128, TT + 30, skin, ang=86 if p else 20, up_len=118, fo_len=112, w=60,
                          band=BANDAGE, band_stripe=BANDAGE_SH, flex=0 if p else -6))
    # vendas en antebrazos (rayas cruzadas) ya resueltas por la muñequera ancha
    # ---- cuello y torso
    up.append(rrect(CX - 30, 300, 60, 80, 10, skin))
    tw_t, tw_b = 136, 92
    torso = [(CX - tw_t, TT), (CX + tw_t, TT), (CX + tw_b, TB), (CX - tw_b, TB)]
    if form == 'base':
        up.append(poly(torso, K_TUNIC))
        up.append(poly([(CX - 54, TT), (CX + 54, TT), (CX, TT + 150)], skin, 5))      # escote en V
        up.append(line([(CX - 40, TT + 40), (CX, TT + 60), (CX + 40, TT + 40)], K_SH, 5))
        up.append(seal(CX, TT + 92, None, 18))
        up.append(line([(CX - 54, TT), (CX + 8, TT + 150)], K_SASH, 7))
        up.append(line([(CX + 70, TT + 110), (CX + 110, TT + 100)], '#3a3442', 5))
    else:
        up.append(poly(torso, skin))
        sh = K_SH
        up.append(line([(CX - 110, TT + 70), (CX - 54, TT + 95), (CX, TT + 80), (CX + 54, TT + 95), (CX + 110, TT + 70)], sh, 6))
        up.append(line([(CX, TT + 82), (CX, TB - 15)], sh, 5))
        for i, yy in enumerate((TT + 130, TT + 162, TT + 192)):
            up.append(line([(CX - 42 + i * 4, yy), (CX + 42 - i * 4, yy)], sh, 5))
        # restos de túnica quemada (hombro izq)
        up.append(poly([(CX - tw_t, TT), (CX - 70, TT), (CX - 92, TT + 50), (CX - 110, TT + 30), (CX - 122, TT + 70)], K_TUNIC, 5))
        # venas de fuego (brasa) o grietas apagadas (rodillas)
        vc = YELLOW if form == 'brasa' else '#6b5550'
        for pts in ([(CX, TT + 92), (CX - 40, TT + 120), (CX - 60, TT + 170), (CX - 80, TB - 30)],
                    [(CX, TT + 92), (CX + 44, TT + 116), (CX + 70, TT + 160)],
                    [(CX, TT + 92), (CX - 8, TT + 40), (CX - 30, TT + 10)]):
            up.append(line(pts, vc, 5))
        up.append(seal(CX, TT + 92, ORANGE if form == 'brasa' else None, 24))
    # faja roja + faldón
    up.append(rrect(CX - 100, TB - 14, 200, 30, 8, K_SASH))
    up.append(poly([(CX - 98, TB + 14), (CX + 98, TB + 14), (CX + 116, TB + 82), (CX + 8, TB + 70), (CX - 116, TB + 82)], K_TUNIC))
    up.append(poly([(CX + 60, TB + 14), (CX + 84, TB + 14), (CX + 74, TB + 110), (CX + 54, TB + 104)], K_SASH, 5))
    # hombros
    for s in (-1, 1):
        up.append(circ(CX + s * 128, TT + 32, 42, skin if form != 'base' else K_TUNIC))
    # ---- cabeza
    up.append(head(skin))
    cap = [(CX - 70, HY + 14), (CX - 74, HY - 40), (CX - 40, HY - 76), (CX, HY - 82), (CX + 40, HY - 76), (CX + 74, HY - 40), (CX + 70, HY + 14),
           (CX + 60, HY - 14), (CX + 34, HY - 6), (CX + 30, HY - 30), (CX + 4, HY - 10), (CX - 12, HY - 34), (CX - 34, HY - 8), (CX - 60, HY - 24)]
    up.append(poly(cap, hair_c))
    up.append(poly([(CX + 34, HY - 70), (CX + 68, HY - 40), (CX + 60, HY - 14), (CX + 44, HY - 40)], hair_sh, 0))
    # cinta de la frente roja con nudo atrás (lado izq)
    up.append(rrect(CX - 72, HY - 18, 144, 18, 6, K_SASH, sw=5))
    up.append(poly([(CX - 70, HY - 12), (CX - 118, HY - 30), (CX - 108, HY - 4)], K_SASH, 5))
    up.append(poly([(CX - 70, HY - 6), (CX - 112, HY + 20), (CX - 96, HY + 26)], K_SASH, 5))
    # marca de cicatriz bajo el ojo derecho (rasgo propio)
    if form == 'rodillas':
        up.append(sleep_eyes(CX, HY + 32))
        up.append(line([(CX - 16, HY + 74), (CX + 16, HY + 72)], K, 5))
        up.append(line([(CX + 40, HY + 52), (CX + 46, HY + 70)], '#7a6a8a', 4))   # sudor
    elif form == 'brasa':
        up.append(fierce_eyes(CX, HY + 28, 30, ORANGE))
        up.append(f'<path d="M{CX-26},{HY+62} L{CX+26},{HY+62} L{CX+18},{HY+80} L{CX-18},{HY+80} Z" {st("#fff", 5)}/>')
        up.append(line([(CX - 22, HY + 71), (CX + 22, HY + 71)], K, 3))
        for s in (-1, 1):  # marcas de fuego en las mejillas
            up.append(poly([(CX + s * 40, HY + 44), (CX + s * 56, HY + 38), (CX + s * 50, HY + 52)], ORANGE, 3))
    else:
        up.append(fierce_eyes(CX, HY + 28, 30, '#8a4a22', slit=False))
        up.append(line([(CX - 18, HY + 72), (CX + 18, HY + 68)], K, 6))
    up.append(line([(CX - 46, HY + 46), (CX - 34, HY + 60)], K_SH, 4))
    up.append(nose(K_SH))
    upper = ''.join(up)
    if kneel:
        upper = f'<g transform="translate(0 {dy}) rotate(10 {CX} {TB})">{upper}</g>'
        smoke = ''.join(f'<circle cx="{CX + dx}" cy="{HY + dy - 110 - i * 50}" r="{22 + i * 6}" fill="#8a8494" opacity="{.5 - i * .12}"/>'
                        for i, dx in enumerate((10, -20, 15)))
        return svg_wrap(''.join(g) + ''.join(body) + upper + smoke)
    return svg_wrap(''.join(g) + ''.join(body) + upper)

# ================================================================= TAMBO
# Concepto propio: tamborilero de cuerpo elástico. Base = camiseta sin mangas teal con emblema de tambor,
# moño alto morado, pantalón negro con franja, zapatillas, tambor taiko a la espalda con baquetas.
# Forma Tambor = piel con marcas eléctricas cian, pelo en rayos hacia arriba, anillo de tambores flotando (estilo dios del trueno).
T_SKIN, T_SH = '#c98a5e', '#9e6440'
T_HAIR, T_HAIR_SH = '#3b2a5c', '#24183c'
TEAL, TEAL_SH = '#1aa6b8', '#0f7280'
PANTS, STRIPE = '#22222c', '#1aa6b8'
CYAN, CYAN2 = '#3ae8ff', '#c8faff'
DRUM, DRUM_SH, DRUM_SKIN = '#b2442a', '#7e2c18', '#f2e2c0'

def drum(x, y, r, rot=0):
    """tambor taiko visto de frente-lado (cilindro bajo)"""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<rect x="{x-r}" y="{y-r*.55}" width="{2*r}" height="{r*1.1}" rx="{r*.25}" {st(DRUM, 5)}/>'
            f'<ellipse cx="{x}" cy="{y-r*.55}" rx="{r}" ry="{r*.32}" {st(DRUM_SKIN, 5)}/>'
            + ''.join(f'<circle cx="{x+i*r*.4}" cy="{y-r*.1}" r="{max(3,r*.07)}" fill="#e8c048"/>' for i in (-2, -1, 0, 1, 2))
            + f'<path d="M{x-r*.8},{y+r*.3} L{x+r*.8},{y+r*.3}" stroke="{DRUM_SH}" stroke-width="5"/></g>')

def bolt(pts, col=CYAN, w=7):
    return line(pts, K, w + 6) + line(pts, col, w)

def tambo(form='base', punch=0, gigante=False):
    """form: base | tambor | anciano"""
    tam = form == 'tambor'; old = form == 'anciano'
    skin = '#b48a72' if old else T_SKIN
    sh = '#8a6450' if old else T_SH
    g = []
    # ---- anillo de tambores (forma tambor)
    if tam:
        g.append(f'<circle cx="{CX}" cy="{TT+40}" r="270" fill="none" stroke="{K}" stroke-width="22"/>'
                 f'<circle cx="{CX}" cy="{TT+40}" r="270" fill="none" stroke="{CYAN}" stroke-width="12"/>')
        for i in range(8):
            a = math.radians(i * 45 + 22.5)
            g.append(drum(CX + math.cos(a) * 270, TT + 40 + math.sin(a) * 270, 46, i * 45 + 22.5 + 90))
    # ---- tambor a la espalda (base / anciano)
    else:
        g.append(drum(CX, TT + 10, 120 if not old else 104))
        for s in (-1, 1):  # baquetas cruzadas
            g.append(rrect(CX + s * 120 - 9, TT - 150, 18, 190, 9, '#e8d2a0', rot=s * 28, cx=CX + s * 120, cy=TT - 60, sw=5))
    # ---- piernas: pantalón negro con franja + zapatillas
    for sd in (-1, 1):
        hx = CX + sd * 54
        g.append(f'<g transform="rotate({4*sd} {hx} 630)">')
        w = 66 if old else 84
        g.append(rrect(hx - w / 2, 630, w, 230, 16, PANTS if not tam else '#1c2a36'))
        g.append(line([(hx + sd * (w / 2 - 12), 650), (hx + sd * (w / 2 - 12), 850)], STRIPE if not old else '#8a8a9a', 7))
        if tam:
            g.append(bolt([(hx - 10, 690), (hx + 12, 730), (hx - 8, 760), (hx + 10, 800)], CYAN, 5))
        g.append(f'<path d="M{hx-w/2-6},{850} L{hx+w/2+6},{850} Q{hx+w/2+30*sd if sd>0 else hx+w/2+8},{880} {hx+w/2+24 if sd>0 else hx+w/2+6},{904} '
                 f'L{hx-w/2-24 if sd<0 else hx-w/2-6},{904} Q{hx-w/2-8},{880} {hx-w/2-6},{850} Z" {st("#f4f4f6")}/>')
        g.append(rrect(hx - w / 2 - 10, 892, w + 20 + 14, 14, 6, TEAL if not old else '#9a9aa8', sw=5))
        g.append('</g>')
    # ---- brazos (elásticos: un poco más largos y finos)
    w_arm = 42 if old else 56
    ax = 96 if old else 120
    for sd in (-1, 1):
        p = sd == punch
        g.append(arm(sd, CX + sd * ax, TT + 30, skin, ang=86 if p else (10 if old else 16), up_len=126, fo_len=124, w=w_arm,
                     band=TEAL if not old else '#9a9aa8', band_stripe='#fff', flex=0 if p else -8))
    if gigante and punch:
        fx = CX + punch * 430
        g.append(fist_big(fx, TT + 30, 1.0, skin))
        for i, (dx, dy) in enumerate(((-60, -110), (40, -120), (120, -40), (-130, 40))):
            g.append(bolt([(fx + dx * .6, TT + 30 + dy * .6), (fx + dx * .8 + 14, TT + 30 + dy * .8 - 10), (fx + dx, TT + 30 + dy)], CYAN, 5))
    # ---- cuello y torso
    g.append(rrect(CX - (22 if old else 28), 300, 44 if old else 56, 80, 10, skin))
    tw_t, tw_b = (94, 68) if old else (120, 84)
    g.append(poly([(CX - tw_t, TT), (CX + tw_t, TT), (CX + tw_b, TB), (CX - tw_b, TB)], skin))
    if tam:
        # camiseta reventada: solo jirones en la cintura; marcas eléctricas en el torso
        g.append(line([(CX - 96, TT + 64), (CX - 46, TT + 88), (CX, TT + 74), (CX + 46, TT + 88), (CX + 96, TT + 64)], sh, 6))
        g.append(line([(CX, TT + 78), (CX, TB - 15)], sh, 5))
        for i, yy in enumerate((TT + 126, TT + 158, TT + 188)):
            g.append(line([(CX - 36 + i * 3, yy), (CX + 36 - i * 3, yy)], sh, 5))
        g.append(bolt([(CX - 100, TT + 20), (CX - 60, TT + 60), (CX - 84, TT + 90), (CX - 50, TT + 140)], CYAN, 6))
        g.append(bolt([(CX + 100, TT + 30), (CX + 70, TT + 80), (CX + 92, TT + 110), (CX + 56, TT + 170)], CYAN, 6))
        g.append(poly([(CX - tw_b - 4, TB - 40), (CX + tw_b + 4, TB - 40), (CX + tw_b + 10, TB + 20), (CX + 40, TB + 6), (CX, TB + 24),
                       (CX - 40, TB + 6), (CX - tw_b - 10, TB + 20)], TEAL))
    else:
        # camiseta sin mangas cerrada
        tank = TEAL if not old else '#7aa8b0'
        g.append(poly([(CX - tw_t + 22, TT), (CX - 34, TT), (CX, TT + 34), (CX + 34, TT), (CX + tw_t - 22, TT),
                       (CX + tw_b + 2, TB), (CX - tw_b - 2, TB)], tank))
        if old:  # agujeros / roturas
            g.append(poly([(CX + 30, TB - 10), (CX + 46, TB - 60), (CX + 62, TB - 10)], skin, 4))
            g.append(poly([(CX - 60, TT + 70), (CX - 40, TT + 110), (CX - 70, TT + 120)], skin, 4))
        # emblema: tambor con dos baquetas
        ey = TT + 110
        g.append(circ(CX, ey, 36, '#fff', 5))
        g.append(drum(CX, ey + 6, 20))
        g.append(line([(CX - 28, ey - 30), (CX - 8, ey - 8)], K, 5) + line([(CX + 28, ey - 30), (CX + 8, ey - 8)], K, 5))
        g.append(line([(CX - 60, TB - 40), (CX - 30, TB - 30)], TEAL_SH, 5))
    # cinturón ancho con hebilla redonda
    g.append(rrect(CX - 92, TB - 14, 184, 28, 8, '#2a2a34'))
    g.append(circ(CX, TB, 16, '#e8c048', 5))
    # hombros
    for sd in (-1, 1):
        g.append(circ(CX + sd * ax, TT + 32, 28 if old else 38, skin))
    # ---- cabeza
    g.append(head(skin))
    if tam:
        # pelo en rayos hacia arriba, cian
        g.append(spikes(CX, HY - 20, [(a, L, 24) for a, L in ((-60, 150), (-35, 190), (-12, 220), (12, 230), (35, 195), (60, 150))], CYAN, '#14a8c8'))
        cap = [(CX - 70, HY + 10), (CX - 72, HY - 40), (CX - 40, HY - 76), (CX, HY - 82), (CX + 40, HY - 76), (CX + 72, HY - 40), (CX + 70, HY + 10),
               (CX + 50, HY - 20), (CX + 20, HY - 8), (CX, HY - 30), (CX - 20, HY - 8), (CX - 50, HY - 20)]
        g.append(poly(cap, CYAN))
    else:
        hc, hs = (T_HAIR, T_HAIR_SH) if not old else ('#d8d8e2', '#a8a8b8')
        # lados rapados + moño alto redondo
        g.append(f'<path d="M{CX-64},{HY-6} Q{CX-66},{HY-60} {CX},{HY-72} Q{CX+66},{HY-60} {CX+64},{HY-6} Q{CX},{HY-34} {CX-64},{HY-6} Z" fill="{hs}" opacity=".9"/>')
        r_bun = 56 if not old else 40
        g.append(rrect(CX - 46, HY - 110, 92, 60, 22, hc))
        g.append(circ(CX, HY - 120 - (r_bun - 40), r_bun, hc))
        g.append(f'<path d="M{CX-r_bun*.6},{HY-120-(r_bun-40)+r_bun*.2} Q{CX},{HY-120-(r_bun-40)+r_bun*.7} {CX+r_bun*.6},{HY-120-(r_bun-40)+r_bun*.2}" fill="none" stroke="{hs}" stroke-width="7" stroke-linecap="round"/>')
        g.append(rrect(CX - 50, HY - 78, 100, 18, 8, TEAL if not old else '#9a9aa8', sw=5))
    # cara
    if form == 'base':
        for sd in (-1, 1):  # ojos alegres medio cerrados + cejas gruesas arqueadas
            x = CX + sd * 30
            g.append(f'<path d="M{x-18},{HY+32} Q{x},{HY+14} {x+18},{HY+32} Z" {st("#fff", 5)}/>')
            g.append(f'<circle cx="{x}" cy="{HY+27}" r="6" fill="{K}"/>')
            g.append(f'<path d="M{x-22},{HY+6} Q{x},{HY-6} {x+22},{HY+6}" fill="none" stroke="{K}" stroke-width="9" stroke-linecap="round"/>')
        g.append(grin(CX, HY + 58, 34, big=False))
        g.append(line([(CX + 44, HY - 4), (CX + 50, HY + 4)], sh, 4))
    elif tam:
        for sd in (-1, 1):  # ojos brillantes blancos
            x = CX + sd * 30
            g.append(f'<path d="M{x-22},{HY+34} Q{x},{HY+14} {x+22},{HY+28} Z" {st(CYAN2, 5)}/>')
            g.append(line([(x - 26 * sd, HY + 8), (x + 22 * sd, HY + 2)], K, 9))
        g.append(grin(CX, HY + 54, 46))
        g.append(bolt([(CX - 52, HY + 40), (CX - 40, HY + 54), (CX - 52, HY + 66)], CYAN, 4))
    else:  # anciano
        g.append(laugh_eyes(CX, HY + 32))
        for sd in (-1, 1):
            g.append(line([(CX + sd * 48, HY + 26), (CX + sd * 58, HY + 36)], sh, 4))
            g.append(line([(CX + sd * 30, HY + 50), (CX + sd * 36, HY + 76)], sh, 4))
            g.append(f'<path d="M{CX+sd*8},{HY+6} Q{CX+sd*30},{HY-2} {CX+sd*52},{HY+8}" fill="none" stroke="#d8d8e2" stroke-width="8" stroke-linecap="round"/>')
        g.append(line([(CX - 26, HY - 14), (CX + 26, HY - 14)], sh, 4))
        g.append(grin(CX, HY + 60, 30))
    g.append(nose(sh))
    svg = ''.join(g)
    if old:
        svg = f'<g transform="rotate(-4 {CX} 900)">{svg}</g>'
    return svg_wrap(svg)

CHARS = {
    'kaen': lambda: kaen('base'), 'kaen_golpe': lambda: kaen('base', 1),
    'kaen_brasa': lambda: kaen('brasa'), 'kaen_brasa_golpe': lambda: kaen('brasa', 1),
    'kaen_rodillas': lambda: kaen('rodillas'),
    'tambo': lambda: tambo('base'), 'tambo_golpe': lambda: tambo('base', -1),
    'tambo_tambor': lambda: tambo('tambor'), 'tambo_tambor_golpe': lambda: tambo('tambor', -1),
    'tambo_tambor_gigante': lambda: tambo('tambor', -1, gigante=True),
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
