import { interpretarComando } from '../repository/agent_repository';
import type { ComandoAgente, RespostaAgente } from '../schema/agent_schema';
import { formatarData } from '../utils/formatters';

export const processarComando = async (
  entrada: ComandoAgente
): Promise<RespostaAgente> => {
  const resposta = await interpretarComando(entrada);

  // RN21 (relatórios), RF36 – formatar datas legíveis para exibição
  if (resposta.data_movimentacao) {
    resposta.data_movimentacao = formatarData(resposta.data_movimentacao);
  }
  if (resposta.data_inicio) {
    resposta.data_inicio = formatarData(resposta.data_inicio);
  }
  if (resposta.data_fim) {
    resposta.data_fim = formatarData(resposta.data_fim);
  }

  if (resposta.mensagem) {
    resposta.mensagem = resposta.mensagem.trim();
  }

  return resposta;
};
