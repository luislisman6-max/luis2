import json, sys, wave, re, difflib, subprocess
import numpy as np
import _pywhispercpp as pw
from pywhispercpp.model import Model
S = sys.argv[1]
wf = wave.open(S + '/work/voz16.wav'); A = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
SR = 16000
hh = 160; fr = A[:len(A)//hh*hh].reshape(-1, hh); rr = 20*np.log10(np.sqrt((fr**2).mean(1))+1e-9)
qq = rr < -38; sil = []; i = 0
while i < len(qq):
    if qq[i]:
        j = i
        while j < len(qq) and qq[j]: j += 1
        if (j - i) * 0.01 >= 0.06: sil.append((i*0.01, j*0.01))
        i = j
    else: i += 1
# cortes en el centro de cada silencio; trozos de <= ~9 s
dur = len(A) / SR
cuts = [0.0]
for a, b in sil:
    m = (a + b) / 2
    if m - cuts[-1] > 5.0 and b - a >= 0.08: cuts.append(m)
cuts.append(dur)
if len(sys.argv) > 2: cuts = [0.0, dur]
m = Model(S + '/dl/kt/package/model/ggml-base-q5_1.bin', n_threads=4, language='es', no_context=True, token_timestamps=True, print_progress=False,
          context_params={'flash_attn': False, 'dtw_token_timestamps': True, 'dtw_aheads_preset': pw.whisper_alignment_heads_preset.WHISPER_AHEADS_BASE}, redirect_whispercpp_logs_to=None,
          initial_prompt='Tu piel tiene un mapa oculto: líneas de Blaschko, células, vientre, erupciones, espirales.')
words = []
for c0, c1 in zip(cuts[:-1], cuts[1:]):
    seg = A[int(c0 * SR):int(c1 * SR)]
    seg = np.concatenate([seg, np.zeros(SR // 2, np.float32)])
    m.transcribe(seg)
    ctx = m._ctx
    eot = pw.whisper_token_eot(ctx)
    for si in range(pw.whisper_full_n_segments(ctx)):
        for ti in range(pw.whisper_full_n_tokens(ctx, si)):
            td = pw.whisper_full_get_token_data(ctx, si, ti)
            if td.id >= eot: continue
            txt = pw.whisper_full_get_token_text(ctx, si, ti)
            t = c0 + td.t_dtw / 100; t1 = c0 + td.t1 / 100; t0r = c0 + td.t0/100
            if txt.startswith(' ') or not words or words[-1].get('closed'):
                words.append({'w': txt.strip(), 's': t, 't0': t0r, 'e': t1, 'toks': [t]})
            else:
                words[-1]['w'] += txt; words[-1]['toks'].append(t); words[-1]['e'] = t1
    if words: words[-1]['closed'] = True
    print(f'{c0:6.2f}-{c1:6.2f}', ' '.join(w['w'] for w in words if w['s'] >= c0), flush=True)
json.dump([{'w': w['w'], 's': w['s'], 'e': w['e'], 't0': w['t0']} for w in words if w['w']], open(S + '/work/dtw.json', 'w'), ensure_ascii=False)
json.dump(sil, open(S + '/work/sil.json', 'w'))
