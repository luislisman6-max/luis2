export function saludo(nombre: string): string {
  const limpio = nombre.trim();
  return limpio ? `¡Hola, ${limpio}!` : '¡Hola, mundo!';
}
