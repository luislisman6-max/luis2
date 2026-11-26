"""Escenas del video «Tu nariz desaparece». Todos los tiempos salen de words.json (palabra exacta),
así animación, efectos y subtítulos usan el mismo reloj."""
import json, math, os, random, sys, unicodedata
from functools import lru_cache
from PIL import Image, ImageDraw, ImageChops, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from lib import *          # noqa
from art import *          # noqa
from scenes import brain_sprite, follow_button, label, pill, sparkle, float_bubbles, glitch, puff_sprite, device_sprite  # noqa

WORDS = json.load(open(os.path.join(HERE, 'words.json')))


def _n(w):
    w = unicodedata.normalize('NFD', w.lower())
    return ''.join(c for c in w if unicodedata.category(c) != 'Mn' and c.isalnum())


def T(word, approx):
    """inicio (s) de la aparición de `word` más cercana a `approx` (s)"""
    c = [w['s'] for w in WORDS if _n(w['w']) == _n(word)]
    if not c: raise KeyError(word)
    best = min(c, key=lambda s: abs(s - approx))
    assert abs(best - approx) < 1.0, (word, approx, best)
    return best


def TE(word, approx):
    c = [w for w in WORDS if _n(w['w']) == _n(word)]
    return min(c, key=lambda w: abs(w['s'] - approx))['e']


SFX = []


def sfx(t, name, g=0.0, **kw):
    SFX.append((t, name, g, kw))


# ==================================================================== arte
SKIN = (241, 194, 160)
SKIN_D = (214, 158, 126)
HAIR = (60, 38, 26)
SHIRT = (236, 92, 70)
YEL = (255, 225, 80, 255)


# ---- vista en primera persona (POV): parque + nariz borrosa abajo al centro
@lru_cache(maxsize=1)
def pov_bg():
    img = vgrad((W, H), rgba('#7cc8ff'), rgba('#d8f0ff'))
    d = ImageDraw.Draw(img)
    g = layer(); ImageDraw.Draw(g).ellipse([700, 420, 1000, 720], fill=(255, 250, 200, 200))
    img.alpha_composite(blur(g, 60))
    d.ellipse([790, 510, 910, 630], fill=(255, 248, 205, 255))
    for (x, y, s) in ((180, 640, 1.0), (560, 560, 0.8)):
        for dx, dy, r in ((0, 0, 60), (60, -20, 70), (120, 0, 55), (60, 20, 60)):
            d.ellipse([x + dx * s - r * s, y + dy * s - r * s, x + dx * s + r * s, y + dy * s + r * s], fill=(255, 255, 255, 235))
    # colinas
    d.polygon([(0, 1150)] + [(x, 1080 - 90 * math.sin(x / 300)) for x in range(0, W + 20, 20)] + [(W, 1300), (0, 1300)], fill=rgba('#7fcf7a'))
    d.rectangle([0, 1180, W, H], fill=rgba('#5fb85e'))
    d.polygon([(0, 1240)] + [(x, 1200 - 40 * math.sin(x / 170 + 1)) for x in range(0, W + 20, 20)] + [(W, H), (0, H)], fill=rgba('#4fa64f'))
    # arbustos
    for (x, y, r) in ((620, 1215, 60), (690, 1225, 48), (60, 1290, 70)):
        d.ellipse([x - r, y - r * 0.8, x + r, y + r * 0.8], fill=rgba('#3f9a4c'))
    # árboles
    for (x, y, s) in ((140, 1120, 1.0), (930, 1100, 1.15), (330, 1160, 0.7)):
        d.rectangle([x - 18 * s, y - 40 * s, x + 18 * s, y + 120 * s], fill=rgba('#8a5a34'))
        for dx, dy, r in ((0, -150, 110), (-70, -90, 85), (70, -90, 85)):
            d.ellipse([x + (dx - r) * s, y + (dy - r) * s, x + (dx + r) * s, y + (dy + r) * s], fill=rgba('#2f8f46'))
        d.ellipse([x - 60 * s, y - 230 * s, x + 10 * s, y - 170 * s], fill=rgba('#49ad5d'))
    # flores
    rnd = random.Random(7)
    for _ in range(40):
        x, y = rnd.randint(0, W), rnd.randint(1260, H)
        c = rnd.choice(((255, 120, 150), (255, 230, 90), (255, 255, 255)))
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=c + (255,))
    return img


@lru_cache(maxsize=1)
def nose_pov_layer():
    """la nariz como la ves tú: una mancha borrosa abajo al centro (cada ojo ve un lado)."""
    L = layer(); d = ImageDraw.Draw(L)
    col = (238, 168, 140, 255)
    pts = [(540, 1060)]
    for i in range(41):
        u = i / 40
        pts.append((540 + 280 * u ** 0.75, 1060 + 900 * u))
    pts += [(540 - 280 * (i / 40) ** 0.75, 1060 + 900 * (i / 40)) for i in range(40, -1, -1)]
    d.polygon(pts, fill=col)
    out = blur(L, 34)
    # sombra lateral (cada ojo ve un costado)
    S = layer(); sd = ImageDraw.Draw(S)
    sd.ellipse([300, 1300, 470, 1980], fill=(170, 110, 90, 140)); sd.ellipse([610, 1300, 780, 1980], fill=(170, 110, 90, 140))
    out.alpha_composite(blur(S, 50))
    H_ = layer(); ImageDraw.Draw(H_).ellipse([500, 1200, 590, 1700], fill=(255, 225, 205, 120))
    out.alpha_composite(blur(H_, 30))
    return out


@lru_cache(maxsize=1)
def eye_edge():
    """oscurecimiento borroso de los bordes (como mirar desde dentro de la cabeza)"""
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    d.ellipse([-200, 260, W + 200, H + 380], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(90))
    L = Image.new('RGBA', (W, H), (40, 20, 30, 255))
    L.putalpha(Image.eval(m, lambda v: int((255 - v) * 0.85)))
    return L


def nose_outline(img, t, k):
    """círculo rojo punteado que gira alrededor de la nariz"""
    if k <= 0: return
    d = ImageDraw.Draw(img)
    cx, cy, rx, ry = 540, 1560, 330 * k, 400 * k
    n = 28
    for i in range(n):
        if i % 2: continue
        a0 = i / n * 2 * math.pi + t * 1.5; a1 = a0 + 2 * math.pi / n
        d.line([(cx + rx * math.cos(a0), cy + ry * math.sin(a0)), (cx + rx * math.cos(a1), cy + ry * math.sin(a1))], fill=(255, 50, 70, 255), width=14)


def pov(t, nose=0.55, glow=0.0, ring=0.0, sway=True):
    img = pov_bg().copy()
    if glow > 0:
        g = layer(); gd = ImageDraw.Draw(g)
        gd.ellipse([240, 1060, 840, 2000], fill=(255, 220, 90, int(150 * glow)))
        img.alpha_composite(blur(g, 60))
    paste(img, nose_pov_layer(), 540, 960, alpha=nose)
    img.alpha_composite(eye_edge())
    nose_outline(img, t, ring)
    return img


def mini_pov(w, h, shift=0, nose_side=0, nose_a=0.0):
    """miniatura de lo que ve un ojo. nose_side -1 (nariz a la izquierda) / 1 (a la derecha)"""
    big = pov_bg().crop((60 + shift, 380, 60 + shift + 960, 380 + int(960 * h / w))).resize((w, h), Image.BILINEAR)
    if nose_a > 0 and nose_side:
        L = layer(w, h); d = ImageDraw.Draw(L)
        x = w if nose_side > 0 else 0
        d.ellipse([x - w * 0.32, h * 0.45, x + w * 0.32, h * 1.5], fill=(232, 176, 146, int(255 * nose_a)))
        big.alpha_composite(blur(L, 14))
    return big


# ---- personaje con nariz grande
NOSE_C = (320, 292)     # centro de la nariz en coordenadas del sprite del personaje (640x980)


@lru_cache(maxsize=4)
def nose_sprite(glow=False):
    def fn(im, s):
        d = ImageDraw.Draw(im)
        if glow:
            L = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(L).ellipse([20 * s, 20 * s, 140 * s, 150 * s], fill=(255, 220, 80, 150))
            im.alpha_composite(blur(L, 12 * s)); d = ImageDraw.Draw(im)
        d.polygon([(80 * s, 20 * s), (55 * s, 95 * s), (105 * s, 95 * s)], fill=SKIN_D + (255,))
        d.ellipse([34 * s, 74 * s, 126 * s, 138 * s], fill=SKIN_D + (255,))
        d.polygon([(80 * s, 16 * s), (60 * s, 90 * s), (100 * s, 90 * s)], fill=(230, 176, 142, 255))
        d.ellipse([40 * s, 70 * s, 120 * s, 130 * s], fill=(230, 176, 142, 255))
        d.ellipse([60 * s, 104 * s, 74 * s, 116 * s], fill=(150, 80, 70, 255))
        d.ellipse([86 * s, 104 * s, 100 * s, 116 * s], fill=(150, 80, 70, 255))
        d.ellipse([54 * s, 78 * s, 78 * s, 94 * s], fill=(255, 225, 205, 230))
    return ss_sprite(160, 170, fn)


_hc = {}


