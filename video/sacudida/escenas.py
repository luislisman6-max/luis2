"""Escenas del video «Sacudida hípnica». Todos los tiempos salen de words.json (palabra exacta),
así animación, efectos y subtítulos usan el mismo reloj."""
import json, math, os, random, sys, unicodedata
from functools import lru_cache
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from lib import *          # noqa
from art import *          # noqa
from scenes import P, puff_sprite, brain_sprite, follow_button, label, pill, sparkle, float_bubbles, glitch, blanket  # noqa

WORDS = json.load(open(os.path.join(HERE, 'words.json')))


def _n(w):
    w = unicodedata.normalize('NFD', w.lower())
    return ''.join(c for c in w if unicodedata.category(c) != 'Mn' and c.isalnum())


def at(word, k=1):
    """inicio (s) de la k-ésima aparición de una palabra en la voz"""
    c = 0
    for w in WORDS:
        if _n(w['w']) == _n(word):
            c += 1
            if c == k: return w['s']
    raise KeyError(word)


def end(word, k=1):
    c = 0
    for w in WORDS:
        if _n(w['w']) == _n(word):
            c += 1
            if c == k: return w['e']
    raise KeyError(word)


# ------------------------------------------------------------------ efectos de sonido (se rellenan abajo)
SFX = []


def sfx(t, name, g=0.0, **kw):
    SFX.append((t, name, g, kw))


# ==================================================================== piezas de arte
SKIN = (241, 194, 160)
HAIR = (70, 45, 30)
PJ = (90, 120, 230)   # pijama


@lru_cache(maxsize=1)
def pillow_sprite():
    def fn(im, s):
        L = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rounded_rectangle([10 * s, 20 * s, 610 * s, 330 * s], 110 * s, fill=(30, 30, 80, 120))
        im.alpha_composite(blur(L, 14 * s)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, 600 * s, 320 * s], 110 * s, fill=(214, 224, 255, 255), outline=(170, 185, 240, 255), width=5 * s)
        d.arc([120 * s, 40 * s, 480 * s, 300 * s], 200, 340, fill=(240, 245, 255, 255), width=10 * s)
        d.line([(300 * s, 18 * s), (300 * s, 60 * s)], fill=(180, 195, 245, 255), width=5 * s)
    return ss_sprite(620, 340, fn)


def face(eyes='closed', mouth='flat', brows='normal', sweat=False, cheeks=0.3, look=(0, 0)):
    return P(body=False, eyes=eyes, mouth=mouth, brows=brows, sweat=sweat, cheeks=cheeks, skin=SKIN, hair=HAIR, look=look)


def zzz(img, t, x=760, y=700, alpha=1.0):
    for j in range(3):
        u = ((t * 0.45) + j / 3) % 1
        paste(img, label("Z", 70 + j * 12, fill=(220, 225, 255, 255), stroke=6), x + 120 * u, y - 200 * u,
              alpha=alpha * math.sin(math.pi * u), rot=-15)


def motion_lines(img, cx, cy, w, k, col=(255, 255, 255)):
    """rayitas de movimiento bajo algo que salta"""
    if k <= 0: return
    d = ImageDraw.Draw(img)
    a = int(230 * k)
    for dx, ln in ((-0.35, 0.8), (0.0, 1.0), (0.35, 0.8)):
        x = cx + dx * w
        d.line([(x, cy + 20), (x, cy + 20 + 120 * ln * k)], fill=col + (a,), width=10)


def bed(t, eyes='closed', mouth='flat', brows='normal', jump=0.0, shake=0.0, zz=1.0, sweat=False, cheeks=0.3, look=(0, 0)):
    """cuarto azul de noche con el personaje acostado. jump 0..1 sube todo el cuerpo."""
    img = bg_room().copy()
    jy = -150 * jump
    jx = math.sin(t * 95) * 9 * shake
    paste(img, pillow_sprite(), 540 + jx * 0.3, 830 + jy * 0.55)
    paste(img, face(eyes, mouth, brows, sweat, cheeks, look), 540 + jx, 1023 + jy, scale=0.95, rot=4 * shake * math.sin(t * 70))
    paste(img, blanket(), 540 + jx * 0.6, 1460 + jy * 0.8, rot=-3 * jump)
    if jump > 0.05:
        motion_lines(img, 540, 1460 + 500 + jy * 0.8 - 40, 560, min(1, jump * 1.5))
    if zz > 0.01: zzz(img, t, alpha=zz)
    return img


@lru_cache(maxsize=1)
def bg_room():
    img = bg_bed().copy()
    d = ImageDraw.Draw(img)
    # ventana con luna (lado derecho, debajo de los subtítulos)
    g = layer(); ImageDraw.Draw(g).rounded_rectangle([700, 1700, 1000, 1880], 20, fill=(0, 0, 0, 0))
    win = [740, 140, 1010, 470]
    d.rounded_rectangle(win, 26, fill=(18, 24, 70, 255), outline=(110, 125, 210, 255), width=10)
    gl = layer(); ImageDraw.Draw(gl).ellipse([840, 190, 960, 310], fill=(255, 245, 190, 150))
    img.alpha_composite(blur(gl, 30))
    d.ellipse([860, 210, 940, 290], fill=(255, 245, 200, 255))
    d.ellipse([882, 200, 962, 280], fill=(18, 24, 70, 255))
    rnd = random.Random(2)
    for _ in range(10):
        x, y = rnd.randint(760, 990), rnd.randint(160, 450); d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(230, 230, 255, 230))
    d.line([(875, 140), (875, 470)], fill=(110, 125, 210, 255), width=8)
    d.line([(740, 305), (1010, 305)], fill=(110, 125, 210, 255), width=8)
    # mesita con lámpara (izquierda)
    d.rounded_rectangle([0, 1180, 70, 1500], 16, fill=(90, 70, 140, 255))
    return img


# ---- vacío / caída
@lru_cache(maxsize=2)
def bg_void(tint=0):
    top, bot = (rgba('#2d1650'), rgba('#07030f')) if tint == 0 else (rgba('#13305e'), rgba('#050a18'))
    img = rgrad((W, H), (540, 900), 1300, top, bot)
    rnd = random.Random(9 + tint)
    d = ImageDraw.Draw(img)
    for _ in range(90):
        x, y, r = rnd.randint(0, W), rnd.randint(0, H), rnd.choice((2, 2, 3, 4))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(220, 210, 255, rnd.randint(90, 220)))
    return img


def speed_streaks(img, t, n=26, seed=2, speed=2600, col=(200, 190, 255)):
    rnd = random.Random(seed)
    L = layer(); d = ImageDraw.Draw(L)
    for i in range(n):
        x = rnd.uniform(30, W - 30); ln = rnd.uniform(160, 420); ph = rnd.random()
        y = H + 400 - ((ph * (H + 800) + t * speed * rnd.uniform(0.7, 1.3)) % (H + 800))
        d.line([(x, y), (x, y + ln)], fill=col + (rnd.randint(70, 160),), width=rnd.choice((3, 4, 6)))
    img.alpha_composite(blur(L, 1.5))


def arms_flail(img, cx, cy, sc, t, col=PJ, skin=SKIN):
    """brazos levantados agitándose (dibujados detrás del cuerpo)"""
    d = ImageDraw.Draw(img)
    for side in (-1, 1):
        a = math.radians(-60 + 22 * math.sin(t * 17 + side))
        sx, sy = cx + side * 180 * sc, cy + (540 - 490) * sc
        ex = sx + side * math.cos(a) * 230 * sc; ey = sy + math.sin(a) * 230 * sc
        hx = ex + side * 70 * sc * math.cos(a + side * 0.6); hy = ey + 120 * sc * math.sin(a - 0.4)
        d.line([(sx, sy), (ex, ey), (hx, hy)], fill=col + (255,), width=int(70 * sc), joint='curve')
        r = 42 * sc
        d.ellipse([hx - r, hy - r, hx + r, hy + r], fill=skin + (255,), outline=tuple(int(c * .86) for c in skin) + (255,), width=4)


