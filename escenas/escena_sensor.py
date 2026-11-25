import math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

W, H = 1080, 1920
S = 2  # supersample
w, h = W * S, H * S
random.seed(7); np.random.seed(7)
FB = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FX = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"

def rgba(hexs, a=255):
    hexs = hexs.lstrip('#'); return tuple(int(hexs[i:i+2], 16) for i in (0, 2, 4)) + (a,)

def vgrad(size, top, bot):
    ww, hh = size
    t = np.linspace(0, 1, hh)[:, None]
    a = np.array(top, float); b = np.array(bot, float)
    arr = (a + (b - a) * t[..., None]) * np.ones((hh, ww, 1))
    return Image.fromarray(arr.astype(np.uint8), 'RGBA' if len(top) == 4 else 'RGB')

def layer():
    return Image.new('RGBA', (w, h), (0, 0, 0, 0))

def wave(x, amp, per, ph):
    return amp * math.sin(x / per * 2 * math.pi + ph)

img = vgrad((w, h), rgba('#24091c'), rgba('#160612')).convert('RGBA')

# ---------- geometry ----------
TOP_A, TOP_B = 300 * S, 560 * S        # upper wall
BOT_A, BOT_B = 1330 * S, 1600 * S      # lower wall
SPH_X = 830 * S                        # sphincter left edge

# ---------- lumen (inner tube) ----------
lum = vgrad((w, BOT_A - TOP_B + 80 * S), rgba('#8e2148'), rgba('#5e1233'))
img.alpha_composite(lum, (0, TOP_B - 40 * S))
# soft light spot in lumen center
glow = layer(); gd = ImageDraw.Draw(glow)
gd.ellipse([150 * S, 650 * S, 900 * S, 1200 * S], fill=rgba('#c2456f', 90))
img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120 * S)))

# villi: wavy vertical lines
vil = layer(); vd = ImageDraw.Draw(vil)
for i, x0 in enumerate(range(-20 * S, SPH_X + 60 * S, 78 * S)):
    ph = random.random() * 6
    pts = [(x0 + wave(y, 16 * S, 260 * S, ph), y) for y in range(TOP_B - 40 * S, BOT_A + 40 * S, 6 * S)]
    vd.line(pts, fill=rgba('#c45a80', 150), width=7 * S, joint='curve')
    pts2 = [(x + 30 * S, y) for x, y in pts]
    vd.line(pts2, fill=rgba('#6a1638', 120), width=5 * S, joint='curve')
img.alpha_composite(vil.filter(ImageFilter.GaussianBlur(1.2 * S)))

# ---------- yellow food / mucus layer ----------
food = layer(); fd = ImageDraw.Draw(food)
top_edge = [(x, 1175 * S + wave(x, 14 * S, 300 * S, 1.0) + wave(x, 6 * S, 90 * S, 2)) for x in range(0, w + 8, 8)]
fd.polygon(top_edge + [(w, BOT_A + 30 * S), (0, BOT_A + 30 * S)], fill=rgba('#e3a23a'))
# marbling
for k in range(14):
    y = random.randint(1200, 1310) * S; x = random.randint(0, 800) * S
    fd.line([(x + j * 30 * S, y + wave(j * 30 * S, 8 * S, 120 * S, k)) for j in range(8)], fill=rgba('#f6cd6a', 200), width=4 * S, joint='curve')
fd.line(top_edge, fill=rgba('#f8d77d'), width=7 * S)
img.alpha_composite(food)

