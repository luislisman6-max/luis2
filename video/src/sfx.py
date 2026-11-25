import json, sys, wave
import numpy as np

SR = 44100
rng = np.random.default_rng(1)
work = sys.argv[1]
meta = json.load(open(f"{work}/sfx.json"))
DUR = meta["dur"]

def t_(d): return np.arange(int(d * SR)) / SR
def env(n, a=0.005, r=0.1, shape=1.0):
    e = np.ones(n); na = max(1, int(a * SR)); nr = max(1, min(n - na, int(r * SR)))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr) ** shape; return e
def expd(n, k): return np.exp(-np.arange(n) / SR * k)
def noise(d): return rng.standard_normal(int(d * SR))
from scipy.signal import lfilter
def lp(x, fc):  # one-pole lowpass (fc scalar or array)
    if np.isscalar(fc):
        a = np.exp(-2 * np.pi * fc / SR); return lfilter([1 - a], [1, -a], x)
    fc = np.broadcast_to(np.asarray(fc, float), x.shape)
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0.0
    for i in range(len(x)): s = (1 - a[i]) * x[i] + a[i] * s; y[i] = s
    return y
def hp(x, fc): return x - lp(x, fc)
def bp(x, lo, hi): return lp(hp(x, lo), hi)
def sweep(f0, f1, d, wav='sin'):
    t = t_(d); f = np.geomspace(f0, f1, len(t)); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) if wav == 'sin' else (2 * (ph / (2 * np.pi) % 1) - 1)
def tone(f, d): return np.sin(2 * np.pi * f * t_(d))
def norm(x, p=1.0): m = np.max(np.abs(x)) + 1e-9; return x / m * p

def whoosh(d=0.6, f0=300, f1=2500):
    n = noise(d); fc = np.concatenate([np.geomspace(f0, f1, len(n) // 2), np.geomspace(f1, f0, len(n) - len(n) // 2)])
    x = bp(n, 150, 6000); x = lp(x, fc); return norm(x * np.hanning(len(x)), 0.8)
def pop():
    d = 0.09; x = sweep(900, 300, d) * expd(int(d * SR), 45); return norm(x, 0.8)
def ping(f=1320):
    d = 1.2; x = (tone(f, d) + 0.4 * tone(f * 2.01, d) + 0.2 * tone(f * 3.0, d)) * expd(int(d * SR), 4.5); return norm(x * env(len(x), 0.002, 0.1), 0.7)
def sparkle():
    d = 0.9; out = np.zeros(int(d * SR))
    for i, f in enumerate([2093, 2637, 3136, 4186, 3520, 4699]):
        st = int(i * 0.07 * SR); dd = 0.5; s = tone(f, dd) * expd(int(dd * SR), 9)
        out[st:st + len(s)] += s[:len(out) - st]
    return norm(out, 0.6)
def shimmer(big=False):
    d = 1.6 if big else 1.2; out = np.zeros(int(d * SR)); t = t_(d)
    for f in ([523, 659, 784, 1046, 1318] if not big else [392, 523, 659, 784, 1046, 1318, 1568]):
        out += np.sin(2 * np.pi * f * t + 3 * np.sin(2 * np.pi * 5 * t)) * 0.3
    out += bp(noise(d), 3000, 9000) * 0.15
    e = np.minimum(t / (0.15 if not big else 0.05), 1) * np.exp(-t * (2.5 if not big else 2.0))
    return norm(out * e, 0.7)
def switch(on):
    d = 0.5; click = bp(noise(0.02), 800, 6000) * env(int(0.02 * SR), 0.001, 0.015)
    hum = (tone(60, d) + 0.5 * tone(120, d) + 0.25 * tone(180, d)) * 0.5
    t = t_(d); hume = (np.minimum(t / 0.3, 1) if on else np.exp(-t * 8)) * (np.exp(-t * 2) if on else 1)
    x = hum * hume; x[:len(click)] += click * 3
    if not on: x = np.concatenate([x[:int(0.35 * SR)]])
    return norm(x, 0.8)
def alarm():
    d = 1.4; t = t_(d); f = 700 + 250 * np.sin(2 * np.pi * 3 * t)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.05, 0.3); return norm(lp(x, 2500), 0.45)
def chomp():
    out = np.zeros(int(0.35 * SR))
    for st in [0, 0.15]:
        s = lp(noise(0.08), 1800) * expd(int(0.08 * SR), 40) + sweep(300, 120, 0.08) * expd(int(0.08 * SR), 30)
        i = int(st * SR); out[i:i + len(s)] += s
    return norm(out, 0.8)
def boom():
    d = 2.0; x = sweep(80, 35, d) * expd(int(d * SR), 2.2) + lp(noise(d), 200) * expd(int(d * SR), 3) * 0.6
    return norm(x * env(len(x), 0.01, 0.3), 0.9)
def stinger():
    d = 1.8; t = t_(d); x = (tone(98, d) + tone(147, d) * 0.6 + tone(196, d) * 0.4) * np.exp(-t * 1.8)
    x += lp(noise(d), 400) * np.exp(-t * 6) * 0.5; return norm(x * env(len(x), 0.005, 0.3), 0.85)
def gulp():
    d = 0.35; x = sweep(200, 700, d) * np.sin(np.pi * t_(d) / d) ** 2; return norm(lp(x, 1500), 0.8)
def scribble(d=1.3):
    n = noise(d); t = t_(d); am = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 7 * t + np.sin(2 * np.pi * 1.3 * t)))
    x = bp(n, 2000, 7000) * lp(am, 40); return norm(x * env(len(x), 0.02, 0.1), 0.55)
