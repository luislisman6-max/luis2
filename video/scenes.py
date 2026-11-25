"""Escenas del video. Todos los tiempos son absolutos (segundos del audio de voz)."""
import math, random
from functools import lru_cache
from PIL import Image, ImageDraw
from lib import *
from art import *

# ---------------------------------------------------------------- helpers
_pcache = {}


def P(**kw):
    """person() con caché"""
    key = tuple(sorted(kw.items()))
    if key not in _pcache:
        if len(_pcache) > 60: _pcache.clear()
        _pcache[key] = person(**kw)
    return _pcache[key]


def hb(sx, sy, cx=540, cy=1060, sc=1.05):
    return cx + (sx - HB_W / 2) * sc, cy + (sy - HB_H / 2) * sc


def dashes(img, x, y, r, side=-1, alpha=1.0):
    d = ImageDraw.Draw(img)
    for dy, ln in ((-0.55, 0.32), (-0.18, 0.5), (0.25, 0.36), (0.6, 0.26)):
        x1 = x + side * (r + 30)
        d.line([(x1, y + dy * r), (x1 + side * ln * r, y + dy * r)], fill=(255, 228, 238, int(200 * alpha)), width=6)


@lru_cache(maxsize=4)
def puff_sprite(col=(255, 255, 255)):
    def fn(im, s):
        L = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for (x, y, r) in ((150, 150, 80), (90, 170, 60), (210, 170, 62), (120, 110, 55), (190, 105, 58), (150, 200, 55)):
            d.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s], fill=col + (200,))
        im.alpha_composite(blur(L, 10 * s))
    return ss_sprite(300, 300, fn)


@lru_cache(maxsize=2)
def brain_sprite():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        for (x, y, r) in ((70, 80, 50), (120, 60, 55), (170, 80, 50), (95, 120, 50), (150, 120, 50)):
            d.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s], fill=(255, 160, 190, 255), outline=(200, 80, 120, 255), width=4 * s)
        for (x, y, r) in ((70, 80, 50), (120, 60, 55), (170, 80, 50), (95, 120, 50), (150, 120, 50)):
            d.ellipse([(x - r + 4) * s, (y - r + 4) * s, (x + r - 4) * s, (y + r - 4) * s], fill=(255, 175, 200, 255))
        for a, b in (((60, 70), (100, 95)), ((130, 50), (150, 90)), ((160, 120), (185, 95)), ((90, 130), (120, 150))):
            d.line([(a[0] * s, a[1] * s), (b[0] * s, b[1] * s)], fill=(210, 90, 130, 255), width=5 * s)
        d.line([(120 * s, 30 * s), (120 * s, 160 * s)], fill=(210, 90, 130, 255), width=4 * s)
    return glow_sprite(ss_sprite(240, 190, fn), 10, (255, 120, 170, 160))


@lru_cache(maxsize=2)
def follow_button():
    txt = "Sígueme para más curiosidades"
    f = font(38, 'x')
    tw = ImageDraw.Draw(Image.new('RGBA', (1, 1))).textlength(txt, font=f)
    w, h = int(tw + 140), 92
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, w * s - 1, h * s - 1], h * s // 2, fill=(236, 40, 70, 255))
        d.ellipse([18 * s, 16 * s, 78 * s, 76 * s], fill=(255, 255, 255, 255))
        d.line([(48 * s, 30 * s), (48 * s, 62 * s)], fill=(236, 40, 70, 255), width=8 * s)
        d.line([(32 * s, 46 * s), (64 * s, 46 * s)], fill=(236, 40, 70, 255), width=8 * s)
        d.text((96 * s, h * s / 2), txt, font=font(38 * s, 'x'), fill='white', anchor='lm')
    return glow_sprite(ss_sprite(w, h, fn), 14, (255, 60, 90, 200))


@lru_cache(maxsize=2)
def plane_sprite():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        pts = [(10, 110), (230, 20), (150, 200), (115, 135)]
        d.polygon([(x * s, y * s) for x, y in pts], fill=(255, 255, 255, 255), outline=(60, 130, 240, 255))
        d.line([(115 * s, 135 * s), (230 * s, 20 * s)], fill=(60, 130, 240, 255), width=5 * s)
        d.polygon([(115 * s, 135 * s), (110 * s, 190 * s), (140 * s, 160 * s)], fill=(200, 220, 255, 255))
    return glow_sprite(ss_sprite(240, 210, fn), 10, (90, 160, 255, 200))


@lru_cache(maxsize=2)
def device_sprite():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, 380 * s, 560 * s], 50 * s, fill=(238, 242, 246, 255), outline=(190, 200, 210, 255), width=6 * s)
        d.rounded_rectangle([40 * s, 50 * s, 340 * s, 380 * s], 24 * s, fill=(25, 35, 50, 255))
        d.ellipse([160 * s, 430 * s, 220 * s, 490 * s], fill=(200, 210, 220, 255))
    return ss_sprite(380, 560, fn)


@lru_cache(maxsize=2)
def grid_dot(green=False):
    def fn(im, s):
        d = ImageDraw.Draw(im)
        if green:
            L = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(L).ellipse([6 * s, 6 * s, 58 * s, 58 * s], fill=(90, 255, 120, 200))
            im.alpha_composite(blur(L, 8 * s)); d = ImageDraw.Draw(im)
            d.ellipse([16 * s, 16 * s, 48 * s, 48 * s], fill=(110, 240, 110, 255), outline=(220, 255, 220, 255), width=3 * s)
        else:
            d.ellipse([16 * s, 16 * s, 48 * s, 48 * s], fill=(160, 150, 220, 60), outline=(210, 200, 255, 220), width=3 * s)
            d.ellipse([22 * s, 21 * s, 30 * s, 29 * s], fill=(255, 255, 255, 160))
    return ss_sprite(64, 64, fn)


