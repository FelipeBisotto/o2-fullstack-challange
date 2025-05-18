export interface ProdutoEstoque {
  nome: string;
  quantidade_disponivel: number;
  valor_total: number; // quantidade × preço unitário
}

export interface VendaMensal {
  mes: string; 
  total_vendas: number; // Considera apenas movimentações do tipo "saída"
}

export interface DashboardResponse {
  produtos_estoque: ProdutoEstoque[];          // RF20
  grafico_vendas_mensais: VendaMensal[];       // RF21
  valor_total_estoque: number;                 // RF22
  quantidade_total_itens_vendidos: number;     // RF23
}
