"""Generador de personajes (partes 2-5) en el mismo estilo que Arthur:
hombres adultos en proporción realista; mujeres y niños en proporción «chibi» como Beatrice y Arthur de 14.
Uso: python3 chars_gen.py"""
from dibujar_rdr import K, st, p, ln, shade, svg_wrap, render, CHARS, BRASS, LEATHER, LEATHER_SH
from chars_p1 import eye_dot, closed_smile_eye, CHEEK, baby_head

SK = {'light': ('#e3b08c', '#c48d68'), 'mid': ('#d9a07a', '#b97c58'), 'pale': ('#dcc6ac', '#b9a080'),
      'tan': ('#c98e66', '#a66f4c'), 'dark': ('#9c6644', '#7a4c30')}


# ============================================================ HOMBRE ADULTO
def man(c):
    skin, skin_sh = SK[c.get('skin', 'mid')]
    hair, hair_sh = c.get('hair', ('#3a2616', '#24170c'))
    wf = c.get('wf', 1.0)                    # complexión: <1 delgado, >1 robusto
    g, body = [], []
    pants, boots = c.get('pants', '#45434a'), c.get('boots', '#4a3322')
    shirt, shirt_sh = c.get('shirt', ('#e9e2d0', '#c9c0aa'))
    outer = c.get('outer')                    # ('vest'|'coat'|'suit', color)
    sleeve = outer[1] if outer and outer[0] in ('coat', 'suit') else shirt
    # ---- piernas
    body.append(p('M198,744 Q186,880 194,1010 L204,1236 L284,1236 L292,1010 Q300,900 302,800 Z', pants))
    body.append(p('M402,744 Q414,880 406,1010 L396,1236 L316,1236 L308,1010 Q300,900 298,800 Z', pants))
    body.append(p('M196,744 L404,744 L402,800 Q300,830 198,800 Z', pants, 0))
    body.append(shade('M366,760 Q404,880 398,1010 L390,1232 L370,1232 L376,1010 Q384,880 366,760 Z', .28))
    body.append(ln('M300,760 L300,812', K, 3))
    for x0 in (202, 312):
        body.append(p(f'M{x0},1214 L{x0-2},1300 Q{x0-4},1326 {x0+22},1328 L{x0+96},1328 Q{x0+104},1312 {x0+88},1300 '
                      f'L{x0+86},1214 Z', boots))
        body.append(ln(f'M{x0},1236 L{x0+86},1236', K, 4))
    # ---- brazos
    for s in (-1, 1):
        X = lambda x: 300 + s * (x - 300)
        body.append(p(f'M{X(212)},404 Q{X(150)},404 {X(140)},470 L{X(130)},600 L{X(128)},736 L{X(180)},736 '
                      f'L{X(184)},604 L{X(198)},500 Z', sleeve))
        body.append(shade(f'M{X(150)},440 L{X(140)},600 L{X(138)},732 L{X(152)},732 L{X(156)},600 L{X(166)},470 Z', .2))
        body.append(ln(f'M{X(136)},600 Q{X(158)},612 {X(182)},604', K, 2.5, .5))
        body.append(p(f'M{X(130)},736 Q{X(122)},790 {X(138)},816 Q{X(156)},832 {X(174)},818 Q{X(186)},796 {X(182)},736 Z', skin))
        body.append(ln(f'M{X(144)},786 L{X(146)},812 M{X(158)},788 L{X(160)},818', skin_sh, 2.5))
    # ---- torso
    body.append(p('M196,420 Q206,402 256,398 Q300,392 344,398 Q394,402 404,420 L408,744 L192,744 Z', shirt))
    if c.get('stripes'):
        for x in range(214, 400, 22): body.append(ln(f'M{x},420 L{x},740', shirt_sh, 2, .6))
    if outer:
        kind, col = outer[0], outer[1]; col_sh = outer[2] if len(outer) > 2 else '#00000040'
        if kind == 'vest':
            body.append(p('M194,428 Q214,404 262,400 L282,470 L296,744 L196,746 Q186,600 194,428 Z', col))
            body.append(p('M406,428 Q386,404 338,400 L318,470 L304,744 L404,746 Q414,600 406,428 Z', col))
            body.append(shade('M356,410 L404,430 Q412,600 402,742 L352,742 Z', .25))
            for y in (530, 590, 650): body.append(f'<circle cx="309" cy="{y}" r="5" fill="{BRASS}" stroke="{K}" stroke-width="2"/>')
            if c.get('watch'): body.append(ln('M240,600 Q270,640 306,620', BRASS, 4))
        elif kind == 'suit':
            body.append(p('M194,428 Q214,404 262,400 L300,560 L300,760 L194,760 Q186,600 194,428 Z', col))
            body.append(p('M406,428 Q386,404 338,400 L300,560 L300,760 L406,760 Q414,600 406,428 Z', col))
            body.append(p('M262,400 L300,560 L250,480 L236,410 Z', col_sh, 3))
            body.append(p('M338,400 L300,560 L350,480 L364,410 Z', col_sh, 3))
            body.append(shade('M356,410 L404,430 Q414,600 406,758 L352,758 Z', .22))
            for y in (600, 680): body.append(f'<circle cx="300" cy="{y}" r="6" fill="{K}"/>')
        elif kind == 'coat':
            body.append(p('M196,424 Q214,404 256,402 L262,520 L250,890 L168,880 Q178,600 196,424 Z', col))
            body.append(p('M404,424 Q386,404 344,402 L338,520 L350,890 L432,880 Q422,600 404,424 Z', col))
            body.append(p('M250,400 L276,440 L262,520 L238,470 Z', col_sh, 4))
            body.append(p('M350,400 L324,440 L338,520 L362,470 Z', col_sh, 4))
            body.append(shade('M360,420 L404,430 Q420,600 430,876 L380,884 Z', .25))
    if c.get('suspenders'):
        body.append(ln('M248,420 Q240,600 244,744', c['suspenders'], 9)); body.append(ln('M352,420 Q360,600 356,744', c['suspenders'], 9))
    if c.get('belt', True) and not (outer and outer[0] == 'suit'):
        body.append(p('M190,712 L410,712 L410,748 L190,748 Z', LEATHER_SH))
        body.append(p('M288,712 L324,712 L324,748 L288,748 Z', BRASS))
    if c.get('gun'):
        body.append(p('M196,742 L240,742 L246,880 Q230,894 212,882 Z', LEATHER))
        body.append(p('M200,702 Q206,680 230,684 L240,728 L210,740 Z', '#3a3330', 4))
    if c.get('gun2'):
        body.append(p('M404,742 L360,742 L354,880 Q370,894 388,882 Z', LEATHER))
        body.append(p('M400,702 Q394,680 370,684 L360,728 L390,740 Z', '#d8d0c0', 4))
    # ---- cuello y prenda del cuello
    body.append(p('M268,340 L268,404 Q300,418 332,404 L332,340 Z', skin))
    body.append(shade('M268,350 L332,350 L332,380 Q300,392 268,380 Z', .25, skin_sh))
    body.append(p('M258,398 L300,420 L280,452 L246,420 Z', shirt_sh, 4))
    body.append(p('M342,398 L300,420 L320,452 L354,420 Z', shirt_sh, 4))
    nk = c.get('neck')
    if nk:
        kind, col = nk
        if kind == 'bandana':
            body.append(p('M262,394 Q300,414 338,394 L346,408 Q300,436 254,408 Z', col, 4))
            body.append(p('M290,440 L270,520 L298,498 Z', col, 4)); body.append(p('M310,440 L326,526 L300,500 Z', col, 4))
            body.append(p('M286,420 Q300,412 314,420 Q318,440 300,446 Q282,440 286,420 Z', col, 4))
        elif kind == 'tie':
            body.append(p('M288,420 L312,420 L306,440 L318,560 L300,584 L282,560 L294,440 Z', col, 4))
        elif kind == 'bowtie':
            body.append(p('M300,424 L266,408 L266,444 Z', col, 4)); body.append(p('M300,424 L334,408 L334,444 Z', col, 4))
            body.append(f'<circle cx="300" cy="426" r="8" fill="{col}" stroke="{K}" stroke-width="3"/>')
        elif kind == 'cravat':
            body.append(p('M276,410 Q300,440 324,410 L330,470 Q300,500 270,470 Z', col, 4))
    if wf != 1.0:
        g.append(f'<g transform="translate(300,0) scale({wf},1) translate(-300,0)">{"".join(body)}</g>')
    else:
        g.extend(body)

    # ---- cabeza
    hs = c.get('hairstyle', 'neck')
    if hs == 'long':
        g.append(p('M222,226 Q196,330 214,400 Q240,420 256,380 L254,240 Z', hair))
        g.append(p('M378,226 Q404,330 386,400 Q360,420 344,380 L346,240 Z', hair))
    elif hs in ('neck', 'slick'):
        g.append(p('M224,226 Q206,300 222,352 Q240,368 252,348 L254,240 Z', hair))
        g.append(p('M376,226 Q394,300 378,352 Q360,368 348,348 L346,240 Z', hair))
    g.append(p('M234,268 Q216,262 218,290 Q222,318 240,318 Z', skin))
    g.append(p('M366,268 Q384,262 382,290 Q378,318 360,318 Z', skin))
    jaw = c.get('jaw', 'square')
    face = ('M236,218 Q234,300 244,330 Q262,372 300,376 Q338,372 356,330 Q366,300 364,218 Q300,196 236,218 Z' if jaw == 'square'
            else 'M240,214 Q236,300 250,336 Q270,380 300,382 Q330,380 350,336 Q364,300 360,214 Q300,190 240,214 Z')
    g.append(p(face, skin))
    g.append(shade('M330,214 Q366,218 364,240 Q366,300 356,330 Q340,366 312,374 Q340,330 336,260 Z', .32, skin_sh))
    if c.get('hollow'):     # mejillas hundidas (enfermo)
        g.append(shade('M250,300 Q258,330 270,334 Q262,312 258,296 Z', .4, skin_sh))
        g.append(shade('M350,300 Q342,330 330,334 Q338,312 342,296 Z', .4, skin_sh))
    # ---- vello facial
    beard = c.get('beard')
    bcol = c.get('bcol', hair[0])
    if beard in ('stubble', 'full'):
        d = ('M240,292 Q244,330 262,356 Q282,378 300,378 Q318,378 338,356 Q356,330 360,292 Q352,316 334,322 Q318,312 300,316 '
             'Q282,312 266,322 Q248,316 240,292 Z' if beard == 'stubble' else
             'M238,286 Q236,350 264,384 Q284,404 300,408 Q316,404 336,384 Q364,350 362,286 Q350,316 332,322 Q318,312 300,316 '
             'Q282,312 268,322 Q250,316 238,286 Z')
        g.append(p(d, bcol, 0 if beard == 'stubble' else 3, 'opacity="0.8"' if beard == 'stubble' else ''))
        for (x, y) in [(258, 332), (272, 350), (300, 362), (328, 350), (342, 332), (288, 342), (312, 342)]:
            g.append(ln(f'M{x},{y} l2,6', '#00000060', 2))
    if beard == 'chops':    # patillas largas (Sr. Linton)
        g.append(p('M238,250 L248,250 Q252,320 282,346 Q256,350 240,320 Z', bcol, 3))
        g.append(p('M362,250 L352,250 Q348,320 318,346 Q344,350 360,320 Z', bcol, 3))
    if beard == 'goatee':
        g.append(p('M286,340 Q300,350 314,340 L312,372 Q300,384 288,372 Z', bcol, 3))
    if beard == 'gray':
        g.append(p('M240,290 Q240,350 266,378 Q284,396 300,398 Q316,396 334,378 Q360,350 360,290 Q348,318 332,322 Q318,314 300,318 '
                   'Q282,314 268,322 Q252,318 240,290 Z', bcol, 3))
    mst = c.get('mustache')
    if mst == 'thick':      # bigote grueso de Dutch
        g.append(p('M262,322 Q280,300 300,312 Q320,300 338,322 Q346,336 334,334 Q318,322 300,326 Q282,322 266,334 Q254,336 262,322 Z', bcol, 3))
    elif mst == 'thin':
        g.append(p('M274,318 Q288,310 300,314 Q312,310 326,318 Q314,324 300,322 Q286,324 274,318 Z', bcol, 3))
    elif mst == 'droop':    # bigote caído de Micah
        g.append(p('M272,316 Q300,302 328,316 L334,350 L326,350 L320,324 Q300,318 280,324 L274,350 L266,350 Z', bcol, 3))
    # ---- boca
    mouth = c.get('mouth', 'flat')
    if mouth == 'flat': g.append(ln('M286,338 Q300,342 314,338', K, 3))
    elif mouth == 'smile': g.append(ln('M282,334 Q300,350 318,334', K, 3.5))
    elif mouth == 'smirk': g.append(ln('M284,340 Q304,344 320,330', K, 3.5))
    elif mouth == 'frown': g.append(ln('M286,342 Q300,334 314,342', K, 3))
    elif mouth == 'open': g.append(p('M286,334 Q300,330 314,334 Q312,352 300,354 Q288,352 286,334 Z', '#5a1e1e', 3))
    # ---- nariz
    g.append(ln('M302,252 L298,292 Q296,302 304,304', K, 3)); g.append(ln('M290,302 Q296,308 302,304', K, 2.5, .8))
    # ---- ojos
    eyes = c.get('eyes', 'hard'); iris = c.get('iris', '#4a3a2a'); brow = c.get('brow', hair_sh)
    for s in (-1, 1):
        x = 300 + s * 32
        if eyes == 'sly':
            g.append(p(f'M{x-16},268 Q{x},262 {x+16},266 Q{x},274 {x-16},268 Z', '#f2ece4', 2.5))
            g.append(f'<circle cx="{x+5*s}" cy="268" r="4.5" fill="{iris}"/>')
            g.append(p(f'M{x-24*s},252 Q{x},250 {x+24*s},244 L{x+22*s},252 Q{x},258 {x-20*s},260 Z', brow, 2))
        elif eyes == 'kind':
            g.append(ln(f'M{x-14},268 Q{x},258 {x+14},268', K, 4))
            g.append(p(f'M{x-20*s},250 Q{x},240 {x+22*s},248 L{x+20*s},252 Q{x},246 {x-18*s},256 Z', brow, 2))
            g.append(ln(f'M{x+s*18},272 l{s*8},6 M{x+s*16},278 l{s*8},8', skin_sh, 2))
        elif eyes == 'tired':
            g.append(p(f'M{x-16},266 Q{x},262 {x+16},266 Q{x},276 {x-16},266 Z', '#ece0cc', 2.5))
            g.append(f'<circle cx="{x}" cy="269" r="5" fill="{iris}"/>')
            g.append(p(f'M{x-18},264 Q{x},256 {x+18},264 L{x+18},268 Q{x},262 {x-18},268 Z', skin_sh, 2))
            g.append(ln(f'M{x-14},282 Q{x},290 {x+14},282', '#8a5a6a', 3, .8))
            g.append(p(f'M{x-22*s},248 Q{x},246 {x+22*s},254 L{x+20*s},258 Q{x},252 {x-20*s},254 Z', brow, 2))
        elif eyes == 'wide':
            g.append(f'<ellipse cx="{x}" cy="266" rx="14" ry="12" {st("#f8f4ec", 2.5)}/>')
            g.append(f'<circle cx="{x}" cy="266" r="6" fill="{iris}"/><circle cx="{x+2}" cy="264" r="2" fill="#fff"/>')
            g.append(p(f'M{x-22*s},244 Q{x},234 {x+22*s},242 L{x+20*s},248 Q{x},240 {x-20*s},250 Z', brow, 2))
        else:   # hard
            g.append(shade(f'M{x-22},256 Q{x},248 {x+22},256 L{x+20},270 Q{x},264 {x-20},270 Z', .3, skin_sh))
            g.append(p(f'M{x-16},266 Q{x},258 {x+16},266 Q{x},274 {x-16},266 Z', '#f2ece4', 2.5))
            g.append(f'<circle cx="{x+2*s}" cy="266" r="5.5" fill="{iris}" stroke="{K}" stroke-width="1.5"/>')
            g.append(f'<circle cx="{x+2*s}" cy="266" r="2.4" fill="{K}"/>')
            g.append(p(f'M{x-22*s},252 Q{x},240 {x+22*s},246 L{x+22*s},252 Q{x},248 {x-20*s},258 Z', brow, 2))
    if c.get('wrinkles'):
        g.append(ln('M270,230 Q300,224 330,230 M276,240 Q300,236 324,240', skin_sh, 2, .7))
        g.append(ln('M254,300 Q260,322 272,330 M346,300 Q340,322 328,330', skin_sh, 2, .7))
    if c.get('scars'):      # cicatrices de John (lobos)
        for dx in (0, 12, 24):
            g.append(ln(f'M{236+dx},284 L{250+dx},336', '#b56a5a', 3.5))
        g.append(ln('M326,300 L350,322', '#b56a5a', 3.5))
    if c.get('glasses'):
        for s in (-1, 1): g.append(f'<circle cx="{300+s*32}" cy="266" r="21" fill="#ffffff22" stroke="{K}" stroke-width="3.5"/>')
        g.append(ln('M311,266 Q300,260 289,266', K, 3))
    # ---- pelo delantero
    if hs in ('neck', 'long'):
        g.append(p('M238,212 Q220,240 222,290 Q230,270 236,256 Q234,284 240,300 Q244,260 246,226 Z', hair))
        g.append(p('M362,212 Q380,240 378,290 Q370,270 364,256 Q366,284 360,300 Q356,260 354,226 Z', hair))
    if not c.get('hat'):
        if hs == 'slick':   # peinado hacia atrás con raya (Dutch)
            g.append(p('M234,250 Q226,180 270,166 Q300,156 330,166 Q374,180 366,250 Q360,214 330,204 Q300,196 270,204 Q240,214 234,250 Z', hair))
            g.append(ln('M262,178 Q300,170 336,186', hair_sh, 3)); g.append(ln('M250,200 Q290,186 340,200', hair_sh, 3))
        elif hs == 'bald':
            g.append(p('M236,262 Q230,232 240,222 L246,262 Z', hair)); g.append(p('M364,262 Q370,232 360,222 L354,262 Z', hair))
            g.append(ln('M262,214 Q300,206 338,214', skin_sh, 2, .6))
        elif hs == 'short':
            g.append(p('M236,250 Q228,190 270,176 Q300,168 330,176 Q372,190 364,250 Q352,214 300,210 Q248,214 236,250 Z', hair))
        elif hs in ('neck', 'long'):
            g.append(p('M236,236 Q228,186 270,174 Q300,166 330,174 Q372,186 364,236 Q340,206 300,214 Q262,206 236,236 Z', hair))
    # ---- sombrero
    hat = c.get('hat')
    if hat:
        kind, col = hat
        if kind == 'cowboy':
            g.append(p('M240,212 Q232,150 252,110 Q276,96 300,104 Q324,96 348,110 Q368,150 360,212 Z', col))
            g.append(shade('M320,104 Q348,110 356,150 Q364,190 360,212 L330,212 Q336,150 320,104 Z', .3))
            g.append(ln('M272,112 Q300,130 328,112', '#00000080', 3))
            g.append(p('M240,186 Q300,176 360,186 L360,204 Q300,194 240,204 Z', c.get('band', '#4a3a2e'), 3))
            g.append(p('M136,212 Q150,196 200,198 Q300,206 400,198 Q450,196 464,212 Q450,232 400,226 Q300,220 200,226 Q150,232 136,212 Z', col))
            g.append(shade('M140,214 Q170,224 200,222 Q300,216 400,222 Q430,224 460,214 Q450,230 400,226 Q300,220 200,226 Q150,232 140,214 Z', .4))
        elif kind == 'flat':   # copa plana (Hosea)
            g.append(p('M244,212 L252,140 Q300,130 348,140 L356,212 Z', col))
            g.append(p('M244,186 L356,186 L356,206 L244,206 Z', c.get('band', '#2a1e14'), 3))
            g.append(p('M170,212 Q300,198 430,212 Q440,226 420,228 Q300,218 180,228 Q160,226 170,212 Z', col))
        elif kind == 'bowler':
            g.append(p('M246,212 Q240,120 300,116 Q360,120 354,212 Z', col))
            g.append(p('M246,190 L354,190 L354,206 L246,206 Z', '#1a1410', 3))
            g.append(p('M216,212 Q300,200 384,212 Q392,224 376,226 Q300,216 224,226 Q208,224 216,212 Z', col))
        g.append(shade('M238,222 Q300,214 362,222 L364,240 Q300,226 236,240 Z', .25))
    return svg_wrap(''.join(g), 600, 1380)


