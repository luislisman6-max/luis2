"""Ficha de personajes KAEN vs TAMBO sobre fondo burst (mismo estilo que personajes/ficha.py)."""
import math, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
D = os.path.dirname(os.path.abspath(__file__))
items = [('kaen', 'KAEN', '#ff6a1f', '#2a0e06'), ('kaen_brasa', 'MODO BRASA', '#ffb02e', '#3a1a06'),
         ('kaen_rodillas', 'KAEN APAGADO', '#a04a2a', '#1a0a06'),
         ('tambo', 'TAMBO', '#2ab0b4', '#06242a'), ('tambo_tambor', 'FORMA TAMBOR', '#e8eefc', '#2a3048'),
         ('tambo_viejo', 'TAMBO AGOTADO', '#9aa6c0', '#1a1e2a')]
W, H = 720, 1280
def hexc(h, a=255): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (a,)
F = ImageFont.truetype(os.path.join(D, '..', 'jvb', 'fonts', 'Anton.ttf'), 70)
sheet = Image.new('RGB', (W * 3, H * 2))
for k, (f, name, col, dark) in enumerate(items):
    c = Image.new('RGBA', (W, H), hexc(dark)); d = ImageDraw.Draw(c)
    cx, cy = W // 2, 560
    for i in range(28):
        a0 = i * 2 * math.pi / 28; a1 = a0 + math.pi / 28
        d.polygon([(cx, cy), (cx + 1600*math.cos(a0), cy + 1600*math.sin(a0)), (cx + 1600*math.cos(a1), cy + 1600*math.sin(a1))], fill=hexc(col, 110))
    glow = Image.new('RGBA', (W, H)); ImageDraw.Draw(glow).ellipse([60, 160, 660, 960], fill=hexc(col, 200))
    c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(90)))
    ch = Image.open(os.path.join(D, 'personajes', f + '.png')); ch = ch.resize((int(ch.width*.6), int(ch.height*.6)))
    c.alpha_composite(ch, ((W - ch.width)//2, 80))
    tw = d.textlength(name, font=F)
    d.text(((W - tw)/2, 1150), name, font=F, fill='white', stroke_width=7, stroke_fill='black')
    sheet.paste(c.convert('RGB'), ((k % 3) * W, (k // 3) * H))
sheet.save(os.path.join(D, 'ficha_kvt.png'))
