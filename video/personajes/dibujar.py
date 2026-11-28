"""Personajes estilo referencia (vector plano, contorno negro grueso, cuerpo de bloques).
Genera SVG -> PNG transparente con Chromium. Uso: python3 dibujar.py"""
import math, os, sys
import subprocess, json

OUT = os.path.dirname(os.path.abspath(__file__))
K = '#111'          # contorno
SW = 7              # grosor contorno

def st(fill, w=SW, extra=''):
    return f'fill="{fill}" stroke="{K}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round" {extra}'

def line(pts, col=K, w=5):
    d = ' '.join(f'{x},{y}' for x, y in pts)
    return f'<polyline points="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'

def poly(pts, fill, w=SW):
    d = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return f'<polygon points="{d}" {st(fill, w)}/>'

def rrect(x, y, w, h, r, fill, rot=0, cx=None, cy=None, sw=SW):
    t = f'transform="rotate({rot} {cx if cx is not None else x+w/2} {cy if cy is not None else y})"' if rot else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" {st(fill, sw)} {t}/>'

def circ(x, y, r, fill, sw=SW):
    return f'<circle cx="{x}" cy="{y}" r="{r}" {st(fill, sw)}/>'

# ---------------------------------------------------------------- piezas
def spikes(cx, cy, specs, fill, shade):
    """specs: (ángulo°, largo, ancho_base). 0° = arriba, + = derecha."""
    out = []
    for ang, L, bw in specs:
        a = math.radians(ang)
        dx, dy = math.sin(a), -math.cos(a)
        px, py = -dy, dx
        bx, by = cx + dx * 40, cy + dy * 40
        tip = (cx + dx * L, cy + dy * L)
        p1 = (bx + px * bw, by + py * bw); p2 = (bx - px * bw, by - py * bw)
        mid = (bx + dx * L * 0.45, by + dy * L * 0.45)
        out.append(poly([p1, tip, p2], fill))
        out.append(f'<polygon points="{mid[0]:.1f},{mid[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{shade}" opacity=".55"/>')
    return ''.join(out)

def arm(side, sx, sy, skin, ang=18, up_len=120, fo_len=115, w=62, band='#1a1a1a', band_stripe='#fff',
        glove=None, sleeve=None, flex=0):
    """Brazo de bloques: hombro (sx,sy), ángulo hacia fuera. side = -1 izq, 1 der."""
    a = ang * side
    g = []
    t = f'rotate({-a} {sx} {sy})'
    g.append(f'<g transform="{t}">')
    g.append(rrect(sx - w / 2, sy, w, up_len, 22, sleeve or skin))
    ex, ey = sx, sy + up_len
    a2 = flex * side
    g.append(f'<g transform="rotate({-a2} {ex} {ey})">')
    g.append(rrect(ex - w / 2 + 3, ey - 12, w - 6, fo_len, 20, skin))
    # muñequera
    if band:
        g.append(rrect(ex - w / 2 - 2, ey + fo_len - 50, w + 4, 38, 8, band))
        if band_stripe:
            g.append(line([(ex - w / 2 + 4, ey + fo_len - 31), (ex + w / 2 - 4, ey + fo_len - 31)], band_stripe, 5))
    # puño
    fy = ey + fo_len - 14
    fc = glove or skin
    g.append(rrect(ex - w / 2 - 6, fy, w + 12, 66, 26, fc))
    for i in range(3):
        xx = ex - w / 2 + 10 + i * (w - 8) / 3 + (w - 8) / 6
        g.append(line([(xx, fy + 40), (xx, fy + 60)], K, 4))
    g.append('</g></g>')
    return ''.join(g)

def leg(side, hx, hy, pants, boot, boot_band=None, L=200, w=86, ang=4):
    g = [f'<g transform="rotate({ang*side} {hx} {hy})">']
    g.append(rrect(hx - w / 2, hy, w, L, 14, pants))
    by = hy + L - 10
    g.append(f'<path d="M{hx-w/2-4},{by} L{hx+w/2+4},{by} L{hx+w/2+4+18*side if side>0 else hx+w/2+4},{by+62} '
             f'L{hx-w/2-4-18 if side<0 else hx-w/2-4},{by+62} Z" {st(boot)}/>')
    if boot_band:
        g.append(rrect(hx - w / 2 - 4, by + 10, w + 8, 16, 4, boot_band, sw=5))
    g.append('</g>')
    return ''.join(g)