def legs_flail(img, cx, cy, sc, t, col=(60, 85, 190)):
    d = ImageDraw.Draw(img)
    for side in (-1, 1):
        a = 16 * math.sin(t * 15 + side * 2)
        sx, sy = cx + side * 80 * sc, cy + 560 * sc
        ex = sx + side * (60 + a) * sc; ey = sy + 250 * sc
        d.line([(sx, sy), (ex, ey)], fill=col + (255,), width=int(95 * sc))
        d.ellipse([ex - 55 * sc, ey - 25 * sc, ex + 55 * sc, ey + 40 * sc], fill=(235, 235, 245, 255))


def faller(img, t, cx, cy, sc=0.8, rot=0.0):
    arms_flail(img, cx, cy, sc, t)
    legs_flail(img, cx, cy, sc, t)
    p = P(mouth='o', eyes='wide', brows='raised', sweat=True, cheeks=0.6, shirt=PJ, arms='none', skin=SKIN, hair=HAIR)
    paste(img, p, cx, cy, scale=sc, rot=rot)


# ---- holograma con sistema nervioso
HB_BRAIN = (280, 140)


def nerve_paths():
    """caminos (en coordenadas del holograma) desde el cerebro hacia brazos y piernas"""
    spine = [(280, 150 + i * 14) for i in range(41)]   # 150 -> 710
    arm_l = [(280, 330)] + [(lerp(240, 140, k / 10), lerp(330, 330, k / 10)) for k in range(11)] + \
            [(lerp(140, 95, k / 10), lerp(330, 560, k / 10)) for k in range(11)] + [(lerp(95, 85, k / 10), lerp(560, 760, k / 10)) for k in range(11)]
    arm_r = [(560 - x, y) for x, y in arm_l]
    leg_l = [(lerp(280, 215, k / 10), lerp(700, 720, k / 10)) for k in range(11)] + [(lerp(215, 205, k / 20), lerp(720, 1130, k / 20)) for k in range(21)]
    leg_r = [(560 - x, y) for x, y in leg_l]
    return spine, arm_l, arm_r, leg_l, leg_r


def _poly(pts, sc=1.05, cx=540, cy=1060):
    return [(cx + (x - HB_W / 2) * sc, cy + (y - HB_H / 2) * sc) for x, y in pts]


@lru_cache(maxsize=1)
def nerves_layer():
    L = layer(); d = ImageDraw.Draw(L)
    for p in nerve_paths():
        d.line(_poly(p), fill=(255, 230, 120, 200), width=11, joint='curve')
    g = blur(L, 6); g.alpha_composite(L)
    return g


def holo(t, brain=0.0, nerves=0.0, brain_col=None):
    img = bg_holo('blue').copy()
    paste(img, holo_body(), 540, 1060, scale=1.05)
    if nerves > 0.01:
        paste(img, nerves_layer(), 540, 960, alpha=nerves)
    if brain > 0.01:
        bx, by = _poly([HB_BRAIN])[0]
        b = brain_sprite()
        paste(img, b, bx, by, scale=0.62 * brain * (1 + 0.04 * math.sin(t * 6)))
    return img


def pulse_dots(img, k, paths=None, col=(255, 240, 140)):
    """bolitas de luz que recorren los nervios. k 0..1"""
    if k <= 0 or k >= 1.15: return
    paths = paths or nerve_paths()
    L = layer(); d = ImageDraw.Draw(L)
    for p in paths:
        pp = _poly(p)
        for off in (0.0, -0.08, -0.16):
            kk = k + off
            if not (0 <= kk <= 1): continue
            x, y = pp[min(len(pp) - 1, int(kk * (len(pp) - 1)))]
            r = 22 if off == 0 else 14 + off * 30
            d.ellipse([x - r, y - r, x + r, y + r], fill=col + (255 if off == 0 else 150,))
    img.alpha_composite(blur(L, 10)); img.alpha_composite(L)


# ---- corazón + electro
@lru_cache(maxsize=2)
def heart_sprite():
    def fn(im, s):
        L = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.ellipse([20 * s, 30 * s, 300 * s, 300 * s], fill=(255, 60, 100, 160))
        im.alpha_composite(blur(L, 26 * s)); d = ImageDraw.Draw(im)
        d.ellipse([40 * s, 50 * s, 170 * s, 180 * s], fill=(235, 40, 80, 255))
        d.ellipse([150 * s, 50 * s, 280 * s, 180 * s], fill=(235, 40, 80, 255))
        d.polygon([(44 * s, 140 * s), (276 * s, 140 * s), (160 * s, 290 * s)], fill=(235, 40, 80, 255))
        d.ellipse([75 * s, 80 * s, 125 * s, 115 * s], fill=(255, 170, 190, 230))
    return ss_sprite(320, 320, fn)


def ecg(img, t, t0, beats, y=1450, x0=90, x1=990, col=(90, 255, 160)):
    """línea del electro: dibuja picos en las horas de latido (beats)"""
    d = ImageDraw.Draw(img)
    span = 2.4                  # segundos visibles
    pts = []
    for i in range(0, 181):
        tt = t - span + span * i / 180
        x = lerp(x0, x1, i / 180)
        v = 0
        for b in beats:
            dt = tt - b
            if -0.05 < dt < 0.12:
                v += (-260 * math.exp(-((dt - 0.02) / 0.018) ** 2) + 90 * math.exp(-((dt - 0.06) / 0.02) ** 2))
        pts.append((x, y + v))
    L = layer(); ImageDraw.Draw(L).line(pts, fill=col + (160,), width=18, joint='curve')
    img.alpha_composite(blur(L, 10))
    d.line(pts, fill=col + (255,), width=7, joint='curve')
    x, yy = pts[-1]
    d.ellipse([x - 12, yy - 12, x + 12, yy + 12], fill=(230, 255, 240, 255))


# ---- fibras musculares (mundo rosa)
@lru_cache(maxsize=1)
def bg_muscle():
    img = vgrad((W, H), rgba('#8e2148'), rgba('#5e1233'))
    g = layer(); ImageDraw.Draw(g).ellipse([60, 500, 1020, 1400], fill=rgba('#c2456f', 110))
    img.alpha_composite(blur(g, 150))
    rnd = random.Random(3)
    v = layer(); vd = ImageDraw.Draw(v)
    for x0 in range(-20, W + 60, 70):
        ph = rnd.random() * 6
        vd.line([(x0 + wave(y, 14, 260, ph), y) for y in range(0, H, 8)], fill=rgba('#a83a62', 90), width=6)
    img.alpha_composite(blur(v, 2))
    return img


def fiber(img, y, h, waviness, squeeze, t, ph, glow=0.0):
    """una fibra muscular horizontal a rayas. waviness: 0 tensa / 1 relajada. squeeze: contracción"""
    hh = h * (1 + 0.35 * squeeze)
    x0, x1 = 40 + 90 * squeeze, W - 40 - 90 * squeeze
    n = 60
    amp = 6 + 46 * waviness
    top, bot = [], []
    for i in range(n + 1):
        x = lerp(x0, x1, i / n)
        c = y + amp * math.sin(i / n * math.pi * 2.2 + ph + t * (0.8 + 1.2 * waviness)) + 18 * waviness * math.sin(i / n * math.pi)
        top.append((x, c - hh / 2)); bot.append((x, c + hh / 2))
    poly = top + bot[::-1]
    L = layer(); d = ImageDraw.Draw(L)
    if glow > 0:
        d.polygon(poly, fill=(255, 80, 110, int(200 * glow)))
        g = blur(L, 30); img.alpha_composite(g); L = layer(); d = ImageDraw.Draw(L)
    d.polygon(poly, fill=rgba('#d24a73'))
    for i in range(0, n, 2):   # rayas
        a, b = top[i], bot[i]; c, e = top[i + 1], bot[i + 1]
        d.polygon([a, c, e, b], fill=rgba('#a8325a'))
    d.line([(x, yy + hh * 0.18) for x, yy in top], fill=(255, 190, 210, 120), width=8)
    d.line(top, fill=rgba('#ffc2d2'), width=6); d.line(bot, fill=rgba('#7a1a3e'), width=6)
    d.ellipse([x0 - hh / 2 * 0.6, top[0][1], x0 + hh / 2 * 0.6, bot[0][1]], fill=rgba('#ffc2d2'))
    d.ellipse([x1 - hh / 2 * 0.6, top[-1][1], x1 + hh / 2 * 0.6, bot[-1][1]], fill=rgba('#e98aa6'))
    img.alpha_composite(L)


