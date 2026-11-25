"""Herramientas de dibujo comunes (estilo «Mente Curiosa»: 2D vectorial con degradados, brillos y grano)."""
import math, random
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

W, H, FPS = 1080, 1920, 30
FONT_B = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FONT_X = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
FONT_K = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"


@lru_cache(maxsize=64)
def font(size, kind="x"):
    return ImageFont.truetype({"b": FONT_B, "x": FONT_X, "k": FONT_K}[kind], int(size))


def rgba(h, a=255):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def layer(w=W, h=H):
    return Image.new('RGBA', (w, h), (0, 0, 0, 0))


def vgrad(size, top, bot):
    w, h = size
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    a = np.array(top, np.float32); b = np.array(bot, np.float32)
    arr = np.broadcast_to(a + (b - a) * t, (h, w, len(top)))
    return Image.fromarray(np.ascontiguousarray(arr).astype(np.uint8), 'RGBA' if len(top) == 4 else 'RGB')


def rgrad(size, center, radius, inner, outer):
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.clip(np.sqrt((xx - center[0]) ** 2 + (yy - center[1]) ** 2) / radius, 0, 1)[..., None]
    a = np.array(inner, np.float32); b = np.array(outer, np.float32)
    return Image.fromarray((a + (b - a) * d).astype(np.uint8), 'RGBA')


def blur(im, r):
    return im.filter(ImageFilter.GaussianBlur(r))


def wave(x, amp, per, ph=0.0):
    return amp * math.sin(x / per * 2 * math.pi + ph)


# ---------------- easing ----------------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def prog(t, t0, dur):
    return clamp((t - t0) / dur) if dur > 0 else float(t >= t0)


def ease_out(x):
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def ease_back(x, s=1.9):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    x -= 1
    return x * x * ((s + 1) * x + s) + 1


def pop(t, t0, dur=0.28):
    """escala 0 -> overshoot -> 1"""
    return ease_back(prog(t, t0, dur))


def lerp(a, b, x):
    return a + (b - a) * x


# ---------------- sprites ----------------
def set_alpha(im, a):
    if a >= 0.999: return im
    r, g, b, al = im.split()
    al = al.point(lambda v: int(v * a))
    return Image.merge('RGBA', (r, g, b, al))


def paste(dst, spr, cx, cy, scale=1.0, alpha=1.0, rot=0.0, anchor='c'):
    """Pega un sprite RGBA centrado en (cx, cy) con escala/rotación/opacidad, recortando a los bordes."""
    if scale <= 0.01 or alpha <= 0.01: return
    if abs(scale - 1) > 1e-3:
        spr = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.BILINEAR)
    if abs(rot) > 0.05:
        spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
    spr = set_alpha(spr, alpha)
    if anchor == 'c':
        x, y = int(round(cx - spr.width / 2)), int(round(cy - spr.height / 2))
    elif anchor == 'b':
        x, y = int(round(cx - spr.width / 2)), int(round(cy - spr.height))
    else:
        x, y = int(cx), int(cy)
    sx0, sy0 = max(0, -x), max(0, -y)
    sx1, sy1 = min(spr.width, dst.width - x), min(spr.height, dst.height - y)
    if sx1 <= sx0 or sy1 <= sy0: return
    dst.alpha_composite(spr, (x + sx0, y + sy0), (sx0, sy0, sx1, sy1))


def ss_sprite(w, h, draw_fn, ss=2):
    """Dibuja con supermuestreo y reduce (bordes suaves)."""
    big = Image.new('RGBA', (w * ss, h * ss), (0, 0, 0, 0))
    draw_fn(big, ss)
    return big.resize((w, h), Image.LANCZOS)


def glow_sprite(spr, radius, color=None, strength=1.0):
    """Halo difuminado alrededor de un sprite."""
    pad = int(radius * 2.5)
    base = Image.new('RGBA', (spr.width + pad * 2, spr.height + pad * 2), (0, 0, 0, 0))
    if color is None:
        base.paste(spr, (pad, pad), spr)
    else:
        sol = Image.new('RGBA', spr.size, color)
        base.paste(sol, (pad, pad), spr.split()[3])
    g = blur(base, radius)
    if strength != 1.0:
        g = set_alpha(g, min(1.0, strength))
    out = g.copy()
    out.alpha_composite(spr, (pad, pad))
    return out


