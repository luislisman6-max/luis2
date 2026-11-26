"""Escenas del video «Tu piel tiene un mapa oculto» (líneas de Blaschko).
Todos los tiempos salen de words.json (palabra exacta): animación, efectos y subtítulos usan el mismo reloj."""
import json, math, os, random, sys, unicodedata
from functools import lru_cache
from PIL import Image, ImageDraw, ImageChops, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from lib import *          # noqa
from art import *          # noqa
from scenes import P, label, pill, sparkle, float_bubbles, glitch, follow_button, lens_sprite, puff_sprite  # noqa

WORDS = json.load(open(os.path.join(HERE, 'words.json')))


def _n(w):
    w = unicodedata.normalize('NFD', w.lower())
    return ''.join(c for c in w if unicodedata.category(c) != 'Mn' and c.isalnum())


def T(word, approx):
    """inicio (s) de la aparición de `word` más cercana a `approx` (s)"""
    c = [w['s'] for w in WORDS if _n(w['w']) == _n(word)]
    if not c: raise KeyError(word)
    best = min(c, key=lambda s: abs(s - approx))
    assert abs(best - approx) < 0.6, (word, approx, best)
    return best


SFX = []


def sfx(t, name, g=0.0, **kw):
    SFX.append((t, name, g, kw))


# ==================================================================== colores
SKIN = (241, 194, 160)
SKIN_D = (214, 158, 126)
SKIN_L = (252, 214, 186)
HAIR = (60, 38, 26)
YEL = (255, 225, 80, 255)
MAG = (255, 95, 215)          # líneas de Blaschko (holograma)
MAG_L = (255, 200, 245)
SPOT = (178, 92, 78)          # manchas sobre la piel


def P2(**kw):
    kw.setdefault('skin', SKIN); kw.setdefault('hair', HAIR)
    return P(**kw)


# ==================================================================== ARTE: brazo
ARM_CY = 1120


def _arm_shape(d, s=1, fill=255, grow=0):
    def Q(x, y): return (x * s, y * s)
    g = grow
    # antebrazo (entra desde la izquierda) + mano a la derecha
    d.polygon([Q(-40, ARM_CY - 150 - g), Q(700, ARM_CY - 118 - g), Q(760, ARM_CY - 110 - g), Q(760, ARM_CY + 110 + g),
               Q(700, ARM_CY + 120 + g), Q(-40, ARM_CY + 160 + g)], fill=fill)
    d.ellipse([(700 - g) * s, (ARM_CY - 150 - g) * s, (930 + g) * s, (ARM_CY + 150 + g) * s], fill=fill)
    for i, (y, ln) in enumerate(((-105, 150), (-38, 175), (30, 165), (95, 130))):
        d.rounded_rectangle([(880 - g) * s, (ARM_CY + y - 30 - g) * s, (880 + ln + g) * s, (ARM_CY + y + 30 + g) * s], (30 + g) * s, fill=fill)
    d.line([Q(760, ARM_CY - 120), Q(840, ARM_CY - 205), Q(905, ARM_CY - 225)], fill=fill, width=int((62 + 2 * g) * s), joint='curve')
    d.ellipse([(870 - 31 - g) * s, (ARM_CY - 225 - 31 - g) * s, (910 + 31 + g) * s, (ARM_CY - 225 + 31 + g) * s], fill=fill)


@lru_cache(maxsize=1)
def arm_mask():
    m = Image.new('L', (W * 2, H * 2), 0)
    _arm_shape(ImageDraw.Draw(m), 2)
    return m.resize((W, H), Image.LANCZOS)


@lru_cache(maxsize=1)
def arm_layer():
    """brazo de piel lisa (uniforme)"""
    L = layer()
    out = Image.new('L', (W * 2, H * 2), 0); _arm_shape(ImageDraw.Draw(out), 2, grow=5)
    out = out.resize((W, H), Image.LANCZOS)
    L.paste(Image.new('RGBA', (W, H), SKIN_D + (255,)), (0, 0), out)
    sk = vgrad((W, H), SKIN_L + (255,), SKIN + (255,))
    L.paste(sk, (0, 0), arm_mask())
    # sombra inferior + brillo superior
    sh = layer(); sd = ImageDraw.Draw(sh)
    sd.rectangle([0, ARM_CY + 60, W, ARM_CY + 200], fill=SKIN_D + (150,))
    sd.rectangle([0, ARM_CY - 150, W, ARM_CY - 95], fill=(255, 240, 225, 120))
    sh = blur(sh, 30)
    t = layer(); t.paste(sh, (0, 0), arm_mask()); L.alpha_composite(t)
    d = ImageDraw.Draw(L)
    for i, (y, ln) in enumerate(((-105, 150), (-38, 175), (30, 165), (95, 130))):
        x = 880 + ln - 34
        d.rounded_rectangle([x - 4, ARM_CY + y - 20, x + 26, ARM_CY + y + 20], 12, fill=(255, 228, 214, 255))
    return L


def arm_stripe_paths():
    out = []
    for j in range(7):
        y0 = ARM_CY - 120 + j * 40
        pts = []
        for i in range(60):
            x = -40 + i * 15
            y = y0 + 22 * math.sin(x / 210 + j * 0.9) + (y0 - ARM_CY) * 0.0005 * x
            pts.append((x, y))
        out.append(pts)
    return out


@lru_cache(maxsize=4)
def arm_stripes(kind='glow'):
    """rayas de Blaschko sobre el brazo. kind: 'glow' (holograma) o 'spots' (manchas reales)"""
    L = layer(); d = ImageDraw.Draw(L)
    if kind == 'glow':
        for pts in arm_stripe_paths():
            d.line(pts, fill=MAG + (150,), width=26, joint='curve')
        g = blur(L, 12)
        L2 = layer(); d2 = ImageDraw.Draw(L2)
        for pts in arm_stripe_paths():
            d2.line(pts, fill=MAG_L + (255,), width=7, joint='curve')
        g.alpha_composite(L2)
    else:
        rnd = random.Random(3)
        for pts in arm_stripe_paths()[1::2]:
            for i in range(0, len(pts), 2):
                x, y = pts[i]; r = rnd.randint(9, 16)
                d.ellipse([x - r * 1.4, y - r, x + r * 1.4, y + r], fill=SPOT + (rnd.randint(150, 210),))
        g = blur(L, 3)
    out = layer(); out.paste(g, (0, 0), arm_mask())
    return out


def reveal(src, x0, x1):
    """muestra `src` sólo entre x0 y x1"""
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).rectangle([x0, 0, x1, H], fill=255)
    t = layer(); t.paste(src, (0, 0), m)
    return t


def scan_bar(img, x, alpha=1.0):
    L = layer(); d = ImageDraw.Draw(L)
    d.rectangle([x - 40, 560, x + 40, 1680], fill=(110, 220, 255, int(110 * alpha)))
    img.alpha_composite(blur(L, 24))
    d = ImageDraw.Draw(img)
    d.line([(x, 560), (x, 1680)], fill=(210, 245, 255, int(255 * alpha)), width=6)


# ==================================================================== ARTE: holograma con líneas
@lru_cache(maxsize=1)
def hb_mask():
    big = Image.new('L', (HB_W * 2, HB_H * 2), 0); d = ImageDraw.Draw(big); s = 2
    def Q(x, y): return (x * s, y * s)
    d.ellipse([195 * s, 55 * s, 365 * s, 245 * s], fill=255)
    d.rounded_rectangle([245 * s, 220 * s, 315 * s, 300 * s], 20 * s, fill=255)
    d.rounded_rectangle([130 * s, 280 * s, 430 * s, 700 * s], 70 * s, fill=255)
    d.line([Q(140, 320), Q(95, 560), Q(85, 760)], fill=255, width=58 * s, joint='curve')
    d.line([Q(420, 320), Q(465, 560), Q(475, 760)], fill=255, width=58 * s, joint='curve')
    d.line([Q(215, 660), Q(205, 1140)], fill=255, width=88 * s)
    d.line([Q(345, 660), Q(355, 1140)], fill=255, width=88 * s)
    return big.resize((HB_W, HB_H), Image.LANCZOS)


def _bez(p0, p1, p2, n=30):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
            for t in (i / (n - 1) for i in range(n))]


def lines_back():   # V en la espalda (la punta en la columna)
    out = []
    for i in range(7):
        y = 330 + i * 58
        for side in (-1, 1):
            out.append(_bez((280, y + 40), (280 + side * 70, y + 10), (280 + side * 160, y - 50)))
    return out


def lines_front():  # S en el pecho y abdomen
    out = []
    for side in (-1, 1):
        for j in range(4):
            xb = 280 + side * (28 + j * 36)
            out.append([(xb + side * 28 * math.sin((y - 300) / 400 * 2 * math.pi), y) for y in range(300, 700, 12)])
    return out


def _limb(a, b, c, off, n=40, amp=10, ph=0.0):
    pts = []
    for i in range(n):
        t = i / (n - 1)
        if t < 0.5:
            u = t * 2; x = lerp(a[0], b[0], u); y = lerp(a[1], b[1], u)
        else:
            u = (t - 0.5) * 2; x = lerp(b[0], c[0], u); y = lerp(b[1], c[1], u)
        pts.append((x + off + amp * math.sin(t * 9 + ph), y))
    return pts


def lines_limbs():  # curvas a lo largo de brazos y piernas
    out = []
    for o in (-14, 0, 14):
        out.append(_limb((140, 330), (95, 560), (85, 750), o, ph=o / 6))
        out.append(_limb((420, 330), (465, 560), (475, 750), o, ph=o / 6))
        out.append(_limb((215, 680), (210, 900), (205, 1120), o * 1.6, amp=14, ph=o / 5))
        out.append(_limb((345, 680), (350, 900), (355, 1120), o * 1.6, amp=14, ph=o / 5))
    return out


SPIRALS = [(110, 470), (450, 470), (210, 900), (350, 900)]   # remolinos en brazos y piernas
SPIRAL_HEAD = (280, 140)


def spiral_pts(cx, cy, r, turns=2.3, n=60, rot=0.0):
    return [(cx + r * (i / n) * math.cos(rot + turns * 2 * math.pi * i / n), cy + r * (i / n) * math.sin(rot + turns * 2 * math.pi * i / n)) for i in range(n + 1)]


