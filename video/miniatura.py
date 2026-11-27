"""Miniatura 3:4 (1080x1440) en el estilo del video."""
import sys, math
from PIL import Image, ImageDraw
from lib import *
from art import person, bg_holo
from scenes import lens_sprite, puff_sprite, label

TW, TH = 1080, 1440
img = rgrad((TW, TH), (540, 760), 900, (120, 60, 200, 255), (20, 8, 40, 255))
g = layer(TW, TH); ImageDraw.Draw(g).ellipse([140, 360, 940, 1160], fill=(255, 90, 160, 90))
img.alpha_composite(blur(g, 140))
for (x, y, r) in ((110, 520, 40), (960, 620, 55), (150, 1050, 30), (930, 1180, 38), (80, 820, 22), (1000, 900, 26)):
    paste(img, bubble(r), x, y)

# personaje en shock
p = person(eyes='big', mouth='o', cheeks=1.0, sweat=True, brows='worried', shirt=(236, 128, 52), arms='down', res=2)
paste(img, p, 540, 1700, scale=0.69, anchor='b')
mx, my = 540, 1700 - (980 - 372) * 1.38
bx, by = 540, 1360

# lupa en la panza + camino hacia la boca
paste(img, lens_sprite(150), bx, by, scale=0.95)
pts = [(bx + 120 * math.sin(i / 30 * math.pi), by - 120 - (by - 120 - (my + 60)) * i / 30) for i in range(31)]
L = layer(TW, TH); ld = ImageDraw.Draw(L); ld.line(pts, fill=(90, 255, 140, 200), width=40, joint='curve')
img.alpha_composite(blur(L, 14))
d = ImageDraw.Draw(img)
for i in range(0, 29, 2):
    d.line([pts[i], pts[i + 1]], fill=(160, 255, 180, 255), width=14)
x1, y1 = pts[-1]
d.polygon([(x1 - 34, y1 + 20), (x1 + 34, y1 + 20), (x1, y1 - 28)], fill=(160, 255, 180, 255))
paste(img, bubble(60), bx, by + 5)
# la burbuja saliendo por la boca
paste(img, puff_sprite(), mx + 150, my - 20, scale=0.75, alpha=0.85)
paste(img, bubble(58), mx + 125, my - 10)
paste(img, alert_badge(56), 820, 560)

# título
paste(img, label("TU PEDO SALE", 112, stroke=12), 540, 120)
t2 = label("POR TU BOCA", 132, fill=(255, 214, 60, 255), stroke=13)
L = layer(TW, TH); ImageDraw.Draw(L).rounded_rectangle([60, 185, 1020, 345], 28, fill=(236, 40, 70, 255))
img.alpha_composite(L)
paste(img, t2, 540, 265, rot=-2)

out = img.convert('RGB')
arr = np.asarray(out).astype(np.int16) + np.random.default_rng(2).integers(-5, 6, (TH, TW, 1))
Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(sys.argv[1], quality=95)