def squish():
    d = 0.5; x = lp(noise(d), np.linspace(1200, 200, int(d * SR))) * np.sin(np.pi * t_(d) / d) + sweep(400, 120, d) * 0.4 * np.sin(np.pi * t_(d) / d)
    return norm(x, 0.7)
def boing():
    d = 0.6; t = t_(d); f = 220 + 120 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 5)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5); return norm(x, 0.7)
def bubbles(d=1.0, k=9):
    out = np.zeros(int(d * SR))
    for _ in range(k):
        st = rng.uniform(0, d - 0.12); dd = rng.uniform(0.04, 0.1); f0 = rng.uniform(400, 1200)
        s = sweep(f0, f0 * 2.2, dd) * np.sin(np.pi * t_(dd) / dd); i = int(st * SR); out[i:i + len(s)] += s
    return norm(out, 0.55)
def munch():
    out = np.zeros(int(0.7 * SR))
    for st in [0, 0.22, 0.44]:
        s = bp(noise(0.1), 300, 3000) * expd(int(0.1 * SR), 30); i = int(st * SR); out[i:i + len(s)] += s
    return norm(out, 0.75)
def shrink():
    d = 0.9; x = sweep(900, 150, d) * env(int(d * SR), 0.02, 0.2) + lp(noise(d), 600) * 0.2
    return norm(x, 0.7)
def creak():
    d = 1.4; t = t_(d); x = np.zeros(len(t)); per = (0.012 + 0.01 * t / d)
    ph = np.cumsum(1 / per) / SR; imp = (np.diff(np.floor(ph), prepend=0) > 0).astype(float)
    x = bp(imp + 0.05 * noise(d), 150, 1500) * env(len(t), 0.1, 0.4); return norm(x, 0.7)
def riser():
    d = 1.3; x = sweep(200, 1200, d) * 0.6 + bp(noise(d), 500, 5000) * np.linspace(0, 1, int(d * SR)) * 0.4
    return norm(x * env(len(x), 0.4, 0.08), 0.6)
def paper():
    d = 0.4; return norm(bp(noise(d), 1500, 8000) * env(int(d * SR), 0.01, 0.2) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 15 * t_(d)))), 0.6)
def clank():
    d = 0.6; t = t_(d); x = sum(np.sin(2 * np.pi * f * t) for f in [523, 1187, 1933, 2771]) * np.exp(-t * 9); return norm(x, 0.55)
def swipe():
    d = 0.25; x = bp(noise(d), 1500, 7000) * np.sin(np.pi * t_(d) / d) ** 2; return norm(x, 0.8)
def rec():
    d = 0.3; x = np.concatenate([tone(1800, 0.08) * env(int(0.08 * SR), 0.003, 0.02), np.zeros(int(0.06 * SR)), tone(1800, 0.08) * env(int(0.08 * SR), 0.003, 0.02)])
    return norm(x, 0.5)
def swim():
    out = np.zeros(int(1.2 * SR))
    for k in range(4):
        s = lp(noise(0.25), 700) * np.sin(np.pi * t_(0.25) / 0.25) ** 2; i = int(k * 0.28 * SR); out[i:i + len(s)] += s
    return norm(out, 0.5)