# ---------- muscle walls (striped) ----------
def wall(y0, y1, inner_y, inner_up):
    lay = layer(); d = ImageDraw.Draw(lay)
    edge = [(x, inner_y + wave(x, 10 * S, 520 * S, 0.6)) for x in range(0, w + 8, 8)]
    if inner_up:   # bottom wall: inner edge on top
        poly = edge + [(w, y1), (0, y1)]
    else:
        poly = [(0, y0), (w, y0)] + edge[::-1]
    mask = Image.new('L', (w, h), 0); ImageDraw.Draw(mask).polygon(poly, fill=255)
    base = vgrad((w, h), rgba('#d24a73'), rgba('#a8325a')) if not inner_up else vgrad((w, h), rgba('#b53a62'), rgba('#d6527a'))
    stripes = layer(); sd = ImageDraw.Draw(stripes)
    for x in range(0, w, 34 * S):
        sd.rectangle([x, 0, x + 12 * S, h], fill=rgba('#8f2449', 95))
        sd.rectangle([x + 18 * S, 0, x + 21 * S, h], fill=rgba('#ee7b9b', 60))
    base.alpha_composite(stripes)
    # shading toward outer edge
    shade = vgrad((w, h), (20, 4, 12, 150), (20, 4, 12, 0)) if not inner_up else vgrad((w, h), (20, 4, 12, 0), (20, 4, 12, 150))
    base.alpha_composite(shade)
    lay.paste(base, (0, 0), mask)
    d = ImageDraw.Draw(lay)
    d.line(edge, fill=rgba('#ffc2d2', 235), width=6 * S)          # bright inner rim
    d.line([(x, y + (14 * S if inner_up else -14 * S)) for x, y in edge], fill=rgba('#ff9db8', 90), width=10 * S)
    return lay

img.alpha_composite(wall(TOP_A, TOP_B, TOP_B, False))
img.alpha_composite(wall(BOT_A, BOT_B, BOT_A, True))
# dark mucosal ridge strip above the top wall (like reference)
dd = ImageDraw.Draw(img, 'RGBA')
dd.rectangle([0, 0, w, TOP_A], fill=rgba('#1c0716'))
dd.rectangle([0, BOT_B, w, h], fill=rgba('#1c0716'))
rim = layer(); rd = ImageDraw.Draw(rim)
rd.line([(x, TOP_A + wave(x, 6 * S, 400 * S, 2)) for x in range(0, w + 8, 8)], fill=rgba('#7d2445'), width=10 * S)
rd.line([(x, BOT_B + wave(x, 6 * S, 400 * S, 1)) for x in range(0, w + 8, 8)], fill=rgba('#7d2445'), width=10 * S)
img.alpha_composite(rim)

# ---------- sphincter (red ring muscle, right side) ----------
sph = layer(); sd = ImageDraw.Draw(sph)
left = [(SPH_X + wave(y, 10 * S, 700 * S, 0.3), y) for y in range(TOP_A - 30 * S, BOT_B + 40 * S, 8)]
sd.polygon(left + [(w + 10, BOT_B + 40 * S), (w + 10, TOP_A - 30 * S)], fill=rgba('#c4213a'))
sph_t = vgrad((w, h), rgba('#e5364f'), rgba('#a9182f'))
m = sph.split()[3]
sph2 = layer(); sph2.paste(sph_t, (0, 0), m)
sl_ = layer(); s2 = ImageDraw.Draw(sl_)
for i, x in enumerate(range(SPH_X, w, 26 * S)):
    pts = [(x + wave(y, 8 * S, 700 * S, 0.3) + (y - h / 2) * 0.03, y) for y in range(TOP_A - 30 * S, BOT_B + 40 * S, 10 * S)]
    s2.line(pts, fill=rgba('#7e0f22', 130), width=4 * S)
    s2.line([(a + 9 * S, b) for a, b in pts], fill=rgba('#ff6b7e', 70), width=2 * S)
for y in (TOP_A + 40 * S, BOT_B - 60 * S):   # little tendon bands
    s2.line([(SPH_X + 70 * S, y), (SPH_X + 150 * S, y + 4 * S)], fill=rgba('#ffd0d6', 200), width=4 * S)
