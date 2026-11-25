"""Fondos y personajes reutilizables."""
import math, random
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import *

# ======================================================================
#  INTESTINO (fondo rosa estilo referencia)
# ======================================================================
TOP_B = 600     # borde interior pared superior
BOT_A = 1360    # borde interior pared inferior
SPH_X = 840     # borde izquierdo del esfínter


@lru_cache(maxsize=4)
def bg_intestine(sphincter=False, food=True):
    S = 2; w, h = W * S, H * S
    rnd = random.Random(7)
    img = vgrad((w, h), rgba('#24091c'), rgba('#160612'))
    TOP_A, TB, BA, BOT_B = 330 * S, TOP_B * S, BOT_A * S, 1630 * S
    lum = vgrad((w, BA - TB + 80 * S), rgba('#8e2148'), rgba('#5e1233'))
    img.alpha_composite(lum, (0, TB - 40 * S))
    g = layer(w, h); ImageDraw.Draw(g).ellipse([100 * S, 700 * S, 950 * S, 1250 * S], fill=rgba('#c2456f', 90))
    img.alpha_composite(blur(g, 120 * S))
    v = layer(w, h); vd = ImageDraw.Draw(v)
    for x0 in range(-20 * S, w + 60 * S, 78 * S):
        ph = rnd.random() * 6
        pts = [(x0 + wave(y, 16 * S, 260 * S, ph), y) for y in range(TB - 40 * S, BA + 40 * S, 6 * S)]
        vd.line(pts, fill=rgba('#c45a80', 150), width=7 * S, joint='curve')
        vd.line([(x + 30 * S, y) for x, y in pts], fill=rgba('#6a1638', 120), width=5 * S, joint='curve')
    img.alpha_composite(blur(v, 1.2 * S))
    if food:
        f = layer(w, h); fd = ImageDraw.Draw(f)
        edge = [(x, 1205 * S + wave(x, 14 * S, 300 * S, 1.0) + wave(x, 6 * S, 90 * S, 2)) for x in range(0, w + 8, 8)]
        fd.polygon(edge + [(w, BA + 30 * S), (0, BA + 30 * S)], fill=rgba('#e3a23a'))
        for k in range(16):
            y = rnd.randint(1230, 1340) * S; x = rnd.randint(0, 1000) * S
            fd.line([(x + j * 30 * S, y + wave(j * 30 * S, 8 * S, 120 * S, k)) for j in range(8)], fill=rgba('#f6cd6a', 200), width=4 * S, joint='curve')
        fd.line(edge, fill=rgba('#f8d77d'), width=7 * S)
        img.alpha_composite(f)

    def wall(inner_y, inner_up):
        L = layer(w, h)
        edge = [(x, inner_y + wave(x, 10 * S, 520 * S, 0.6)) for x in range(0, w + 8, 8)]
        poly = edge + [(w, h), (0, h)] if inner_up else [(0, 0), (w, 0)] + edge[::-1]
        mask = Image.new('L', (w, h), 0); ImageDraw.Draw(mask).polygon(poly, fill=255)
        base = vgrad((w, h), rgba('#b53a62'), rgba('#d6527a')) if inner_up else vgrad((w, h), rgba('#d24a73'), rgba('#a8325a'))
        st = layer(w, h); sd = ImageDraw.Draw(st)
        for x in range(0, w, 34 * S):
            sd.rectangle([x, 0, x + 12 * S, h], fill=rgba('#8f2449', 95))
            sd.rectangle([x + 18 * S, 0, x + 21 * S, h], fill=rgba('#ee7b9b', 60))
        base.alpha_composite(st)
        if inner_up:
            sh = vgrad((w, h), (20, 4, 12, 0), (20, 4, 12, 170))
        else:
            sh = vgrad((w, h), (20, 4, 12, 170), (20, 4, 12, 0))
        base.alpha_composite(sh)
        L.paste(base, (0, 0), mask)
        d = ImageDraw.Draw(L)
        d.line([(x, y + (14 * S if inner_up else -14 * S)) for x, y in edge], fill=rgba('#ff9db8', 90), width=10 * S)
        d.line(edge, fill=rgba('#ffc2d2', 235), width=6 * S)
        return L
    img.alpha_composite(wall(TB, False))
    img.alpha_composite(wall(BA, True))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, TOP_A], fill=rgba('#1c0716'))
    d.rectangle([0, BOT_B, w, h], fill=rgba('#1c0716'))
    r = layer(w, h); rd = ImageDraw.Draw(r)
    rd.line([(x, TOP_A + wave(x, 6 * S, 400 * S, 2)) for x in range(0, w + 8, 8)], fill=rgba('#7d2445'), width=10 * S)
    rd.line([(x, BOT_B + wave(x, 6 * S, 400 * S, 1)) for x in range(0, w + 8, 8)], fill=rgba('#7d2445'), width=10 * S)
    img.alpha_composite(r)
    if sphincter:
        img.alpha_composite(sphincter_layer(S, 0.0))
    return img.resize((W, H), Image.LANCZOS)