def label(txt, size=64, fill=(255, 255, 255, 255), stroke=7, kind='k'):
    return _label(txt, size, fill, stroke, kind)


@lru_cache(maxsize=64)
def _label(txt, size, fill, stroke, kind):
    return text_sprite(txt, size, fill=fill, kind=kind, stroke=stroke, stroke_fill=(35, 12, 30, 255))


@lru_cache(maxsize=16)
def pill(txt, bg=(40, 120, 240), size=44):
    f = font(size, 'x')
    tw = ImageDraw.Draw(Image.new('RGBA', (1, 1))).textlength(txt, font=f)
    w, h = int(tw + 70), int(size * 1.9)
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, w * s - 1, h * s - 1], h * s // 2, fill=bg + (255,), outline=(255, 255, 255, 230), width=3 * s)
        d.text((w * s / 2, h * s / 2), txt, font=font(size * s, 'x'), fill='white', anchor='mm')
    return glow_sprite(ss_sprite(w, h, fn), 12, bg + (180,))


@lru_cache(maxsize=4)
def lens_sprite(r=150):
    def fn(im, s):
        c = (r + 30) * s; rr = r * s
        L = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(L).ellipse([c - rr - 10 * s, c - rr - 10 * s, c + rr + 10 * s, c + rr + 10 * s], fill=(90, 200, 255, 160))
        im.alpha_composite(blur(L, 16 * s))
        d = ImageDraw.Draw(im)
        d.ellipse([c - rr, c - rr, c + rr, c + rr], fill=(20, 50, 110, 235))
        L = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(L)
        for y in range(int(c - rr), int(c + rr), 8 * s):
            ld.line([(c - rr, y), (c + rr, y)], fill=(120, 190, 255, 35), width=2 * s)
        # trozo de intestino dentro de la lupa
        ld.arc([c - rr * 0.9, c - rr * 0.5, c + rr * 0.9, c + rr * 1.3], 190, 350, fill=(255, 120, 160, 150), width=int(rr * 0.12))
        m = Image.new('L', im.size, 0); ImageDraw.Draw(m).ellipse([c - rr, c - rr, c + rr, c + rr], fill=255)
        t = Image.new('RGBA', im.size, (0, 0, 0, 0)); t.paste(L, (0, 0), m); im.alpha_composite(t)
        d = ImageDraw.Draw(im)
        d.ellipse([c - rr, c - rr, c + rr, c + rr], outline=(170, 235, 255, 255), width=5 * s)
    return ss_sprite(2 * (r + 30), 2 * (r + 30), fn)


def sparkle(img, x, y, size, alpha=1.0):
    d = ImageDraw.Draw(img)
    a = int(255 * alpha)
    d.polygon([(x, y - size), (x + size * .22, y - size * .22), (x + size, y), (x + size * .22, y + size * .22), (x, y + size),
               (x - size * .22, y + size * .22), (x - size, y), (x - size * .22, y - size * .22)], fill=(255, 245, 200, a))


def float_bubbles(img, t, n=10, seed=1, rmin=18, rmax=46, area=(0, 500, W, 1600), speed=60, alpha=0.9):
    rnd = random.Random(seed)
    x0, y0, x1, y1 = area
    for i in range(n):
        r = rnd.randint(rmin, rmax); x = rnd.uniform(x0, x1); ph = rnd.random()
        span = y1 - y0
        y = y1 - ((ph * span + t * speed * (0.6 + rnd.random())) % span)
        x += wave(t * 60 + i * 37, 14, 180, i)
        paste(img, bubble(r), x, y, alpha=alpha)


# ======================================================================
#  ESCENAS  (cada una: draw(t) -> (RGBA frame, zoom, (cx, cy)))
# ======================================================================
def meeting_frame(t, tense=1.0, look_side=0.0, lens=1.0, bubble_y_off=0.0, lens_alpha=1.0, alert_t=None, sweat=True, shake=0.0):
    img = bg_meeting().copy()
    paste(img, P(hair_style='curly', hair=(45, 28, 20), skin=(176, 120, 84), shirt=(232, 172, 64), look=(look_side, 0),
                 mouth='side' if look_side else 'flat', brows='raised' if look_side else 'normal'), 205, 1330, scale=0.6, anchor='b')
    paste(img, P(hair_style='long', hair=(32, 22, 22), skin=(122, 82, 58), shirt=(222, 92, 142), look=(-look_side, 0),
                 mouth='side' if look_side else 'flat', brows='raised' if look_side else 'normal'), 875, 1330, scale=0.6, anchor='b')
    jx = math.sin(t * 90) * 4 * shake
    paste(img, P(mouth='tense' if tense > 0.5 else 'flat', cheeks=round(tense, 1), sweat=sweat and tense > 0.5, brows='worried' if tense > 0.5 else 'normal',
                 shirt=(236, 128, 52), arms='down'), 540 + jx, 1390, scale=0.8, anchor='b')
    img.alpha_composite(table_layer())
    if lens > 0.01:
        paste(img, lens_sprite(), 540 + jx, 1125, scale=lens * 0.85, alpha=lens_alpha)
        wob = 1 + 0.04 * math.sin(t * 7)
        paste(img, bubble(62), 540 + jx, 1130 + bubble_y_off, scale=lens * wob, alpha=lens_alpha)
    if alert_t is not None:
        paste(img, alert_badge(), 680, 995, scale=pop(t, alert_t))
    return img


