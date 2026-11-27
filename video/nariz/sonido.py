"""Efectos sintetizados para «Tu nariz desaparece» y mezcla con la voz.
La voz manda: efectos ~15 dB por debajo y con ducking (bajan cuando hay voz). Sin música."""
import os, sys, subprocess, wave
import numpy as np
from scipy import signal

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sfx as base                      # efectos del video anterior
from sfx import SR, env, bp, lp, sweep, norm, rng
import escenas


def whoosh_down(dur=0.8):
    n = int(dur * SR); x = rng.normal(0, 1, n)
    out = bp(x, 200, 2500) * np.linspace(1, 0.3, n)
    tone = sweep(900, 140, dur) * 0.5
    return norm((out + tone) * np.sin(np.linspace(0, np.pi, n)) ** 1.3)


def zap(dur=0.6):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * (300 + 900 * t / dur) * t)) * 0.4 + 0.6 * bp(rng.normal(0, 1, n), 2000, 7000)
    x *= 0.6 + 0.4 * (np.sin(2 * np.pi * 30 * t) > 0)
    return norm(lp(x, 6000) * env(n, 0.01, 0.15))


def steps(dur=1.0):
    out = np.zeros(int(dur * SR) + SR // 4)
    k = 0; t = 0.0
    while t < dur:
        n = int(0.06 * SR)
        s = bp(rng.normal(0, 1, n), 120, 900) * np.exp(-np.linspace(0, 8, n))
        i = int(t * SR); out[i:i + n] += s
        t += 0.24; k += 1
    return norm(out)


def thunder():
    n = int(0.9 * SR); t = np.arange(n) / SR
    x = lp(rng.normal(0, 1, n), 300) * np.exp(-t * 4) + 0.6 * bp(rng.normal(0, 1, n), 1500, 6000) * np.exp(-t * 25)
    return norm(x)


def powerdown():
    d = 0.6; n = int(d * SR)
    return norm(sweep(700, 90, d, 'sq') * env(n, 0.005, 0.2))


def rise(dur=0.5):
    n = int(dur * SR)
    return norm(sweep(300, 1400, dur) * env(n, 0.02, 0.08))


def sweep_fx(dur=0.8):
    n = int(dur * SR)
    return norm(sweep(250, 900, dur) * np.sin(np.linspace(0, np.pi, n)))


def poof():
    n = int(0.45 * SR); t = np.arange(n) / SR
    return norm(bp(rng.normal(0, 1, n), 300, 3000) * env(n, 0.01, 0.3) * np.exp(-t * 6))


def shutter():
    out = np.zeros(int(0.25 * SR))
    for k, (dt, f) in enumerate(((0.0, 2500), (0.09, 1800))):
        n = int(0.05 * SR); i = int(dt * SR)
        out[i:i + n] += bp(rng.normal(0, 1, n), f * 0.5, f * 2) * np.exp(-np.linspace(0, 10, n))
    return norm(out)


def snip():
    out = np.zeros(int(0.3 * SR))
    for dt in (0.0, 0.12):
        n = int(0.04 * SR); i = int(dt * SR); t = np.arange(n) / SR
        out[i:i + n] += (bp(rng.normal(0, 1, n), 3000, 9000) + 0.6 * np.sin(2 * np.pi * 4200 * t)) * np.exp(-t * 120)
    return norm(out)


def blink():
    n = int(0.12 * SR); t = np.arange(n) / SR
    return norm(np.sin(2 * np.pi * (900 - 2500 * t) * t) * np.exp(-t * 35) + 0.3 * bp(rng.normal(0, 1, n), 2000, 6000) * np.exp(-t * 60))


def alarm(dur=0.9):
    n = int(dur * SR); t = np.arange(n) / SR
    f = np.where((t * 6).astype(int) % 2 == 0, 880, 660)
    return norm(np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 * env(n, 0.01, 0.1))


def swirl(dur=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 600 + 300 * np.sin(2 * np.pi * 3 * t)
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.05, 0.2))


