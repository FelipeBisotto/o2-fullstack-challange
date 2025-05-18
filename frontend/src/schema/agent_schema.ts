export interface ComandoAgente {
  comando: string;
}

export interface RespostaAgente {
  tipo_acao: 'consultar' | 'movimentar';       // RF32, RN24
  tipo_movimentacao?: 'entrada' | 'saida';     // RN27 (só se tipo_acao = movimentar)
  nome_produto?: string;                       // RF33
  quantidade?: number;                         // RN25
  data_inicio?: string;                        // ISO date – para consultas com intervalo
  data_fim?: string;                           // ISO date – para consultas com intervalo
  data_movimentacao?: string;                  // para ações tipo 'movimentar' – RN26
  mensagem?: string;                           // mensagens de erro ou sucesso (RF34, RF36)
}