def _partial(pts, k):
    if k >= 1: return pts
    n = max(2, int(len(pts) * k))
    return pts[:n]


def holo_lines(sets, k=1.0, alpha=1.0, col=MAG, spin=0.0):
    """capa del tamaño del holograma con las líneas dibujadas hasta la fracción k"""
    L = Image.new('RGBA', (HB_W, HB_H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    polys = []
    for s in sets:
        if s == 'back': polys += lines_back()
        elif s == 'front': polys += lines_front()
        elif s == 'limbs': polys += lines_limbs()
        elif s == 'spirals': polys += [spiral_pts(x, y, 46, rot=spin) for x, y in SPIRALS]
        elif s == 'head': polys += [spiral_pts(*SPIRAL_HEAD, 55, rot=spin)]
    if k <= 0: return L
    for p in polys:
        d.line(_partial(p, k), fill=col + (int(170 * alpha),), width=20, joint='curve')
    g = blur(L, 9)
    d = ImageDraw.Draw(g)
    for p in polys:
        d.line(_partial(p, k), fill=MAG_L + (int(255 * alpha),), width=6, joint='curve')
    out = Image.new('RGBA', (HB_W, HB_H), (0, 0, 0, 0)); out.paste(g, (0, 0), hb_mask())
    return out


HBX, HBY, HBS = 540, 1090, 1.0


def hbp(x, y, cx=HBX, cy=HBY, sc=HBS):
    return cx + (x - HB_W / 2) * sc, cy + (y - HB_H / 2) * sc


def holo_scene(t, sets=(), k=1.0, alpha=1.0, cx=HBX, cy=HBY, sc=HBS, spin=0.0, body_alpha=1.0):
    img = bg_holo().copy()
    paste(img, holo_body(), cx, cy + 6 * math.sin(t * 2), scale=sc, alpha=body_alpha)
    if sets and k > 0 and alpha > 0:
        paste(img, holo_lines(tuple(sets), round(k, 3), alpha, spin=spin), cx, cy + 6 * math.sin(t * 2), scale=sc)
    return img


def scan_line_h(img, y, x0=150, x1=930, alpha=1.0):
    L = layer(); d = ImageDraw.Draw(L)
    d.rectangle([x0, y - 30, x1, y + 30], fill=(110, 220, 255, int(90 * alpha)))
    img.alpha_composite(blur(L, 20))
    ImageDraw.Draw(img).line([(x0, y), (x1, y)], fill=(210, 245, 255, int(255 * alpha)), width=5)


# ==================================================================== ARTE: útero / feto / células
@lru_cache(maxsize=1)
def bg_womb():
    img = rgrad((W, H), (540, 1080), 900, rgba('#8e2148'), rgba('#3a0a20'))
    L = layer(); d = ImageDraw.Draw(L)
    # pared muscular a rayas alrededor
    cx, cy, R = 540, 1080, 560
    for i in range(28):
        a0 = i / 28 * 360; a1 = a0 + 360 / 28
        d.pieslice([cx - R - 120, cy - R - 120, cx + R + 120, cy + R + 120], a0, a1, fill=rgba('#d24a73') if i % 2 else rgba('#a8325a'))
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(0, 0, 0, 0))
    m = Image.new('L', (W, H), 255); ImageDraw.Draw(m).ellipse([cx - R, cy - R, cx + R, cy + R], fill=0)
    ring = layer(); ring.paste(L, (0, 0), m)
    img.alpha_composite(ring)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=rgba('#ffc2d2'), width=10)
    # líquido interior más claro
    g = layer(); ImageDraw.Draw(g).ellipse([cx - R + 30, cy - R + 30, cx + R - 30, cy + R - 30], fill=(255, 140, 180, 70))
    img.alpha_composite(blur(g, 80))
    # fuera del anillo, oscuro arriba (zona de subtítulos tranquila)
    top = vgrad((W, 520), (40, 6, 20, 235), (40, 6, 20, 0))
    img.alpha_composite(top, (0, 0))
    return img


FET_W, FET_H = 620, 640


@lru_cache(maxsize=4)
def fetus_sprite(lines=False):
    def shape(d, s, fill):
        def B(x0, y0, x1, y1): return [x0 * s, y0 * s, x1 * s, y1 * s]
        d.ellipse(B(150, 40, 420, 300), fill=fill)                    # cabeza
        d.ellipse(B(170, 200, 500, 560), fill=fill)                   # cuerpo encogido
        d.line([(300 * s, 400 * s), (230 * s, 430 * s), (270 * s, 330 * s)], fill=fill, width=46 * s, joint='curve')   # brazo
        d.ellipse(B(250, 305, 300, 350), fill=fill)
        d.line([(430 * s, 470 * s), (330 * s, 560 * s), (250 * s, 520 * s)], fill=fill, width=60 * s, joint='curve')  # pierna
        d.ellipse(B(215, 495, 280, 545), fill=fill)
    def fn(im, s):
        m = Image.new('L', im.size, 0); shape(ImageDraw.Draw(m), s, 255)
        body = Image.new('RGBA', im.size, (0, 0, 0, 0))
        body.paste(vgrad(im.size, (255, 196, 200, 255), (240, 140, 160, 255)), (0, 0), m)
        im.alpha_composite(body)
        d = ImageDraw.Draw(im)
        # brillo
        hl = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(hl).ellipse([200 * s, 70 * s, 320 * s, 150 * s], fill=(255, 255, 255, 120))
        im.alpha_composite(blur(hl, 14 * s)); d = ImageDraw.Draw(im)
        # contorno
        e = m.filter(ImageFilter.FIND_EDGES)
        oc = Image.new('RGBA', im.size, (200, 70, 110, 0)); oc.putalpha(e.point(lambda v: min(255, v * 3)))
        im.alpha_composite(oc)
        # ojo cerrado y mejilla
        d.arc([215 * s, 150 * s, 265 * s, 190 * s], 20, 160, fill=(150, 60, 80, 255), width=6 * s)
        ch = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(ch).ellipse([195 * s, 195 * s, 250 * s, 230 * s], fill=(240, 80, 110, 140))
        im.alpha_composite(blur(ch, 6 * s)); d = ImageDraw.Draw(im)
        d.arc([180 * s, 215 * s, 215 * s, 245 * s], 200, 320, fill=(160, 60, 80, 255), width=4 * s)
        if lines:   # líneas de Blaschko sobre la espalda del bebé
            L = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(L)
            for i in range(6):
                a = math.radians(-60 + i * 22)
                cx, cy = 330, 380
                pts = [((cx + (150 + 30 * math.sin(u * 3)) * math.cos(a + u * 0.6)) * s, (cy + (150 + 30 * math.sin(u * 3)) * math.sin(a + u * 0.6)) * s) for u in (j / 20 for j in range(21))]
                ld.line(pts, fill=MAG + (200,), width=14 * s, joint='curve')
            g = blur(L, 6 * s); ImageDraw.Draw(g)
            L2 = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld2 = ImageDraw.Draw(L2)
            for i in range(6):
                a = math.radians(-60 + i * 22); cx, cy = 330, 380
                pts = [((cx + (150 + 30 * math.sin(u * 3)) * math.cos(a + u * 0.6)) * s, (cy + (150 + 30 * math.sin(u * 3)) * math.sin(a + u * 0.6)) * s) for u in (j / 20 for j in range(21))]
                ld2.line(pts, fill=MAG_L + (255,), width=4 * s, joint='curve')
            g.alpha_composite(L2)
            t2 = Image.new('RGBA', im.size, (0, 0, 0, 0)); t2.paste(g, (0, 0), m); im.alpha_composite(t2)
    return ss_sprite(FET_W, FET_H, fn)


def womb(t, sc=1.0, lines_a=0.0, beat=True, cord=True):
    img = bg_womb().copy()
    hb_k = 0.5 + 0.5 * math.sin(t * 2 * math.pi * 1.6) if beat else 0
    if cord:
        d = ImageDraw.Draw(img)
        pts = [(540 + 420 * (1 - u) + 40 * math.sin(u * 8 + t * 2), 760 + 380 * u + 30 * math.cos(u * 6)) for u in (i / 30 for i in range(31))]
        d.line(pts, fill=(220, 120, 150, 255), width=34, joint='curve')
        d.line(pts, fill=(255, 175, 195, 255), width=14, joint='curve')
    s = sc * (1 + 0.012 * hb_k)
    paste(img, fetus_sprite(False), 540, 1100 + 8 * math.sin(t * 1.3), scale=s, rot=4 * math.sin(t * 0.8))
    if lines_a > 0:
        paste(img, fetus_sprite(True), 540, 1100 + 8 * math.sin(t * 1.3), scale=s, rot=4 * math.sin(t * 0.8), alpha=lines_a)
    # corazoncito que late
    if beat:
        L = layer(); ImageDraw.Draw(L).ellipse([500, 1150, 580, 1230], fill=(255, 60, 100, int(60 + 120 * hb_k)))
        img.alpha_composite(blur(L, 18))
    return img


@lru_cache(maxsize=1)
def bg_tissue():
    """interior rosa: tejido de la piel con paredes a rayas"""
    img = vgrad((W, H), rgba('#8e2148'), rgba('#5e1233'))
    d = ImageDraw.Draw(img)
    # pared superior (zona subtítulos) e inferior a rayas
    for y0, y1, flip in ((0, 560, 1), (1640, H, -1)):
        for i in range(0, W + 80, 80):
            d.polygon([(i, y0), (i + 40, y0), (i + 40 + 30 * flip, y1), (i + 30 * flip, y1)], fill=rgba('#d24a73'))
            d.polygon([(i + 40, y0), (i + 80, y0), (i + 80 + 30 * flip, y1), (i + 40 + 30 * flip, y1)], fill=rgba('#a8325a'))
    # bordes ondulados rosa claro
    top = [(x, 560 + 22 * math.sin(x / 60)) for x in range(0, W + 10, 10)]
    bot = [(x, 1640 + 22 * math.sin(x / 70 + 1)) for x in range(0, W + 10, 10)]
    d.polygon(top + [(W, 600), (W, 700), (0, 700)], fill=rgba('#8e2148'))
    d.polygon(bot + [(W, 1600), (0, 1600)], fill=rgba('#6a173c'))
    d.line(top, fill=rgba('#ffc2d2'), width=10)
    d.line(bot, fill=rgba('#ffc2d2'), width=10)
    # vellosidades
    for x in range(30, W, 90):
        d.ellipse([x - 26, 600, x + 26, 680], fill=rgba('#b03060'))
        d.ellipse([x - 26 + 45, 1560, x + 26 + 45, 1630], fill=rgba('#b03060'))
    top_dark = vgrad((W, 480), (40, 6, 20, 210), (40, 6, 20, 0))
    img.alpha_composite(top_dark, (0, 0))
    g = layer(); ImageDraw.Draw(g).ellipse([120, 760, 960, 1500], fill=(255, 120, 170, 60))
    img.alpha_composite(blur(g, 120))
    return img


