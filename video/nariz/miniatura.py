"""Miniatura 3:4 (1080x1440): «Tu cerebro borra tu nariz»."""
import sys, math
from PIL import Image, ImageDraw
import escenas as E
from lib import *
from art import alert_badge
from scenes import label

TW, TH = 1080, 1440
img = rgrad((TW, TH), (540, 820), 950, (120, 60, 200, 255), (20, 8, 40, 255))
g = layer(TW, TH); ImageDraw.Draw(g).ellipse([140, 440, 940, 1240], fill=(120, 110, 255, 90))
img.alpha_composite(blur(g, 140))
for (x, y, r) in ((110, 560, 40), (970, 640, 50), (140, 1080, 30), (950, 1200, 36), (70, 840, 22)):
    paste(img, bubble(r), x, y)
# personaje en shock mirando su nariz (bizco)
spr = E.hero(eyes='wide', mouth='o', brows='raised', sweat=True, cheeks=1.0, cross=1.0)
nx, ny = E.put_hero(img, spr, 540, 1280, 1.55, nose_glow=True, nose_scale=1.25)
# círculo rojo punteado alrededor de la nariz
d = ImageDraw.Draw(img)
for i in range(0, 24, 2):
    a0 = i / 24 * 2 * math.pi; a1 = a0 + 2 * math.pi / 24
    d.line([(nx + 135 * math.cos(a0), ny + 25 + 120 * math.sin(a0)), (nx + 135 * math.cos(a1), ny + 25 + 120 * math.sin(a1))], fill=(255, 50, 70, 255), width=14)
# flecha curva: borrador -> nariz
pts = [(900 - 250 * (i / 30) ** 1.1, 560 + 300 * math.sin(i / 30 * math.pi * 0.5)) for i in range(31)]
L = layer(TW, TH); ImageDraw.Draw(L).line(pts, fill=(255, 210, 60, 200), width=40, joint='curve')
img.alpha_composite(blur(L, 14))
d = ImageDraw.Draw(img)
d.line(pts, fill=(255, 225, 90, 255), width=16, joint='curve')
x1, y1 = pts[-1]
d.polygon([(x1 - 46, y1 - 6), (x1 + 6, y1 - 40), (x1 + 14, y1 + 30)], fill=(255, 225, 90, 255))
paste(img, E.brain_sprite(), 900, 500, scale=1.0)
paste(img, alert_badge(56), 190, 560)
paste(img, label("¿?", 120, fill=(255, 225, 80, 255), stroke=11), 200, 900, rot=-12)
# título
paste(img, label("TU CEREBRO BORRA", 98, stroke=12), 540, 115)
L = layer(TW, TH); ImageDraw.Draw(L).rounded_rectangle([50, 180, 1030, 340], 28, fill=(236, 40, 70, 255))
img.alpha_composite(L)
paste(img, label("TU NARIZ", 140, fill=(255, 214, 60, 255), stroke=13), 540, 260, rot=-2)
out = img.convert('RGB')
arr = np.asarray(out).astype(np.int16) + np.random.default_rng(2).integers(-5, 6, (TH, TW, 1))
Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(sys.argv[1], quality=95)