s2.line(left, fill=rgba('#ff8f9e', 220), width=6 * S)
sph2.alpha_composite(sl_)
img.alpha_composite(sph2)
# closed "gate" bulge where bubble presses + red glow
gl = layer(); g2 = ImageDraw.Draw(gl)
g2.ellipse([SPH_X - 90 * S, 780 * S, SPH_X + 130 * S, 1020 * S], fill=rgba('#ff3a55', 200))
img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(45 * S)))
bulge = layer(); b2 = ImageDraw.Draw(bulge)
b2.chord([SPH_X - 60 * S, 760 * S, SPH_X + 120 * S, 1040 * S], 90, 270, fill=rgba('#e02a44'))
b2.arc([SPH_X - 60 * S, 760 * S, SPH_X + 120 * S, 1040 * S], 90, 270, fill=rgba('#ffc0c9'), width=5 * S)
img.alpha_composite(bulge)

# ---------- scanner beam from sphincter to bubble ----------
BX, BY, BR = 545 * S, 900 * S, 235 * S
beam = layer(); bd = ImageDraw.Draw(beam)
src = (SPH_X - 40 * S, 900 * S)
bd.polygon([src, (BX - BR * 0.55, BY - BR * 0.95), (BX - BR * 0.55, BY + BR * 0.95)], fill=(80, 230, 255, 38))
for k in range(-7, 8):
    ty = BY + k * (BR * 0.95 / 7)
    bd.line([src, (BX - BR * 0.55, ty)], fill=(150, 240, 255, 55), width=2 * S)
bm = Image.new('L', (w, h), 0); ImageDraw.Draw(bm).ellipse([BX - BR, BY - BR, BX + BR, BY + BR], fill=255)
beam2 = layer(); beam2.paste(beam.filter(ImageFilter.GaussianBlur(6 * S)), (0, 0), bm)
img.alpha_composite(beam2)
# emitter eye
em = layer(); e2 = ImageDraw.Draw(em)
e2.ellipse([src[0] - 34 * S, src[1] - 34 * S, src[0] + 34 * S, src[1] + 34 * S], fill=(90, 235, 255, 255))
img.alpha_composite(em.filter(ImageFilter.GaussianBlur(18 * S)))
e3 = ImageDraw.Draw(img, 'RGBA')
e3.ellipse([src[0] - 16 * S, src[1] - 16 * S, src[0] + 16 * S, src[1] + 16 * S], fill=(235, 255, 255, 255))

# ---------- the gas bubble ----------
bub = layer(); bb = ImageDraw.Draw(bub)
bb.ellipse([BX - BR, BY - BR, BX + BR, BY + BR], fill=(255, 235, 242, 34))
img.alpha_composite(bub)
# inner rim glow (pinkish refraction ring)
ring = layer(); rr = ImageDraw.Draw(ring)
rr.ellipse([BX - BR, BY - BR, BX + BR, BY + BR], outline=(255, 210, 225, 150), width=26 * S)
img.alpha_composite(ring.filter(ImageFilter.GaussianBlur(14 * S)))
ring2 = layer(); r2 = ImageDraw.Draw(ring2)
r2.ellipse([BX - BR, BY - BR, BX + BR, BY + BR], outline=(255, 245, 250, 235), width=5 * S)
# horizontal scan line across bubble
r2.line([(BX - BR + 10 * S, BY + 40 * S), (BX + BR - 10 * S, BY + 40 * S)], fill=(150, 245, 255, 230), width=5 * S)
img.alpha_composite(ring2)
sl = layer(); ImageDraw.Draw(sl).line([(BX - BR, BY + 40 * S), (BX + BR, BY + 40 * S)], fill=(90, 235, 255, 255), width=24 * S)
mask = Image.new('L', (w, h), 0); ImageDraw.Draw(mask).ellipse([BX - BR, BY - BR, BX + BR, BY + BR], fill=255)
sl2 = layer(); sl2.paste(sl.filter(ImageFilter.GaussianBlur(14 * S)), (0, 0), mask)
img.alpha_composite(sl2)
# specular highlight
hl = layer(); hd = ImageDraw.Draw(hl)
hl_e = Image.new('RGBA', (170 * S, 80 * S), (0, 0, 0, 0))
ImageDraw.Draw(hl_e).ellipse([0, 0, 170 * S - 1, 80 * S - 1], fill=(255, 255, 255, 240))
hl_e = hl_e.rotate(32, expand=True, resample=Image.BICUBIC)
hl.alpha_composite(hl_e, (BX - 170 * S, BY - 165 * S))
hd.ellipse([BX - 42 * S, BY - 200 * S, BX - 20 * S, BY - 178 * S], fill=(255, 255, 255, 220))
img.alpha_composite(hl)
# rim reflection bottom-right
rf = layer(); ImageDraw.Draw(rf).arc([BX - BR + 18 * S, BY - BR + 18 * S, BX + BR - 18 * S, BY + BR - 18 * S], 20, 70, fill=(255, 255, 255, 170), width=5 * S)
img.alpha_composite(rf)
# motion dashes on left (moving toward exit)
md = ImageDraw.Draw(img, 'RGBA')
for dy, ln in ((-120, 70), (-40, 110), (60, 80), (150, 60)):
    x1 = BX - BR - 40 * S
    md.line([(x1 - ln * S, BY + dy * S), (x1, BY + dy * S)], fill=(255, 225, 235, 200), width=5 * S)

