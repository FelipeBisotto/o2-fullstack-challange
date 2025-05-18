export function required(value: string): string | null {
  return value.trim() === '' ? 'Campo obrigatório' : null;
}

export function greaterThanZero(value: string): string | null {
  const number = parseFloat(value.replace(',', '.'));
  return isNaN(number) || number <= 0 ? 'Deve ser maior que zero' : null;
}

export function greaterThanOrEqualToZero(value: string): string | null {
  const number = parseInt(value);
  return isNaN(number) || number < 0 ? 'Não pode ser negativo' : null;
}

export function uniqueName(
  value: string,
  lista: { nome: string; id?: number }[],
  currentId?: number
): string | null {
  const nomeLower = value.trim().toLowerCase();
  const duplicado = lista.some(
    (item) =>
      item.nome.trim().toLowerCase() === nomeLower &&
      (currentId === undefined || item.id !== currentId)
  );
  return duplicado ? 'Nome já existe' : null;
}

export function validate(value: string, rules: ((v: string) => string | null)[]): string | null {
  for (const rule of rules) {
    const erro = rule(value);
    if (erro) return erro;
  }
  return null;
}