def muscle_scene(t, waviness, squeeze=0.0, glow=0.0):
    img = bg_muscle().copy()
    for i, y in enumerate((690, 900, 1110, 1320)):
        fiber(img, y, 150, waviness, squeeze, t, i * 1.3, glow)
    return img


# ---- iconos
@lru_cache(maxsize=2)
def person_icon(on):
    def fn(im, s):
        col = (255, 205, 60, 255) if on else (120, 110, 170, 255)
        d = ImageDraw.Draw(im)
        if on:
            L = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(L).ellipse([10 * s, 10 * s, 150 * s, 210 * s], fill=(255, 200, 60, 130))
            im.alpha_composite(blur(L, 14 * s)); d = ImageDraw.Draw(im)
        d.ellipse([50 * s, 20 * s, 110 * s, 80 * s], fill=col)
        d.rounded_rectangle([30 * s, 92 * s, 130 * s, 200 * s], 40 * s, fill=col)
    return ss_sprite(160, 220, fn)


@lru_cache(maxsize=1)
def coffee_sprite():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.ellipse([20 * s, 250 * s, 300 * s, 300 * s], fill=(240, 240, 250, 255))
        d.rounded_rectangle([60 * s, 110 * s, 240 * s, 280 * s], 40 * s, fill=(255, 255, 255, 255), outline=(200, 200, 215, 255), width=5 * s)
        d.arc([210 * s, 140 * s, 290 * s, 230 * s], -90, 90, fill=(255, 255, 255, 255), width=18 * s)
        d.ellipse([70 * s, 100 * s, 230 * s, 140 * s], fill=(110, 60, 30, 255))
        d.rounded_rectangle([60 * s, 170 * s, 240 * s, 200 * s], 5 * s, fill=(236, 70, 90, 255))
    return ss_sprite(320, 320, fn)


@lru_cache(maxsize=1)
def storm_sprite():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        for (x, y, r) in ((110, 140, 70), (180, 110, 85), (250, 150, 65), (160, 170, 60), (220, 175, 60)):
            d.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s], fill=(110, 115, 150, 255))
        for (x, y, r) in ((180, 100, 60), (120, 130, 45)):
            d.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s], fill=(140, 145, 180, 255))
        d.polygon([(185 * s, 190 * s), (140 * s, 270 * s), (180 * s, 270 * s), (150 * s, 330 * s), (235 * s, 240 * s), (195 * s, 240 * s), (225 * s, 190 * s)],
                  fill=(255, 220, 60, 255), outline=(255, 250, 200, 255))
    return glow_sprite(ss_sprite(330, 340, fn), 10, (255, 220, 80, 120))


@lru_cache(maxsize=1)
def battery_sprite():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([20 * s, 70 * s, 270 * s, 200 * s], 26 * s, fill=(30, 30, 50, 255), outline=(255, 255, 255, 255), width=10 * s)
        d.rounded_rectangle([270 * s, 110 * s, 300 * s, 160 * s], 8 * s, fill=(255, 255, 255, 255))
        d.rounded_rectangle([42 * s, 92 * s, 90 * s, 178 * s], 10 * s, fill=(240, 50, 70, 255))
    return glow_sprite(ss_sprite(320, 270, fn), 12, (255, 60, 80, 140))


@lru_cache(maxsize=1)
def bolt_sprite():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.polygon([(130 * s, 0), (20 * s, 190 * s), (100 * s, 190 * s), (60 * s, 340 * s), (210 * s, 130 * s), (130 * s, 130 * s), (180 * s, 0)],
                  fill=(255, 215, 60, 255), outline=(255, 250, 210, 255))
    return glow_sprite(ss_sprite(230, 350, fn), 16, (255, 210, 60, 200))


@lru_cache(maxsize=1)
def rock_sprite():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.polygon([(10 * s, 150 * s), (40 * s, 60 * s), (120 * s, 20 * s), (200 * s, 50 * s), (240 * s, 150 * s)], fill=(130, 125, 160, 255), outline=(80, 75, 110, 255))
        d.polygon([(60 * s, 70 * s), (120 * s, 35 * s), (150 * s, 60 * s), (90 * s, 90 * s)], fill=(175, 170, 205, 255))
    return ss_sprite(250, 160, fn)


@lru_cache(maxsize=1)
def stairs_layer():
    L = layer(); d = ImageDraw.Draw(L)
    for i in range(7):
        x = 60 + i * 140; y = 760 + i * 130
        d.rectangle([x, y, W + 40, y + 130], fill=(120, 95, 170, 255))
        d.rectangle([x, y, W + 40, y + 22], fill=(185, 160, 235, 255))
    return L


@lru_cache(maxsize=1)
def gift_sprite():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([30 * s, 120 * s, 290 * s, 320 * s], 16 * s, fill=(236, 60, 100, 255))
        d.rounded_rectangle([15 * s, 85 * s, 305 * s, 140 * s], 14 * s, fill=(255, 90, 130, 255))
        d.rectangle([140 * s, 85 * s, 180 * s, 320 * s], fill=(255, 215, 70, 255))
        d.ellipse([80 * s, 30 * s, 160 * s, 95 * s], outline=(255, 215, 70, 255), width=16 * s)
        d.ellipse([160 * s, 30 * s, 240 * s, 95 * s], outline=(255, 215, 70, 255), width=16 * s)
    return ss_sprite(320, 330, fn)


@lru_cache(maxsize=1)
def dream_frame():
    """borde de nube (escena de sueño)"""
    L = layer(); d = ImageDraw.Draw(L)
    d.rectangle([0, 0, W, H], fill=(235, 235, 255, 255))
    m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m)
    md.rounded_rectangle([70, 470, W - 70, H - 230], 120, fill=255)
    for i in range(9):
        x = 70 + i * (W - 140) / 8
        md.ellipse([x - 70, 410, x + 70, 550], fill=255); md.ellipse([x - 70, H - 300, x + 70, H - 160], fill=255)
    for j in range(10):
        y = 520 + j * (H - 800) / 9
        md.ellipse([10, y - 70, 150, y + 70], fill=255); md.ellipse([W - 150, y - 70, W - 10, y + 70], fill=255)
    hole = Image.eval(m, lambda v: 255 - v)
    out = layer(); out.paste(Image.new('RGBA', (W, H), (16, 14, 40, 200)), (0, 0), hole)
    edge = layer(); edge.paste(Image.new('RGBA', (W, H), (190, 190, 255, 255)), (0, 0), m)
    e2 = blur(edge, 3)
    ring = ImageChops.subtract(m.filter(ImageFilter.MaxFilter(9)), m)
    rl = layer(); rl.paste(Image.new('RGBA', (W, H), (220, 220, 255, 230)), (0, 0), ring)
    out.alpha_composite(blur(rl, 4))
    return out


def bars(img, t, t0, k_end, x0=180, y0=1500):
    hs = (170, 290, 430, 600)
    d = ImageDraw.Draw(img)
    for i, h in enumerate(hs):
        k = ease_back(prog(t, t0 + i * 0.22, 0.35), 1.4)
        if k <= 0: continue
        x = x0 + i * 190
        top = y0 - h * k
        L = layer(); ImageDraw.Draw(L).rounded_rectangle([x, top, x + 130, y0], 22, fill=(255, 200, 60, 140))
        img.alpha_composite(blur(L, 14))
        d.rounded_rectangle([x, top, x + 130, y0], 22, fill=(255, 205, 60, 255), outline=(255, 240, 190, 255), width=4)
        paste(img, bolt_sprite(), x + 65, top - 80, scale=0.33 * k)
    d.line([(x0 - 40, y0 + 6), (x0 + 760, y0 + 6)], fill=(255, 255, 255, 220), width=6)


