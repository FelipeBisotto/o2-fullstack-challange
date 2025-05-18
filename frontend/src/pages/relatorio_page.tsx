import { useState } from 'react';
import {
  obterRelatorioFiltrado,
  baixarRelatorioCSV,
  baixarRelatorioPDF,
} from '../service/relatorio_service';
import type { RelatorioItem } from '../schema/relatorio_schema';
import './relatorio_page.css';
import PageTitle from '@/components/page_title';

export default function RelatorioPage() {
  const [dataInicio, setDataInicio] = useState('');
  const [dataFim, setDataFim] = useState('');
  const [relatorio, setRelatorio] = useState<RelatorioItem[]>([]);
  const [carregando, setCarregando] = useState(false);

  const handleBuscar = async () => {
    if (!dataInicio || !dataFim) {
      alert('Por favor, preencha as datas de início e fim.');
      return;
    }

    setCarregando(true);
    try {
      const dados = await obterRelatorioFiltrado({
        data_inicio: dataInicio,
        data_fim: dataFim,
      });
      setRelatorio(dados);
    } catch (error) {
      console.error('Erro ao buscar relatório:', error);
      alert('Erro ao buscar relatório.');
    } finally {
      setCarregando(false);
    }
  };

  const handleExportarCSV = async () => {
    if (!dataInicio || !dataFim) {
      alert('Preencha as datas para exportar.');
      return;
    }

    await baixarRelatorioCSV({
      data_inicio: dataInicio,
      data_fim: dataFim,
    });
  };

  const handleExportarPDF = async () => {
    if (!dataInicio || !dataFim) {
      alert('Preencha as datas para exportar.');
      return;
    }

    await baixarRelatorioPDF({
      data_inicio: dataInicio,
      data_fim: dataFim,
    });
  };

  return (
    <div className="container">
      <PageTitle texto="Relatórios" />

      <div className="filtros">
        <label>
          Data Início:
          <input
            type="date"
            value={dataInicio}
            onChange={(e) => setDataInicio(e.target.value)}
          />
        </label>

        <label>
          Data Fim:
          <input
            type="date"
            value={dataFim}
            onChange={(e) => setDataFim(e.target.value)}
          />
        </label>

        <div className="botoes-filtros">
          <button onClick={handleBuscar}>Buscar</button>
          <button onClick={handleExportarCSV}>Exportar CSV</button>
          <button onClick={handleExportarPDF}>Exportar PDF</button>
        </div>
      </div>

      {carregando && <p>Carregando relatório...</p>}

      {!carregando && relatorio.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>Data</th>
              <th>Produto</th>
              <th>Tipo</th>
              <th>Quantidade</th>
            </tr>
          </thead>
          <tbody>
            {relatorio.map((item, index) => (
              <tr key={index}>
                <td>{item.data}</td>
                <td>{item.produto_nome}</td>
                <td>{item.tipo}</td>
                <td>{item.quantidade}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {!carregando && relatorio.length === 0 && (
        <p className="mensagem-central">
          Nenhum dado encontrado para o período selecionado.
        </p>
      )}
    </div>
  );
}
