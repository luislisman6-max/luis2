"""Personajes originales KAEN y TAMBO, mismo estilo que video/personajes/dibujar.py.
Uso: python3 dibujar_kvt.py"""
import os, sys, json, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'personajes'))
from dibujar import st, line, poly, rrect, circ, spikes, arm, leg, eyes_angry, svg_wrap, K

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'personajes')
os.makedirs(OUT, exist_ok=True)

def torso_muscles(cx, tt, tb, sh):
    out = [line([(cx-105, tt+70), (cx-50, tt+92), (cx, tt+78), (cx+50, tt+92), (cx+105, tt+70)], sh, 6),
           line([(cx, tt+80), (cx, tb-15)], sh, 5)]
    for i, yy in enumerate((tt+128, tt+160, tt+190)):
        out.append(line([(cx-42+i*4, yy), (cx+42-i*4, yy)], sh, 5))
    return ''.join(out)

def head(cx, hy, skin):
    return (f'<path d="M{cx-60},{hy-40} Q{cx-64},{hy+50} {cx-34},{hy+80} L{cx},{hy+92} L{cx+34},{hy+80} '
            f'Q{cx+64},{hy+50} {cx+60},{hy-40} Q{cx},{hy-76} {cx-60},{hy-40} Z" {st(skin)}/>'
            + ''.join(f'<ellipse cx="{cx+s*64}" cy="{hy+10}" rx="12" ry="20" {st(skin,5)}/>' for s in (-1, 1)))

def grin(cx, y, w=40):
    return (f'<path d="M{cx-w},{y} Q{cx},{y-4} {cx+w},{y} Q{cx+w*.7},{y+36} {cx},{y+38} Q{cx-w*.7},{y+36} {cx-w},{y} Z" {st("#c8283a",5)}/>'
            f'<path d="M{cx-w+4},{y+2} Q{cx},{y-2} {cx+w-4},{y+2} L{cx+w-8},{y+11} Q{cx},{y+7} {cx-w+8},{y+11} Z" fill="#fff"/>')

def happy_eyes(cx, y, sep=30):
    return ''.join(line([(cx+s*sep-16, y+6), (cx+s*sep, y-8), (cx+s*sep+16, y+6)], K, 7) for s in (-1, 1))