@lru_cache(maxsize=8)
def cell_sprite(r=60, hue=0, blink=False):
    cols = [((255, 170, 200), (230, 90, 140)), ((255, 205, 160), (225, 130, 90)), ((235, 175, 255), (170, 90, 220))][hue % 3]
    def fn(im, s):
        c = (r + 16) * s; rr = r * s
        L = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(L).ellipse([c - rr - 8 * s, c - rr - 8 * s, c + rr + 8 * s, c + rr + 8 * s], fill=cols[0] + (110,))
        im.alpha_composite(blur(L, 8 * s))
        d = ImageDraw.Draw(im)
        d.ellipse([c - rr, c - rr, c + rr, c + rr], fill=cols[0] + (240,), outline=cols[1] + (255,), width=4 * s)
        d.ellipse([c - rr * 0.35 + rr * 0.25, c - rr * 0.1, c + rr * 0.25 + rr * 0.35, c + rr * 0.6], fill=cols[1] + (200,))   # núcleo
        for ex in (-0.32, 0.18):
            x = c + ex * rr; y = c - rr * 0.25
            if blink:
                d.line([(x - rr * 0.12, y), (x + rr * 0.12, y)], fill=(40, 20, 30, 255), width=3 * s)
            else:
                d.ellipse([x - rr * 0.13, y - rr * 0.16, x + rr * 0.13, y + rr * 0.16], fill=(255, 255, 255, 255))
                d.ellipse([x - rr * 0.07, y - rr * 0.06, x + rr * 0.07, y + rr * 0.12], fill=(30, 15, 25, 255))
                d.ellipse([x - rr * 0.06, y - rr * 0.12, x - rr * 0.0, y - rr * 0.06], fill=(255, 255, 255, 255))
        d.arc([c - rr * 0.25, c - rr * 0.05, c + rr * 0.1, c + rr * 0.22], 20, 160, fill=(120, 30, 60, 255), width=3 * s)
        hl = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(hl).ellipse([c - rr * 0.7, c - rr * 0.8, c - rr * 0.2, c - rr * 0.5], fill=(255, 255, 255, 170))
        im.alpha_composite(hl)
    return ss_sprite(2 * (r + 16), 2 * (r + 16), fn)


def cell_paths():
    """recorridos de las células: salen de la línea media (columna) y se abren en curva"""
    out = []
    for j in range(5):
        y0 = 760 + j * 190
        for side in (-1, 1):
            out.append(_bez((540, y0), (540 + side * 250, y0 - 40), (540 + side * 470, y0 + 120), n=50))
    return out


def tissue_trails(img, k, alpha=1.0):
    L = layer(); d = ImageDraw.Draw(L)
    for p in cell_paths():
        d.line(_partial(p, k), fill=MAG + (int(150 * alpha),), width=34, joint='curve')
    g = blur(L, 14); d = ImageDraw.Draw(g)
    for p in cell_paths():
        d.line(_partial(p, k), fill=MAG_L + (int(230 * alpha),), width=8, joint='curve')
    img.alpha_composite(g)


# ==================================================================== ARTE: iconos
@lru_cache(maxsize=1)
def scientist(pointing=True, mouth='smile'):
    spr = P2(shirt=(245, 248, 252), mouth=mouth, cheeks=0.5, brows='raised', arms='down', hair=(90, 90, 95)).copy()
    d = ImageDraw.Draw(spr)
    for x in (255, 385):   # gafas
        d.ellipse([x - 44, 220, x + 44, 306], outline=(40, 40, 60, 255), width=8)
    d.line([(299, 258), (341, 258)], fill=(40, 40, 60, 255), width=8)
    d.polygon([(260, 470), (320, 640), (380, 470)], fill=(120, 190, 240, 255))    # camisa debajo de la bata
    d.line([(320, 470), (320, 1000)], fill=(210, 215, 225, 255), width=6)
    return spr


@lru_cache(maxsize=1)
def board_sprite():
    w, h = 520, 640
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, w * s - 1, h * s - 1], 30 * s, fill=(30, 60, 70, 255), outline=(200, 170, 120, 255), width=14 * s)
        # silueta
        cx = w / 2
        def B(x0, y0, x1, y1): return [x0 * s, y0 * s, x1 * s, y1 * s]
        sil = (230, 240, 240, 255)
        d.ellipse(B(cx - 50, 60, cx + 50, 160), outline=sil, width=6 * s)
        d.rounded_rectangle(B(cx - 95, 170, cx + 95, 430), 40 * s, outline=sil, width=6 * s)
        d.line([(cx - 95) * s, 200 * s, (cx - 150) * s, 400 * s], fill=sil, width=6 * s)
        d.line([(cx + 95) * s, 200 * s, (cx + 150) * s, 400 * s], fill=sil, width=6 * s)
        d.line([(cx - 50) * s, 430 * s, (cx - 60) * s, 600 * s], fill=sil, width=6 * s)
        d.line([(cx + 50) * s, 430 * s, (cx + 60) * s, 600 * s], fill=sil, width=6 * s)
        for i in range(5):   # V con tiza rosa
            y = 210 + i * 42
            d.line([((cx - 80) * s, (y - 30) * s), (cx * s, y * s), ((cx + 80) * s, (y - 30) * s)], fill=(255, 150, 220, 255), width=6 * s, joint='curve')
    return ss_sprite(w, h, fn)


@lru_cache(maxsize=1)
def pencil_sprite():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.polygon([(20 * s, 300 * s), (60 * s, 240 * s), (90 * s, 270 * s)], fill=(250, 220, 170, 255))
        d.polygon([(20 * s, 300 * s), (36 * s, 276 * s), (46 * s, 286 * s)], fill=(255, 95, 215, 255))
        d.polygon([(60 * s, 240 * s), (90 * s, 270 * s), (280 * s, 80 * s), (250 * s, 50 * s)], fill=(255, 200, 60, 255))
        d.polygon([(250 * s, 50 * s), (280 * s, 80 * s), (300 * s, 60 * s), (270 * s, 30 * s)], fill=(200, 200, 210, 255))
        d.polygon([(270 * s, 30 * s), (300 * s, 60 * s), (318 * s, 42 * s), (288 * s, 12 * s)], fill=(255, 130, 150, 255))
    return ss_sprite(330, 320, fn)


@lru_cache(maxsize=4)
def dice_sprite(face=5):
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([10 * s, 10 * s, 250 * s, 250 * s], 46 * s, fill=(255, 255, 255, 255), outline=(200, 190, 220, 255), width=6 * s)
        pts = {1: [(130, 130)], 2: [(80, 80), (180, 180)], 3: [(75, 75), (130, 130), (185, 185)], 4: [(80, 80), (180, 80), (80, 180), (180, 180)],
               5: [(75, 75), (185, 75), (130, 130), (75, 185), (185, 185)], 6: [(80, 70), (180, 70), (80, 130), (180, 130), (80, 190), (180, 190)]}[face]
        for x, y in pts:
            d.ellipse([(x - 20) * s, (y - 20) * s, (x + 20) * s, (y + 20) * s], fill=(40, 30, 60, 255))
    return ss_sprite(260, 260, fn)


@lru_cache(maxsize=1)
def eye_icon():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.chord([10 * s, 30 * s, 290 * s, 250 * s], 200, 340, fill=(255, 255, 255, 255))
        d.chord([10 * s, -30 * s, 290 * s, 190 * s], 20, 160, fill=(255, 255, 255, 255))
        d.ellipse([105 * s, 65 * s, 195 * s, 155 * s], fill=(70, 140, 220, 255))
        d.ellipse([130 * s, 90 * s, 170 * s, 130 * s], fill=(20, 15, 30, 255))
        d.ellipse([135 * s, 88 * s, 152 * s, 105 * s], fill=(255, 255, 255, 255))
    return glow_sprite(ss_sprite(300, 220, fn), 10, (150, 200, 255, 140))


@lru_cache(maxsize=1)
def lock_sprite():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.arc([50 * s, 10 * s, 190 * s, 170 * s], 180, 360, fill=(220, 230, 255, 255), width=24 * s)
        d.line([(62 * s, 90 * s), (62 * s, 130 * s)], fill=(220, 230, 255, 255), width=24 * s)
        d.line([(178 * s, 90 * s), (178 * s, 130 * s)], fill=(220, 230, 255, 255), width=24 * s)
        d.rounded_rectangle([20 * s, 120 * s, 220 * s, 290 * s], 30 * s, fill=(70, 120, 240, 255), outline=(200, 220, 255, 255), width=6 * s)
        d.ellipse([100 * s, 170 * s, 140 * s, 210 * s], fill=(20, 30, 70, 255))
        d.rectangle([112 * s, 200 * s, 128 * s, 245 * s], fill=(20, 30, 70, 255))
    return glow_sprite(ss_sprite(240, 300, fn), 12, (100, 160, 255, 170))


@lru_cache(maxsize=1)
def fingerprint_sprite():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        c = 150
        for i in range(9):
            r = 18 + i * 14
            d.arc([(c - r) * s, (c - r * 1.25) * s, (c + r) * s, (c + r * 1.25) * s], 200 - i * 4, 340 + i * 6 + (30 if i % 2 else 0), fill=MAG_L + (255,), width=6 * s)
    return glow_sprite(ss_sprite(300, 340, fn), 14, MAG + (200,))