def eyes_blank(cx, y, sep=38, col='#fff'):
    """ojos en blanco de saiyajin furioso (Broly legendario)"""
    out = []
    for s in (-1, 1):
        x = cx + s * sep
        pts = [(x - 26 * s, y - 6), (x + 26 * s, y - 16), (x + 22 * s, y + 10), (x - 22 * s, y + 10)]
        out.append(poly(pts, col, 5))
    return ''.join(out)

def eyes_angry(cx, y, sep=38, iris='#2a8a3a'):
    out = []
    for s in (-1, 1):
        x = cx + s * sep
        pts = [(x - 24 * s, y - 4), (x + 24 * s, y - 14), (x + 20 * s, y + 10), (x - 20 * s, y + 10)]
        out.append(poly(pts, '#fff', 5))
        out.append(f'<circle cx="{x+2*s}" cy="{y+1}" r="8" fill="{iris}"/><circle cx="{x+2*s}" cy="{y+1}" r="4" fill="{K}"/>')
        out.append(line([(x - 30 * s, y - 14), (x + 28 * s, y - 30)], K, 9))
    return ''.join(out)

def jiren_eyes(cx, y, sep=44, skin='#e9e9ef'):
    out = []
    for s in (-1, 1):
        x = cx + s * sep
        out.append(f'<ellipse cx="{x}" cy="{y}" rx="22" ry="15" transform="rotate({-14*s} {x} {y})" fill="#1c1c22" stroke="{K}" stroke-width="5"/>')
        out.append(f'<ellipse cx="{x+6*s}" cy="{y-5}" rx="6" ry="4" fill="#a8a8b6"/>')
        out.append(line([(x - 18 * s, y - 18), (x + 22 * s, y - 30)], K, 6))
    return ''.join(out)

def svg_wrap(body, w=1000, h=1000):
    # lienzo ancho (x de -200 a 800) para que quepan los brazos estirados; ancla de los pies = (500, 915) px/2
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-200 0 {w} {h}" width="{w}" height="{h}">{body}</svg>'

# ---------------------------------------------------------------- BROLY
SKIN_B = '#f3b88a'; SKIN_B_SH = '#d58e5e'
PURP = '#7a3cb3'; GREEN_FUR = '#8fd63a'; GREEN_FUR_SH = '#5fa627'

