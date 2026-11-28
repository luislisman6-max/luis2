"""Efectos de sonido sintetizados (sin música) para la serie de Arthur Morgan.
Lee <WORK>/sfx.json (tiempos exactos generados por el render) y escribe <WORK>/sfx.wav.
Uso: python3 sfx_rdr.py <WORK>"""
import json, sys, wave
import numpy as np

SR = 44100
rng = np.random.default_rng(1)
work = sys.argv[1]
meta = json.load(open(f"{work}/sfx.json"))
DUR = meta["dur"]


def t_(d): return np.arange(int(d * SR)) / SR
def expd(n, k): return np.exp(-np.arange(n) / SR * k)
def noise(d): return rng.standard_normal(int(d * SR))
def norm(x, p=1.0): return x / (np.max(np.abs(x)) + 1e-9) * p
def env(n, a=0.005, r=0.1):
    e = np.ones(n); na = max(1, int(a * SR)); nr = max(1, min(n - na, int(r * SR)))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e


def band(x, lo=0, hi=SR / 2):
    """filtro pasa-banda por FFT (suave en los bordes)"""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.ones_like(f)
    if lo > 0: m *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4)
    if hi < SR / 2: m *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * m, len(x))


def tone(f, d): return np.sin(2 * np.pi * f * t_(d))
def sweep(f0, f1, d):
    f = np.geomspace(f0, f1, int(d * SR)); return np.sin(2 * np.pi * np.cumsum(f) / SR)


def mixat(dst, src, at):
    i = int(at * SR); n = min(len(src), len(dst) - i)
    if n > 0: dst[i:i + n] += src[:n]
    return dst


# ---------------------------------------------------------------- sonidos
def whoosh(d=0.5):
    n = noise(d); x = np.zeros_like(n); seg = 6
    for k in range(seg):   # barrido de brillo: oscuro → brillante → oscuro
        a, b = k * len(n) // seg, (k + 1) * len(n) // seg
        hi = 600 + 3500 * np.sin(np.pi * (k + .5) / seg)
        x[a:b] = band(n, 200, hi)[a:b]
    return norm(x * np.hanning(len(x)), .8)
def pop():
    d = .1; return norm(sweep(900, 260, d) * expd(int(d * SR), 40), .8)
def thunk():   # sello de goma golpeando el papel
    d = .25; body = sweep(180, 60, d) * expd(int(d * SR), 18)
    slap = band(noise(d), 300, 3000) * expd(int(d * SR), 60)
    return norm(body + .6 * slap, .95)
def paper():
    d = .45; x = band(noise(d), 1500, 7000) * (np.abs(np.sin(t_(d) * 40)) ** 3) * env(int(d * SR), .01, .2)
    return norm(x, .6)
def pageflip():
    d = .6; t = t_(d); x = band(noise(d), 800, 6000) * np.exp(-((t - .25) / .12) ** 2)
    return norm(x + .3 * band(noise(d), 100, 600) * np.exp(-((t - .3) / .05) ** 2), .7)
def cash():
    out = np.zeros(int(.9 * SR))
    for i, f in enumerate([2637, 3520]): mixat(out, (tone(f, .6) + .3 * tone(f * 2.4, .6)) * expd(int(.6 * SR), 8), i * .08)
    mixat(out, band(noise(.05), 2000, 8000) * expd(int(.05 * SR), 80), 0)
    return norm(out, .6)
def coins():
    out = np.zeros(int(1.0 * SR))
    for i in range(7):
        f = 2400 + rng.random() * 2200; mixat(out, (tone(f, .3) + .4 * tone(f * 1.5, .3)) * expd(int(.3 * SR), 18), i * .07 + rng.random() * .03)
    return norm(out, .6)
def clink():
    d = .8; x = (tone(1900, d) + .6 * tone(2860, d) + .3 * tone(4100, d)) * expd(int(d * SR), 9)
    return norm(x * env(len(x), .001, .1), .6)
def gunshot():
    d = 1.6; t = t_(d)
    crack = band(noise(d), 800, 9000) * expd(int(d * SR), 45)
    boom = band(noise(d), 40, 400) * expd(int(d * SR), 6)
    tail = band(noise(d), 200, 2000) * np.exp(-t * 3) * .25          # eco del desierto
    return norm(crack * 1.2 + boom * 1.4 + tail, .95)
