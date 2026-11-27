"""Efectos de sonido sintetizados + música de fondo + mezcla con la voz.
Uso: python sfx.py  (lee cues.json y voz.mp3) -> mix.wav  — versión SAW
"""
import json, os, subprocess, wave
import numpy as np

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(7)

def t(d): return np.arange(int(SR * d)) / SR
def env(n, a=0.005, r=None, curve=4.0):
    x = np.linspace(0, 1, n)
    e = np.exp(-curve * x) if r is None else np.clip(1 - x / r, 0, 1)
    at = max(1, int(SR * a))
    e[:at] *= np.linspace(0, 1, at)
    return e
def noise(d): return rng.standard_normal(int(SR * d))
def lp(x, k):  # pasa-bajos simple (k 0..1)
    y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)):
        acc += k * (x[i] - acc); y[i] = acc
    return y
def lp_fast(x, cutoff):
    # filtro por FFT (rápido)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))
def hp_fast(x, cutoff):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 - 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))
def sweep(f0, f1, d, wave="sine"):
    tt = t(d); f = np.geomspace(f0, f1, len(tt)); ph = 2 * np.pi * np.cumsum(f) / SR
    if wave == "saw": return 2 * ((ph / (2 * np.pi)) % 1) - 1
    if wave == "sq": return np.sign(np.sin(ph))
    return np.sin(ph)
def norm(x, peak=0.9): return x / (np.max(np.abs(x)) + 1e-9) * peak

def whoosh(d=0.45):
    n = noise(d); x = np.zeros_like(n)
    # barrido de filtro: mezcla de bandas
    lo, hi = lp_fast(n, 600), hp_fast(lp_fast(n, 4000), 800)
    k = np.sin(np.linspace(0, np.pi, len(n))) ** 2
    x = lo * (1 - k) + hi * k
    return norm(x * np.sin(np.linspace(0, np.pi, len(n))) ** 1.5, 0.6)
def impact(d=0.7):
    body = sweep(140, 38, d) * env(int(SR * d), curve=6)
    crack = hp_fast(noise(0.08), 1500) * env(int(SR * 0.08), curve=30)
    x = body.copy(); x[:len(crack)] += crack * 0.6
    return norm(np.tanh(x * 2.2), 0.95)
def boom(d=1.8):
    b = sweep(90, 28, d) * env(int(SR * d), curve=3)
    n = lp_fast(noise(d), 300) * env(int(SR * d), curve=4) * 2
    c = hp_fast(noise(0.12), 1200) * env(int(SR * 0.12), curve=20)
    x = b + n; x[:len(c)] += c
    return norm(np.tanh(x * 2), 0.98)
def pop():
    return norm(sweep(500, 1400, 0.09) * env(int(SR * 0.09), curve=8), 0.55)
def ding():
    tt = t(0.9); x = sum(np.sin(2 * np.pi * f * tt) * a for f, a in ((1568, 1), (3136, .4), (4704, .15)))
    return norm(x * env(len(tt), curve=5), 0.5)
def sparkle():
    out = np.zeros(int(SR * 0.6))
    for i, f in enumerate((2093, 2637, 3136, 4186)):
        s = int(SR * 0.07 * i); tt = t(0.3)
        out[s:s + len(tt)] += np.sin(2 * np.pi * f * tt) * env(len(tt), curve=9)
    return norm(out, 0.4)