def sphincter_layer(S=1, squeeze=0.0):
    """Músculo rojo de salida (lado derecho). squeeze 0..1 lo hace brillar y avanzar."""
    w, h = W * S, H * S
    sx = (SPH_X - 40 * squeeze) * S
    TOP_A, BOT_B = 330 * S, 1630 * S
    sp = layer(w, h)
    left = [(sx + wave(y, (10 + 14 * squeeze) * S, 700 * S, 0.3), y) for y in range(TOP_A - 30 * S, BOT_B + 40 * S, 8)]
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).polygon(left + [(w + 10, BOT_B + 40 * S), (w + 10, TOP_A - 30 * S)], fill=255)
    top = (229 + int(26 * squeeze), 54, 79, 255)
    sp.paste(vgrad((w, h), top, rgba('#a9182f')), (0, 0), mask)
    ln = layer(w, h); s2 = ImageDraw.Draw(ln)
    for x in range(int(sx), w, 26 * S):
        pts = [(x + wave(y, 8 * S, 700 * S, 0.3) + (y - h / 2) * 0.03, y) for y in range(TOP_A - 30 * S, BOT_B + 40 * S, 10 * S)]
        s2.line(pts, fill=rgba('#7e0f22', 130), width=4 * S)
        s2.line([(a + 9 * S, b) for a, b in pts], fill=rgba('#ff6b7e', 70), width=2 * S)
    for y in (TOP_A + 40 * S, BOT_B - 60 * S):
        s2.line([(sx + 70 * S, y), (sx + 150 * S, y + 4 * S)], fill=rgba('#ffd0d6', 200), width=4 * S)
    s2.line(left, fill=rgba('#ff8f9e', 220), width=6 * S)
    sp.alpha_composite(ln)
    return sp


@lru_cache(maxsize=4)
def sphincter_sprite(sq_level):
    """versiones precalculadas del esfínter (0..4)"""
    return sphincter_layer(1, sq_level / 4.0)


@lru_cache(maxsize=2)
def gate_bulge():
    def fn(im, s):
        L = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.ellipse([20 * s, 40 * s, 240 * s, 300 * s], fill=rgba('#ff3a55', 200))
        im.alpha_composite(blur(L, 40 * s))
        d = ImageDraw.Draw(im)
        d.chord([70 * s, 30 * s, 250 * s, 310 * s], 90, 270, fill=rgba('#e02a44'))
        d.arc([70 * s, 30 * s, 250 * s, 310 * s], 90, 270, fill=rgba('#ffc0c9'), width=5 * s)
    return ss_sprite(260, 340, fn)