def clap():
    d = 0.2; x = bp(noise(d), 800, 5000) * expd(int(d * SR), 35) + sweep(500, 200, d) * expd(int(d * SR), 30) * 0.5; return norm(x, 0.85)
def thunk():
    d = 0.3; x = sweep(180, 80, d) * expd(int(d * SR), 18); return norm(x, 0.8)
def buzz():
    d = 0.5; t = t_(d); x = np.sign(np.sin(2 * np.pi * 140 * t)) * env(len(t), 0.01, 0.05); return norm(lp(x, 1500), 0.4)
def rumble():
    d = 2.2; x = lp(noise(d), 120) * env(int(d * SR), 0.5, 0.8) + sweep(50, 40, d) * 0.4; return norm(x, 0.9)
def thud():
    d = 1.0; t = t_(d); x = np.sin(2 * np.pi * np.cumsum(np.geomspace(90, 40, len(t))) / SR) * np.exp(-t * 7) + lp(noise(d), 300) * np.exp(-t * 12) * 0.7
    return norm(x, 1.0)
def puff():
    d = 1.0; return norm(lp(noise(d), 900) * env(int(d * SR), 0.02, 0.8, 2), 0.6)
def sand():
    d = 1.2; return norm(bp(noise(d), 2000, 8000) * env(int(d * SR), 0.3, 0.6) * (0.6 + 0.4 * np.sin(2 * np.pi * 2 * t_(d))), 0.35)
def skitter():
    d = 1.1; out = np.zeros(int(d * SR))
    for _ in range(26):
        st = rng.uniform(0, d - 0.02); s = bp(noise(0.012), 2000, 7000) * env(int(0.012 * SR), 0.001, 0.008); i = int(st * SR); out[i:i + len(s)] += s
    return norm(out, 0.55)
def waves():
    d = 6.0; t = t_(d); x = bp(noise(d), 200, 2000) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.35 * t) ** 2) * env(len(t), 1.0, 2.0); return norm(x, 0.45)
def sonar():
    d = 2.2; t = t_(d); x = np.sin(2 * np.pi * 1100 * t) * np.exp(-t * 2.6) * env(len(t), 0.003, 0.2)
    dl = int(0.35 * SR); echo = np.zeros_like(x); echo[dl:] = x[:-dl] * 0.35
    return norm(x + echo, 0.8)

LIB = {
    'whoosh': lambda: whoosh(), 'whooshDown': lambda: whoosh(0.8, 2500, 200), 'pop': pop, 'ping': ping, 'sparkle': sparkle,
    'shimmer': lambda: shimmer(False), 'shimmerBig': lambda: shimmer(True), 'on': lambda: switch(True), 'off': lambda: switch(False),
    'alarm': alarm, 'chomp': chomp, 'boom': boom, 'stinger': stinger, 'gulp': gulp, 'scribble': lambda: scribble(1.3),
    'scribbleLong': lambda: scribble(2.6), 'squish': squish, 'boing': boing, 'bubbles': lambda: bubbles(), 'munch': munch,
    'shrink': shrink, 'creak': creak, 'riser': riser, 'paper': paper, 'clank': clank, 'swipe': swipe, 'rec': rec, 'swim': swim,
    'clap': clap, 'thunk': thunk, 'buzz': buzz, 'rumble': rumble, 'thud': thud, 'puff': puff, 'sand': sand, 'skitter': skitter,
    'waves': waves, 'sonar': sonar,
}
cache = {}
N = int((DUR + 3) * SR)
L = np.zeros(N); R = np.zeros(N)
LEVEL = 0.32
for i, e in enumerate(meta["events"]):
    nm = e["name"]
    s = LIB[nm]() if nm in ('bubbles', 'skitter') else cache.setdefault(nm, LIB[nm]())
    st = int(e["t"] * SR); s = s[:N - st] * e["g"] * LEVEL
    pan = 0.5 + 0.25 * np.sin(i * 1.7)  # slight stereo variety
    L[st:st + len(s)] += s * np.sqrt(1 - pan) * 1.41
    R[st:st + len(s)] += s * np.sqrt(pan) * 1.41
# deep-water ambience bed (very low), no music
amb = lp(lp(rng.standard_normal(N), 180), 180)
amb = amb / np.max(np.abs(amb)) * 0.035
L += amb; R += amb
out = np.stack([L, R], 1)
pk = np.max(np.abs(out)); print("peak", pk)
if pk > 0.95: out *= 0.95 / pk
with wave.open(f"{work}/sfx.wav", 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("ok", len(meta["events"]), "events")
