import json, sys, wave, re, difflib, subprocess
import numpy as np
import _pywhispercpp as pw
from pywhispercpp.model import Model
S = sys.argv[1]
wf = wave.open(S + '/work/voz16.wav'); A = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
SR = 16000
out = subprocess.run(['ffmpeg', '-hide_banner', '-i', S + '/work/voz16.wav', '-af', 'silencedetect=noise=-35dB:d=0.2', '-f', 'null', '-'], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', out)]
en = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', out)]
sil = list(zip(st, en))
# cortes en el centro de cada silencio; trozos de <= ~9 s
dur = len(A) / SR
cuts = [0.0]
for a, b in sil:
    m = (a + b) / 2
    if m - cuts[-1] > 4.0: cuts.append(m)
cuts.append(dur)
m = Model(S + '/dl/kt/package/model/ggml-base-q5_1.bin', n_threads=4, language='es', no_context=True, token_timestamps=True, print_progress=False,
          context_params={'flash_attn': False, 'dtw_token_timestamps': True, 'dtw_aheads_preset': pw.whisper_alignment_heads_preset.WHISPER_AHEADS_BASE}, redirect_whispercpp_logs_to=None,
          initial_prompt='sacudida hípnica, cafeína, montaña rusa, almohada.')
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
