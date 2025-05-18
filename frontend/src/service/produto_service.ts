import type { Produto } from '@/schema/produto_schema';
import { getProdutos } from '@/repository/produto_repository';
import { produtoFormSchema } from '@/schema/produto_schema';
import type { ProdutoFormSchemaData, ProdutoFormDataManual } from '@/schema/produto_schema';


export function ordenarProdutosPorNome(produtos: Produto[]): Produto[] {
  return [...produtos].sort((a, b) => a.nome.localeCompare(b.nome));
}

export function calcularValorTotal(produto: Produto): number {
  return produto.preco_unitario * produto.quantidade;
}

export function formatarPreco(preco: number): string {
  return preco.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  });
}

/**
 * Verifica se o nome informado já existe entre os produtos (case insensitive).
 * RN02: nome único.
 */
export async function nomeJaExiste(nome: string): Promise<boolean> {
  const response = await getProdutos();
  const produtos = response.data;
  return produtos.some(p => p.nome.trim().toLowerCase() === nome.trim().toLowerCase());
}

export function normalizarForm(form: ProdutoFormDataManual): ProdutoFormSchemaData {
  return produtoFormSchema.parse(form);
}