def zap(d=0.35):
    n = int(SR * d); f = 300 + 2500 * np.abs(rng.standard_normal(n // 200 + 1)).repeat(200)[:n]
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sign(np.sin(ph)) * 0.5 + hp_fast(noise(d), 2000) * 0.5
    return norm(x * env(n, curve=7), 0.5)
def powerup(d=2.8):
    x = sweep(80, 900, d, "saw") * 0.5 + sweep(160, 1800, d, "sine") * 0.3
    x = lp_fast(x, 3500) + hp_fast(noise(d), 3000) * np.linspace(0, .35, int(SR * d))
    e = np.linspace(0.15, 1, len(x)) ** 1.5; e[-int(SR * .05):] *= np.linspace(1, 0, int(SR * .05))
    return norm(x * e, 0.7)
def glass():
    x = np.zeros(int(SR * 0.9))
    for _ in range(40):
        s = int(rng.uniform(0, 0.35) * SR); d = rng.uniform(.03, .2); f = rng.uniform(2500, 7000)
        tt = t(d); x[s:s + len(tt)] += np.sin(2 * np.pi * f * tt) * env(len(tt), curve=12) * rng.uniform(.3, 1)
    c = hp_fast(noise(0.15), 2500) * env(int(SR * 0.15), curve=15)
    x[:len(c)] += c * 1.5
    return norm(x, 0.7)
def crack():
    c = hp_fast(noise(0.25), 900) * env(int(SR * 0.25), curve=14)
    b = sweep(200, 60, 0.25) * env(int(SR * 0.25), curve=10)
    return norm(c + b * .7, 0.8)
def beam(d=3.6):
    hum = sweep(110, 160, d, "saw") * 0.4 + sweep(220, 330, d) * 0.3
    hiss = hp_fast(lp_fast(noise(d), 6000), 500)
    wob = 1 + 0.25 * np.sin(2 * np.pi * 9 * t(d))
    x = (lp_fast(hum, 1500) + hiss * 0.6) * wob
    e = np.minimum(1, np.linspace(0, 6, len(x))) * np.linspace(0.6, 1, len(x)); e[-int(SR * .3):] *= np.linspace(1, 0, int(SR * .3))
    return norm(x * e, 0.75)
def rumble(d=2.2):
    x = lp_fast(noise(d), 120) * 3 + sweep(45, 35, d) * .5
    e = np.sin(np.linspace(0, np.pi, int(SR * d))) ** .7
    return norm(np.tanh(x) * e, 0.7)
def heartbeat():
    out = np.zeros(int(SR * 0.9))
    for s in (0, 0.28):
        th = sweep(70, 40, 0.18) * env(int(SR * 0.18), curve=9)
        i = int(SR * s); out[i:i + len(th)] += th
    return norm(out, 0.95)
def tick():
    return norm(hp_fast(noise(0.02), 3000) * env(int(SR * 0.02), curve=40), 0.45)
def riser(d=1.2):
    x = hp_fast(noise(d), 1500) * np.linspace(0, 1, int(SR * d)) ** 2 + sweep(200, 1200, d) * .2
    return norm(x, 0.5)
def bassdrop(d=2.0):
    x = sweep(70, 30, d) * env(int(SR * d), curve=2) + sweep(140, 60, d) * env(int(SR * d), curve=3) * .4
    return norm(np.tanh(x * 2.5), 0.95)
def slam():
    w = whoosh(0.25); i = impact(0.6)
    out = np.zeros(len(w) + len(i)); out[:len(w)] += w * .6; out[len(w) - 600:len(w) - 600 + len(i)] += i
    return norm(out, 0.95)
def thud():
    return norm(sweep(110, 45, 0.3) * env(int(SR * 0.3), curve=10) + lp_fast(noise(.3), 400) * env(int(SR * .3), curve=12), 0.85)
def shimmer(d=1.6):
    out = np.zeros(int(SR * d))
    for i, f in enumerate((523, 659, 784, 1047, 1319, 1568)):
        tt = t(d - 0.12 * i); s = int(SR * 0.12 * i)
        out[s:s + len(tt)] += np.sin(2 * np.pi * f * tt) * env(len(tt), curve=3) * .5
    return norm(out, 0.4)
def laugh():  # risa malvada estilizada (tres golpes graves)
    out = np.zeros(int(SR * 0.9))
    for k in range(3):
        tt = t(0.16); f = 170 - k * 12
        v = np.sign(np.sin(2 * np.pi * f * tt)) * env(len(tt), curve=5)
        i = int(SR * 0.22 * k); out[i:i + len(v)] += lp_fast(v, 900)
    return norm(out, 0.5)


# ---------------- efectos nuevos para SAW ----------------
def bp(x, lo, hi): return hp_fast(lp_fast(x, hi), lo)
def buzz(d=0.9):  # zumbido de tubo fluorescente
    tt = t(d); x = np.sign(np.sin(2 * np.pi * 120 * tt)) * .4 + np.sin(2 * np.pi * 240 * tt) * .3
    gate = (rng.random(int(d * 25) + 2) > .35).repeat(int(SR / 25) + 1)[:len(tt)]
    return norm(lp_fast(x, 2500) * gate * np.linspace(1, .6, len(tt)), .45)
def drone(d=4.0):
    tt = t(d); x = np.sin(2 * np.pi * 55 * tt) + np.sin(2 * np.pi * 82.4 * tt) * .5 + lp_fast(noise(d), 200) * .6
    e = np.minimum(1, np.linspace(0, 3, len(tt))) * np.minimum(1, np.linspace(4, 0, len(tt)))
    return norm(x * e, .6)
def chainfx(d=0.7):
    out = np.zeros(int(SR * d))
    for _ in range(14):
        s = int(rng.uniform(0, d - .08) * SR); tt = t(.06)
        f = rng.uniform(2500, 5500)
        out[s:s + len(tt)] += (np.sin(2 * np.pi * f * tt) + hp_fast(noise(.06), 3000) * .6) * env(len(tt), curve=25)
    return norm(out, .55)
def stinger(d=1.6):
    x = sweep(60, 30, d) * env(int(SR * d), curve=2.5) * 1.2
    hi = (np.sin(2 * np.pi * 740 * t(d)) + np.sin(2 * np.pi * 785 * t(d))) * env(int(SR * d), curve=3) * .25
    c = hp_fast(noise(.1), 1500) * env(int(SR * .1), curve=20)
    out = x + hi; out[:len(c)] += c
    return norm(np.tanh(out * 2), .95)
def splash(d=0.9):
    n = bp(noise(d), 300, 5000) * env(int(SR * d), curve=5)
    bl = np.zeros_like(n)
    for _ in range(10):
        s = int(rng.uniform(.05, .6) * SR); tt = t(.05)
        bl[s:s + len(tt)] += np.sin(2 * np.pi * np.geomspace(600, 1400, len(tt)) * tt) * env(len(tt), curve=12)
    return norm(n + bl * .4, .8)
def plug(): return norm(sweep(300, 900, .08) * env(int(SR * .08), curve=10), .6)
def gurgle(d=1.6):
    out = np.zeros(int(SR * d))
    for _ in range(26):
        s = int(rng.uniform(0, d - .12) * SR); dd = rng.uniform(.05, .12); tt = t(dd)
        f0 = rng.uniform(150, 400)
        out[s:s + len(tt)] += np.sin(2 * np.pi * np.cumsum(np.geomspace(f0, f0 * 2.2, len(tt))) / SR) * env(len(tt), curve=6)
    return norm(lp_fast(out + lp_fast(noise(d), 500) * .3, 1800), .6)
def drain(d=1.0): return norm(gurgle(d)[:int(SR * d)] + sweep(500, 120, d) * env(int(SR * d), curve=3) * .4, .6)
def glint():
    out = np.zeros(int(SR * .8))
    for i, f in enumerate((2637, 3520, 4186)):
        tt = t(.5); s = int(SR * .05 * i); out[s:s + len(tt)] += np.sin(2 * np.pi * f * tt) * env(len(tt), curve=7)
    return norm(out, .4)
def clickfx():
    out = np.zeros(int(SR * .2)); a = bp(noise(.03), 1500, 6000) * env(int(SR * .03), curve=30)
    out[:len(a)] += a; s = int(SR * .09); out[s:s + len(a)] += a * .7
    return norm(out, .7)
def tape(d=1.0):
    tt = t(d); x = lp_fast(noise(d), 3000) * .25 + np.sin(2 * np.pi * 60 * tt) * .2 + np.sin(2 * np.pi * 7 * tt) * lp_fast(noise(d), 800) * .2
    return norm(x * np.minimum(1, np.linspace(0, 10, len(tt))) * np.minimum(1, np.linspace(5, 0, len(tt))), .3)
def metal(d=1.2):
    tt = t(d); x = sum(np.sin(2 * np.pi * f * tt) * a for f, a in ((523, 1), (1187, .6), (1871, .4), (2730, .3)))
    x = x * env(len(tt), curve=5); x[:int(SR * .02)] += noise(.02) * .5
    return norm(x, .55)
def sawfx(d=1.0):
    out = np.zeros(int(SR * d)); per = .16
    for k in range(int(d / per)):
        s = int(k * per * SR); dd = per * .85
        n = bp(noise(dd), 1500, 7000) * np.sin(np.linspace(0, np.pi, int(SR * dd))) ** .6
        out[s:s + len(n)] += n * (1 if k % 2 else .75)
    return norm(out, .6)
def snap():
    c = hp_fast(noise(.06), 2000) * env(int(SR * .06), curve=30)
    r = metal(.8) * .6; out = np.zeros(len(r)); out[:len(c)] += c * 1.2; out += r
    return norm(out, .85)
def static(d=0.8): return norm(hp_fast(noise(d), 800) * (0.6 + .4 * (rng.random(int(SR * d)) > .5)) * np.minimum(1, np.linspace(5, 0, int(SR * d))), .45)
def pin(): return norm(sweep(900, 600, .05) * env(int(SR * .05), curve=15), .4)
def rain(d=2.4):
    x = bp(noise(d), 1200, 8000) * .5
    for _ in range(60):
        s = int(rng.uniform(0, d - .02) * SR); dd = .01; tt = t(dd)
        x[s:s + len(tt)] += noise(dd) * env(len(tt), curve=20) * 1.5
    e = np.minimum(1, np.linspace(0, 4, len(x))) * np.minimum(1, np.linspace(4, 0, len(x)))
    return norm(x * e, .3)
def shutter():
    out = np.zeros(int(SR * .25)); a = bp(noise(.025), 1000, 6000) * env(int(SR * .025), curve=25)
    out[:len(a)] += a; s = int(SR * .08); out[s:s + len(a)] += a * .8
    return norm(out, .65)
def creak(d=1.1):
    tt = t(d); f = 180 + 70 * np.sin(2 * np.pi * 1.3 * tt) + 30 * rng.standard_normal(len(tt)).cumsum() / np.sqrt(len(tt))
    ph = 2 * np.pi * np.cumsum(np.abs(f)) / SR
    x = np.sign(np.sin(ph)) * (rng.random(len(tt)) > .15)
    return norm(bp(x, 300, 2500) * np.sin(np.linspace(0, np.pi, len(tt))), .45)
def cock():
    out = np.zeros(int(SR * .3)); a = bp(noise(.02), 2000, 8000) * env(int(SR * .02), curve=25)
    out[:len(a)] += a; s = int(SR * .12); b = bp(noise(.03), 1200, 6000) * env(int(SR * .03), curve=25); out[s:s + len(b)] += b
    return norm(out, .7)
def ring(d=0.75):
    tt = t(d); x = (np.sin(2 * np.pi * 1400 * tt) + np.sin(2 * np.pi * 1750 * tt)) * (np.sin(2 * np.pi * 22 * tt) > 0)
    return norm(x * np.minimum(1, np.linspace(10, 0, len(tt))), .4)
def scream(d=1.3):
    tt = t(d); f = np.geomspace(500, 900, len(tt)) * (1 + .03 * np.sin(2 * np.pi * 7 * tt))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = (2 * ((ph / (2 * np.pi)) % 1) - 1) * .6 + np.sin(ph * 2) * .3 + bp(noise(d), 1500, 5000) * .25
    x = bp(x, 400, 4000) * np.minimum(1, np.linspace(0, 8, len(tt))) * np.linspace(1, 0, len(tt)) ** .5
    return norm(x, .45)
def drag(d=0.35): return norm(bp(noise(d), 200, 1500) * np.sin(np.linspace(0, np.pi, int(SR * d))), .45)
def gunshot():
    c = noise(.03) * env(int(SR * .03), curve=8)
    b = sweep(120, 40, .5) * env(int(SR * .5), curve=6)
    tail = lp_fast(noise(1.0), 1200) * env(int(SR * 1.0), curve=5) * .5
    out = np.zeros(int(SR * 1.0)); out[:len(c)] += c * 2; out[:len(b)] += b; out += tail
    return norm(np.tanh(out * 3), .98)
def step(): return norm(lp_fast(noise(.08), 600) * env(int(SR * .08), curve=14) + sweep(90, 50, .08) * env(int(SR * .08), curve=12), .5)
def hit():
    a = impact(.5); c = metal(.5) * .3; return norm(a + c[:len(a)], .95)
def reverse(d=1.0):
    x = stinger(d)[:int(SR * d)][::-1]
    return norm(x, .6)
def switch(): return norm(bp(noise(.02), 1500, 7000) * env(int(SR * .02), curve=20), .7)
def doorslam():
    b = boom(1.2); c = metal(.6) * .25; out = b.copy(); out[:len(c)] += c
    return norm(out, .98)

def blip(): return norm(sweep(700, 1100, .06) * env(int(SR * .06), curve=10), .45)
def tremble(d=0.9):
    tt = t(d); am = .5 + .5 * np.sign(np.sin(2 * np.pi * 18 * tt))
    x = bp(noise(d), 150, 1200) * am + chainfx(d)[:len(tt)] * .35
    return norm(x * np.sin(np.linspace(0, np.pi, len(tt))), .5)
def swish(d=0.35):
    n = noise(d); k = np.sin(np.linspace(0, np.pi, len(n)))
    return norm(bp(n, 500, 3500) * k ** 2, .5)
def swell(d=1.6):
    x = lp_fast(noise(d), 400) + sweep(50, 70, d) * .6
    return norm(x * np.sin(np.linspace(0, np.pi, int(SR * d))) ** 1.5, .5)
def thump(): return norm(np.tanh((sweep(90, 35, .45) * env(int(SR * .45), curve=7) + lp_fast(noise(.45), 250) * env(int(SR * .45), curve=9)) * 2.5), .95)
def drip():
    tt = t(.12); f = np.geomspace(900, 1900, len(tt))
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(tt), curve=14), .35)

