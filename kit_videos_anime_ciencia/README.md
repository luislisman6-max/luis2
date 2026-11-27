# Kit: videos virales anime + ciencia (TikTok 9:16)

Todo funciona en local y gratis: HTML+SVG+GSAP para animar, Chrome (puppeteer-core) para capturar cuadros, Whisper local para los tiempos de cada palabra, numpy para los efectos de sonido y ffmpeg para el MP4. Las instrucciones para Claude están en **SKILL.md**.

## 1. Instalar (una sola vez)
- **Node.js 18+**, **Python 3.10+**, **ffmpeg** (en el PATH) y **Google Chrome** (o Edge).
- En esta carpeta:
```
npm install
pip install faster-whisper numpy
```
- Si Chrome no está en la ruta normal: variable de entorno `CHROME` con la ruta a `chrome.exe`.
- La primera transcripción descarga el modelo Whisper "small" (~460 MB).

## 2. Instalarlo como skill de Claude Code (opcional)
Copia esta carpeta completa a `.claude/skills/video-anime-ciencia/` del proyecto (o a `~/.claude/skills/video-anime-ciencia/`). Claude leerá `SKILL.md` cuando pidas un video de este tipo. Si no, simplemente dile a Claude: "lee kit_videos_anime_ciencia/SKILL.md y trabaja así".

## 3. Hacer un video nuevo
```
cp -r plantilla_video mi_video          # dentro de esta carpeta del kit
cd mi_video
cp "C:/ruta/a/la/voz.mp3" voz.mp3
python transcribe.py . small "Goku. Vegeta."
# editar anim.js (escenas) y chars.js (personajes)
node render.mjs stills 1,5,10,20        # storyboard.png para revisar
node render.mjs cues && python sfx.py   # efectos + mezcla (mix.wav)
node render.mjs video                   # video.mp4 (WORKERS=4 si la PC es potente)
ffmpeg -y -i video.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest final.mp4
node shot_thumb.mjs                     # miniatura_3x4.png
```
Hoja de personajes: `cd plantilla_personajes && node shot.mjs` (usa `plantilla_video/chars.js`).

## 4. Ejemplos incluidos
- `plantilla_video/` = el video "Sin Vegeta no hay Ultra Instinto" completo (para ver todas las técnicas).
- `ejemplos/vegeta_rival/` y `ejemplos/black_flash/` = guiones, hojas de personajes y miniaturas terminadas.