GEN = {
    'poof': poof, 'shutter': shutter, 'snip': snip, 'blink': blink, 'alarm': alarm, 'swirl': swirl,
    'whoosh': lambda dur=0.35: base.whoosh(dur), 'whoosh_down': whoosh_down, 'pop': base.pop_, 'bloop': base.bloop,
    'click': base.click, 'beep': lambda: base.beep(1300), 'scan': lambda dur=0.9: base.scan(dur), 'ding': base.ding,
    'buzz': base.buzz, 'squeeze': base.squeeze, 'boing': base.boing, 'glu': base.glu, 'exhale': lambda dur=0.8: base.exhale(dur),
    'thump': base.thump, 'snore': lambda dur=1.2: base.snore(dur), 'tick': base.tick, 'impact': base.impact,
    'sparkle': base.sparkle, 'glitch': base.glitch, 'zap': zap, 'steps': steps, 'thunder': thunder,
    'powerdown': powerdown, 'rise': rise, 'sweep': sweep_fx,
}


def main(voice_in, out_wav):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', voice_in, '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'], capture_output=True).stdout
    voice = np.frombuffer(raw, np.float32).astype(np.float64)
    tail = int(0.5 * SR)
    voice = np.concatenate([voice, np.zeros(tail)])
    n = len(voice)
    fx = np.zeros(n + 2 * SR)
    for t, name, g, kw in escenas.build_sfx():
        s = GEN[name](**kw)
        i = int(round(t * SR))
        if i < 0: s = s[-i:]; i = 0
        s = s[: len(fx) - i]
        fx[i:i + len(s)] += s * 10 ** (g / 20)
    fx = fx[:n]
    voice = voice / (np.max(np.abs(voice)) + 1e-9) * 0.89
    win = int(0.05 * SR)
    rms = np.sqrt(np.convolve(voice ** 2, np.ones(win) / win, 'same'))
    rms = lp(rms, 8)
    duck = 1 - 0.55 * np.clip(rms / 0.06, 0, 1)
    # nivel: efectos ~15 dB bajo la voz (medido en zonas activas)
    v_rms = np.sqrt(np.mean(voice[np.abs(voice) > 0.02] ** 2))
    fx = fx * duck
    f_rms = np.sqrt(np.mean(fx[np.abs(fx) > 0.01 * np.max(np.abs(fx))] ** 2))
    fx *= (v_rms / f_rms) * 10 ** (-15 / 20)
    # limitador: ningún efecto se acerca a menos de 10 dB de la voz típica
    vm = np.median(np.sqrt(np.convolve(voice ** 2, np.ones(win) / win, 'same'))[::win])
    vm = np.median([x for x in np.sqrt(np.convolve(voice ** 2, np.ones(win) / win, 'same'))[::win // 2] if x > 0.03])
    fenv = lp(np.sqrt(np.convolve(fx ** 2, np.ones(win) / win, 'same')), 20)
    fenv = np.maximum.accumulate(fenv[::-1])[::-1] * 0 + fenv
    gain = np.minimum(1.0, (vm * 10 ** (-10 / 20)) / (np.abs(fenv) + 1e-9))
    gain = -np.maximum.reduceat(-gain, np.arange(0, len(gain), 480)).repeat(480)[:len(gain)]
    gain = lp(gain, 30)
    fx = fx * np.clip(gain, 0, 1)
    mix = voice + fx
    mix = mix / max(1.0, np.max(np.abs(mix)) / 0.97)
    pcm = (np.clip(np.stack([mix, mix], 1), -1, 1) * 32767).astype(np.int16)
    with wave.open(out_wav, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    f_rms2 = np.sqrt(np.mean(fx[np.abs(fx) > 0.01 * np.max(np.abs(fx))] ** 2))
    print('voz RMS %.3f | efectos RMS %.3f | voz por encima: %.1f dB | duración %.2f s' % (v_rms, f_rms2, 20 * np.log10(v_rms / f_rms2), n / SR))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
