import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from '@/components/layout';
import ProdutoPage from '@/pages/produto_page';
import MovimentacaoPage from '@/pages/movimentacao_page';
import DashboardPage from '@/pages/dashboard_page';
import RelatorioPage from '@/pages/relatorio_page';
import AgentePage from '@/pages/agent_page';

export function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<ProdutoPage />} />
          <Route path="produtos" element={<ProdutoPage />} />
          <Route path="movimentacoes" element={<MovimentacaoPage />} />
          <Route path="dashboard" element={<DashboardPage/>}/>
          <Route path="relatorios" element={<RelatorioPage/>}/>
          <Route path="agente" element={<AgentePage/>}/>
        </Route>
      </Routes>
    </Router>
  );
}