def hero(eyes='open', mouth='flat', brows='normal', sweat=False, cheeks=0.4, look=(0, 0), cross=0.0, arms='down', shirt=SHIRT, body=True):
    """personaje sin nariz (la nariz se pega aparte con hero_nose)."""
    key = (eyes, mouth, brows, sweat, cheeks, look, round(cross, 2), arms, shirt, body)
    if key in _hc: return _hc[key]
    if len(_hc) > 80: _hc.clear()
    im = person(skin=SKIN, hair=HAIR, shirt=shirt, eyes='wide' if cross > 0 else eyes, look=look, mouth=mouth, cheeks=cheeks,
                sweat=sweat, arms=arms, brows=brows, body=body, res=2)
    d = ImageDraw.Draw(im); s = 2
    def B(x0, y0, x1, y1): return [x0 * s, y0 * s, x1 * s, y1 * s]
    d.ellipse(B(298, 288, 342, 327), fill=SKIN + (255,))     # tapa la nariz pequeña
    if cross > 0:
        for x, side in ((255, 1), (385, -1)):
            d.ellipse(B(x - 38, 214, x + 38, 310), fill=(255, 255, 255, 255), outline=(90, 60, 50, 255), width=3 * s)
            px, py = x + side * 17 * cross, 266 + 22 * cross
            d.ellipse(B(px - 20, py - 20, px + 20, py + 20), fill=(85, 55, 35, 255))
            d.ellipse(B(px - 10, py - 10, px + 10, py + 10), fill=(20, 12, 10, 255))
            d.ellipse(B(px - 12, py - 14, px - 3, py - 5), fill=(255, 255, 255, 255))
    im = im.resize((PW, PH), Image.LANCZOS)
    _hc[key] = im
    return im


def put_hero(img, spr, cx, cy, sc, nose=1.0, nose_scale=1.0, nose_glow=False, rot=0.0):
    paste(img, spr, cx, cy, scale=sc, rot=rot)
    nx = cx + (NOSE_C[0] - PW / 2) * sc; ny = cy + (NOSE_C[1] - PH / 2) * sc
    if nose > 0.01:
        paste(img, nose_sprite(nose_glow), nx, ny, scale=sc * nose_scale, alpha=nose)
    return nx, ny


# ---- iconos
@lru_cache(maxsize=4)
def eyeball(r=150, iris=(70, 140, 220)):
    def fn(im, s):
        c = (r + 20) * s; rr = r * s
        d = ImageDraw.Draw(im)
        d.ellipse([c - rr, c - rr, c + rr, c + rr], fill=(255, 255, 255, 255), outline=(60, 40, 60, 255), width=6 * s)
        L = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(L).ellipse([c - rr, c + rr * 0.1, c + rr, c + rr * 1.3], fill=(200, 200, 230, 120))
        m = Image.new('L', im.size, 0); ImageDraw.Draw(m).ellipse([c - rr + 6 * s, c - rr + 6 * s, c + rr - 6 * s, c + rr - 6 * s], fill=255)
        tt = Image.new('RGBA', im.size, (0, 0, 0, 0)); tt.paste(blur(L, 10 * s), (0, 0), m); im.alpha_composite(tt); d = ImageDraw.Draw(im)
        ir = rr * 0.5
        d.ellipse([c - ir, c - ir, c + ir, c + ir], fill=iris + (255,))
        d.ellipse([c - ir * 0.75, c - ir * 0.75, c + ir * 0.75, c + ir * 0.75], outline=tuple(min(255, v + 60) for v in iris) + (255,), width=4 * s)
        d.ellipse([c - ir * 0.5, c - ir * 0.5, c + ir * 0.5, c + ir * 0.5], fill=(15, 10, 20, 255))
        d.ellipse([c - ir * 0.55, c - ir * 0.6, c - ir * 0.1, c - ir * 0.15], fill=(255, 255, 255, 240))
    return ss_sprite(2 * (r + 20), 2 * (r + 20), fn)


def eye_with_lid(img, cx, cy, r, lid, look=(0, 0)):
    """ojo grande con párpado. lid 0 abierto .. 1 cerrado"""
    e = eyeball(r)
    big = layer(e.width, e.height)
    paste(big, e, e.width / 2 + look[0] * r * 0.2, e.height / 2 + look[1] * r * 0.2)
    m = Image.new('L', big.size, 0); c = e.width / 2
    ImageDraw.Draw(m).ellipse([c - r, c - r, c + r, c + r], fill=255)
    out = layer(e.width, e.height); out.paste(big, (0, 0), m)
    d = ImageDraw.Draw(out)
    if lid > 0.01:
        y = c - r + 2 * r * lid
        lm = Image.new('L', big.size, 0); ImageDraw.Draw(lm).rectangle([0, 0, e.width, y], fill=255)
        lm = ImageChops.multiply(lm, m)
        sk = Image.new('RGBA', big.size, SKIN + (255,)); out.paste(sk, (0, 0), lm)
        d.arc([c - r, y - 30 * lid, c + r, y + 30 * lid], 0, 180, fill=(70, 40, 30, 255), width=10)
        for k in range(-3, 4):      # pestañas
            x = c + k * r * 0.25
            d.line([(x, y + 18 * lid), (x + k * 6, y + 18 * lid + 34)], fill=(50, 30, 25, 255), width=7)
    ImageDraw.Draw(out).ellipse([c - r, c - r, c + r, c + r], outline=(60, 40, 60, 255), width=6)
    paste(img, out, cx, cy)


@lru_cache(maxsize=2)
def bulb_sprite():
    def fn(im, s):
        L = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(L).ellipse([10 * s, 10 * s, 250 * s, 250 * s], fill=(255, 230, 80, 170))
        im.alpha_composite(blur(L, 24 * s)); d = ImageDraw.Draw(im)
        d.ellipse([50 * s, 40 * s, 210 * s, 200 * s], fill=(255, 232, 90, 255), outline=(255, 250, 210, 255), width=5 * s)
        d.rounded_rectangle([95 * s, 190 * s, 165 * s, 250 * s], 10 * s, fill=(170, 170, 190, 255))
        d.line([(95 * s, 210 * s), (165 * s, 210 * s)], fill=(120, 120, 140, 255), width=5 * s)
        d.line([(95 * s, 230 * s), (165 * s, 230 * s)], fill=(120, 120, 140, 255), width=5 * s)
        d.arc([90 * s, 80 * s, 150 * s, 140 * s], 180, 270, fill=(255, 255, 255, 255), width=8 * s)
    return ss_sprite(260, 270, fn)


@lru_cache(maxsize=2)
def clock_face():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        L = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(L).ellipse([0, 0, 300 * s, 300 * s], fill=(120, 200, 255, 120))
        im.alpha_composite(blur(L, 14 * s)); d = ImageDraw.Draw(im)
        d.ellipse([20 * s, 20 * s, 280 * s, 280 * s], fill=(255, 255, 255, 255), outline=(60, 80, 140, 255), width=12 * s)
        for k in range(12):
            a = k / 12 * 2 * math.pi
            r0, r1 = (100, 118) if k % 3 else (88, 118)
            d.line([(150 * s + r0 * s * math.cos(a), 150 * s + r0 * s * math.sin(a)), (150 * s + r1 * s * math.cos(a), 150 * s + r1 * s * math.sin(a))],
                   fill=(60, 80, 140, 255), width=6 * s)
    return ss_sprite(300, 300, fn)


def clock(img, cx, cy, sc, ang_h, ang_m):
    paste(img, clock_face(), cx, cy, scale=sc)
    d = ImageDraw.Draw(img)
    for a, ln, w, col in ((ang_h, 62, 14, (40, 50, 90)), (ang_m, 95, 9, (236, 60, 80))):
        r = math.radians(a - 90)
        d.line([(cx, cy), (cx + ln * sc * math.cos(r), cy + ln * sc * math.sin(r))], fill=col + (255,), width=int(w * sc))
    d.ellipse([cx - 12 * sc, cy - 12 * sc, cx + 12 * sc, cy + 12 * sc], fill=(40, 50, 90, 255))


@lru_cache(maxsize=2)
def scissors_sprite():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        for y in (60, 180):
            d.ellipse([10 * s, (y - 45) * s, 100 * s, (y + 45) * s], outline=(236, 60, 80, 255), width=20 * s)
        d.polygon([(90 * s, 80 * s), (300 * s, 135 * s), (95 * s, 115 * s)], fill=(220, 225, 240, 255), outline=(150, 155, 180, 255))
        d.polygon([(90 * s, 160 * s), (300 * s, 105 * s), (95 * s, 125 * s)], fill=(235, 240, 250, 255), outline=(150, 155, 180, 255))
        d.ellipse([110 * s, 110 * s, 130 * s, 130 * s], fill=(120, 120, 140, 255))
    return glow_sprite(ss_sprite(310, 240, fn), 8, (255, 255, 255, 120))


@lru_cache(maxsize=2)
def shirt_icon():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.polygon([(60 * s, 20 * s), (110 * s, 10 * s), (130 * s, 40 * s), (170 * s, 10 * s), (220 * s, 20 * s), (275 * s, 90 * s),
                   (230 * s, 125 * s), (215 * s, 105 * s), (215 * s, 260 * s), (65 * s, 260 * s), (65 * s, 105 * s), (50 * s, 125 * s), (5 * s, 90 * s)],
                  fill=SHIRT + (255,), outline=(255, 220, 210, 255))
    return ss_sprite(280, 270, fn)