# ---------------------------------------------------------------- KAEN
SK = '#e8b48c'; SK_SH = '#c48862'
def kaen(form='base', punch=0, pose='pie'):
    cx = 300; brasa = form == 'brasa'
    hair, hsh = ('#ff8a1f', '#d4560c') if brasa else ('#5a1a1a', '#3a0e0e')
    tunic = '#ff9a2e' if brasa else '#1e1a22'
    trim = '#fff1c2' if brasa else '#c22a2a'
    tt, tb = 368, 590
    g = []
    if brasa:  # llamas de fondo
        g.append(spikes(cx, 430, [(a, 300 + (40 if i % 2 else 0), 34) for i, a in enumerate(range(-150, 151, 25))], '#ffb02e', '#ff6a10'))
    # coleta alta
    g.append(circ(cx, 168, 30, hair)); g.append(spikes(cx, 190, [(150, 150, 20), (-150, 150, 20)], hair, hsh))
    kneel = pose == 'rodillas'
    if kneel:
        for s in (-1, 1):
            g.append(rrect(cx + s*54 - 42, 590, 84, 110, 14, '#2a2430'))
            g.append(rrect(cx + s*54 - 46, 690, 92, 40, 10, '#2a2430'))
            g.append(rrect(cx + s*54 + (10 if s > 0 else -90), 700, 80, 34, 10, '#3a2a1e'))
    else:
        for s in (-1, 1):
            g.append(leg(s, cx + s*54, 600, '#2a2430', '#3a2a1e', trim, L=220, w=84))
    for s in (-1, 1):
        p = s == punch
        g.append(arm(s, cx + s*124, tt + 32, SK, ang=86 if p else (6 if kneel else 16), up_len=120, fo_len=112, w=60,
                     band='#f2ead8', band_stripe='#c9b98f', flex=0 if p else -6))
    g.append(rrect(cx-30, 300, 60, 78, 10, SK))
    # túnica sin mangas cruzada
    g.append(poly([(cx-132, tt), (cx+132, tt), (cx+98, tb), (cx-98, tb)], tunic))
    g.append(poly([(cx-40, tt), (cx+40, tt), (cx+6, tt+120), (cx-6, tt+120)], SK, 5))
    g.append(torso_muscles(cx, tt-40, tt+120, SK_SH)[:0])
    g.append(line([(cx-40, tt), (cx+6, tt+120)], trim, 7)); g.append(line([(cx+40, tt), (cx-6, tt+120)], trim, 7))
    # sello en el pecho (se apaga al final)
    seal = {'base': '#ff5a1f', 'brasa': '#fff3a0', 'apagado': '#5a4a44'}[form if form != 'base' else 'base']
    g.append(f'<circle cx="{cx}" cy="{tt+70}" r="20" {st(seal,5)}/>')
    g.append(line([(cx-10, tt+70), (cx+10, tt+70)], K, 4)); g.append(line([(cx, tt+60), (cx, tt+80)], K, 4))
    # cinturón ancho
    g.append(rrect(cx-104, tb-30, 208, 38, 8, trim, sw=6))
    g.append(rrect(cx-22, tb-36, 44, 50, 8, '#1e1a22', sw=5))
    for s in (-1, 1):
        g.append(circ(cx + s*124, tt + 30, 44, tunic))
        g.append(f'<path d="M{cx+s*90},{tt+8} A40,40 0 0 {1 if s>0 else 0} {cx+s*160},{tt+8}" fill="none" stroke="{trim}" stroke-width="9"/>')
    hy = 245
    g.append(head(cx, hy, SK))
    # pelo recogido: casquete liso + mechones laterales
    cap = [(cx-66, hy+20), (cx-70, hy-38), (cx-36, hy-74), (cx, hy-80), (cx+36, hy-74), (cx+70, hy-38), (cx+66, hy+20),
           (cx+52, hy-14), (cx+20, hy-28), (cx-20, hy-28), (cx-52, hy-14)]
    g.append(poly(cap, hair))
    g.append(poly([(cx+28, hy-68), (cx+64, hy-38), (cx+52, hy-14), (cx+36, hy-36)], hsh, 0))
    for s in (-1, 1):
        g.append(poly([(cx+s*62, hy-10), (cx+s*76, hy+60), (cx+s*54, hy+30)], hair))
    # marca de brasa bajo un ojo (rasgo propio)
    g.append(poly([(cx+48, hy+44), (cx+56, hy+60), (cx+40, hy+58)], '#ff5a1f' if form != 'apagado' else '#7a5a50', 3))
    if form == 'apagado':
        g.append(''.join(line([(cx+s*30-16, hy+30), (cx+s*30+16, hy+30)], K, 6) for s in (-1, 1)))
        g.append(line([(cx-14, hy+70), (cx+14, hy+68)], K, 5))
    else:
        g.append(eyes_angry(cx, hy+28, 30, iris='#ff8a1f' if brasa else '#7a2a1a'))
        g.append(line([(cx-16, hy+70), (cx+16, hy+66)], K, 6))
    g.append(line([(cx-4, hy+40), (cx-8, hy+52), (cx+2, hy+54)], SK_SH, 4))
    return svg_wrap(''.join(g))

