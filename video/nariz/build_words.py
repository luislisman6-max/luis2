import json, difflib, unicodedata, sys, re
import numpy as np
S = sys.argv[1]
rec = [w for w in json.load(open(S + '/work/dtw.json')) if not w['w'].startswith('[')]
sil = [s for s in json.load(open(S + '/work/sil.json'))]
script = open(S + '/guion.txt').read().split()
END = float(sys.argv[2])
def n(w):
    w = unicodedata.normalize('NFD', w.lower()); w = ''.join(c for c in w if unicodedata.category(c) != 'Mn')
    return ''.join(c for c in w if c.isalnum())
def syl(w):
    pass
    return max(1, len(re.findall(r'[aeiouáéíóúü]+', w.lower())))
A = [n(w) for w in script]; B = [n(w['w']) for w in rec]
sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
E1 = [None] * len(script); E2 = [None] * len(script)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal' or (tag == 'replace' and i2 - i1 == j2 - j1):
        for k in range(i2 - i1):
            E1[i1 + k] = rec[j1 + k]['s'] - 0.09; E2[i1 + k] = rec[j1 + k]['t0']
# estimación 3: reparto por sílabas dentro de cada tramo de voz (entre silencios)
regions = []; prev = 0.0
for a, b in sil:
    if a > prev + 0.05: regions.append((prev, a))
    prev = b
if prev < END: regions.append((prev, END))
regions = [(max(r[0], 0.22), r[1]) for r in regions]
import math
NW, NR = len(script), len(regions)
SY = [syl(w) for w in script]
tot_dur = sum(r1 - r0 for r0, r1 in regions); rate = sum(SY) / tot_dur
def wcost(i, r):
    r0, r1 = regions[r]; c = []
    for x in (E1[i], E2[i]):
        if x is None: continue
        c.append(0 if r0 - 0.12 <= x <= r1 - 0.05 else min(abs(x - r0), abs(x - r1)))
    return min(c) if c else 0.3
INF = 1e9
D = [[INF] * (NW + 1) for _ in range(NR + 1)]; P = [[0] * (NW + 1) for _ in range(NR + 1)]
D[0][0] = 0
for r in range(1, NR + 1):
    for j in range(1, NW + 1):
        best = INF
        for k in range(max(0, j - 25), j):
            if D[r - 1][k] >= INF: continue
            sy = sum(SY[k:j]); dur = regions[r - 1][1] - regions[r - 1][0]
            c = D[r - 1][k] + sum(wcost(i, r - 1) for i in range(k, j)) * 4 + 0.6 * math.log((sy / dur) / rate) ** 2 + (0 if script[j - 1][-1] in '.,?!:;' else 0.5) + (0.8 if script[j - 1].lower() in ('y', 'o', 'que', 'de', 'la', 'el', 'tu') else 0)
            if c < best: best, P[r][j] = c, k
        D[r][j] = best
reg_of = [0] * NW; j = NW
for r in range(NR, 0, -1):
    k = P[r][j]
    for i in range(k, j): reg_of[i] = r - 1
    j = k
for r in range(NR):
    print(f"{regions[r][0]:6.2f}-{regions[r][1]:6.2f}", ' '.join(script[i] for i in range(NW) if reg_of[i] == r))
E3 = [None] * len(script)
for r in set(reg_of):
    idx = [i for i in range(len(script)) if reg_of[i] == r]
    tot = sum(syl(script[i]) for i in idx); c = 0
    r0, r1 = regions[r]
    for i in idx:
        E3[i] = r0 + (r1 - r0) * c / tot; c += syl(script[i])
st = []
for i in range(len(script)):
    xs = [x for x in (E1[i], E2[i], E3[i]) if x is not None]
    v = float(np.median(xs))
    r0, r1 = regions[reg_of[i]]
    # primera palabra de un tramo: empieza justo al acabar el silencio
    if i == 0 or reg_of[i] != reg_of[i - 1]: v = r0 - 0.02
    v = min(max(v, r0 - 0.02), r1 - 0.1)
    if st and v < st[-1] + 0.07: v = st[-1] + 0.07
    st.append(v)
out = []
for i, w in enumerate(script):
    e = st[i + 1] if i + 1 < len(script) else END
    r1 = regions[reg_of[i]][1]
    e = min(e, r1)
    out.append({'w': w, 's': round(st[i], 3), 'e': round(e, 3)})
json.dump(out, open(S + '/work/words.json', 'w'), ensure_ascii=False, indent=0)
print(' '.join(f"{o['w']}[{o['s']:.2f}]" for o in out))
bad = [(script[i], E1[i], E2[i], E3[i]) for i in range(len(script)) if E1[i] is not None and max(abs(E1[i]-E2[i]), abs(E1[i]-E3[i]), abs(E2[i]-E3[i])) > 0.4]
print(len(bad), 'palabras con desacuerdo > 0.4 s:', [(b[0], round(b[1],2), round(b[2],2), round(b[3],2)) for b in bad])
