// Converte de 'YYYY-MM-DD' para 'DD/MM/AAAA' — RN21
export const formatarData = (data: string): string => {
  if (!data.includes('-')) return data; 
  const [ano, mes, dia] = data.split('-');
  return `${dia}/${mes}/${ano}`;
};
