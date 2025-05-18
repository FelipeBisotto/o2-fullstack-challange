import { obterDashboard } from "../repository/dashboard_repository";
import type { DashboardResponse } from "../schema/dashboard_schema";

const formatarDataISO = (data: Date): string => {
  return data.toISOString().split("T")[0];
};

// RN20 – Se não forem informadas datas, assume os últimos 12 meses
export const getDashboardData = async (
  dataInicio?: Date,
  dataFim?: Date
): Promise<DashboardResponse> => {
  const hoje = new Date();

  const fim = dataFim ?? hoje;
  const inicio = dataInicio ?? new Date(fim.getFullYear() - 1, fim.getMonth(), fim.getDate());

  const inicioStr = formatarDataISO(inicio);
  const fimStr = formatarDataISO(fim);

  return await obterDashboard(inicioStr, fimStr);
};
