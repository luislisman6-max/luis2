"""Miniatura 3:4 (1080x1440): «Tu piel esconde un mapa»."""
import sys, math
from PIL import Image, ImageDraw
import escenas as E
from lib import *
from art import alert_badge, bubble
from scenes import label

TW, TH = 1080, 1440
img = rgrad((TW, TH), (540, 820), 950, (120, 60, 200, 255), (20, 8, 40, 255))
g = layer(TW, TH); ImageDraw.Draw(g).ellipse([140, 440, 940, 1240], fill=(120, 110, 255, 90))
img.alpha_composite(blur(g, 140))
for (x, y, r) in ((110, 560, 40), (970, 520, 50), (90, 1000, 30), (1000, 1250, 36), (60, 760, 22)):
    paste(img, bubble(r), x, y)
# brazo con las líneas brillando (cruza la imagen) + personaje en shock
arm = layer(); arm.alpha_composite(E.arm_layer())
tint = layer(); tint.paste(Image.new('RGBA', (1080, 1920), (40, 90, 200, 60)), (0, 0), E.arm_mask())
arm.alpha_composite(E.arm_stripes('glow')); arm.alpha_composite(E.arm_stripes('glow'))
spr = E.P2(shirt=(236, 92, 70), eyes='wide', mouth='o', brows='raised', sweat=True, cheeks=1.0, look=(1, 1))
paste(img, arm, 515, 610, scale=0.95)
paste(img, spr, 330, 1390, scale=1.22)
# flecha curva: cara -> brazo
pts = [(560 + 220 * (i / 30), 1060 - 230 * math.sin(i / 30 * math.pi * 0.5)) for i in range(31)]
L = layer(TW, TH); ImageDraw.Draw(L).line(pts, fill=(255, 210, 60, 200), width=40, joint='curve')
img.alpha_composite(blur(L, 14))
d = ImageDraw.Draw(img)
d.line(pts, fill=(255, 225, 90, 255), width=16, joint='curve')
x1, y1 = pts[-1]
d.polygon([(x1 - 40, y1 + 20), (x1 + 40, y1 + 20), (x1, y1 - 40)], fill=(255, 225, 90, 255))
paste(img, alert_badge(56), 930, 1000)
paste(img, label("¿?", 110, fill=(255, 225, 80, 255), stroke=11), 140, 1000, rot=-12)
# título
paste(img, label("TU PIEL ESCONDE", 100, stroke=12), 540, 115)
L = layer(TW, TH); ImageDraw.Draw(L).rounded_rectangle([50, 180, 1030, 340], 28, fill=(236, 40, 70, 255))
img.alpha_composite(L)
paste(img, label("UN MAPA", 140, fill=(255, 214, 60, 255), stroke=13), 540, 260, rot=-2)
out = img.convert('RGB')
arr = np.asarray(out).astype(np.int16) + np.random.default_rng(2).integers(-5, 6, (TH, TW, 1))
Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(sys.argv[1], quality=95)
