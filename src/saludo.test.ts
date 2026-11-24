import { describe, expect, it } from 'vitest';
import { saludo } from './saludo';

describe('saludo', () => {
  it('saluda por nombre', () => {
    expect(saludo('Luis')).toBe('¡Hola, Luis!');
  });

  it('usa "mundo" si el nombre está vacío', () => {
    expect(saludo('   ')).toBe('¡Hola, mundo!');
  });
});