def big_arrow(img, x, y, s, up=True, col=(80, 230, 140)):
    if s <= 0: return
    d = ImageDraw.Draw(img)
    k = -1 if up else 1
    pts = [(x, y + k * 160 * s), (x - 120 * s, y + k * 20 * s), (x - 50 * s, y + k * 20 * s), (x - 50 * s, y - k * 150 * s),
           (x + 50 * s, y - k * 150 * s), (x + 50 * s, y + k * 20 * s), (x + 120 * s, y + k * 20 * s)]
    L = layer(); ImageDraw.Draw(L).polygon(pts, fill=col + (150,))
    img.alpha_composite(blur(L, 18))
    d.polygon(pts, fill=col + (255,), outline=(255, 255, 255, 255))


def cross(img, x, y, s, col=(240, 50, 70)):
    if s <= 0: return
    d = ImageDraw.Draw(img); r = 150 * s
    for a, b in (((x - r, y - r), (x + r, y + r)), ((x + r, y - r), (x - r, y + r))):
        d.line([a, b], fill=(255, 255, 255, 255), width=int(54 * s))
        d.line([a, b], fill=col + (255,), width=int(38 * s))


def coaster_track(k_draw):
    """vía de la montaña rusa (coordenadas de pantalla)"""
    pts = []
    for i in range(0, 241):
        u = i / 240
        x = lerp(-60, W + 60, u)
        y = 1000 - 330 * math.sin(u * math.pi * 1.0) * (1 - u * 0.4) + 240 * math.sin(u * math.pi * 3.0)
        pts.append((x, y))
    return pts[:max(2, int(len(pts) * k_draw))]


# ==================================================================== ESCENAS
# cada escena: f(t) -> (imagen RGBA, zoom, (cx, cy))

def sc_hook(t):   # ¿Alguna vez has estado a punto de dormir y, de repente,
    t_sleep, t_rep = at('dormir', 1), at('repente')
    eyes = 'open' if t < t_sleep - 0.1 else 'closed'
    if t >= t_rep: eyes = 'wide'
    shk = 1.0 if t >= t_rep else 0.0
    img = bed(t, eyes=eyes, mouth='o' if t >= t_rep else 'flat', brows='raised' if t >= t_rep else 'normal',
              zz=ease_out(prog(t, t_sleep, 0.4)) * (1 - prog(t, t_rep, 0.15)), shake=shk, sweat=t >= t_rep, cheeks=0.6 if t >= t_rep else 0.3)
    if t >= t_rep:
        paste(img, alert_badge(), 720, 830, scale=pop(t, t_rep))
    z = lerp(1.0, 1.10, ease_in_out(prog(t, 0, t_rep))) + 0.08 * ease_out(prog(t, t_rep, 0.3))
    return img, z, (540, 1000)


def sc_fall(t, t0, tint=0, label_txt=None, t_lab=None):
    img = bg_void(tint).copy()
    speed_streaks(img, t, speed=2000 + 1400 * prog(t, t0, 0.6))
    y = lerp(700, 1000, ease_out(prog(t, t0, 0.8))) + 18 * math.sin(t * 9)
    faller(img, t, 540 + 30 * math.sin(t * 3.1), y, 0.72, rot=8 * math.sin(t * 4))
    if label_txt and t >= t_lab:
        paste(img, label(label_txt, 120, fill=(255, 225, 80, 255), stroke=10), 540, 1580, scale=pop(t, t_lab), rot=-6)
    return img, 1.0 + 0.06 * prog(t, t0, 2.0), (540, 960)


def sc_fall1(t):   # sientes que caes al vacío
    return sc_fall(t, at('caes', 1), 0, '¡AL VACÍO!', at('vacio', 1))


def sc_jump(t, t_salto, txt_t=None, badge_t=None):
    k = prog(t, t_salto, 0.55)
    jump = math.sin(math.pi * k) if 0 < k < 1 else 0.0
    after = t >= t_salto
    img = bed(t, eyes='wide' if after else 'closed', mouth='o' if after else 'flat', brows='raised' if after else 'normal',
              jump=jump, shake=1.0 if after and k >= 1 else 0, zz=0 if after else 0.8, sweat=after, cheeks=0.7 if after else 0.3)
    if after:
        paste(img, label('¡ZAS!', 130, fill=(255, 225, 80, 255), stroke=11), 300, 700, scale=pop(t, t_salto, 0.3), rot=-12)
    if badge_t and t >= badge_t:
        paste(img, alert_badge(), 770, 860, scale=pop(t, badge_t))
    z = 1.0 + 0.05 * math.sin(math.pi * k) if 0 < k < 1 else 1.0
    return img, z, (540, 1100)


def sc_jump1(t):   # y tu cuerpo da un salto involuntario?
    return sc_jump(t, at('salto', 1), badge_t=at('involuntario'))


def sc_still(t):   # Lo más extraño es que ni siquiera te estabas moviendo.
    img = holo(t)
    t_ext, t_mov = at('extrano'), at('moviendo')
    # flechas de movimiento alrededor
    for i, (x, y, rot) in enumerate(((210, 900, 90), (870, 900, -90), (540, 1720, 180))):
        s = pop(t, at('siquiera') + i * 0.12) * 0.45
        if s > 0:
            big_arrow(img, x, y, s, up=True, col=(120, 200, 255))
    if t >= t_ext:
        paste(img, label('?', 220, fill=(255, 225, 80, 255), stroke=12), 820, 620, scale=pop(t, t_ext), rot=10 * math.sin(t * 3))
    if t >= t_mov:
        cross(img, 540, 1060, pop(t, t_mov) * 1.4)
        paste(img, pill('0 MOVIMIENTO', (200, 50, 80), 52), 540, 1560, scale=pop(t, t_mov + 0.15))
    return img, lerp(1.0, 1.06, prog(t, 7.8, 2.8)), (540, 1000)


def sc_name(t):   # Este fenómeno se llama sacudida hípnica,
    img = bg_teal().copy()
    float_bubbles(img, t, n=8, seed=4, rmin=14, rmax=36, area=(0, 500, W, 1700), speed=50, alpha=0.5)
    t_s, t_h = at('sacudida', 1), at('hipnica')
    if t < t_s:
        paste(img, pill('???', (40, 120, 240), 90), 540, 1000 + 8 * math.sin(t * 5), scale=pop(t, at('fenomeno')))
    else:
        paste(img, bolt_sprite(), 540, 760, scale=pop(t, t_s) * (1 + 0.05 * math.sin(t * 9)))
        paste(img, label('SACUDIDA', 150, fill=(255, 255, 255, 255), stroke=12), 540, 1060, scale=pop(t, t_s))
        if t >= t_h:
            paste(img, label('HÍPNICA', 150, fill=(255, 215, 60, 255), stroke=12), 540, 1230, scale=pop(t, t_h))
    if t_s <= t < t_s + 0.22:
        img = glitch(img, t)
    z = 1.0 + 0.1 * (1 - ease_out(prog(t, t_s, 0.35))) if t >= t_s else 1.0
    return img, z, (540, 1060)


