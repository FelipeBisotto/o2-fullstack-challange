
export interface RelatorioFiltro {
  data_inicio: string; // ISO 
  data_fim: string;     // ISO
  tipo?: 'entrada' | 'saida'; 
  produto_id?: string;       
}


export interface RelatorioItem {
  data: string;               // VAI SER convertido para DD/MM/AAAA no frontend (RN21)
  produto_nome: string;
  tipo: 'entrada' | 'saida';
  quantidade: number;
}
