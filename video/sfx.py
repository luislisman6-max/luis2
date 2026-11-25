"""Efectos de sonido sintetizados y mezcla con la voz (voz siempre por encima, sin música)."""
import json, os, sys, subprocess
import numpy as np
from scipy import signal

SR = 48000
rng = np.random.default_rng(1)


def env(n, a=0.005, r=0.1):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr) ** 2
    return e


def bp(x, lo, hi, order=2):
    b, a = signal.butter(order, [lo / (SR / 2), hi / (SR / 2)], 'band')
    return signal.lfilter(b, a, x)


def lp(x, f, order=2):
    b, a = signal.butter(order, f / (SR / 2), 'low'); return signal.lfilter(b, a, x)


def sweep(f0, f1, dur, kind='sin'):
    n = int(dur * SR); f = np.geomspace(f0, f1, n); ph = 2 * np.pi * np.cumsum(f) / SR
    if kind == 'sin': return np.sin(ph)
    if kind == 'saw': return 2 * ((ph / (2 * np.pi)) % 1) - 1
    if kind == 'sq': return np.sign(np.sin(ph)) * 0.6


def norm(x, peak=1.0):
    m = np.max(np.abs(x)) + 1e-9
    return x / m * peak


def whoosh(dur=0.35, up=True):
    n = int(dur * SR); x = rng.normal(0, 1, n)
    f = np.geomspace(300, 3000, n) if up else np.geomspace(3000, 300, n)
    out = np.zeros(n); blk = 512
    for i in range(0, n, blk):
        seg = x[max(0, i - 2048):i + blk]
        y = bp(seg, f[i] * 0.6, min(f[i] * 1.6, 20000))
        out[i:i + blk] = y[-len(x[i:i + blk]):]
    e = np.sin(np.linspace(0, np.pi, n)) ** 1.5
    return norm(out * e)


def pop_():
    x = sweep(900, 250, 0.07) * env(int(0.07 * SR), 0.001, 0.05); return norm(x)


def bloop():
    x = sweep(220, 900, 0.14) * env(int(0.14 * SR), 0.004, 0.06); return norm(x)


def click():
    n = int(0.02 * SR); x = rng.normal(0, 1, n) * np.exp(-np.linspace(0, 12, n)); return norm(bp(x, 1500, 6000))


def beep(f=1200, dur=0.09):
    n = int(dur * SR); t = np.arange(n) / SR
    return norm(np.sin(2 * np.pi * f * t) * env(n, 0.003, 0.03))


def scan(dur=0.9):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sweep(500, 1800, dur) * (0.6 + 0.4 * np.sin(2 * np.pi * 14 * t))
    return norm(x * env(n, 0.05, 0.2))


def ding():
    n = int(0.6 * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t) * a for f, a in ((1320, 1), (1980, .5), (2640, .25)))
    return norm(x * np.exp(-t * 7))


def buzz():
    n = int(0.22 * SR); t = np.arange(n) / SR
    x = lp(np.sign(np.sin(2 * np.pi * 140 * t)), 1500) * env(n, 0.005, 0.05)
    return norm(x)


def prrt(dur=0.45):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 95 + 25 * np.sin(2 * np.pi * 3 * t) + rng.normal(0, 6, n).cumsum() / 300
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = 2 * ((ph / (2 * np.pi)) % 1) - 1
    am = 0.55 + 0.45 * np.sign(np.sin(2 * np.pi * 26 * t))
    x = lp(x * am, 900) + 0.15 * lp(rng.normal(0, 1, n), 600)
    return norm(x * env(n, 0.01, 0.12))


def squeeze():
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = np.geomspace(380, 140, n) * (1 + 0.06 * np.sin(2 * np.pi * 30 * t))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return norm(lp(x + 0.3 * np.sign(x), 2500) * env(n, 0.01, 0.1))


def boing():
    n = int(0.3 * SR); t = np.arange(n) / SR
    f = 180 * (1 + 0.35 * np.exp(-t * 12) * np.sin(2 * np.pi * 18 * t))
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10))


def glu():
    a = sweep(500, 160, 0.09) * env(int(0.09 * SR), 0.003, 0.03)
    b = sweep(420, 120, 0.12) * env(int(0.12 * SR), 0.003, 0.05)
    return norm(np.concatenate([a, np.zeros(int(0.04 * SR)), b]))