def sc_stat(t):   # y se estima que hasta el 70% de las personas lo experimenta alguna vez.
    img = bg_purple().copy()
    t_h, t_70, t_p = at('hasta'), at('70%'), at('personas')
    k = ease_out(prog(t, t_h, (t_70 + 0.35) - t_h))
    n = int(round(70 * k))
    if t >= t_h:
        s = pop(t, t_h, 0.25) * (1 + 0.15 * (1 - prog(t, t_70 + 0.35, 0.25)) * (t >= t_70 + 0.35))
        paste(img, label(f'{n}%', 300, fill=(255, 205, 60, 255), stroke=14), 540, 820, scale=s)
    # 10 personitas, se encienden 7
    for i in range(10):
        x = 140 + (i % 5) * 200; y = 1180 + (i // 5) * 250
        s = pop(t, t_h + 0.05 * i, 0.25)
        on = i < 7 and t >= t_p + i * 0.07
        paste(img, person_icon(on), x, y, scale=s * (1.08 if on and t < t_p + i * 0.07 + 0.15 else 1.0))
    if t >= at('experimenta'):
        paste(img, pill('7 DE CADA 10', (236, 50, 90), 54), 540, 1700, scale=pop(t, at('experimenta')))
    return img, 1.0, (540, 960)


def sc_lungs(t):   # Cuando comienzas a dormir, tu respiración se hace más lenta,
    img = holo(t)
    t_r, t_l = at('respiracion'), at('lenta')
    # la respiración se va haciendo lenta: frecuencia 0.9 Hz -> 0.35 Hz
    f = lerp(0.9, 0.35, ease_in_out(prog(t, t_r, t_l + 0.5 - t_r)))
    ph = (t - 19.0) * f * 2 * math.pi if t < t_r else None
    breathe = 0.5 + 0.5 * math.sin(_breath_phase(t))
    s = pop(t, t_r - 0.05)
    if s > 0:
        lx, ly = _poly([(280, 430)])[0]
        paste(img, lungs_sprite(), lx, ly, scale=s * (1.15 + 0.16 * breathe), alpha=0.95)
    if t < t_r:
        paste(img, label('Zzz', 110, fill=(200, 215, 255, 255), stroke=8), 800, 640, scale=pop(t, at('dormir', 2)))
    if t >= t_l:
        paste(img, pill('RESPIRACIÓN  ▼', (40, 120, 240), 52), 540, 1640, scale=pop(t, t_l))
    return img, lerp(1.0, 1.12, ease_in_out(prog(t, t_r, 1.2))), (540, 900)


def _breath_phase(t):
    # integral de la frecuencia (para que la respiración no salte)
    t0 = at('respiracion'); t1 = at('lenta') + 0.5
    acc, step, x = 0.0, 1 / 30, 19.0
    while x < t:
        f = lerp(0.9, 0.35, ease_in_out(clamp((x - t0) / (t1 - t0))))
        acc += 2 * math.pi * f * step; x += step
    return acc


HEART_BEATS = []


def heart_beats():
    if HEART_BEATS: return HEART_BEATS
    t = at('tu', 3) - 0.6
    t_d = at('disminuye'); t_end = at('y', 4) + 0.3
    while t < t_end:
        HEART_BEATS.append(t)
        rate = 1.6 if t < t_d else lerp(1.6, 0.85, clamp((t - t_d) / 0.7))
        t += 1 / rate
    return HEART_BEATS


def sc_heart(t):   # tu ritmo cardíaco disminuye
    img = bg_holo('blue').copy()
    beats = heart_beats()
    last = max([b for b in beats if b <= t] or [-9])
    k = prog(t, last, 0.22)
    s = pop(t, at('tu', 3) - 0.03) * (1 + 0.16 * math.sin(math.pi * k) if k < 1 else 1)
    paste(img, heart_sprite(), 540, 930, scale=1.5 * s)
    ecg(img, t, 0, beats, y=1400)
    if t >= at('disminuye'):
        paste(img, pill('RITMO  ▼', (200, 50, 80), 54), 540, 1650, scale=pop(t, at('disminuye')))
    return img, 1.0, (540, 960)


def sc_muscle_relax(t):   # y tus músculos empiezan a relajarse.
    t_m, t_r = at('musculos'), at('relajarse')
    wv = ease_in_out(prog(t, t_r, 0.9))
    img = muscle_scene(t, wv, 0.0)
    if t < t_r:
        paste(img, pill('TENSO', (200, 50, 80), 50), 540, 1580, scale=pop(t, t_m))
    else:
        paste(img, pill('RELAJADO', (40, 170, 110), 50), 540, 1580, scale=pop(t, t_r))
    return img, lerp(1.06, 1.0, ease_out(prog(t, t_m, 2.0))), (540, 1000)


def sc_transition(t):   # Pero durante esa transición,
    img = bed(t, eyes='closed', zz=0.6)
    t_tr = at('transicion')
    x0, x1, y = 170, 910, 1700
    d = ImageDraw.Draw(img)
    s = pop(t, at('pero', 1))
    if s > 0:
        L = layer(); ld = ImageDraw.Draw(L)
        ld.rounded_rectangle([x0 - 30, y - 110, x1 + 30, y + 70], 40, fill=(12, 16, 45, 210), outline=(160, 180, 255, 255), width=4)
        img.alpha_composite(L)
        d.text((x0, y - 70), 'DESPIERTO', font=font(36, 'x'), fill=(255, 230, 140, 255), anchor='lm')
        d.text((x1, y - 70), 'DORMIDO', font=font(36, 'x'), fill=(180, 200, 255, 255), anchor='rm')
        d.rounded_rectangle([x0, y - 6, x1, y + 22], 14, fill=(60, 70, 130, 255))
        kk = lerp(0.12, 0.5, ease_in_out(prog(t, at('durante'), t_tr + 0.3 - at('durante'))))
        xs = lerp(x0, x1, kk)
        d.rounded_rectangle([x0, y - 6, xs, y + 22], 14, fill=(255, 205, 60, 255))
        d.ellipse([xs - 30, y - 22, xs + 30, y + 38], fill=(255, 255, 255, 255), outline=(255, 205, 60, 255), width=6)
        if t >= t_tr:
            paste(img, alert_badge(36), xs, y - 150, scale=pop(t, t_tr + 0.25))
    return img, 1.0, (540, 960)


def sc_nerves(t, t_on, t_pulse, dur=0.9, txt=None, t_txt=None):
    img = holo(t, brain=pop(t, t_on), nerves=ease_out(prog(t, t_on, 0.3)))
    pulse_dots(img, prog(t, t_pulse, dur))
    if txt and t >= t_txt:
        paste(img, pill(txt, (40, 120, 240), 50), 540, 1700, scale=pop(t, t_txt))
    return img


def sc_nervous(t):   # tu sistema nervioso puede provocar una contracción...
    img = sc_nerves(t, at('sistema', 1), at('provocar'), at('contraccion') - at('provocar'), 'SISTEMA NERVIOSO', at('nervioso', 1))
    return img, lerp(1.0, 1.05, prog(t, at('tu', 4), 2.2)), (540, 1000)


def sc_contract(t):   # contracción muscular repentina.
    t_c, t_r = at('contraccion'), at('repentina')
    sq = math.sin(math.pi * prog(t, t_c, 0.35)) + 1.0 * math.sin(math.pi * prog(t, t_r, 0.3))
    img = muscle_scene(t, 0.15, min(1, sq), glow=min(1, sq))
    if t >= t_r:
        paste(img, label('¡ZAS!', 150, fill=(255, 225, 80, 255), stroke=12), 540, 1580, scale=pop(t, t_r), rot=-8)
        paste(img, alert_badge(), 870, 600, scale=pop(t, t_r + 0.1))
    sh = 1.0 if (t_c < t < t_c + 0.3) or (t_r < t < t_r + 0.35) else 0.0
    return img, 1.0 + 0.05 * min(1, sq), (540 + sh * 14 * math.sin(t * 90), 1000)


def sc_curious(t):   # Y aquí viene lo curioso.
    img = bg_purple().copy()
    float_bubbles(img, t, n=10, seed=8, rmin=16, rmax=44, area=(20, 520, W - 20, 1700), speed=60, alpha=0.6)
    t_c = at('curioso')
    paste(img, label('?', 420, fill=(255, 215, 60, 255), stroke=16), 540, 1000 + 20 * math.sin(t * 4), scale=pop(t, at('y', 5)), rot=8 * math.sin(t * 3))
    if t >= t_c:
        for i, (x, y) in enumerate(((260, 760), (820, 820), (300, 1260), (800, 1240))):
            sparkle(img, x, y, 34 * pop(t, t_c + i * 0.06), 1.0)
        paste(img, follow_button(), 540, 1580, scale=pop(t, t_c + 0.1) * (1 + 0.04 * math.sin(t * 8)))
    return img, 1.0, (540, 960)


def sc_theory(t):   # Una de las teorías
    img = bg_teal().copy()
    t_t = at('teorias')
    paste(img, brain_sprite(), 540, 980 + 10 * math.sin(t * 3), scale=1.6 * pop(t, at('una', 2)))
    if t >= t_t:
        paste(img, pill('TEORÍA', (236, 50, 90), 70), 540, 1350, scale=pop(t, t_t))
        sparkle(img, 760, 760, 40 * pop(t, t_t), 1.0)
    return img, 1.0, (540, 960)


def sc_brain_reads(t):   # sugiere que tu cerebro podría interpretar esa relajación muscular
    t_c, t_i, t_r = at('cerebro'), at('interpretar'), at('relajacion')
    img = holo(t, brain=pop(t, t_c) * (1 + 0.25 * math.sin(math.pi * prog(t, t_c, 0.3))), nerves=0.5)
    # ondas suben desde las piernas al cerebro
    if t >= t_r:
        k = (t - t_r) * 0.9
        sp, al, ar, ll, lr = nerve_paths()
        rev = [p[::-1] for p in (ll, lr)] + [sp[::-1]]
        for j in range(3):
            pulse_dots(img, ((k + j * 0.33) % 1.0), [ll[::-1] + sp[::-1][14:], lr[::-1] + sp[::-1][14:]], col=(140, 255, 190))
        paste(img, pill('RELAJACIÓN', (40, 170, 110), 50), 540, 1700, scale=pop(t, t_r))
    if t >= t_i:
        bx, by = _poly([HB_BRAIN])[0]
        paste(img, label('?', 160, fill=(255, 225, 80, 255), stroke=10), bx + 180, by - 60, scale=pop(t, t_i), rot=12 * math.sin(t * 5))
    return img, lerp(1.0, 1.08, ease_in_out(prog(t, t_c - 0.3, 1.0))), (540, 760)


def sc_brain_fall(t):   # como una sensación de caída,
    t_s, t_c = at('sensacion'), at('caida')
    img = bg_holo('red' if t >= t_c else 'blue').copy()
    if t >= t_c:
        g = layer(); ImageDraw.Draw(g).rectangle([0, 0, W, H], fill=(255, 40, 70, int(90 * (1 - prog(t, t_c, 0.6)) + 30)))
        img.alpha_composite(g)
    shk = 12 * math.sin(t * 80) if t >= t_c else 0
    paste(img, brain_sprite(), 540 + shk, 900, scale=1.7 * pop(t, at('como') - 0.02))
    if t >= t_s and t < t_c:
        paste(img, label('...', 140, stroke=10), 760, 700, scale=pop(t, t_s))
    if t >= t_c:
        paste(img, label('¡CAÍDA!', 150, fill=(255, 90, 100, 255), stroke=12), 540, 1330, scale=pop(t, t_c), rot=-5)
        big_arrow(img, 540, 1600, pop(t, t_c + 0.1) * 0.7, up=False, col=(255, 70, 90))
        paste(img, alert_badge(), 800, 700, scale=pop(t, t_c + 0.05))
    return img, 1.0 + 0.06 * ease_out(prog(t, t_c, 0.3)), (540, 960)


def sc_scientists(t):   # aunque los científicos todavía no conocen la causa exacta.
    img = bg_purple().copy()
    t_c, t_x = at('cientificos'), at('causa')
    look = (math.sin(t * 2.5), 0)
    paste(img, P(shirt=(245, 245, 250), hair=(60, 60, 70), hair_style='curly', skin=(200, 150, 110), brows='worried', mouth='wobble', look=look),
          290, 1480, scale=0.6 * pop(t, t_c - 0.02), anchor='b')
    paste(img, P(shirt=(245, 245, 250), hair=(150, 90, 40), hair_style='long', skin=(241, 194, 160), brows='raised', mouth='side', look=(-look[0], 0)),
          790, 1480, scale=0.6 * pop(t, t_c + 0.08), anchor='b')
    if t >= at('todavia'):
        for i, x in enumerate((290, 790)):
            paste(img, label('?', 150, fill=(255, 225, 80, 255), stroke=10), x, 780 + 12 * math.sin(t * 5 + i), scale=pop(t, at('todavia') + 0.1 * i))
    if t >= t_x:
        paste(img, pill('CAUSA EXACTA: ???', (236, 50, 90), 56), 540, 1640, scale=pop(t, t_x), rot=-3)
    return img, 1.0, (540, 960)


def sc_trip(t):   # Por eso puedes sentir que tropiezas,
    img = bg_void(1).copy()
    t_t = at('tropiezas')
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1330, W, H], fill=(40, 60, 120, 255)); d.line([(0, 1330), (W, 1330)], fill=(120, 160, 255, 255), width=6)
    x = lerp(160, 520, prog(t, at('por', 1), t_t - at('por', 1))) if t < t_t else 520
    k = ease_out(prog(t, t_t, 0.4))
    paste(img, rock_sprite(), 690, 1290)
    p = P(mouth='o' if t >= t_t else 'smile', eyes='wide' if t >= t_t else 'open', brows='raised' if t >= t_t else 'normal',
          shirt=PJ, skin=SKIN, hair=HAIR, sweat=t >= t_t)
    paste(img, p, x + 180 * k, 1340 + 40 * k, scale=0.5, rot=-55 * k, anchor='b')
    if t >= t_t:
        paste(img, label('¡UPS!', 120, fill=(255, 225, 80, 255), stroke=10), 760, 860, scale=pop(t, t_t + 0.1), rot=-10)
    img.alpha_composite(dream_frame())
    return img, 1.0, (540, 960)


