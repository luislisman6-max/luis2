"""Efectos sintetizados sincronizados con render_jvb.py y mezcla con la voz (voz por encima, sin música)."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from sfx import SR, env, bp, lp, sweep, norm, whoosh, thump, impact, tick, ding, glitch, main as _main
import sfx as base

rng = np.random.default_rng(7)


def noise(d): return rng.normal(0, 1, int(d * SR))


def punch(power=1.0):
    n = int(0.5 * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * np.cumsum(np.geomspace(160, 45, n)) / SR) * np.exp(-t * (9 / power))
    crack = bp(rng.normal(0, 1, n), 1200, 7000) * np.exp(-t * 45)
    return norm(body + 0.7 * crack)


def boom(d=1.6):
    n = int(d * SR); t = np.arange(n) / SR
    x = lp(rng.normal(0, 1, n), 300, 4) * np.exp(-t * 2.4) * 3
    x += np.sin(2 * np.pi * np.cumsum(np.geomspace(80, 28, n)) / SR) * np.exp(-t * 3)
    x += 0.4 * bp(rng.normal(0, 1, n), 1500, 6000) * np.exp(-t * 14)
    return norm(x)


def rumble(d=1.2):
    n = int(d * SR); x = lp(rng.normal(0, 1, n), 120, 4)
    return norm(x * np.sin(np.linspace(0, np.pi, n)) ** 0.8)


def power_up(d=1.2, f0=80, f1=420):
    n = int(d * SR); t = np.arange(n) / SR
    s = sweep(f0, f1, d, 'saw') * 0.5 + sweep(f0 * 2, f1 * 2, d, 'sin') * 0.3
    s = lp(s, 2500) + 0.35 * bp(rng.normal(0, 1, n), 300, 3000) * (t / d)
    return norm(s * env(n, d * 0.6, 0.12))


def crash(d=1.0):
    n = int(d * SR); x = np.zeros(n); t = np.arange(n) / SR
    for k in range(14):
        i = int(rng.uniform(0, 0.6) * SR); m = int(0.08 * SR)
        x[i:i + m] += bp(rng.normal(0, 1, m), rng.uniform(400, 3000), 7000)[:len(x[i:i + m])] * np.exp(-np.linspace(0, 6, m))[:len(x[i:i + m])]
    x += 1.5 * lp(rng.normal(0, 1, n), 400) * np.exp(-t * 5)
    return norm(x)


def rip(d=0.5):
    n = int(d * SR); t = np.arange(n) / SR
    x = bp(rng.normal(0, 1, n), 800, 6000) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 70 * t)))
    return norm(x * env(n, 0.005, 0.15))


def shatter(d=0.9):
    n = int(d * SR); t = np.arange(n) / SR
    x = bp(rng.normal(0, 1, n), 3000, 12000) * np.exp(-t * 7)
    for f in rng.uniform(2500, 6000, 7):
        s = int(rng.uniform(0, 0.3) * SR); tt = t[: n - s]
        x[s:] += 0.5 * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 18)
    return norm(x)


def zap(d=0.6):
    n = int(d * SR); t = np.arange(n) / SR
    f = 200 + 1800 * rng.random(n // 300 + 1).repeat(300)[:n]
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 + 0.5 * bp(rng.normal(0, 1, n), 2000, 8000)
    return norm(lp(x, 7000) * env(n, 0.003, 0.2))


def wind(d=2.5):
    n = int(d * SR); t = np.arange(n) / SR
    x = bp(rng.normal(0, 1, n), 250, 1200) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * t))
    return norm(x * np.sin(np.linspace(0, np.pi, n)) ** 1.5)


def bell():
    n = int(1.4 * SR); t = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * dcy) for f, a, dcy in ((880, 1, 2.5), (1320, .6, 3), (2200, .4, 4.5), (3100, .2, 6)))
    return norm(x)


def sting():
    n = int(0.9 * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * np.cumsum(np.geomspace(220, 55, n)) / SR) * np.exp(-t * 3.5)
    return norm(x + 0.3 * bp(rng.normal(0, 1, n), 2000, 8000) * np.exp(-t * 20))


def hum(d=2.0, f=60):
    n = int(d * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.01 * t) + 0.3 * bp(rng.normal(0, 1, n), 100, 900)
    return norm(x * env(n, 0.2, 0.4))


def events():
    E = []
    a = lambda t, s, g=0: E.append((t, s, g))
    # cortes de escena: whoosh suave justo antes de cada corte
    cuts = [2.72, 4.70, 7.10, 8.50, 9.45, 13.45, 15.85, 18.20, 24.62, 26.10, 27.70, 29.70, 32.92, 34.58, 38.00, 41.00,
            43.02, 45.00, 48.05, 50.60, 52.05, 54.50, 57.20, 58.18, 59.60, 61.22, 63.92, 67.42, 68.60, 69.88, 72.80,
            75.25, 81.00, 86.95, 88.12]
    for c in cuts:
        if c in (32.92,):   # «silencio»: sin efectos
            continue
        a(c - 0.12, whoosh(0.28), -12)
    # hook
    a(0.00, sting(), -6); a(2.00, punch(1.3), -2); a(2.00, rumble(0.6), -8)
    a(2.78, power_up(1.9, 60, 300), -9)
    for tt in (3.00, 3.48, 3.90): a(tt, thump(), -3)
    a(4.70, whoosh(0.25), -6); a(4.95, punch(1.5), 0); a(4.95, boom(1.2), -6); a(4.95, zap(0.3), -10)
    a(5.90, tick(), -10)
    a(7.18, sting(), -3); a(7.18, rumble(1.0), -10)
    a(8.54, bell(), -5)
    # ronda 1
    a(10.20, whoosh(0.32), -6); a(10.52, punch(1.0), -1); a(12.48, tick(), -12)
    a(15.90, hum(2.3, 55), -12); a(17.46, glitch(), -12)
    a(18.24, power_up(0.9, 120, 500), -10)
    a(20.20, whoosh(0.25), -6); a(20.44, punch(1.2), -1)
    a(21.92, whoosh(0.22), -6); a(22.14, punch(1.4), 0)
    a(23.12, bp(noise(1.1), 200, 2500) * env(int(1.1 * SR), 0.05, 0.3) * 0.6, -6)
    # Jiren contesta
    a(24.68, power_up(0.8, 90, 260), -6)
    a(26.30, whoosh(0.26), -5); a(26.56, punch(2.0), 0); a(26.56, boom(1.0), -5)
    a(27.75, whoosh(0.7), -8); a(28.60, crash(1.2), -2)
    a(29.74, rumble(1.6), -4)
    for k in range(8): a(29.76 + k * 0.05, thump(), -8)
    # silencio 31.8-32.9 (nada)
    a(32.94, rumble(0.6), -9); a(32.94, power_up(0.6, 60, 200), -12)
    a(33.52, boom(1.8), 0)
    a(34.60, power_up(2.2, 100, 600), -9); a(36.66, punch(1.0), -8)
    # mirada
    a(40.10, hum(1.0, 70), -6)
    for k in range(4): a(40.10 + k * 0.22, whoosh(0.2, False), -14)
    a(41.70, whoosh(0.26), -5); a(41.96, punch(1.8), 0); a(41.96, boom(0.8), -8)
    a(43.26, sting(), -8)
    a(45.22, whoosh(1.4), -3); a(45.22, rumble(1.5), -10)
    a(48.10, rumble(2.0), -6)
    a(51.30, rip(0.45), -1); a(51.30, punch(1.0), -6)
    a(52.08, power_up(1.4, 70, 350), -8); a(53.32, punch(0.8), -8)
    a(54.60, hum(2.5, 45), -9)
    a(57.22, sting(), -8); a(58.68, zap(0.4), -10)
    a(59.64, power_up(1.3, 60, 700), -5); a(60.16, boom(1.0), -6)
    a(61.32, thump(), -1); a(62.64, thump(), 0); a(62.64, rumble(0.7), -8)
    # puño contra puño
    a(64.20, whoosh(0.2), -6)
    for tc in (64.40, 65.50, 66.36):
        a(tc, punch(1.6), 0); a(tc, zap(0.4), -9)
    a(66.36, shatter(0.8), -9)
    a(67.60, punch(1.0), -3)
    a(68.62, hum(1.2, 65), -12)
    for i, h in enumerate((70.12, 71.36, 71.84)):
        a(h - 0.12, whoosh(0.2), -9); a(h, punch(1.2 + 0.4 * i), -2 + i)
    a(72.94, rumble(2.3), -6); a(73.88, shatter(1.0), -3); a(74.32, shatter(1.0), -3)
    a(75.28, power_up(1.3, 80, 500), -6)
    a(76.54, zap(0.6), -6); a(77.04, zap(1.2), -5); a(77.04, rumble(1.3), -8)
    a(78.44, power_up(0.45, 200, 900), -8); a(78.88, boom(2.4), 0)
    a(81.00, wind(3.0), -10); a(83.72, sting(), -10)
    a(84.88, thump(), -4); a(86.30, thump(), -1); a(86.30, rumble(0.5), -9)
    a(86.98, boom(1.0), -6); a(87.26, punch(1.0), -6)
    a(88.20, wind(3.0), -14); a(91.48, punch(1.6), -1); a(91.48, sting(), -6)
    return E


if __name__ == '__main__':
    base.events = lambda: [(t, s, g + 3) for t, s, g in events()]
    _main(sys.argv[1], sys.argv[2])