# ======================================================================
#  HOLOGRAMA AZUL
# ======================================================================
@lru_cache(maxsize=2)
def bg_holo(tint='blue'):
    if tint == 'blue':
        img = vgrad((W, H), rgba('#13305e'), rgba('#0a1a38'))
    else:
        img = vgrad((W, H), rgba('#2a1a52'), rgba('#150c2e'))
    rnd = random.Random(5)
    fog = layer()
    d = ImageDraw.Draw(fog)
    for _ in range(26):
        x, y, r = rnd.randint(-100, W + 100), rnd.randint(0, H), rnd.randint(120, 300)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(120, 170, 255, 18))
    img.alpha_composite(blur(fog, 70))
    # suelo con rejilla en perspectiva
    g = layer(); gd = ImageDraw.Draw(g)
    hz = 1420
    for i in range(-14, 15):
        gd.line([(W / 2 + i * 26, hz), (W / 2 + i * 190, H)], fill=(110, 170, 255, 55), width=2)
    y = hz; k = 1.0
    while y < H:
        gd.line([(0, y), (W, y)], fill=(110, 170, 255, int(30 + 30 * k)), width=2)
        k += 0.35; y += 16 * k
    m = vgrad((W, H), (0, 0, 0, 0), (0, 0, 0, 255)).split()[3]
    g2 = layer(); g2.paste(g, (0, 0), m)
    img.alpha_composite(g2)
    return img


HB_W, HB_H = 560, 1180
HB_MOUTH = (280, 205)
HB_BELLY = (280, 600)
HB_EXIT = (280, 720)
HB_LUNG_L, HB_LUNG_R = (215, 410), (345, 410)


@lru_cache(maxsize=2)
def holo_body():
    def shape(d, s, fill, extra=0):
        e = extra * s
        def P(x, y): return (x * s, y * s)
        d.ellipse([(195 - extra) * s, (55 - extra) * s, (365 + extra) * s, (245 + extra) * s], fill=fill)
        d.rounded_rectangle([(245 - extra) * s, 220 * s, (315 + extra) * s, 300 * s], 20 * s, fill=fill)
        d.rounded_rectangle([(130 - extra) * s, (280 - extra) * s, (430 + extra) * s, (700 + extra) * s], 70 * s, fill=fill)
        d.line([P(140, 320), P(95, 560), P(85, 760)], fill=fill, width=int((62 + 2 * extra) * s), joint='curve')
        d.line([P(420, 320), P(465, 560), P(475, 760)], fill=fill, width=int((62 + 2 * extra) * s), joint='curve')
        d.ellipse([(55 - extra) * s, (735 - extra) * s, (115 + extra) * s, (805 + extra) * s], fill=fill)
        d.ellipse([(445 - extra) * s, (735 - extra) * s, (505 + extra) * s, (805 + extra) * s], fill=fill)
        d.line([P(215, 660), P(205, 1140)], fill=fill, width=int((92 + 2 * extra) * s))
        d.line([P(345, 660), P(355, 1140)], fill=fill, width=int((92 + 2 * extra) * s))
    def fn(im, s):
        w, h = im.size
        outer = Image.new('L', (w, h), 0); shape(ImageDraw.Draw(outer), s, 255, extra=4)
        inner = Image.new('L', (w, h), 0); shape(ImageDraw.Draw(inner), s, 255, extra=-3)
        edge = ImageChops.subtract(outer, inner)
        body = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        fillc = vgrad((w, h), (40, 95, 200, 215), (25, 60, 150, 215))
        body.paste(fillc, (0, 0), outer)
        lines = layer(w, h); ld = ImageDraw.Draw(lines)
        for y in range(0, h, 9 * s):
            ld.line([(0, y), (w, y)], fill=(130, 190, 255, 40), width=2 * s)
        tmp = layer(w, h); tmp.paste(lines, (0, 0), inner)
        body.alpha_composite(tmp)
        glow = Image.new('RGBA', (w, h), (110, 200, 255, 0)); glow.putalpha(edge)
        im.alpha_composite(blur(glow, 14 * s)); im.alpha_composite(blur(glow, 5 * s))
        im.alpha_composite(body)
        e2 = Image.new('RGBA', (w, h), (190, 235, 255, 0)); e2.putalpha(edge)
        im.alpha_composite(e2)
    return ss_sprite(HB_W, HB_H, fn)


