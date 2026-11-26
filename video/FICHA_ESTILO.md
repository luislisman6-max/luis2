# Ficha de estilo — videos de curiosidades del cuerpo (estilo «Mente Curiosa» mejorado)

## Formato
- Video vertical 9:16, 1080x1920, 30 fps. Miniatura 3:4 (1080x1440).
- Narración con voz en off. NADA de música, solo efectos de sonido.
- Duración según el audio de la voz (el último salió de ~1:38).

## Estructura del guion (viral)
1. **Killer hook (0–3 s):** el dato más impactante primero. Ej: «Ese pedo que te aguantaste en la reunión… lo vas a terminar respirando.»
2. **Intro tipo pregunta:** «¿Qué pasa en tu cuerpo cuando…?»
3. **Bomba/spoiler:** el dato absurdo con pausa antes del remate.
4. **Mecanismo** explicado paso a paso (ciencia real, frases cortas).
5. **Dato numérico grande** en pantalla (contador).
6. **Conflicto + consecuencia** (lo que pasa cuando haces X).
7. **CTA a mitad:** «Quédate, porque ahora viene lo más raro» + botón «Sígueme».
8. **Payoff + prueba real** (estudio, prueba médica).
9. **Giro final** + conclusión en una frase.
10. **Cierre:** «Mándaselo a ese amigo que…» + frase cortada que empalma con el hook (bucle).

Solo datos científicos verificados.

## Estilo visual
- Ilustración 2D vectorial con degradados suaves, brillos (glow), viñeta oscura y grano fino. Nada de 3D realista.
- Tres «mundos» que se alternan, con un corte cada 1–3 s:
  - **a) Interior del cuerpo ROSA:** paredes musculares a rayas (`#d24a73` / `#a8325a`) con borde rosa claro (`#ffc2d2`), interior magenta (`#8e2148` → `#5e1233`) con vellosidades onduladas, capa amarilla de comida (`#e3a23a`), esfínter rojo con fibras (`#e5364f`).
  - **b) HOLOGRAMA AZUL:** fondo azul marino (`#13305e` → `#0a1a38`) con niebla y rejilla en perspectiva en el suelo; silueta humana azul con líneas horizontales y borde cian brillante; caminos verdes (✓) y rojos punteados (✗).
  - **c) Personajes 2D planos estilo cartoon:** cabeza grande, ojos grandes con brillo, mejillas rojas, sudor; fondos morado (`#2d1650`), teal (`#1c6b72`), sala de reunión beige, cuarto azul de noche.
- **Elementos recurrentes:** burbuja de gas translúcida con reflejo ovalado; badge rojo «!»; check verde ✓ / X roja; lupa de rayos X sobre la panza; bacterias con ojitos; nube de aliento; rayitas de movimiento; chispas; textos cómicos (PRRT, GLU, GRRR) amarillos con borde oscuro.
- **Animaciones:** pop con rebote (ease-back), zoom lento de cámara, golpe de zoom en cada corte, temblor en momentos de tensión, glitch en «spoiler».

## Subtítulos
- Palabra por palabra, sincronizados al milisegundo con la voz (tiempos sacados con Whisper).
- Arriba, a ~330 px del borde superior (debajo de la barra de TikTok, sin tapar la acción).
- Fuente Inter Display Black, ~76 px, blanca con borde oscuro grueso + sombra.
- Grupos de 1–4 palabras; las palabras aparecen con un pequeño salto mientras se dicen; las ya dichas quedan un poco más tenues.
- La palabra clave que suena va en una caja azul con puntitos en las esquinas (estilo selección).

## Sonido
- Efectos sintetizados y sincronizados con cada animación: pop, burbuja (bloop), whoosh en los cortes, beep/escáner, ding de acierto, buzz de error, apretón, GLU, gruñido de tripa, globo inflándose, latido, exhalación, ronquido, pedo cómico, tick de contador, impacto.
- La voz siempre manda: efectos ~15 dB por debajo de la voz y con ducking (bajan solos cuando hay voz).

## Flujo de trabajo
1. Guion → el usuario graba/genera la voz (MP3).
2. Transcribir con Whisper para sacar el tiempo de cada palabra (corregir ortografía a mano).
3. Planear escenas y efectos amarrados a palabras exactas.
4. Renderizar con Python (Pillow + numpy + ffmpeg), mezclar voz + efectos, comprimir a ~55 MB.
5. Revisar fotogramas en las palabras clave para confirmar la sincronización.

## Título y miniatura
- Título viral de una sola línea con el dato más fuerte + emoji. Ej: «El pedo que te aguantas termina saliendo por tu boca 😳»
- Miniatura 3:4: título grande arriba (línea blanca + línea amarilla sobre franja roja), personaje en shock en primer plano, la burbuja y una flecha que cuentan la historia sin leer, badge «!», fondo morado con burbujas.

## Código de referencia
Carpeta `video/` de esta rama: `lib.py`, `art.py`, `scenes.py`, `render.py`, `sfx.py`, `miniatura.py`.