def growl(dur=0.9):
    n = int(dur * SR); t = np.arange(n) / SR
    x = bp(rng.normal(0, 1, n), 60, 260) * (0.5 + 0.5 * np.sin(2 * np.pi * 7 * t + np.sin(2 * np.pi * 1.3 * t) * 3))
    x += 0.4 * np.sin(2 * np.pi * np.cumsum(70 + 20 * np.sin(2 * np.pi * 2 * t)) / SR)
    return norm(x * env(n, 0.08, 0.25))


def inflate(dur=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    x = bp(rng.normal(0, 1, n), 800, 5000) * 0.5 + 0.5 * sweep(180, 700, dur)
    return norm(x * env(n, 0.05, 0.1) * np.linspace(0.5, 1, n))


def exhale(dur=0.8):
    n = int(dur * SR)
    x = bp(rng.normal(0, 1, n), 400, 3000)
    e = np.sin(np.linspace(0, np.pi, n)) ** 1.2
    return norm(x * e)


def thump():
    n = int(0.25 * SR); t = np.arange(n) / SR
    return norm(np.sin(2 * np.pi * np.cumsum(np.geomspace(110, 45, n)) / SR) * np.exp(-t * 16))


def snore(dur=1.2):
    n = int(dur * SR); t = np.arange(n) / SR
    x = bp(rng.normal(0, 1, n), 80, 500) * (0.5 + 0.5 * np.sin(2 * np.pi * 28 * t))
    return norm(x * np.sin(np.linspace(0, np.pi, n)) ** 2)


def tick():
    n = int(0.03 * SR); t = np.arange(n) / SR
    return norm(np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 160))


def impact():
    n = int(0.45 * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * np.cumsum(np.geomspace(140, 40, n)) / SR) * np.exp(-t * 7)
    x += 0.5 * bp(rng.normal(0, 1, n), 1000, 6000) * np.exp(-t * 30)
    return norm(x)


def sparkle():
    n = int(0.5 * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for k, f in enumerate((2093, 2637, 3136, 4186)):
        s = int(k * 0.06 * SR); tt = t[: n - s]
        x[s:] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 12)
    return norm(x)


def chomp():
    n = int(0.08 * SR)
    x = bp(rng.normal(0, 1, n), 200, 1600) * np.exp(-np.linspace(0, 9, n))
    return norm(x)


def glitch():
    n = int(0.22 * SR); t = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * 60 * t)) * (rng.random(n) > 0.4) + 0.5 * rng.normal(0, 1, n)
    x = x * (np.sign(np.sin(2 * np.pi * 25 * t)) > 0)
    return norm(lp(x, 4000) * env(n, 0.002, 0.04))


