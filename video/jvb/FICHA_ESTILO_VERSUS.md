# FICHA DE ESTILO — Formato «¿QUIÉN CAE PRIMERO?» (versus anime, vertical)

Video de referencia ya hecho: JIREN vs BROLY (1:32, 1080x1920, 30 fps).

## 1. Formato
- Vertical 9:16, 1080x1920, 30 fps, H.264 + AAC 192k. Duración 1:20–1:35 (más de 1 minuto para el programa de recompensas de TikTok).
- Sin música. Solo voz en off + efectos de sonido sintetizados/originales.
- Narrador rápido y épico (voz acelerada ~1.1–1.2x), ~2.6 palabras por segundo, ~220–240 palabras.

## 2. Estructura del guion (viral)
1. GANCHO (0–5 s): dos fuerzas absolutas que chocan + pregunta. Ej.: «X nunca ha hecho A. Y nunca ha dejado de B. Cuando choquen… solo uno queda en pie. ¿Quién cae primero?»
2. «Ronda uno»: el favorito domina fácil (frena el golpe con una mano, ni se mueve).
3. ESCALADA del rival: aprende / se transforma / crece (X2, X3). Cada transformación = nuevo color de aura.
4. Contraataque brutal: un solo golpe, el otro atraviesa un edificio y queda enterrado.
5. «Silencio.» (0,8–1 s sin ningún efecto) → las rocas explotan → transformación.
6. Por primera vez el invencible sale volando (fuera del planeta).
7. El invencible se enoja / forma final. El otro responde con su forma definitiva.
8. Puño contra puño: cada choque rompe una galaxia → el universo se cae a pedazos.
9. Último ataque: color contra color → «y todo… se vuelve blanco».
10. Entre el humo hay una silueta → revelación → da un paso… y se desploma.
11. «Gana [NOMBRE].»
12. CIERRE EN BUCLE: repetir la frase del gancho con un remate («…hasta hoy»), para que enlace con el inicio.
- Frases cortas, 3–8 palabras. Pausas dramáticas con «…».