# ---------------- reusable art ----------------
@lru_cache(maxsize=16)
def bubble(r):
    """Burbuja de gas translúcida (como la del video de referencia)."""
    R = r + 12
    def fn(im, s):
        cx = cy = R * s
        rr = r * s
        L = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(255, 232, 242, 40))
        im.alpha_composite(L)
        L = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(255, 210, 228, 150), width=int(rr * 0.12))
        mask = Image.new('L', im.size, 0); ImageDraw.Draw(mask).ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=255)
        g = blur(L, rr * 0.07); g2 = Image.new('RGBA', im.size, (0, 0, 0, 0)); g2.paste(g, (0, 0), mask)
        im.alpha_composite(g2)
        d = ImageDraw.Draw(im)
        L = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(255, 248, 252, 240), width=max(2, int(rr * 0.022)))
        d.arc([cx - rr * 0.9, cy - rr * 0.9, cx + rr * 0.9, cy + rr * 0.9], 20, 70, fill=(255, 255, 255, 170), width=max(2, int(rr * 0.022)))
        im.alpha_composite(L)
        hl = Image.new('RGBA', (int(rr * 0.75), int(rr * 0.36)), (0, 0, 0, 0))
        ImageDraw.Draw(hl).ellipse([0, 0, hl.width - 1, hl.height - 1], fill=(255, 255, 255, 240))
        hl = hl.rotate(32, expand=True, resample=Image.BICUBIC)
        im.alpha_composite(hl, (int(cx - rr * 0.72), int(cy - rr * 0.70)))
        d = ImageDraw.Draw(im)
        q = rr * 0.09
        d.ellipse([cx - rr * 0.17 - q, cy - rr * 0.84 - q, cx - rr * 0.17 + q, cy - rr * 0.84 + q], fill=(255, 255, 255, 220))
    return ss_sprite(2 * R, 2 * R, fn)


@lru_cache(maxsize=8)
def alert_badge(r=46):
    def fn(im, s):
        c = (r + 30) * s; rr = r * s
        L = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.ellipse([c - rr - 16 * s, c - rr - 16 * s, c + rr + 16 * s, c + rr + 16 * s], fill=(255, 40, 70, 170))
        im.alpha_composite(blur(L, 14 * s))
        d = ImageDraw.Draw(im)
        d.ellipse([c - rr, c - rr, c + rr, c + rr], fill=rgba('#e8213e'), outline=rgba('#ffd5db'), width=4 * s)
        d.text((c, c + 2 * s), "!", font=font(r * 1.45 * s, 'k'), fill='white', anchor='mm')
    return ss_sprite(2 * (r + 30), 2 * (r + 30), fn)


@lru_cache(maxsize=8)
def check_badge(r=40, ok=True):
    def fn(im, s):
        c = (r + 24) * s; rr = r * s
        col = (46, 211, 122, 255) if ok else (230, 50, 70, 255)
        L = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(L).ellipse([c - rr - 10 * s, c - rr - 10 * s, c + rr + 10 * s, c + rr + 10 * s], fill=col[:3] + (150,))
        im.alpha_composite(blur(L, 12 * s))
        d = ImageDraw.Draw(im)
        d.ellipse([c - rr, c - rr, c + rr, c + rr], fill=col, outline=(255, 255, 255, 255), width=4 * s)
        if ok:
            d.line([(c - rr * .45, c + rr * .02), (c - rr * .1, c + rr * .38), (c + rr * .5, c - rr * .38)], fill='white', width=int(rr * .26), joint='curve')
        else:
            k = rr * .36
            d.line([(c - k, c - k), (c + k, c + k)], fill='white', width=int(rr * .26))
            d.line([(c + k, c - k), (c - k, c + k)], fill='white', width=int(rr * .26))
    return ss_sprite(2 * (r + 24), 2 * (r + 24), fn)


def text_sprite(txt, size, fill=(255, 255, 255, 255), kind='x', stroke=0, stroke_fill=(30, 10, 25, 255), shadow=True):
    f = font(size, kind)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    b = tmp.textbbox((0, 0), txt, font=f, stroke_width=stroke)
    pad = int(size * 0.35) + stroke
    w, h = b[2] - b[0] + pad * 2, b[3] - b[1] + pad * 2
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    if shadow:
        sh = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((pad - b[0] + 3, pad - b[1] + 6), txt, font=f, fill=(0, 0, 0, 150), stroke_width=stroke, stroke_fill=(0, 0, 0, 150))
        im.alpha_composite(blur(sh, max(3, size // 12)))
    ImageDraw.Draw(im).text((pad - b[0], pad - b[1]), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return im


def grain_tiles(n=6, seed=3):
    rng = np.random.default_rng(seed)
    return [rng.normal(0, 4.2, (H, W, 1)).astype(np.float32) for _ in range(n)]


@lru_cache(maxsize=1)
def vignette():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.47) / (H * 0.62)) ** 2)
    return np.clip(1.06 - 0.42 * d ** 2, 0.5, 1.04)[..., None].astype(np.float32)