@lru_cache(maxsize=2)
def speaker_icon():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.rectangle([20 * s, 80 * s, 80 * s, 160 * s], fill=(255, 255, 255, 255))
        d.polygon([(80 * s, 80 * s), (150 * s, 30 * s), (150 * s, 210 * s), (80 * s, 160 * s)], fill=(255, 255, 255, 255))
    return ss_sprite(170, 240, fn)


@lru_cache(maxsize=2)
def book_sprite():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.polygon([(10 * s, 40 * s), (200 * s, 70 * s), (200 * s, 250 * s), (10 * s, 220 * s)], fill=(250, 250, 255, 255), outline=(150, 150, 190, 255))
        d.polygon([(390 * s, 40 * s), (200 * s, 70 * s), (200 * s, 250 * s), (390 * s, 220 * s)], fill=(240, 242, 255, 255), outline=(150, 150, 190, 255))
        for k in range(5):
            y = 90 + k * 26
            d.line([(40 * s, (y) * s), (175 * s, (y + 22) * s)], fill=(170, 175, 210, 255), width=5 * s)
            d.line([(225 * s, (y + 22) * s), (360 * s, y * s)], fill=(170, 175, 210, 255), width=5 * s)
    return ss_sprite(400, 260, fn)


@lru_cache(maxsize=1)
def note_sprite():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        for (x0, y0, x1, y1) in ((20, 120, 80, 170), (110, 100, 170, 150)):
            d.ellipse([(x0 - 6) * s, (y0 - 6) * s, (x1 + 6) * s, (y1 + 6) * s], fill=(35, 12, 30, 255))
            d.ellipse([x0 * s, y0 * s, x1 * s, y1 * s], fill=YEL)
        d.line([(76 * s, 145 * s), (76 * s, 30 * s), (166 * s, 10 * s), (166 * s, 125 * s)], fill=(35, 12, 30, 255), width=22 * s)
        d.line([(76 * s, 145 * s), (76 * s, 30 * s), (166 * s, 10 * s), (166 * s, 125 * s)], fill=YEL, width=12 * s)
    return ss_sprite(190, 190, fn)


def swirl(img, cx, cy, r, t, alpha=1.0):
    d = ImageDraw.Draw(img)
    pts = [(cx + (r * k / 60) * math.cos(k / 60 * 4 * math.pi + t * 8), cy + (r * k / 60) * 0.6 * math.sin(k / 60 * 4 * math.pi + t * 8)) for k in range(61)]
    d.line(pts, fill=(255, 225, 80, int(255 * alpha)), width=9, joint='curve')


def stars_ring(img, cx, cy, r, t, n=4):
    for i in range(n):
        a = t * 4 + i / n * 2 * math.pi
        sparkle(img, cx + r * math.cos(a), cy + r * 0.35 * math.sin(a), 22)


def spot(img, cx, cy, rx, ry, a):
    """haz de luz (foco) que cae sobre (cx, cy)"""
    L = layer(); d = ImageDraw.Draw(L)
    d.polygon([(cx - 60, 0), (cx + 60, 0), (cx + rx, cy), (cx - rx, cy)], fill=(255, 245, 190, int(70 * a)))
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(255, 245, 190, int(110 * a)))
    img.alpha_composite(blur(L, 18))


@lru_cache(maxsize=1)
def bg_stage():
    img = vgrad((W, H), rgba('#1b0f33'), rgba('#07040f'))
    d = ImageDraw.Draw(img)
    d.ellipse([-200, 1380, W + 200, 1900], fill=(45, 28, 80, 255))
    return img


@lru_cache(maxsize=1)
def bg_desk():
    img = vgrad((W, H), rgba('#2d1650'), rgba('#170a2c'))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1460, W, H], fill=(120, 72, 40, 255)); d.rectangle([0, 1460, W, 1490], fill=(160, 100, 60, 255))
    return img


def rings(img, cx, cy, t, period, alpha, col=(140, 220, 255), n=3, rmax=260):
    d = ImageDraw.Draw(img)
    for i in range(n):
        u = ((t / period) + i / n) % 1
        r = 40 + rmax * u
        a = int(255 * alpha * (1 - u))
        if a > 4:
            d.arc([cx - r, cy - r, cx + r, cy + r], -50, 50, fill=col + (a,), width=10)


# ---- editor de video
def editor_ui(t, cut_k=0.0, nose_a=0.55, play_x=None, scissors=0.0):
    img = vgrad((W, H), rgba('#1a1f2e'), rgba('#0d1018'))
    d = ImageDraw.Draw(img)
    # ventana
    d.rounded_rectangle([50, 520, 1030, 1720], 30, fill=(34, 40, 58, 255), outline=(90, 110, 160, 255), width=4)
    for i, c in enumerate(((255, 95, 90), (255, 190, 60), (90, 210, 100))):
        d.ellipse([85 + i * 46, 548, 115 + i * 46, 578], fill=c + (255,))
    d.text((540, 563), "EDITOR · CEREBRO", font=font(34, 'x'), fill=(170, 190, 230, 255), anchor='mm')
    # vista previa
    pv = pov_bg().crop((60, 700, 1020, 1340)).resize((900, 600), Image.BILINEAR)
    if nose_a > 0.01:
        L = layer(900, 600); ImageDraw.Draw(L).ellipse([300, 330, 600, 900], fill=(232, 176, 146, int(255 * nose_a)))
        pv.alpha_composite(blur(L, 22))
    img.alpha_composite(pv, (90, 610))
    d.rectangle([90, 610, 990, 1210], outline=(120, 140, 200, 255), width=3)
    # línea de tiempo
    d.rounded_rectangle([90, 1260, 990, 1680], 18, fill=(24, 28, 42, 255))
    tracks = [(1300, [(110, 520, (90, 160, 255)), (540, 970, (90, 160, 255))], 'VISTA'),
              (1420, [(110, 380, (255, 150, 90)), (400, 700, (255, 150, 90)), (720, 970, (255, 150, 90))], 'NARIZ'),
              (1540, [(110, 970, (120, 220, 140))], 'MUNDO')]
    for ti, (y, clips, name) in enumerate(tracks):
        for (x0, x1, col) in clips:
            a = 1.0
            if name == 'NARIZ':
                a = 1 - cut_k
            if a > 0.02:
                L = layer(); ImageDraw.Draw(L).rounded_rectangle([x0, y, x1, y + 90], 14, fill=col + (int(255 * a),), outline=(255, 255, 255, int(160 * a)), width=3)
                img.alpha_composite(L)
        d = ImageDraw.Draw(img)
        d.text((122, y + 45), name, font=font(34, 'x'), fill=(20, 24, 36, 255), anchor='lm')
    px = play_x if play_x is not None else 110 + (t * 160) % 860
    d.line([(px, 1270), (px, 1670)], fill=(255, 70, 90, 255), width=6)
    d.polygon([(px - 16, 1262), (px + 16, 1262), (px, 1286)], fill=(255, 70, 90, 255))
    if scissors > 0:
        paste(img, scissors_sprite(), 540, 1465, scale=scissors, rot=8 * math.sin(t * 30))
    return img


# ---- panel de lista (prioridades)
def prio_panel(img, t, rows, x0=150, y0=820, dy=150):
    for i, (txt, ok, t_in, t_mark) in enumerate(rows):
        if t < t_in: continue
        s = pop(t, t_in, 0.3)
        y = y0 + i * dy
        L = layer(800, 120); dd = ImageDraw.Draw(L)
        col = (20, 60, 40, 220) if (ok and t >= t_mark) else (60, 20, 40, 220) if t >= t_mark else (20, 40, 80, 220)
        dd.rounded_rectangle([3, 3, 797, 117], 30, fill=col, outline=(170, 245, 255, 255), width=4)
        fade = (not ok) and t >= t_mark
        dd.text((60, 60), txt, font=font(54, 'x'), fill=(255, 255, 255, 255) if not fade else (170, 150, 170, 255), anchor='lm')
        if fade:
            tw = dd.textlength(txt, font=font(54, 'x'))
            dd.line([(55, 62), (65 + tw, 62)], fill=(255, 80, 100, 255), width=8)
        g = glow_sprite(L, 10, (90, 230, 255, 120), 0.7)
        paste(img, g, x0 + 400, y + 60, scale=s)
        if t >= t_mark:
            paste(img, check_badge(40, ok), x0 + 760, y + 60, scale=pop(t, t_mark))


# ==================================================================== ESCENAS
# cada escena: f(t) -> (imagen RGBA, zoom, (cx, cy))
t_nariz1 = T('nariz', 0.38)


def sc_hook(t):   # Tu nariz lleva toda tu vida delante de tus ojos,
    tn, td, to = T('nariz', 0.38), T('delante', 1.78), T('ojos', 2.56)
    g = 0.5 + 0.5 * math.sin((t - tn) * 7) if t >= tn else 0
    img = pov(t, nose=0.6 + 0.3 * prog(t, tn, 0.3), glow=0.55 * g * prog(t, tn, 0.2), ring=ease_back(prog(t, tn, 0.35)))
    if t >= tn:
        paste(img, alert_badge(), 840, 1180, scale=pop(t, tn + 0.08))
    if t >= td:
        paste(img, label('¡SIEMPRE AHÍ!', 104, fill=YEL, stroke=10), 540, 760, scale=pop(t, td), rot=-5)
    if t >= to:
        for x in (330, 750):
            eye_with_lid(img, x, 1010, 70, 0.0, look=(0.6 if x < 540 else -0.6, 1))
    z = lerp(1.0, 1.12, ease_in_out(prog(t, 0, 3.0)))
    return img, z, (540, 1300)