def qmarks(img, t, t0, pos, size=120):
    for i, (x, y) in enumerate(pos):
        if t >= t0 + i * 0.12:
            paste(img, label('?', size, fill=YEL, stroke=10), x, y + 8 * math.sin(t * 6 + i), scale=pop(t, t0 + i * 0.12), rot=-12 + 12 * i)


def bigx(img, cx, cy, r, k):
    if k <= 0: return
    d = ImageDraw.Draw(img)
    a = r * ease_back(min(1, k))
    L = layer(); ld = ImageDraw.Draw(L)
    ld.line([(cx - a, cy - a), (cx + a, cy + a)], fill=(255, 40, 70, 160), width=70)
    ld.line([(cx + a, cy - a), (cx - a, cy + a)], fill=(255, 40, 70, 160), width=70)
    img.alpha_composite(blur(L, 16))
    d.line([(cx - a, cy - a), (cx + a, cy + a)], fill=(240, 40, 70, 255), width=38)
    d.line([(cx + a, cy - a), (cx - a, cy + a)], fill=(240, 40, 70, 255), width=38)


def shake(t, t0, dur=0.35, amp=14):
    k = prog(t, t0, dur)
    if k <= 0 or k >= 1: return 0, 0
    a = amp * (1 - k)
    return a * math.sin(t * 90), a * math.cos(t * 77)


# ==================================================================== ESCENAS
# cada escena: f(t) -> (imagen RGBA, zoom, (cx, cy))
def arm_bg():
    return bg_teal()


def sc_hook(t):   # Tu piel parece uniforme…
    tp, tu = T('piel', 0.28), T('uniforme', 1.03)
    img = arm_bg().copy()
    float_bubbles(img, t, n=7, seed=2, rmin=14, rmax=34, area=(0, 560, W, 1800), speed=40, alpha=0.4)
    img.alpha_composite(arm_layer())
    if t >= tp:
        sparkle(img, 420, 1060, 34 * pop(t, tp)); sparkle(img, 620, 1170, 24 * pop(t, tp + 0.1))
    if t >= tu:
        paste(img, label('LISA', 130, fill=(255, 255, 255, 255), stroke=11), 540, 760, scale=pop(t, tu), rot=-4)
        paste(img, check_badge(48, True), 850, 760, scale=pop(t, tu + 0.12))
    z = lerp(1.0, 1.08, ease_in_out(prog(t, 0, 1.4)))
    return img, z, (560, 1120)


def sc_hook2(t):   # pero en realidad tiene un mapa oculto.
    tr, tm, to = T('realidad', 1.92), T('mapa', 2.80), T('oculto', 2.87)
    img = arm_bg().copy()
    img.alpha_composite(arm_layer())
    xs = lerp(-60, 1100, ease_in_out(prog(t, tr - 0.1, 0.9)))
    # tinte azul holograma donde ya pasó el escáner
    tint = layer(); tint.paste(Image.new('RGBA', (W, H), (40, 90, 200, 110)), (0, 0), arm_mask())
    img.alpha_composite(reveal(tint, -100, xs))
    img.alpha_composite(reveal(arm_stripes('glow'), -100, xs))
    if xs < 1090: scan_bar(img, xs)
    if t >= tm:
        paste(img, label('MAPA OCULTO', 112, fill=YEL, stroke=11), 540, 760, scale=pop(t, tm + 0.05), rot=-4)
    if t >= to + 0.15:
        paste(img, alert_badge(50), 900, 640, scale=pop(t, to + 0.15))
    if tm <= t < tm + 0.18:
        img = glitch(img, t)
    dx, dy = shake(t, tm, 0.4, 10)
    z = 1.08 + 0.06 * ease_out(prog(t, tm, 0.5))
    return img, z, (560 + dx, 1120 + dy)


def sc_rayas(t):   # Un mapa de rayas invisibles que recorre tu cuerpo
    tr, ti, tq, tc = T('rayas', 3.82), T('invisibles', 4.20), T('recorre', 5.00), T('cuerpo', 5.54)
    k = ease_in_out(prog(t, tr - 0.1, (tc + 0.3) - tr))
    # "invisibles": parpadean como si se apagaran
    a = 1.0
    if ti <= t < tq:
        a = 0.25 + 0.75 * (0.5 + 0.5 * math.cos((t - ti) * 18)) * (1 - prog(t, ti, 0.6) * 0.6)
    img = holo_scene(t, ('back', 'limbs'), k, a)
    if t >= tr:
        paste(img, pill('RAYAS', (200, 50, 170), 56), 540, 600, scale=pop(t, tr))
    if t >= ti:
        paste(img, label('INVISIBLES', 96, fill=(200, 235, 255, 255), stroke=9), 540, 720, scale=pop(t, ti), alpha=0.55 + 0.45 * abs(math.sin(t * 9)))
    sy = lerp(450, 1690, prog(t, tq, 0.9))
    if tq <= t < tq + 0.9: scan_line_h(img, sy)
    z = lerp(1.0, 1.08, ease_in_out(prog(t, 3.2, 2.6)))
    return img, z, (540, 1080)


def sc_antes(t):   # desde antes de que nacieras.
    td, tn = T('desde', 5.92), T('nacieras', 6.66)
    img = womb(t, sc=lerp(0.85, 1.0, ease_out(prog(t, td, 0.6))), lines_a=ease_out(prog(t, tn, 0.4)))
    if t >= td:
        paste(img, pill('ANTES DE NACER', (220, 50, 110), 56), 540, 600, scale=pop(t, td + 0.1))
    if t >= tn:
        for i in range(4):
            a = i / 4 * 2 * math.pi + t
            sparkle(img, 540 + 330 * math.cos(a), 1100 + 330 * math.sin(a), 28 * pop(t, tn + i * 0.05))
    z = lerp(1.06, 1.0, ease_out(prog(t, td - 0.1, 0.5)))
    return img, z, (540, 1100)


def sc_teoria(t):   # Y no, no es una teoría rara.
    tn, tt, tr = T('no', 7.32), T('teoria', 8.00), T('rara', 8.40)
    img = bg_purple().copy()
    float_bubbles(img, t, n=7, seed=5, rmin=16, rmax=40, area=(0, 560, W, 1800), speed=50, alpha=0.5)
    sh = math.sin((t - tn) * 22) * 18 * (1 - prog(t, tn, 0.7)) if t >= tn else 0
    spr = P2(shirt=(70, 130, 220), mouth='smile', cheeks=0.6, brows='raised', eyes='closed' if tn <= t < tn + 0.5 else 'open')
    paste(img, spr, 540 + sh, 1420, scale=1.4, rot=-sh * 0.4)
    if t >= tt:
        paste(img, pill('¿TEORÍA RARA?', (110, 70, 180), 58), 540, 700, scale=pop(t, tt))
    if t >= tr:
        bigx(img, 540, 700, 130, prog(t, tr, 0.25))
    dx, dy = shake(t, tr, 0.35, 12)
    return img, 1.0 + 0.05 * prog(t, 7.1, 1.5), (540 + dx, 1150 + dy)


def counter(img, t, t0, dur, val, x, y, size=150, fmt='{:d}'):
    k = ease_out(prog(t, t0, dur))
    v = int(round(val * k))
    paste(img, label(fmt.format(v), size, fill=YEL, stroke=12), x, y, scale=pop(t, t0, 0.25))


def sc_cientificos(t):   # Los científicos las conocen como líneas de Blaschko.
    tc, tl, tb = T('cientificos', 9.00), T('lineas', 10.31), T('blaschko', 10.92)
    img = bg_teal().copy()
    float_bubbles(img, t, n=6, seed=8, rmin=14, rmax=30, area=(0, 560, W, 1800), speed=40, alpha=0.35)
    paste(img, board_sprite(), 720, 1050 + 4 * math.sin(t * 2), scale=0.95 * pop(t, tc - 0.05, 0.3))
    paste(img, scientist(), 300, 1460, scale=1.15)
    if t >= tl:
        paste(img, pill('LÍNEAS DE', (200, 50, 170), 50), 540, 600, scale=pop(t, tl))
    if t >= tb:
        paste(img, label('BLASCHKO', 140, fill=YEL, stroke=13), 540, 720, scale=pop(t, tb, 0.3), rot=-3)
        for i in range(5):
            a = i / 5 * 2 * math.pi
            sparkle(img, 540 + 420 * math.cos(a), 720 + 120 * math.sin(a), 26 * (1 - prog(t, tb, 0.8)))
    if tb <= t < tb + 0.16:
        img = glitch(img, t)
    z = 1.0 + 0.07 * ease_out(prog(t, tb, 0.4))
    return img, z, (540, 1000)


def sc_1901(t):   # Son patrones naturales  (dato: descritas en 1901)
    ts, tp, tn = T('son', 11.39), T('patrones', 11.84), T('naturales', 12.30)
    img = holo_scene(t, ('back', 'front', 'limbs', 'spirals'), ease_in_out(prog(t, ts, 1.2)), 0.9, spin=t * 0.8, sc=0.82, cy=1180, body_alpha=0.9)
    counter(img, t, ts, 0.9, 1901, 540, 680, 170)
    paste(img, pill('DESCRITAS EN', (40, 120, 240), 44), 540, 560, scale=pop(t, ts))
    if t >= tn:
        paste(img, pill('NATURALES', (46, 170, 100), 52), 820, 860, scale=pop(t, tn), rot=6)
        paste(img, check_badge(40, True), 250, 860, scale=pop(t, tn + 0.1))
    return img, 1.0 + 0.05 * prog(t, ts, 1.4), (540, 1100)


