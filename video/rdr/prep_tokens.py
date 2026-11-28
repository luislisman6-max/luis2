"""Une los tiempos de Whisper con el texto del guion (corrige nombres mal oídos).
Uso: python3 prep_tokens.py <WORK> <guion.txt>"""
import json, sys, re, unicodedata, difflib
work, guion = sys.argv[1], sys.argv[2]
def norm(s): return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode())
segs = json.load(open(f'{work}/words.json'))
wh = [dict(t=w['w'].strip(), s=w['s'], e=w['e']) for sg in segs for w in sg['words'] if w['w'].strip()]
txt = open(guion, encoding='utf8').read()
sc = [w for w in re.findall(r'\S+', txt) if norm(w)]
A, B = [norm(w['t']) for w in wh], [norm(w) for w in sc]
out = [dict(w) for w in wh]
fixed = 0
for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
    if op == 'equal':
        for k in range(i2 - i1): out[i1 + k]['t'] = sc[j1 + k]
    elif op == 'replace' and i2 - i1 == j2 - j1:
        for k in range(i2 - i1):
            if not A[i1 + k].isdigit():
                out[i1 + k]['t'] = sc[j1 + k]; fixed += 1
                print('fix:', wh[i1 + k]['t'], '->', sc[j1 + k])
    elif op != 'equal':
        print(op, ' '.join(w['t'] for w in wh[i1:i2]), '|', ' '.join(sc[j1:j2]))
MANUAL = {'Dodge': 'Dutch', 'Vander': 'van der'}
for w in out:
    w['t'] = MANUAL.get(w['t'].strip('.,'), w['t']) + ('.' if w['t'].endswith('.') and w['t'].strip('.,') in MANUAL else '')
    w['t'] = w['t'].strip('"“”«»')
    w['n'] = norm(w['t'])
json.dump(out, open(f'{work}/tokens.json', 'w'), ensure_ascii=False, indent=0)
print('tokens', len(out), 'corregidos', fixed)
