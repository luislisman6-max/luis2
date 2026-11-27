"""Tiempos por palabra: guion corregido a mano + tiempos DTW de whisper.cpp, ajustados al final de cada pausa real."""
import json, difflib, unicodedata, sys
S = sys.argv[1]; END = float(sys.argv[2])
rec = [w for w in json.load(open(S + '/work/dtw.json')) if not w['w'].startswith('[')]
sil = [s for s in json.load(open(S + '/work/sil.json')) if s[1] - s[0] >= 0.06]
script = open(S + '/guion.txt').read().split()
def n(w):
    w = unicodedata.normalize('NFD', w.lower()); w = ''.join(c for c in w if unicodedata.category(c) != 'Mn')
    return ''.join(c for c in w if c.isalnum())
A = [n(w) for w in script]; B = [n(w['w']) for w in rec]
st = [None] * len(script)
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
    if tag == 'equal' or (tag == 'replace' and i2 - i1 == j2 - j1):
        for k in range(i2 - i1): st[i1 + k] = rec[j1 + k]['s'] - 0.10
miss = [script[i] for i in range(len(st)) if st[i] is None]
for i in range(len(st)):            # interpolar las que no casaron
    if st[i] is None:
        a = max(j for j in range(i) if st[j] is not None) if any(st[:i]) else 0
        b = next(j for j in range(i, len(st)) if st[j] is not None)
        st[i] = st[a] + (st[b] - st[a]) * (i - a) / (b - a)
snapped = 0
raw = st[:]
for s0, s1 in sil:                  # la primera palabra tras cada pausa empieza donde acaba la pausa
    if s1 - s0 < 0.08: continue
    c = [i for i in range(len(raw)) if raw[i] + 0.10 > s1 - 0.05]
    if c and raw[c[0]] + 0.10 - s1 <= 0.40:
        st[c[0]] = s1 - 0.02; snapped += 1
for i in range(1, len(st)):
    if st[i] < st[i - 1] + 0.07: st[i] = st[i - 1] + 0.07
out = []
for i, w in enumerate(script):
    e = st[i + 1] if i + 1 < len(script) else END
    for s0, s1 in sil:
        if st[i] < s0 < e: e = s0; break
    out.append({'w': w, 's': round(max(0, st[i]), 3), 'e': round(e, 3)})
json.dump(out, open(S + '/words.json', 'w'), ensure_ascii=False, indent=0)
print(len(script), 'palabras | sin casar:', miss, '| ajustadas a pausa:', snapped)
print(' '.join(f"{o['w']}[{o['s']:.2f}]" for o in out))
