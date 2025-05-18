import api from '../service/api';
import type { ComandoAgente, RespostaAgente } from '../schema/agent_schema';

// Envia o comando textual para o agente inteligente e retorna a resposta interpretada
export const interpretarComando = async (
  comando: ComandoAgente
): Promise<RespostaAgente> => {
  const response = await api.post('/agente/interpretar-comando', comando);
  return response.data;
};