# ============================================================ MUJER (estilo Beatrice)
def woman(c):
    skin, skin_sh = SK[c.get('skin', 'light')]
    hair, hair_sh = c.get('hair', ('#4a2e1c', '#2f1c10'))
    dress, dress_sh = c.get('dress', ('#6f6386', '#54496a'))
    g = []
    g.append(p('M170,420 Q150,640 110,940 Q250,975 390,940 Q350,640 330,420 Q250,400 170,420 Z', dress))
    g.append(shade('M290,416 Q340,640 388,940 Q350,952 312,958 Q300,640 270,412 Z', .22))
    if c.get('apron'):
        g.append(p('M196,520 L304,520 Q318,760 330,900 Q250,920 170,900 Q182,760 196,520 Z', c['apron'], 4))
    if c.get('sash'): g.append(p('M178,500 Q250,516 322,500 L324,530 Q250,546 176,530 Z', c['sash'], 4))
    if c.get('buttons'):
        for y in (450, 490, 530): g.append(f'<circle cx="250" cy="{y}" r="6" fill="{c["buttons"]}" stroke="{K}" stroke-width="2"/>')
    # brazos: manos juntas a la cintura
    for s in (-1, 1):
        g.append(p(f'M{250+s*76},428 Q{250+s*112},520 {250+s*60},600 L{250+s*30},590 Q{250+s*70},520 {250+s*56},450 Z', dress))
    g.append(f'<ellipse cx="250" cy="596" rx="40" ry="22" {st(skin, 4)}/>')
    if c.get('holds') == 'book':
        g.append(p('M210,560 L290,560 L290,610 L210,610 Z', '#2a1a10', 4)); g.append(ln('M250,566 L250,604 M236,580 L264,580', '#d1a646', 4))
    g.append(p('M228,372 L228,420 Q250,430 272,420 L272,372 Z', skin))
    g.append(p('M206,414 Q250,440 294,414 L300,428 Q250,456 200,428 Z', c.get('collar', '#ece4d4'), 4))
    hy = 240
    nun = c.get('nun')
    if nun:   # hábito de monja: toca blanca y velo negro
        g.append(p(f'M120,{hy+10} Q120,{hy-130} 250,{hy-134} Q380,{hy-130} 380,{hy+10} L400,{hy+220} Q250,{hy+250} 100,{hy+220} Z', '#16141a'))
    if c.get('hairstyle') == 'loose' and not nun:
        g.append(p(f'M146,{hy-20} Q120,{hy+120} 150,{hy+200} Q180,{hy+220} 200,{hy+150} L300,{hy+150} Q320,{hy+220} 350,{hy+200} '
                   f'Q380,{hy+120} 354,{hy-20} Z', hair))
    g.append(p(f'M150,{hy-30} Q148,{hy+90} 210,{hy+130} Q250,{hy+150} 290,{hy+130} Q352,{hy+90} 350,{hy-30} Q250,{hy-110} 150,{hy-30} Z', skin))
    g.append(shade(f'M300,{hy-70} Q352,{hy-40} 350,{hy-10} Q352,{hy+90} 290,{hy+130} Q330,{hy+40} 300,{hy-70} Z', .25, skin_sh))
    if nun:
        g.append(p(f'M150,{hy-20} Q150,{hy-90} 250,{hy-94} Q350,{hy-90} 350,{hy-20} L352,{hy+20} Q350,{hy-50} 250,{hy-56} '
                   f'Q150,{hy-50} 148,{hy+20} Z', '#f4f1ea', 4))
        g.append(p(f'M190,{hy+120} Q250,{hy+150} 310,{hy+120} L330,{hy+180} Q250,{hy+200} 170,{hy+180} Z', '#f4f1ea', 4))
    else:
        style = c.get('hairstyle', 'bun')
        if style in ('bun', 'updo'):
            r = 46 if style == 'bun' else 60
            g.append(f'<circle cx="250" cy="{hy-112}" r="{r}" {st(hair, 5)}/>')
        g.append(p(f'M146,{hy+10} Q140,{hy-96} 250,{hy-92} Q360,{hy-96} 354,{hy+10} Q340,{hy-30} 300,{hy-50} Q270,{hy-60} 250,{hy-40} '
                   f'Q230,{hy-60} 200,{hy-50} Q160,{hy-30} 146,{hy+10} Z', hair))
        g.append(ln(f'M250,{hy-90} L250,{hy-42}', hair_sh, 3))
        if style == 'updo':
            for s in (-1, 1): g.append(ln(f'M{250+s*96},{hy-10} Q{250+s*110},{hy+40} {250+s*98},{hy+70}', hair, 8))
        if c.get('flower'): g.append(f'<circle cx="322" cy="{hy-110}" r="16" fill="{c["flower"]}" stroke="{K}" stroke-width="3"/>')
    face = c.get('face', 'smile')
    for s in (-1, 1):
        x = 250 + s * 46
        if face == 'smile': g.append(closed_smile_eye(x, hy + 30, 18))
        elif face == 'sad':
            g.append(eye_dot(x, hy + 34, 9)); g.append(ln(f'M{x-s*20},{hy+4} L{x+s*18},{hy+12}', hair_sh, 4))
            if s == 1: g.append(f'<path d="M{x+6},{hy+48} q6,14 0,22 q-6,-8 0,-22 Z" fill="#8fc6ea"/>')
        else:
            g.append(eye_dot(x, hy + 34, 9)); g.append(ln(f'M{x-s*20},{hy+10} Q{x},{hy} {x+s*22},{hy+8}', hair_sh, 4))
        g.append(f'<ellipse cx="{250+s*62}" cy="{hy+66}" rx="18" ry="10" fill="{CHEEK}" opacity=".5"/>')
    g.append(ln(f'M246,{hy+50} Q252,{hy+62} 244,{hy+66}', skin_sh, 3))
    if face == 'sad': g.append(ln(f'M232,{hy+96} Q250,{hy+86} 268,{hy+96}', K, 4))
    elif face == 'calm': g.append(ln(f'M232,{hy+90} Q250,{hy+100} 268,{hy+90}', K, 4))
    else: g.append(p(f'M228,{hy+84} Q250,{hy+104} 272,{hy+84} Q250,{hy+92} 228,{hy+84} Z', '#9c4a3c', 3))
    return svg_wrap(''.join(g), 500, 1000)


