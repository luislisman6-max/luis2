"""JIREN vs BROLY — render 1080x1920 sincronizado con la voz (tiempos de words.json).
Uso:  python3 render_jvb.py out            -> render completo en partes
      python3 render_jvb.py out stills 1.0 10.5 ...
"""
import sys, os, json, math, random, subprocess
from functools import lru_cache
from multiprocessing import Process
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from lib import W, H, FPS, rgba, layer, vgrad, blur, clamp, prog, ease_out, ease_in_out, ease_back, lerp

PJ = os.path.join(HERE, '..', 'personajes')
DUR = 92.40
NFR = int(DUR * FPS)
BEBAS = os.path.join(HERE, 'fonts', 'BebasNeue.ttf')
ANTON = os.path.join(HERE, 'fonts', 'Anton.ttf')
GY = 1250            # suelo (pies)
HOR = 1150           # horizonte del escenario
REACH = 910          # px del sprite desde el ancla hasta la punta del puño
ANC = (1000, 1830)   # ancla (pies) en el sprite 2000x2000
HEADY = {'j': 470, 'b': 500}

RED, GREEN, GOLD, CYAN, WHITE = '#ff3b4e', '#7dff3a', '#ffd23a', '#5fe6ff', '#ffffff'


@lru_cache(maxsize=None)
def F(path, size):
    return ImageFont.truetype(path, int(size))


# ============================================================ sprites
@lru_cache(maxsize=None)
def raw(name):
    return Image.open(os.path.join(PJ, name + '.png')).convert('RGBA')


@lru_cache(maxsize=None)
def tinted(name, mode):
    im = raw(name)
    if mode == 'sil':
        a = im.getchannel('A')
        out = Image.new('RGBA', im.size, (12, 8, 16, 255)); out.putalpha(a); return out
    return im


@lru_cache(maxsize=48)
def scaled(name, q, mode=None):
    s = q / 200.0
    im = tinted(name, mode) if mode else raw(name)
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)


def paste(dst, src, x, y, alpha=1.0):
    """alpha_composite recortando (x,y = esquina sup-izq, puede ser negativa)."""
    x, y = int(round(x)), int(round(y))
    sx0, sy0 = max(0, -x), max(0, -y)
    sx1, sy1 = min(src.width, dst.width - x), min(src.height, dst.height - y)
    if sx1 <= sx0 or sy1 <= sy0:
        return
    part = src.crop((sx0, sy0, sx1, sy1))
    if alpha < 0.999:
        a = part.getchannel('A').point(lambda v: int(v * alpha)); part = part.copy(); part.putalpha(a)
    dst.alpha_composite(part, (x + sx0, y + sy0))


def place(dst, name, x, y, s, rot=0.0, alpha=1.0, mode=None):
    """coloca el personaje con los pies en (x,y). rot gira alrededor del pecho."""
    q = max(4, int(round(s * 200)))
    im = scaled(name, q, mode)
    s = q / 200.0
    if rot:
        cx, cy = ANC[0] * s, (ANC[1] - 900) * s       # pivote en el pecho
        im = im.rotate(rot, resample=Image.BILINEAR, center=(cx, cy))
    paste(dst, im, x - ANC[0] * s, y - ANC[1] * s, alpha)


@lru_cache(maxsize=24)
def head_crop(name, q):
    im = raw(name).crop((400, 0, 1600, 1250))
    s = q / 200.0
    return im.resize((int(im.width * s), int(im.height * s)), Image.BILINEAR)


def head(dst, name, cx, cy, s, alpha=1.0):
    """primer plano: centro de la cara en (cx,cy)."""
    q = max(4, int(round(s * 200)))
    im = head_crop(name, q); s = q / 200.0
    hy = HEADY['j' if name.startswith('j') else 'b']
    paste(dst, im, cx - 600 * s, cy - hy * s, alpha)


# ============================================================ fondos
def hexagon(d, cx, cy, r, rot, fill, outline, w=5):
    pts = [(cx + r * math.cos(rot + k * math.pi / 3), cy + r * math.sin(rot + k * math.pi / 3)) for k in range(6)]
    d.polygon(pts, fill=fill, outline=outline)
    d.line(pts + [pts[0]], fill=outline, width=w, joint='curve')


@lru_cache(maxsize=None)
def bg_arena(red=False):
    rnd = random.Random(3 if red else 4)
    top, hor = ('#2a0707', '#e4562c') if red else ('#1a0b38', '#c2477f')
    img = vgrad((W, H), rgba(top), rgba(hor))
    g = layer(); ImageDraw.Draw(g).ellipse([240, 760, 840, 1260], fill=rgba('#ffd27a' if red else '#ff8fc0', 170))
    img.alpha_composite(blur(g, 80))
    d = ImageDraw.Draw(img)
    # aro decorativo superior (como la referencia)
    d.ellipse([-260, 150, W + 260, 470], outline=rgba('#000000', 70), width=26)
    d.ellipse([-260, 150, W + 260, 470], outline=rgba('#ff9a6a' if red else '#b58cff', 90), width=5)
    for _ in range(16):
        x, y, r = rnd.randint(0, W), rnd.randint(250, 800), rnd.randint(18, 46)
        hexagon(d, x, y, r, rnd.random(), rgba('#3a0a0a' if red else '#2b1550', 230), rgba('#ff7a4a' if red else '#c79bff', 200), 4)
    # skyline
    sky = rgba('#3a0c0c' if red else '#25103f')
    x = -20
    while x < W:
        w = rnd.randint(70, 150); h = rnd.randint(160, 420)
        d.rectangle([x, HOR - h, x + w, HOR], fill=sky)
        for wy in range(HOR - h + 30, HOR - 15, 46):
            for wx in range(x + 14, x + w - 20, 34):
                if rnd.random() < 0.35:
                    d.rectangle([wx, wy, wx + 12, wy + 18], fill=rgba('#ffb36b' if red else '#ff7fd0', 120))
        x += w + rnd.randint(4, 30)
    # suelo con rejilla en perspectiva
    d.rectangle([0, HOR, W, H], fill=rgba('#2e0a0a' if red else '#2a1840'))
    gl = rgba('#ff6a4a' if red else '#9a6ad8', 110)
    for k in range(-14, 15):
        d.line([(540 + k * 40, HOR), (540 + k * 260, H)], fill=gl, width=3)
    yy = HOR; step = 22
    while yy < H:
        d.line([(0, yy), (W, yy)], fill=gl, width=3); yy += step; step *= 1.35
    d.line([(0, HOR), (W, HOR)], fill=rgba('#ffb08a' if red else '#e0a8ff', 200), width=5)
    return img


@lru_cache(maxsize=None)
def bg_space(galaxy=True, moon=False, planet=False):
    rnd = random.Random(9)
    img = vgrad((W, H), rgba('#06041a'), rgba('#180c36'))
    d = ImageDraw.Draw(img)
    neb = layer(); nd = ImageDraw.Draw(neb)
    for _ in range(6):
        x, y, r = rnd.randint(0, W), rnd.randint(0, H), rnd.randint(200, 420)
        nd.ellipse([x - r, y - r, x + r, y + r], fill=rgba(rnd.choice(['#5a2a9a', '#2a3a9a', '#8a2a7a']), 60))
    img.alpha_composite(blur(neb, 120))
    for _ in range(380):
        x, y = rnd.randint(0, W), rnd.randint(0, H); r = rnd.choice([1, 1, 2, 2, 3])
        d.ellipse([x - r, y - r, x + r, y + r], fill=rgba('#ffffff', rnd.randint(120, 255)))
    if galaxy:
        gal = layer(1600, 1600); gd = ImageDraw.Draw(gal)
        cols = ['#7a4cff', '#c05cff', '#4ab0ff', '#ff7ad0', '#e6c07a']
        for i in range(9):
            rx, ry = 120 + i * 85, 50 + i * 34
            gd.ellipse([800 - rx, 800 - ry, 800 + rx, 800 + ry], outline=rgba(cols[i % 5], 180), width=14 - i)
        core = layer(1600, 1600); ImageDraw.Draw(core).ellipse([650, 720, 950, 880], fill=rgba('#fff2c8', 230))
        gal.alpha_composite(blur(core, 40))
        gal = blur(gal, 3).rotate(-18, resample=Image.BICUBIC)
        img.alpha_composite(gal, (540 - 800, 820 - 800))
    if moon:
        d.ellipse([60, 200, 340, 480], fill=rgba('#bdb8c8'), outline=rgba('#111111'), width=6)
        for cx, cy, r in ((150, 300, 30), (240, 390, 22), (260, 270, 16), (130, 410, 14)):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgba('#9a94a8'))
    if planet:
        pg = layer(); ImageDraw.Draw(pg).ellipse([-500, 1400, W + 500, 3200], fill=rgba('#6ad0ff', 150))
        img.alpha_composite(blur(pg, 50))
        d.ellipse([-420, 1470, W + 420, 3120], fill=rgba('#2a6ad8'), outline=rgba('#111111'), width=8)
        for cx, cy, rx, ry in ((200, 1640, 140, 50), (720, 1700, 200, 60), (460, 1820, 120, 40)):
            d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=rgba('#1c4fae'))
    return img