def sc_celulas(t):   # que siguen el recorrido que hicieron tus células de la piel
    tsig, trec, tcel, tpiel = T('siguen', 13.00), T('recorrido', 13.42), T('celulas', 14.66), T('piel', 15.12)
    img = bg_tissue().copy()
    k = ease_in_out(prog(t, tsig, (tpiel + 0.3) - tsig))
    tissue_trails(img, k)
    paths = cell_paths()
    for i, p in enumerate(paths):
        q = p[min(len(p) - 1, int(k * (len(p) - 1)))]
        bob = 6 * math.sin(t * 10 + i)
        paste(img, cell_sprite(46, i % 3, blink=(int(t * 3 + i) % 7 == 0)), q[0], q[1] + bob, scale=pop(t, tsig - 0.1 + (i % 5) * 0.04))
    # columna (línea media) de donde salen
    d = ImageDraw.Draw(img)
    d.line([(540, 700), (540, 1600)], fill=(255, 194, 210, 120), width=8)
    if t >= trec:
        paste(img, pill('RECORRIDO', (200, 50, 170), 52), 540, 600, scale=pop(t, trec))
    if t >= tcel:
        paste(img, label('CÉLULAS', 120, fill=YEL, stroke=11), 540, 720, scale=pop(t, tcel), rot=-3)
    z = lerp(1.0, 1.1, ease_in_out(prog(t, tsig, 2.5)))
    return img, z, (540, 1150)


def sc_vientre(t):   # mientras te estabas formando dentro del vientre.
    tf, tv = T('formando', 16.40), T('vientre', 17.30)
    grow = ease_out(prog(t, tf - 0.3, 0.9))
    img = womb(t, sc=lerp(0.55, 1.0, grow), lines_a=ease_in_out(prog(t, tf, 0.8)))
    if t >= tf:
        paste(img, pill('FORMÁNDOTE', (220, 50, 110), 54), 540, 600, scale=pop(t, tf))
    if t >= tv:
        paste(img, label('EN EL VIENTRE', 100, fill=YEL, stroke=10), 540, 720, scale=pop(t, tv), rot=-3)
    z = lerp(1.15, 1.0, ease_out(prog(t, 15.4, 1.0)))
    return img, z, (540, 1100)


def sc_extrano(t):   # Lo más extraño es que casi nunca puedes verlas a simple vista.
    te, tn, tv, tsv = T('extrano', 18.24), T('nunca', 19.20), T('verlas', 19.84), T('vista', 20.82)
    img = bg_purple().copy()
    float_bubbles(img, t, n=7, seed=9, rmin=16, rmax=36, area=(0, 560, W, 1800), speed=40, alpha=0.4)
    look = (1, 1) if t >= tv else (0, 0)
    spr = P2(shirt=(236, 92, 70), mouth='side' if t < tv else 'o', brows='worried' if t >= tn else 'raised', cheeks=0.5, look=look, sweat=t >= tv)
    paste(img, spr, 400, 1450, scale=1.3)
    # su brazo (piel lisa) a la derecha
    if t >= te:
        paste(img, label('¡QUÉ RARO!', 104, fill=YEL, stroke=10), 540, 650, scale=pop(t, te), rot=-5)
    if t >= tv:
        paste(img, eye_icon(), 790, 980, scale=pop(t, tv))
    if t >= tsv:
        paste(img, check_badge(60, False), 900, 900, scale=pop(t, tsv))
        paste(img, pill('A SIMPLE VISTA', (110, 70, 180), 44), 790, 1170, scale=pop(t, tsv + 0.05))
    z = 1.0 + 0.06 * ease_out(prog(t, tv, 0.5))
    return img, z, (540, 1150)


def sc_escondidas(t):   # Están ahí… pero permanecen escondidas.
    ta, tpe, tes = T('ahi', 21.52), T('permanecen', 22.08), T('escondidas', 22.56)
    a = 1.0 if t < tpe else 1 - 0.85 * ease_in_out(prog(t, tpe, 0.7))
    img = holo_scene(t, ('back', 'limbs', 'head'), ease_out(prog(t, 21.0, 0.5)), a)
    if t >= ta:
        paste(img, pill('ESTÁN AHÍ', (46, 170, 100), 56), 540, 600, scale=pop(t, ta))
    if t >= tes:
        paste(img, lock_sprite(), 830, 780, scale=0.75 * pop(t, tes))
        paste(img, label('ESCONDIDAS', 110, fill=(200, 235, 255, 255), stroke=10), 470, 760, scale=pop(t, tes + 0.05), rot=-3)
    return img, 1.0 + 0.06 * prog(t, 21.0, 2.6), (540, 1100)


def sc_como(t):   # Entonces, ¿cómo sabemos que existen?
    tc, ts, tex = T('como', 24.07), T('sabemos', 24.58), T('existen', 25.04)
    img = bg_teal().copy()
    float_bubbles(img, t, n=8, seed=11, rmin=14, rmax=36, area=(0, 560, W, 1800), speed=50, alpha=0.45)
    spr = P2(shirt=(70, 130, 220), mouth='side', brows='worried', cheeks=0.4, look=(1, -1))
    paste(img, spr, 540, 1480, scale=1.35)
    qmarks(img, t, tc, ((800, 760), (290, 840), (880, 1020)))
    if t >= tex:
        paste(img, label('¿EXISTEN?', 120, fill=YEL, stroke=11), 540, 660, scale=pop(t, tex), rot=-4)
    if tex <= t < tex + 0.16:
        img = glitch(img, t)
    z = 1.0 + 0.08 * ease_out(prog(t, ts, 0.5))
    return img, z, (540, 1180)


def sc_enfermedades(t):   # Porque en algunas enfermedades de la piel,
    te, tp = T('enfermedades', 26.52), T('piel', 27.32)
    img = arm_bg().copy()
    img.alpha_composite(arm_layer())
    lx = lerp(300, 560, ease_in_out(prog(t, 25.5, 1.6)))
    # lupa de rayos X: dentro se ven las rayas
    r = 210
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).ellipse([lx - r, ARM_CY - r, lx + r, ARM_CY + r], fill=255)
    inside = layer(); inside.paste(Image.new('RGBA', (W, H), (20, 50, 110, 220)), (0, 0), m)
    st = layer(); st.paste(arm_stripes('glow'), (0, 0), m)
    img.alpha_composite(inside); img.alpha_composite(st)
    d = ImageDraw.Draw(img)
    d.ellipse([lx - r, ARM_CY - r, lx + r, ARM_CY + r], outline=(170, 235, 255, 255), width=12)
    d.line([(lx + r * 0.7, ARM_CY + r * 0.7), (lx + r * 1.35, ARM_CY + r * 1.35)], fill=(60, 70, 100, 255), width=50)
    if t >= te:
        paste(img, alert_badge(52), 880, 760, scale=pop(t, te))
        paste(img, pill('ENFERMEDADES DE LA PIEL', (220, 40, 70), 46), 500, 620, scale=pop(t, te + 0.05))
    return img, 1.0 + 0.05 * prog(t, 25.5, 2.0), (540, 1120)


def sc_manchas(t):   # ciertas manchas, erupciones o cambios de color
    tm, te, tc, tco = T('manchas', 28.12), T('erupciones', 28.67), T('cambios', 29.74), T('color', 30.22)
    img = arm_bg().copy()
    img.alpha_composite(arm_layer())
    sp = arm_stripes('spots')
    k = ease_in_out(prog(t, tm, (tco + 0.3) - tm))
    img.alpha_composite(reveal(sp, -100, lerp(-100, 1100, k)))
    for i, (tt, txt, col, x, y) in enumerate(((tm, 'MANCHAS', (180, 90, 70), 300, 620), (te, 'ERUPCIONES', (220, 40, 70), 720, 700),
                                             (tc, 'CAMBIOS DE COLOR', (200, 50, 170), 540, 800))):
        if t >= tt:
            paste(img, pill(txt, col, 46), x, y, scale=pop(t, tt), rot=(-4, 4, -2)[i])
    return img, lerp(1.0, 1.08, ease_in_out(prog(t, tm, 2.4))), (560, 1100)


def sc_siguiendo(t):   # aparecen siguiendo exactamente esas mismas líneas,
    ta, tsi, tex, tl = T('aparecen', 30.56), T('siguiendo', 31.04), T('exactamente', 31.88), T('lineas', 32.86)
    img = arm_bg().copy()
    img.alpha_composite(arm_layer())
    img.alpha_composite(arm_stripes('spots'))
    k = ease_in_out(prog(t, tsi, (tl + 0.2) - tsi))
    if k > 0:
        gl = arm_stripes('glow')
        img.alpha_composite(reveal(gl, -100, lerp(-100, 1100, k)))
    if t >= tex:
        paste(img, label('EXACTAMENTE', 110, fill=YEL, stroke=11), 540, 660, scale=pop(t, tex), rot=-3)
    if t >= tl:
        paste(img, check_badge(54, True), 880, 800, scale=pop(t, tl))
        paste(img, pill('MISMAS LÍNEAS', (200, 50, 170), 50), 480, 800, scale=pop(t, tl + 0.05))
    return img, 1.08 + 0.05 * ease_out(prog(t, tex, 0.4)), (560, 1100)


def sc_dibujado(t):   # como si alguien hubiera dibujado un mapa secreto sobre el cuerpo.
    tdi, tma, tse, tcu = T('dibujado', 34.58), T('mapa', 35.12), T('secreto', 35.46), T('cuerpo', 36.36)
    k = ease_in_out(prog(t, T('alguien', 33.88), (tcu + 0.2) - T('alguien', 33.88)))
    img = holo_scene(t, ('back',), k, 1.0)
    # el lápiz sigue la punta de la línea que se está dibujando
    lb = lines_back()
    idx = min(len(lb) - 1, int(k * len(lb)))
    p = lb[idx]
    sub = (k * len(lb)) % 1
    q = p[min(len(p) - 1, int(sub * (len(p) - 1)))]
    # holo_lines dibuja todas a la vez: el lápiz recorre la línea según k
    q = lb[(int(t * 5)) % len(lb)][min(29, int(k * 29))]
    x, y = hbp(*q)
    if k < 1:
        paste(img, pencil_sprite(), x + 150, y - 140, scale=0.9)
    if t >= tma:
        paste(img, label('MAPA SECRETO', 106, fill=YEL, stroke=11), 540, 640, scale=pop(t, tma), rot=-3)
    if t >= tcu:
        paste(img, fingerprint_sprite(), 870, 1500, scale=0.6 * pop(t, tcu))
    return img, 1.0 + 0.06 * prog(t, 33.3, 3.2), (540, 1050)


