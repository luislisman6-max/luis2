"""Renderiza el video completo: escenas + subtítulos palabra por palabra + grano, a 1080x1920 30fps."""
import json, math, os, sys, subprocess
from multiprocessing import Process
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import escenas as scenes
from lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = json.load(open(os.path.join(HERE, 'words.json')))
DUR = float(os.environ.get('DUR', '84.90'))
NFR = int(math.ceil(DUR * FPS))

# --------------------------------------------------------------- subtítulos
KEY = {'dormir', 'caes', 'vacío', 'salto', 'involuntario', 'extraño', 'moviendo', 'sacudida', 'hípnica', '70%', 'personas',
       'respiración', 'lenta', 'ritmo', 'cardíaco', 'disminuye', 'músculos', 'relajarse', 'transición', 'nervioso',
       'contracción', 'repentina', 'curioso', 'teorías', 'cerebro', 'caída', 'científicos', 'exacta', 'tropiezas',
       'escaleras', 'cama', 'estrés', 'cafeína', 'sueño', 'frecuentes', 'normales', 'recuerda', 'cayendo', 'montaña',
       'rusa', 'almohada', 'tranquilo', 'inesperado'}
PUNCT = '.,?!…:;'


def norm(w):
    return w.strip('¿¡.,?!…:;"').lower()


def chunks():
    out, cur = [], []
    for i, w in enumerate(WORDS):
        if cur:
            prev = cur[-1]
            gap = w['s'] - prev['e']
            text_len = sum(len(x['w']) + 1 for x in cur) + len(w['w'])
            if prev['w'][-1] in PUNCT or len(cur) >= 4 or gap > 0.45 or text_len > 24:
                out.append(cur); cur = []
        cur.append(w)
    if cur: out.append(cur)
    res = []
    for i, c in enumerate(out):
        start = c[0]['s'] - 0.04
        nxt = out[i + 1][0]['s'] - 0.04 if i + 1 < len(out) else DUR
        end = min(nxt, c[-1]['e'] + 0.6)
        res.append(dict(words=c, s=start, e=end))
    return res


CHUNKS = chunks()
CAP_Y = 330
CAP_SIZE = 76
_cap_cache = {}


def word_sprite(txt, state):
    """state: 'act' (palabra que suena), 'old' (ya dicha)"""
    k = (txt, state)
    if k not in _cap_cache:
        fill = (255, 255, 255, 255) if state == 'act' else (232, 222, 236, 255)
        _cap_cache[k] = text_sprite(txt, CAP_SIZE, fill=fill, kind='k', stroke=8, stroke_fill=(28, 10, 26, 255))
    return _cap_cache[k]


def layout(ch):
    if 'lay' in ch: return ch['lay']
    f = font(CAP_SIZE, 'k')
    dr = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    sp = CAP_SIZE * 0.28
    lines, cur, wsum = [], [], 0
    for w in ch['words']:
        ww = dr.textlength(w['w'], font=f)
        if cur and wsum + sp + ww > 900:
            lines.append(cur); cur, wsum = [], 0
        cur.append((w, ww)); wsum += (sp if len(cur) > 1 else 0) + ww
    lines.append(cur)
    lay = []
    lh = CAP_SIZE * 1.18
    y0 = CAP_Y - (len(lines) - 1) * lh / 2
    for li, ln in enumerate(lines):
        tot = sum(ww for _, ww in ln) + sp * (len(ln) - 1)
        x = W / 2 - tot / 2
        for w, ww in ln:
            lay.append((w, x + ww / 2, y0 + li * lh, ww))
            x += ww + sp
    ch['lay'] = lay
    return lay


def draw_captions(img, t):
    for ch in CHUNKS:
        if not (ch['s'] <= t < ch['e']): continue
        lay = layout(ch)
        words = ch['words']
        act = None
        for i, w in enumerate(words):
            nxt = words[i + 1]['s'] if i + 1 < len(words) else ch['e']
            if w['s'] - 0.04 <= t < nxt - 0.04: act = i
        for i, (w, cx, cy, ww) in enumerate(lay):
            if t < w['s'] - 0.04: continue
            state = 'act' if i == act else 'old'
            sc = 0.75 + 0.25 * ease_back(prog(t, w['s'] - 0.04, 0.13), 2.2)
            if state == 'act' and norm(w['w']) in KEY:
                d = ImageDraw.Draw(img)
                pad = 10
                box = [cx - ww / 2 - pad, cy - CAP_SIZE * 0.55, cx + ww / 2 + pad, cy + CAP_SIZE * 0.55]
                L = layer(); ImageDraw.Draw(L).rectangle(box, fill=(40, 110, 230, 120))
                img.alpha_composite(L)
                d.rectangle(box, outline=(70, 150, 255, 255), width=4)
                for bx, by in ((box[0], box[1]), (box[2], box[1]), (box[0], box[3]), (box[2], box[3])):
                    d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(255, 255, 255, 255), outline=(70, 150, 255, 255), width=3)
            paste(img, word_sprite(w['w'], state), cx, cy, scale=sc, alpha=1.0 if state == 'act' else 0.88)
        break


# --------------------------------------------------------------- frame
GRAIN = None


def frame(t, fi):
    global GRAIN
    st, fn = scenes.scene_at(t)
    img, z, (cx, cy) = fn(t)
    # golpe de zoom en cada corte
    since = t - st
    if st > 0 and since < 0.18:
        z *= 1 + 0.06 * (1 - ease_out(since / 0.18))
    if abs(z - 1) > 1e-3:
        cw, chh = W / z, H / z
        x0 = clamp(cx - cw / 2, 0, W - cw); y0 = clamp(cy - chh / 2, 0, H - chh)
        img = img.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + chh))
    draw_captions(img, t)
    arr = np.asarray(img.convert('RGB'), dtype=np.int16)
    if GRAIN is None:
        rng = np.random.default_rng(5)
        GRAIN = [rng.integers(-7, 8, (H, W, 1), dtype=np.int16) for _ in range(4)]
    arr = arr + GRAIN[fi % 4]
    return np.clip(arr, 0, 255).astype(np.uint8)


def worker(k, f0, f1, out):
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(f0, f1):
        p.stdin.write(frame(fi / FPS, fi).tobytes())
        if (fi - f0) % 150 == 0:
            print(f'[w{k}] {fi - f0}/{f1 - f0}', flush=True)
    p.stdin.close(); p.wait()


if __name__ == '__main__':
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    if len(sys.argv) > 2 and sys.argv[2] == 'stills':
        for tt in sys.argv[3:]:
            t = float(tt)
            Image.fromarray(frame(t, 0)).save(os.path.join(outdir, f'still_{t:06.2f}.png'))
        sys.exit()
    nw = int(os.environ.get('NW', '4'))
    bounds = [round(NFR * i / nw) for i in range(nw + 1)]
    procs = []
    for k in range(nw):
        p = Process(target=worker, args=(k, bounds[k], bounds[k + 1], os.path.join(outdir, f'part{k}.mp4')))
        p.start(); procs.append(p)
    for p in procs: p.join()
    with open(os.path.join(outdir, 'parts.txt'), 'w') as f:
        for k in range(nw): f.write(f"file 'part{k}.mp4'\n")
    print('done', NFR, 'frames')