@lru_cache(maxsize=None)
def bg_burst(col, dark, cx=540, cy=860, n=30):
    img = Image.new('RGBA', (W, H), rgba(dark))
    d = ImageDraw.Draw(img)
    for i in range(n):
        a0 = i * 2 * math.pi / n; a1 = a0 + math.pi / n
        d.polygon([(cx, cy), (cx + 2600 * math.cos(a0), cy + 2600 * math.sin(a0)), (cx + 2600 * math.cos(a1), cy + 2600 * math.sin(a1))],
                  fill=rgba(col, 120))
    g = layer(); ImageDraw.Draw(g).ellipse([cx - 420, cy - 520, cx + 420, cy + 520], fill=rgba(col, 230))
    img.alpha_composite(blur(g, 140))
    return img


@lru_cache(maxsize=None)
def bg_smoke():
    rnd = random.Random(11)
    img = vgrad((W, H), rgba('#120c16'), rgba('#3a2a32'))
    s = layer(); sd = ImageDraw.Draw(s)
    for _ in range(26):
        x, y, r = rnd.randint(-100, W + 100), rnd.randint(200, 1500), rnd.randint(120, 300)
        sd.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=rgba(rnd.choice(['#4a3a48', '#2a2030', '#5a4650']), 150))
    img.alpha_composite(blur(s, 50))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1390, W, H], fill=rgba('#1a1014'))
    for _ in range(26):
        hexagon(d, rnd.randint(0, W), rnd.randint(1390, H), rnd.randint(24, 60), rnd.random(), rgba('#24141a'), rgba('#e8873a', 220), 4)
    return img


@lru_cache(maxsize=None)
def bg_city_buildings():
    img = bg_arena(True).copy()
    d = ImageDraw.Draw(img)
    for x, w, h in ((60, 150, 820), (300, 120, 640), (820, 170, 900)):
        d.rectangle([x, HOR - h, x + w, HOR], fill=rgba('#1e0606'), outline=rgba('#111111'), width=6)
    return img


# ============================================================ efectos
def shake_off(t, t0, amp, dur=0.45):
    if t < t0 or t > t0 + dur:
        return 0.0, 0.0
    k = 1 - (t - t0) / dur
    return amp * k * math.sin((t - t0) * 95), amp * k * math.cos((t - t0) * 77)


def star(img, x, y, t, t0, size=260, col='#ffffff', col2='#ffe14a', dur=0.32):
    p = (t - t0) / dur
    if p < 0 or p > 1:
        return
    L = layer(); d = ImageDraw.Draw(L)
    r = size * (0.5 + 0.8 * ease_out(p)); a = int(255 * (1 - p) ** 0.7)
    rnd = random.Random(int(t0 * 100))
    for rr, c in ((r, col2), (r * 0.62, col)):
        pts = []
        for k in range(24):
            ang = k * math.pi / 12 + rnd.random() * 0.1
            rad = rr if k % 2 == 0 else rr * 0.42
            pts.append((x + rad * math.cos(ang), y + rad * math.sin(ang)))
        d.polygon(pts, fill=rgba(c, a))
    rr = size * (0.4 + 1.6 * ease_out(p))
    d.ellipse([x - rr, y - rr * 0.55, x + rr, y + rr * 0.55], outline=rgba('#ffffff', a), width=max(2, int(14 * (1 - p))))
    img.alpha_composite(L)


def ring(img, x, y, t, t0, col, maxr=500, dur=0.5, w=12, flat=0.55):
    p = (t - t0) / dur
    if p < 0 or p > 1:
        return
    d = ImageDraw.Draw(img); r = maxr * ease_out(p); a = int(255 * (1 - p))
    d.ellipse([x - r, y - r * flat, x + r, y + r * flat], outline=rgba(col, a), width=max(2, int(w * (1 - p) + 2)))


def flash(img, a, col='#ffffff'):
    if a <= 0:
        return
    img.alpha_composite(Image.new('RGBA', (W, H), rgba(col, int(255 * clamp(a)))))


def speedlines(img, t, col='#ffffff', a=150, cx=540, cy=900, n=40, seed=0):
    d = ImageDraw.Draw(img)
    rnd = random.Random(int(t * 30) * 7 + seed)
    for _ in range(n):
        ang = rnd.random() * 2 * math.pi; r0 = rnd.randint(520, 760); r1 = r0 + rnd.randint(300, 700)
        d.line([(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)), (cx + r1 * math.cos(ang), cy + r1 * math.sin(ang))],
               fill=rgba(col, a), width=rnd.randint(3, 9))


def hlines(img, t, col='#ffffff', a=140, n=22, seed=0):
    d = ImageDraw.Draw(img); rnd = random.Random(int(t * 30) + seed)
    for _ in range(n):
        y = rnd.randint(300, 1700); x = rnd.randint(-200, W); L = rnd.randint(200, 600)
        d.line([(x, y), (x + L, y)], fill=rgba(col, a), width=rnd.randint(3, 8))


def aura(img, x, y, s, t, col, strength=1.0):
    """aura de energía tras el personaje (pies en x,y; escala s)."""
    hgt = 1750 * s; wid = 700 * s
    L = layer(); d = ImageDraw.Draw(L)
    cx, cy = x, y - hgt * 0.48
    rnd = random.Random(int(t * 15))
    g = layer(); ImageDraw.Draw(g).ellipse([cx - wid, cy - hgt * 0.62, cx + wid, cy + hgt * 0.6], fill=rgba(col, int(150 * strength)))
    img.alpha_composite(blur(g, 60 * s + 10))
    for k in range(26):
        ang = -math.pi / 2 + (k - 13) * 0.2 + rnd.uniform(-0.05, 0.05)
        r0 = wid * 0.7; r1 = wid * (1.0 + rnd.random() * 0.9) * (1.3 if abs(k - 13) < 5 else 1)
        bx, by = cx + r0 * math.cos(ang) * 0.8, cy + r0 * math.sin(ang) * 1.25
        tx, ty = cx + r1 * math.cos(ang) * 0.8, cy + r1 * math.sin(ang) * 1.25
        px, py = -math.sin(ang) * 22 * s * 4, math.cos(ang) * 22 * s * 4
        d.polygon([(bx + px, by + py), (tx, ty), (bx - px, by - py)], fill=rgba(col, int(190 * strength)))
    img.alpha_composite(L)
    # chispas
    d = ImageDraw.Draw(img)
    for k in range(10):
        px = cx + rnd.uniform(-wid, wid); py = cy + rnd.uniform(-hgt * 0.5, hgt * 0.5)
        d.line([(px, py), (px + rnd.uniform(-20, 20), py - rnd.uniform(30, 70))], fill=rgba('#ffffff', 200), width=4)


def dust(img, x, y, t, t0, dur=0.8, n=14, col='#d8c0e0', spread=260):
    p = (t - t0) / dur
    if p < 0 or p > 1:
        return
    d = ImageDraw.Draw(img); rnd = random.Random(int(t0 * 77))
    for _ in range(n):
        ang = rnd.uniform(math.pi, 2 * math.pi); sp = rnd.uniform(0.3, 1)
        px = x + math.cos(ang) * spread * sp * ease_out(p); py = y + math.sin(ang) * spread * 0.35 * sp * ease_out(p)
        r = rnd.uniform(18, 46) * (0.6 + p)
        d.ellipse([px - r, py - r, px + r, py + r], fill=rgba(col, int(170 * (1 - p))))