def sc_hide(t):   # pero tu cerebro hace que prácticamente desaparezca.
    tc, tp, tdes = T('cerebro', 3.53), T('practicamente', 4.37), T('desaparezca', 5.07)
    img = bg_teal().copy()
    float_bubbles(img, t, n=8, seed=3, rmin=14, rmax=34, area=(0, 500, W, 1800), speed=40, alpha=0.4)
    gone = t >= tdes + 0.15
    spr = hero(eyes='open' if not gone else 'wide', mouth='flat' if not gone else 'o', brows='normal' if not gone else 'raised', cheeks=0.5, sweat=gone)
    na = 1 - prog(t, tdes, 0.3)
    nx, ny = put_hero(img, spr, 540, 1420, 1.55, nose=na, nose_scale=1 + 0.2 * prog(t, tdes, 0.3))
    if t >= tc:
        b = brain_sprite()
        paste(img, b, 540 + 6 * math.sin(t * 9), 620, scale=0.95 * pop(t, tc) * (1 + 0.04 * math.sin(t * 7)))
    if tp <= t < tdes + 0.2:     # varita mágica que se acerca a la nariz
        k = ease_in_out(prog(t, tp, tdes - tp))
        wx, wy = lerp(900, nx + 90, k), lerp(820, ny - 60, k)
        d = ImageDraw.Draw(img)
        d.line([(wx, wy), (wx + 170, wy - 170)], fill=(60, 40, 70, 255), width=20)
        d.line([(wx, wy), (wx + 40, wy - 40)], fill=(255, 255, 255, 255), width=20)
        sparkle(img, wx, wy, 38 + 8 * math.sin(t * 20))
    if tdes <= t < tdes + 0.8:
        k = prog(t, tdes, 0.8)
        paste(img, puff_sprite(), nx, ny, scale=0.6 + 0.9 * k, alpha=1 - k)
        for i in range(5):
            a = i / 5 * 2 * math.pi
            sparkle(img, nx + 180 * k * math.cos(a), ny + 180 * k * math.sin(a), 26 * (1 - k))
    if t >= tdes + 0.15:
        paste(img, label('¿Y MI NARIZ?', 92, fill=YEL, stroke=9), 540, 830, scale=pop(t, tdes + 0.25), rot=-4)
    if tdes <= t < tdes + 0.2:
        img = glitch(img, t)
    z = 1.0 + 0.06 * prog(t, 3.0, 3.0)
    return img, z, (540, 1150)


def sc_challenge(t):   # ¿No me crees? Intenta mirarla ahora mismo.
    tc, ti, tm, ta = T('crees', 6.42), T('intenta', 7.04), T('mirarla', 7.47), T('ahora', 7.87)
    img = bg_purple().copy()
    float_bubbles(img, t, n=7, seed=5, rmin=16, rmax=40, area=(0, 500, W, 1800), speed=50, alpha=0.5)
    cr = ease_out(prog(t, ti, 0.35))
    spr = hero(eyes='open', mouth='smile' if t < ti else 'o', brows='raised', cheeks=0.6, cross=cr if t >= ti else 0.0)
    nx, ny = put_hero(img, spr, 540, 1430, 1.5, nose_glow=t >= tm)
    if tc <= t < ti:
        paste(img, label('¿SEGURO?', 120, fill=YEL, stroke=10), 540, 760, scale=pop(t, tc), rot=-6)
    if t >= tm:   # flechas hacia la nariz
        d = ImageDraw.Draw(img)
        for side in (-1, 1):
            k = pop(t, tm, 0.3)
            x0 = nx + side * (330 - 25 * math.sin(t * 14))
            pts = [(x0, ny), (x0 - side * 120 * k, ny)]
            d.line(pts, fill=(255, 225, 80, 255), width=22)
            hx = x0 - side * 120 * k
            d.polygon([(hx - side * 50 * k, ny), (hx, ny - 36 * k), (hx, ny + 36 * k)], fill=(255, 225, 80, 255))
    if t >= ta:
        paste(img, pill('¡AHORA MISMO!', (236, 40, 70), 62), 540, 800, scale=pop(t, ta), rot=3 * math.sin(t * 12))
    z = 1.0 + 0.1 * ease_out(prog(t, ti, 0.4))
    return img, z, (540, 1120)


def sc_notice(t):   # Acabas de notar algo
    tn, ta = T('notar', 9.42), T('algo', 9.76)
    k = ease_out(prog(t, tn, 0.4))
    img = pov(t, nose=lerp(0.35, 1.0, k), glow=0.6 * k * (0.7 + 0.3 * math.sin(t * 9)), ring=ease_back(prog(t, ta, 0.3)))
    if t >= tn:
        paste(img, bulb_sprite(), 540, 820, scale=pop(t, tn) * (1 + 0.05 * math.sin(t * 10)))
        stars_ring(img, 540, 820, 220, t)
    z = 1.0 + 0.1 * ease_out(prog(t, tn, 0.4))
    return img, z, (540, 1300)


def sc_allday(t):   # que llevabas todo el día ignorando.
    tt, td, ti = T('todo', 10.66), T('dia', 11.04), T('ignorando', 11.19)
    img = bg_holo().copy()
    k = ease_in_out(prog(t, tt, (ti + 0.3) - tt))
    ang = 360 * 2 * k
    sc = pop(t, tt - 0.1, 0.3)
    # sol -> luna
    d = ImageDraw.Draw(img)
    if sc > 0:
        clock(img, 540, 1060, 1.5 * sc, 30 * 12 * k * 2, ang * 6)
        a = math.radians(-90 + 180 * k)
        sx, sy = 540 + 380 * math.cos(a + math.pi), 1060 + 380 * math.sin(a + math.pi) * 0.8
        col = (255, 220, 80) if k < 0.5 else (210, 220, 255)
        g = layer(); ImageDraw.Draw(g).ellipse([sx - 90, sy - 90, sx + 90, sy + 90], fill=col + (150,))
        img.alpha_composite(blur(g, 30))
        d = ImageDraw.Draw(img); d.ellipse([sx - 55, sy - 55, sx + 55, sy + 55], fill=col + (255,))
    if t >= td:
        paste(img, pill('24 H', (40, 120, 240), 60), 540, 1500, scale=pop(t, td))
    if t >= ti:
        paste(img, label('IGNORADA', 130, fill=(255, 80, 100, 255), stroke=11), 540, 740, scale=pop(t, ti, 0.25) * 1.0, rot=-8)
    z = 1.0 + 0.05 * prog(t, tt, 1.5)
    return img, z, (540, 1060)


def sc_how(t):   # Pero ¿cómo es posible?
    tc, tp = T('como', 12.32), T('posible', 12.88)
    img = bg_teal().copy()
    float_bubbles(img, t, n=8, seed=8, rmin=14, rmax=36, area=(0, 500, W, 1800), speed=50, alpha=0.45)
    spr = hero(eyes='open', mouth='side', brows='worried', cheeks=0.4, look=(1, -1))
    put_hero(img, spr, 540, 1480, 1.35)
    if t >= tc:
        for i, (x, y, s) in enumerate(((800, 700, 1.0), (300, 780, 0.7), (870, 980, 0.6))):
            paste(img, label('?', 200, fill=YEL, stroke=12), x, y + 14 * math.sin(t * 4 + i), scale=s * pop(t, tc + i * 0.12), rot=12 * math.sin(t * 3 + i))
    if tp <= t < tp + 0.2:
        img = glitch(img, t)
    return img, 1.0 + 0.05 * prog(t, 12.1, 1.6), (540, 1100)


EYE_Y = 690
PAN_Y = 1290
PW2, PH2 = 470, 660


def eye_panels(t, shift_k=0.0, nose_k=0.0, merge=0.0, single=0.0, flash=None):
    img = bg_holo().copy()
    xs = (290, 790)
    if merge > 0:
        xs = (lerp(290, 540, merge), lerp(790, 540, merge))
    for i, x in enumerate(xs):
        side = 1 if i == 0 else -1   # ojo izq ve la nariz a su derecha
        sh = int((-36 if i == 0 else 36) * shift_k)
        mp = mini_pov(PW2, PH2, shift=80 + sh, nose_side=side, nose_a=0.95 * nose_k * (1 - merge))
        fr = layer(PW2 + 24, PH2 + 24); fd = ImageDraw.Draw(fr)
        fr.alpha_composite(mp, (12, 12))
        fd.rounded_rectangle([2, 2, PW2 + 21, PH2 + 21], 22, outline=(140, 220, 255, 255), width=8)
        a = 1.0 if merge < 0.9 else (1 - (merge - 0.9) * 10) * (1 - single)
        paste(img, glow_sprite(fr, 14, (90, 200, 255, 160)), x, PAN_Y, alpha=max(a, 0.5 if merge > 0 else 1) * (0.6 if merge > 0 and i == 1 else 1))
        if merge < 0.5:
            eye_with_lid(img, x, EYE_Y, 95, 0.0, look=(0.5 * side, 0.3))
            d = ImageDraw.Draw(img)
            for k in range(3):     # rayos del ojo a su imagen
                d.line([(x - 60 + 60 * k, EYE_Y + 100), (x - 180 + 180 * k, PAN_Y - PH2 / 2 - 20)], fill=(120, 210, 255, 90), width=4)
        if flash is not None and flash <= t < flash + 0.25:
            L = layer(); ImageDraw.Draw(L).rounded_rectangle([x - PW2 / 2, PAN_Y - PH2 / 2, x + PW2 / 2, PAN_Y + PH2 / 2], 22, fill=(255, 255, 255, int(230 * (1 - prog(t, flash, 0.25)))))
            img.alpha_composite(L)
    if single > 0:   # imagen combinada: sin nariz
        mp = mini_pov(620, 760, shift=80, nose_side=0)
        fr = layer(644, 784); fr.alpha_composite(mp, (12, 12))
        ImageDraw.Draw(fr).rounded_rectangle([2, 2, 641, 781], 26, outline=(120, 255, 170, 255), width=9)
        paste(img, glow_sprite(fr, 16, (90, 255, 160, 170)), 540, PAN_Y - 40, scale=0.7 + 0.3 * ease_back(single), alpha=min(1, single * 2))
    return img