# ============================================================ NIÑO (estilo Arthur 14)
def kid(c):
    skin, skin_sh = SK[c.get('skin', 'light')]
    hair, hair_sh = c.get('hair', ('#3a2616', '#24170c'))
    shirt, shirt_sh = c.get('shirt', ('#e6dcc5', '#c3b799'))
    pants = c.get('pants', '#5e5040')
    g = []; cx = 250
    for s in (-1, 1):
        x = cx + s * 34
        g.append(p(f'M{x-28},640 L{x-24},900 L{x+24},900 L{x+28},640 Z', pants))
        g.append(p(f'M{x-30},880 L{x-30},930 Q{x-30},946 {x-12},946 L{x+30},946 Q{x+36},930 {x+26},880 Z', '#4a3322'))
    g.append(p('M176,450 Q250,428 324,450 L320,660 L180,660 Z', shirt))
    g.append(shade('M282,440 Q324,450 320,660 L290,660 Z', .2))
    if c.get('suspenders'):
        g.append(ln('M210,448 L206,660', c['suspenders'], 9)); g.append(ln('M290,448 L294,660', c['suspenders'], 9))
    if c.get('vest'):
        g.append(p('M178,452 Q210,440 236,440 L244,660 L182,660 Z', c['vest'])); g.append(p('M322,452 Q290,440 264,440 L256,660 L318,660 Z', c['vest']))
    g.append(p('M178,640 L322,640 L322,664 L178,664 Z', '#6a4428', 4))
    for s in (-1, 1):
        x = cx + s * 76
        g.append(p(f'M{x-s*4},454 Q{x+s*34},470 {x+s*34},540 L{x+s*36},640 L{x+s*12},642 L{x+s*8},548 Z', shirt))
        g.append(f'<circle cx="{x+s*24}" cy="652" r="18" {st(skin, 4)}/>')
    g.append(p('M232,400 L232,446 Q250,454 268,446 L268,400 Z', skin))
    if c.get('neck'): g.append(p('M226,436 Q250,456 274,436 L280,450 Q250,476 220,450 Z', c['neck'], 3))
    hy = 270
    if c.get('hairstyle') == 'long':
        g.append(p(f'M144,{hy-10} Q130,{hy+110} 160,{hy+150} L200,{hy+60} L300,{hy+60} L340,{hy+150} Q370,{hy+110} 356,{hy-10} Z', hair))
    g.append(p(f'M150,{hy-20} Q150,{hy+100} 214,{hy+132} Q250,{hy+146} 286,{hy+132} Q350,{hy+100} 350,{hy-20} Q250,{hy-100} 150,{hy-20} Z', skin))
    g.append(shade(f'M300,{hy-62} Q352,{hy-36} 350,{hy-10} Q350,{hy+100} 286,{hy+132} Q330,{hy+40} 300,{hy-62} Z', .25, skin_sh))
    for s in (-1, 1): g.append(f'<ellipse cx="{250+s*102}" cy="{hy+24}" rx="16" ry="24" {st(skin, 4)}/>')
    g.append(p(f'M144,{hy+20} Q130,{hy-110} 250,{hy-112} Q370,{hy-110} 356,{hy+20} Q344,{hy-20} 330,{hy-36} L322,{hy-6} L300,{hy-44} '
               f'L284,{hy-14} L262,{hy-50} L244,{hy-16} L222,{hy-48} L204,{hy-12} L186,{hy-40} Q160,{hy-10} 144,{hy+20} Z', hair))
    face = c.get('face', 'happy')
    for s in (-1, 1):
        x = 250 + s * 44
        if face == 'happy':
            g.append(f'<ellipse cx="{x}" cy="{hy+36}" rx="14" ry="17" fill="{K}"/><circle cx="{x+4}" cy="{hy+30}" r="5" fill="#fff"/>')
            g.append(ln(f'M{x-18},{hy+6} Q{x},{hy-4} {x+18},{hy+6}', hair_sh, 4))
        else:   # pícaro / bocón
            g.append(f'<ellipse cx="{x}" cy="{hy+36}" rx="16" ry="18" {st("#fff", 4)}/>')
            g.append(eye_dot(x + s * 2, hy + 38, 9, c.get('iris', '#3b2a20')))
            g.append(p(f'M{x-s*24},{hy+8} L{x+s*22},{hy+2} L{x+s*22},{hy+9} L{x-s*22},{hy+15} Z', hair_sh, 2))
        g.append(f'<ellipse cx="{250+s*64}" cy="{hy+76}" rx="16" ry="9" fill="{CHEEK}" opacity=".5"/>')
    g.append(ln(f'M252,{hy+50} Q258,{hy+66} 248,{hy+70}', skin_sh, 3))
    if face == 'happy': g.append(p(f'M226,{hy+86} Q250,{hy+114} 274,{hy+86} Q250,{hy+94} 226,{hy+86} Z', '#9c4a3c', 3))
    else: g.append(p(f'M222,{hy+88} Q250,{hy+84} 278,{hy+88} Q262,{hy+116} 236,{hy+108} Z', '#7a2a2a', 3))
    return svg_wrap(''.join(g), 500, 960)