def gunCock():
    out = np.zeros(int(.5 * SR))
    for at, f in [(0, 2500), (.16, 1800)]: mixat(out, band(noise(.04), f, f * 3) * expd(int(.04 * SR), 90), at)
    return norm(out, .7)
def cough():
    out = np.zeros(int(1.3 * SR))
    for i, at in enumerate([0, .34, .62]):
        d = .28; t = t_(d); x = band(noise(d), 150, 1800 - i * 300) * np.exp(-t * 11) * (1 - np.exp(-t * 300))
        x += .25 * np.sin(2 * np.pi * (140 - i * 10) * t) * np.exp(-t * 14)
        mixat(out, x * (1 - .18 * i), at)
    return norm(out, .85)
def buzz():
    d = .45; t = t_(d); x = np.sign(np.sin(2 * np.pi * 110 * t)) * .6 + np.sin(2 * np.pi * 220 * t) * .4
    return norm(band(x, 80, 2500) * env(len(t), .005, .08), .55)
def stinger():   # golpe cinematográfico grave + metal
    d = 2.2; t = t_(d)
    hit = band(noise(d), 30, 300) * np.exp(-t * 5) * 1.4
    sub = np.sin(2 * np.pi * 48 * t) * np.exp(-t * 2.5)
    metal = (tone(311, d) + .7 * tone(466, d) + .5 * tone(622 * 1.01, d)) * np.exp(-t * 2.2) * .35
    return norm(hit + sub + metal, .95)
def boom():
    d = 2.0; t = t_(d); return norm(np.sin(2 * np.pi * 45 * t) * np.exp(-t * 2.5) + band(noise(d), 30, 250) * np.exp(-t * 4), .9)
def gallop(d=2.6):
    out = np.zeros(int(d * SR)); beat = .36
    for k in range(int(d / beat)):
        for j, off in enumerate([0, .07, .15]):
            h = band(noise(.08), 60, 700) * expd(int(.08 * SR), 45); mixat(out, h * (1 - .2 * j), k * beat + off)
    return norm(out * env(len(out), .3, .8), .7)
def crackle(d=7.0):
    out = band(noise(d), 100, 900) * .12
    for _ in range(int(d * 14)): mixat(out, band(noise(.02), 1500, 7000) * expd(int(.02 * SR), 150) * rng.random(), rng.random() * d)
    return norm(out * env(len(out), .5, 1.5), .4)
def puff():
    d = .5; return norm(band(noise(d), 200, 2500) * np.exp(-((t_(d) - .12) / .08) ** 2), .5)
def squish():
    d = .3; t = t_(d); return norm(band(noise(d), 100, 900) * np.exp(-t * 12) + .4 * sweep(300, 120, d) * np.exp(-t * 10), .55)
def sparkle():
    out = np.zeros(int(.9 * SR))
    for i, f in enumerate([2093, 2637, 3136, 4186]): mixat(out, tone(f, .5) * expd(int(.5 * SR), 9), i * .07)
    return norm(out, .5)
def shimmer(down=False):
    d = 1.3; t = t_(d); fs = [523, 659, 784, 1046]
    out = sum(np.sin(2 * np.pi * f * (1 - (.25 * t / d if down else 0)) * t) for f in fs) * .3
    e = np.minimum(t / .1, 1) * np.exp(-t * 2.5); return norm(out * e, .55)
def bell():   # campana lejana (luto)
    d = 3.2; t = t_(d); x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, a, k in
                               [(220, 1, 1.1), (440 * 1.003, .6, 1.6), (660 * .997, .4, 2.2), (563, .3, 1.8)])
    return norm(x * env(len(t), .003, .5), .75)
def blow():   # se apaga la vela
    d = .5; return norm(band(noise(d), 300, 3000) * np.exp(-((t_(d) - .15) / .1) ** 2), .55)
def hiccup():
    d = .2; t = t_(d); return norm(sweep(500, 900, d) * np.exp(-t * 20) + band(noise(d), 400, 2000) * np.exp(-t * 40) * .4, .5)