def sc_stairs(t):   # caes por unas escaleras
    img = bg_void(1).copy()
    img.alpha_composite(stairs_layer())
    t0 = at('caes', 2)
    k = prog(t, t0, at('o', 1) - t0)
    # rebota escalón por escalón
    step = k * 5.0
    i = int(step); f = step - i
    x = 200 + step * 140; y = 760 + i * 130 - 120 * math.sin(math.pi * f)
    p = P(mouth='o', eyes='wide', brows='raised', shirt=PJ, skin=SKIN, hair=HAIR, sweat=True, cheeks=0.6)
    paste(img, p, x, y, scale=0.38, rot=-200 * k, anchor='b')
    img.alpha_composite(dream_frame())
    return img, 1.0, (540, 960)


def sc_fall2(t):   # o incluso te precipitas al vacío.
    return sc_fall(t, at('precipitas'), 1, '¡AAAH!', at('vacio', 2))


def sc_calm(t):   # Y todo sucede mientras estás acostado tranquilamente en tu cama.
    img = bed(t, eyes='closed', mouth='smile', zz=1.0)
    t_c = at('cama', 1)
    if t >= at('acostado'):
        paste(img, pill('EN TU CAMA', (40, 120, 240), 54), 540, 1700, scale=pop(t, at('acostado')))
    if t >= t_c:
        paste(img, check_badge(46, True), 800, 820, scale=pop(t, t_c))
    return img, lerp(1.08, 1.0, ease_out(prog(t, at('y', 6), 3.0))), (540, 1000)