def sc_rectas(t):   # Y ese mapa no forma líneas rectas.  (+ botón Sígueme)
    tno, tl, tr = T('no', 37.24), T('lineas', 37.72), T('rectas', 38.30)
    img = bg_purple().copy()
    float_bubbles(img, t, n=6, seed=4, rmin=14, rmax=34, area=(0, 560, W, 1800), speed=40, alpha=0.4)
    d = ImageDraw.Draw(img)
    ks = ease_out(prog(t, T('mapa', 37.04) - 0.1, 0.45))
    # regla + línea recta
    if ks > 0:
        d.rounded_rectangle([140, 1010, 140 + 800 * ks, 1090], 14, fill=(255, 210, 90, 255), outline=(150, 100, 30, 255), width=5)
        for i in range(0, int(800 * ks), 40):
            d.line([(150 + i, 1010), (150 + i, 1010 + (34 if i % 200 == 0 else 18))], fill=(150, 100, 30, 255), width=4)
        d.line([(140, 1150), (140 + 800 * ks, 1150)], fill=(255, 255, 255, 255), width=14)
    if t >= tr:
        bigx(img, 540, 1110, 170, prog(t, tr, 0.25))
    # la línea curva de verdad
    kc = ease_in_out(prog(t, tr + 0.15, 0.6))
    if kc > 0:
        pts = [(140 + 800 * u, 1380 + 90 * math.sin(u * 2 * math.pi * 1.5)) for u in (i / 60 for i in range(61))]
        L = layer(); ImageDraw.Draw(L).line(_partial(pts, kc), fill=MAG + (170,), width=34, joint='curve')
        img.alpha_composite(blur(L, 12))
        ImageDraw.Draw(img).line(_partial(pts, kc), fill=MAG_L + (255,), width=12, joint='curve')
    if t >= tl:
        paste(img, label('NO SON RECTAS', 110, fill=YEL, stroke=11), 540, 700, scale=pop(t, tl), rot=-3)
    # CTA a mitad del video
    tb = T('ese', 36.76)
    paste(img, follow_button(), 540, 1650 + 6 * math.sin(t * 5), scale=pop(t, tb, 0.3))
    dx, dy = shake(t, tr, 0.35, 12)
    return img, 1.0, (540 + dx, 1100 + dy)


def big_letter(img, t, t0, ch, x, y):
    if t < t0: return
    paste(img, label(ch, 300, fill=YEL, stroke=18), x, y, scale=pop(t, t0, 0.3) * (1 + 0.03 * math.sin(t * 8)), rot=-6)


def sc_espalda(t):   # En la espalda parece una V.
    tes, tv = T('espalda', 38.96), T('v', 39.82)
    k = ease_in_out(prog(t, tes - 0.1, 0.8))
    img = holo_scene(t, ('back',), k, 1.0)
    paste(img, pill('ESPALDA', (40, 120, 240), 56), 540, 600, scale=pop(t, tes))
    big_letter(img, t, tv, 'V', 860, 760)
    z = lerp(1.0, 1.35, ease_in_out(prog(t, tes, 0.9)))
    return img, z, (540, 900)


def sc_pecho(t):   # En el pecho, una S.
    tpe, ts = T('pecho', 40.36), T('s', 41.24)
    k = ease_in_out(prog(t, tpe - 0.1, 0.7))
    img = holo_scene(t, ('front',), k, 1.0)
    paste(img, pill('PECHO', (40, 120, 240), 56), 540, 600, scale=pop(t, tpe))
    big_letter(img, t, ts, 'S', 860, 760)
    z = lerp(1.0, 1.35, ease_in_out(prog(t, tpe, 0.7)))
    return img, z, (540, 950)


def sc_espirales(t):   # Y en brazos y piernas, curvas y espirales.
    tb, tpi, tcu, tesp = T('brazos', 41.72), T('piernas', 42.20), T('curvas', 42.78), T('espirales', 43.22)
    img = holo_scene(t, ('limbs',), ease_in_out(prog(t, tb - 0.1, (tcu + 0.3) - tb)), 1.0)
    if t >= tesp:
        sp = holo_lines(('spirals', 'head'), ease_out(prog(t, tesp, 0.5)), 1.0, spin=(t - tesp) * 3)
        paste(img, sp, HBX, HBY + 6 * math.sin(t * 2))
    if t >= tb: paste(img, pill('BRAZOS', (40, 120, 240), 46), 250, 640, scale=pop(t, tb))
    if t >= tpi: paste(img, pill('PIERNAS', (40, 120, 240), 46), 830, 640, scale=pop(t, tpi))
    if t >= tcu: paste(img, label('CURVAS', 96, fill=YEL, stroke=10), 230, 1350, scale=pop(t, tcu), rot=-8)
    if t >= tesp: paste(img, label('ESPIRALES', 96, fill=YEL, stroke=10), 830, 1350, scale=pop(t, tesp), rot=7)
    return img, 1.0 + 0.04 * prog(t, 41.4, 2.4), (540, 1080)


def sc_azar(t):   # O sea: tu piel no se construyó al azar.
    tc, taz = T('construyo', 45.30), T('azar', 45.80)
    img = bg_teal().copy()
    float_bubbles(img, t, n=7, seed=13, rmin=14, rmax=34, area=(0, 560, W, 1800), speed=40, alpha=0.4)
    # dados rodando
    for i, (x, f) in enumerate(((360, 5), (700, 3))):
        k = prog(t, 43.9 + i * 0.1, 1.2)
        rot = (1 - ease_out(k)) * 720 * (1 if i else -1)
        y = 1150 - 260 * abs(math.sin(k * math.pi * 2)) * (1 - k)
        face = [1, 4, 2, 6, 3, f][min(5, int(k * 6))]
        paste(img, dice_sprite(face), x, y, scale=1.0, rot=rot)
    if t >= taz:
        bigx(img, 530, 1150, 300, prog(t, taz, 0.25))
        paste(img, label('NO ES AL AZAR', 110, fill=YEL, stroke=11), 540, 680, scale=pop(t, taz + 0.05), rot=-3)
    elif t >= tc:
        paste(img, pill('¿AL AZAR?', (110, 70, 180), 56), 540, 680, scale=pop(t, tc))
    dx, dy = shake(t, taz, 0.35, 14)
    return img, 1.0, (540 + dx, 1100 + dy)