# ---------------------------------------------------------------- TAMBO
ST = '#d99a6c'; ST_SH = '#b06f45'
def tambo(form='base', punch=0, pose='pie'):
    cx = 300; nube = form == 'tambor'; viejo = form == 'viejo'
    hair, hsh = (('#ffffff', '#cfd6e6') if nube else ('#d8d8d8', '#a8a8a8') if viejo else ('#2a2018', '#4a3828'))
    vest = '#ffffff' if nube else '#2a8a8c'
    shorts = '#f2f4fa' if nube else '#6a4a2a'
    skin = '#c99070' if viejo else ST
    g = []
    tt, tb = 368, 580
    thin = viejo
    sw_ = 88 if thin else 128
    # pelo de atrás: rizos (círculos) o nube
    if nube:
        for i, (dx, dy, r) in enumerate([(-90, 220, 46), (-50, 170, 52), (0, 150, 58), (50, 170, 52), (90, 220, 46), (-110, 280, 36), (110, 280, 36)]):
            g.append(circ(cx+dx, dy, r, '#ffffff'))
            g.append(f'<circle cx="{cx+dx+r*.3}" cy="{dy+r*.3}" r="{r*.45}" fill="#dde3f0"/>')
        # bufanda de nube
        for i in range(6):
            g.append(circ(cx+150+i*34, 360-i*18, 26-i*2, '#ffffff', 5))
    else:
        g.append(spikes(cx, 225, [(-70, 130, 30), (-40, 150, 32), (-10, 160, 32), (20, 155, 32), (50, 140, 30), (80, 120, 26)], hair, hsh))
    for s in (-1, 1):
        g.append(leg(s, cx + s*48, 590, shorts, shorts, None, L=110, w=90 if not thin else 76))
    for s in (-1, 1):
        g.append(rrect(cx + s*48 - 32, 712, 64, 110, 18, skin))  # pantorrilla descubierta
        g.append(rrect(cx + s*48 - 40, 812, 80, 28, 8, '#a8743a' if not nube else '#ffffff'))  # sandalia
    for s in (-1, 1):
        p = s == punch
        if p and punch:
            # brazo elástico estirado (más largo)
            g.append(arm(s, cx + s*sw_, tt+30, skin, ang=88, up_len=170, fo_len=170, w=56 if not thin else 46, band=None, flex=0))
        else:
            g.append(arm(s, cx + s*sw_, tt+30, skin, ang=18, up_len=118, fo_len=108, w=58 if not thin else 44, band=None, flex=-8))
    g.append(rrect(cx-28, 300, 56, 78, 10, skin))
    g.append(poly([(cx-sw_-6, tt), (cx+sw_+6, tt), (cx+90, tb), (cx-90, tb)], skin))
    g.append(torso_muscles(cx, tt, tb, ST_SH) if not thin else '')
    if thin:
        for i in range(3):
            g.append(line([(cx-80, tt+40+i*22), (cx-50, tt+46+i*22)], '#9a6a4a', 4))
            g.append(line([(cx+80, tt+40+i*22), (cx+50, tt+46+i*22)], '#9a6a4a', 4))
    # chaleco abierto
    for s in (-1, 1):
        g.append(poly([(cx+s*(sw_+6), tt), (cx+s*44, tt), (cx+s*58, tb-4), (cx+s*90, tb-4)], vest))
    g.append(rrect(cx-96, tb-14, 192, 30, 8, '#f2c23a' if not nube else '#e6ebf5', sw=6))  # faja
    for s in (-1, 1):
        g.append(circ(cx + s*sw_, tt + 28, 38 if thin else 44, vest))
    hy = 245
    g.append(head(cx, hy, skin))
    if nube:
        for dx, dy, r in [(-50, -40, 34), (-14, -60, 38), (26, -58, 36), (58, -34, 30), (-66, 0, 22), (66, 0, 22)]:
            g.append(circ(cx+dx, hy+dy, r, '#ffffff'))
    else:
        cap = [(cx-66, hy+18), (cx-70, hy-38), (cx-36, hy-74), (cx, hy-80), (cx+36, hy-74), (cx+70, hy-38), (cx+66, hy+18),
               (cx+50, hy-6), (cx+30, hy-24), (cx+12, hy-4), (cx-8, hy-26), (cx-28, hy-4), (cx-48, hy-22)]
        g.append(poly(cap, hair))
        g.append(poly([(cx+28, hy-68), (cx+64, hy-38), (cx+50, hy-6), (cx+40, hy-36)], hsh, 0))
    # tirita en la nariz (rasgo propio) + ojos felices
    g.append(rrect(cx-14, hy+38, 28, 12, 4, '#f4e2c0', sw=3))
    if viejo:
        g.append(happy_eyes(cx, hy+26))
        for s in (-1, 1):
            g.append(line([(cx+s*44, hy+40), (cx+s*54, hy+56)], '#9a6a4a', 4))
        g.append(grin(cx, hy+60, 30))
    elif nube:
        for s in (-1, 1):
            g.append(f'<ellipse cx="{cx+s*30}" cy="{hy+26}" rx="18" ry="14" {st("#fff",5)}/>')
            g.append(f'<circle cx="{cx+s*30}" cy="{hy+26}" r="9" fill="#e23a3a"/><circle cx="{cx+s*30}" cy="{hy+26}" r="4" fill="{K}"/>')
        g.append(grin(cx, hy+56, 44))
    else:
        g.append(happy_eyes(cx, hy+26))
        g.append(grin(cx, hy+58, 40))
    return svg_wrap(''.join(g))

CHARS = {
    'kaen': lambda: kaen('base'), 'kaen_golpe': lambda: kaen('base', 1),
    'kaen_brasa': lambda: kaen('brasa'), 'kaen_brasa_golpe': lambda: kaen('brasa', 1),
    'kaen_rodillas': lambda: kaen('apagado', pose='rodillas'),
    'tambo': lambda: tambo('base'), 'tambo_golpe': lambda: tambo('base', -1),
    'tambo_tambor': lambda: tambo('tambor'), 'tambo_tambor_golpe': lambda: tambo('tambor', -1),
    'tambo_viejo': lambda: tambo('viejo'),
}

if __name__ == '__main__':
    for n, fn in CHARS.items():
        open(os.path.join(OUT, n + '.svg'), 'w').write(fn())
    js = """const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1000,height:1000},deviceScaleFactor:2});
for(const n of %s){await p.setContent('<html><body style="margin:0;background:transparent">'+fs.readFileSync('%s/'+n+'.svg','utf8')+'</body></html>');
await p.locator('svg').screenshot({path:'%s/'+n+'.png',omitBackground:true});}await b.close();})();""" % (json.dumps(list(CHARS)), OUT, OUT)
    subprocess.run(['node', '-e', js], check=True)