def camera():
    out = np.zeros(int(.4 * SR)); mixat(out, band(noise(.03), 2000, 8000) * expd(int(.03 * SR), 100), 0)
    mixat(out, band(noise(.05), 800, 5000) * expd(int(.05 * SR), 70), .09); return norm(out, .6)
def wind(d=5.0):
    n = noise(d); t = t_(d); x = band(n, 200, 900) * (.6 + .4 * np.sin(2 * np.pi * .3 * t))
    return norm(x * env(len(t), 1.0, 1.5), .35)
def scribble(d=2.6):
    t = t_(d); x = band(noise(d), 1500, 6000) * (.5 + .5 * np.sign(np.sin(2 * np.pi * 7 * t + 2 * np.sin(t * 3))))
    return norm(x * env(len(t), .02, .2), .35)
def steps():
    out = np.zeros(int(2.0 * SR))
    for k in range(5): mixat(out, band(noise(.06), 80, 1200) * expd(int(.06 * SR), 50), k * .38)
    return norm(out, .55)


# ---------------------------------------------------------------- partes 2-5
def punch():
    d = .35; t = t_(d); return norm(band(noise(d), 60, 900) * np.exp(-t * 22) * 1.3 + sweep(160, 50, d) * np.exp(-t * 14), .95)
def laugh():   # risas graves "ja ja ja"
    out = np.zeros(int(1.4 * SR))
    for i in range(5):
        d = .16; t = t_(d); f = 140 - i * 6; v = (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 2 * t) + .3 * np.sin(2 * np.pi * f * 3 * t))
        mixat(out, band(v + .4 * noise(d), 100, 2500) * np.sin(np.pi * t / d), i * .22)
    return norm(out, .6)
def glass():
    out = np.zeros(int(.8 * SR))
    for i in range(9): f = 2500 + rng.random() * 4500; mixat(out, tone(f, .25) * expd(int(.25 * SR), 20), rng.random() * .15)
    mixat(out, band(noise(.2), 2000, 9000) * expd(int(.2 * SR), 25), 0); return norm(out, .55)
def cards():
    out = np.zeros(int(.6 * SR))
    for i in range(6): mixat(out, band(noise(.03), 1500, 6000) * expd(int(.03 * SR), 120), i * .06)
    return norm(out, .55)
def chalk(d=.9):
    t = t_(d); x = band(noise(d), 2500, 7000) * (.4 + .6 * (np.sin(2 * np.pi * 5 * t) > 0)); return norm(x * env(len(t), .01, .1), .35)
def riser():
    d = 1.2; t = t_(d); return norm((band(noise(d), 300, 5000) * .5 + sweep(200, 900, d) * .4) * (t / d) ** 2, .6)
def anger():
    d = .4; t = t_(d); return norm(np.sign(np.sin(2 * np.pi * 90 * t)) * np.exp(-t * 6) * .6 + sweep(600, 300, d) * .4 * np.exp(-t * 5), .5)
def scribble1(): return scribble(1.0)
def heartbeat():
    out = np.zeros(int(1.6 * SR))
    for at in (0, .28, .8, 1.08): d = .15; t = t_(d); mixat(out, np.sin(2 * np.pi * 55 * t) * np.exp(-t * 25), at)
    return norm(out, .8)
def door():
    d = 1.0; t = t_(d); f = 300 + 120 * np.sin(2 * np.pi * 1.3 * t); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * band(noise(d), 200, 3000) * .5
    return norm(x * env(len(t), .05, .3), .5)
def heartbreak():
    out = np.zeros(int(1.4 * SR)); mixat(out, band(noise(.08), 1000, 6000) * expd(int(.08 * SR), 40), 0)
    mixat(out, (tone(392, 1.2) + tone(370, 1.2)) * expd(int(1.2 * SR), 2.5) * .5, .05); return norm(out, .6)
def deflate():
    d = .6; return norm(sweep(700, 150, d) * np.exp(-t_(d) * 3) * .6 + band(noise(d), 500, 2000) * .2, .5)
def trainHorn():
    d = 1.8; t = t_(d); x = sum(np.sin(2 * np.pi * f * t) for f in (311, 370, 466)) * env(len(t), .1, .5); return norm(band(x, 100, 3000), .5)
