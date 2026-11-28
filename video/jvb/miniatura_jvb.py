"""Portada TikTok 1080x1920 + miniatura YouTube 1280x720 para JIREN vs BROLY."""
import math, random
from PIL import Image, ImageDraw, ImageFilter
from render_jvb import *


def split_bg(w, h, ang_off=140):
    img = Image.new('RGBA', (w, h))
    L = bg_burst('#ff2a3a', '#2a0508', 270, 900).resize((w, h)); R = bg_burst('#6aff2a', '#062006', 810, 900).resize((w, h))
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).polygon([(w / 2 + ang_off, 0), (w, 0), (w, h), (w / 2 - ang_off, h)], fill=255)
    img.paste(L, (0, 0)); img.paste(R, (0, 0), mask)
    return img, mask


def text(img, txt, col, cx, cy, size, rot=4, sw=18):
    f = F(ANTON, size); bb = f.getbbox(txt, stroke_width=sw)
    t = layer(bb[2] - bb[0] + 60, bb[3] - bb[1] + 60); d = ImageDraw.Draw(t)
    d.text((30 - bb[0], 44 - bb[1]), txt, font=f, fill=(0, 0, 0, 190), stroke_width=sw, stroke_fill=(0, 0, 0, 190))
    d.text((30 - bb[0], 30 - bb[1]), txt, font=f, fill=rgba(col), stroke_width=sw, stroke_fill=rgba('#0b0b10'))
    t = t.rotate(rot, resample=Image.BICUBIC, expand=True)
    paste(img, t, cx - t.width / 2, cy - t.height / 2)


def crack_line(img, w, h, off):
    d = ImageDraw.Draw(img); rnd = random.Random(4)
    pts = []
    for i in range(13):
        f = i / 12; pts.append((w / 2 + off - 2 * off * f + rnd.uniform(-30, 30), h * f))
    d.line(pts, fill=rgba('#ffffff', 90), width=40, joint='curve'); d.line(pts, fill=rgba('#ffffff'), width=12, joint='curve')


def cover():
    img, _ = split_bg(W, H)
    speedlines(img, 1.0, '#ffffff', 70, 540, 900, 50)
    crack_line(img, W, H, 140)
    # primeros planos en diagonal, Broly más grande (el favorito), Jiren abajo (el que cae)
    g = layer(); ImageDraw.Draw(g).ellipse([380, 650, 1180, 1450], fill=rgba('#8aff3a', 170)); img.alpha_composite(blur(g, 90))
    g = layer(); ImageDraw.Draw(g).ellipse([-100, 1150, 620, 1850], fill=rgba('#ff3a3a', 170)); img.alpha_composite(blur(g, 90))
    head(img, 'broly_legendario', 760, 1020, 1.25)
    head(img, 'jiren_rojo', 300, 1430, 1.0)
    star(img, 500, 1290, 1.0, 0.92, 280, '#ffffff', '#d8b0ff')
    for k in range(3): lightning(img, 500, 1290, random.Random(k).uniform(550, 1000), random.Random(k + 20).uniform(1400, 1800), k, w=6, jit=45)
    text(img, 'VS', WHITE, 500, 1290, 150, 0, 14)
    text(img, '¿QUIÉN', WHITE, 470, 300, 230, 4)
    text(img, 'CAE PRIMERO?', GOLD, 540, 520, 175, 4)
    # placa nombres
    text(img, 'JIREN', RED, 270, 1780, 150, 5, 14); text(img, 'BROLY', GREEN, 820, 1560, 160, -4, 14)
    return img


def thumb():
    w, h = 1280, 720
    img, _ = split_bg(w, h, 90)
    img = img.resize((w, h))
    crack_line(img, w, h, 90)
    aura(img, 960, 760, 0.42, 0.3, '#8aff3a'); aura(img, 300, 760, 0.36, 0.7, '#ff3a3a')
    head(img, 'broly_legendario', 980, 330, 0.95)
    head(img, 'jiren_rojo', 290, 360, 0.80)
    star(img, 640, 380, 1.0, 0.92, 230, '#ffffff', '#d8b0ff')
    for k in range(4): lightning(img, 640, 380, random.Random(k).uniform(400, 880), random.Random(k + 20).uniform(0, 720), k, w=5, jit=40)
    text(img, '¿QUIÉN CAE?', GOLD, 640, 600, 150, 3, 14)
    return img


def cover34():
    w, h = 1080, 1440
    img, _ = split_bg(w, h, 120)
    speedlines(img, 1.0, '#ffffff', 70, 540, 700, 50)
    crack_line(img, w, h, 120)
    g = layer(w, h); ImageDraw.Draw(g).ellipse([380, 420, 1180, 1220], fill=rgba('#8aff3a', 170)); img.alpha_composite(blur(g, 90))
    g = layer(w, h); ImageDraw.Draw(g).ellipse([-100, 820, 620, 1500], fill=rgba('#ff3a3a', 170)); img.alpha_composite(blur(g, 90))
    head(img, 'broly_legendario', 770, 790, 1.08)
    head(img, 'jiren_rojo', 290, 1100, 0.88)
    star(img, 500, 990, 1.0, 0.92, 250, '#ffffff', '#d8b0ff')
    for k in range(3): lightning(img, 500, 990, random.Random(k).uniform(560, 1000), random.Random(k + 20).uniform(1150, 1400), k, w=6, jit=40)
    text(img, 'VS', WHITE, 500, 990, 130, 0, 13)
    text(img, '¿QUIÉN', WHITE, 470, 175, 200, 4)
    text(img, 'CAE PRIMERO?', GOLD, 540, 365, 150, 4)
    text(img, 'BROLY', GREEN, 830, 1240, 140, -4, 13)
    text(img, 'JIREN', RED, 270, 1340, 130, 5, 13)
    return img


if __name__ == '__main__':
    cover().convert('RGB').save('PORTADA_TIKTOK_1080x1920.png')
    thumb().convert('RGB').save('MINIATURA_YOUTUBE_1280x720.jpg', quality=95)
    cover34().convert('RGB').save('MINIATURA_3x4_1080x1440.jpg', quality=95)
