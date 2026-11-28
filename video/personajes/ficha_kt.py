"""Ficha de personajes KAEN y TAMBO sobre aura radial."""
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
items = [('kaen', 'KAEN', '#ff7a1a', '#2a1206'), ('kaen_brasa', 'MODO BRASA', '#ff8a1f', '#2a1206'),
         ('kaen_rodillas', 'APAGADO', '#9a6a4a', '#1a1214'),
         ('tambo', 'TAMBO', '#1aa6b8', '#06202a'), ('tambo_tambor', 'FORMA TAMBOR', '#3ae8ff', '#061a2a'),
         ('tambo_anciano', 'AL LÍMITE', '#9fd6e0', '#141a24')]
W, H = 720, 1280
def hexc(h, a=255): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (a,)
F = ImageFont.truetype('../jvb/fonts/Anton.ttf', 74)
cards = []
for f, name, col, dark in items:
    c = Image.new('RGBA', (W, H), hexc(dark)); d = ImageDraw.Draw(c)
    cx, cy = W // 2, 560
    for i in range(28):
        a0 = i * 2 * math.pi / 28; a1 = a0 + math.pi / 28
        d.polygon([(cx, cy), (cx + 1600 * math.cos(a0), cy + 1600 * math.sin(a0)), (cx + 1600 * math.cos(a1), cy + 1600 * math.sin(a1))], fill=hexc(col, 90))
    glow = Image.new('RGBA', (W, H)); ImageDraw.Draw(glow).ellipse([60, 160, 660, 960], fill=hexc(col, 170))
    c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(90)))
    ch = Image.open(f + '.png'); ch = ch.resize((int(ch.width * 0.6), int(ch.height * 0.6)), Image.LANCZOS)
    c.alpha_composite(ch, ((W - ch.width) // 2, 80))
    d = ImageDraw.Draw(c); tw = d.textlength(name, font=F)
    d.text(((W - tw) / 2, 1150), name, font=F, fill=col if col != '#9a6a4a' else 'white', stroke_width=7, stroke_fill='black')
    cards.append(c)
sheet = Image.new('RGB', (W * len(cards), H))
for i, c in enumerate(cards): sheet.paste(c.convert('RGB'), (i * W, 0))
sheet.save('ficha_kaen_tambo.png')
g = Image.new('RGB', (W * 5, H))
for i, n in enumerate(['kaen_golpe', 'kaen_brasa_golpe', 'tambo_golpe', 'tambo_tambor_golpe', 'tambo_tambor_gigante']):
    ch = Image.open(n + '.png'); ch = ch.resize((int(ch.width * 0.36), int(ch.height * 0.36)), Image.LANCZOS)
    bg = Image.new('RGBA', (W, H), (40, 40, 60, 255)); bg.alpha_composite(ch, ((W - ch.width) // 2, 300)); g.paste(bg.convert('RGB'), (i * W, 0))
g.save('ficha_kaen_tambo_golpes.png')
