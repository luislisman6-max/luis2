"""Efectos de sonido sintetizados (numpy, sin descargas) + mezcla con la voz. SIN música. La voz siempre por encima.
Uso: node render.mjs cues ; python sfx.py -> mix.wav
Nombres válidos para sfx(t, nombre, vol) en anim.js = claves del dict G de abajo."""
import json, os, sys, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sfx_base as B
from sfx_base import SR, t, env, noise, lp_fast, hp_fast, sweep, norm, bp
rng = np.random.default_rng(9)
def place(out, x, sec, g=1.0):
    i = int(sec * SR); j = min(len(out), i + len(x))
    if j > i: out[i:j] += x[:j - i] * g
def bag():   # puñetazo seco al saco
    a = lp_fast(noise(.16), 260) * env(int(SR * .16), curve=9) * 1.2
    b = bp(noise(.05), 700, 3200) * env(int(SR * .05), curve=22) * .5
    s = sweep(110, 45, .16) * env(int(SR * .16), curve=7) * .8
    out = a + s; out[:len(b)] += b
    return norm(np.tanh(out * 1.6), .85)
def crackle(d=.7):
    out = np.zeros(int(SR * d))
    for _ in range(60):
        o = rng.uniform(0, d - .02); c = bp(noise(.006), 2000, 9000) * env(int(SR * .006), curve=30)
        place(out, c, o, rng.uniform(.2, 1) * (1 - o / d))
    return norm(out, .6)
def bf():    # impacto Black Flash: golpe + chispazo eléctrico + boom grave
    out = np.zeros(int(SR * 1.8))
    place(out, B.impact(), 0, 1.0); place(out, B.boom(), 0, .7); place(out, bag(), 0, .8)
    place(out, B.zap(), .01, .55); place(out, crackle(), .03, .7)
    return norm(np.tanh(out * 1.3), .95)
def powerup():  # transformación: subida + brillo + golpe grave
    out = np.zeros(int(SR * 1.4))
    place(out, B.riser(), 0, .5); place(out, B.shimmer(), .05, .6); place(out, B.boom(), .0, .6); place(out, B.impact(), 0, .5)
    tt = t(1.2); hum = (np.sin(2 * np.pi * 70 * tt) + .5 * np.sin(2 * np.pi * 140 * tt)) * env(len(tt), curve=3) * .5
    place(out, hum, 0)
    return norm(np.tanh(out * 1.2), .9)
def aura(d=1.6):  # zumbido de aura
    tt = t(d); x = (np.sin(2 * np.pi * 55 * tt) * .6 + bp(noise(d), 200, 900) * .5) * (0.7 + .3 * np.sin(2 * np.pi * 6 * tt))
    return norm(x * np.minimum(1, np.linspace(0, 4, len(tt))) * np.minimum(1, np.linspace(3, 0, len(tt))), .5)
def magic(d=1.0):  # hechizo de Babidi
    tt = t(d); f = 600 + 400 * np.sin(2 * np.pi * 5 * tt) + 300 * tt
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * .5 + np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR) * .25 + bp(noise(d), 2000, 6000) * .15
    return norm(x * np.sin(np.linspace(0, np.pi, len(tt))), .5)
def neon():
    d = .45; tt = t(d); hum = np.sin(2 * np.pi * 120 * tt) * .5 + bp(noise(d), 1500, 6000) * .3
    gate = np.ones(len(tt))
    for a, b in ((.05, .1), (.16, .22)): gate[int(a * SR):int(b * SR)] = .15
    return norm(hum * gate * env(len(tt), curve=2), .4)
G = dict(powerup=powerup, aura=aura, magic=magic, step=B.GEN['step'], buzz=B.GEN['buzz'], stinger=B.GEN['stinger'], rumble=B.GEN['rumble'], boom=B.boom, bag=bag, bf=bf, neon=neon, crackle=crackle,
         whoosh=B.whoosh, impact=B.impact, pop=B.pop, tick=B.tick, slam=B.slam, thud=B.thud, thump=B.thump,
         chain=B.chainfx, glass=B.glass, crack=B.crack, zap=B.zap, ding=B.ding, riser=B.riser, shimmer=B.shimmer,
         glint=B.glint, blip=B.blip, swish=B.swish, hit=B.hit)
if __name__ == "__main__":
    cues = sorted(json.load(open(os.path.join(HERE, "cues.json"))))
    last, kept = {}, []
    for c in cues:
        if c[0] - last.get(c[1], -9) >= .08: kept.append(c); last[c[1]] = c[0]
    raw = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(HERE, "voz.mp3")], capture_output=True, text=True).stdout
    total = max(float(raw.strip()), max(c[0] for c in kept) + 2) + .5; n = int(SR * total); fx = np.zeros(n); cache = {}
    for tm, name, vol in kept:
        if name not in cache: cache[name] = G[name]()
        place(fx, cache[name], tm, vol)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(HERE, "voz.mp3"), "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True, check=True).stdout
    voice = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    v = np.zeros(n); v[:min(n, len(voice))] = voice[:n]
    v = v / (np.max(np.abs(v)) + 1e-9) * 0.95
    envv = np.convolve(np.abs(v), np.ones(4410) / 4410, mode="same")
    duck = 1 - 0.55 * np.clip(envv / 0.06, 0, 1)
    fxm = fx * 0.30 * duck
    mix = np.tanh((v + fxm) * 1.05) * 0.95
    st = np.stack([mix, mix], 1)
    with wave.open(os.path.join(HERE, "mix.wav"), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
    vr = np.sqrt(np.mean(v[np.abs(v) > .01] ** 2)); fr = np.sqrt(np.mean(fxm[np.abs(fxm) > .01] ** 2))
    print("mix.wav", len(kept), "efectos | voz RMS", round(20 * np.log10(vr), 1), "dB | efectos RMS", round(20 * np.log10(fr + 1e-9), 1), "dB")