def debris(img, x, y, t, t0, dur=1.0, n=16, col='#5a1a1a', out='#ff8a5a', spread=900, grav=1400, size=(18, 46)):
    p = t - t0
    if p < 0 or p > dur:
        return
    d = ImageDraw.Draw(img); rnd = random.Random(int(t0 * 31))
    for _ in range(n):
        ang = rnd.uniform(0, 2 * math.pi); v = rnd.uniform(0.4, 1) * spread
        px = x + math.cos(ang) * v * p; py = y + math.sin(ang) * v * p + 0.5 * grav * p * p
        hexagon(d, px, py, rnd.uniform(*size), rnd.random() + p * 4, rgba(col), rgba(out), 4)


def lightning(img, x0, y0, x1, y1, seed, col='#e6d8ff', w=5, segs=12, jit=60):
    rnd = random.Random(seed); d = ImageDraw.Draw(img)
    pts = [(x0, y0)]
    for i in range(1, segs):
        f = i / segs
        pts.append((x0 + (x1 - x0) * f + rnd.uniform(-jit, jit), y0 + (y1 - y0) * f + rnd.uniform(-jit, jit)))
    pts.append((x1, y1))
    d.line(pts, fill=rgba(col, 120), width=w * 3, joint='curve')
    d.line(pts, fill=rgba('#ffffff', 255), width=w, joint='curve')


def orb(img, x, y, r, col):
    g = layer(); ImageDraw.Draw(g).ellipse([x - r * 2, y - r * 2, x + r * 2, y + r * 2], fill=rgba(col, 160))
    img.alpha_composite(blur(g, r * 0.6 + 4))
    d = ImageDraw.Draw(img)
    d.ellipse([x - r, y - r, x + r, y + r], fill=rgba(col), outline=rgba('#111111'), width=5)
    d.ellipse([x - r * 0.55, y - r * 0.55, x + r * 0.55, y + r * 0.55], fill=rgba('#ffffff', 210))


def floating_hex(img, t, seed, col, out, n=10):
    d = ImageDraw.Draw(img); rnd = random.Random(seed)
    for _ in range(n):
        x0, y0, sp, r = rnd.uniform(0, W), rnd.uniform(250, 1300), rnd.uniform(15, 50), rnd.uniform(16, 40)
        hexagon(d, (x0 + sp * t) % (W + 100) - 50, y0 + 14 * math.sin(t * 1.3 + x0), r, t * 0.4 + x0, rgba(col), rgba(out), 4)


# ============================================================ escenas
def jx_from_tip(tip, s):
    return tip - REACH * s


def bx_from_tip(tip, s):
    return tip + REACH * s


def dash(t, t0, t1, a, b):
    return lerp(a, b, ease_in_out(prog(t, t0, t1 - t0)))


S_DUEL = 0.36


def sc_hook(t):
    img = bg_burst('#ff2a3a', '#2a0508').copy()
    speedlines(img, t, '#ffffff', 90)
    z = 1.0 + 0.05 * t
    head(img, 'jiren', 540, 860, 1.05 * z)
    dust(img, 540, 1650, t, 2.0, 0.7, col='#ffb0b0', spread=420)
    return img, 1.0, shake_off(t, 2.0, 30)


def sc_grow(t):
    img = bg_burst('#6aff2a', '#0a2a06').copy()
    steps = [(2.78, 0.33), (3.00, 0.40), (3.48, 0.47), (3.90, 0.56)]
    s = 0.30
    for t0, sv in steps:
        if t >= t0:
            s = lerp(s, sv, ease_back(prog(t, t0, 0.18)))
    aura(img, 540, 1640, s, t, '#8aff3a')
    place(img, 'broly_legendario', 540, 1640, s)
    off = shake_off(t, 3.90, 26)
    if t >= 3.0 and off == (0.0, 0.0): off = shake_off(t, 3.48, 14)
    return img, 1.0, off


