"""Personajes de la Parte 1 (infancia): bebé Arthur, Beatrice, Lyle, Arthur de 14 años y jinete.
Mismo estilo que dibujar_rdr.py. Los niños (y la mamá) en proporción «chibi» como en el video
de referencia; los hombres adultos en proporción realista.
Uso: python3 chars_p1.py"""
import os
from dibujar_rdr import K, st, p, ln, shade, svg_wrap, render, CHARS, arthur, \
    SKIN, SKIN_SH, HAIR, HAIR_SH, BEARD, PANTS, BOOT, LEATHER, LEATHER_SH, BRASS

CHEEK = '#e98c7a'


def eye_dot(x, y, r=7, iris='#3b2a20'):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{iris}"/>'
            f'<circle cx="{x+r*.35}" cy="{y-r*.35}" r="{r*.32}" fill="#fff"/>')


def closed_smile_eye(x, y, w=16):
    return ln(f'M{x-w},{y+4} Q{x},{y-10} {x+w},{y+4}', K, 5)


# ---------------------------------------------------------------- BEBÉ
def baby_head(cx, cy, r, grumpy=True):
    g = [f'<circle cx="{cx}" cy="{cy}" r="{r}" {st(SKIN, 5)}/>',
         shade(f'M{cx+r*.35},{cy-r*.9} A{r},{r} 0 0 1 {cx+r*.55},{cy+r*.83} Q{cx+r*.75},{cy} {cx+r*.35},{cy-r*.9} Z',
               .25, SKIN_SH)]
    # orejas
    for s in (-1, 1):
        g.append(f'<ellipse cx="{cx+s*r*.98}" cy="{cy+r*.08}" rx="{r*.16}" ry="{r*.22}" {st(SKIN, 4)}/>')
    # rulito de pelo
    g.append(ln(f'M{cx-6},{cy-r+4} Q{cx-18},{cy-r-26} {cx+4},{cy-r-22} Q{cx+16},{cy-r-12} {cx+2},{cy-r-6}',
                HAIR, 6))
    ey = cy + r * .05
    for s in (-1, 1):
        x = cx + s * r * .36
        g.append(eye_dot(x, ey, r * .1))
        if grumpy:   # ceja enojada: el bebé ya tiene carácter
            g.append(ln(f'M{x-s*r*.2},{ey-r*.16} L{x+s*r*.18},{ey-r*.3}', K, 5))
        g.append(f'<ellipse cx="{x+s*r*.08}" cy="{ey+r*.28}" rx="{r*.13}" ry="{r*.08}" fill="{CHEEK}" opacity=".6"/>')
    g.append(ln(f'M{cx-r*.14},{cy+r*.48} Q{cx},{cy+r*.4} {cx+r*.14},{cy+r*.48}', K, 4) if grumpy else
             ln(f'M{cx-r*.14},{cy+r*.42} Q{cx},{cy+r*.56} {cx+r*.14},{cy+r*.42}', K, 4))
    g.append(f'<circle cx="{cx}" cy="{cy+r*.25}" r="{r*.05}" fill="{SKIN_SH}"/>')
    return ''.join(g)


def baby():
    """bebé envuelto en su manta (para la cuna)"""
    g = [p('M70,360 Q40,250 120,210 L280,210 Q360,250 330,360 Q200,400 70,360 Z', '#c9b38a'),
         shade('M230,212 L280,210 Q360,250 330,360 Q290,374 250,380 Q300,300 230,212 Z', .2),
         ln('M110,300 Q200,330 290,300', '#a8915f', 4), ln('M100,340 Q200,370 300,340', '#a8915f', 4)]
    g.append(baby_head(200, 170, 105))
    return svg_wrap(''.join(g), 400, 400)


# ---------------------------------------------------------------- BEATRICE (mamá) con el bebé
DRESS, DRESS_SH = '#6f6386', '#54496a'
APRON = '#e9dfc9'
MOM_HAIR, MOM_HAIR_SH = '#4a2e1c', '#2f1c10'