def telegraph():
    out = np.zeros(int(1.2 * SR))
    for i, dd in enumerate([.06, .06, .18, .06, .18]): mixat(out, np.sin(2 * np.pi * 800 * t_(dd)) * env(int(dd * SR), .002, .01), i * .2)
    return norm(out, .4)
def gunfight():
    out = np.zeros(int(3.2 * SR)); g = gunshot()
    for i in range(9): mixat(out, g * (.4 + rng.random() * .6), i * .32 + rng.random() * .12)
    return norm(out, .9)
def scream():
    d = .9; t = t_(d); f = 700 + 300 * np.sin(2 * np.pi * 5 * t) * np.exp(-t * 2); v = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return norm(band(v + .3 * noise(d), 300, 4000) * env(len(t), .05, .4) * .5, .45)
def rain(d=6.0):
    x = band(noise(d), 1500, 8000) * .4
    for _ in range(int(d * 40)): mixat(x, band(noise(.01), 2000, 8000) * expd(int(.01 * SR), 200) * rng.random(), rng.random() * d)
    return norm(x * env(len(x), .5, 1.5), .35)
def blizzard(d=5.0):
    t = t_(d); x = band(noise(d), 300, 3000) * (.6 + .4 * np.sin(2 * np.pi * .5 * t)); return norm(x * env(len(t), .6, 1.5), .5)
def growl():
    d = 1.6; t = t_(d); x = band(noise(d), 60, 500) * (1 + np.sin(2 * np.pi * 28 * t)) * env(len(t), .2, .5); return norm(x, .7)
def howl():
    d = 2.4; t = t_(d); f = 450 + 250 * np.sin(np.pi * t / d); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d)
    return norm(x + .1 * band(noise(d), 400, 2000), .4)
def snowSteps():
    out = np.zeros(int(4.0 * SR))
    for k in range(9): mixat(out, band(noise(.12), 800, 5000) * np.hanning(int(.12 * SR)), k * .42)
    return norm(out, .4)
def ding(): return norm((tone(1568, 1.0) + .5 * tone(3136, 1.0)) * expd(int(SR), 5), .55)
def wipe():
    d = .4; return norm(band(noise(d), 1500, 6000) * np.hanning(int(d * SR)), .35)
def horse():
    d = 1.0; t = t_(d); f = 400 + 300 * np.abs(np.sin(2 * np.pi * 6 * t)) * np.exp(-t * 2); return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .05, .3) * .6 + band(noise(d), 300, 2000) * .2, .45)
def city(d=5.0):
    x = band(noise(d), 150, 1200) * .3
    for _ in range(14): mixat(x, gallop(1.0) * .15, rng.random() * (d - 1))
    return norm(x * env(len(x), .5, 1.2), .3)
def tramBell(): return norm(sum(tone(f, 1.0) * expd(int(SR), 5) for f in (1318, 1760)) + np.roll(sum(tone(f, 1.0) * expd(int(SR), 5) for f in (1318, 1760)), int(.25 * SR)), .45)
def whistle():
    d = 1.0; t = t_(d); f = 2800 + 200 * np.sign(np.sin(2 * np.pi * 14 * t)); return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .02, .1), .4)
def thunder():
    d = 3.0; t = t_(d); return norm(band(noise(d), 30, 400) * np.exp(-t * 1.2) * (1 + .5 * np.sin(2 * np.pi * 3 * t)), .9)
def seagull():
    out = np.zeros(int(1.4 * SR))
    for at in (0, .4): d = .3; t = t_(d); f = 1800 - 600 * t / d; mixat(out, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d), at)
    return norm(out, .35)
def waves(d=6.0):
    t = t_(d); return norm(band(noise(d), 200, 2000) * (.5 + .5 * np.sin(2 * np.pi * .35 * t) ** 2) * env(len(t), 1.0, 2.0), .4)
def breath():
    d = 1.4; t = t_(d); return norm(band(noise(d), 300, 3000) * (np.sin(np.pi * t / .6) ** 2 * (t < .6) + .6 * np.sin(np.pi * (t - .7) / .7) ** 2 * (t > .7)), .45)
def clock():
    out = np.zeros(int(2.0 * SR))
    for i in range(4): mixat(out, band(noise(.02), 2000, 6000) * expd(int(.02 * SR), 150), i * .5)
    return norm(out, .45)