# ---------- alert "!" badge above bubble ----------
ax, ay, ar = BX + 175 * S, BY - 215 * S, 50 * S
ab = layer(); a2 = ImageDraw.Draw(ab)
a2.ellipse([ax - ar - 14 * S, ay - ar - 14 * S, ax + ar + 14 * S, ay + ar + 14 * S], fill=(255, 40, 70, 160))
img.alpha_composite(ab.filter(ImageFilter.GaussianBlur(16 * S)))
a3 = ImageDraw.Draw(img, 'RGBA')
a3.ellipse([ax - ar, ay - ar, ax + ar, ay + ar], fill=rgba('#e8213e'), outline=rgba('#ffd5db'), width=4 * S)
fbang = ImageFont.truetype(FX, 74 * S)
a3.text((ax, ay + 2 * S), "!", font=fbang, fill='white', anchor='mm')

# ---------- holographic analysis panel ----------
PX0, PY0, PX1, PY1 = 150 * S, 1650 * S, 930 * S, 1830 * S
pan = layer(); p2 = ImageDraw.Draw(pan)
p2.rounded_rectangle([PX0, PY0, PX1, PY1], 34 * S, fill=(20, 40, 70, 175))
img.alpha_composite(pan)
pg = layer(); ImageDraw.Draw(pg).rounded_rectangle([PX0, PY0, PX1, PY1], 34 * S, outline=(90, 230, 255, 255), width=8 * S)
img.alpha_composite(pg.filter(ImageFilter.GaussianBlur(10 * S)))
p3 = ImageDraw.Draw(img, 'RGBA')
p3.rounded_rectangle([PX0, PY0, PX1, PY1], 34 * S, outline=(170, 245, 255, 255), width=3 * S)
scn = layer(); sc_ = ImageDraw.Draw(scn)
for yy in range(PY0 + 10 * S, PY1 - 10 * S, 9 * S):  # scanlines
    sc_.line([(PX0 + 20 * S, yy), (PX1 - 20 * S, yy)], fill=(120, 220, 255, 30), width=1 * S)