def sc_clash(t):
    img = Image.new('RGBA', (W, H))
    left = bg_burst('#ff2a3a', '#2a0508', 270, 900).crop((0, 0, W // 2, H))
    right = bg_burst('#6aff2a', '#0a2a06', 810, 900).crop((W // 2, 0, W, H))
    img.paste(left, (0, 0)); img.paste(right, (W // 2, 0))
    hit = 4.95; s = 0.40
    tip = 540
    p = prog(t, 4.70, hit - 4.70)
    jx = lerp(-250, jx_from_tip(tip, s), ease_in_out(p)); bx = lerp(W + 250, bx_from_tip(tip, s), ease_in_out(p))
    if t >= hit:
        k = ease_out(prog(t, hit, 0.25)); jx -= 40 * k; bx += 40 * k
    aura(img, bx, GY, s, t, '#8aff3a', 0.7); aura(img, jx, GY, s, t, '#ff3a3a', 0.7)
    place(img, 'jiren_golpe', jx, GY, s); place(img, 'broly_base_golpe', bx, GY, s)
    star(img, 540, GY - 1030 * s, t, hit, 340)
    if t < hit: hlines(img, t, '#ffffff', 120)
    lightning(img, 540, 0, 540, H, int(t * 30), '#ffffff', 6, 18, 50) if 4.95 <= t < 5.25 else None
    flash(img, 1 - prog(t, hit, 0.18) if t >= hit else 0)
    return img, 1.0, shake_off(t, hit, 34)


def sc_quien(t):
    img = bg_space(False, False, True).copy()
    s = 0.85 + 0.03 * (t - 7.1)
    place(img, 'broly_legendario', 540, 2080, s * 1.05)
    aura(img, 540, 1530, 0.16, t, '#ff3a3a')
    place(img, 'jiren', 540, 1530, 0.16)
    return img, 1.0 + 0.04 * (t - 7.1), shake_off(t, 7.18, 16)


def sc_ronda(t):
    img = bg_burst('#9a4aff', '#120626').copy()
    speedlines(img, t, '#ffffff', 110)
    return img, 1.0, shake_off(t, 8.54, 26)


def duel_base(red=False):
    return bg_arena(red).copy()


def sc_round1(t):
    img = duel_base()
    floating_hex(img, t, 1, '#2b1550', '#c79bff', 0)
    s = S_DUEL; tip = 520
    jx = jx_from_tip(tip, s)
    bstart, bend = 1010, bx_from_tip(tip, s)
    # golpes de Broly: (inicio dash, impacto)
    hits = [(10.28, 10.52), (20.24, 20.44), (21.96, 22.14)]
    bx = bstart; bpose = 'broly_base'; jpose = 'jiren'
    for i, (a, b) in enumerate(hits):
        if t >= a:
            bx = dash(t, a, b, bstart if i == 0 else bend + 120, bend); bpose = 'broly_base_golpe'; jpose = 'jiren_golpe'
        if i + 1 < len(hits) and t >= b + 0.9 and t < hits[i + 1][0]:
            bx = dash(t, b + 0.9, b + 1.2, bend, bend + 120); bpose = 'broly_base'
    # arrastre (23.16 - 24.2)
    slide = 230 * ease_in_out(prog(t, 23.10, 1.1))
    jx -= slide; bx -= slide
    if 13.0 < t < 19.8:
        bx += 4 * math.sin(t * 40)   # empuja
    green = 0.0
    if t > 18.2: green = 0.6
    if t > 20.3: green = 0.8
    if t > 21.9: green = 1.0
    if green: aura(img, bx, GY, s, t, '#5aff3a', green)
    place(img, jpose, jx, GY, s); place(img, bpose, bx, GY, s)
    hy = GY - 1030 * s
    for a, b in hits:
        star(img, tip - slide * (b > 23), hy, t, b, 220 if b < 20 else 300)
        ring(img, tip, hy, t, b, '#ffffff', 420)
        dust(img, jx, GY, t, b, 0.7, spread=240)
    if 10.28 <= t < 10.52 or 20.24 <= t < 20.44 or 21.96 <= t < 22.14:
        hlines(img, t, '#ffffff', 150)
    if 23.1 < t < 24.3:
        dust(img, jx + 60, GY, t, 23.1 + ((t - 23.1) // 0.12) * 0.12, 0.5, 6, spread=150)
        hlines(img, t, '#ffd0ff', 110, 12)
    # cámara
    z = 1.0; cx = 540; cy = 960
    if 10.52 <= t < 13.45:
        z = 1.0 + 0.15 * ease_out(prog(t, 10.52, 2.6)); cx = lerp(540, 580, prog(t, 10.52, 1)); cy = lerp(960, hy + 120, prog(t, 10.52, 1))
    off = (0, 0)
    for a, b in hits:
        o = shake_off(t, b, 22 if b < 20 else 34)
        if o != (0.0, 0.0): off = o
    return img, (z, cx, cy), off


def sc_calm(t):
    img = bg_arena(False).copy()
    img = blur(img, 6)
    head(img, 'jiren', 540, 880, 1.1 + 0.04 * (t - 13.45))
    return img, 1.0, (0, 0)


def sc_learn(t):
    img = bg_burst('#3aff5a', '#06200c').copy()
    st = 0.4 + 0.6 * prog(t, 15.9, 2.2)
    g = layer(); ImageDraw.Draw(g).ellipse([140, 300, 940, 1500], fill=rgba('#5aff3a', int(140 * st)))
    img.alpha_composite(blur(g, 90))
    head(img, 'broly_base', 540, 880, 1.15 + 0.06 * (t - 15.85))
    if t > 17.4:
        speedlines(img, t, '#ccffcc', 120)
    return img, 1.0, shake_off(t, 17.46, 10)


def sc_jiren_answer(t):
    img = bg_burst('#ff2a2a', '#300406').copy()
    s = 0.5 + 0.04 * (t - 24.62)
    aura(img, 540, 1700, s, t, '#ff3a3a', ease_out(prog(t, 24.68, 0.3)))
    place(img, 'jiren', 540, 1700, s)
    flash(img, 0.8 * (1 - prog(t, 24.68, 0.25)) if t >= 24.68 else 0, '#ff4a4a')
    return img, 1.0, shake_off(t, 24.68, 14)


def sc_punch(t):
    img = duel_base(True)
    s = S_DUEL; hit = 26.56
    bx0 = 850
    btip_body = bx0 - 150 * s * 2
    jx_end = jx_from_tip(bx0 - 120, s)
    jx = dash(t, 26.30, hit, 140, jx_end)
    jp = 'jiren_golpe' if t >= 26.30 else 'jiren'
    aura(img, jx, GY, s, t, '#ff3a3a', 0.8)
    if t < hit:
        place(img, 'broly_base', bx0, GY, s)
    else:
        k = t - hit
        place(img, 'broly_base', bx0 + 1700 * k, GY - 400 * k, s, rot=-200 * k)
    place(img, jp, jx, GY, s)
    star(img, bx0 - 120, GY - 1030 * s, t, hit, 420, '#ffffff', '#ff6a3a', 0.4)
    ring(img, bx0 - 120, GY - 1030 * s, t, hit, '#ffd0a0', 700)
    if 26.3 <= t < hit: hlines(img, t, '#ffffff', 160)
    if t >= hit: hlines(img, t, '#ffd0a0', 120)
    flash(img, 1 - prog(t, hit, 0.2) if t >= hit else 0)
    return img, 1.0 + 0.1 * ease_out(prog(t, hit, 0.3)), shake_off(t, hit, 46, 0.6)


def sc_building(t):
    img = bg_city_buildings().copy()
    d = ImageDraw.Draw(img)
    crash = 28.60
    bxl, bw, bh = 560, 190, 760
    if t < crash:
        d.rectangle([bxl, HOR - bh, bxl + bw, HOR], fill=rgba('#240808'), outline=rgba('#111111'), width=7)
        for wy in range(HOR - bh + 40, 1360, 60):
            for wx in (bxl + 30, bxl + 110):
                d.rectangle([wx, wy, wx + 40, wy + 30], fill=rgba('#ffb36b', 150))
    else:
        k = t - crash
        top = layer(); td = ImageDraw.Draw(top)
        td.rectangle([bxl, HOR - bh, bxl + bw, HOR - bh * 0.55], fill=rgba('#240808'), outline=rgba('#111111'), width=7)
        top = top.rotate(-40 * k, center=(bxl + bw / 2, HOR - bh * 0.55), resample=Image.BILINEAR)
        img.alpha_composite(top, (int(260 * k), int(-60 * k + 500 * k * k)))
        d.polygon([(bxl, HOR), (bxl, HOR - bh * 0.45), (bxl + 50, HOR - bh * 0.5), (bxl + 90, HOR - bh * 0.38),
                   (bxl + 140, HOR - bh * 0.48), (bxl + bw, HOR - bh * 0.4), (bxl + bw, HOR)], fill=rgba('#240808'), outline=rgba('#111111'))
        debris(img, bxl + bw / 2, HOR - bh * 0.5, t, crash, 1.2, 20, '#3a0c0c', '#ff8a5a', 900, 1500)
    # Broly volando de izq a der
    bx = lerp(-200, 1400, prog(t, 27.72, 1.6)); by = lerp(860, 720, prog(t, 27.72, 1.6))
    place(img, 'broly_base', bx, by + 500, 0.3, rot=-90 - 500 * (t - 27.72))
    hlines(img, t, '#ffd0a0', 130)
    star(img, bxl + bw / 2, HOR - bh * 0.5, t, crash, 380, '#ffffff', '#ff8a3a')
    return img, 1.0, shake_off(t, crash, 40, 0.6)


ROCKS = [(random.Random(i).uniform(300, 780), random.Random(i + 50).uniform(1150, 1300), random.Random(i + 90).uniform(45, 95)) for i in range(26)]


def rock_pile(img, t, t_drop=29.74, glow=0.0):
    d = ImageDraw.Draw(img)
    for i, (x, y, r) in enumerate(sorted(ROCKS, key=lambda v: v[1])):
        td = t_drop + i * 0.018
        if t < td:
            continue
        p = ease_out(prog(t, td, 0.28)); yy = lerp(-200, y, p)
        hexagon(d, x, yy, r, i, rgba('#4a1212'), rgba('#111111'), 6)
        hexagon(d, x - r * 0.15, yy - r * 0.15, r * 0.45, i, rgba('#6a1c1c'), rgba('#6a1c1c'), 1)
    if glow > 0:
        g = layer(); ImageDraw.Draw(g).ellipse([300, 1010, 780, 1410], fill=rgba('#ffd23a', int(220 * glow)))
        img.alpha_composite(blur(g, 50))


def sc_buried(t):
    img = bg_arena(True).copy()
    dark = 0.0 if t < 31.78 else 0.35
    rock_pile(img, t)
    dust(img, 540, 1290, t, 29.9, 1.2, 20, '#c8a090', 420)
    if dark: flash(img, dark, '#000000')
    z = 1.0 + 0.05 * prog(t, 31.78, 1.2)
    return img, z, shake_off(t, 29.96, 30)


def sc_explode(t):
    img = bg_arena(True).copy()
    ex = 33.52
    if t < ex:
        rock_pile(img, 40, glow=prog(t, 32.94, ex - 32.94))
        d = ImageDraw.Draw(img); rnd = random.Random(int(t * 30))
        for _ in range(int(10 * prog(t, 32.94, 0.6))):
            x = rnd.uniform(360, 720); d.line([(x, 1330), (x + rnd.uniform(-60, 60), rnd.uniform(650, 1050))], fill=rgba('#ffe27a', 200), width=6)
        return img, 1.0, (math.sin(t * 90) * 6 * prog(t, 32.94, 0.6), 0)
    aura(img, 540, GY, 0.42, t, '#ffd23a', ease_out(prog(t, ex, 0.4)))
    place(img, 'broly_ssj', 540, GY, 0.42)
    debris(img, 540, 1260, t, ex, 1.0, 26, '#4a1212', '#ffb04a', 1500, 1200, (30, 70))
    star(img, 540, 1150, t, ex, 600, '#ffffff', '#ffd23a', 0.45)
    flash(img, 1 - prog(t, ex, 0.3), '#fff2b0')
    return img, 1.0, shake_off(t, ex, 44, 0.6)


def sc_ssj(t):
    img = bg_burst('#ffc61a', '#2a1a02').copy()
    z = 1.0 + 0.9 * ease_in_out(prog(t, 35.0, 0.8))
    aura(img, 540, 1640, 0.5, t, '#ffd23a')
    place(img, 'broly_ssj', 540, 1640, 0.5)
    speedlines(img, t, '#fff6c0', 110)
    return img, (z, 540, 1640 - 1330 * 0.5), shake_off(t, 36.66, 18)


def sc_glare(t):
    img = bg_burst('#d01a2a', '#200204').copy()
    head(img, 'jiren', 540, 860, 1.25 + 0.05 * (t - 38.0))
    for k in range(4):
        ring(img, 540, 830, t, 40.10 + k * 0.22, '#ff2a3a', 900, 0.7, 16, 0.75)
    return img, 1.0, shake_off(t, 40.10, 12)


def sc_hit_ssj(t):
    img = bg_space(True, True).copy()
    s = S_DUEL; hit = 41.96
    jx = 200
    tip = jx + 150 * s * 2 + 40
    bx = dash(t, 41.70, hit, 1050, bx_from_tip(tip, s))
    aura(img, bx, GY, s, t, '#ffd23a', 0.9)
    if t < hit:
        place(img, 'jiren', jx, GY, s)
    else:
        k = t - hit
        place(img, 'jiren', jx - 120 * k, GY - 30 * k, s, rot=12 * k)
    place(img, 'broly_ssj_golpe' if t >= 41.70 else 'broly_ssj', bx, GY, s)
    star(img, tip, GY - 1030 * s, t, hit, 360, '#ffffff', '#ffd23a', 0.4)
    ring(img, tip, GY - 1030 * s, t, hit, '#ffffff', 600)
    if 41.70 <= t < hit: hlines(img, t)
    flash(img, 0.9 * (1 - prog(t, hit, 0.2)) if t >= hit else 0)
    return img, 1.0 + 0.15 * ease_out(prog(t, hit, 0.5)), shake_off(t, hit, 40)


def sc_slowmo(t):
    img = bg_space(True, True).copy()
    k = t - 43.02
    gray = Image.new('RGBA', (W, H), (40, 30, 60, 110)); img.alpha_composite(gray)
    hlines(img, t * 0.3, '#ffffff', 90, 14)
    place(img, 'jiren', 380 - 30 * k, 1500 - 20 * k, 0.5, rot=10 + 6 * k)
    ring(img, 540, 900, t, 43.26, '#ffffff', 900, 0.9, 10)
    return img, 1.1 + 0.03 * k, (0, 0)


def sc_fly(t):
    img = bg_space(False, True, True).copy()
    p = prog(t, 45.04, 2.9)
    x = lerp(560, 640, p); y = lerp(1500, 200, ease_in_out(p)); s = lerp(0.42, 0.12, p)
    # estela de fuego
    tr = layer(); td = ImageDraw.Draw(tr)
    for i in range(8):
        f = i / 8
        tx = lerp(560, x, f); ty = lerp(1900, y + 200 * s, f); r = 90 * (1 - f * 0.5) * (s / 0.42 + 0.4)
        td.ellipse([tx - r, ty - r * 1.6, tx + r, ty + r * 1.6], fill=rgba('#ff9a2a', 120))
        td.ellipse([tx - r * 0.5, ty - r, tx + r * 0.5, ty + r], fill=rgba('#ffe27a', 160))
    if t >= 45.04: img.alpha_composite(blur(tr, 18))
    place(img, 'jiren', x, y + 900 * s, s, rot=160 + 240 * (t - 45.0))
    speedlines(img, t, '#ffffff', 90)
    return img, 1.0, shake_off(t, 45.22, 22)


def sc_angry(t):
    img = bg_burst('#ff1a2a', '#2a0204').copy()
    head(img, 'jiren', 540, 880, 1.2 + 0.08 * (t - 48.05))
    rumble = 6 * prog(t, 48.1, 1.5)
    return img, 1.0, (math.sin(t * 70) * rumble, math.cos(t * 63) * rumble)


def sc_rip(t):
    img = bg_burst('#ff1a2a', '#2a0204').copy()
    rip = 51.30; s = 0.52
    aura(img, 540, 1720, s, t, '#ff3a3a', 0.7 + 0.3 * (t >= rip))
    place(img, 'jiren_rojo' if t >= rip else 'jiren', 540, 1720, s)
    if t >= rip:
        k = t - rip; d = ImageDraw.Draw(img); rnd = random.Random(5)
        for _ in range(16):
            ang = rnd.uniform(0, 2 * math.pi); v = rnd.uniform(400, 1000)
            px = 540 + math.cos(ang) * v * k; py = 1100 + math.sin(ang) * v * k + 600 * k * k
            sz = rnd.uniform(20, 50); rot = k * 8 + ang
            pts = [(px + sz * math.cos(rot + a), py + sz * 0.6 * math.sin(rot + a)) for a in (0, 2.2, 3.6, 5.0)]
            d.polygon(pts, fill=rgba(rnd.choice(['#1b1b20', '#d9263a'])), outline=rgba('#111111'))
    flash(img, 1 - prog(t, rip, 0.25) if t >= rip else 0)
    off = shake_off(t, rip, 36) if t >= rip else (math.sin(t * 70) * 7, 0)
    return img, 1.0, off


def sc_red(t):
    img = bg_burst('#ff2a3a', '#2a0204').copy()
    s = 0.52 + 0.03 * (t - 52.05)
    aura(img, 540, 1720, s, t, '#ff3a3a', 1.0)
    place(img, 'jiren_rojo', 540, 1720, s)
    speedlines(img, t, '#ffc0c0', 100)
    return img, 1.0, shake_off(t, 53.32, 24)


def sc_dot(t):
    img = bg_space(True).copy()
    p = prog(t, 54.6, 2.5)
    r = 8 + 60 * p ** 2
    orb(img, 540, 820, r, '#6aff3a')
    return img, 1.0 + 0.1 * p, (0, 0)


def sc_smile(t):
    img = bg_burst('#6aff2a', '#0a2a06').copy()
    head(img, 'broly_legendario', 540, 900, 1.25 + 0.1 * (t - 57.2))
    return img, 1.0, shake_off(t, 57.22, 10)


def sc_eyes(t):
    img = bg_burst('#6aff2a', '#0a2a06').copy()
    sc = 2.4 + 0.2 * (t - 58.18)
    head(img, 'broly_legendario', 540, 1000 - 0 * sc, sc)
    flash(img, 0.85 * (1 - prog(t, 58.68, 0.3)) if t >= 58.68 else 0)
    return img, 1.0, shake_off(t, 58.68, 16)


def sc_legend(t):
    img = bg_burst('#7aff2a', '#062006').copy()
    s = 0.56
    aura(img, 540, 1700, s, t, '#8aff3a')
    place(img, 'broly_legendario', 540, 1700, s)
    speedlines(img, t, '#e0ffd0', 130)
    flash(img, 0.7 * (1 - prog(t, 59.64, 0.3)) if t >= 59.64 else 0, '#d0ffb0')
    return img, 1.0, shake_off(t, 60.16, 30)


def sc_double(t):
    img = bg_space(True).copy()
    sb = 0.34
    for t0, v in ((61.32, 0.45), (62.64, 0.54)):
        if t >= t0: sb = lerp(sb, v, ease_back(prog(t, t0, 0.22)))
    aura(img, 300, GY, 0.30, t, '#ff3a3a', 0.6)
    place(img, 'jiren_rojo', 250, GY, 0.30)
    aura(img, 790, GY + 40, sb, t, '#8aff3a', 0.9)
    place(img, 'broly_legendario', 790, GY + 40, sb)
    off = shake_off(t, 62.64, 30)
    if off == (0.0, 0.0): off = shake_off(t, 61.32, 22)
    return img, 1.0, off


CLASH = [64.40, 65.50, 66.36]


def sc_fist(t):
    img = bg_space(True).copy()
    s = 0.38; tip = 540
    # grietas en la galaxia
    d = ImageDraw.Draw(img)
    for k, tc in enumerate(CLASH[1:]):
        if t >= tc:
            rnd = random.Random(k)
            for _ in range(6):
                ang = rnd.uniform(0, 2 * math.pi); x, y = 540, 820; pts = [(x, y)]
                for j in range(6):
                    ang += rnd.uniform(-0.5, 0.5); x += math.cos(ang) * 90; y += math.sin(ang) * 90; pts.append((x, y))
                d.line(pts, fill=rgba('#ffffff', 230), width=6); d.line(pts, fill=rgba('#c0a0ff', 120), width=16)
    # vaivén: retroceden y chocan en cada golpe
    back = 0.0
    for tc in CLASH:
        if t >= tc - 0.25:
            back = 160 * (1 - ease_in_out(prog(t, tc - 0.25, 0.25))) if t < tc else 90 * ease_out(prog(t, tc, 0.15)) * (1 - prog(t, tc + 0.15, 0.5))
    jx = jx_from_tip(tip, s) - back - (220 if t < 64.15 else 0) * (1 - ease_out(prog(t, 63.96, 0.2)))
    bx = bx_from_tip(tip, s) + back + (220 if t < 64.15 else 0) * (1 - ease_out(prog(t, 63.96, 0.2)))
    aura(img, jx, GY, s, t, '#ff3a3a', 0.8); aura(img, bx, GY, s, t, '#8aff3a', 0.8)
    place(img, 'jiren_rojo_golpe', jx, GY, s); place(img, 'broly_legendario_golpe', bx, GY, s)
    hy = GY - 1030 * s
    for tc in CLASH:
        star(img, tip, hy, t, tc, 320, '#ffffff', '#c8a0ff')
        if tc <= t < tc + 0.35:
            for k in range(3): lightning(img, tip, hy, tip + random.Random(k + int(tc * 9)).uniform(-500, 500), random.Random(k + 3).uniform(200, 1700), int(t * 30) + k)
    off = (0, 0)
    for tc in CLASH:
        o = shake_off(t, tc, 34)
        if o != (0.0, 0.0): off = o
    return img, 1.0, off


def sc_exchange(t):
    img = bg_space(True).copy()
    s = 0.38
    jhit = 67.60; bhits = [70.12, 71.36, 71.84]
    jx = 230; bx = 850
    jp, bp = 'jiren_rojo', 'broly_legendario'
    if t < 68.6:
        jx = dash(t, 67.42, jhit, 230, jx_from_tip(bx - 130, s)); jp = 'jiren_rojo_golpe'
        hx = bx - 130
    else:
        jx = 230
    knock = 0.0
    for i, h in enumerate(bhits):
        if t >= h: knock += (90 + 70 * i) * ease_out(prog(t, h, 0.25))
    if t >= 69.88:
        bp = 'broly_legendario_golpe'
        tipb = jx + 150 * s * 2 + 30
        bx = bx_from_tip(tipb, s) + 120 * (1 - ease_out(prog(t, 69.9, 0.22)))
        jx -= knock; bx -= knock * 0.7
    aura(img, jx, GY, s, t, '#ff3a3a', 0.7); aura(img, bx, GY, s, t, '#8aff3a', 1.0)
    place(img, jp, jx, GY, s, rot=-6 * (knock > 0))
    place(img, bp, bx, GY, s)
    hy = GY - 1030 * s
    star(img, 850 - 130, hy, t, jhit, 240, '#ffffff', '#ff6a6a')
    for i, h in enumerate(bhits):
        star(img, jx + 150 * s * 2 + 30 + knock if t < h + 0.1 else jx + 120, hy, t, h, 260 + 90 * i, '#ffffff', '#9aff6a')
        ring(img, 540, hy, t, h, '#c0ffb0', 500 + 200 * i)
    off = shake_off(t, jhit, 14)
    for i, h in enumerate(bhits):
        o = shake_off(t, h, 24 + 14 * i)
        if o != (0.0, 0.0): off = o
    return img, 1.0, off


def sc_nocae(t):
    img = bg_burst('#6aff2a', '#0a2a06').copy()
    head(img, 'broly_legendario', 540, 900, 1.3)
    ring(img, 540, 900, t, 68.62, '#ffffff', 700)
    return img, 1.0, shake_off(t, 68.62, 14)


SHARDS = [(random.Random(i).uniform(0, W), random.Random(i + 7).uniform(0, H), random.Random(i + 13).uniform(60, 180)) for i in range(18)]


def sc_shatter(t):
    img = bg_space(True).copy()
    p = prog(t, 72.94, 1.5)
    d = ImageDraw.Draw(img)
    rnd = random.Random(2)
    for k in range(14):
        ang = k * 2 * math.pi / 14 + rnd.uniform(-0.2, 0.2); x, y = 540, 820; pts = [(x, y)]
        n = int(1 + 9 * p)
        for j in range(n):
            ang += rnd.uniform(-0.4, 0.4); x += math.cos(ang) * 120; y += math.sin(ang) * 120; pts.append((x, y))
        d.line(pts, fill=rgba('#ffe0a0', 110), width=18); d.line(pts, fill=rgba('#ffffff'), width=6)
    for t0 in (73.88, 74.32):
        if t >= t0:
            k = t - t0
            for i, (x, y, r) in enumerate(SHARDS[int(t0 * 10) % 5::2]):
                dx, dy = (x - 540) * 0.6 * k, (y - 820) * 0.6 * k + 300 * k * k
                pts = [(x + dx + r * math.cos(a + k * 2 + i), y + dy + r * math.sin(a + k * 2 + i)) for a in (0, 2.1, 4.2)]
                d.polygon(pts, fill=rgba('#2a1650'), outline=rgba('#ffe0a0'))
    g = layer(); ImageDraw.Draw(g).ellipse([340, 620, 740, 1020], fill=rgba('#fff0c0', int(200 * p)))
    img.alpha_composite(blur(g, 60))
    s = 0.3
    aura(img, 330, GY, s, t, '#ff3a3a', 0.7); aura(img, 750, GY, s, t, '#8aff3a', 0.9)
    place(img, 'jiren_rojo', 330, GY, s); place(img, 'broly_legendario', 750, GY, s)
    off = shake_off(t, 73.88, 28)
    if off == (0.0, 0.0): off = shake_off(t, 74.32, 28)
    if off == (0.0, 0.0): off = (math.sin(t * 60) * 5, 0)
    return img, 1.0, off


def sc_charge(t):
    img = bg_space(True).copy()
    s = 0.38
    jx, bx = 140, 940
    aura(img, jx, GY, s, t, '#ff3a3a', 1.0); aura(img, bx, GY, s, t, '#8aff3a', 1.0)
    place(img, 'jiren_rojo_golpe', jx, GY, s); place(img, 'broly_legendario_golpe', bx, GY, s)
    hy = GY - 1030 * s
    jt, bt = jx + REACH * s, bx - REACH * s
    p = prog(t, 75.28, 1.2)
    beam_r = 0
    if t < 76.54:
        orb(img, jt + 20, hy, 20 + 50 * p, '#ff3a3a'); orb(img, bt - 20, hy, 20 + 50 * p, '#6aff3a')
    else:
        # rayos
        mid = 540
        rl = mid if t >= 77.04 else lerp(jt, mid + 120, ease_out(prog(t, 76.54, 0.3)))
        gl = mid if t >= 77.04 else bt
        if t >= 77.04 - 0.25: gl = lerp(bt, mid, ease_out(prog(t, 76.80, 0.24)))
        L = layer(); dl = ImageDraw.Draw(L)
        dl.rectangle([jt, hy - 55, rl, hy + 55], fill=rgba('#ff3a3a')); dl.rectangle([jt, hy - 22, rl, hy + 22], fill=rgba('#ffffff'))
        dl.rectangle([gl, hy - 55, bt, hy + 55], fill=rgba('#6aff3a')); dl.rectangle([gl, hy - 22, bt, hy + 22], fill=rgba('#ffffff'))
        img.alpha_composite(blur(L, 3))
        orb(img, jt + 10, hy, 60, '#ff3a3a'); orb(img, bt - 10, hy, 60, '#6aff3a')
        if t >= 77.04:
            orb(img, mid, hy, 70 + 30 * prog(t, 77.04, 1.3) + 10 * math.sin(t * 40), '#f0e0ff')
            for k in range(4): lightning(img, mid, hy, mid + random.Random(int(t * 30) + k).uniform(-520, 520), random.Random(int(t * 30) + k + 9).uniform(200, 1800), int(t * 30) + k)
    off = (math.sin(t * 80) * 4 * p, 0)
    o = shake_off(t, 77.04, 30)
    if o != (0.0, 0.0): off = o
    return img, 1.0, off


def sc_white(t):
    img = bg_space(True).copy()
    hy = GY - 1030 * 0.38
    r = lerp(100, 2400, ease_in_out(prog(t, 78.44, 0.5)))
    g = layer(); ImageDraw.Draw(g).ellipse([540 - r, hy - r, 540 + r, hy + r], fill=rgba('#ffffff'))
    img.alpha_composite(blur(g, 40))
    if t >= 78.9:
        flash(img, 1.0)
        # se desvanece a humo gris
        sm = bg_smoke()
        a = prog(t, 80.2, 0.8)
        if a > 0:
            img = Image.blend(img, sm, a)
    return img, 1.0, shake_off(t, 78.88, 40, 0.8)


def sc_smoke(t):
    img = bg_smoke().copy()
    s = 0.46
    k = t - 81.0
    # humo que deriva
    L = layer(); d = ImageDraw.Draw(L); rnd = random.Random(3)
    for _ in range(14):
        x0, y0, r = rnd.uniform(-200, W + 200), rnd.uniform(700, 1700), rnd.uniform(150, 300)
        x = x0 + 25 * k * (1 if x0 < 540 else -1)
        d.ellipse([x - r, y0 - r * 0.5, x + r, y0 + r * 0.5], fill=rgba('#8a7a88', 70))
    reveal = prog(t, 83.6, 0.6)
    stepf = ease_out(prog(t, 84.80, 0.25))
    y = 1400 + 30 * stepf; sc = s + 0.03 * stepf
    fall = 85.86
    rot = 0.0; drop = 0.0
    if t >= fall:
        fp = ease_in_out(prog(t, fall, 0.5)) if False else clamp((t - fall) / 0.45) ** 2
        rot = -88 * fp; drop = 150 * fp
    if reveal < 1:
        place(img, 'jiren_rojo', 540, y + drop, sc, rot=rot, mode='sil')
    if reveal > 0:
        place(img, 'jiren_rojo', 540, y + drop, sc, rot=rot, alpha=reveal)
    img.alpha_composite(blur(L, 30))
    if t >= fall + 0.4:
        dust(img, 540, 1400, t, fall + 0.4, 1.0, 22, '#9a8a98', 600)
    ember = ImageDraw.Draw(img); rnd = random.Random(8)
    for _ in range(18):
        x = rnd.uniform(0, W); y0 = rnd.uniform(0, H); yy = (y0 - 60 * k) % H
        ember.ellipse([x - 4, yy - 4, x + 4, yy + 4], fill=rgba('#ffb04a', 200))
    return img, 1.0 + 0.02 * k, shake_off(t, fall + 0.4, 26)


def sc_win(t):
    img = bg_burst('#6aff2a', '#062006').copy()
    s = 0.6
    aura(img, 540, 1820, s, t, '#8aff3a')
    place(img, 'broly_legendario', 540, 1820, s)
    speedlines(img, t, '#e0ffd0', 110)
    return img, 1.0, shake_off(t, 87.26, 24)


def sc_end(t):
    img = bg_smoke().copy()
    g = layer(); ImageDraw.Draw(g).ellipse([140, 400, 940, 1400], fill=rgba('#ff2a3a', 90))
    img.alpha_composite(blur(g, 120))
    head(img, 'jiren_rojo', 540, 880, 1.2 + 0.05 * (t - 88.12))
    return img, 1.0, shake_off(t, 91.48, 26)


SCENES = [
    (0.00, 2.72, sc_hook), (2.72, 4.70, sc_grow), (4.70, 7.10, sc_clash), (7.10, 8.50, sc_quien), (8.50, 9.45, sc_ronda),
    (9.45, 13.45, sc_round1), (13.45, 15.85, sc_calm), (15.85, 18.20, sc_learn), (18.20, 24.62, sc_round1),
    (24.62, 26.10, sc_jiren_answer), (26.10, 27.70, sc_punch), (27.70, 29.70, sc_building), (29.70, 32.92, sc_buried),
    (32.92, 34.58, sc_explode), (34.58, 38.00, sc_ssj), (38.00, 41.00, sc_glare), (41.00, 43.02, sc_hit_ssj),
    (43.02, 45.00, sc_slowmo), (45.00, 48.05, sc_fly), (48.05, 50.60, sc_angry), (50.60, 52.05, sc_rip),
    (52.05, 54.50, sc_red), (54.50, 57.20, sc_dot), (57.20, 58.18, sc_smile), (58.18, 59.60, sc_eyes),
    (59.60, 61.22, sc_legend), (61.22, 63.92, sc_double), (63.92, 67.42, sc_fist), (67.42, 68.60, sc_exchange),
    (68.60, 69.88, sc_nocae), (69.88, 72.80, sc_exchange), (72.80, 75.25, sc_shatter), (75.25, 78.42, sc_charge),
    (78.42, 81.00, sc_white), (81.00, 86.95, sc_smoke), (86.95, 88.12, sc_win), (88.12, 99.0, sc_end),
]
CUTS = [a for a, b, f in SCENES[1:]]

# ============================================================ textos grandes (rótulos)
BIG = [  # (t, texto, color, y, dur)
    (2.00, 'NI UN PASO', RED, 470, 0.75), (3.90, 'CRECER', GREEN, 470, 0.8),
    (5.90, 'SOLO UNO', WHITE, 470, 1.2), (7.18, '¿QUIÉN CAE?', WHITE, 560, 1.32),
    (8.54, 'RONDA 1', GOLD, 880, 0.9), (12.48, 'UNA SOLA MANO', WHITE, 470, 1.0),
    (18.24, 'APRENDE', GREEN, 470, 1.5), (20.44, 'X2', GREEN, 470, 1.3), (22.14, 'X3', GREEN, 470, 1.4),
    (26.56, '¡PUM!', GOLD, 470, 1.1), (29.96, 'ENTERRADO', WHITE, 470, 1.8),
    (36.66, 'SÚPER SAIYAJIN', GOLD, 470, 1.3), (41.96, '¡SÍ LLEGA!', GOLD, 470, 1.0),
    (43.26, 'POR PRIMERA VEZ', WHITE, 470, 1.6), (46.58, 'FUERA DEL PLANETA', CYAN, 470, 1.4),
    (53.32, 'SIN FRENOS', RED, 470, 1.15), (60.16, 'LEGENDARIO', GREEN, 470, 1.05),
    (61.32, 'X2 TAMAÑO', GREEN, 470, 1.2), (62.64, 'X2 FUERZA', GREEN, 470, 1.25),
    (64.40, '¡CRACK!', CYAN, 470, 1.0), (68.90, 'NO CAE', GREEN, 470, 0.95), (71.60, 'MÁS FUERTE', GREEN, 470, 1.15),
    (72.94, 'FIN DEL UNIVERSO', '#ff9a3a', 470, 2.2), (86.98, 'GANA', WHITE, 470, 1.14), (87.26, 'BROLY', GREEN, 1460, 0.86),
    (91.48, 'HASTA HOY', RED, 470, 1.0),
]
NO_CAPTION = [(7.10, 8.50), (8.50, 9.45), (86.95, 88.12)]


@lru_cache(maxsize=None)
def big_sprite(txt, col, size):
    f = F(ANTON, size)
    bb = f.getbbox(txt, stroke_width=14)
    w, h = bb[2] - bb[0] + 40, bb[3] - bb[1] + 40
    while w > 1000:
        size = int(size * 0.9); f = F(ANTON, size); bb = f.getbbox(txt, stroke_width=14); w, h = bb[2] - bb[0] + 40, bb[3] - bb[1] + 40
    im = layer(w, h + 14); d = ImageDraw.Draw(im)
    d.text((20 - bb[0], 34 - bb[1]), txt, font=f, fill=(0, 0, 0, 160), stroke_width=14, stroke_fill=(0, 0, 0, 160))
    d.text((20 - bb[0], 20 - bb[1]), txt, font=f, fill=rgba(col), stroke_width=14, stroke_fill=rgba('#0d0d12'))
    return im.rotate(4, resample=Image.BICUBIC, expand=True)


def draw_big(img, t):
    for t0, txt, col, y, dur in BIG:
        if t0 <= t < t0 + dur:
            p = t - t0
            sc = ease_back(prog(p, 0, 0.2), 2.4) * (1 + 0.04 * p)
            a = 1 - prog(p, dur - 0.15, 0.15)
            spr = big_sprite(txt, col, 190 if len(txt) <= 10 else 150)
            if sc <= 0.02: continue
            sp = spr.resize((max(1, int(spr.width * sc)), max(1, int(spr.height * sc))), Image.BILINEAR)
            jit = 5 * math.sin(p * 60) * (1 - prog(p, 0, 0.3))
            paste(img, sp, 540 - sp.width / 2 + jit, y - sp.height / 2, a)


# ============================================================ subtítulos
KEYC = {'JIREN': RED, 'BROLY': GREEN, 'ROJO': RED, 'ENOJA': RED, 'DESPLOMA': RED, 'VOLANDO': RED, 'ROMPE': RED,
        'VERDE': GREEN, 'LEGENDARIO': GREEN, 'APRENDE': GREEN, 'CRECER': GREEN, 'SONREÍR': GREEN,
        'DORADO': GOLD, 'SÚPER': GOLD, 'SAIYAJIN': GOLD, 'PUÑETAZO': GOLD, 'GALAXIA': CYAN, 'UNIVERSO': CYAN,
        'PLANETA': CYAN, 'BLANCO': WHITE, 'ENTERRADO': GOLD, 'EXPLOTAN': GOLD, 'PEDAZOS': '#ff9a3a', 'HOY': RED}
FIX = {'pelo,@24.00': 'suelo,', '1,@8.86': 'uno,'}


def load_words():
    d = json.load(open(os.path.join(HERE, 'work', 'words.json')))
    out = []
    for s in d:
        for w in s['words']:
            txt = w['w'].strip()
            txt = FIX.get(f"{txt}@{w['s']:.2f}", txt)
            out.append((txt, w['s'], w['e']))
    return out


def make_chunks():
    ws = load_words(); chunks = []; cur = []
    for i, (txt, s, e) in enumerate(ws):
        cur.append((txt, s, e))
        clean = ' '.join(c[0] for c in cur)
        brk = txt[-1] in ',.?!' or len(cur) >= 3 or len(clean) >= 15
        nxt = ws[i + 1] if i + 1 < len(ws) else None
        if nxt and len(clean) + len(nxt[0]) > 17: brk = True
        if nxt and nxt[1] - e > 0.35: brk = True
        if brk or not nxt:
            chunks.append(cur); cur = []
    res = []
    for k, c in enumerate(chunks):
        t0 = c[0][1]; t1 = chunks[k + 1][0][1] if k + 1 < len(chunks) else c[-1][2] + 0.6
        t1 = min(t1, c[-1][2] + 0.7)
        res.append((t0, t1, [(w.strip(',.').upper(), s) for w, s, e in c]))
    return res


CHUNKS = make_chunks()
CAP_Y = 1440


@lru_cache(maxsize=256)
def word_img(w, col):
    f = F(BEBAS, 128)
    bb = f.getbbox(w, stroke_width=10)
    im = layer(bb[2] - bb[0] + 24, bb[3] - bb[1] + 30); d = ImageDraw.Draw(im)
    d.text((12 - bb[0], 20 - bb[1]), w, font=f, fill=(0, 0, 0, 150), stroke_width=10, stroke_fill=(0, 0, 0, 150))
    d.text((12 - bb[0], 12 - bb[1]), w, font=f, fill=rgba(col), stroke_width=10, stroke_fill=rgba('#0b0b10'))
    return im


def draw_caption(img, t):
    for a, b in NO_CAPTION:
        if a <= t < b:
            return
    for t0, t1, words in CHUNKS:
        if t0 <= t < t1:
            shown = [(w, s) for w, s in words if s <= t + 0.02]
            ims = []
            for w, s in shown:
                key = w.strip('¿?¡!')
                ims.append((word_img(w, KEYC.get(key, WHITE)), s))
            gap = 18
            tw = sum(i.width for i, _ in ims) + gap * (len(ims) - 1)
            x = 540 - tw / 2
            for im, s in ims:
                sc = 0.75 + 0.25 * ease_back(prog(t, s, 0.12), 2.2)
                if sc != 1.0:
                    sim = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)
                else:
                    sim = im
                paste(img, sim, x + (im.width - sim.width) / 2, CAP_Y - sim.height / 2)
                x += im.width + gap
            return


@lru_cache(maxsize=None)
def header_img():
    im = layer(W, 120); d = ImageDraw.Draw(im); f = F(BEBAS, 72); fv = F(BEBAS, 46)
    for txt, col, x, ff in (('JIREN', RED, 70, f), ('VS', WHITE, 540, fv), ('BROLY', GREEN, W - 70, f)):
        bb = ff.getbbox(txt, stroke_width=6)
        xx = x if txt == 'JIREN' else (x - (bb[2] - bb[0]) if txt == 'BROLY' else x - (bb[2] - bb[0]) / 2)
        d.text((xx, 60 - (bb[3] - bb[1]) / 2 - bb[1]), txt, font=ff, fill=rgba(col), stroke_width=6, stroke_fill=rgba('#0b0b10'))
    return im


# ============================================================ composición
def camera(img, z, cx, cy, off):
    if isinstance(z, tuple):
        z, cx, cy = z
    dx, dy = off
    if z <= 1.0001 and abs(dx) < 0.5 and abs(dy) < 0.5:
        return img
    z = max(z, 1.0 + (abs(dx) + abs(dy)) / 500)   # margen para la sacudida
    w2, h2 = W / z / 2, H / z / 2
    cx = clamp(cx + dx / z, w2, W - w2); cy = clamp(cy + dy / z, h2, H - h2)
    return img.transform((W, H), Image.EXTENT, (cx - w2, cy - h2, cx + w2, cy + h2), Image.BILINEAR)


def frame(t):
    for a, b, fn in SCENES:
        if a <= t < b:
            break
    img, z, off = fn(t)
    # golpe de zoom en cada corte
    punch = 1 + 0.07 * (1 - ease_out(prog(t, a, 0.22))) if a > 0 else 1
    if isinstance(z, tuple):
        z = (z[0] * punch, z[1], z[2])
    else:
        z = (z * punch, 540, 960)
    img = camera(img.convert('RGBA'), z, 540, 960, off)
    draw_big(img, t)
    draw_caption(img, t)
    if not (78.9 <= t < 80.3):
        img.alpha_composite(header_img(), (0, 150))
    return np.asarray(img.convert('RGB'))


def worker(k, f0, f1, out):
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(f0, f1):
        p.stdin.write(frame(fi / FPS).tobytes())
        if (fi - f0) % 150 == 0:
            print(f'[w{k}] {fi - f0}/{f1 - f0}', flush=True)
    p.stdin.close(); p.wait()


if __name__ == '__main__':
    outdir = sys.argv[1]; os.makedirs(outdir, exist_ok=True)
    if len(sys.argv) > 2 and sys.argv[2] == 'stills':
        for tt in sys.argv[3:]:
            Image.fromarray(frame(float(tt))).save(os.path.join(outdir, f'still_{float(tt):06.2f}.png'))
        sys.exit()
    nw = int(os.environ.get('NW', '4'))
    bounds = [round(NFR * i / nw) for i in range(nw + 1)]
    ps = [Process(target=worker, args=(k, bounds[k], bounds[k + 1], os.path.join(outdir, f'part{k}.mp4'))) for k in range(nw)]
    for p in ps: p.start()
    for p in ps: p.join()
    with open(os.path.join(outdir, 'parts.txt'), 'w') as f:
        for k in range(nw): f.write(f"file 'part{k}.mp4'\n")
    print('done', NFR)