def beatrice():
    g = []
    cx = 250
    # vestido largo
    g.append(p(f'M170,420 Q150,640 110,940 Q250,975 390,940 Q350,640 330,420 Q250,400 170,420 Z', DRESS))
    g.append(shade('M290,416 Q340,640 388,940 Q350,952 312,958 Q300,640 270,412 Z', .22))
    g.append(p('M196,520 L304,520 Q318,760 330,900 Q250,920 170,900 Q182,760 196,520 Z', APRON, 4))
    g.append(ln('M200,560 Q250,568 300,560', '#cfc3a8', 3))
    # brazos que sostienen al bebé
    for s in (-1, 1):
        x0 = cx + s * 78
        g.append(p(f'M{x0},430 Q{x0+s*40},500 {x0+s*16},590 L{cx+s*10},600 L{cx+s*14},570 L{x0-s*14},540 Z',
                   DRESS, 5))
    # bebé en brazos
    g.append(p('M150,520 Q140,610 250,630 Q360,610 350,520 Q250,500 150,520 Z', '#c9b38a'))
    g.append(baby_head(250, 500, 58, grumpy=False))
    # manos
    for s in (-1, 1):
        g.append(f'<ellipse cx="{cx+s*58}" cy="{604}" rx="24" ry="18" {st(SKIN, 4)}/>')
    # cuello y cuello del vestido
    g.append(p('M228,372 L228,420 Q250,430 272,420 L272,372 Z', SKIN))
    g.append(p('M206,414 Q250,440 294,414 L300,428 Q250,456 200,428 Z', '#ece4d4', 4))
    # cabeza grande
    hy = 240
    g.append(p(f'M150,{hy-30} Q148,{hy+90} 210,{hy+130} Q250,{hy+150} 290,{hy+130} Q352,{hy+90} 350,{hy-30} '
               f'Q250,{hy-110} 150,{hy-30} Z', SKIN))
    g.append(shade(f'M300,{hy-70} Q352,{hy-40} 350,{hy-10} Q352,{hy+90} 290,{hy+130} Q330,{hy+40} 300,{hy-70} Z',
                   .25, SKIN_SH))
    # pelo con raya al medio y moño
    g.append(f'<circle cx="250" cy="{hy-112}" r="46" {st(MOM_HAIR, 5)}/>')
    g.append(ln(f'M222,{hy-130} Q250,{hy-150} 278,{hy-130}', MOM_HAIR_SH, 3))
    g.append(p(f'M146,{hy+10} Q140,{hy-96} 250,{hy-92} Q360,{hy-96} 354,{hy+10} Q340,{hy-30} 300,{hy-50} '
               f'Q270,{hy-60} 250,{hy-40} Q230,{hy-60} 200,{hy-50} Q160,{hy-30} 146,{hy+10} Z', MOM_HAIR))
    g.append(ln(f'M250,{hy-90} L250,{hy-42}', MOM_HAIR_SH, 3))
    # cara dulce: ojos cerrados sonriendo, mejillas
    for s in (-1, 1):
        g.append(closed_smile_eye(250 + s * 46, hy + 30, 18))
        g.append(f'<ellipse cx="{250+s*62}" cy="{hy+66}" rx="18" ry="10" fill="{CHEEK}" opacity=".55"/>')
        g.append(ln(f'M{250+s*30},{hy+4} Q{250+s*46},{hy-6} {250+s*64},{hy+2}', MOM_HAIR_SH, 4))
    g.append(ln(f'M246,{hy+50} Q252,{hy+62} 244,{hy+66}', SKIN_SH, 3))
    g.append(p(f'M228,{hy+84} Q250,{hy+104} 272,{hy+84} Q250,{hy+92} 228,{hy+84} Z', '#9c4a3c', 3))
    return svg_wrap(''.join(g), 500, 1000)


# ---------------------------------------------------------------- LYLE (papá): adulto realista, desaliñado
COAT, COAT_SH = '#5d5640', '#423c2b'
LSHIRT, LSHIRT_SH = '#cbbf9f', '#a89c7c'
LHAT = '#4a3a2c'
LBEARD = '#3a2616'