def scene_A(t):  # 0.00 - 4.20  HOOK
    lens = pop(t, 0.40, 0.30)
    img = meeting_frame(t, tense=clamp(0.4 + t), look_side=ease_out(prog(t, 1.60, 0.25)), lens=lens,
                        alert_t=0.92, shake=1.0 if 0.92 < t < 3.1 else 0.0)
    # 3.12 «respirando»: la burbuja sube de la panza a la boca y sale como aliento
    k = prog(t, 3.12, 0.45)
    if k > 0:
        y = lerp(1130, 860, ease_in_out(k))
        if k < 1:
            paste(img, bubble(40), 540, y, scale=1.0)
        pk = prog(t, 3.55, 0.6)
        if pk > 0:
            paste(img, puff_sprite(), 600 + 120 * pk, 850 - 40 * pk, scale=0.4 + 0.9 * pk, alpha=1 - pk)
    z = lerp(1.0, 1.13, ease_in_out(prog(t, 0.0, 3.1)))
    return img, z, (540, 1010)


def scene_B(t):  # 4.20 - 7.00  intro intestino
    img = bg_intestine(False, True).copy()
    float_bubbles(img, t, n=6, seed=3, rmin=14, rmax=30, area=(0, 650, W, 1180), speed=40, alpha=0.7)
    k = ease_out(prog(t, 4.22, 0.7))
    x = lerp(-260, 520, k) + 18 * math.sin(t * 1.6)
    y = 900 + 14 * math.sin(t * 2.1)
    if k < 0.97: dashes(img, x, y, 230, -1, 1 - k)
    paste(img, bubble(230), x, y, scale=1 + 0.015 * math.sin(t * 5))
    paste(img, bubble(70), 880, 760 + 10 * math.sin(t * 3), scale=pop(t, 6.24))
    return img, lerp(1.0, 1.06, prog(t, 4.2, 2.8)), (540, 900)


def holo_base(t, bubble_r=70, show_bubble=True, bx=None, by=None, lung=0.0, breathe=0.0):
    img = bg_holo('blue').copy()
    paste(img, holo_body(), 540, 1060, scale=1.05)
    if lung > 0.01:
        lx, ly = hb(280, 420)
        paste(img, lungs_sprite(), lx, ly, scale=lung * (1.15 + 0.08 * breathe), alpha=0.95)
    if show_bubble:
        x, y = hb(*HB_BELLY) if bx is None else (bx, by)
        paste(img, bubble(bubble_r), x, y, scale=1 + 0.03 * math.sin(t * 6))
    return img


def draw_path(img, pts, k, col, width=10, dashed=False):
    if k <= 0: return
    n = max(2, int(len(pts) * k))
    d = ImageDraw.Draw(img)
    seg = pts[:n]
    L = layer(); ld = ImageDraw.Draw(L)
    ld.line(seg, fill=col[:3] + (150,), width=width * 3, joint='curve')
    img.alpha_composite(blur(L, 10))
    if dashed:
        for i in range(0, len(seg) - 1, 2):
            d.line([seg[i], seg[i + 1]], fill=col, width=width)
    else:
        d.line(seg, fill=col, width=width, joint='curve')


def path_up():   # panza -> boca
    (x0, y0), (x1, y1) = hb(*HB_BELLY), hb(*HB_MOUTH)
    return [(x0 + wave(i, 20, 30, 0.3) * (1 - i / 40), lerp(y0, y1, i / 40)) for i in range(41)]


def path_down():
    (x0, y0) = hb(*HB_BELLY)
    return [(x0, y0 + i * 6) for i in range(30)]


def scene_C(t):  # 7.00 - 12.85
    up = path_up()
    k_up = ease_in_out(prog(t, 11.36, 0.62))
    on_belly = k_up <= 0
    bx, by = up[min(40, int(k_up * 40))] if not on_belly else hb(*HB_BELLY)
    r = int(lerp(70, 44, k_up))
    pulse = 1 + 0.25 * math.sin(math.pi * prog(t, 8.04, 0.35))
    img = holo_base(t, show_bubble=False)
    # salida de abajo: X roja («salida» 9.90)
    kd = prog(t, 9.90, 0.3)
    if kd > 0:
        draw_path(img, path_down(), kd, (255, 70, 90, 255), dashed=True)
        ex, ey = hb(280, 800)
        paste(img, check_badge(40, False), ex, ey, scale=pop(t, 10.05))
    # camino hacia arriba (11.0 - 11.4)
    draw_path(img, up, prog(t, 11.0, 0.4), (120, 255, 170, 255))
    if t < 11.98:
        paste(img, bubble(r), bx, by, scale=pulse * (1 + 0.03 * math.sin(t * 6)))
    pk = prog(t, 11.98, 0.7)
    if pk > 0:
        mx, my = hb(*HB_MOUTH)
        paste(img, puff_sprite(), mx + 60 * pk, my - 20 * pk, scale=0.3 + 0.8 * pk, alpha=1 - pk * 0.9)
        paste(img, check_badge(40, True), mx + 150, my - 60, scale=pop(t, 12.0))
    if 7.06 <= t < 7.30:  # glitch «Spoiler»
        img = glitch(img, t)
    z = lerp(1.0, 1.12, ease_in_out(prog(t, 11.2, 1.0)))
    return img, z, (540, 760)


def glitch(img, t):
    rnd = random.Random(int(t * 60))
    out = img.copy()
    for _ in range(7):
        y = rnd.randint(300, H - 300); h = rnd.randint(20, 90); dx = rnd.randint(-60, 60)
        strip = img.crop((0, y, W, y + h))
        out.paste(strip, (dx, y))
    tint = Image.new('RGBA', img.size, (120, 220, 255, 40))
    out.alpha_composite(tint)
    return out


