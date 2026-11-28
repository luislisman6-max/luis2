"""Personajes para «¿Y si nacieras como Arthur Morgan?».
Estilo del video de referencia: ilustración 2D plana, proporciones realistas (~6.5 cabezas),
contorno café oscuro, colores planos con sombra suave de un lado.
Uso: python3 dibujar_rdr.py   → genera <nombre>.svg y <nombre>.png en esta carpeta."""
import os, json, subprocess

OUT = os.path.dirname(os.path.abspath(__file__))
K = '#1e130d'          # contorno
W, H = 600, 1500       # lienzo de cuerpo entero


def st(fill, w=5):
    return f'fill="{fill}" stroke="{K}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'


def p(d, fill, w=5, extra=''):
    return f'<path d="{d}" {st(fill, w)} {extra}/>'


def ln(d, color=K, w=3, op=1):
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>')


def shade(d, op=.22, color='#000'):
    """sombra plana sin contorno"""
    return f'<path d="{d}" fill="{color}" opacity="{op}"/>'


def svg_wrap(body, w=W, h=H):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'{body}</svg>')


# ---------------------------------------------------------------- ARTHUR
SKIN, SKIN_SH = '#d9a07a', '#b97c58'
HAIR, HAIR_SH = '#8a5a2e', '#5e3b1c'
BEARD = '#6b4523'
SHIRT, SHIRT_SH, STRIPE = '#7d91b0', '#5d6f8e', '#9aaccb'
VEST, VEST_SH = '#4b2f20', '#33200f'
LEATHER, LEATHER_SH = '#9a6434', '#6f4420'
PANTS, PANTS_SH = '#45434a', '#2f2d33'
BOOT, BOOT_SH = '#5a3820', '#3d2513'
HAT, HAT_SH = '#2a211d', '#17110e'
BANDANA = '#2b3352'
BRASS = '#d1a646'