## 3. Estilo de dibujo
- 2D vectorial plano, SIN degradados en los personajes, contorno negro grueso (#111, 7 px sobre 600 px de alto), uniones redondeadas.
- Cuerpo de «bloques» tipo muñeco articulado: cabeza grande, cuello rectangular, torso trapecio, hombros = círculos grandes, brazo superior y antebrazo = rectángulos redondeados, puño = rectángulo redondeado con 3 líneas de dedos, muñequeras negras con raya blanca, piernas rectangulares, botas blancas.
- Musculatura con 4–6 líneas finas de un tono más oscuro de la piel (pectorales en «M», línea central, 3 líneas de abdomen).
- Pelo de saiyajin = triángulos (picos) en abanico, con media cara de cada pico en un tono más oscuro (sombra plana); flequillo = casquete con picos sobre la frente.
- Caras simples: ojos almendrados blancos con iris pequeño y ceja gruesa inclinada (enfado); «ojos en blanco» para formas berserker; boca roja abierta con dientes blancos para sonrisa/grito.
- Poses: de frente (presentación/transformación) y «golpe» = un brazo estirado horizontal hacia el rival. Volar/caer = rotar el sprite.
- Cada personaje tiene SU color, que se repite en aura, fondo y en su nombre en subtítulos (Jiren rojo #ff3b4e, Broly verde #7dff3a, dorado #ffd23a para SSJ).
- Generados como SVG → PNG transparente 2000x2000 (lienzo ancho para que quepa el brazo estirado; pies anclados abajo en el centro).

## 4. Escenarios (fondos planos con capas)
- Arena ciudad morada: cielo degradado #1a0b38→#c2477f, sol difuminado, aro decorativo arriba, hexágonos flotantes con borde lila, skyline oscuro con ventanas, suelo con rejilla en perspectiva (estilo synthwave).
- Arena roja: misma composición en #2a0707→#e4562c con bordes naranjas.
- Espacio: estrellas, nebulosas difuminadas, galaxia espiral de anillos de colores, luna gris con cráteres, planeta azul abajo.
- Fondo «burst»: rayos radiales alternados del color del personaje + brillo central (para primeros planos y transformaciones).
- Humo final: gris-morado oscuro, nubes difuminadas, hexágonos naranjas en el suelo, brasas subiendo.
- La historia ESCALA de escenario: calle → rocas → planeta → galaxia → universo roto → blanco → humo.

## 5. Edición / animación
- Corte cada 1–2,5 s, siempre en la palabra exacta (tiempos por palabra con Whisper).
- «Zoom punch» de 7 % en cada corte (se acerca y vuelve en 0,22 s).
- En cada golpe: estallido de estrella (2 capas, blanco + color), anillo/onda expansiva, sacudida de cámara que decae (0,35–0,6 s), flash blanco corto, polvo en el suelo, líneas de velocidad durante el dash.
- Auras: picos de energía parpadeantes + resplandor difuminado + chispas blancas.
- Rayos (lightning) en choques, grietas en la galaxia, esquirlas triangulares, rocas hexagonales que caen/explotan.
- Primeros planos de cara para frases emocionales; planos generales para golpes.
- Silueta negra entre el humo → se revela con fundido → cae rotando 90°.

## 6. Subtítulos
- Fuente: Bebas Neue (subtítulos) y Anton (rótulos grandes).
- Subtítulo: MAYÚSCULAS, 1–3 palabras por bloque, ~128 px, relleno blanco, contorno negro 10 px + sombra; aparecen palabra por palabra con pequeño «pop» (75 %→100 % en 0,12 s).
- Palabras clave coloreadas: nombres en su color, ROJO/ENOJA/DESPLOMA en rojo, VERDE/LEGENDARIO/APRENDE en verde, DORADO/SÚPER/SAIYAJIN en dorado, GALAXIA/UNIVERSO/PLANETA en cian.
- Posición: y ≈ 1440 de 1920 (debajo de los personajes, sobre el suelo), centrado, ancho máx. ~900 px → no tapa a los personajes ni queda bajo la interfaz de TikTok.
- Rótulos grandes (¡PUM!, X2, X3, ENTERRADO, LEGENDARIO, FIN DEL UNIVERSO, HASTA HOY): Anton 150–190 px, color + contorno negro 14 px + sombra, girados 4°, en y ≈ 470 (tercio superior), entran con rebote y salen en 0,15 s.
- Cabecera fija arriba (y ≈ 150–270): «JIREN  vs  BROLY» con cada nombre en su color.
- Ocultar el subtítulo cuando el rótulo grande dice lo mismo (¿QUIÉN CAE?, RONDA 1, GANA BROLY).

## 7. Sonido
- Efectos sintetizados y sincronizados al mismo segundo que la animación: golpe (grave + crujido), boom/explosión, whoosh antes de cada corte y de cada dash, subida de poder (sierra ascendente), retumbo, derrumbe, desgarro (uniforme), cristal roto (universo), rayo eléctrico, campana (ronda), viento (humo), sting grave en revelaciones.
- «Silencio» = cero efectos.
- Mezcla: voz normalizada a -1 dB de pico; efectos ~14 dB por debajo de la voz y con ducking automático (bajan 50 % cuando habla el narrador). Sin música.

## 8. Portada y miniaturas
- Fondo partido en diagonal con los dos colores + grieta blanca en el centro + líneas de velocidad.
- Primeros planos en diagonal: el ganador arriba y más grande, el perdedor abajo y más pequeño (insinúa sin revelar).
- Estallido con «VS» en el punto de choque + rayos.
- Texto: «¿QUIÉN» blanco + «CAE PRIMERO?» dorado (Anton con contorno negro), nombres abajo en su color.
- Tamaños: TikTok 1080x1920, 3:4 1080x1440, YouTube 1280x720.

## 9. Flujo de trabajo
1. Guion con la estructura del punto 2.
2. Voz en off (mp3) → Whisper con tiempos por palabra (corregir palabras mal entendidas solo en el subtítulo).
3. Dibujar personajes (pose frente + pose golpe por cada forma).
4. Lista de escenas con tiempo de inicio = palabra exacta; rótulos y efectos de sonido anclados a los mismos tiempos.
5. Render 1080x1920 en paralelo → unir con el audio mezclado.
6. Revisar fotogramas de cada impacto antes de entregar.

## 10. Publicación
- Título que genere tensión sin revelar el final (ej.: «Jiren nunca retrocedió… hasta que llegó Broly»).
- Descripción pidiendo votar ANTES del final («Comenta 🔴 JIREN o 🟢 BROLY») + 8–10 hashtags del anime.
- Comentario fijado preguntando por el próximo combate.