def broly(form='legendario', punch=0):
    cx = 300
    hair = {'base': ('#1b1b20', '#3a3a48'), 'ssj': ('#ffd83a', '#e8a21a'), 'legendario': ('#a6ea3c', '#6bb82a')}[form]
    big = form == 'legendario'
    S = 1.0
    shoulder_w = 150 if big else 118
    torso_top, torso_bot = 365, 585
    g = []
    # pelo de atrás
    if form == 'base':
        sp = [(-70, 150, 26), (-45, 175, 28), (-20, 185, 28), (5, 190, 28), (30, 180, 28), (55, 165, 26), (80, 140, 24), (-95, 120, 22), (100, 120, 22)]
    else:
        sp = [(-95, 175, 26), (-75, 205, 28), (-52, 235, 30), (-30, 255, 30), (-10, 270, 30), (10, 270, 30), (30, 255, 30),
              (52, 235, 30), (75, 205, 28), (95, 175, 26), (-118, 140, 22), (118, 140, 22)]
    g.append(spikes(cx, 235, [(a, L, w * 1.45) for a, L, w in sp], *hair))
    # piernas
    g.append(leg(-1, cx - 58, 640, PURP, '#f4f4f6', '#1a1a1a', L=210, w=96 if big else 84))
    g.append(leg(1, cx + 58, 640, PURP, '#f4f4f6', '#1a1a1a', L=210, w=96 if big else 84))
    # brazos (detrás del torso)
    sleeve = None
    for s in (-1, 1):
        p = s == punch
        g.append(arm(s, cx + s * (shoulder_w + 6), torso_top + 30, SKIN_B, ang=86 if p else 20, up_len=130 if big else 118,
                     fo_len=125 if big else 112, w=74 if big else 62, flex=0 if p else -6))
    # cuello
    g.append(rrect(cx - (40 if big else 32), 300, 80 if big else 64, 80, 10, SKIN_B))
    # torso
    tw_top = shoulder_w + 10; tw_bot = 105 if big else 88
    g.append(poly([(cx - tw_top, torso_top), (cx + tw_top, torso_top), (cx + tw_bot, torso_bot), (cx - tw_bot, torso_bot)], SKIN_B))
    # musculatura
    g.append(line([(cx - 120, torso_top + 70), (cx - 60, torso_top + 95), (cx, torso_top + 80), (cx + 60, torso_top + 95), (cx + 120, torso_top + 70)], SKIN_B_SH, 6))
    g.append(line([(cx, torso_top + 82), (cx, torso_bot - 15)], SKIN_B_SH, 5))
    for i, yy in enumerate((torso_top + 130, torso_top + 165, torso_top + 198)):
        ww = 46 - i * 4
        g.append(line([(cx - ww, yy), (cx + ww, yy)], SKIN_B_SH, 5))
    if form != 'legendario':
        # chaleco negro tipo tirantes + gema verde (Broly película)
        g.append(poly([(cx - tw_top + 20, torso_top), (cx - 40, torso_top), (cx - 52, torso_bot - 10), (cx - tw_bot + 4, torso_bot - 10)], '#18181d'))
        g.append(poly([(cx + tw_top - 20, torso_top), (cx + 40, torso_top), (cx + 52, torso_bot - 10), (cx + tw_bot - 4, torso_bot - 10)], '#18181d'))
        g.append(poly([(cx - 70, torso_top + 40), (cx + 70, torso_top + 40), (cx + 60, torso_top + 150), (cx - 60, torso_top + 150)], '#18181d'))
        g.append(poly([(cx, torso_top + 60), (cx + 24, torso_top + 80), (cx + 24, torso_top + 112), (cx, torso_top + 130), (cx - 24, torso_top + 112), (cx - 24, torso_top + 80)], '#38c45a', 5))
        g.append(poly([(cx, torso_top + 74), (cx + 12, torso_top + 86), (cx, torso_top + 98), (cx - 12, torso_top + 86)], '#9df0a8', 0))
    # hombreras redondas (deltoides)
    for s in (-1, 1):
        g.append(circ(cx + s * (shoulder_w + 2), torso_top + 32, 52 if big else 42, SKIN_B))
        if form != 'legendario':
            g.append(f'<path d="M{cx+s*(shoulder_w-38)},{torso_top+20} A44,44 0 0 {1 if s>0 else 0} {cx+s*(shoulder_w+42)},{torso_top+20}" fill="none" stroke="#2fae4a" stroke-width="12"/>')
    # collar
    g.append(rrect(cx - 46, 352, 92, 22, 10, '#e6e6ea' if form != 'base' else '#d8d8de', sw=5))
    # faldón de piel verde
    fy = torso_bot - 12
    zig = []
    n = 9
    for i in range(n + 1):
        x = cx - 150 + i * 300 / n
        zig.append((x, fy + 110 + (18 if i % 2 else 0)))
    g.append(poly([(cx - 128, fy), (cx + 128, fy)] + [(x, y) for x, y in reversed(zig)][::-1][::-1][::-1][:0] + list(reversed(zig)), GREEN_FUR))
    ww = []
    for i in range(9):
        ww.append((cx - 90 + i * 22.5, fy + 40 + (30 if i % 2 else 0)))
    g.append(line(ww, GREEN_FUR_SH, 6))
    g.append(rrect(cx - 130, fy - 6, 260, 24, 8, '#3a2a18', sw=5))
    # cabeza
    hy = 250
    g.append(f'<path d="M{cx-62},{hy-40} Q{cx-66},{hy+50} {cx-36},{hy+82} L{cx},{hy+96} L{cx+36},{hy+82} Q{cx+66},{hy+50} {cx+62},{hy-40} Q{cx},{hy-78} {cx-62},{hy-40} Z" {st(SKIN_B)}/>')
    # orejas
    for s in (-1, 1):
        g.append(f'<ellipse cx="{cx+s*66}" cy="{hy+10}" rx="12" ry="20" {st(SKIN_B, 5)}/>')
    # flequillo
    fr = [(-50, 120, 24), (-22, 105, 22), (8, 110, 22), (35, 118, 22), (58, 112, 20)] if form != 'base' else [(-40, 95, 20), (-10, 92, 20), (20, 95, 20), (45, 90, 18)]
    g.append(spikes(cx, hy - 12, [(a + 180 * 0, -L * 0.0 + L, w) for a, L, w in []], *hair))
    # casquete de pelo con flequillo en picos sobre la frente
    col, shd = hair
    cap = [(cx - 70, hy + 14), (cx - 74, hy - 40), (cx - 40, hy - 74), (cx, hy - 82), (cx + 40, hy - 74), (cx + 74, hy - 40), (cx + 70, hy + 14),
           (cx + 56, hy - 18), (cx + 40, hy + 2), (cx + 26, hy - 22), (cx + 6, hy - 2), (cx - 8, hy - 24), (cx - 28, hy + 0), (cx - 40, hy - 20), (cx - 56, hy - 2)]
    g.append(poly(cap, col))
    g.append(poly([(cx + 30, hy - 70), (cx + 66, hy - 40), (cx + 56, hy - 18), (cx + 40, hy - 40)], shd, 0))
    # diadema/ceja verde característica (legendario)
    if form == 'legendario':
        g.append(poly([(cx - 52, hy - 2), (cx - 6, hy + 8), (cx - 8, hy + 18), (cx - 54, hy + 8)], '#3e9a32', 4))
        g.append(poly([(cx + 52, hy - 2), (cx + 6, hy + 8), (cx + 8, hy + 18), (cx + 54, hy + 8)], '#3e9a32', 4))
        g.append(eyes_blank(cx, hy + 30, 30))
        # boca abierta gritando/sonriendo
        g.append(f'<path d="M{cx-32},{hy+56} Q{cx},{hy+50} {cx+32},{hy+56} Q{cx+22},{hy+88} {cx},{hy+88} Q{cx-22},{hy+88} {cx-32},{hy+56} Z" {st("#c8283a", 5)}/>')
        g.append(f'<path d="M{cx-28},{hy+58} Q{cx},{hy+53} {cx+28},{hy+58} L{cx+24},{hy+66} Q{cx},{hy+61} {cx-24},{hy+66} Z" fill="#fff"/>')
    else:
        g.append(eyes_angry(cx, hy + 28, 30, iris='#2a8a3a' if form == 'base' else '#2ab0c8'))
        g.append(line([(cx - 18, hy + 70), (cx + 18, hy + 66)], K, 6))
    g.append(line([(cx - 4, hy + 40), (cx - 8, hy + 52), (cx + 2, hy + 54)], SKIN_B_SH, 4))
    return svg_wrap(''.join(g))