def jail():
    out = np.zeros(int(1.2 * SR)); mixat(out, (tone(220, 1.0) + .6 * tone(331, 1.0) + .4 * tone(587, 1.0)) * expd(int(SR), 5), 0)
    mixat(out, band(noise(.1), 400, 4000) * expd(int(.1 * SR), 30), 0); return norm(out, .6)
def rip():
    d = .6; return norm(band(noise(d), 1000, 7000) * (np.abs(np.sin(t_(d) * 90)) ** 4) * env(int(d * SR), .01, .2), .55)
def whisper():
    d = 1.6; t = t_(d); return norm(band(noise(d), 2000, 8000) * (.5 + .5 * np.sin(2 * np.pi * 4 * t)) * env(len(t), .1, .4), .3)
def squeak():
    out = np.zeros(int(.6 * SR))
    for at in (0, .2): d = .12; mixat(out, sweep(3000, 4200, d) * np.hanning(int(d * SR)), at)
    return norm(out, .4)
def siren():
    d = 3.0; t = t_(d); f = 700 + 250 * np.sin(2 * np.pi * .8 * t); return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .5, 1.0), .3)
def tick(): return norm(band(noise(.02), 2000, 6000) * expd(int(.02 * SR), 150), .45)
def chime(): return norm(sum(tone(f, 1.6) * expd(int(1.6 * SR), 3) * a for f, a in [(1046, 1), (1318, .7), (1568, .5)]), .4)
def thud():
    d = .4; t = t_(d); return norm(band(noise(d), 40, 400) * np.exp(-t * 14) + np.sin(2 * np.pi * 60 * t) * np.exp(-t * 12), .8)
def silence(): return np.zeros(int(.1 * SR)) + 1e-6


LIB = {'whoosh': whoosh, 'pop': pop, 'thunk': thunk, 'paper': paper, 'pageflip': pageflip, 'cash': cash, 'coins': coins,
       'clink': clink, 'gunshot': gunshot, 'gunCock': gunCock, 'cough': cough, 'buzz': buzz, 'stinger': stinger, 'boom': boom,
       'gallop': gallop, 'crackle': crackle, 'puff': puff, 'squish': squish, 'sparkle': sparkle, 'shimmer': shimmer,
       'shimmerDown': lambda: shimmer(True), 'bell': bell, 'blow': blow, 'hiccup': hiccup, 'camera': camera, 'wind': wind,
       'scribbleLong': scribble, 'steps': steps,
       'punch': punch, 'laugh': laugh, 'glass': glass, 'cards': cards, 'chalk': chalk, 'riser': riser, 'anger': anger,
       'scribble': scribble1, 'heartbeat': heartbeat, 'door': door, 'heartbreak': heartbreak, 'shimmerBig': lambda: shimmer(False),
       'deflate': deflate, 'trainHorn': trainHorn, 'telegraph': telegraph, 'gunfight': gunfight, 'scream': scream, 'rain': rain,
       'blizzard': blizzard, 'growl': growl, 'howl': howl, 'snowSteps': snowSteps, 'ding': ding, 'wipe': wipe, 'horse': horse,
       'city': city, 'tramBell': tramBell, 'whistle': whistle, 'thunder': thunder, 'seagull': seagull, 'waves': waves,
       'breath': breath, 'clock': clock, 'jail': jail, 'rip': rip, 'whisper': whisper, 'squeak': squeak, 'siren': siren,
       'tick': tick, 'chime': chime, 'thud': thud, 'silence': silence}

N = int((DUR + 3) * SR)
L = np.zeros(N); R = np.zeros(N); cache = {}
for i, e in enumerate(meta["events"]):
    s = cache.setdefault(e["name"], LIB[e["name"]]()) * e["g"]
    pan = .5 + .2 * np.sin(i * 1.7)
    mixat(L, s * np.sqrt(1 - pan) * 1.41, e["t"]); mixat(R, s * np.sqrt(pan) * 1.41, e["t"])
out = np.stack([L, R], 1); pk = np.max(np.abs(out))
if pk > .95: out *= .95 / pk
with wave.open(f"{work}/sfx.wav", 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
print('sfx ok', len(meta["events"]), 'eventos, pico', round(float(pk), 2))
