// node shot.mjs -> hoja_personajes.png (hoja) + png/<nombre>.png (cada tarjeta)
import fs from 'fs'; import path from 'path'; import { fileURLToPath, pathToFileURL } from 'url';
import { loadPuppeteer, chromePath } from '../../common_puppeteer.mjs';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const puppeteer = loadPuppeteer();
const b = await puppeteer.launch({ executablePath: chromePath(), headless: true,
  args: [...(process.platform === 'linux' ? ['--no-sandbox'] : []), '--allow-file-access-from-files', '--hide-scrollbars', '--force-color-profile=srgb'] });
const p = await b.newPage();
await p.setViewport({ width: 1440, height: 1810, deviceScaleFactor: 1 });
await p.goto(pathToFileURL(path.join(HERE, 'hoja.html')).href, { waitUntil: 'load' });
await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: path.join(HERE, 'hoja_personajes.png') });
fs.mkdirSync(path.join(HERE, 'png'), { recursive: true });
const ids = await p.$$eval('svg', s => s.map(e => e.id));
for (const id of ids) await (await p.$('#' + id)).screenshot({ path: path.join(HERE, 'png', id + '.png') });
console.log('ok', ids.length);
await b.close();