# ---------------------------------------------------------------- JIREN
J_SKIN = '#e9e9ef'; J_SH = '#b9b9c6'; J_RED = '#d9263a'; J_RED_SH = '#9c1424'
J_SKIN_RED = '#e4566a'; J_SKIN_RED_SH = '#b23348'

def jiren(form='normal', punch=0):
    cx = 300
    red = form == 'rojo'
    skin = J_SKIN_RED if red else J_SKIN
    sh = J_SKIN_RED_SH if red else J_SH
    g = []
    torso_top, torso_bot = 372, 600
    # piernas negras + botas blancas
    for s in (-1, 1):
        g.append(leg(s, cx + s * 52, 588, '#1b1b20', '#f2f2f5', '#bfc0c8', L=262, w=84))
    # brazos
    for s in (-1, 1):
        p = s == punch
        g.append(arm(s, cx + s * 150, torso_top + 40, skin if red else '#1b1b20', ang=86 if p else 12, up_len=125, fo_len=118, w=66,
                     band=None, glove='#f2f2f5' if not red else skin, flex=0 if p else -4))
    # cuello
    g.append(rrect(cx - 30, 320, 60, 70, 10, skin))
    # torso
    g.append(poly([(cx - 150, torso_top), (cx + 150, torso_top), (cx + 96, torso_bot), (cx - 96, torso_bot)], skin if red else '#1b1b20'))
    if red:
        g.append(line([(cx - 110, torso_top + 70), (cx - 50, torso_top + 95), (cx, torso_top + 80), (cx + 50, torso_top + 95), (cx + 110, torso_top + 70)], sh, 6))
        g.append(line([(cx, torso_top + 82), (cx, torso_bot - 15)], sh, 5))
        for i, yy in enumerate((torso_top + 130, torso_top + 165, torso_top + 198)):
            g.append(line([(cx - 44 + i * 4, yy), (cx + 44 - i * 4, yy)], sh, 5))
        # cicatrices / uniforme roto
        g.append(line([(cx - 120, torso_top + 30), (cx - 80, torso_top + 60)], '#fff', 4))
        g.append(line([(cx + 70, torso_top + 120), (cx + 110, torso_top + 95)], '#fff', 4))
    else:
        # pechera roja con franja
        g.append(poly([(cx - 150, torso_top), (cx + 150, torso_top), (cx + 128, torso_top + 110), (cx - 128, torso_top + 110)], J_RED))
        g.append(line([(cx - 120, torso_top + 70), (cx + 120, torso_top + 70)], J_RED_SH, 6))
        # líneas del traje
        g.append(line([(cx, torso_top + 110), (cx, torso_bot - 8)], '#444450', 5))
        for yy in (torso_top + 150, torso_top + 185):
            g.append(line([(cx - 34, yy), (cx + 34, yy)], '#444450', 5))
        g.append(rrect(cx - 100, torso_bot - 20, 200, 26, 6, '#2a2a30', sw=5))
    # hombreras gigantes rojas
    for s in (-1, 1):
        x = cx + s * 150
        g.append(f'<ellipse cx="{x}" cy="{torso_top + 30}" rx="62" ry="54" {st(J_RED if not red else skin)}/>')
        g.append(f'<path d="M{x-40*s},{torso_top+4} Q{x+10*s},{torso_top-6} {x+40*s},{torso_top+30}" fill="none" stroke="#ffffff" stroke-opacity=".6" stroke-width="7" stroke-linecap="round"/>')
    # cabeza: calva, ancha arriba, mandíbula cuadrada
    hy = 230
    g.append(f'<path d="M{cx-70},{hy-10} Q{cx-74},{hy-96} {cx},{hy-100} Q{cx+74},{hy-96} {cx+70},{hy-10} '
             f'L{cx+62},{hy+60} Q{cx+50},{hy+96} {cx},{hy+100} Q{cx-50},{hy+96} {cx-62},{hy+60} Z" {st(skin)}/>')
    # "orejas" circulares tipo auricular
    for s in (-1, 1):
        g.append(circ(cx + s * 72, hy + 18, 20, skin, 5))
        g.append(circ(cx + s * 72, hy + 18, 9, sh, 4))
    # sombra lateral de la cabeza
    g.append(f'<path d="M{cx+50},{hy-60} Q{cx+66},{hy} {cx+52},{hy+70}" fill="none" stroke="{sh}" stroke-width="8" stroke-linecap="round"/>')
    g.append(jiren_eyes(cx, hy + 18, 38))
    g.append(line([(cx - 3, hy + 34), (cx - 9, hy + 58), (cx + 3, hy + 60)], sh, 4))
    g.append(line([(cx - 18, hy + 78), (cx + 18, hy + 78)], K, 5))
    # marcas faciales (mejillas)
    for s in (-1, 1):
        g.append(line([(cx + s * 40, hy + 50), (cx + s * 58, hy + 40)], '#ffffff' if red else sh, 4))
    return svg_wrap(''.join(g))

CHARS = {
    'broly_base': lambda: broly('base'),
    'broly_ssj': lambda: broly('ssj'),
    'broly_legendario': lambda: broly('legendario'),
    'jiren': lambda: jiren('normal'),
    'jiren_rojo': lambda: jiren('rojo'),
    'jiren_golpe': lambda: jiren('normal', 1),
    'jiren_rojo_golpe': lambda: jiren('rojo', 1),
    'broly_base_golpe': lambda: broly('base', -1),
    'broly_ssj_golpe': lambda: broly('ssj', -1),
    'broly_legendario_golpe': lambda: broly('legendario', -1),
}

if __name__ == '__main__':
    for name, fn in CHARS.items():
        open(os.path.join(OUT, name + '.svg'), 'w').write(fn())
    js = """const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1000,height:1000},deviceScaleFactor:2});
for(const n of %s){await p.setContent('<html><body style="margin:0;background:transparent">'+fs.readFileSync('%s/'+n+'.svg','utf8')+'</body></html>');
await p.locator('svg').screenshot({path:'%s/'+n+'.png',omitBackground:true});console.log('ok',n);}await b.close();})();""" % (json.dumps(list(CHARS)), OUT, OUT)
    subprocess.run(['node', '-e', js], check=True)