def sc_eyes(t):   # Cada uno de tus ojos captura una imagen ligeramente diferente,
    tc, tl, td = T('captura', 14.79), T('ligeramente', 15.86), T('diferente', 16.55)
    img = eye_panels(t, shift_k=ease_in_out(prog(t, tl, td - tl + 0.2)), flash=tc)
    if t < tc + 0.05:
        pass
    if t >= td:
        d = ImageDraw.Draw(img)
        for x, side in ((290, -1), (790, 1)):
            k = pop(t, td, 0.3)
            y = PAN_Y + 330
            d.line([(x - 70 * k, y), (x + 70 * k, y)], fill=(255, 225, 80, 255), width=16)
            for sd in (-1, 1):
                hx = x + sd * 70 * k
                d.polygon([(hx + sd * 34 * k, y), (hx, y - 26 * k), (hx, y + 26 * k)], fill=(255, 225, 80, 255))
    return img, 1.0 + 0.05 * prog(t, 13.6, 3.5), (540, 1000)


def sc_eyes_nose(t):   # y en ambas aparece una parte de tu nariz.
    ta, tn = T('ambas', 17.66), T('nariz', 19.14)
    nk = ease_out(prog(t, T('parte', 18.68), 0.5))
    img = eye_panels(t, shift_k=1.0, nose_k=nk, flash=ta)
    if t >= T('parte', 18.68):
        d = ImageDraw.Draw(img)
        for x, side in ((290, 1), (790, -1)):
            cx = x + side * PW2 * 0.38; cy = PAN_Y + PH2 * 0.3
            r = 130 * ease_back(prog(t, T('parte', 18.68), 0.35))
            d.ellipse([cx - r, cy - r * 1.2, cx + r, cy + r * 1.2], outline=(255, 50, 70, 255), width=12)
    if t >= tn:
        paste(img, alert_badge(), 540, PAN_Y - 120, scale=pop(t, tn))
    return img, 1.0 + 0.06 * prog(t, 17.3, 2.5), (540, 1150)


def sc_combine(t):   # Sin embargo, tu cerebro combina esas imágenes
    tc, tcb = T('cerebro', 21.0), T('combina', 21.44)
    m = ease_in_out(prog(t, tcb, 0.9))
    img = eye_panels(t, shift_k=1.0, nose_k=1.0, merge=m)
    if t >= tc:
        paste(img, brain_sprite(), 540, 690, scale=1.05 * pop(t, tc) * (1 + 0.05 * math.sin(t * 8)))
        if t >= tcb:
            d = ImageDraw.Draw(img)
            for k in range(2):
                x = 290 + 500 * k
                d.line([(540, 780), (lerp(x, 540, m), PAN_Y - PH2 / 2)], fill=(255, 160, 200, 160), width=8)
    if t >= T('sin', 19.88) and t < tc:
        paste(img, pill('PERO…', (236, 40, 70), 60), 540, 690, scale=pop(t, T('sin', 19.88)))
    return img, 1.0, (540, 1000)


def sc_single(t):   # para construir una sola representación del mundo.
    tu, tr, tm = T('una', 23.38), T('representacion', 23.90), T('mundo', 24.77)
    sg = ease_out(prog(t, tu, 0.5))
    img = eye_panels(t, shift_k=1.0, nose_k=1.0, merge=1.0, single=sg)
    paste(img, brain_sprite(), 540, 690, scale=1.05 * (1 + 0.05 * math.sin(t * 8)))
    if t >= tu:
        paste(img, pill('1 SOLA IMAGEN', (30, 150, 90), 58), 540, 1760, scale=pop(t, tu + 0.1))
    if t >= tm:
        paste(img, check_badge(56, True), 830, PAN_Y - 400, scale=pop(t, tm))
        stars_ring(img, 540, PAN_Y - 40, 360, t, 5)
    return img, 1.0 + 0.08 * ease_out(prog(t, tu, 0.6)), (540, 1150)


def holo_eyes_path(img, k, t):
    """camino ojo -> cerebro dentro del holograma"""
    if k <= 0: return
    d = ImageDraw.Draw(img)
    pts = [(510, 588 - 40), (470, 600 - 60), (450, 560 - 90), (500, 470), (560, 455)]
    pts = [(x, y + 120) for x, y in pts]
    n = max(2, int(len(pts) * k))
    L = layer(); ImageDraw.Draw(L).line(pts[:n], fill=(120, 255, 170, 255), width=14, joint='curve')
    img.alpha_composite(blur(L, 10)); img.alpha_composite(L)


def sc_visual(t):   # Además, tu sistema visual aprende
    ts, tv, ta = T('sistema', 26.71), T('visual', 27.16), T('aprende', 27.46)
    img = bg_holo().copy()
    paste(img, holo_body(), 540, 1160, scale=1.05)
    hx, hy = 540, 1160 - 1180 * 1.05 / 2 + 150 * 1.05
    if t >= ts:
        k = ease_out(prog(t, ts, 0.6))
        L = layer(); dd = ImageDraw.Draw(L)
        for ex in (hx - 40, hx + 40):
            dd.ellipse([ex - 20, hy + 10 - 16, ex + 20, hy + 10 + 16], fill=(120, 255, 170, int(255 * k)))
        dd.line([(hx - 40, hy + 10), (hx, hy - 50), (hx + 40, hy + 10)], fill=(120, 255, 170, int(255 * k)), width=12, joint='curve')
        img.alpha_composite(blur(L, 10)); img.alpha_composite(L)
    if t >= tv:
        paste(img, eyeball(70), hx + 250, hy - 40, scale=pop(t, tv))
    if t >= ta:
        k = ease_out(prog(t, ta, 0.9))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([190, 1700, 890, 1760], 30, fill=(20, 40, 80, 255), outline=(140, 220, 255, 255), width=4)
        d.rounded_rectangle([196, 1706, 196 + 688 * k, 1754], 26, fill=(120, 255, 170, 255))
        paste(img, pill('APRENDIENDO…', (40, 120, 240), 50), 540, 1620, scale=pop(t, ta))
    return img, 1.0 + 0.05 * prog(t, 25.6, 2.4), (540, 900)


@lru_cache(maxsize=2)
def nose_chip(grey=False):
    def fn(im, s):
        d = ImageDraw.Draw(im)
        col = (150, 140, 160, 255) if grey else SKIN + (255,)
        d.ellipse([6 * s, 6 * s, 174 * s, 174 * s], fill=col, outline=(255, 255, 255, 255), width=6 * s)
    out = ss_sprite(180, 180, fn)
    n = nose_sprite(False)
    if grey:
        n = Image.merge('RGBA', (*Image.merge('RGB', n.split()[:3]).convert('L').convert('RGB').split(), n.split()[3]))
    paste(out, n, 90, 92, scale=0.95)
    return out


def nose_token(img, x, y, sc, grey=0.0, alpha=1.0):
    paste(img, nose_chip(grey > 0.5), x, y, scale=sc * 0.62, alpha=alpha)


def sc_ignore(t):   # a ignorar los estímulos constantes que no considera importantes.
    ti, te, tc, timp = T('ignorar', 27.98), T('estimulos', 28.51), T('constantes', 29.25), T('importantes', 30.60)
    img = bg_holo().copy()
    paste(img, brain_sprite(), 540, 760, scale=1.5 * (1 + 0.03 * math.sin(t * 7)))
    # cinta de estímulos que llegan al cerebro una y otra vez
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([60, 1280, 1020, 1440], 40, fill=(20, 40, 80, 220), outline=(140, 220, 255, 255), width=4)
    for i in range(7):
        x = 1100 - ((t - ti) * 330 + i * 190) % 1300
        if x < 40 or x > 1060: continue
        grey = prog(t, tc, 0.4)
        nose_token(img, x, 1360, 1.05, grey)
        if t >= tc and 120 < x < 960:
            pass
    if t >= te:
        paste(img, pill('MISMO ESTÍMULO x1000', (40, 120, 240), 46), 540, 1540, scale=pop(t, te))
    if t >= tc:
        # cerebro «apaga» la señal
        paste(img, check_badge(48, False), 540, 1180, scale=pop(t, tc))
    if t >= timp:
        paste(img, label('NO IMPORTA', 110, fill=(255, 80, 100, 255), stroke=10), 540, 1720, scale=pop(t, timp), rot=-4)
    z = 1.0 + 0.05 * prog(t, ti, 3.0)
    return img, z, (540, 1100)