def lyle():
    g = []
    # piernas y botas gastadas
    g.append(p('M200,744 Q190,880 198,1010 L206,1236 L284,1236 L292,1010 Q300,900 302,800 Z', '#4e4637'))
    g.append(p('M400,744 Q410,880 402,1010 L394,1236 L316,1236 L308,1010 Q300,900 298,800 Z', '#4e4637'))
    g.append(p('M198,744 L402,744 L400,800 Q300,830 200,800 Z', '#4e4637', 0))
    g.append(shade('M366,760 Q404,880 398,1010 L390,1232 L370,1232 L376,1010 Q384,880 366,760 Z', .28))
    g.append(p('M246,940 L276,940 L274,972 L246,970 Z', '#6e6450', 3))                # remiendo
    for x0 in (202, 312):
        g.append(p(f'M{x0},1214 L{x0-2},1300 Q{x0-4},1326 {x0+22},1328 L{x0+96},1328 Q{x0+104},1312 {x0+88},1300 '
                   f'L{x0+86},1214 Z', '#4a3322'))
        g.append(ln(f'M{x0},1236 L{x0+86},1236', K, 4))
    # brazo izquierdo colgando
    g.append(p('M210,410 Q154,410 144,480 L134,610 L132,740 L184,740 L188,610 L200,500 Z', COAT))
    g.append(f'<ellipse cx="158" cy="770" rx="28" ry="36" {st(SKIN, 4)}/>')
    # camisa sucia sin abotonar arriba
    g.append(p('M200,420 Q300,396 400,420 L404,744 L196,744 Z', LSHIRT))
    for (x, y) in [(250, 520), (330, 600), (270, 660)]:
        g.append(f'<ellipse cx="{x}" cy="{y}" rx="16" ry="10" fill="#8d7f5c" opacity=".45"/>')        # manchas
    # tirantes caídos
    g.append(ln('M248,420 Q232,600 240,744', '#5a3a24', 9))
    g.append(ln('M352,420 Q368,600 360,744', '#5a3a24', 9))
    # abrigo largo abierto
    g.append(p('M196,424 Q214,404 256,402 L262,520 L250,880 L170,870 Q178,600 196,424 Z', COAT))
    g.append(p('M404,424 Q386,404 344,402 L338,520 L350,880 L430,870 Q422,600 404,424 Z', COAT))
    g.append(shade('M360,420 L404,430 Q420,600 428,866 L380,874 Z', .25))
    g.append(p('M250,400 L276,440 L262,520 L238,470 Z', COAT_SH, 4))
    g.append(p('M350,400 L324,440 L338,520 L362,470 Z', COAT_SH, 4))
    g.append(p('M196,560 L240,560 L240,600 L196,600 Z', COAT_SH, 3))                    # bolsillo roto
    g.append(ln('M200,600 L212,612', K, 2))
    # brazo derecho con la botella
    g.append(p('M390,410 Q446,414 456,480 L470,600 L452,690 L410,680 L420,600 L400,500 Z', COAT))
    g.append(p('M432,640 L460,640 L462,560 L470,540 L470,520 L450,520 L450,540 L432,560 Z', '#5f7a3a', 4))
    g.append(p('M450,520 L470,520 L470,508 L450,508 Z', '#8a6a46', 3))
    g.append(shade('M436,566 L446,566 L446,630 L436,630 Z', .35, '#fff'))
    g.append(f'<ellipse cx="440" cy="690" rx="30" ry="26" {st(SKIN, 4)}/>')
    # cuello
    g.append(p('M268,340 L268,404 Q300,418 332,404 L332,340 Z', SKIN))
    g.append(p('M270,400 Q300,430 330,400 L300,470 Z', SKIN, 3))
    # cabeza
    g.append(p('M224,226 Q206,300 222,352 Q240,368 252,348 L254,240 Z', '#3a2616'))
    g.append(p('M376,226 Q394,300 378,352 Q360,368 348,348 L346,240 Z', '#3a2616'))
    g.append(p('M234,268 Q216,262 218,290 Q222,318 240,318 Z', SKIN))
    g.append(p('M366,268 Q384,262 382,290 Q378,318 360,318 Z', SKIN))
    g.append(p('M238,218 Q232,300 246,334 Q264,374 300,378 Q336,374 354,334 Q368,300 362,218 Q300,198 238,218 Z',
               SKIN))
    g.append(shade('M330,214 Q366,218 364,240 Q366,300 356,330 Q340,366 312,374 Q340,330 336,260 Z', .35, SKIN_SH))
    # barba descuidada, más larga y oscura
    g.append(p('M238,286 Q236,350 264,382 Q284,400 300,404 Q316,400 336,382 Q364,350 362,286 Q350,316 332,322 '
               'Q318,312 300,316 Q282,312 268,322 Q250,316 238,286 Z', LBEARD, 3))
    for (x, y) in [(256, 340), (276, 370), (300, 388), (324, 370), (344, 340), (290, 350), (312, 352)]:
        g.append(ln(f'M{x},{y} l-2,10', '#5a3d24', 2, .8))
    g.append(p('M272,318 Q286,306 300,312 Q314,306 328,318 Q320,330 300,326 Q280,330 272,318 Z', LBEARD, 3))
    g.append(ln('M288,340 Q300,334 312,340', '#7a3d30', 3))           # boca torcida hacia abajo
    # nariz roja de borracho
    g.append(ln('M302,252 L298,290', K, 3))
    g.append(f'<ellipse cx="300" cy="298" rx="13" ry="10" fill="#c9705a" stroke="{K}" stroke-width="3"/>')
    # ojos caídos, con ojeras, mirada torva
    for s in (-1, 1):
        x = 300 + s * 32
        g.append(p(f'M{x-16},266 Q{x},262 {x+16},266 Q{x},276 {x-16},266 Z', '#efe2c8', 2.5))
        g.append(f'<circle cx="{x}" cy="268" r="5" fill="#3b2a20"/>')
        g.append(p(f'M{x-18},264 Q{x},256 {x+18},264 L{x+18},268 Q{x},262 {x-18},268 Z', SKIN_SH, 2))  # párpado
        g.append(ln(f'M{x-12},280 Q{x},286 {x+12},280', '#9a5c48', 2.5, .9))
        g.append(p(f'M{x-22*s},254 Q{x},250 {x+22*s},242 L{x+22*s},248 Q{x},256 {x-20*s},260 Z', '#2a1a10', 2))
    # pelo grasiento que asoma
    g.append(p('M238,212 Q222,240 224,290 Q232,270 238,256 Q236,284 242,300 Q246,260 248,226 Z', '#3a2616'))
    g.append(p('M362,212 Q378,240 376,290 Q368,270 362,256 Q364,284 358,300 Q354,260 352,226 Z', '#3a2616'))
    # sombrero viejo, abollado y con agujero
    g.append(p('M244,214 Q238,160 256,124 Q262,110 300,118 Q336,108 346,126 Q364,160 356,214 Z', LHAT))
    g.append(ln('M262,140 Q290,150 300,128', '#2a1e14', 3))
    g.append(f'<circle cx="326" cy="160" r="6" fill="#1a120c"/>')
    g.append(p('M160,214 Q170,200 210,202 Q300,208 390,202 Q430,200 440,216 Q428,232 390,228 Q300,222 210,228 '
               'Q170,232 160,214 Z', LHAT))
    g.append(p('M400,204 L440,216 L420,226 Z', '#3a2c20', 2))
    g.append(shade('M238,222 Q300,214 362,222 L364,240 Q300,226 236,240 Z', .3))
    return svg_wrap(''.join(g), 600, 1380)


