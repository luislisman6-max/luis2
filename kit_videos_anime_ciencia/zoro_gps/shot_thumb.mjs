import path from 'path'; import { fileURLToPath, pathToFileURL } from 'url';
import { loadPuppeteer, chromePath } from '../common_puppeteer.mjs';
const HERE = path.dirname(fileURLToPath(import.meta.url)); const puppeteer = loadPuppeteer();
const b = await puppeteer.launch({ executablePath: chromePath(), headless: true, args: [...(process.platform === 'linux' ? ['--no-sandbox'] : []), '--allow-file-access-from-files'] });
const p = await b.newPage(); await p.setViewport({ width: 1080, height: 1440 });
p.on('pageerror', e => console.error('ERR', e.message));
await p.goto(pathToFileURL(path.join(HERE, 'thumb.html')).href, { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: path.join(HERE, 'miniatura_3x4.png') }); await b.close(); console.log('ok');
