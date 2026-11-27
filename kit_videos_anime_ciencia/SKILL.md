---
name: video-anime-ciencia
description: Crear videos verticales virales de TikTok (1080x1920, 1:20-1:30) que mezclan anime (Dragon Ball, Jujutsu Kaisen, One Piece…) + ciencia real + consejo práctico, con personajes vectoriales dibujados en código, subtítulos virales palabra por palabra, efectos de sonido sincronizados, voz por encima y SIN música; también temas, guion, hoja de personajes, títulos y miniatura 3:4.
---

# Videos virales "anime + ciencia" (kit completo)

Responde SIEMPRE en español. El usuario hace videos de TikTok y entra al programa de recompensas solo si el contenido es ORIGINAL: narración propia, opinión, valor práctico, edición atractiva, > 1 minuto, sin clips del anime y sin música con copyright. Por eso TODO se dibuja y anima en código y los efectos se sintetizan.

## Estructura del kit
```
kit_videos_anime_ciencia/
  SKILL.md                 <- estas instrucciones
  README.md                <- instalación (Node, Python, ffmpeg, Chrome)
  package.json             <- npm install  (puppeteer-core)
  common_puppeteer.mjs     <- localiza Chrome y baja la prioridad del proceso
  plantilla_video/         <- COPIAR esta carpeta para cada video nuevo
    index.html  anim.js  chars.js  words.js  sfx.py  sfx_base.py  render.mjs  transcribe.py
    thumb.html  shot_thumb.mjs  fonts/  gsap.min.js
  plantilla_personajes/    <- hoja.html + shot.mjs (hoja de personajes PNG)
  ejemplos/vegeta_rival/   <- guion, hoja de personajes y miniatura de un video terminado
  ejemplos/black_flash/    <- otro video terminado (anim.js y chars.js completos como referencia)
```
`plantilla_video/anim.js` es el video COMPLETO "Sin Vegeta no hay Ultra Instinto" (91 s): úsalo como ejemplo vivo de cada técnica y reemplaza sus escenas por las del nuevo guion. Crea cada video nuevo como carpeta hermana de `plantilla_video/` (dentro del kit) para que las rutas `../common_puppeteer.mjs` funcionen.

## Flujo (el usuario pide cada paso; tú haces todo y entregas)
1. **Temas** → 3 ideas nuevas y virales: hook, ciencia real (con estudio verificable), valor práctico, por qué genera comentarios/compartidos. Recomienda una. No repetir temas ya hechos (pregunta/lista: Gogeta vs Vegetto, Gohan poder oculto, 7 transformaciones de Goku, Goku agujero negro, SSJ4 vs SSJ Dios, Trunks 6 niveles, Ultra Ego huesos, Luffy gears, Black Flash, Vegeta el rival).
2. **Guion ~1:20** (~220 palabras, la voz es TTS rápida) listo para copiar y pegar, guardado como `guion_<tema>.md`:
   - Frase 1 = killer hook otaku polémico. → conexión con el anime → dato científico con fuente → mini-pregunta "¿Por qué?" → giro / lado oscuro a la mitad (retención) → "Uno / Dos / Tres" pasos prácticos → llamado a comentar/etiquetar → última frase = el hook (BUCLE).
   - Debajo: tabla de escenas por tiempos, fuentes, título y hashtags. Ver `ejemplos/*/guion_*.md`.
3. **Personajes** → busca referencias del diseño oficial (web) y dibuja TODOS los personajes del guion, fieles y reconocibles ("perfectos, no mal dibujados"). Añádelos a `chars.js` (lista `CHARS`) y renderiza la hoja: `cd plantilla_personajes && node shot.mjs` → `hoja_personajes.png` + `png/<id>.png`. MIRA la imagen y corrige manos, pelo, solapes antes de entregar.
4. **Video** con el MP3 que da el usuario (ver "Pipeline").
5. **Títulos** (5, uno recomendado) + descripción + hashtags.
6. **Miniatura 3:4** (1080x1440): `thumb.html` + `node shot_thumb.mjs` → `miniatura_3x4.png`. Personajes grandes cara a cara (VS + rayo), fondo con líneas de velocidad/aura, 2 textos gigantes Anton con contorno negro (arriba blanco con palabra clave roja; abajo amarillo, máx. 2 líneas). Mírala y corrige textos cortados.

## Reglas del video (OBLIGATORIAS, el usuario las repite siempre)
- **Subtítulos virales**: Montserrat 900 MAYÚSCULAS, contorno negro grueso, bloques de 1–3 palabras (≤20 letras), cada palabra hace "pop" justo cuando se dice; rojo = impacto/villano/rival, amarillo = datos/números/protagonista, azul = otras clave. Posición: `top:1500px` (debajo de los pies, suelo en y=1430) para NO tapar la animación.
- **Efectos de sonido sincronizados** con cada acción (cada helper ya llama `sfx()`): whoosh en cortes, pop en textos, slam en texto gigante, impact en golpes, powerup en transformaciones, step al correr, magic, ding en checks, tick en contadores, buzz en ✘.
- **La voz más fuerte que los efectos** (≈10 dB; `sfx.py` hace ducking automático). **NADA de música.**
- **Sincronía exacta**: escenas, cortes y efectos en el tiempo de la palabra (de `words.json`). Sin errores.
- Revisar **storyboard** antes del render final y corregir solapes (pill arriba vs badge, textos cortados, personajes fuera de cuadro, subtítulo de 3 líneas chocando con `lab`).
- No congelar la PC: render con 1 worker en prioridad baja (por defecto). Si la PC es potente: `WORKERS=4`.