def sc_editor(t):   # Es como tener un editor de video trabajando
    te, tt = T('editor', 32.67), T('trabajando', 33.46)
    img = editor_ui(t, play_x=110 + 860 * ease_in_out(prog(t, tt, 0.8)) if t >= tt else 110)
    if t >= te:
        paste(img, label('EDITOR', 120, fill=YEL, stroke=10), 540, 1830, scale=pop(t, te), rot=-3)
    sc = 1.0 if t >= te else 0.0
    z = lerp(1.25, 1.0, ease_out(prog(t, T('es', 31.85), 0.7)))
    return img, z, (540, 1100)


def sc_head(t):   # dentro de tu cabeza,
    tc = T('cabeza', 34.76)
    img = bg_teal().copy()
    spr = hero(eyes='open', mouth='flat', cheeks=0.4)
    put_hero(img, spr, 540, 1480, 1.35)
    # mini editor en la frente
    k = pop(t, T('dentro', 34.06), 0.3)
    if k > 0:
        mini = editor_ui(t).crop((40, 510, 1040, 1730)).resize((300, 366), Image.BILINEAR)
        fr = layer(320, 386); fr.alpha_composite(mini, (10, 10))
        ImageDraw.Draw(fr).rounded_rectangle([2, 2, 317, 383], 20, outline=(140, 220, 255, 255), width=6)
        paste(img, glow_sprite(fr, 14, (90, 200, 255, 180)), 540, 700, scale=k)
        d = ImageDraw.Draw(img)
        for i in range(3):
            cy = 900 + i * 38; r = 16 - i * 4
            d.ellipse([540 - r, cy - r, 540 + r, cy + r], fill=(220, 245, 255, 255))
    if t >= tc:
        paste(img, alert_badge(40), 760, 560, scale=pop(t, tc))
    return img, 1.0 + 0.05 * prog(t, 34.0, 1.3), (540, 1100)


def sc_cut(t):   # eliminando distracciones
    tel, tdis = T('eliminando', 35.34), T('distracciones', 36.01)
    ck = ease_out(prog(t, tdis, 0.35))
    img = editor_ui(t, cut_k=ck, nose_a=0.6 * (1 - ck), play_x=540, scissors=pop(t, tel, 0.3) * (1 - prog(t, tdis + 0.35, 0.2)))
    if tdis <= t < tdis + 0.7:
        k = prog(t, tdis, 0.7)
        paste(img, puff_sprite(), 540, 1465, scale=0.5 + 0.8 * k, alpha=1 - k)
    if t >= tdis:
        paste(img, label('¡CORTE!', 120, fill=(255, 80, 100, 255), stroke=10), 540, 1830, scale=pop(t, tdis), rot=-5)
    return img, 1.0 + 0.1 * ease_out(prog(t, tel, 0.4)), (540, 1350)


def sc_unaware(t):   # sin que te des cuenta.
    tcu = T('cuenta', 37.37)
    img = bg_purple().copy()
    float_bubbles(img, t, n=7, seed=9, rmin=16, rmax=36, area=(0, 500, W, 1800), speed=50, alpha=0.4)
    spr = hero(eyes='closed', mouth='smile', cheeks=0.6, brows='raised')
    put_hero(img, spr, 540, 1440, 1.45, rot=4 * math.sin(t * 5))
    if t >= tcu:
        for i, x in enumerate((780, 300)):
            paste(img, note_sprite(), x, 760 - 40 * ((t * 1.2 + i * 0.5) % 1), scale=pop(t, tcu + i * 0.1), rot=10 * math.sin(t * 4 + i))
    return img, 1.0 + 0.04 * prog(t, 36.6, 1.5), (540, 1150)


def sc_surprise(t):   # Pero aquí viene lo más sorprendente.
    ta, ts = T('aqui', 38.40), T('sorprendente', 39.12)
    img = bg_purple().copy()
    float_bubbles(img, t, n=10, seed=11, rmin=16, rmax=46, area=(0, 500, W, 1800), speed=70, alpha=0.6)
    spr = hero(eyes='wide', mouth='o', brows='raised', cheeks=0.8, sweat=True)
    put_hero(img, spr, 540, 1500, 1.4, rot=3 * math.sin(t * 40) * (t >= ts))
    if t >= ta:
        paste(img, alert_badge(64), 820, 700, scale=pop(t, ta))
    if t >= ts:
        stars_ring(img, 540, 1030, 380, t, 6)
    if t >= T('pero', 38.18):
        paste(img, follow_button(), 540, 1800, scale=pop(t, T('pero', 38.18) + 0.1))
    if ts <= t < ts + 0.22:
        img = glitch(img, t)
    z = 1.0 + 0.08 * ease_out(prog(t, ts, 0.3))
    return img, z, (540, 1150)


def sc_not_only(t):   # Tu cerebro no solamente ignora tu nariz.
    tn, tig, tna = T('solamente', 40.92), T('ignora', 41.48), T('nariz', 41.98)
    img = bg_holo().copy()
    paste(img, brain_sprite(), 540, 760, scale=1.3 * (1 + 0.03 * math.sin(t * 7)))
    nose_token(img, 540, 1180, 1.6 * pop(t, T('tu', 40.24)))
    if t >= tig:
        paste(img, check_badge(60, False), 680, 1080, scale=pop(t, tig))
    if t >= tn:
        for i, x in enumerate((220, 860)):
            s = pop(t, tn + 0.25 + i * 0.15)
            if s > 0:
                paste(img, pill('+ ?', (40, 120, 240), 70), x, 1500, scale=s)
    return img, 1.0 + 0.05 * prog(t, 40.2, 2.4), (540, 1050)


def sc_blink(t):   # También puede dejar de prestar atención al parpadeo de tus ojos,
    tp, to = T('parpadeo', 44.95), T('ojos', 45.84)
    img = bg_teal().copy()
    # parpadeos: uno en «parpadeo» y otro en «ojos»
    lid = 0.0
    for b in (tp, to):
        k = prog(t, b, 0.28)
        if 0 < k < 1: lid = max(lid, math.sin(math.pi * k))
    for x in (300, 780):
        eye_with_lid(img, x, 1050, 200, lid, look=(0.2 * math.sin(t * 2), 0))
    if t >= tp:
        n = int(round(15 * ease_out(prog(t, tp, to + 0.25 - tp))))
        paste(img, label(f'~{n}', 200, fill=YEL, stroke=12), 540, 1460, scale=pop(t, tp, 0.25))
        paste(img, pill('PARPADEOS POR MINUTO', (236, 40, 70), 46), 540, 1640, scale=pop(t, tp + 0.1))
    if t >= T('atencion', 44.35):
        paste(img, pill('ATENCIÓN: OFF', (40, 120, 240), 48), 540, 720, scale=pop(t, T('atencion', 44.35)))
    return img, 1.0 + 0.05 * prog(t, 42.8, 3.6), (540, 1100)


def sc_clothes(t):   # al contacto de tu ropa con la piel
    tc, tr, tpi = T('contacto', 46.65), T('ropa', 47.40), T('piel', 48.12)
    img = bg_purple().copy()
    spr = hero(eyes='open', mouth='flat', cheeks=0.4)
    put_hero(img, spr, 540, 1240, 1.1)
    # chispitas de tacto en hombros/brazos que se apagan
    fade = 1 - 0.75 * prog(t, tpi, 0.4)
    pts = [(360, 1080), (720, 1080), (300, 1300), (780, 1300), (540, 1420), (420, 1600), (660, 1600)]
    for i, (x, y) in enumerate(pts):
        s = pop(t, tc + i * 0.08)
        if s <= 0: continue
        r = 30 + 10 * math.sin(t * 9 + i)
        L = layer(); ImageDraw.Draw(L).ellipse([x - r, y - r, x + r, y + r], fill=(255, 235, 120, int(200 * fade)))
        img.alpha_composite(blur(L, 10))
        sparkle(img, x, y, 24 * s, alpha=fade)
    if t >= tr:
        paste(img, label('ROCE', 110, fill=YEL, stroke=10), 840, 760, scale=pop(t, tr), alpha=fade, rot=8)
    if t >= tpi:
        paste(img, pill('IGNORADO', (120, 110, 150), 52), 540, 1780, scale=pop(t, tpi))
    return img, 1.0 + 0.04 * prog(t, 46.4, 2.0), (540, 1150)


def sc_sounds(t):   # e incluso a ciertos sonidos repetitivos.
    ts, tr = T('sonidos', 49.67), T('repetitivos', 50.10)
    img = bg_holo('purple').copy()
    clock(img, 330, 1100, 1.1, 300, (t * 360) % 360)
    paste(img, speaker_icon(), 700, 1100, scale=1.1 * pop(t, T('ciertos', 49.35)))
    fade = 1 - 0.7 * prog(t, tr + 0.3, 0.6)
    if t >= ts:
        rings(img, 770, 1100, t, 0.5, fade, rmax=190)
        tic = 'TIC' if int(t * 2) % 2 == 0 else 'TAC'
        paste(img, label(tic, 100, fill=YEL, stroke=9), 330, 780, alpha=fade, scale=pop(t, ts))
    if t >= tr:
        paste(img, pill('x1000', (236, 40, 70), 62), 540, 1500, scale=pop(t, tr))
    return img, 1.0 + 0.04 * prog(t, 48.6, 2.8), (540, 1100)


