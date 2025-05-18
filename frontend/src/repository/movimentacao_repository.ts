import api from '@/service/api';
import type { Movimentacao, MovimentacaoFormData } from '@/schema/movimentacao_schema';

export async function getMovimentacoes() {
  return api.get<Movimentacao[]>('/movimentacoes');
}

export async function getMovimentacoesPorProduto(produtoId: number) {
  return api.get<Movimentacao[]>(`/movimentacoes/produto/${produtoId}`);
}

export async function createMovimentacao(data: MovimentacaoFormData) {
  return api.post<Movimentacao>('/movimentacoes', data);
}
