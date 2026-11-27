"""Transcribe voz.mp3 con marcas de tiempo por palabra (Whisper local) -> words.json + words.js
Uso: python transcribe.py <carpeta_del_video> [modelo] ["nombres propios para ayudar a Whisper"]
  modelo: "small" (se descarga solo la 1a vez) o ruta a un modelo CTranslate2 local.
Requiere: pip install faster-whisper numpy ; ffmpeg en el PATH.
Después REVISA words.js y corrige palabras mal oídas (ej. "ser trampa" -> "hacer trampa", "1." -> "1").
"""
import sys, json, subprocess, numpy as np
from faster_whisper import WhisperModel
V = sys.argv[1]; M = sys.argv[2] if len(sys.argv) > 2 else "small"; P = sys.argv[3] if len(sys.argv) > 3 else ""
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", V + "/voz.mp3", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
m = WhisperModel(M, device="cpu", compute_type="int8")
segs, _ = m.transcribe(a, language="es", beam_size=5, word_timestamps=True, vad_filter=False, initial_prompt=P or None)
words = []
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}")
    words += [{"w": x.word.strip(), "s": round(x.start, 2), "e": round(x.end, 2)} for x in s.words]
json.dump(words, open(V + "/words.json", "w", encoding="utf-8"), ensure_ascii=False)
open(V + "/words.js", "w", encoding="utf-8").write("window.WORDS=" + json.dumps(words, ensure_ascii=False) + ";")
print(len(words), "palabras; duración voz ~", words[-1]["e"] if words else 0, "s")
