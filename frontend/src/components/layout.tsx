import { Outlet, Link } from 'react-router-dom';
import './layout.css';

export default function Layout() {
  return (
    <div className="layout-container">
      <header className="navbar">
        <h1 className="logo">FbbStock</h1>
        <nav>
          <ul className="nav-links">
            <li><Link to="/produtos">Produtos</Link></li>
            <li><Link to="/movimentacoes">Movimentações</Link></li>
            <li><Link to="/agente">Agente Inteligente</Link></li>
            <li><Link to="/dashboard">Dashboard</Link></li>
            <li><Link to="/relatorios">Relatórios</Link></li>
          </ul>
        </nav>
      </header>

      <main className="main-content">
        <Outlet />
      </main>

      <footer className="footer">
        © 2025 FBB - Sistema de Gestão de Estoque
      </footer>
    </div>
  );
}