## Pipeline (desde la carpeta del video, p.ej. `kit/mi_video/` copiada de `plantilla_video/`)
1. Copia el audio: `cp "<ruta del mp3>" voz.mp3` (los nombres de Descargas suelen tener corchetes → usa comillas o `ls -t ~/Downloads/*.mp3 | head -1`).
2. `python transcribe.py . small "Goku. Vegeta. Ultra Instinto."` → `words.json` + `words.js`. Lee la transcripción y **corrige palabras mal oídas** en `words.js` (también "1." → "1").
3. Escribe `anim.js` (ver API abajo): `END` = duración de la voz + 0.1; una escena por bloque del guion, cortes en el inicio de la palabra.
4. `node render.mjs stills 0.5,2,4,...` → `storyboard.png` (24 cuadros por hoja). Míralo, corrige, repite por tramos hasta cubrir todo el video.
5. `node render.mjs cues` → `cues.json`; `python sfx.py` → `mix.wav` (imprime RMS de voz y efectos; la voz debe quedar ~10 dB arriba).
6. `node render.mjs video` → `video.mp4` (sin audio).
7. `ffmpeg -y -i video.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest <nombre>.mp4`
8. Extrae 3–4 cuadros del MP4 final en momentos clave para verificar y entrega.

## API de `chars.js` (personajes SVG, caja local 400x660, centro x=200, pies y≈620)
`person(o)` devuelve SVG. Opciones principales:
- Piel/cara: `skin, iris, brow, angry, calm, noPupil, veins, majinM, mouth:'smile'|'smirk'|'grit', lips, headExtra (SVG extra en la cabeza)`
- Pelo: `hair:'goku'|'ssj'|'ui'|'vegeta'|'none', hairC, hairHi, hairScale` (añade nuevos paths en `HAIR`)
- Ropa: `top:'goku'|'suit'|'tank'|'bare', topC, under, emblem:'悟'|'亀', sleeve:'short'|'long'|'none', cuff, glove, belt, armor, pads, bottom, shorts, boots, bootTie, shoes, toe, sole, bib, robe, ring, abs, bare`
- Efectos: `aura:'#color', auraOp, behind (SVG detrás), over (SVG delante)`
- `pose: 'stand'|'guard'|'cross'|'punch'|'run'|'run2'|'up'`
Presets: `GI` (gi de Goku), `SAIYAN` (traje + armadura), `GSKIN`. Personajes especiales: `babidi()`, `whisHair`, `whisStaff`. Para un personaje nuevo: nueva entrada de `HAIR`, nuevas opciones de ropa en `person()` o función propia (como `babidi()`), y entrada en `CHARS` para la hoja.

## API de `anim.js` (timeline GSAP en pausa; `window.seek(t)` dibuja el cuadro t)
- Básicos: `sfx(t,nombre,vol)`, `ft(el,from,to,t)`, `rig(id,ox,oy)` (+ `RIGS[id].x/y/r/s`), `pg(id,cx,cy,svg)` grupo animable oculto, `popS(id,t,snd)`, `hideS(id,t)`, `show(id,t)`, `scene(id,t0,t1)`, `cut(t)`.
- Cámara: `cam(t,cx,cy,zoom,dur,ease)`, `shake(t,dur,amp)`, `flash(t,color,op,dur)`.
- Personajes: `actor(id,opciones|función,x,sueloY,escala,[poses],extraSVG,flip)`, `pose(id,i,t)`, `enter(id,t,dx)`, `powerUp(id,t,color)`, `auraPulse(id,t0,t1)`, `breathe(id,t0,t1)`, `runCycle(id,t0,t1)`, `strike(id,t,hold,push)`, `impactFx(id,x,y)` + `boom(id,t)`.
- Textos HTML: `pill(txt,t0,t1,'y'|'r'|'b')` (arriba, top 236), `lab(...)` (abajo, top 1688), `big(txt,t0,t1,color,size,top)` (texto gigante Anton + slam), `stamp(txt,t0,t1,color,top)`, `badge(n,txt,t0,t1)` (pasos 1-2-3, arriba izquierda; no uses `pill` a la vez → usa `lab`).
- Fondos: `radBg(c0,c1,colorLineas)`, `wasteland()`, `nightBg()`, `track(p)` + `trackRun(p,t0,t1)`, `speedLines(id)` + `zoomLines(t0,t1,id)`, `flr(x,y)` sombra en el suelo.
- Subtítulos: bloque `subs()` al final (colores con regex RED/YEL/BLU: ajusta palabras al tema).
- Sonidos disponibles en `sfx.py`: aura, bag, bf, blip, boom, buzz, chain, crack, crackle, ding, glass, glint, hit, impact, magic, neon, pop, powerup, riser, rumble, shimmer, slam, step, stinger, swish, thud, thump, tick, whoosh, zap (más en `sfx_base.GEN`). Para uno nuevo: función numpy en `sfx.py` y añádela al dict `G`.
- Trampas conocidas: no redeclarar nombres de `chars.js` (`OL, fsh, aura, lerp, limb, head, hair, person`); los selectores GSAP deben existir en el DOM (el markup se inserta antes de crear tweens); un `actor` que empieza oculto necesita `tl.set('#id',{opacity:0},0)` o envolverlo en `<g opacity="0">`.

## Estilo visual
Vector plano 2D, contorno oscuro fino, sombra lateral suave, ojos angulosos estilo Toriyama. Fondos con líneas de velocidad del color de la escena. Mucha energía: zooms, temblor en impactos, flashes, auras que pulsan, entradas deslizando, transformaciones con flash. Final que repite el encuadre del inicio (bucle).

## Entrega
Archivos (mp4 en la raíz del proyecto, png, guion .md) + 3–6 líneas: qué escenas hay, qué se verificó y qué no (por ejemplo, si no se escuchó completo).
