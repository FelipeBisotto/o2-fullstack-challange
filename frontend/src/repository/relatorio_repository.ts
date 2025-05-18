import api from '../service/api';
import type { RelatorioFiltro } from '../schema/relatorio_schema';

export const buscarRelatorioMovimentacoes = async (filtro: RelatorioFiltro) => {
  const response = await api.get('/relatorios/movimentacoes', {
    params: {
      data_inicio: filtro.data_inicio,
      data_fim: filtro.data_fim,
    },
  });
  return response.data;
};

export const buscarRelatorioJSON = async (filtro: RelatorioFiltro) => {
  const response = await api.get('/relatorios/estoque', {
    params: {
      data_inicio: filtro.data_inicio,
      data_fim: filtro.data_fim,
      format: 'json',
    },
  });
  return response.data;
};

export const exportarRelatorioCSV = async (filtro: RelatorioFiltro) => {
  const response = await api.get('/relatorios/estoque', {
    params: {
      data_inicio: filtro.data_inicio,
      data_fim: filtro.data_fim,
      format: 'csv',
    },
    responseType: 'blob',
  });
  return response;
};

export const exportarRelatorioPDF = async (filtro: RelatorioFiltro) => {
  const response = await api.get('/relatorios/estoque', {
    params: {
      data_inicio: filtro.data_inicio,
      data_fim: filtro.data_fim,
      format: 'pdf',
    },
    responseType: 'blob',
  });
  return response;
};
