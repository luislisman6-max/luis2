import ctranslate2, json, sys
from faster_whisper import WhisperModel
S=sys.argv[1]
import numpy as np, wave
wf=wave.open(S+"/work/voz16.wav");audio=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768
m=WhisperModel(S+"/model",device="cpu",compute_type="int8",cpu_threads=4)
segs,info=m.transcribe(audio,language="es",word_timestamps=True,beam_size=5,vad_filter=False,
  initial_prompt="Atolla, abismo Challenger, fosa de las Marianas, nieve marina, anfípodos, pez caracol, La Duda Animada.")
out=[]
for s in segs:
    out.append({"start":s.start,"end":s.end,"text":s.text,"words":[{"w":w.word,"s":w.start,"e":w.end,"p":w.probability} for w in s.words]})
    print(f"{s.start:7.2f} {s.end:7.2f} {s.text}",flush=True)
json.dump(out,open(S+"/work/words.json","w"),ensure_ascii=False,indent=1)
