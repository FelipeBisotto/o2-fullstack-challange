import { useState } from 'react';
import { processarComando } from '../service/agent_service';
import type { ComandoAgente, RespostaAgente } from '../schema/agent_schema';
import "./agent_page.css";
import PageTitle from '@/components/page_title';

export default function AgentePage() {
  const [comando, setComando] = useState('');
  const [resposta, setResposta] = useState<RespostaAgente | null>(null);
  const [erro, setErro] = useState('');
  const [carregando, setCarregando] = useState(false);

  const handleInterpretar = async () => {
    setErro('');
    setResposta(null);

    if (!comando.trim()) {
      setErro('Por favor, digite um comando.');
      return;
    }

    setCarregando(true);
    try {
      const dados = await processarComando({ comando } as ComandoAgente);
      setResposta(dados);
    } catch (err) {
      console.error(err);
      setErro(`Erro. Verifique se o formato da data é valido e se o produto foi cadastrado.`);


    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="container">
      <PageTitle texto="Agente Inteligente" />

      <div className="instrucoes">
        <p><strong>Exemplos de comandos:</strong></p>
        <ul>
          <li>Consultar vendas no dia <em>15/05/2025</em></li>
          <li>Consultar vendas de <em>01/05/2025 até 10/05/2025</em></li>
          <li>Movimentar entrada de <em>10 lapis branco no dia 15/05/2025</em></li>
          <li>Movimentar saída de <em>10 lápis branco no dia 15/05/2025</em></li>
        </ul>
      </div>

      <div className="input-comando">
        <textarea
          rows={4}
          value={comando}
          onChange={(e) => setComando(e.target.value)}
        />
        <button onClick={handleInterpretar} disabled={carregando}>
          {carregando ? 'Interpretando...' : 'Interpretar Comando'}
        </button>
      </div>

      {erro && <p className="erro">{erro}</p>}

      {resposta && (
        <div className="resposta">
          <h3>Resultado</h3>
          <p><strong>Ação:</strong> {resposta.tipo_acao}</p>
          {resposta.tipo_acao === 'movimentar' && (
            <>
              <p><strong>Tipo de Movimentação:</strong> {resposta.tipo_movimentacao}</p>
              <p><strong>Produto:</strong> {resposta.nome_produto}</p>
              <p><strong>Quantidade:</strong> {resposta.quantidade}</p>
              <p><strong>Data da Movimentação:</strong> {resposta.data_movimentacao}</p>
            </>
          )}
          {resposta.tipo_acao === 'consultar' && (
            <>
              <p><strong>Período:</strong> {resposta.data_inicio} até {resposta.data_fim}</p>
            </>
          )}
          {resposta.mensagem && (
            <p><strong>Mensagem:</strong> {resposta.mensagem}</p>
          )}
        </div>
      )}
    </div>
  );
}
