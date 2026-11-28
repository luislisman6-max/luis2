"""Fondo de atardecer del estilo de referencia + personaje encima (solo para revisar)."""
import sys, os, subprocess, json
D = os.path.dirname(os.path.abspath(__file__))
name = sys.argv[1] if len(sys.argv) > 1 else 'arthur'
char = open(os.path.join(D, name + '.svg')).read()
bg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#5a3a6e"/><stop offset=".45" stop-color="#d9673e"/><stop offset=".75" stop-color="#f2a64e"/></linearGradient>
<radialGradient id="sun"><stop offset="0" stop-color="#fff6d8"/><stop offset=".5" stop-color="#ffe7a0"/><stop offset="1" stop-color="#ffe7a0" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/></radialGradient></defs>
<rect width="1280" height="720" fill="url(#sky)"/>
<circle cx="420" cy="440" r="160" fill="url(#sun)"/><circle cx="420" cy="440" r="62" fill="#fff3cf"/>
<path d="M0,470 L120,400 L180,430 L260,330 L340,420 L420,380 L520,450 L640,360 L720,420 L820,340 L900,410 L1000,350 L1100,430 L1180,380 L1280,430 L1280,720 L0,720Z" fill="#9b4f52" stroke="#1e130d" stroke-width="3"/>
<path d="M260,330 L240,362 L262,352 L280,368 L300,356 Z M820,340 L800,372 L822,362 L840,376 Z M1000,350 L984,378 L1004,370 L1020,380 Z" fill="#f3d7d0"/>
<path d="M0,520 Q320,500 640,520 T1280,515 L1280,720 L0,720Z" fill="#7a3a2e" stroke="#1e130d" stroke-width="3"/>
<rect y="560" width="1280" height="160" fill="#5e2c22"/>
<g transform="translate(700,70) scale(0.46)">''' + char.split('>',1)[1].rsplit('</svg>',1)[0] + '''</g>
<ellipse cx="838" cy="676" rx="90" ry="10" fill="#000" opacity=".25"/>
<rect width="1280" height="720" fill="url(#vig)"/></svg>'''
open(os.path.join(D, 'preview_' + name + '.svg'), 'w').write(bg)
js = """const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:1});
await p.setContent('<html><body style="margin:0">'+fs.readFileSync(%s,'utf8')+'</body></html>');await p.locator('svg').screenshot({path:%s});await b.close();})();""" % (
    json.dumps(os.path.join(D, 'preview_' + name + '.svg')), json.dumps(os.path.join(D, 'preview_' + name + '.png')))
subprocess.run(['node', '-e', js], check=True)