# ============================================================ PERSONAJES
DEFS = {
    'dutch': lambda: man(dict(hair=('#1a1410', '#0a0806'), hairstyle='slick', mustache='thick', bcol='#1a1410', eyes='hard',
                              iris='#3a2a1a', mouth='smirk', shirt=('#efe8d8', '#cfc6b0'), outer=('vest', '#1e1a22'),
                              neck=('cravat', '#8e1f2a'), pants='#26232a', gun=True, gun2=True, watch=True, skin='light', wf=1.05)),
    'hosea': lambda: man(dict(hair=('#9a948a', '#6e685e'), hairstyle='short', beard='gray', bcol='#b4aea2', eyes='kind',
                              iris='#5a6a4a', mouth='smile', wrinkles=True, shirt=('#efe8d8', '#cfc6b0'),
                              outer=('suit', '#7a5a3a', '#5e4428'), neck=('tie', '#3a2a1a'), pants='#5e4a36',
                              hat=('flat', '#5a4632'), skin='light', wf=.92)),
    'john': lambda: man(dict(hair=('#14100c', '#060504'), hairstyle='long', beard='stubble', bcol='#1e1812', scars=True,
                             eyes='hard', iris='#4a5a6a', mouth='flat', shirt=('#5e6e7e', '#465460'), outer=('coat', '#3a2e24', '#2a2018'),
                             neck=('bandana', '#2a2a2a'), pants='#3a3a40', gun=True, hat=('cowboy', '#3a2e26'), wf=.95)),
    'micah': lambda: man(dict(hair=('#d8c08a', '#a8905a'), hairstyle='long', mustache='droop', beard='goatee', bcol='#cdb47a',
                              eyes='sly', iris='#6a7a5a', mouth='smirk', shirt=('#2a2a2e', '#1a1a1e'), outer=('vest', '#e2dccb'),
                              neck=('bandana', '#a8242e'), pants='#2e2b2a', gun=True, gun2=True, hat=('cowboy', '#e2d8c0'),
                              band='#2a1e14', skin='light', wf=.95)),
    'strauss': lambda: man(dict(hair=('#bdb6aa', '#8e887e'), hairstyle='bald', mustache='thin', bcol='#bdb6aa', glasses=True,
                                eyes='sly', iris='#4a4a4a', mouth='flat', wrinkles=True, shirt=('#f2ece0', '#d2cabb'),
                                outer=('suit', '#4a4a52', '#38383e'), neck=('bowtie', '#2a2a2e'), pants='#3a3a40',
                                belt=False, skin='pale', wf=.88)),
    'downes': lambda: man(dict(hair=('#6a5a48', '#4a3e30'), hairstyle='short', beard='stubble', bcol='#5a4a3a', eyes='tired',
                               iris='#5a4a3a', mouth='open', hollow=True, shirt=('#d8ccae', '#b4a888'), suspenders='#5a3a24',
                               pants='#5a5040', skin='pale', wf=.84)),
    'linton': lambda: man(dict(hair=('#c4beb2', '#8e887e'), hairstyle='short', beard='chops', bcol='#c4beb2', eyes='hard',
                               iris='#4a4a4a', mouth='frown', wrinkles=True, shirt=('#f4f0e6', '#d4ccbc'),
                               outer=('suit', '#22222a', '#16161c'), neck=('bowtie', '#16161c'), pants='#22222a', belt=False,
                               skin='light', wf=1.08)),
    'doctor': lambda: man(dict(hair=('#7a7268', '#5a544a'), hairstyle='short', beard='full', bcol='#8a8276', glasses=True,
                               eyes='kind', mouth='frown', wrinkles=True, shirt=('#f4f0e6', '#d4ccbc'),
                               outer=('vest', '#3a2e26'), neck=('tie', '#5a1e1e'), pants='#3a3430', skin='light')),
    'mary': lambda: woman(dict(hair=('#b8642e', '#8a4418'), hairstyle='updo', dress=('#3d7a5a', '#2e5e44'), sash='#e9dfc9',
                               buttons='#e9dfc9', flower='#e8485a', face='smile', skin='light')),
    'eliza': lambda: woman(dict(hair=('#3a2414', '#24160c'), hairstyle='loose', dress=('#9a4a36', '#7a3626'), apron='#ece4d4',
                                face='calm', skin='mid')),
    'abigail': lambda: woman(dict(hair=('#2a1c14', '#1a100a'), hairstyle='bun', dress=('#4a6a8e', '#3a546e'), apron='#e2d8c4',
                                  face='calm', skin='light')),
    'monja': lambda: woman(dict(nun=True, dress=('#16141a', '#0a080c'), collar='#f4f1ea', face='calm', holds='book', skin='light')),
    'viuda': lambda: woman(dict(hair=('#5a4a3e', '#3a2e24'), hairstyle='bun', dress=('#2a2a30', '#1c1c22'), face='sad', skin='light')),
    'isaac': lambda: kid(dict(hair=('#7a4e26', '#5a3818'), shirt=('#a8c4d8', '#88a4b8'), suspenders='#5a3a24', face='happy')),
    'jack': lambda: kid(dict(hair=('#2a1c12', '#1a100a'), shirt=('#e6dcc5', '#c3b799'), vest='#5a6a4a', neck='#8e1f2a', face='happy')),
    'john_teen': lambda: kid(dict(hair=('#14100c', '#060504'), hairstyle='long', shirt=('#8a9aa8', '#6a7a88'), suspenders='#3a2a1a',
                                  face='cheeky', iris='#4a5a6a', skin='light')),
}
CHARS.update(DEFS)

if __name__ == '__main__':
    render(list(DEFS))