@lru_cache(maxsize=2)
def lungs_sprite():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        for cx, flip in ((70, -1), (200, 1)):
            box = [(cx - 58) * s, 10 * s, (cx + 58) * s, 250 * s]
            d.rounded_rectangle(box, 58 * s, fill=(255, 140, 170, 235), outline=(255, 220, 230, 255), width=4 * s)
            for k in range(4):
                y = (60 + k * 45) * s
                d.line([(cx * s, y), ((cx - 30 * flip) * s, y + 30 * s)], fill=(200, 60, 100, 200), width=4 * s)
        d.line([(135 * s, 0), (135 * s, 50 * s), (95 * s, 85 * s)], fill=(230, 90, 120, 255), width=8 * s)
        d.line([(135 * s, 50 * s), (175 * s, 85 * s)], fill=(230, 90, 120, 255), width=8 * s)
    return ss_sprite(270, 260, fn)


# ======================================================================
#  OTROS FONDOS
# ======================================================================
@lru_cache(maxsize=2)
def bg_purple():
    img = vgrad((W, H), rgba('#2d1650'), rgba('#170a2c'))
    g = layer(); ImageDraw.Draw(g).ellipse([140, 520, 940, 1320], fill=(150, 90, 230, 70))
    img.alpha_composite(blur(g, 160))
    fl = layer(); fd = ImageDraw.Draw(fl)
    fd.rectangle([0, 1480, W, H], fill=(40, 20, 70, 180))
    fd.line([(0, 1480), (W, 1480)], fill=(150, 100, 230, 90), width=3)
    img.alpha_composite(fl)
    return img


@lru_cache(maxsize=2)
def bg_teal():
    img = vgrad((W, H), rgba('#1c6b72'), rgba('#0d3c45'))
    g = layer(); ImageDraw.Draw(g).ellipse([0, 300, 900, 1300], fill=(120, 230, 230, 60))
    img.alpha_composite(blur(g, 170))
    return img


VEIN_PATHS = []


@lru_cache(maxsize=2)
def bg_veins():
    rnd = random.Random(11)
    img = vgrad((W, H), rgba('#c4466e'), rgba('#9c2a52'))
    g = layer(); ImageDraw.Draw(g).ellipse([100, 400, 1000, 1400], fill=(255, 150, 185, 90))
    img.alpha_composite(blur(g, 160))
    st = layer(); sd = ImageDraw.Draw(st)
    for y in range(240, H, 120):
        sd.line([(0, y + rnd.randint(-10, 10)), (W, y + rnd.randint(-10, 10))], fill=(255, 200, 215, 45), width=6)
    img.alpha_composite(blur(st, 3))
    hair = layer(); hd = ImageDraw.Draw(hair)
    for _ in range(40):
        x, y = rnd.randint(0, W), rnd.randint(500, 1700)
        pts = [(x + wave(k * 10, 12, 80, rnd.random() * 6), y + k * 10) for k in range(rnd.randint(8, 22))]
        hd.line(pts, fill=(210, 40, 70, 190), width=5, joint='curve')
    img.alpha_composite(blur(hair, 1.5))
    return img


def vein_paths():
    """Venitas: una arteria horizontal + capilares verticales que suben hacia las burbujas."""
    if VEIN_PATHS: return VEIN_PATHS
    main = [(x, 1250 + wave(x, 22, 700, 0.8)) for x in range(-40, W + 41, 10)]
    VEIN_PATHS.append(main)
    for i, x0 in enumerate((200, 410, 620, 830)):
        top = 640 + (i % 2) * 110
        pts = [(x0 + wave(y, 18, 380, i), y) for y in range(top, 1250 + int(wave(x0, 22, 700, 0.8)) + 1, 10)]
        VEIN_PATHS.append(pts)
    return VEIN_PATHS