GEN = dict(whoosh=whoosh, impact=impact, boom=boom, pop=pop, tick=tick, heartbeat=heartbeat, rumble=rumble, slam=slam, thud=thud,
           laugh=laugh, glass=glass, buzz=buzz, drone=drone, chain=chainfx, stinger=stinger, splash=splash, plug=plug, gurgle=gurgle,
           drain=drain, glint=glint, click=clickfx, tape=tape, metal=metal, saw=sawfx, snap=snap, static=static, pin=pin, rain=rain,
           shutter=shutter, creak=creak, cock=cock, ring=ring, scream=scream, drag=drag, gunshot=gunshot, step=step, hit=hit,
           reverse=reverse, switch=switch, doorslam=doorslam, blip=blip, tremble=tremble, swish=swish, swell=swell, thump=thump, drip=drip)

def music(total, mute=()):
    """Fondo de suspenso: pulso grave lento + pad disonante + tic de reloj."""
    n = int(SR * total); out = np.zeros(n); tt = np.arange(n) / SR
    pulse = sweep(70, 40, .35) * env(int(SR * .35), curve=8)
    beat = 60 / 72
    b = 0
    while b * beat < total:
        i = int(b * beat * SR); m = min(len(pulse), n - i)
        if m > 0: out[i:i + m] += pulse[:m] * (1 if b % 2 == 0 else .55)
        b += 1
    pad = (np.sin(2 * np.pi * 110 * tt) + np.sin(2 * np.pi * 116.5 * tt) * .8 + np.sin(2 * np.pi * 164.8 * tt) * .4) * .08
    pad *= .6 + .4 * np.sin(2 * np.pi * tt / 9)
    out += lp_fast(pad, 900) if n < SR * 300 else pad
    g = np.ones(n)
    for a, z in mute: g[int(a * SR):int(z * SR)] = 0
    g = np.convolve(g, np.ones(4000) / 4000, mode="same")
    return out * g