# ---------------------------------------------------------------- ARTHUR 14 AÑOS (chibi)
TSHIRT, TSHIRT_SH = '#e6dcc5', '#c3b799'
TPANTS = '#5e5040'


def arthur_teen():
    g = []
    cx = 250
    # piernas y botas
    for s in (-1, 1):
        x = cx + s * 34
        g.append(p(f'M{x-28},640 L{x-24},900 L{x+24},900 L{x+28},640 Z', TPANTS))
        g.append(p(f'M{x-30},880 L{x-30},930 Q{x-30},946 {x-12},946 L{x+34*s if s>0 else x+30},946 '
                   f'Q{x+36},930 {x+26},880 Z', '#4a3322'))
    g.append(p('M222,770 L244,770 L244,792 L222,792 Z', '#7a6a52', 3))     # remiendo
    # torso
    g.append(p('M176,450 Q250,428 324,450 L320,660 L180,660 Z', TSHIRT))
    g.append(shade('M282,440 Q324,450 320,660 L290,660 Z', .2))
    g.append(ln('M250,452 L250,560', TSHIRT_SH, 3))
    for y in (480, 520):
        g.append(f'<circle cx="250" cy="{y}" r="4" fill="{TSHIRT_SH}"/>')
    g.append(ln('M210,448 L206,660', '#6a4428', 9))
    g.append(ln('M290,448 L294,660', '#6a4428', 9))
    g.append(p('M178,640 L322,640 L322,664 L178,664 Z', '#6a4428', 4))
    # brazos con mangas arremangadas
    for s in (-1, 1):
        x = cx + s * 76
        g.append(p(f'M{x-s*4},454 Q{x+s*34},470 {x+s*34},540 L{x+s*8},548 Z', TSHIRT))
        g.append(p(f'M{x+s*8},540 L{x+s*34},536 L{x+s*36},640 L{x+s*12},642 Z', SKIN))
        g.append(f'<circle cx="{x+s*24}" cy="652" r="18" {st(SKIN, 4)}/>')
    # cuello
    g.append(p('M232,400 L232,446 Q250,454 268,446 L268,400 Z', SKIN))
    g.append(p('M220,438 L250,456 L280,438 L284,452 L250,470 L216,452 Z', TSHIRT_SH, 3))
    # cabeza
    hy = 270
    g.append(p(f'M150,{hy-20} Q150,{hy+100} 214,{hy+132} Q250,{hy+146} 286,{hy+132} Q350,{hy+100} 350,{hy-20} '
               f'Q250,{hy-100} 150,{hy-20} Z', SKIN))
    g.append(shade(f'M300,{hy-62} Q352,{hy-36} 350,{hy-10} Q350,{hy+100} 286,{hy+132} Q330,{hy+40} 300,{hy-62} Z',
                   .25, SKIN_SH))
    for s in (-1, 1):
        g.append(f'<ellipse cx="{250+s*102}" cy="{hy+24}" rx="16" ry="24" {st(SKIN, 4)}/>')
    # pelo revuelto con mechones
    g.append(p(f'M144,{hy+20} Q130,{hy-110} 250,{hy-112} Q370,{hy-110} 356,{hy+20} Q344,{hy-20} 330,{hy-36} '
               f'L322,{hy-6} L300,{hy-44} L284,{hy-14} L262,{hy-50} L244,{hy-16} L222,{hy-48} L204,{hy-12} '
               f'L186,{hy-40} Q160,{hy-10} 144,{hy+20} Z', HAIR))
    g.append(ln(f'M200,{hy-80} Q230,{hy-96} 262,{hy-88}', HAIR_SH, 3))
    g.append(ln(f'M280,{hy-84} Q310,{hy-90} 330,{hy-70}', HAIR_SH, 3))
    # cara: ceño desafiante, ojos azul grisáceo
    for s in (-1, 1):
        x = 250 + s * 44
        g.append(f'<ellipse cx="{x}" cy="{hy+36}" rx="16" ry="18" {st("#fff", 4)}/>')
        g.append(eye_dot(x + s * 2, hy + 38, 9, '#5f7f99'))
        g.append(f'<circle cx="{x+s*2}" cy="{hy+38}" r="4" fill="{K}"/>')
        g.append(p(f'M{x-s*24},{hy+18} L{x+s*22},{hy+2} L{x+s*22},{hy+9} L{x-s*22},{hy+25} Z', HAIR_SH, 2))
        for dx in (-8, 0, 8):
            g.append(f'<circle cx="{x+s*6+dx}" cy="{hy+70}" r="2.2" fill="#b0704f" opacity=".8"/>')    # pecas
    g.append(ln(f'M252,{hy+50} Q258,{hy+66} 248,{hy+70}', SKIN_SH, 3))
    g.append(ln(f'M232,{hy+94} L268,{hy+92}', K, 4))
    g.append(ln(f'M262,{hy+88} L270,{hy+92}', K, 3))
    g.append(f'<ellipse cx="208" cy="{hy+92}" rx="12" ry="6" fill="#8a6a50" opacity=".35"/>')     # mugre
    return svg_wrap(''.join(g), 500, 960)


