// Uso:
//   node render.mjs stills 1.0,3.5,...   -> stills/*.png + storyboard.png
//   node render.mjs cues                  -> cues.json (efectos de sonido)
//   node render.mjs video                 -> video.mp4 (sin audio). WORKERS=1 por defecto (no congela la PC); WORKERS=4 si la PC aguanta
import { spawn, execFileSync } from 'child_process';
import fs from 'fs'; import path from 'path'; import { fileURLToPath, pathToFileURL } from 'url';
import { loadPuppeteer, chromePath, lowPriority } from '../common_puppeteer.mjs';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const puppeteer = loadPuppeteer();
const CHROME = chromePath();
lowPriority();
const URL = pathToFileURL(path.join(HERE, 'index.html')).href;
const FPS = 30;

async function open() {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: true, args: [...(process.platform === 'linux' ? ['--no-sandbox'] : []), '--allow-file-access-from-files', '--disable-gpu', '--hide-scrollbars', '--force-color-profile=srgb'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  p.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await p.goto(URL, { waitUntil: 'load' });
  await p.evaluate(() => window.ready);
  return { b, p };
}

const mode = process.argv[2];
if (mode === 'cues') {
  const { b, p } = await open();
  const cues = await p.evaluate(() => window.SFX.sort((a, b) => a[0] - b[0]));
  fs.writeFileSync(path.join(HERE, 'cues.json'), JSON.stringify(cues));
  console.log(cues.length, 'efectos'); await b.close();
} else if (mode === 'stills') {
  const times = process.argv[3].split(',').map(Number);
  const dir = path.join(HERE, 'stills'); fs.mkdirSync(dir, { recursive: true });
  for (const f of fs.readdirSync(dir)) fs.unlinkSync(path.join(dir, f));
  const { b, p } = await open();
  const files = [];
  for (const t of times) {
    await p.evaluate(t => window.seek(t), t);
    const f = path.join(dir, `t${t.toFixed(2).padStart(6, '0')}.png`); files.push(f);
    await p.screenshot({ path: f });
  }
  await b.close();
  // hoja de contacto con la marca de tiempo
  const cols = Math.min(6, times.length), rows = Math.ceil(times.length / cols);
  const inputs = files.flatMap(f => ['-i', f]);
  const lbl = files.map((f, i) => `[${i}:v]scale=270:480,drawtext=text='${times[i].toFixed(2)}':x=8:y=8:fontsize=26:fontcolor=yellow:box=1:boxcolor=black@0.6[v${i}]`).join(';');
  const layout = files.map((_, i) => `${(i % cols) * 270}_${Math.floor(i / cols) * 480}`).join('|');
  const filter = `${lbl};${files.map((_, i) => `[v${i}]`).join('')}xstack=inputs=${files.length}:layout=${layout}:fill=black`;
  execFileSync('ffmpeg', ['-v', 'error', '-y', ...inputs, '-filter_complex', files.length > 1 ? filter : lbl.replace('[v0]', ''), path.join(HERE, 'storyboard.png')]);
  console.log('storyboard.png', times.length, 'cuadros');
} else if (mode === 'video' || mode === 'part') {
  if (mode === 'video') {
    const N = Math.max(1, Number(process.env.WORKERS || 1));
    const { b, p } = await open(); const dur = await p.evaluate(() => window.DURATION); await b.close();
    const frames = Math.ceil(dur * FPS), per = Math.ceil(frames / N);
    const t0 = Date.now();
    await Promise.all(Array.from({ length: N }, (_, k) => new Promise((res, rej) => {
      const c = spawn(process.execPath, [fileURLToPath(import.meta.url), 'part', k * per, Math.min(frames, (k + 1) * per), `part${k}.mp4`], { stdio: 'inherit' });
      lowPriority(c.pid); c.on('exit', code => code ? rej(new Error('parte ' + k)) : res());
    })));
    fs.writeFileSync(path.join(HERE, 'parts.txt'), Array.from({ length: N }, (_, k) => `file 'part${k}.mp4'`).join('\n'));
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', path.join(HERE, 'parts.txt'), '-c', 'copy', path.join(HERE, 'video.mp4')]);
    for (let k = 0; k < N; k++) fs.unlinkSync(path.join(HERE, `part${k}.mp4`));
    console.log('video.mp4 listo en', ((Date.now() - t0) / 1000).toFixed(0), 's');
  } else {
    const [a, z, out] = [Number(process.argv[3]), Number(process.argv[4]), process.argv[5]];
    const { b, p } = await open();
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-c:v', 'libx264', '-threads', '2', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', path.join(HERE, out)], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = a; f < z; f++) {
      await p.evaluate(t => window.seek(t), f / FPS);
      const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if ((f - a) % 150 === 0) console.log(`[${out}] ${f - a}/${z - a}`);
    }
    ff.stdin.end(); await new Promise(r => ff.on('exit', r)); await b.close();
  }
}