@lru_cache(maxsize=1)
def veins_layer():
    L = layer(); d = ImageDraw.Draw(L)
    for i, p in enumerate(vein_paths()):
        wdt = 34 if i == 0 else 16
        d.line(p, fill=(150, 10, 35, 255), width=wdt + 8, joint='curve')
        d.line(p, fill=(222, 32, 58, 255), width=wdt, joint='curve')
        d.line([(x, y - wdt * 0.22) for x, y in p], fill=(255, 120, 135, 160), width=max(3, wdt // 5), joint='curve')
    return L


@lru_cache(maxsize=1)
def bg_meeting():
    img = vgrad((W, H), rgba('#e9d6b8'), rgba('#c9a57a'))
    d = ImageDraw.Draw(img)
    # ventana esmerilada
    win = layer(); wd = ImageDraw.Draw(win)
    wd.rounded_rectangle([90, 420, 990, 900], 24, fill=(250, 245, 235, 230))
    for x in (390, 690):
        wd.rectangle([x - 6, 420, x + 6, 900], fill=(190, 160, 120, 255))
    wd.rectangle([90, 655, 990, 667], fill=(190, 160, 120, 255))
    img.alpha_composite(blur(win, 2))
    g = layer(); ImageDraw.Draw(g).ellipse([200, 400, 880, 900], fill=(255, 255, 240, 120))
    img.alpha_composite(blur(g, 90))
    return img


@lru_cache(maxsize=1)
def table_layer():
    L = layer(); d = ImageDraw.Draw(L)
    top = vgrad((W, 140), rgba('#a8693b'), rgba('#8a5229'))
    L.alpha_composite(top, (0, 1240))
    d.rectangle([0, 1240, W, 1248], fill=rgba('#c98a55'))
    front = vgrad((W, H - 1380), rgba('#6e3f1f'), rgba('#4a2812'))
    L.alpha_composite(front, (0, 1380))
    # papeles y tazas
    d.polygon([(90, 1280), (300, 1265), (310, 1350), (100, 1365)], fill=(250, 250, 245, 255))
    d.polygon([(760, 1270), (960, 1280), (950, 1360), (750, 1355)], fill=(250, 250, 245, 255))
    for cx in (330, 760):
        d.rounded_rectangle([cx - 38, 1190, cx + 38, 1280], 14, fill=(255, 255, 255, 255), outline=(200, 200, 200, 255), width=3)
        d.ellipse([cx - 38, 1180, cx + 38, 1202], fill=(120, 70, 40, 255), outline=(230, 230, 230, 255), width=4)
    return L


@lru_cache(maxsize=1)
def bg_bed():
    img = vgrad((W, H), rgba('#2a3370'), rgba('#141a40'))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([60, 520, 1020, 1000], 60, fill=rgba('#3a4590'))
    d.rounded_rectangle([60, 520, 1020, 560], 20, fill=rgba('#5260b0'))
    g = layer(); ImageDraw.Draw(g).ellipse([300, 300, 1000, 800], fill=(140, 150, 255, 50))
    img.alpha_composite(blur(g, 120))
    return img


# ======================================================================
#  PERSONAJE 2D (versión plana de los personajes del video de referencia)
# ======================================================================
PW, PH = 640, 980   # lienzo del personaje


def person(skin=(241, 194, 160), hair=(110, 68, 40), hair_style='short', shirt=(70, 130, 220),
           eyes='open', look=(0, 0), mouth='flat', cheeks=0.0, sweat=False, belly=0.0,
           arms='down', brows='normal', shake=0.0, body=True):
    s = 2
    im = Image.new('RGBA', (PW * s, PH * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    def B(x0, y0, x1, y1): return [x0 * s, y0 * s, x1 * s, y1 * s]
    def P(x, y): return (x * s, y * s)
    sk = tuple(skin) + (255,); skd = tuple(int(c * 0.86) for c in skin) + (255,)
    sh = tuple(shirt) + (255,); shd = tuple(int(c * 0.78) for c in shirt) + (255,); shl = tuple(min(255, int(c * 1.15 + 10)) for c in shirt) + (255,)
    hr = tuple(hair) + (255,); hrl = tuple(min(255, int(c * 1.35 + 10)) for c in hair) + (255,)
    cx = 320
    if hair_style == 'long':
        d.rounded_rectangle(B(150, 140, 490, 640), 150 * s, fill=hr)
    if body:
        # torso
        d.rounded_rectangle(B(120, 470, 520, 1100), 130 * s, fill=sh)
        d.rounded_rectangle(B(120, 470, 520, 1100), 130 * s, outline=shd, width=6 * s)
        d.ellipse(B(260, 440, 380, 520), fill=shd)  # cuello de la prenda
        d.rounded_rectangle(B(275, 390, 365, 480), 30 * s, fill=skd)  # cuello
        if belly > 0.001:
            bw, bh = 150 + 175 * belly, 120 + 100 * belly
            by = 790 - 30 * belly
            d.ellipse(B(cx - bw, by - bh, cx + bw, by + bh), fill=sh, outline=shd, width=6 * s)
            hl = Image.new('RGBA', im.size, (0, 0, 0, 0))
            ImageDraw.Draw(hl).ellipse(B(cx - bw * 0.55, by - bh * 0.75, cx - bw * 0.05, by - bh * 0.35), fill=(255, 255, 255, int(90 * belly)))
            im.alpha_composite(blur(hl, 14 * s)); d = ImageDraw.Draw(im)
        else:
            bw, bh, by = 150, 120, 790
        if arms == 'belly':
            for side in (-1, 1):
                x_sh = cx + side * 175
                hx = cx + side * (bw * 0.62)
                d.line([P(x_sh, 540), P(cx + side * (210 + bw * 0.25), 700), P(hx, by - bh * 0.15)], fill=sh, width=78 * s, joint='curve')
                d.line([P(x_sh, 540), P(cx + side * (210 + bw * 0.25), 700), P(hx, by - bh * 0.15)], fill=shd, width=6 * s)
                d.ellipse(B(hx - 46, by - bh * 0.15 - 38, hx + 46, by - bh * 0.15 + 38), fill=sk, outline=skd, width=4 * s)
        elif arms == 'down':
            for side in (-1, 1):
                x_sh = cx + side * 180
                d.line([P(x_sh, 540), P(cx + side * 215, 760), P(cx + side * 205, 960)], fill=sh, width=78 * s, joint='curve')
    # cabeza
    d.ellipse(B(155, 235, 205, 315), fill=skd)  # orejas
    d.ellipse(B(435, 235, 485, 315), fill=skd)
    d.ellipse(B(170, 90, 470, 420), fill=sk)
    sh_l = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh_l).ellipse(B(250, 330, 460, 430), fill=skd[:3] + (120,))
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).ellipse(B(170, 90, 470, 420), fill=255)
    tmp = Image.new('RGBA', im.size, (0, 0, 0, 0)); tmp.paste(blur(sh_l, 20 * s), (0, 0), m); im.alpha_composite(tmp); d = ImageDraw.Draw(im)
    # pelo
    if hair_style in ('short', 'long'):
        d.chord(B(160, 70, 480, 330), 180, 360, fill=hr)
        d.pieslice(B(160, 70, 480, 330), 150, 200, fill=hr)
        d.polygon([P(200, 200), P(300, 160), P(260, 215)], fill=hr)
        d.polygon([P(270, 190), P(420, 150), P(440, 215)], fill=hr)
        d.arc(B(200, 95, 420, 260), 200, 300, fill=hrl, width=10 * s)
        if hair_style == 'long':
            d.rounded_rectangle(B(160, 160, 215, 520), 30 * s, fill=hr)
            d.rounded_rectangle(B(425, 160, 480, 520), 30 * s, fill=hr)
    elif hair_style == 'curly':
        rnd = random.Random(4)
        for a in range(150, 391, 14):
            r = math.radians(a)
            x, y = cx + 165 * math.cos(r), 235 + 160 * math.sin(r)
            q = rnd.randint(40, 55)
            d.ellipse(B(x - q, y - q, x + q, y + q), fill=hr)
        d.chord(B(180, 95, 460, 300), 180, 360, fill=hr)
        for a in range(170, 371, 25):
            r = math.radians(a); x, y = cx + 150 * math.cos(r), 220 + 140 * math.sin(r)
            d.arc(B(x - 25, y - 25, x + 25, y + 25), 200, 340, fill=hrl, width=6 * s)
    # mejillas
    if cheeks > 0:
        ch = Image.new('RGBA', im.size, (0, 0, 0, 0)); cd = ImageDraw.Draw(ch)
        for x in (225, 415):
            cd.ellipse(B(x - 42, 318, x + 42, 362), fill=(240, 60, 60, int(170 * cheeks)))
        im.alpha_composite(blur(ch, 9 * s)); d = ImageDraw.Draw(im)
    # cejas
    for side, x in ((-1, 255), (1, 385)):
        if brows == 'worried':
            d.line([P(x - 38, 200 - side * 6 + (6 if side < 0 else 0)), P(x + 38, 200 + side * 6)], fill=hr, width=12 * s)
            d.line([P(x - 38, 196 + (side * 10)), P(x + 38, 196 - (side * 10))], fill=hr, width=12 * s)
        elif brows == 'raised':
            d.arc(B(x - 40, 180 - (10 if side > 0 else 0), x + 40, 230), 200, 340, fill=hr, width=11 * s)
        else:
            d.arc(B(x - 40, 186, x + 40, 236), 210, 330, fill=hr, width=11 * s)
    # ojos
    lx, ly = look
    for x in (255, 385):
        if eyes == 'closed':
            d.arc(B(x - 34, 240, x + 34, 290), 20, 160, fill=(70, 40, 30, 255), width=8 * s)
        elif eyes == 'squeeze':
            dx = 1 if x < 320 else -1
            d.line([P(x - 26 * dx, 245), P(x + 26 * dx, 262), P(x - 26 * dx, 280)], fill=(70, 40, 30, 255), width=9 * s, joint='curve')
        else:
            ew, eh = (34, 42) if eyes == 'open' else (38, 48)
            d.ellipse(B(x - ew, 262 - eh, x + ew, 262 + eh), fill=(255, 255, 255, 255), outline=(90, 60, 50, 255), width=3 * s)
            px, py = x + lx * 12, 266 + ly * 10
            d.ellipse(B(px - 20, py - 20, px + 20, py + 20), fill=(85, 55, 35, 255))
            d.ellipse(B(px - 10, py - 10, px + 10, py + 10), fill=(20, 12, 10, 255))
            d.ellipse(B(px - 12, py - 14, px - 3, py - 5), fill=(255, 255, 255, 255))
    # nariz
    d.ellipse(B(300, 290, 340, 325), fill=skd)
    # boca
    mc = (120, 40, 40, 255)
    if mouth == 'tense':
        d.rounded_rectangle(B(270, 355, 370, 385), 14 * s, fill=(255, 255, 255, 255), outline=mc, width=5 * s)
        for x in (295, 320, 345):
            d.line([P(x, 357), P(x, 383)], fill=(200, 160, 160, 255), width=3 * s)
    elif mouth == 'o':
        d.ellipse(B(298, 350, 342, 395), fill=(110, 30, 40, 255))
    elif mouth == 'smile':
        d.chord(B(270, 320, 370, 390), 10, 170, fill=(150, 45, 50, 255))
    elif mouth == 'wobble':
        d.line([P(275, 372), P(295, 360), P(320, 375), P(345, 360), P(365, 372)], fill=mc, width=8 * s, joint='curve')
    elif mouth == 'side':
        d.line([P(290, 372), P(350, 362)], fill=mc, width=8 * s)
    else:
        d.arc(B(285, 340, 355, 380), 30, 150, fill=mc, width=7 * s)
    if sweat:
        d.polygon([P(452, 160), P(436, 205), P(468, 205)], fill=(170, 225, 255, 255))
        d.ellipse(B(434, 190, 470, 228), fill=(170, 225, 255, 255))
        d.ellipse(B(444, 198, 454, 210), fill=(255, 255, 255, 255))
    return im.resize((PW, PH), Image.LANCZOS)


# ---- bacterias (personajes) ----
@lru_cache(maxsize=32)
def bacterium(kind, mouth_open=0):
    cols = {'green': ((120, 210, 90), (70, 150, 50)), 'purple': ((150, 110, 230), (100, 70, 170)),
            'blue': ((90, 190, 240), (50, 130, 190)), 'orange': ((250, 170, 60), (200, 120, 30))}
    c, cd = cols[kind]
    def fn(im, s):
        d = ImageDraw.Draw(im)
        if kind == 'green':      # bacilo con flagelo
            d.line([(40 * s, 95 * s), (10 * s, 80 * s), (0, 110 * s)], fill=cd + (255,), width=6 * s, joint='curve')
            d.rounded_rectangle([40 * s, 50 * s, 230 * s, 140 * s], 45 * s, fill=c + (255,), outline=cd + (255,), width=5 * s)
            for x in (80, 130, 180):
                d.ellipse([(x - 12) * s, 115 * s, (x + 12) * s, 130 * s], fill=cd + (255,))
            ex = [150, 195]; ey = 82
        elif kind == 'purple':   # coco
            d.ellipse([40 * s, 30 * s, 210 * s, 170 * s], fill=c + (255,), outline=cd + (255,), width=5 * s)
            ex = [100, 150]; ey = 85
        elif kind == 'orange':   # cadena (estreptococo)
            for i, x in enumerate((50, 105, 160, 215)):
                d.ellipse([(x - 30) * s, 70 * s, (x + 30) * s, 130 * s], fill=c + (255,), outline=cd + (255,), width=4 * s)
            ex = [195, 230]; ey = 92
        else:
            d.ellipse([30 * s, 40 * s, 220 * s, 160 * s], fill=c + (255,), outline=cd + (255,), width=5 * s)
            ex = [105, 155]; ey = 88
        for x in ex:
            d.ellipse([(x - 17) * s, (ey - 20) * s, (x + 17) * s, (ey + 20) * s], fill=(255, 255, 255, 255), outline=(40, 40, 60, 255), width=3 * s)
            d.ellipse([(x - 7) * s, (ey - 6) * s, (x + 9) * s, (ey + 10) * s], fill=(20, 20, 40, 255))
            d.ellipse([(x - 4) * s, (ey - 4) * s, (x + 1) * s, (ey + 1) * s], fill=(255, 255, 255, 255))
        mx = sum(ex) / 2
        if mouth_open:
            d.ellipse([(mx - 16) * s, (ey + 26) * s, (mx + 16) * s, (ey + 52) * s], fill=(90, 20, 40, 255))
        else:
            d.arc([(mx - 16) * s, (ey + 16) * s, (mx + 16) * s, (ey + 40) * s], 20, 160, fill=(60, 20, 30, 255), width=4 * s)
    return ss_sprite(250, 200, fn)


@lru_cache(maxsize=8)
def food_item(kind):
    def fn(im, s):
        d = ImageDraw.Draw(im)
        if kind == 'bread':
            d.rounded_rectangle([20 * s, 40 * s, 160 * s, 160 * s], 30 * s, fill=(222, 160, 90, 255))
            d.rounded_rectangle([34 * s, 54 * s, 146 * s, 150 * s], 22 * s, fill=(250, 232, 200, 255))
        elif kind == 'lettuce':
            for a in range(0, 360, 30):
                r = math.radians(a); x, y = 90 + 52 * math.cos(r), 100 + 52 * math.sin(r)
                d.ellipse([(x - 34) * s, (y - 34) * s, (x + 34) * s, (y + 34) * s], fill=(110, 190, 70, 255))
            d.ellipse([50 * s, 60 * s, 130 * s, 140 * s], fill=(150, 215, 100, 255))
            for a in range(0, 360, 45):
                r = math.radians(a); d.line([(90 * s, 100 * s), ((90 + 60 * math.cos(r)) * s, (100 + 60 * math.sin(r)) * s)], fill=(200, 240, 160, 255), width=3 * s)
        else:  # carrot
            d.polygon([(30 * s, 70 * s), (70 * s, 40 * s), (170 * s, 160 * s)], fill=(245, 130, 40, 255))
            d.line([(60 * s, 80 * s), (75 * s, 70 * s)], fill=(200, 90, 20, 255), width=4 * s)
            d.line([(90 * s, 110 * s), (105 * s, 100 * s)], fill=(200, 90, 20, 255), width=4 * s)
            for dx in (-12, 0, 12):
                d.line([(45 * s, 55 * s), ((25 + dx) * s, 15 * s)], fill=(90, 170, 60, 255), width=8 * s)
    return ss_sprite(180, 180, fn)