# ---------------------------------------------------------------- JINETE (silueta a caballo)
def jinete():
    C = '#1a0f14'
    leg = lambda d, w=16: f'<path d="{d}" fill="none" stroke="{C}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
    g = [
        # cola
        f'<path d="M160,300 Q110,330 112,420 Q116,470 100,500 Q140,470 150,420 Q156,370 178,330 Z" fill="{C}"/>',
        # patas traseras (muslo grueso, corvejón, caña)
        f'<path d="M170,300 Q150,380 196,420 L188,470 L200,470 L214,400 Q236,370 230,320 Z" fill="{C}"/>',
        leg('M194,468 L186,560 L180,596'), leg('M232,380 L246,470 L232,560 L230,596'),
        # patas delanteras
        leg('M396,370 L404,470 L398,560 L404,596'), leg('M424,366 L446,450 L470,520 L466,560', 15),
        # cascos
        f'<path d="M168,590 h26 v12 h-28 Z M218,590 h26 v12 h-28 Z M392,590 h26 v12 h-28 Z M454,552 h24 v12 h-26 Z" fill="{C}"/>',
        # cuerpo
        f'<ellipse cx="300" cy="330" rx="152" ry="64" fill="{C}"/>',
        # pecho y cuello
        f'<path d="M380,290 Q420,250 446,200 Q458,170 480,160 L512,196 Q478,236 470,280 Q456,340 430,372 L380,380 Z" fill="{C}"/>',
        # cabeza con hocico
        f'<path d="M470,156 Q496,148 516,168 L572,236 Q580,256 562,262 Q546,264 530,250 L494,214 Q470,200 470,156 Z" fill="{C}"/>',
        # orejas y crin
        f'<path d="M478,160 L482,128 L494,154 Z M492,156 L500,126 L506,158 Z" fill="{C}"/>',
        f'<path d="M470,160 Q440,170 426,210 Q412,240 392,262 Q430,236 446,214 Q460,190 478,176 Z" fill="{C}"/>',
        # jinete: pierna, torso, brazo a las riendas, cabeza y sombrero
        f'<path d="M286,300 L318,300 L330,390 L344,420 L312,424 L300,392 Z" fill="{C}"/>',
        f'<path d="M272,306 Q266,250 284,212 Q300,196 322,204 Q340,214 338,256 L330,308 Z" fill="{C}"/>',
        leg('M326,226 L372,262 L430,232', 18),
        f'<circle cx="306" cy="186" r="22" fill="{C}"/>',
        f'<path d="M262,170 Q306,158 352,168 Q346,176 306,176 Q268,178 262,170 Z M286,170 Q286,140 306,138 Q328,140 326,170 Z" fill="{C}"/>',
        f'<path d="M260,168 Q256,160 264,158 L270,168 Z M352,168 Q358,158 350,156 L344,168 Z" fill="{C}"/>',
    ]
    return svg_wrap(''.join(g), 640, 620)


CHARS.update({'baby': baby, 'beatrice': beatrice, 'lyle': lyle, 'arthur_teen': arthur_teen, 'jinete': jinete})

if __name__ == '__main__':
    render(['baby', 'beatrice', 'lyle', 'arthur_teen', 'jinete'])