# -------- lista de eventos: (tiempo, sonido, ganancia dB) --------
def events():
    E = []
    add = lambda t, s, g=0: E.append((t, s, g))
    # A hook
    add(0.38, bloop(), -2); add(0.92, squeeze(), -4); add(0.92, pop_(), -6); add(1.60, tick(), -8)
    add(3.10, whoosh(0.4), -4); add(3.55, exhale(0.6), -6)
    # cortes
    for c in (4.20, 7.00, 12.85, 20.85, 26.95, 38.85, 45.40, 52.90, 60.60, 65.45, 73.90, 79.95, 87.25, 91.80):
        add(c - 0.16, whoosh(0.32), -9)
    # B
    add(4.25, whoosh(0.5, False), -6); add(6.24, pop_(), -6)
    # C
    add(7.06, glitch(), -6); add(8.04, bloop(), -5); add(9.90, whoosh(0.25, False), -9); add(10.05, buzz(), -8)
    add(11.00, sweep(300, 900, 0.4) * env(int(0.4 * SR), 0.05, 0.2), -14); add(11.36, whoosh(0.6), -6)
    add(11.98, pop_(), -3); add(12.0, ding(), -9); add(12.0, exhale(0.5), -8)
    # D
    add(12.92, impact(), -8)
    for tb in (15.08, 15.40, 15.96, 16.10): add(tb, pop_(), -5)
    for k in range(10): add(16.80 + k * 0.13, chomp(), -7)
    for i in range(4): add(19.44 + i * 0.15, bloop(), -4)
    # E
    add(21.92, pop_(), -6); add(23.04, impact(), -5)
    for k in range(8): add(23.42 + k * 0.035, tick(), -9)
    add(23.70, impact(), -4); add(23.72, ding(), -10); add(24.06, pop_(), -6)
    add(24.88, prrt(0.38), -3); add(25.28, pop_(), -5)
    # F sensor
    add(27.90, whoosh(0.9, True), -8); add(29.30, thump(), -3); add(30.48, sparkle(), -8)
    add(32.10, scan(1.0), -10); add(32.60, pop_(), -7); add(33.78, beep(1500), -9); add(33.92, beep(1500), -9)
    add(34.32, beep(900, 0.06), -10); add(34.42, beep(1200, 0.06), -10); add(34.52, beep(1600, 0.06), -10)
    add(35.10, ding(), -6); add(36.10, buzz(), -8); add(37.46, sparkle(), -9)
    # G
    add(39.42, squeeze(), -3); add(39.45, beep(1500), -10); add(40.90, boing(), -4); add(41.50, boing(), -4)
    add(42.98, whoosh(0.6, False), -5); add(44.30, glu(), -2)
    # H
    add(46.05, inflate(1.05), -6); add(48.05, growl(1.0), -5); add(49.50, growl(0.9), -5)
    add(50.72, pop_(), -4); add(50.95, click(), -6); add(52.44, sparkle(), -9)
    # J
    for tb in (53.60, 53.72, 53.84, 53.96): add(tb, pop_(), -10)
    add(55.60, thump(), -4); add(56.30, thump(), -5); add(57.20, whoosh(0.8, False), -9); add(59.76, thump(), -3)
    # K
    add(60.80, whoosh(1.1), -9); add(61.90, pop_(), -5); add(64.20, exhale(0.9), -5)
    # L
    add(65.50, whoosh(0.5, False), -6); add(67.96, pop_(), -6); add(69.34, exhale(1.0), -5)
    add(69.96, beep(1000), -7); add(71.40, sweep(400, 1200, 0.5) * env(int(.5 * SR), .01, .1), -12)
    add(71.80, sweep(400, 1000, 0.5) * env(int(.5 * SR), .01, .1), -12); add(72.74, pop_(), -5)
    # M
    add(73.96, sparkle(), -10); add(74.32, pop_(), -7); add(77.46, ding(), -5)
    add(78.74, pop_(), -7); add(79.35, boing(), -4)
    # N
    add(80.10, snore(1.2), -10); add(81.60, snore(1.2), -12); add(83.84, bloop(), -5); add(86.80, prrt(0.5), -2)
    # O
    add(88.34, bloop(), -6); add(89.06, buzz(), -10); add(90.32, buzz(), -8); add(90.74, whoosh(0.5), -6)
    add(91.30, pop_(), -5); add(91.32, ding(), -8)
    # P
    add(91.90, whoosh(0.7), -5); add(92.66, ding(), -8); add(94.70, tick(), -8); add(96.20, bloop(), -3)
    return E


def main(voice_in, out_wav):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', voice_in, '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'], capture_output=True).stdout
    voice = np.frombuffer(raw, np.float32).astype(np.float64)
    n = len(voice)
    sfx = np.zeros(n + SR)
    for t, s, g in events():
        i = int(t * SR); s = s[: len(sfx) - i]
        sfx[i:i + len(s)] += s * 10 ** (g / 20)
    sfx = sfx[:n]
    # voz normalizada; efectos ~13 dB por debajo y con «ducking» cuando hay voz
    voice = voice / (np.max(np.abs(voice)) + 1e-9) * 0.89
    venv = np.abs(signal.hilbert(lp(voice, 40))) if False else None
    rms = np.sqrt(np.convolve(voice ** 2, np.ones(int(0.05 * SR)) / int(0.05 * SR), 'same'))
    rms = lp(rms, 8)
    duck = 1 - 0.5 * np.clip(rms / 0.08, 0, 1)
    sfx = sfx * 0.22 * duck
    mix = voice + sfx
    mix = mix / max(1.0, np.max(np.abs(mix)) / 0.97)
    st = np.stack([mix, mix], 1)
    pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
    import wave
    with wave.open(out_wav, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    v_rms = np.sqrt(np.mean(voice[np.abs(voice) > 0.02] ** 2)); s_rms = np.sqrt(np.mean(sfx[np.abs(sfx) > 0.005] ** 2))
    print('voz RMS %.3f | efectos RMS %.3f | diferencia %.1f dB' % (v_rms, s_rms, 20 * np.log10(v_rms / s_rms)))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
