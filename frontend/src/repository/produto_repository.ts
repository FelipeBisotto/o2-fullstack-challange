import api from '@/service/api';
import type { Produto, ProdutoFormSchemaData } from "@/schema/produto_schema";

export async function getProdutos() {
  return api.get<Produto[]>('/produtos');
}

export async function getProdutoById(id: number) {
  return api.get<Produto>(`/produtos/${id}`);
}

export async function createProduto(data: ProdutoFormSchemaData) {
  return api.post<Produto>('/produtos', data);
}

export async function updateProduto(id: number, data: ProdutoFormSchemaData) {
  return api.put<Produto>(`/produtos/${id}`, data);
}

export async function deleteProduto(id: number, confirmado = true) {
  return api.delete(`/produtos/${id}?confirmado=${confirmado}`);
}
