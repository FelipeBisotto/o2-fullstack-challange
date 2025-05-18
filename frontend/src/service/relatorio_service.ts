import {
  buscarRelatorioMovimentacoes, 
  exportarRelatorioCSV,
  exportarRelatorioPDF,
} from '../repository/relatorio_repository';
import type { RelatorioFiltro, RelatorioItem } from '../schema/relatorio_schema';
import { formatarData } from '../utils/formatters';

// RN21 – Formatar data para DD/MM/AAAA
export const obterRelatorioFiltrado = async (
  filtro: RelatorioFiltro
): Promise<RelatorioItem[]> => {
  const dados = await buscarRelatorioMovimentacoes(filtro);
  return dados.map((item: RelatorioItem) => ({
    ...item,
    data: formatarData(item.data),
  }));
};

// RF29 – Exportar relatório como CSV (ESTOQUE)
export const baixarRelatorioCSV = async (filtro: RelatorioFiltro): Promise<void> => {
  const response = await exportarRelatorioCSV(filtro);
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', 'relatorio_estoque.csv');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

// RF29 – Exportar relatório como PDF (ESTOQUE)
export const baixarRelatorioPDF = async (filtro: RelatorioFiltro): Promise<void> => {
  const response = await exportarRelatorioPDF(filtro);
  const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', 'relatorio_estoque.pdf');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