FOODS = [('lettuce', 170, 1190), ('bread', 420, 1200), ('carrot', 680, 1190), ('bread', 930, 1205)]
BACT = [('green', 230, 900, 15.08), ('purple', 560, 820, 15.40), ('blue', 860, 930, 15.96), ('orange', 420, 1030, 16.10)]


def scene_D(t):  # 12.85 - 20.85 bacterias
    img = bg_intestine(False, True).copy()
    eat = prog(t, 16.78, 1.3)
    for i, (k, x, y) in enumerate(FOODS):
        paste(img, food_item(k), x, y, scale=0.9 * (1 - 0.35 * eat * (i % 2 == 0 or True)))
    # billones: puntitos-bacteria
    kb = prog(t, 15.40, 0.4)
    if kb > 0:
        rnd = random.Random(8)
        d = ImageDraw.Draw(img)
        for i in range(70):
            x, y = rnd.uniform(20, W - 20), rnd.uniform(660, 1150)
            if rnd.random() > kb: continue
            r = rnd.uniform(5, 10)
            x += wave(t * 40 + i * 13, 6, 90, i)
            d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=rnd.choice([(140, 220, 110, 200), (170, 130, 240, 200), (110, 200, 245, 200)]))
    chomp = 1 if (16.78 <= t < 18.15 and int(t * 8) % 2 == 0) else 0
    for i, (k, x, y, t0) in enumerate(BACT):
        s = pop(t, t0)
        if s <= 0: continue
        yy = y + 14 * math.sin(t * 3 + i) + 60 * ease_out(eat) * (1 if t < 18.4 else max(0, 1 - (t - 18.4) * 2))
        eating = 16.78 <= t < 18.15
        paste(img, bacterium(k, (chomp if i % 2 == 0 else 1 - chomp) if eating else 0), x, yy, scale=s * 0.95, rot=4 * math.sin(t * 2 + i))
        # 19.44 «burbujas de gas»
        tb = 19.44 + i * 0.15
        kb2 = prog(t, tb, 1.3)
        if kb2 > 0:
            paste(img, bubble(48), x + 20 + 30 * math.sin(t * 2 + i), yy - 60 - 260 * ease_out(kb2), scale=pop(t, tb, 0.22) * (1 + 0.12 * math.sin(math.pi * prog(t, 20.04, 0.3))))
    z = 1.0 + 0.25 * (1 - ease_out(prog(t, 12.90, 0.5)))
    return img, z, (540, 950)


def scene_E(t):  # 20.85 - 26.95 contador
    img = bg_purple().copy()
    float_bubbles(img, t, n=12, seed=5, rmin=20, rmax=55, area=(30, 300, W - 30, 1700), speed=55, alpha=0.85)
    tl = pill("LO NORMAL", (130, 80, 230), 46)
    paste(img, tl, 540, 640, scale=pop(t, 21.92))
    if t >= 23.04:
        if t < 23.42: n = 14
        elif t < 23.70: n = 15 + int((t - 23.42) / (0.28 / 8))
        else: n = 23
        n = min(n, 23)
        s = pop(t, 23.04, 0.25) if t < 23.42 else (1 + 0.18 * (1 - prog(t, 23.70, 0.25)) if t >= 23.70 else 1.0)
        num = label(str(n), 330, fill=(255, 205, 60, 255), stroke=12)
        paste(img, num, 540, 930, scale=s)
        if t >= 23.70:
            paste(img, label("PEDOS AL DÍA", 84, stroke=8), 540, 1150, scale=pop(t, 24.06))
    if t >= 24.88:
        paste(img, label("PRRT", 80, fill=(255, 225, 80, 255), stroke=8), 860, 760, scale=pop(t, 24.88), rot=-12)
    if t >= 25.28:
        paste(img, pill("SÍ, TÚ TAMBIÉN", (236, 50, 90), 54), 540, 1380, scale=pop(t, 25.28), rot=2 * math.sin(t * 8) if t < 26.5 else 0)
    return img, 1.0, (540, 960)


GATE_X = SPH_X - 30


def intestine_gate(t, squeeze=0.0):
    img = bg_intestine(True, True).copy()
    if squeeze > 0.01:
        img.alpha_composite(sphincter_sprite(max(1, int(round(squeeze * 4)))))
    paste(img, gate_bulge(), GATE_X + 90 - 30 * squeeze, 900, scale=1 + 0.22 * squeeze)
    return img


def panel(img, t, t_in, title, rows):
    s = pop(t, t_in, 0.3)
    if s <= 0: return
    L = layer(800, 210)
    d = ImageDraw.Draw(L)
    d.rounded_rectangle([4, 4, 796, 206], 34, fill=(20, 40, 70, 200), outline=(170, 245, 255, 255), width=4)
    for yy in range(16, 200, 9):
        d.line([(26, yy), (774, yy)], fill=(120, 220, 255, 25), width=1)
    d.text((400, 48), title, font=font(32, 'b'), fill=(150, 235, 255, 255), anchor='mm')
    for (x, txt, ok, t0) in rows:
        if t < t0: continue
        b = check_badge(34, ok)
        ps = pop(t, t0)
        paste(L, b, x + 40, 135, scale=ps)
        d.text((x + 90, 135), txt, font=font(54, 'x'), fill=(255, 255, 255, 255) if ok else (205, 175, 190, 255), anchor='lm')
    g = glow_sprite(L, 12, (90, 230, 255, 160), 0.8)
    paste(img, g, 540, 1720, scale=s)