def sc_factors(t):   # Además, el estrés, la cafeína y la falta de sueño
    img = bg_teal().copy()
    items = ((storm_sprite(), at('estres'), 'ESTRÉS', 300, 800), (coffee_sprite(), at('cafeina'), 'CAFEÍNA', 780, 800),
             (battery_sprite(), at('falta'), 'POCO SUEÑO', 540, 1290))
    paste(img, pill('ADEMÁS', (236, 50, 90), 52), 540, 560, scale=pop(t, at('ademas')))
    for spr, t0, txt, x, y in items:
        s = pop(t, t0)
        if s <= 0: continue
        paste(img, spr, x, y + 8 * math.sin(t * 4 + x), scale=s * 0.95)
        paste(img, label(txt, 62, stroke=7), x, y + 220, scale=s)
    return img, 1.0, (540, 960)


def sc_more(t):   # pueden hacer que estas sacudidas sean más frecuentes.
    img = bg_purple().copy()
    bars(img, t, at('pueden'), 1.0)
    t_f = at('frecuentes')
    if t >= t_f:
        big_arrow(img, 870, 900, pop(t, t_f) * 0.9, up=True)
        paste(img, pill('MÁS FRECUENTES', (40, 170, 110), 56), 540, 1660, scale=pop(t, t_f))
    return img, 1.0, (540, 960)


def sc_normal(t):   # Pero tranquilo, generalmente son completamente normales.
    img = bg_teal().copy()
    float_bubbles(img, t, n=8, seed=12, rmin=14, rmax=40, area=(0, 500, W, 1700), speed=40, alpha=0.5)
    t_n = at('normales')
    paste(img, P(mouth='smile', shirt=PJ, skin=SKIN, hair=HAIR, cheeks=0.5, arms='down'), 540, 1700, scale=0.85 * pop(t, at('pero', 2)), anchor='b')
    if t >= t_n:
        paste(img, check_badge(70, True), 820, 760, scale=pop(t, t_n))
        paste(img, pill('ES NORMAL', (40, 170, 110), 64), 540, 640, scale=pop(t, t_n + 0.05))
        for i, (x, y) in enumerate(((200, 800), (880, 1100), (230, 1250))):
            sparkle(img, x, y, 36 * pop(t, t_n + 0.08 * i))
    return img, 1.0, (540, 1000)


def sc_next(t):   # Así que la próxima vez que estés a punto de dormir
    t_d = at('dormir', 3)
    eyes = 'open' if t < at('punto', 2) else 'closed'
    img = bed(t, eyes=eyes, zz=ease_out(prog(t, t_d, 0.5)))
    return img, lerp(1.0, 1.1, ease_in_out(prog(t, at('asi'), 2.5))), (540, 1000)


def sc_jump2(t):   # y tu cuerpo dé un salto inesperado,
    return sc_jump(t, at('salto', 2), badge_t=at('inesperado'))


def sc_remember(t):   # recuerda esto:
    img = bg_purple().copy()
    t_r = at('recuerda')
    paste(img, brain_sprite(), 540, 1000, scale=1.5 * pop(t, t_r))
    paste(img, pill('RECUERDA', (236, 50, 90), 72), 540, 1350, scale=pop(t, at('esto')))
    for i, (x, y) in enumerate(((280, 800), (800, 780))):
        sparkle(img, x, y, 40 * pop(t, at('esto') + 0.08 * i))
    return img, 1.0 + 0.1 * ease_out(prog(t, t_r, 1.2)), (540, 1050)


def sc_nofall(t):   # No te estabas cayendo de la cama.
    img = bed(t, eyes='closed', mouth='smile', zz=0.7)
    t_c = at('cayendo')
    big_arrow(img, 540, 1450, pop(t, at('no', 2)) * 0.8, up=False, col=(255, 170, 60))
    if t >= t_c:
        cross(img, 540, 1450, pop(t, t_c) * 1.0)
        paste(img, pill('NO TE CAÍSTE', (200, 50, 80), 58), 540, 1740, scale=pop(t, at('cama', 2)))
    return img, 1.0, (540, 960)


def sc_gift(t):   # Tu sistema nervioso simplemente te regaló
    t_g = at('regalo')
    img = sc_nerves(t, at('sistema', 2) - 0.05, at('nervioso', 2), 0.8)
    if t >= t_g:
        paste(img, gift_sprite(), 790, 760, scale=pop(t, t_g) * 0.9, rot=8 * math.sin(t * 6))
    return img, 1.0, (540, 960)


def sc_coaster(t):   # una montaña rusa sin moverte de la almohada.
    img = bg_bed().copy()
    t_m, t_a = at('montana'), at('almohada')
    # almohada gigante abajo
    paste(img, pillow_sprite(), 540, 1500 + 20 * math.sin(t * 2), scale=1.6 * pop(t, at('sin')) if t >= at('sin') else 0)
    k = ease_out(prog(t, at('una', 4) - 0.05, 0.6))
    pts = coaster_track(k)
    d = ImageDraw.Draw(img)
    L = layer(); ImageDraw.Draw(L).line(pts, fill=(255, 210, 90, 140), width=40, joint='curve')
    img.alpha_composite(blur(L, 14))
    d.line(pts, fill=(255, 205, 60, 255), width=18, joint='curve')
    d.line([(x, y + 14) for x, y in pts], fill=(200, 130, 40, 255), width=6, joint='curve')
    for i in range(0, len(pts) - 1, 12):
        x, y = pts[i]; d.line([(x, y + 10), (x, min(H, y + 180))], fill=(150, 120, 200, 160), width=6)
    # carrito con el personaje
    if t >= t_m:
        full = coaster_track(1.0)
        u = ease_in_out(prog(t, t_m, t_a + 0.5 - t_m))
        i = min(len(full) - 2, int(u * (len(full) - 1)))
        (x, y), (x2, y2) = full[i], full[i + 1]
        ang = -math.degrees(math.atan2(y2 - y, x2 - x))
        cart = _cart()
        p = face('wide' if u < 0.8 else 'open', 'smile', 'raised', cheeks=0.7)
        paste(img, p, x, y - 120, scale=0.42, rot=ang * 0.5)
        paste(img, cart, x, y - 40, rot=ang)
        if u > 0.05:
            paste(img, label('¡WIII!', 96, fill=(255, 225, 80, 255), stroke=9), clamp(x, 220, 860), y - 300, scale=pop(t, t_m + 0.2))
    if t >= t_a:
        paste(img, check_badge(50, True), 820, 1380, scale=pop(t, t_a))
    return img, 1.0, (540, 960)


def sc_end(t):   # ...de la almohada.  (vuelve a la cama: empalma con el inicio)
    t_a = at('almohada')
    img = bed(t, eyes='closed', mouth='smile', zz=1.0)
    paste(img, check_badge(50, True), 800, 820, scale=pop(t, t_a + 0.15))
    paste(img, label('¡WIII!', 80, fill=(255, 225, 80, 255), stroke=8), 300, 760, scale=pop(t, t_a), alpha=1 - prog(t, t_a + 0.6, 0.3), rot=-10)
    return img, 1.0 + 0.04 * (1 - ease_out(prog(t, t_a, 0.5))), (540, 1000)


@lru_cache(maxsize=1)
def _cart():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, 260 * s, 110 * s], 30 * s, fill=(236, 50, 90, 255), outline=(255, 200, 210, 255), width=5 * s)
        for x in (60, 200):
            d.ellipse([(x - 26) * s, 90 * s, (x + 26) * s, 142 * s], fill=(40, 40, 60, 255), outline=(220, 220, 240, 255), width=4 * s)
    return ss_sprite(260, 145, fn)


# ==================================================================== línea de tiempo
def _cut(word, k=1, pre=0.06):
    return at(word, k) - pre