img.alpha_composite(scn)
fl = ImageFont.truetype(FB, 30 * S); fv = ImageFont.truetype(FX, 54 * S)
p3.text(((PX0 + PX1) / 2, PY0 + 40 * S), "ANALIZANDO MUESTRA...", font=fl, fill=(150, 235, 255, 255), anchor='mm')
# left result: GAS + check
cx1, cy = PX0 + 120 * S, PY0 + 118 * S
p3.ellipse([cx1 - 36 * S, cy - 36 * S, cx1 + 36 * S, cy + 36 * S], fill=rgba('#2ed37a'))
p3.line([(cx1 - 16 * S, cy + 2 * S), (cx1 - 4 * S, cy + 15 * S), (cx1 + 18 * S, cy - 14 * S)], fill='white', width=9 * S, joint='curve')
p3.text((cx1 + 56 * S, cy), "GAS", font=fv, fill='white', anchor='lm')
# right result: ¿SÓLIDO? + X (dim)
cx2 = PX0 + 430 * S
p3.ellipse([cx2 - 36 * S, cy - 36 * S, cx2 + 36 * S, cy + 36 * S], fill=(120, 70, 90, 255))
p3.line([(cx2 - 13 * S, cy - 13 * S), (cx2 + 13 * S, cy + 13 * S)], fill=(230, 200, 210, 255), width=8 * S)
p3.line([(cx2 + 13 * S, cy - 13 * S), (cx2 - 13 * S, cy + 13 * S)], fill=(230, 200, 210, 255), width=8 * S)
p3.text((cx2 + 56 * S, cy), "¿SÓLIDO?", font=fv, fill=(190, 160, 175, 255), anchor='lm')

# ---------- caption (reference style) ----------
fc = ImageFont.truetype(FB, 62 * S)
cap = ImageDraw.Draw(img, 'RGBA')
line1 = [("tu", 'dim'), ("recto", 'dim'), ("toma", 'dim'), ("una", 'dim')]
line2 = [("muestra.", 'box')]
def draw_line(words, y):
    sp = 18 * S
    widths = [cap.textlength(t, font=fc) for t, _ in words]
    total = sum(widths) + sp * (len(words) - 1)
    x = (w - total) / 2
    for (t, st), wd in zip(words, widths):
        if st == 'box':
            pad = 12 * S
            sh = layer(); ImageDraw.Draw(sh).text((x + 3 * S, y + 5 * S), t, font=fc, fill=(0, 0, 0, 150), anchor='ls')
            img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6 * S)))
            box = [x - pad, y - 58 * S, x + wd + pad, y + 18 * S]
            bxl = layer(); ImageDraw.Draw(bxl).rectangle(box, fill=(40, 110, 230, 70))
            img.alpha_composite(bxl)
            cap.rectangle(box, outline=rgba('#3d8bff'), width=4 * S)
            for cx, cy2 in ((box[0], box[1]), (box[2], box[1]), (box[0], box[3]), (box[2], box[3])):
                cap.ellipse([cx - 8 * S, cy2 - 8 * S, cx + 8 * S, cy2 + 8 * S], fill='white', outline=rgba('#3d8bff'), width=3 * S)
            cap.text((x, y), t, font=fc, fill='white', anchor='ls')
        else:
            sh = layer(); ImageDraw.Draw(sh).text((x + 3 * S, y + 5 * S), t, font=fc, fill=(0, 0, 0, 120), anchor='ls')
            img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6 * S)))
            tl = layer(); ImageDraw.Draw(tl).text((x, y), t, font=fc, fill=(222, 205, 214, 175), anchor='ls'); img.alpha_composite(tl)
        x += wd + sp
draw_line(line1, 250 * S)
draw_line(line2, 350 * S)

# ---------- finish: downsample, vignette, grain ----------
out = img.convert('RGB').resize((W, H), Image.LANCZOS)
arr = np.asarray(out).astype(np.float32)
yy, xx = np.mgrid[0:H, 0:W]
d = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.47) / (H * 0.62)) ** 2)
arr *= np.clip(1.08 - 0.45 * d ** 2, 0.45, 1.05)[..., None]
arr += np.random.normal(0, 5.5, arr.shape)
out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
out.save(sys.argv[1])
print("ok", out.size)