def scene_F(t):  # 26.95 - 38.85 sensor
    img = intestine_gate(t)
    k = ease_out(prog(t, 27.9, 1.4))
    bx = lerp(-260, 545, k); by = 900 + 8 * math.sin(t * 2.4)
    sq = 1 - 0.08 * math.sin(math.pi * prog(t, 29.30, 0.25))
    if k < 0.98: dashes(img, bx, by, 235, -1, 1 - k)
    # haz del escáner (32.10 «toma»)
    kb = prog(t, 32.10, 0.25)
    if kb > 0 and t < 37.0:
        src = (GATE_X - 10, 900)
        L = layer(); d = ImageDraw.Draw(L)
        d.polygon([src, (bx - 130, by - 225), (bx - 130, by + 225)], fill=(80, 230, 255, int(45 * kb)))
        for j in range(-7, 8):
            d.line([src, (bx - 130, by + j * 30)], fill=(150, 240, 255, int(60 * kb)), width=2)
        img.alpha_composite(blur(L, 5))
    paste(img, bubble(235), bx, by, scale=sq)
    if kb > 0 and t < 37.0:
        sy = by + 200 * math.sin((t - 32.1) * 3.2)
        half = math.sqrt(max(0, 235 ** 2 - (sy - by) ** 2))
        L = layer(); d = ImageDraw.Draw(L)
        d.line([(bx - half, sy), (bx + half, sy)], fill=(90, 235, 255, int(255 * kb)), width=16)
        img.alpha_composite(blur(L, 8))
        ImageDraw.Draw(img).line([(bx - half, sy), (bx + half, sy)], fill=(190, 250, 255, int(255 * kb)), width=4)
        e = layer(); ImageDraw.Draw(e).ellipse([GATE_X - 40, 860, GATE_X + 20, 940], fill=(90, 235, 255, 255))
        img.alpha_composite(blur(e, 14))
        ImageDraw.Draw(img).ellipse([GATE_X - 24, 884, GATE_X + 4, 916], fill=(235, 255, 255, 255))
    # chispas «increíble» 30.48
    ks = prog(t, 30.48, 0.7)
    if 0 < ks < 1:
        for j, (dx, dy) in enumerate(((-60, -200), (40, -260), (-20, 230), (60, 180), (-120, 40))):
            sparkle(img, GATE_X + dx, 900 + dy, 26 * math.sin(math.pi * clamp(ks * 1.4 - j * 0.08)), 1)
    # alerta «avisa» 33.78
    if t >= 33.78:
        paste(img, alert_badge(), bx + 175, by - 215, scale=pop(t, 33.78))
    # cerebro 34.32
    if t >= 34.32:
        paste(img, brain_sprite(), 880, 470, scale=pop(t, 34.32) * 0.8)
        kk = prog(t, 34.32, 0.5)
        d = ImageDraw.Draw(img)
        for j in range(8):
            u = j / 8
            if u > kk: break
            x, y = lerp(GATE_X + 40, 880, u), lerp(800, 560, u) + 12 * math.sin(u * 20 + t * 10)
            d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=(150, 240, 255, 255))
    title = "SENSOR DE SEGURIDAD" if t >= 37.46 else "ANALIZANDO MUESTRA..."
    panel(img, t, 32.60, title, [(60, "GAS", True, 35.10), (420, "¿SÓLIDO?", False, 36.10)])
    return img, 1.0 + 0.04 * prog(t, 27, 12), (600, 900)


def wall_bulges(img, x, k):
    if k <= 0: return
    L = layer(); d = ImageDraw.Draw(L)
    top_y = TOP_B - 150 + 150 * k
    bot_y = BOT_A + 150 - 150 * k
    d.ellipse([x - 280, top_y - 160, x + 280, top_y + 150], fill=rgba('#c9446f'))
    d.ellipse([x - 280, bot_y - 150, x + 280, bot_y + 160], fill=rgba('#c13f69'))
    for xx in range(int(x - 280), int(x + 280), 34):
        d.line([(xx, top_y - 160), (xx, top_y + 150)], fill=(143, 36, 73, 70), width=10)
        d.line([(xx, bot_y - 150), (xx, bot_y + 160)], fill=(143, 36, 73, 70), width=10)
    m = Image.new('L', img.size, 0); md = ImageDraw.Draw(m)
    md.ellipse([x - 280, top_y - 160, x + 280, top_y + 150], fill=255)
    md.ellipse([x - 280, bot_y - 150, x + 280, bot_y + 160], fill=255)
    L2 = layer(); L2.paste(L, (0, 0), m)
    img.alpha_composite(L2)
    d = ImageDraw.Draw(img)
    d.arc([x - 280, top_y - 160, x + 280, top_y + 150], 20, 160, fill=(255, 194, 210, 235), width=6)
    d.arc([x - 280, bot_y - 150, x + 280, bot_y + 160], 200, 340, fill=(255, 194, 210, 235), width=6)


def scene_G(t):  # 38.85 - 45.40 aprietas / regresa / atrapado
    sq = ease_out(prog(t, 39.42, 0.25)) * (1 - 0.3 * prog(t, 43.0, 0.6))
    img = intestine_gate(t, sq)
    bump = 0
    for tb in (40.90, 41.50):
        bump += 28 * math.sin(math.pi * prog(t, tb, 0.22))
    kb = ease_in_out(prog(t, 42.98, 0.6))
    bx = lerp(545, 330, kb) + bump
    by = 900 + 8 * math.sin(t * 2.4)
    katr = ease_out(prog(t, 44.15, 0.25))
    sx = 1 + 0.06 * katr; sy = 1 - 0.12 * katr
    b = bubble(235)
    if katr > 0:
        b = b.resize((int(b.width * sx), int(b.height * sy)), Image.BILINEAR)
    if 0 < kb < 1: dashes(img, bx, by, 235, 1, 1 - kb)
    paste(img, b, bx, by)
    wall_bulges(img, 330, katr)
    if t >= 39.42 and t < 42.9:
        paste(img, alert_badge(), bx + 175, by - 215, scale=pop(t, 39.42))
    if t >= 44.35:
        paste(img, label("GLU", 120, fill=(255, 214, 70, 255), stroke=10), 330, 610, scale=pop(t, 44.35), rot=-8)
    shake = 6 * math.sin(t * 70) * (1 - prog(t, 39.42, 0.4)) if t >= 39.42 else 0
    return img, 1.0, (540 + shake, 960)