def load_voice():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(HERE, "voz.mp3"), "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

if __name__ == "__main__":
    cues = sorted(json.load(open(os.path.join(HERE, "cues.json"))))
    last, kept = {}, []
    for c in cues:  # quita repetidos del mismo efecto muy seguidos
        if c[0] - last.get(c[1], -9) >= .15: kept.append(c); last[c[1]] = c[0]
    cues = kept
    voice = load_voice(); total = 117.0
    n = int(SR * total)
    fx = np.zeros(n); cache = {}
    for tm, name, vol in cues:
        if name not in cache: cache[name] = GEN[name]()
        s = cache[name]; i = int(tm * SR)
        if i >= n: continue
        m = min(len(s), n - i); fx[i:i + m] += s[:m] * vol
    mus = music(total, mute=[(68.9, 72.1), (113.0, 117.0)])
    v = np.zeros(n); v[:len(voice)] = voice[:n]
    v = v / (np.max(np.abs(v)) + 1e-9) * 0.95
    envv = np.convolve(np.abs(v), np.ones(4410) / 4410, mode="same")
    duck = 1 - 0.5 * np.clip(envv / 0.08, 0, 1)
    mix = v * 0.95 + fx * 0.75 * (1 - .25 * np.clip(envv / 0.08, 0, 1)) + mus * 0.22 * duck
    mix = np.tanh(mix * 1.1) * 0.92
    st = np.stack([mix, mix], 1)
    with wave.open(os.path.join(HERE, "mix.wav"), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())
    print("mix.wav", round(total, 2), "s,", len(cues), "efectos")
