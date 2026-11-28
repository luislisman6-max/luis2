// Exporta cada SVG de personajes/rdr a PNG 3x (nítido aunque se amplíe en el video)
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const SRC = path.join(__dirname, '../personajes/rdr'), OUT = path.join(__dirname, 'assets');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 3 });
  for (const f of fs.readdirSync(SRC).filter(f => f.endsWith('.svg') && !f.startsWith('preview'))) {
    await p.setContent('<html><body style="margin:0;background:transparent">' + fs.readFileSync(path.join(SRC, f), 'utf8') + '</body></html>');
    await p.locator('svg').screenshot({ path: path.join(OUT, f.replace('.svg', '.png')), omitBackground: true }); console.log('hd', f);
  }
  await b.close();
})();