def scene_H(t):  # 45.40 - 52.90 globo / retortijones / CTA
    img = bg_purple().copy()
    bel = ease_back(prog(t, 46.12, 0.98), 1.2)
    cramp = 48.08 <= t < 50.7
    wob = (1 + 0.035 * math.sin(t * 38)) if cramp else 1.0
    if t < 46.12:
        face = dict(eyes='open', mouth='flat', brows='normal')
    elif not cramp and t < 48.08:
        face = dict(eyes='big', mouth='o', brows='raised', cheeks=0.5)
    elif cramp:
        face = dict(eyes='squeeze', mouth='wobble', brows='worried', cheeks=0.9, sweat=True)
    else:
        face = dict(eyes='open', mouth='smile', brows='normal', cheeks=0.3)
    belly = round(bel * 20) / 20
    spr = P(belly=belly, arms='belly', shirt=(64, 130, 230), **face)
    if wob != 1.0:
        spr = spr.resize((int(spr.width * wob), int(spr.height * (2 - wob))), Image.BILINEAR)
    paste(img, spr, 540, 2010, scale=1.45, anchor='b')
    if cramp:
        d = ImageDraw.Draw(img)
        cy = 2010 - 1.45 * (980 - 790 + 30 * bel)
        for j in range(3):
            r = 40 + j * 28
            a0 = (t * 400 + j * 120) % 360
            d.arc([540 - r, cy - r, 540 + r, cy + r], a0, a0 + 200, fill=(255, 255, 255, 170), width=6)
    if t >= 49.52 and t < 50.7:
        paste(img, label("GRRR", 96, fill=(255, 120, 140, 255), stroke=9), 820, 1180, scale=pop(t, 49.52), rot=10 + 4 * math.sin(t * 30))
    if t >= 50.72:
        paste(img, follow_button(), 540, 1290, scale=pop(t, 50.72) * (1 + 0.04 * math.sin(t * 9)))
    if t >= 52.44:
        for j, (x, y) in enumerate(((330, 560), (750, 600), (600, 470))):
            paste(img, label("?", 110, fill=(255, 230, 90, 255), stroke=8), x, y, scale=pop(t, 52.44 + j * 0.06), rot=15 * math.sin(t * 5 + j))
    z = lerp(1.0, 1.08, prog(t, 45.4, 5)) if t < 50.7 else lerp(1.08, 1.0, ease_out(prog(t, 50.7, 0.4)))
    return img, z, (540, 1150)


def scene_J(t):  # 52.90 - 60.60 venitas / sangre
    img = bg_veins().copy()
    pulse = max(math.sin(math.pi * prog(t, 55.60, 0.35)), math.sin(math.pi * prog(t, 56.30, 0.35)), math.sin(math.pi * prog(t, 59.76, 0.4)))
    vl = veins_layer()
    if pulse > 0.01:
        g = glow_sprite(vl, 14, (255, 70, 100, 255), 1.0)
        paste(img, g, W / 2, H / 2, alpha=pulse)
    img.alpha_composite(vl)
    paths = vein_paths()
    flow = prog(t, 57.20, 0.4)
    d = ImageDraw.Draw(img)
    if flow > 0:
        for i, p in enumerate(paths):
            n = len(p)
            sp = 0.45 if i else 0.25
            for k in range(7 if i else 12):
                u = ((k / (7 if i else 12)) + (t - 57.2) * sp) % 1.0
                if i and u * n > n * flow + 1: continue
                x, y = p[min(n - 1, int(u * n))]
                d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=(150, 245, 255, 255))
    for i, p in enumerate(paths[1:]):
        x, y = p[0]
        s = pop(t, 53.60 + i * 0.12)
        shrink = 1 - 0.55 * ease_in_out(prog(t, 57.38 + i * 0.1, 1.4))
        paste(img, bubble(38), x, y - 34 * shrink, scale=s * shrink * (1 + 0.05 * math.sin(t * 5 + i)))
    if t >= 59.76:
        flash = 1 - prog(t, 59.76, 0.5)
        if flash > 0:
            img.alpha_composite(Image.new('RGBA', img.size, (255, 60, 90, int(70 * flash))))
    return img, lerp(1.0, 1.07, prog(t, 52.9, 7.7)), (540, 980)


def scene_K(t):  # 60.60 - 65.45 pulmones
    lung = pop(t, 61.90)
    br = math.sin(math.pi * prog(t, 63.6, 1.0))
    img = holo_base(t, show_bubble=False, lung=lung, breathe=br)
    x0, y0 = hb(*HB_BELLY); x1, y1 = hb(280, 470)
    pts = [(x0 + 50 * math.sin(i / 30 * math.pi), lerp(y0, y1, i / 30)) for i in range(31)]
    kp = prog(t, 60.80, 1.1)
    draw_path(img, pts, kp, (255, 60, 80, 255), width=12)
    if kp > 0:
        d = ImageDraw.Draw(img)
        for k in range(5):
            u = ((k / 5) + (t - 60.8) * 0.8) % 1.0
            if u > kp: continue
            x, y = pts[int(u * 30)]
            d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=(150, 245, 255, 255))
    paste(img, bubble(50), x0, y0, scale=1 - 0.4 * prog(t, 60.8, 1.5))
    pk = prog(t, 64.24, 0.9)
    if pk > 0:
        mx, my = hb(*HB_MOUTH)
        paste(img, puff_sprite(), mx + 90 * pk, my - 30 * pk, scale=0.3 + 1.0 * pk, alpha=1 - pk)
    z = lerp(1.0, 1.25, ease_in_out(prog(t, 60.6, 1.6)))
    return img, z, (540, 700)