SCENES = [
    (0.0, sc_hook),
    (_cut('sientes'), sc_fall1),
    (_cut('y', 2), sc_jump1),
    (_cut('lo', 1), sc_still),
    (_cut('este'), sc_name),
    (_cut('y', 3), sc_stat),
    (_cut('cuando'), sc_lungs),
    (_cut('tu', 3), sc_heart),
    (_cut('y', 4), sc_muscle_relax),
    (_cut('pero', 1), sc_transition),
    (_cut('tu', 4), sc_nervous),
    (_cut('contraccion'), sc_contract),
    (_cut('y', 5), sc_curious),
    (_cut('una', 2), sc_theory),
    (_cut('sugiere'), sc_brain_reads),
    (_cut('como'), sc_brain_fall),
    (_cut('aunque'), sc_scientists),
    (_cut('por', 1), sc_trip),
    (_cut('caes', 2), sc_stairs),
    (_cut('o', 1), sc_fall2),
    (_cut('y', 6), sc_calm),
    (_cut('ademas'), sc_factors),
    (_cut('pueden'), sc_more),
    (_cut('pero', 2), sc_normal),
    (_cut('asi'), sc_next),
    (_cut('y', 8), sc_jump2),
    (_cut('recuerda'), sc_remember),
    (_cut('no', 2), sc_nofall),
    (_cut('tu', 8), sc_gift),
    (_cut('una', 4), sc_coaster),
    (_cut('almohada'), sc_end),
]
CUTS = [s for s, _ in SCENES[1:]]


def scene_at(t):
    cur = SCENES[0]
    for s in SCENES:
        if t >= s[0]: cur = s
    return cur


# ==================================================================== efectos sincronizados
def build_sfx():
    SFX.clear()
    for c in CUTS:
        sfx(c - 0.12, 'whoosh', -10, dur=0.3)
    # hook
    sfx(at('dormir', 1), 'snore', -16, dur=0.9)
    sfx(at('repente'), 'impact', -6); sfx(at('repente') + 0.02, 'pop', -8)
    # caída
    sfx(at('caes', 1), 'whoosh_down', -5, dur=1.2); sfx(at('vacio', 1), 'pop', -8)
    # salto 1
    sfx(at('salto', 1), 'boing', -4); sfx(at('salto', 1) + 0.5, 'thump', -6); sfx(at('involuntario'), 'pop', -9)
    # quieto
    for i in range(3): sfx(at('siquiera') + i * 0.12, 'pop', -12)
    sfx(at('extrano'), 'bloop', -8); sfx(at('moviendo'), 'buzz', -10); sfx(at('moviendo') + 0.15, 'pop', -10)
    # nombre
    sfx(at('fenomeno'), 'pop', -9); sfx(at('sacudida', 1), 'glitch', -6); sfx(at('sacudida', 1) + 0.02, 'impact', -7)
    sfx(at('hipnica'), 'pop', -7)
    # 70 %
    sfx(at('hasta'), 'pop', -9)
    t_h, t_70 = at('hasta'), at('70%') + 0.35
    n = 14
    for i in range(n): sfx(t_h + (t_70 - t_h) * i / n, 'tick', -13)
    sfx(t_70, 'ding', -9)
    for i in range(7): sfx(at('personas') + i * 0.07, 'pop', -13)
    sfx(at('experimenta'), 'pop', -9)
    # pulmones
    sfx(at('respiracion') - 0.05, 'bloop', -9); sfx(at('respiracion') + 0.3, 'exhale', -13, dur=1.2)
    sfx(at('lenta'), 'pop', -9)
    # corazón (cada latido)
    for b in heart_beats():
        if _cut('tu', 3) <= b < _cut('y', 4): sfx(b, 'thump', -8)
    sfx(at('disminuye'), 'pop', -10)
    # músculos
    sfx(at('musculos'), 'pop', -10); sfx(at('relajarse'), 'exhale', -11, dur=0.9); sfx(at('relajarse') + 0.02, 'pop', -11)
    # transición
    sfx(at('durante'), 'sweep', -14, dur=0.8); sfx(at('transicion') + 0.25, 'pop', -9)
    # nervios
    sfx(at('nervioso', 1), 'pop', -9); sfx(at('provocar'), 'zap', -9, dur=at('contraccion') - at('provocar'))
    sfx(at('contraccion'), 'squeeze', -5); sfx(at('contraccion'), 'impact', -9)
    sfx(at('repentina'), 'impact', -5); sfx(at('repentina') + 0.1, 'pop', -9)
    # curioso
    sfx(at('y', 5), 'bloop', -7); sfx(at('curioso'), 'sparkle', -10); sfx(at('curioso') + 0.1, 'click', -9)
    # teoría
    sfx(at('una', 2), 'pop', -9); sfx(at('teorias'), 'ding', -11)
    # cerebro
    sfx(at('cerebro'), 'bloop', -7); sfx(at('interpretar'), 'pop', -9)
    sfx(at('relajacion'), 'scan', -14, dur=1.0)
    # caída del cerebro
    sfx(at('como'), 'pop', -10); sfx(at('sensacion'), 'beep', -14)
    sfx(at('caida'), 'buzz', -8); sfx(at('caida'), 'whoosh_down', -9, dur=0.5); sfx(at('caida') + 0.05, 'impact', -10)
    # científicos
    sfx(at('cientificos'), 'pop', -10); sfx(at('cientificos') + 0.1, 'pop', -11)
    sfx(at('todavia') + 0.05, 'bloop', -10); sfx(at('causa'), 'buzz', -12); sfx(at('causa') + 0.02, 'pop', -9)
    # tropiezo
    sfx(at('por', 1) + 0.1, 'steps', -12, dur=at('tropiezas') - at('por', 1) - 0.1)
    sfx(at('tropiezas'), 'thump', -5); sfx(at('tropiezas') + 0.1, 'boing', -9)
    # escaleras: un golpe por escalón
    t0 = at('caes', 2); dur = at('o', 1) - t0
    for i in range(1, 6): sfx(t0 + dur * i / 5.0, 'thump', -8)
    # vacío 2
    sfx(at('precipitas'), 'whoosh_down', -5, dur=1.2); sfx(at('vacio', 2), 'pop', -9)
    # calma
    sfx(at('tranquilamente'), 'snore', -15, dur=1.1); sfx(at('acostado'), 'pop', -10); sfx(at('cama', 1), 'ding', -9)
    # factores
    sfx(at('ademas'), 'pop', -9); sfx(at('estres'), 'thunder', -8); sfx(at('cafeina'), 'pop', -7); sfx(at('cafeina') + 0.05, 'glu', -10)
    sfx(at('falta'), 'powerdown', -9)
    # más frecuentes
    for i in range(4): sfx(at('pueden') + i * 0.22, 'pop', -10)
    sfx(at('frecuentes'), 'rise', -11, dur=0.5); sfx(at('frecuentes') + 0.02, 'pop', -9)
    # normal
    sfx(at('pero', 2), 'bloop', -9); sfx(at('normales'), 'ding', -6); sfx(at('normales') + 0.08, 'sparkle', -11)
    # próxima vez
    sfx(at('dormir', 3), 'snore', -16, dur=0.9)
    sfx(at('salto', 2), 'boing', -4); sfx(at('salto', 2) + 0.5, 'thump', -6); sfx(at('inesperado'), 'pop', -9)
    # recuerda
    sfx(at('recuerda'), 'bloop', -8); sfx(at('esto'), 'pop', -8); sfx(at('esto') + 0.05, 'sparkle', -12)
    # no te caíste
    sfx(at('no', 2), 'pop', -10); sfx(at('cayendo'), 'buzz', -10); sfx(at('cayendo') + 0.02, 'pop', -9); sfx(at('cama', 2), 'pop', -10)
    # regalo + montaña rusa
    sfx(at('nervioso', 2), 'zap', -11, dur=0.8); sfx(at('regalo'), 'pop', -6); sfx(at('regalo') + 0.03, 'sparkle', -11)
    sfx(at('una', 4), 'click', -10)
    for i in range(6): sfx(at('una', 4) + 0.05 + i * 0.07, 'tick', -15)
    sfx(at('montana'), 'whoosh', -8, dur=0.9); sfx(at('montana') + 0.25, 'pop', -11)
    sfx(at('rusa') + 0.1, 'whoosh_down', -10, dur=0.7)
    sfx(at('sin'), 'bloop', -9); sfx(at('almohada'), 'ding', -8)
    return SFX