def arthur():
    g = []
    # ---------- piernas (muslo ancho, rodilla, se estrecha al tobillo)
    g.append(p('M198,744 Q186,880 194,1010 L204,1236 L284,1236 L292,1010 Q300,900 302,800 Z', PANTS))
    g.append(p('M402,744 Q414,880 406,1010 L396,1236 L316,1236 L308,1010 Q300,900 298,800 Z', PANTS))
    g.append(p('M196,744 L404,744 L402,800 Q300,830 198,800 Z', PANTS, 0))
    g.append(ln('M300,760 L300,812', K, 3))
    g.append(shade('M262,800 Q276,900 272,1010 L278,1232 L284,1232 L292,1010 Q300,900 302,800 Z', .28))
    g.append(shade('M366,760 Q404,880 398,1010 L390,1232 L370,1232 L376,1010 Q384,880 366,760 Z', .28))
    g.append(ln('M236,1004 Q250,1014 266,1004', K, 2.5, .55))
    g.append(ln('M334,1004 Q350,1014 364,1004', K, 2.5, .55))
    g.append(ln('M300,800 L300,760', K, 2.5, .6))
    # ---------- botas
    g.append(p('M202,1214 L200,1300 Q198,1326 224,1328 L298,1328 Q306,1312 290,1300 L288,1214 Z', BOOT))
    g.append(p('M312,1214 L310,1300 Q294,1312 302,1328 L376,1328 Q402,1326 400,1300 L398,1214 Z', BOOT))
    g.append(shade('M258,1222 L286,1222 L288,1300 L262,1314 Z', .3))
    g.append(shade('M366,1222 L396,1222 L398,1300 L370,1314 Z', .3))
    g.append(ln('M202,1236 L288,1236', K, 4))
    g.append(ln('M312,1236 L398,1236', K, 4))
    g.append(ln('M200,1292 L184,1298', '#b9b2a6', 4))
    g.append('<circle cx="180" cy="1299" r="7" fill="none" stroke="#b9b2a6" stroke-width="3"/>')
    g.append(ln('M400,1292 L416,1298', '#b9b2a6', 4))
    g.append('<circle cx="420" cy="1299" r="7" fill="none" stroke="#b9b2a6" stroke-width="3"/>')

    # ---------- brazos (deltoide redondo, codo, antebrazo)
    def arm(s):
        X = lambda x: 300 + s * (x - 300)
        d = (f'M{X(212)},404 Q{X(150)},404 {X(140)},470 L{X(130)},600 L{X(128)},736 '
             f'L{X(180)},736 L{X(184)},604 L{X(198)},500 Z')
        out = [p(d, SHIRT)]
        out.append(shade(f'M{X(150)},440 L{X(140)},600 L{X(138)},732 L{X(152)},732 L{X(156)},600 L{X(166)},470 Z',
                         .22))
        for k in (0, 1, 2):
            out.append(ln(f'M{X(176-k*12)},430 L{X(160-k*10)},600 L{X(166-k*10)},728', STRIPE, 2, .7))
        out.append(ln(f'M{X(136)},600 Q{X(158)},612 {X(182)},604', SHIRT_SH, 3, .9))   # pliegue del codo
        out.append(p(f'M{X(126)},708 L{X(182)},708 L{X(182)},738 L{X(126)},738 Z', SHIRT_SH, 4))  # puño
        # mano con pulgar
        out.append(p(f'M{X(130)},736 Q{X(122)},790 {X(138)},816 Q{X(156)},832 {X(174)},818 '
                     f'Q{X(186)},796 {X(182)},736 Z', SKIN))
        out.append(p(f'M{X(174)},752 Q{X(188)},770 {X(180)},790 Q{X(172)},782 {X(170)},768 Z', SKIN, 3))
        out.append(ln(f'M{X(142)},784 L{X(144)},812 M{X(154)},786 L{X(156)},818 M{X(166)},784 L{X(166)},810',
                      SKIN_SH, 2.5))
        return ''.join(out)
    g.append(arm(-1)); g.append(arm(1))

    # ---------- torso: camisa (hombros anchos)
    g.append(p('M196,420 Q206,402 256,398 Q300,392 344,398 Q394,402 404,420 L408,744 L192,744 Z', SHIRT))
    # ---------- chaleco
    g.append(p('M194,428 Q214,404 262,400 L282,470 L296,744 L196,746 Q186,600 194,428 Z', VEST))
    g.append(p('M406,428 Q386,404 338,400 L318,470 L304,744 L404,746 Q414,600 406,428 Z', VEST))
    g.append(shade('M356,410 L404,430 Q412,600 402,742 L352,742 Z', .25))
    for y in (530, 590, 650):
        g.append(f'<circle cx="309" cy="{y}" r="5" fill="{BRASS}" stroke="{K}" stroke-width="2"/>')
    g.append(ln('M334,570 L376,570', K, 3))
    g.append(p('M354,540 L360,540 L360,572 L354,572 Z', '#e8c768', 2))
    g.append(p('M354,540 L357,530 L360,540 Z', '#3a2a20', 2))
    g.append(ln('M210,480 Q212,610 208,730', '#6b4a35', 2, .8))
    g.append(ln('M390,480 Q388,610 392,730', '#6b4a35', 2, .8))

    # ---------- correa cruzada
    g.append(p('M200,416 L232,408 L404,724 L376,738 Z', LEATHER, 4))
    g.append(ln('M215,418 L390,730', '#c78d55', 1.8, .9).replace('fill="none"', 'fill="none" stroke-dasharray="7 6"'))
    g.append(p('M290,552 L320,542 L330,570 L300,580 Z', BRASS, 3))
    g.append(p('M298,556 L316,550 L322,566 L304,572 Z', LEATHER_SH, 2))

    # ---------- cinturón + funda + bolsa
    g.append(p('M190,712 L410,712 L410,748 L190,748 Z', LEATHER_SH))
    for x in range(210, 286, 15):
        g.append(f'<rect x="{x}" y="720" width="8" height="20" rx="3" fill="{BRASS}" stroke="{K}" stroke-width="1.5"/>')
    g.append(p('M288,712 L324,712 L324,748 L288,748 Z', BRASS))
    g.append(p('M296,720 L316,720 L316,740 L296,740 Z', LEATHER_SH, 3))
    g.append(p('M196,742 L240,742 L246,880 Q230,894 212,882 Z', LEATHER))
    g.append(shade('M224,746 L240,746 L246,878 L230,886 Z', .25))
    g.append(ln('M206,800 L240,800', K, 2.5, .7))
    g.append(p('M200,702 Q206,680 230,684 L240,728 L210,740 Z', '#3a3330', 4))
    g.append(p('M210,724 L240,722 L240,748 L208,750 Z', '#7a7470', 4))
    g.append(p('M344,744 L404,744 Q412,812 398,830 L352,830 Q338,812 344,744 Z', LEATHER))
    g.append(p('M342,744 L406,744 L402,782 Q374,796 346,782 Z', LEATHER_SH, 4))
    g.append(f'<circle cx="374" cy="780" r="5" fill="{BRASS}" stroke="{K}" stroke-width="2"/>')

    # ---------- cuello, cuello de camisa y pañuelo
    g.append(p('M268,340 L268,404 Q300,418 332,404 L332,340 Z', SKIN))
    g.append(shade('M268,350 L332,350 L332,380 Q300,392 268,380 Z', .25, SKIN_SH))
    g.append(p('M258,398 L300,420 L280,452 L246,420 Z', SHIRT_SH, 4))
    g.append(p('M342,398 L300,420 L320,452 L354,420 Z', SHIRT_SH, 4))
    g.append(p('M262,394 Q300,414 338,394 L346,408 Q300,436 254,408 Z', BANDANA, 4))
    g.append(p('M290,440 L270,520 L298,498 Z', BANDANA, 4))
    g.append(p('M310,440 L326,526 L300,500 Z', BANDANA, 4))
    g.append(p('M286,420 Q300,412 314,420 Q318,440 300,446 Q282,440 286,420 Z', BANDANA, 4))

    # ---------- cabeza
    g.append(p('M224,226 Q206,300 222,352 Q240,368 252,348 L254,240 Z', HAIR))
    g.append(p('M376,226 Q394,300 378,352 Q360,368 348,348 L346,240 Z', HAIR))
    g.append(p('M234,268 Q216,262 218,290 Q222,318 240,318 Z', SKIN))
    g.append(p('M366,268 Q384,262 382,290 Q378,318 360,318 Z', SKIN))
    g.append(p('M236,218 Q234,300 244,330 Q262,372 300,376 Q338,372 356,330 Q366,300 364,218 '
               'Q300,196 236,218 Z', SKIN))
    g.append(shade('M330,214 Q366,218 364,240 Q366,300 356,330 Q340,366 312,374 Q340,330 336,260 Z',
                   .35, SKIN_SH))
    g.append(p('M240,292 Q244,330 262,356 Q282,378 300,378 Q318,378 338,356 Q356,330 360,292 '
               'Q352,316 334,322 Q318,312 300,316 Q282,312 266,322 Q248,316 240,292 Z',
               BEARD, 0, 'opacity="0.85"'))
    for (x, y) in [(256, 330), (268, 346), (282, 358), (300, 362), (318, 358), (332, 346), (344, 330),
                   (262, 312), (338, 312), (290, 340), (310, 340)]:
        g.append(ln(f'M{x},{y} l2,6', '#3d2612', 2, .7))
    g.append(p('M272,318 Q286,306 300,312 Q314,306 328,318 Q320,326 300,322 Q280,326 272,318 Z', BEARD, 3))
    g.append(ln('M286,334 Q300,338 314,334', K, 3))
    g.append(ln('M292,344 Q300,346 308,344', '#8a4f3a', 2, .7))
    g.append(ln('M302,252 L298,292 Q296,302 304,304', K, 3))
    g.append(ln('M290,302 Q296,308 302,304', K, 2.5, .8))
    g.append(shade('M302,256 L312,296 L304,304 Z', .25, SKIN_SH))
    for s in (-1, 1):
        x = 300 + s * 32
        g.append(shade(f'M{x-22},256 Q{x},248 {x+22},256 L{x+20},270 Q{x},264 {x-20},270 Z', .3, SKIN_SH))
        g.append(p(f'M{x-16},266 Q{x},258 {x+16},266 Q{x},274 {x-16},266 Z', '#f2ece4', 2.5))
        g.append(f'<circle cx="{x+2*s}" cy="266" r="5.5" fill="#6f8fa8" stroke="{K}" stroke-width="1.5"/>')
        g.append(f'<circle cx="{x+2*s}" cy="266" r="2.4" fill="{K}"/>')
        g.append(f'<circle cx="{x+4*s}" cy="264" r="1.3" fill="#fff"/>')
        g.append(p(f'M{x-22*s},252 Q{x},240 {x+22*s},246 L{x+22*s},252 Q{x},248 {x-20*s},258 Z', HAIR_SH, 2))
        g.append(ln(f'M{x-10},279 Q{x},283 {x+12},279', SKIN_SH, 2, .8))
    g.append(ln('M272,232 Q300,226 328,232', SKIN_SH, 2, .7))
    g.append(ln('M296,248 L294,258 M306,248 L308,258', SKIN_SH, 2, .8))
    # mechones a los lados (por fuera de la cara)
    g.append(p('M238,212 Q220,240 222,290 Q230,270 236,256 Q234,284 240,300 Q244,260 246,226 Z', HAIR))
    g.append(p('M362,212 Q380,240 378,290 Q370,270 364,256 Q366,284 360,300 Q356,260 354,226 Z', HAIR))

    # ---------- sombrero
    g.append(p('M240,212 Q232,150 252,110 Q276,96 300,104 Q324,96 348,110 Q368,150 360,212 Z', HAT))
    g.append(shade('M320,104 Q348,110 356,150 Q364,190 360,212 L330,212 Q336,150 320,104 Z', .35))
    g.append(ln('M272,112 Q300,130 328,112', '#000', 3, .6))
    g.append(p('M240,186 Q300,176 360,186 L360,204 Q300,194 240,204 Z', '#4a3a2e', 3))
    for x in range(250, 352, 12):
        g.append(ln(f'M{x},188 l6,12', '#8a7560', 1.5, .8))
    g.append(f'<circle cx="262" cy="194" r="7" fill="#c9bfae" stroke="{K}" stroke-width="2"/>')
    g.append(p('M136,212 Q150,196 200,198 Q300,206 400,198 Q450,196 464,212 Q450,232 400,226 '
               'Q300,220 200,226 Q150,232 136,212 Z', HAT))
    g.append(shade('M140,214 Q170,224 200,222 Q300,216 400,222 Q430,224 460,214 Q450,230 400,226 '
                   'Q300,220 200,226 Q150,232 140,214 Z', .45))
    g.append(shade('M238,222 Q300,214 362,222 L364,240 Q300,226 236,240 Z', .25))
    return svg_wrap(''.join(g), W, 1380)


CHARS = {'arthur': arthur}


def render(names):
    for n in names:
        open(os.path.join(OUT, n + '.svg'), 'w').write(CHARS[n]())
    js = """const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();
const p=await b.newPage({deviceScaleFactor:1});
for(const n of %s){await p.setContent('<html><body style="margin:0;background:transparent">'+fs.readFileSync('%s/'+n+'.svg','utf8')+'</body></html>');
await p.locator('svg').screenshot({path:'%s/'+n+'.png',omitBackground:true});console.log('ok',n);}await b.close();})();""" % (
        json.dumps(names), OUT, OUT)
    subprocess.run(['node', '-e', js], check=True)


if __name__ == '__main__':
    render(list(CHARS))