def scene_L(t):  # 65.45 - 73.90 prueba de aliento
    img = bg_teal().copy()
    k = ease_out(prog(t, 65.54, 0.5))
    dx = lerp(700, 0, k)
    blowing = 69.34 <= t < 70.4
    paste(img, P(hair_style='long', hair=(40, 28, 25), skin=(150, 100, 70), shirt=(225, 80, 110), eyes='closed' if blowing else 'open',
                 mouth='o' if blowing else 'flat', cheeks=1.0 if blowing else 0.0, look=(1, 0), arms='down'), 300, 1960, scale=0.95, anchor='b')
    dev_x, dev_y = 790 + dx, 1050
    # tubo
    d = ImageDraw.Draw(img)
    mx, my = 300 + 0.95 * 30, 1960 - 0.95 * (980 - 372)
    tube = [(mx + 40, my), (mx + 140, my + 40), (dev_x - 150, dev_y + 160), (dev_x - 170, dev_y + 200)]
    if k > 0.6:
        d.line(tube[:2] + [(dev_x - 190, dev_y + 160)], fill=(235, 240, 245, 255), width=22, joint='curve')
    paste(img, device_sprite(), dev_x, dev_y)
    if blowing:
        kk = prog(t, 69.34, 1.0)
        for j in range(6):
            u = (kk * 2 + j / 6) % 1
            x, y = lerp(mx + 40, dev_x - 190, u), lerp(my, dev_y + 160, u) - 20
            ImageDraw.Draw(img).ellipse([x - 9, y - 9, x + 9, y + 9], fill=(230, 255, 255, 220))
    # pantalla
    if t >= 69.96:
        sx0, sy0 = dev_x - 150, dev_y - 230
        on = prog(t, 69.96, 0.2)
        sc = layer(300, 330); sd = ImageDraw.Draw(sc)
        sd.rounded_rectangle([0, 0, 299, 329], 22, fill=(30, 60, 80, int(255 * on)))
        h1 = 200 * ease_out(prog(t, 71.40, 0.5)); h2 = 130 * ease_out(prog(t, 71.80, 0.5))
        sd.rectangle([55, 270 - h1, 125, 270], fill=(90, 230, 255, 255))
        sd.rectangle([175, 270 - h2, 245, 270], fill=(180, 140, 255, 255))
        sd.text((90, 300), "H₂", font=font(32, 'x'), fill='white', anchor='mm')
        sd.text((210, 300), "CH₄", font=font(32, 'x'), fill='white', anchor='mm')
        img.alpha_composite(sc, (int(sx0), int(sy0)))
        if t >= 72.74:
            paste(img, bacterium('green'), dev_x + 140, dev_y - 300, scale=pop(t, 72.74) * 0.7)
    if t >= 67.96:
        paste(img, pill("PRUEBA DE ALIENTO", (20, 150, 160), 46), 540, 560, scale=pop(t, 67.96))
    return img, 1.0, (540, 960)


GRID = [(r, c) for r in range(10) for c in range(10)]
GREEN = (3, 6)


def scene_M(t):  # 73.90 - 79.95 olor
    img = bg_holo('purple').copy()
    dim = prog(t, 77.46, 0.3)
    calm = 1 - 0.7 * prog(t, 75.08, 0.6)
    x0, y0, sp = 540 - 4.5 * 72, 820 - 4.5 * 72, 72
    for i, (r, c) in enumerate(GRID):
        if (r, c) == GREEN: continue
        s = pop(t, 73.96 + (r + c) * 0.022)
        if s <= 0: continue
        jx = 6 * calm * math.sin(t * 7 + i * 1.3); jy = 6 * calm * math.cos(t * 6 + i * 0.7)
        paste(img, grid_dot(False), x0 + c * sp + jx, y0 + r * sp + jy, scale=s, alpha=1 - 0.7 * dim)
    gx, gy = x0 + GREEN[1] * sp, y0 + GREEN[0] * sp
    # 78.74 membrana roja (sangre) y rebote
    km = pop(t, 78.74)
    if km > 0:
        L = layer(); d = ImageDraw.Draw(L)
        d.rounded_rectangle([60, 1500, W - 60, 1560], 30, fill=(225, 40, 70, 255))
        for x in range(90, W - 60, 46):
            d.ellipse([x - 9, 1521, x + 9, 1539], fill=(255, 150, 170, 255))
        paste(img, glow_sprite(L.crop((40, 1480, W - 40, 1580)), 12, (255, 60, 90, 200)), 540, 1530, scale=km)
        paste(img, label("SANGRE", 48, fill=(255, 210, 220, 255), stroke=6), 540, 1620, scale=km)
    kd = ease_in_out(prog(t, 78.90, 0.45))
    ku = ease_out(prog(t, 79.35, 0.45))
    gy2 = gy + (1460 - gy) * kd - (1460 - gy) * 0.75 * ku
    s = pop(t, 74.20) * (1 + 0.6 * dim)
    paste(img, grid_dot(True), gx, gy2, scale=s)
    if t >= 77.46:
        paste(img, label("1%", 120, fill=(120, 255, 130, 255), stroke=10), gx + 170, gy - 80, scale=pop(t, 77.46))
    if t >= 74.32 and t < 77.46:
        paste(img, pill("OLOR", (110, 70, 200), 48), 540, 1560, scale=pop(t, 74.32))
    return img, 1.0, (540, 960)