ICONS = None


def sc_overload(t):   # Si fueras consciente de todos esos estímulos al mismo tiempo,
    tt, te, tm = T('todos', 52.52), T('estimulos', 53.14), T('mismo', 53.92)
    img = bg_purple().copy()
    shk = 1.0 if t >= tm else 0.0
    spr = hero(eyes='wide' if t >= te else 'open', mouth='o' if t >= tm else 'flat', brows='worried' if t >= te else 'normal', sweat=t >= te, cheeks=0.8)
    jx = 10 * math.sin(t * 90) * shk
    put_hero(img, spr, 540 + jx, 1430, 1.35, nose_glow=True)
    items = [('nose', 220, 700), ('eye', 860, 700), ('shirt', 160, 1080), ('clock', 920, 1080), ('spk', 200, 1500), ('nose', 880, 1500), ('eye', 540, 640)]
    for i, (k, x, y) in enumerate(items):
        s = pop(t, tt + i * 0.13, 0.25)
        if s <= 0: continue
        x += 8 * math.sin(t * 50 + i) * shk; y += 8 * math.cos(t * 47 + i) * shk
        if k == 'nose': paste(img, nose_sprite(True), x, y, scale=0.9 * s)
        elif k == 'eye': paste(img, eyeball(60), x, y, scale=s)
        elif k == 'shirt': paste(img, shirt_icon(), x, y, scale=0.5 * s)
        elif k == 'clock': clock(img, x, y, 0.45 * s, 200, t * 500)
        else: paste(img, speaker_icon(), x, y, scale=0.6 * s)
    if t >= tm:
        for i, (x, y) in enumerate(((330, 900), (760, 900))):
            paste(img, alert_badge(44), x, y, scale=pop(t, tm + i * 0.1))
    z = 1.0 + 0.06 * prog(t, 51.4, 3.6)
    return img, z, (540, 1100)


def sc_focus(t):   # te resultaría mucho más difícil concentrarte.
    td, tc = T('dificil', 56.24), T('concentrarte', 56.70)
    img = bg_desk().copy()
    spr = hero(eyes='squeeze' if t >= tc else 'open', mouth='wobble', brows='worried', sweat=True, cheeks=0.8, arms='none')
    put_hero(img, spr, 540, 1240, 1.15)
    paste(img, book_sprite(), 540, 1500, scale=1.2)
    if t >= T('mucho', 55.78):
        swirl(img, 540, 690, 150 * pop(t, T('mucho', 55.78)), t)
    if t >= td:
        paste(img, check_badge(56, False), 850, 820, scale=pop(t, td))
    if t >= tc:
        paste(img, label('¡NO PUEDO!', 100, fill=(255, 80, 100, 255), stroke=10), 540, 1780, scale=pop(t, tc), rot=-4)
    return img, 1.0 + 0.05 * prog(t, 55.0, 2.8), (540, 1100)


def sc_priority(t):   # Por eso tu cerebro prioriza la información que considera relevante.
    tp, ti, tr = T('prioriza', 58.81), T('informacion', 59.34), T('relevante', 60.74)
    img = bg_holo().copy()
    paste(img, brain_sprite(), 540, 640, scale=1.0 * pop(t, T('cerebro', 58.41)) * (1 + 0.04 * math.sin(t * 8)))
    rows = [('¡PELIGRO!', True, tp, tr), ('TU NOMBRE', True, tp + 0.2, tr + 0.1), ('TU NARIZ', False, ti, tr + 0.2), ('LA ROPA', False, ti + 0.2, tr + 0.3)]
    prio_panel(img, t, rows, y0=860, dy=165)
    return img, 1.0 + 0.04 * prog(t, 57.8, 3.3), (540, 1100)


def sc_never(t):   # Tu nariz nunca desapareció.
    tn, td = T('nunca', 62.12), T('desaparecio', 62.40)
    img = pov(t, nose=0.9, glow=0.5 * (0.6 + 0.4 * math.sin(t * 6)), ring=ease_back(prog(t, T('nariz', 61.84), 0.35)))
    if t >= td:
        paste(img, check_badge(60, True), 840, 1200, scale=pop(t, td))
        paste(img, label('SIEMPRE ESTUVO', 92, fill=YEL, stroke=9), 540, 760, scale=pop(t, td + 0.1), rot=-4)
    return img, 1.0 + 0.06 * prog(t, 61.6, 2.0), (540, 1300)


def sc_attention(t):   # Simplemente dejaste de prestarle atención.
    td, ta = T('dejaste', 64.23), T('atencion', 65.59)
    img = bg_stage().copy()
    k = ease_in_out(prog(t, td, ta - td))
    sx = lerp(540, 880, k)
    spot(img, sx, 1450, 230, 70, 1.0)
    nose_token(img, 540, 1330, 2.3, grey=prog(t, ta, 0.4))
    paste(img, label('ATENCIÓN', 80, fill=(255, 245, 190, 255), stroke=8), min(sx, 790), 640, scale=pop(t, T('simplemente', 63.55)))
    if t >= ta:
        paste(img, check_badge(54, False), 700, 1180, scale=pop(t, ta))
    return img, 1.0 + 0.04 * prog(t, 63.5, 2.7), (540, 1100)


def sc_funny(t):   # Y lo más gracioso es que,
    tg = T('gracioso', 66.77)
    img = bg_teal().copy()
    float_bubbles(img, t, n=8, seed=12, rmin=16, rmax=40, area=(0, 500, W, 1800), speed=60, alpha=0.5)
    spr = hero(eyes='closed', mouth='smile', brows='raised', cheeks=0.9)
    put_hero(img, spr, 540, 1460 + 12 * abs(math.sin(t * 12)) * (t >= tg), 1.4)
    if t >= tg:
        for i, (x, y, r) in enumerate(((240, 760, -12), (840, 820, 10))):
            paste(img, label('JAJA', 110, fill=YEL, stroke=10), x, y, scale=pop(t, tg + i * 0.12), rot=r)
    return img, 1.0 + 0.04 * prog(t, 66.2, 1.6), (540, 1150)


def sc_phone(t):   # después de ver este video,
    tv = T('video', 68.79)
    img = bg_purple().copy()
    k = pop(t, T('despues', 67.84), 0.35)
    ph = device_sprite()
    sc = 1.55 * k
    if sc > 0.02:
        scr = layer(380, 560)
        pv = pov(t, nose=0.85, glow=0.3, ring=1.0 if t >= tv else 0.0).resize((300, 533), Image.BILINEAR)
        scr.alpha_composite(ph)
        m = Image.new('L', (300, 330), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 299, 329], 24, fill=255)
        crop = pv.crop((0, 140, 300, 470))
        scr.paste(crop, (40, 50), m)
        paste(img, scr, 540, 1150, scale=sc, rot=-4 + 2 * math.sin(t * 2))
    if t >= tv:
        paste(img, pill('▶ ESTE VIDEO', (236, 40, 70), 56), 540, 1720, scale=pop(t, tv))
    return img, 1.0 + 0.05 * prog(t, 67.8, 1.7), (540, 1150)


def sc_trying(t):   # probablemente pases los próximos segundos intentando dejar de verla.
    ts, ti = T('segundos', 71.16), T('intentando', 71.53)
    img = bg_purple().copy()
    cr = 1.0
    spr = hero(eyes='open', mouth='tense' if t >= ti else 'flat', brows='worried', sweat=t >= ti, cheeks=0.8, cross=cr)
    jx = 6 * math.sin(t * 80) * (t >= ti)
    put_hero(img, spr, 540 + jx, 1440, 1.5, nose_glow=True)
    if t >= ts:
        n = int(max(0, t - ts) * 3) + 1
        paste(img, pill(f'00:{min(n, 59):02d}', (40, 120, 240), 70), 540, 760, scale=pop(t, ts))
    return img, 1.0 + 0.1 * ease_in_out(prog(t, 69.4, 3.2)), (540, 1150)


def sc_loop(t):   # ...dejar de verla.  (vuelve a la nariz del inicio: bucle)
    tv = T('verla', 72.61)
    img = pov(t, nose=0.75, glow=0.4 * prog(t, tv, 0.3), ring=ease_back(prog(t, tv, 0.3)))
    return img, 1.0, (540, 1300)


# ==================================================================== línea de tiempo
def _c(word, approx, pre=0.06):
    return T(word, approx) - pre


