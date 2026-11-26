"""Miniatura 3:4 (1080x1440): «Tu cuerpo te lanza al vacío mientras duermes»."""
import sys, math
from PIL import Image, ImageDraw
import escenas as E
from lib import *
from art import person
from scenes import label

TW, TH = 1080, 1440
img = rgrad((TW, TH), (540, 800), 950, (120, 60, 200, 255), (20, 8, 40, 255))
g = layer(TW, TH); ImageDraw.Draw(g).ellipse([140, 420, 940, 1220], fill=(120, 110, 255, 90))
img.alpha_composite(blur(g, 140))
for (x, y, r) in ((110, 560, 40), (970, 640, 50), (140, 1080, 30), (950, 1200, 36), (70, 840, 22)):
    paste(img, bubble(r), x, y)
# estelas de caída
L = layer(TW, TH); d = ImageDraw.Draw(L)
for x, y, ln in ((200, 420, 260), (330, 520, 200), (760, 470, 280), (880, 560, 220), (560, 400, 160)):
    d.line([(x, y), (x, y + ln)], fill=(210, 200, 255, 150), width=6)
img.alpha_composite(blur(L, 2))
# cama pequeña abajo a la izquierda (de donde «cae»)
d = ImageDraw.Draw(img)
d.rounded_rectangle([40, 1230, 470, 1440], 40, fill=(74, 92, 210, 255))
d.rounded_rectangle([70, 1170, 300, 1260], 40, fill=(214, 224, 255, 255))
# flecha curva: cama -> vacío
pts = [(300 + 220 * math.sin(i / 30 * math.pi * 0.5), 1180 - 330 * (i / 30) ** 0.8) for i in range(31)]
L = layer(TW, TH); ImageDraw.Draw(L).line(pts, fill=(255, 210, 60, 200), width=40, joint='curve')
img.alpha_composite(blur(L, 14))
d = ImageDraw.Draw(img)
d.line(pts, fill=(255, 225, 90, 255), width=16, joint='curve')
x1, y1 = pts[-1]
d.polygon([(x1 - 38, y1 + 26), (x1 + 38, y1 + 10), (x1 + 8, y1 - 40)], fill=(255, 225, 90, 255))
# personaje cayendo en shock
cx, cy = 660, 760
E.arms_flail(img, cx, cy, 0.78, 0.4)
E.legs_flail(img, cx, cy, 0.78, 0.4)
p = person(eyes='big', mouth='o', cheeks=1.0, sweat=True, brows='raised', shirt=E.PJ, arms='none', skin=E.SKIN, hair=E.HAIR, res=2)
paste(img, p, cx, cy, scale=0.39)
paste(img, alert_badge(56), 300, 520)
paste(img, label("¡ZAS!", 110, fill=(255, 225, 80, 255), stroke=11), 250, 900, rot=-12)
# título
paste(img, label("TU CEREBRO CREE", 104, stroke=12), 540, 115)
L = layer(TW, TH); ImageDraw.Draw(L).rounded_rectangle([50, 180, 1030, 340], 28, fill=(236, 40, 70, 255))
img.alpha_composite(L)
paste(img, label("QUE TE CAES", 132, fill=(255, 214, 60, 255), stroke=13), 540, 260, rot=-2)
out = img.convert('RGB')
arr = np.asarray(out).astype(np.int16) + np.random.default_rng(2).integers(-5, 6, (TH, TW, 1))
Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(sys.argv[1], quality=95)