@lru_cache(maxsize=2)
def blanket():
    def fn(im, s):
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, 1180 * s, 1000 * s], 120 * s, fill=(74, 92, 210, 255))
        d.rounded_rectangle([0, 0, 1180 * s, 70 * s], 35 * s, fill=(110, 130, 235, 255))
        for x in (260, 520, 820):
            d.arc([(x - 200) * s, 200 * s, (x + 200) * s, 600 * s], 200, 330, fill=(60, 75, 180, 255), width=10 * s)
    return ss_sprite(1180, 1000, fn)


def scene_N(t):  # 79.95 - 87.25 dormir
    img = bg_bed().copy()
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([250, 640, 830, 980], 90, fill=(200, 215, 255, 255))
    face = P(body=False, eyes='closed', mouth='o' if int(t * 1.2) % 2 else 'flat', skin=(241, 194, 160))
    paste(img, face, 540, 1023, scale=0.95)
    paste(img, blanket(), 540, 1460)
    # Zzz
    for j in range(3):
        u = ((t * 0.45) + j / 3) % 1
        paste(img, label("Z", 70 + j * 10, fill=(220, 225, 255, 255), stroke=6), 740 + 120 * u, 720 - 220 * u, alpha=math.sin(math.pi * u), rot=-15)
    # burbuja bajo la cobija (lupa)
    kx = ease_in_out(prog(t, 83.84, 0.6))
    bx = lerp(540, 880, kx); by = lerp(1360, 1300, kx)
    if t < 86.80:
        paste(img, lens_sprite(110), 540, 1360, scale=0.95, alpha=1 - kx)
        paste(img, bubble(50), bx, by, scale=1 + 0.04 * math.sin(t * 5))
    if t >= 86.80:
        pk = prog(t, 86.80, 0.6)
        paste(img, puff_sprite((150, 230, 90)), 930, 1250, scale=0.4 + 0.8 * pk, alpha=1 - 0.6 * pk)
        paste(img, label("PRRT", 96, fill=(150, 240, 90, 255), stroke=9), 820, 1120, scale=pop(t, 86.80), rot=-10)
    return img, 1.0, (540, 960)


def scene_O(t):  # 87.25 - 91.80 conclusión
    up = path_up()
    k_up = ease_in_out(prog(t, 90.80, 0.5))
    bx, by = up[min(40, int(k_up * 40))]
    img = holo_base(t, show_bubble=False)
    kd = prog(t, 90.32, 0.25)
    if kd > 0:
        draw_path(img, path_down(), kd, (255, 70, 90, 255), dashed=True)
        ex, ey = hb(280, 800)
        paste(img, check_badge(40, False), ex, ey, scale=pop(t, 90.40))
    draw_path(img, up, prog(t, 90.74, 0.25), (120, 255, 170, 255))
    if t < 91.3:
        s = pop(t, 88.34) * (1 + 0.2 * math.sin(math.pi * prog(t, 89.06, 0.3)))
        paste(img, bubble(int(lerp(70, 44, k_up))), bx, by, scale=s)
    if t >= 91.30:
        pk = prog(t, 91.30, 0.5)
        mx, my = hb(*HB_MOUTH)
        paste(img, puff_sprite(), mx + 60 * pk, my - 20 * pk, scale=0.3 + 0.8 * pk, alpha=1 - pk)
        paste(img, check_badge(40, True), mx + 150, my - 60, scale=pop(t, 91.3))
    if t >= 89.06 and t < 90.3:
        paste(img, pill("NO SE BORRA", (200, 50, 80), 50), 540, 1700, scale=pop(t, 89.06))
    return img, 1.0, (540, 960)


def scene_P(t):  # 91.80 - 97.70 cierre + bucle
    looking = ease_out(prog(t, 94.70, 0.25)) * (1 - ease_out(prog(t, 95.74, 0.25)))
    tense = 0.4 + 0.6 * prog(t, 94.70, 0.4)
    lens = pop(t, 96.22, 0.3)
    img = meeting_frame(t, tense=tense, look_side=looking, lens=lens, shake=0)
    kp = prog(t, 91.90, 0.7)
    if 0 < kp < 1:
        x = lerp(-150, 540, ease_out(kp)); y = lerp(1700, 700, ease_out(kp))
        paste(img, plane_sprite(), x, y, scale=0.8, rot=-20)
    if 92.66 <= t < 95.74:
        paste(img, pill("ESE AMIGO", (40, 120, 240), 52), 540, 500 + 10 * math.sin(t * 6), scale=pop(t, 92.66))
        d = ImageDraw.Draw(img)
        s = pop(t, 92.66)
        ay = 580 + 10 * math.sin(t * 6)
        d.polygon([(540 - 26 * s, ay), (540 + 26 * s, ay), (540, ay + 36 * s)], fill=(40, 120, 240, 255))
    return img, 1.0, (540, 1010)


SCENES = [
    (0.00, scene_A), (4.20, scene_B), (7.00, scene_C), (12.85, scene_D), (20.85, scene_E),
    (26.95, scene_F), (38.85, scene_G), (45.40, scene_H), (52.90, scene_J), (60.60, scene_K),
    (65.45, scene_L), (73.90, scene_M), (79.95, scene_N), (87.25, scene_O), (91.80, scene_P),
]
CUTS = [s for s, _ in SCENES[1:]]


def scene_at(t):
    cur = SCENES[0]
    for s in SCENES:
        if t >= s[0]: cur = s
    return cur