def sc_inicio(t):   # Siguió un patrón desde el inicio de tu vida.
    tp, ti, tv = T('patron', 46.76), T('inicio', 47.38), T('vida', 48.14)
    img = bg_tissue().copy()
    # una célula que se divide: 1 -> 2 -> 4 -> 8, colocadas siguiendo un patrón en V
    stage = 0 + (t >= tp) + (t >= ti) + (t >= tv)
    n = 2 ** stage
    k = ease_back(prog(t, [46.10, tp, ti, tv][stage], 0.35), 1.6)
    pos = []
    for i in range(n):
        if n == 1: pos.append((540, 1100))
        else:
            row = i // 2; side = -1 if i % 2 == 0 else 1
            rows = max(1, n // 2)
            y = 1100 + (row - (rows - 1) / 2) * 170
            pos.append((540 + side * (90 + 60 * row), y - 40 * row))
    for i, (x, y) in enumerate(pos):
        prev = (540, 1100) if stage == 0 else (540 + (x - 540) * 0.5, 1100 + (y - 1100) * 0.5)
        cx, cy = lerp(prev[0], x, k), lerp(prev[1], y, k)
        paste(img, cell_sprite(70 if n < 8 else 56, i % 3), cx, cy + 5 * math.sin(t * 8 + i))
    if t >= tp:
        paste(img, pill('UN PATRÓN', (200, 50, 170), 54), 540, 600, scale=pop(t, tp))
    if t >= tv:
        paste(img, label('DESDE EL INICIO', 100, fill=YEL, stroke=10), 540, 720, scale=pop(t, tv), rot=-3)
    return img, 1.0 + 0.05 * prog(t, 46.0, 2.3), (540, 1100)


def sc_huellas(t):   # Es como si tu cuerpo guardara las huellas de cómo fue armado…
    tg, th, ta = T('guardara', 49.50), T('huellas', 49.98), T('armado', 51.00)
    img = bg_holo().copy()
    # el cuerpo se arma por piezas (bloques que bajan y encajan)
    k = ease_out(prog(t, 48.3, 2.6))
    m = hb_mask()
    body = holo_body()
    for i in range(6):
        y0, y1 = i * HB_H // 6, (i + 1) * HB_H // 6
        ki = ease_back(clamp((k * 6 - i * 0.7) / 1.6), 1.4)
        if ki <= 0: continue
        piece = body.crop((0, y0, HB_W, y1))
        off = (1 - ki) * (-300 if i % 2 else 300)
        paste(img, piece, HBX + off, HBY - HB_H / 2 + (y0 + y1) / 2, alpha=min(1, ki * 1.5))
    if t >= th:
        paste(img, holo_lines(('back', 'limbs'), ease_in_out(prog(t, th, 0.8)), 1.0), HBX, HBY)
        paste(img, fingerprint_sprite(), 870, 760, scale=0.7 * pop(t, th))
        paste(img, pill('HUELLAS', (200, 50, 170), 54), 540, 600, scale=pop(t, th))
    if t >= ta:
        paste(img, label('¡ARMADO!', 110, fill=YEL, stroke=11), 300, 760, scale=pop(t, ta), rot=-5)
    return img, 1.0 + 0.04 * prog(t, 48.3, 3.0), (540, 1080)


@lru_cache(maxsize=1)
def skin_section():
    img = bg_tissue().copy()
    d = ImageDraw.Draw(img)
    # superficie de la piel (capa de arriba)
    top = [(x, 760 + 14 * math.sin(x / 45)) for x in range(0, W + 10, 10)]
    d.polygon(top + [(W, 980), (0, 980)], fill=SKIN + (255,))
    d.polygon([(x, y + 150) for x, y in top][::-1] + top, fill=SKIN + (255,))
    for x in range(0, W, 26):
        d.line([(x, 790), (x + 8, 900)], fill=SKIN_D + (120,), width=3)
    d.line(top, fill=SKIN_L + (255,), width=10)
    # células de la capa (filas)
    for row in range(2):
        for x in range(20 + row * 30, W, 60):
            d.ellipse([x - 26, 815 + row * 60, x + 26, 865 + row * 60], fill=(250, 205, 175, 255), outline=SKIN_D + (255,), width=3)
    return img


def sc_debajo(t):   # pero debajo de la superficie.
    td, ts = T('debajo', 51.72), T('superficie', 52.46)
    img = skin_section().copy()
    kl = ease_in_out(prog(t, td, 0.7))
    L = layer(); d = ImageDraw.Draw(L)
    paths = [[(x, 1150 + j * 120 + 50 * math.sin(x / 140 + j)) for x in range(-20, W + 30, 15)] for j in range(4)]
    for p in paths: d.line(_partial(p, kl), fill=MAG + (170,), width=30, joint='curve')
    g = blur(L, 12); d = ImageDraw.Draw(g)
    for p in paths: d.line(_partial(p, kl), fill=MAG_L + (255,), width=8, joint='curve')
    img.alpha_composite(g)
    # flecha hacia abajo
    if t >= td:
        a = pop(t, td)
        d = ImageDraw.Draw(img)
        x, y = 900, 1000 + 20 * math.sin(t * 8)
        d.line([(x, y - 90 * a), (x, y + 60 * a)], fill=YEL, width=26)
        d.polygon([(x - 50 * a, y + 40 * a), (x + 50 * a, y + 40 * a), (x, y + 110 * a)], fill=YEL)
    if t >= ts:
        paste(img, pill('SUPERFICIE', (40, 120, 240), 50), 330, 700, scale=pop(t, ts))
        paste(img, label('DEBAJO', 110, fill=YEL, stroke=11), 540, 1640, scale=pop(t, td + 0.1), rot=-3)
    elif t >= td:
        paste(img, label('DEBAJO', 110, fill=YEL, stroke=11), 540, 1640, scale=pop(t, td + 0.1), rot=-3)
    z = lerp(1.0, 1.12, ease_in_out(prog(t, td - 0.2, 1.2)))
    return img, z, (540, 1250)


def sc_mires(t):   # Así que la próxima vez que mires tu piel y parezca completamente normal,
    tm, tp, tn = T('mires', 54.31), T('piel', 54.90), T('normal', 56.74)
    img = bg_purple().copy()
    float_bubbles(img, t, n=6, seed=17, rmin=12, rmax=28, area=(0, 560, W, 1800), speed=30, alpha=0.3)
    spr = P2(shirt=(46, 170, 120), mouth='flat' if t < tn else 'smile', brows='normal', cheeks=0.5, look=(1, 1) if t >= tm else (0, 0))
    # brazo extendido mirando
    if t >= tm:
        paste(img, arm_layer(), 700 + 160 * (1 - ease_out(prog(t, tm, 0.3))), 1480, scale=0.6)
    paste(img, spr, 330, 1480, scale=1.3)
    if t >= tp:
        paste(img, pill('TU PIEL', (40, 120, 240), 50), 540, 620, scale=pop(t, tp))
    if t >= tn:
        paste(img, label('NORMAL', 120, fill=(255, 255, 255, 255), stroke=11), 520, 760, scale=pop(t, tn), rot=-3)
        paste(img, check_badge(50, True), 830, 760, scale=pop(t, tn + 0.1))
    return img, 1.0 + 0.06 * prog(t, 53.0, 4.0), (540, 1200)


def sc_recuerda(t):   # recuerda esto:
    tr, te = T('recuerda', 57.04), T('esto', 57.60)
    img = bg_purple().copy()
    float_bubbles(img, t, n=8, seed=21, rmin=14, rmax=36, area=(0, 560, W, 1800), speed=60, alpha=0.5)
    paste(img, alert_badge(90), 540, 1100, scale=pop(t, tr, 0.3) * (1 + 0.06 * math.sin(t * 14)))
    for i in range(6):
        a = i / 6 * 2 * math.pi + t * 1.5
        sparkle(img, 540 + 260 * math.cos(a), 1100 + 260 * math.sin(a), 30 * pop(t, tr + 0.05 * i))
    if t >= te:
        paste(img, label('RECUERDA', 140, fill=YEL, stroke=12), 540, 760, scale=pop(t, te), rot=-4)
    dx, dy = shake(t, te, 0.3, 10)
    return img, 1.0 + 0.1 * ease_out(prog(t, tr, 0.5)), (540 + dx, 1100 + dy)


def person_holo(img, t, k, x=540, y=1420, sc=1.3, mouth='flat', eyes='open'):
    """personaje normal; con un escáner (k) se ve por dentro el diseño oculto"""
    spr = P2(shirt=(236, 92, 70), mouth=mouth, cheeks=0.5, brows='raised', eyes=eyes)
    paste(img, spr, x, y, scale=sc)
    if k <= 0: return
    w, h = int(PW * sc), int(PH * sc)
    ox, oy = int(x - w / 2), int(y - h / 2)
    sy = int(lerp(oy, oy + h, k))
    al = spr.split()[3].resize((w, h))
    holo = Image.new('RGBA', (w, h), (40, 95, 200, 255))
    ld = ImageDraw.Draw(holo)
    for yy in range(0, h, 12): ld.line([(0, yy), (w, yy)], fill=(130, 190, 255, 255), width=2)
    # líneas de Blaschko (V en el torso)
    L = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i in range(7):
        yy = (500 + i * 70) * sc
        for side in (-1, 1):
            pts = _bez((w / 2, yy + 40 * sc), (w / 2 + side * 80 * sc, yy), (w / 2 + side * 190 * sc, yy - 70 * sc), n=20)
            d.line(pts, fill=MAG + (220,), width=int(16 * sc), joint='curve')
    rr = [(w / 2 + 140 * sc * math.cos(a) * (a / 12), 260 * sc + 140 * sc * math.sin(a) * (a / 12)) for a in [i / 4 for i in range(48)]]
    holo.alpha_composite(blur(L, 6))
    d = ImageDraw.Draw(holo)
    for i in range(7):
        yy = (500 + i * 70) * sc
        for side in (-1, 1):
            pts = _bez((w / 2, yy + 40 * sc), (w / 2 + side * 80 * sc, yy), (w / 2 + side * 190 * sc, yy - 70 * sc), n=20)
            d.line(pts, fill=MAG_L + (255,), width=5, joint='curve')
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rectangle([0, 0, w, sy - oy], fill=255)
    m = ImageChops.multiply(m, al)
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0)); out.paste(holo, (0, 0), m)
    img.alpha_composite(out, (ox, oy)) if ox >= 0 and oy >= 0 else paste(img, out, x, y)
    if k < 1:
        scan_line_h(img, sy, ox + 40, ox + w - 40)


def sc_fuera(t):   # Podrías estar viendo por fuera un cuerpo común…
    tf, tc = T('fuera', 59.14), T('comun', 60.26)
    img = bg_teal().copy()
    float_bubbles(img, t, n=6, seed=23, rmin=14, rmax=30, area=(0, 560, W, 1800), speed=40, alpha=0.35)
    person_holo(img, t, 0, mouth='flat')
    if t >= tf:
        paste(img, pill('POR FUERA', (40, 120, 240), 54), 540, 620, scale=pop(t, tf))
    if t >= tc:
        paste(img, label('COMÚN', 120, fill=(255, 255, 255, 255), stroke=11), 540, 760, scale=pop(t, tc), rot=-3)
    return img, 1.0 + 0.05 * prog(t, 57.8, 2.7), (540, 1150)


def sc_dentro(t):   # pero por dentro llevas un diseño oculto
    tde, tdi, to = T('dentro', 61.06), T('diseno', 61.92), T('oculto', 62.34)
    img = bg_teal().copy()
    float_bubbles(img, t, n=6, seed=23, rmin=14, rmax=30, area=(0, 560, W, 1800), speed=40, alpha=0.35)
    person_holo(img, t, ease_in_out(prog(t, tde - 0.1, 0.9)), mouth='o' if t >= to else 'flat', eyes='wide' if t >= to else 'open')
    if t >= tde:
        paste(img, pill('POR DENTRO', (200, 50, 170), 54), 540, 620, scale=pop(t, tde))
    if t >= tdi:
        paste(img, label('DISEÑO OCULTO', 104, fill=YEL, stroke=11), 540, 760, scale=pop(t, tdi), rot=-3)
    if t >= to:
        paste(img, alert_badge(50), 900, 900, scale=pop(t, to))
    if tdi <= t < tdi + 0.16:
        img = glitch(img, t)
    return img, 1.0 + 0.08 * ease_out(prog(t, tde, 0.6)), (540, 1150)


def sc_final(t):   # que te acompaña desde antes de nacer.  (vuelve al brazo del inicio: bucle)
    ta, tn = T('acompana', 63.22), T('nacer', 64.46)
    img = womb(t, sc=1.0, lines_a=1.0)
    if t >= ta:
        paste(img, pill('SIEMPRE CONTIGO', (220, 50, 110), 54), 540, 600, scale=pop(t, ta))
    if t >= tn:
        paste(img, label('ANTES DE NACER', 104, fill=YEL, stroke=11), 540, 720, scale=pop(t, tn), rot=-3)
    # últimos 0.35 s: funde al brazo del inicio (empalma con el hook)
    kf = prog(t, END - 0.35, 0.35)
    if kf > 0:
        h, _, _ = sc_hook(0.0)
        img = Image.blend(img, h, ease_in_out(kf))
    return img, lerp(1.0, 1.1, ease_in_out(prog(t, 62.8, 2.0))), (540, 1100)


END = 65.25

# ==================================================================== línea de tiempo
def _c(word, approx, pre=0.06):
    return T(word, approx) - pre


