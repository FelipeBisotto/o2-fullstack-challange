
import type { Movimentacao } from '@/schema/movimentacao_schema';

export function formatarData(dataIso: string): string {
  const data = new Date(dataIso);
  return data.toLocaleDateString('pt-BR');
}

export function ordenarMovimentacoesPorData(movimentacoes: Movimentacao[]): Movimentacao[] {
  return [...movimentacoes].sort((a, b) => new Date(b.data).getTime() - new Date(a.data).getTime());
}

export function filtrarPorTipo(movimentacoes: Movimentacao[], tipo: 'entrada' | 'saida') {
  return movimentacoes.filter(m => m.tipo === tipo);
}

export function classeTipoMovimentacao(tipo: 'entrada' | 'saida') {
  return tipo === 'entrada' ? 'linha-entrada' : 'linha-saida';
}