SCENES = [
    (0.0, sc_hook),
    (_c('pero', 3.09), sc_hide),
    (_c('no', 6.07), sc_challenge),
    (_c('acabas', 8.89), sc_notice),
    (_c('llevabas', 10.16), sc_allday),
    (_c('pero', 12.15), sc_how),
    (_c('cada', 13.71), sc_eyes),
    (_c('y', 17.38), sc_eyes_nose),
    (_c('sin', 19.88), sc_combine),
    (_c('para', 22.59), sc_single),
    (_c('ademas', 25.67), sc_visual),
    (_c('ignorar', 27.98), sc_ignore),
    (_c('es', 31.85), sc_editor),
    (_c('dentro', 34.06), sc_head),
    (_c('eliminando', 35.34), sc_cut),
    (_c('sin', 36.65), sc_unaware),
    (_c('pero', 38.18), sc_surprise),
    (_c('tu', 40.24), sc_not_only),
    (_c('tambien', 42.88), sc_blink),
    (_c('al', 46.47), sc_clothes),
    (_c('e', 48.61), sc_sounds),
    (_c('si', 51.42), sc_overload),
    (_c('te', 54.99), sc_focus),
    (_c('por', 57.86), sc_priority),
    (_c('tu', 61.68), sc_never),
    (_c('simplemente', 63.55), sc_attention),
    (_c('y', 66.29), sc_funny),
    (_c('despues', 67.84), sc_phone),
    (_c('probablemente', 69.46), sc_trying),
    (_c('verla', 72.61), sc_loop),
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
        sfx(c - 0.12, 'whoosh', -11, dur=0.3)
    # hook
    sfx(T('nariz', 0.38), 'pop', -7); sfx(T('nariz', 0.38) + 0.08, 'beep', -13)
    sfx(T('delante', 1.78), 'pop', -8)
    sfx(T('ojos', 2.56), 'bloop', -9)
    # cerebro la borra
    sfx(T('cerebro', 3.53), 'bloop', -7)
    sfx(T('practicamente', 4.37), 'sparkle', -12)
    sfx(T('desaparezca', 5.07), 'glitch', -6); sfx(T('desaparezca', 5.07) + 0.02, 'poof', -7)
    sfx(T('desaparezca', 5.07) + 0.25, 'pop', -9)
    # reto
    sfx(T('crees', 6.42), 'pop', -8)
    sfx(T('intenta', 7.04), 'boing', -9)
    sfx(T('mirarla', 7.47), 'pop', -10); sfx(T('mirarla', 7.47) + 0.05, 'pop', -12)
    sfx(T('ahora', 7.87), 'impact', -9); sfx(T('ahora', 7.87) + 0.02, 'pop', -8)
    # notar
    sfx(T('notar', 9.42), 'ding', -7); sfx(T('notar', 9.42) + 0.05, 'sparkle', -12)
    sfx(T('algo', 9.76), 'beep', -13)
    # todo el día
    sfx(T('todo', 10.66) - 0.1, 'pop', -9)
    t0, t1 = T('todo', 10.66), T('ignorando', 11.19) + 0.3
    for i in range(8): sfx(t0 + (t1 - t0) * i / 8, 'tick', -14)
    sfx(T('dia', 11.04), 'pop', -10)
    sfx(T('ignorando', 11.19), 'buzz', -9); sfx(T('ignorando', 11.19) + 0.02, 'impact', -11)
    # cómo
    for i in range(3): sfx(T('como', 12.32) + i * 0.12, 'pop', -10)
    sfx(T('posible', 12.88), 'glitch', -8)
    # ojos
    sfx(T('ojos', 14.53), 'bloop', -10)
    sfx(T('captura', 14.79), 'shutter', -7)
    sfx(T('ligeramente', 15.86), 'sweep', -14, dur=0.7)
    sfx(T('diferente', 16.55), 'pop', -9)
    sfx(T('ambas', 17.66), 'shutter', -9)
    sfx(T('parte', 18.68), 'scan', -14, dur=0.5)
    sfx(T('nariz', 19.14), 'pop', -7); sfx(T('nariz', 19.14) + 0.02, 'beep', -12)
    # combina
    sfx(T('sin', 19.88), 'pop', -9)
    sfx(T('cerebro', 21.0), 'bloop', -7)
    sfx(T('combina', 21.44), 'whoosh', -8, dur=0.8); sfx(T('combina', 21.44) + 0.85, 'impact', -9)
    sfx(T('una', 23.38), 'pop', -8); sfx(T('una', 23.38) + 0.1, 'pop', -11)
    sfx(T('mundo', 24.77), 'ding', -7); sfx(T('mundo', 24.77) + 0.05, 'sparkle', -12)
    # sistema visual
    sfx(T('sistema', 26.71), 'scan', -13, dur=0.6)
    sfx(T('visual', 27.16), 'pop', -9)
    sfx(T('aprende', 27.46), 'rise', -12, dur=0.8); sfx(T('aprende', 27.46), 'pop', -10)
    # ignorar
    t0 = T('ignorar', 27.98)
    for i in range(9): sfx(t0 + 0.2 + i * 0.36, 'tick', -16)
    sfx(T('estimulos', 28.51), 'pop', -9)
    sfx(T('constantes', 29.25), 'buzz', -10); sfx(T('constantes', 29.25), 'pop', -10)
    sfx(T('importantes', 30.60), 'impact', -9); sfx(T('importantes', 30.60) + 0.02, 'pop', -8)
    # editor
    sfx(T('editor', 32.67), 'pop', -7); sfx(T('editor', 32.67) + 0.05, 'click', -10)
    sfx(T('trabajando', 33.46), 'scan', -15, dur=0.8)
    sfx(T('dentro', 34.06), 'bloop', -8); sfx(T('cabeza', 34.76), 'pop', -8)
    sfx(T('eliminando', 35.34), 'pop', -9)
    sfx(T('distracciones', 36.01), 'snip', -6); sfx(T('distracciones', 36.01) + 0.05, 'poof', -9)
    sfx(T('distracciones', 36.01) + 0.08, 'pop', -9)
    sfx(T('cuenta', 37.37), 'sparkle', -12)
    # sorpresa + sígueme
    sfx(T('pero', 38.18) + 0.1, 'click', -8); sfx(T('aqui', 38.40), 'pop', -8)
    sfx(T('sorprendente', 39.12), 'glitch', -7); sfx(T('sorprendente', 39.12) + 0.02, 'impact', -8)
    sfx(T('sorprendente', 39.12) + 0.1, 'sparkle', -12)
    # no solamente
    sfx(T('tu', 40.24), 'pop', -9); sfx(T('ignora', 41.48), 'buzz', -10)
    sfx(T('solamente', 40.92) + 0.25, 'pop', -9); sfx(T('solamente', 40.92) + 0.4, 'pop', -10)
    # parpadeo
    sfx(T('atencion', 44.35), 'powerdown', -13)
    sfx(T('parpadeo', 44.95), 'blink', -8); sfx(T('ojos', 45.84), 'blink', -8)
    t0, t1 = T('parpadeo', 44.95), T('ojos', 45.84) + 0.25
    for i in range(15): sfx(t0 + (t1 - t0) * i / 15, 'tick', -15)
    sfx(t1, 'ding', -10)
    # ropa
    for i in range(7): sfx(T('contacto', 46.65) + i * 0.08, 'pop', -14)
    sfx(T('ropa', 47.40), 'pop', -8)
    sfx(T('piel', 48.12), 'powerdown', -12)
    # sonidos
    sfx(T('ciertos', 49.35), 'pop', -9)
    t0 = T('sonidos', 49.67)
    for i in range(6): sfx(t0 + i * 0.5, 'tick', -12 - i * 2)
    sfx(T('repetitivos', 50.10), 'pop', -8)
    # sobrecarga
    for i in range(7): sfx(T('todos', 52.52) + i * 0.13, 'pop', -10)
    sfx(T('estimulos', 53.14), 'beep', -13)
    sfx(T('mismo', 53.92), 'impact', -7); sfx(T('mismo', 53.92) + 0.05, 'alarm', -12, dur=0.9)
    # concentrarse
    sfx(T('mucho', 55.78), 'swirl', -13, dur=1.0)
    sfx(T('dificil', 56.24), 'buzz', -9); sfx(T('dificil', 56.24), 'pop', -10)
    sfx(T('concentrarte', 56.70), 'boing', -9)
    # prioridades
    sfx(T('cerebro', 58.41), 'bloop', -9)
    for tt in (T('prioriza', 58.81), T('prioriza', 58.81) + 0.2, T('informacion', 59.34), T('informacion', 59.34) + 0.2): sfx(tt, 'pop', -10)
    tr = T('relevante', 60.74)
    sfx(tr, 'ding', -9); sfx(tr + 0.1, 'ding', -12); sfx(tr + 0.2, 'buzz', -12); sfx(tr + 0.3, 'buzz', -13)
    # nunca desapareció
    sfx(T('nariz', 61.84), 'beep', -12)
    sfx(T('desaparecio', 62.40), 'ding', -7); sfx(T('desaparecio', 62.40) + 0.1, 'pop', -9)
    # foco
    sfx(T('simplemente', 63.55), 'click', -8)
    sfx(T('dejaste', 64.23), 'sweep', -14, dur=1.2)
    sfx(T('atencion', 65.59), 'powerdown', -9); sfx(T('atencion', 65.59) + 0.02, 'pop', -10)
    # gracioso
    sfx(T('gracioso', 66.77), 'boing', -9); sfx(T('gracioso', 66.77) + 0.12, 'pop', -10)
    # móvil
    sfx(T('despues', 67.84), 'pop', -8); sfx(T('video', 68.79), 'click', -8); sfx(T('video', 68.79) + 0.03, 'pop', -9)
    # intentando
    sfx(T('probablemente', 69.46), 'boing', -11)
    t0 = T('segundos', 71.16)
    for i in range(int((72.95 - t0) * 3) + 1): sfx(t0 + i / 3, 'tick', -13)
    sfx(T('intentando', 71.53), 'squeeze', -10)
    sfx(T('verla', 72.61), 'pop', -8); sfx(T('verla', 72.61) + 0.05, 'beep', -12)
    return SFX