SCENES = [
    (0.0, sc_hook),
    (_c('pero', 1.43), sc_hook2),
    (_c('un', 3.23), sc_rayas),
    (_c('desde', 5.92), sc_antes),
    (_c('y', 7.16), sc_teoria),
    (_c('los', 8.62), sc_cientificos),
    (_c('son', 11.39), sc_1901),
    (_c('que', 12.78), sc_celulas),
    (_c('mientras', 15.43), sc_vientre),
    (_c('lo', 17.69), sc_extrano),
    (_c('estan', 21.03), sc_escondidas),
    (_c('entonces', 23.72), sc_como),
    (_c('porque', 25.53), sc_enfermedades),
    (_c('ciertas', 27.59), sc_manchas),
    (_c('aparecen', 30.56), sc_siguiendo),
    (_c('como', 33.36), sc_dibujado),
    (_c('y', 36.57), sc_rectas),
    (_c('en', 38.58), sc_espalda),
    (_c('en', 40.05), sc_pecho),
    (_c('y', 41.44), sc_espirales),
    (_c('o', 43.88), sc_azar),
    (_c('siguio', 46.10), sc_inicio),
    (_c('es', 48.36), sc_huellas),
    (_c('pero', 51.50), sc_debajo),
    (_c('asi', 53.00), sc_mires),
    (_c('recuerda', 57.04), sc_recuerda),
    (_c('podrias', 57.79), sc_fuera),
    (_c('pero', 60.47), sc_dentro),
    (_c('que', 62.84), sc_final),
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
        sfx(c - 0.12, 'whoosh', -12, dur=0.3)
    # hook
    sfx(T('piel', 0.28), 'sparkle', -12)
    sfx(T('uniforme', 1.03), 'pop', -8); sfx(T('uniforme', 1.03) + 0.12, 'ding', -12)
    sfx(T('realidad', 1.92) - 0.1, 'scan', -13, dur=0.9)
    sfx(T('mapa', 2.80) + 0.05, 'glitch', -8); sfx(T('mapa', 2.80) + 0.05, 'impact', -10)
    sfx(T('oculto', 2.87) + 0.15, 'pop', -8)
    # rayas invisibles
    sfx(T('rayas', 3.82), 'pop', -9)
    sfx(T('invisibles', 4.20), 'powerdown', -13)
    sfx(T('recorre', 5.00), 'scan', -14, dur=0.8)
    sfx(T('cuerpo', 5.54), 'bloop', -10)
    # antes de nacer
    t0 = T('desde', 5.92)
    for i in range(2): sfx(t0 + 0.05 + i * 0.62, 'thump', -9); sfx(t0 + 0.2 + i * 0.62, 'thump', -13)
    sfx(T('desde', 5.92) + 0.1, 'pop', -10)
    sfx(T('nacieras', 6.66), 'sparkle', -11)
    # teoría rara
    sfx(T('no', 7.32), 'boing', -11)
    sfx(T('teoria', 8.00), 'pop', -9)
    sfx(T('rara', 8.40), 'buzz', -9); sfx(T('rara', 8.40) + 0.02, 'impact', -11)
    # científicos
    sfx(T('cientificos', 9.00) - 0.05, 'pop', -9)
    sfx(T('lineas', 10.31), 'pop', -9)
    sfx(T('blaschko', 10.92), 'ding', -7); sfx(T('blaschko', 10.92), 'glitch', -11); sfx(T('blaschko', 10.92) + 0.08, 'sparkle', -12)
    # 1901 contador
    ts = T('son', 11.39)
    for i in range(9): sfx(ts + i * 0.1, 'tick', -13)
    sfx(ts + 0.9, 'ding', -10)
    sfx(T('naturales', 12.30), 'pop', -9); sfx(T('naturales', 12.30) + 0.1, 'ding', -13)
    # células
    sfx(T('siguen', 13.00) - 0.1, 'bloop', -9)
    for i in range(6): sfx(T('siguen', 13.00) + 0.1 + i * 0.4, 'bloop', -15)
    sfx(T('recorrido', 13.42), 'pop', -9)
    sfx(T('celulas', 14.66), 'pop', -8); sfx(T('celulas', 14.66) + 0.05, 'boing', -13)
    # vientre
    t0 = T('mientras', 15.43)
    for i in range(3): sfx(t0 + i * 0.62, 'thump', -9); sfx(t0 + 0.15 + i * 0.62, 'thump', -13)
    sfx(T('formando', 16.40), 'rise', -13, dur=0.7); sfx(T('formando', 16.40), 'pop', -10)
    sfx(T('vientre', 17.30), 'pop', -8)
    # extraño / simple vista
    sfx(T('extrano', 18.24), 'boing', -9)
    sfx(T('verlas', 19.84), 'pop', -9); sfx(T('verlas', 19.84) + 0.02, 'blink', -11)
    sfx(T('vista', 20.82), 'buzz', -9)
    # escondidas
    sfx(T('ahi', 21.52), 'ding', -10)
    sfx(T('permanecen', 22.08), 'powerdown', -11)
    sfx(T('escondidas', 22.56), 'click', -7); sfx(T('escondidas', 22.56) + 0.05, 'pop', -10)
    # ¿cómo sabemos?
    for i in range(3): sfx(T('como', 24.07) + i * 0.12, 'pop', -10)
    sfx(T('existen', 25.04), 'glitch', -8)
    # enfermedades
    sfx(T('porque', 25.53), 'scan', -13, dur=1.4)
    sfx(T('enfermedades', 26.52), 'pop', -8); sfx(T('enfermedades', 26.52) + 0.02, 'beep', -12)
    # manchas
    sfx(T('manchas', 28.12), 'pop', -8)
    sfx(T('erupciones', 28.67), 'pop', -8)
    sfx(T('cambios', 29.74), 'pop', -8)
    t0, t1 = T('manchas', 28.12), T('color', 30.22) + 0.3
    for i in range(10): sfx(t0 + (t1 - t0) * i / 10, 'bloop', -17)
    # siguiendo las líneas
    sfx(T('siguiendo', 31.04), 'sweep', -14, dur=1.6)
    sfx(T('exactamente', 31.88), 'pop', -9)
    sfx(T('lineas', 32.86), 'ding', -8); sfx(T('lineas', 32.86) + 0.05, 'pop', -10)
    # dibujado
    sfx(T('alguien', 33.88), 'scan', -16, dur=2.4)
    sfx(T('mapa', 35.12), 'pop', -8)
    sfx(T('secreto', 35.46), 'sparkle', -11)
    sfx(T('cuerpo', 36.36), 'pop', -10)
    # rectas + sígueme
    sfx(T('ese', 36.76), 'click', -9)
    sfx(T('mapa', 37.04) - 0.1, 'sweep', -15, dur=0.45)
    sfx(T('lineas', 37.72), 'pop', -9)
    sfx(T('rectas', 38.30), 'buzz', -8); sfx(T('rectas', 38.30) + 0.02, 'impact', -11)
    sfx(T('rectas', 38.30) + 0.15, 'swirl', -15, dur=0.6)
    # V / S / espirales
    sfx(T('espalda', 38.96), 'pop', -9); sfx(T('espalda', 38.96) - 0.1, 'scan', -15, dur=0.8)
    sfx(T('v', 39.82), 'impact', -8); sfx(T('v', 39.82), 'pop', -8)
    sfx(T('pecho', 40.36), 'pop', -9); sfx(T('pecho', 40.36) - 0.1, 'scan', -15, dur=0.7)
    sfx(T('s', 41.24), 'impact', -8); sfx(T('s', 41.24), 'pop', -8)
    sfx(T('brazos', 41.72), 'pop', -10); sfx(T('piernas', 42.20), 'pop', -10)
    sfx(T('curvas', 42.78), 'boing', -11)
    sfx(T('espirales', 43.22), 'swirl', -11, dur=0.6); sfx(T('espirales', 43.22), 'pop', -9)
    # azar
    for i in range(5): sfx(43.95 + i * 0.22, 'click', -13 - i)
    sfx(T('construyo', 45.30), 'pop', -9)
    sfx(T('azar', 45.80), 'buzz', -8); sfx(T('azar', 45.80) + 0.02, 'impact', -10)
    # inicio de la vida: divisiones
    sfx(T('siguio', 46.10), 'bloop', -9)
    sfx(T('patron', 46.76), 'bloop', -8); sfx(T('patron', 46.76), 'pop', -11)
    sfx(T('inicio', 47.38), 'bloop', -8)
    sfx(T('vida', 48.14), 'bloop', -8); sfx(T('vida', 48.14) + 0.05, 'ding', -11)
    # armado
    for i in range(6): sfx(48.36 + 0.16 + i * 0.36, 'thump', -12)
    sfx(T('huellas', 49.98), 'sparkle', -10); sfx(T('huellas', 49.98), 'pop', -10)
    sfx(T('armado', 51.00), 'impact', -9); sfx(T('armado', 51.00), 'pop', -9)
    # debajo
    sfx(T('debajo', 51.72), 'whoosh_down', -10, dur=0.7)
    sfx(T('superficie', 52.46), 'pop', -9)
    # la próxima vez
    sfx(T('mires', 54.31), 'pop', -9); sfx(T('mires', 54.31) + 0.05, 'scan', -16, dur=0.8)
    sfx(T('piel', 54.90), 'pop', -10)
    sfx(T('normal', 56.74), 'ding', -9); sfx(T('normal', 56.74) + 0.1, 'pop', -11)
    # recuerda
    sfx(T('recuerda', 57.04), 'pop', -7); sfx(T('recuerda', 57.04), 'beep', -12)
    sfx(T('esto', 57.60), 'impact', -10)
    # por fuera / por dentro
    sfx(T('fuera', 59.14), 'pop', -9)
    sfx(T('comun', 60.26), 'pop', -9)
    sfx(T('dentro', 61.06) - 0.1, 'scan', -12, dur=0.9)
    sfx(T('diseno', 61.92), 'glitch', -8); sfx(T('diseno', 61.92) + 0.02, 'pop', -9)
    sfx(T('oculto', 62.34), 'pop', -8); sfx(T('oculto', 62.34) + 0.02, 'beep', -12)
    # final
    t0 = T('que', 62.84)
    for i in range(3): sfx(t0 + 0.05 + i * 0.62, 'thump', -9); sfx(t0 + 0.2 + i * 0.62, 'thump', -13)
    sfx(T('acompana', 63.22), 'pop', -9)
    sfx(T('nacer', 64.46), 'sparkle', -10); sfx(T('nacer', 64.46), 'pop', -9)
    return SFX
