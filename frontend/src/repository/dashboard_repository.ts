import axios from "axios";
import type { DashboardResponse } from "../schema/dashboard_schema";

const BASE_URL = "http://localhost:8000/dashboard";

export const obterDashboard = async (
  dataInicio: string,
  dataFim: string
): Promise<DashboardResponse> => {
  const response = await axios.get(BASE_URL, {
    params: {
      data_inicio: dataInicio,
      data_fim: dataFim,
    },
  });

  const raw = response.data;

  return {
    valor_total_estoque: raw.valor_total_estoque ?? 0,
    quantidade_total_itens_vendidos: raw.total_itens_vendidos ?? 0,
    produtos_estoque: raw.produtos_em_estoque ?? [],
    grafico_vendas_mensais: Array.isArray(raw.grafico_saidas_mensal)
      ? raw.grafico_saidas_mensal.map((item: any) => ({
          mes: item.mes ?? "Mês",
          total_vendas: item.valor_total_saida ?? 0,
        }))
      : []
  };
};
