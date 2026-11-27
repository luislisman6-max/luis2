// Localiza puppeteer-core y Chrome de forma portátil (usado por todos los scripts .mjs del kit)
import { createRequire } from 'module'; import fs from 'fs'; import path from 'path'; import os from 'os';
const require = createRequire(import.meta.url);
export function loadPuppeteer() {
  try { return require('puppeteer-core'); } catch { }
  throw new Error('Falta puppeteer-core: ejecuta "npm install" dentro de la carpeta del kit');
}
export function chromePath() {
  const c = [process.env.CHROME, 'C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    path.join(os.homedir(), 'AppData/Local/Google/Chrome/Application/chrome.exe'), 'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium'].filter(Boolean);
  for (const p of c) if (fs.existsSync(p)) return p;
  throw new Error('No encuentro Chrome. Define la variable CHROME con la ruta a chrome.exe');
}
// baja la prioridad del proceso para no congelar la PC
export function lowPriority(pid = process.pid) { try { os.setPriority(pid, os.constants.priority.PRIORITY_BELOW_NORMAL); } catch { } }
