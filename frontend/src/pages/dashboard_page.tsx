import { useEffect, useState } from "react";
import { getDashboardData } from "../service/dashboard_service";
import type { DashboardResponse } from "../schema/dashboard_schema";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import "./dashboard_page.css";
import PageTitle from '@/components/page_title';

const formatarMoeda = (valor: number): string =>
  new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(valor);

const DashboardPage = () => {
  const hoje = new Date();
  const umAnoAtras = new Date(hoje);
  umAnoAtras.setFullYear(hoje.getFullYear() - 1);

  const [dataInicio, setDataInicio] = useState<string>(
    umAnoAtras.toISOString().split("T")[0]
  );
  const [dataFim, setDataFim] = useState<string>(
    hoje.toISOString().split("T")[0]
  );
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [erro, setErro] = useState<string>("");

  const carregarDados = async () => {
    try {
      setErro("");
      setLoading(true);
      const resultado = await getDashboardData(
        new Date(dataInicio),
        new Date(dataFim)
      );
      setData(resultado);
    } catch (err) {
      console.error("Erro ao obter dados do dashboard:", err);
      setErro("Erro ao carregar dados. Tente novamente mais tarde.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    carregarDados();
  }, []);

  return (
    <div className="dashboard-container">
      <PageTitle texto="Dashboard" />

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

        <button onClick={carregarDados}>Buscar Gráfico de Vendas Mensais</button>
      </div>

      {loading && <p>Carregando...</p>}
      {erro && <p className="erro">{erro}</p>}

      {!loading && data && (
        <>
          <section className="resumo">
            <h2>Resumo</h2>
            <p>
              <strong>Valor total em estoque:</strong>{" "}
              {formatarMoeda(data.valor_total_estoque)}
            </p>
            <p>
              <strong>Total de itens vendidos:</strong>{" "}
              {data.quantidade_total_itens_vendidos}
            </p>
          </section>

          {data.grafico_vendas_mensais.length > 0 && (
            <section className="grafico">
              <h2>Gráfico de Vendas Mensais</h2>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={data.grafico_vendas_mensais}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="mes" />
                  <YAxis />
                  <Tooltip formatter={(value) => formatarMoeda(Number(value))} />
                  <Bar dataKey="total_vendas" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </section>
          )}

          <section className="produtos">
            <h2>Produtos em Estoque</h2>
            {data.produtos_estoque.length > 0 ? (
              <table>
                <thead>
                  <tr>
                    <th>Produto</th>
                    <th>Quantidade</th>
                    <th>Valor Total</th>
                  </tr>
                </thead>
                <tbody>
                  {data.produtos_estoque.map((p, index) => (
                    <tr key={index}>
                      <td>{p.nome}</td>
                      <td>{p.quantidade_disponivel}</td>
                      <td>{formatarMoeda(p.valor_total)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>Nenhum produto em estoque.</p>
            )}
          </section>
        </>
      )}
    </div>
  );
};

export default DashboardPage;
