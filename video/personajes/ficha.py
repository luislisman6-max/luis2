"""Ficha de personajes sobre aura radial (estilo referencia)."""
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
items = [('jiren', 'JIREN', '#d9263a', '#3a0d14'), ('jiren_rojo', 'JIREN AL LÍMITE', '#ff4a5e', '#3a0d14'),
         ('broly_base', 'BROLY', '#2fae4a', '#0e2414'), ('broly_ssj', 'BROLY SSJ', '#ffc928', '#3a2a06'),
         ('broly_legendario', 'BROLY LEGENDARIO', '#8fe83a', '#0e2414')]
W, H = 720, 1280
def hexc(h, a=255): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (a,)
try: F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 58)
except Exception: F = ImageFont.load_default()
cards = []
for f, name, col, dark in items:
    c = Image.new('RGBA', (W, H), hexc(dark)); d = ImageDraw.Draw(c)
    cx, cy = W // 2, 560
    for i in range(28):
        a0 = i * 2 * math.pi / 28; a1 = a0 + math.pi / 28
        d.polygon([(cx, cy), (cx + 1600 * math.cos(a0), cy + 1600 * math.sin(a0)), (cx + 1600 * math.cos(a1), cy + 1600 * math.sin(a1))], fill=hexc(col, 110))
    glow = Image.new('RGBA', (W, H)); ImageDraw.Draw(glow).ellipse([60, 160, 660, 960], fill=hexc(col, 200))
    c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(90)))
    ch = Image.open(f + '.png'); ch = ch.resize((int(ch.width * 0.6), int(ch.height * 0.6)))
    c.alpha_composite(ch, ((W - ch.width) // 2, 80))  # lienzo ancho centrado
    tw = d.textlength(name, font=F)
    d.text(((W - tw) / 2, 1160), name, font=F, fill='white', stroke_width=6, stroke_fill='black')
    cards.append(c)
sheet = Image.new('RGB', (W * 5, H))
for i, c in enumerate(cards): sheet.paste(c.convert('RGB'), (i * W, 0))
sheet.save('ficha_personajes.png')
