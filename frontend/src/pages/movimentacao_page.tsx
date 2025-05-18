import './movimentacao_page.css';
import { useEffect, useState } from 'react';
import type { Movimentacao, MovimentacaoFormData } from '@/schema/movimentacao_schema';
import { movimentacaoFormSchema } from '@/schema/movimentacao_schema';
import { getMovimentacoes, createMovimentacao } from '@/repository/movimentacao_repository';
import {
  formatarData,
  ordenarMovimentacoesPorData,
  classeTipoMovimentacao
} from '@/service/movimentacao_service';
import { getProdutos } from '@/repository/produto_repository';
import type { Produto } from '@/schema/produto_schema';

// Nova tipagem para o estado do formulário
type MovimentacaoFormState = {
  produto_id: string;
  tipo: 'entrada' | 'saida';
  quantidade: number;
};

export default function MovimentacaoPage() {
  const [movimentacoes, setMovimentacoes] = useState<Movimentacao[]>([]);
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [formData, setFormData] = useState<MovimentacaoFormState>({
    produto_id: '',
    tipo: 'entrada',
    quantidade: 1,

  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [mensagem, setMensagem] = useState<string | null>(null);

  useEffect(() => {
    carregarMovimentacoes();
    carregarProdutos();
  }, []);

  async function carregarMovimentacoes() {
    try {
      const res = await getMovimentacoes();
      setMovimentacoes(res.data);
    } catch (err) {
      console.error('Erro ao buscar movimentações:', err);
    }
  }

  async function carregarProdutos() {
    try {
      const res = await getProdutos();
      setProdutos(res.data);
    } catch (err) {
      console.error('Erro ao buscar produtos:', err);
    }
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'quantidade' ? Number(value) : value
    }));
    setErrors({});
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const dadosConvertidos: MovimentacaoFormData = {
      ...formData,
      produto_id: parseInt(formData.produto_id, 10)
    };

    const validacao = movimentacaoFormSchema.safeParse(dadosConvertidos);
    if (!validacao.success) {
      const novosErros: Record<string, string> = {};
      validacao.error.errors.forEach(err => {
        if (err.path.length > 0) {
          novosErros[err.path[0].toString()] = err.message;
        }
      });
      setErrors(novosErros);
      return;
    }

    try {
      await createMovimentacao(validacao.data); 
      setMensagem('Movimentação registrada com sucesso.');
      setFormData({
        produto_id: '',
        tipo: 'entrada',
        quantidade: 1,
      });
      await carregarMovimentacoes();
    } catch (err) {
      setMensagem('Erro ao registrar movimentação.');
      console.error(err);
    }
  }

  return (
    <div className="container">
      <h1 className="page-title">Movimentações de Estoque</h1>

      {mensagem && <div className="alert alert-info">{mensagem}</div>}

      <form className="card" onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Produto *</label>
          <select
            name="produto_id"
            value={formData.produto_id}
            onChange={handleChange}
            className="form-control"
          >
            <option value="">Selecione um produto</option>
            {produtos.map((p) => (
              <option key={p.id} value={p.id.toString()}>
                {p.nome}
              </option>
            ))}
          </select>
          {errors.produto_id && <div className="form-error">{errors.produto_id}</div>}
        </div>

        <div className="form-group">
          <label>Tipo *</label>
          <select name="tipo" value={formData.tipo} onChange={handleChange} className="form-control">
            <option value="entrada">Entrada</option>
            <option value="saida">Saída</option>
          </select>
          {errors.tipo && <div className="form-error">{errors.tipo}</div>}
        </div>

        <div className="form-group">
          <label>Quantidade *</label>
          <input
            type="number"
            name="quantidade"
            value={formData.quantidade}
            onChange={handleChange}
            className="form-control"
            min={1}
          />
          {errors.quantidade && <div className="form-error">{errors.quantidade}</div>}
        </div>


        <button type="submit" className="btn btn-primary">
          Registrar Movimentação
        </button>
      </form>

      <div className="card">
        <h2>Histórico de Movimentações</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Produto</th>
              <th>Tipo</th>
              <th>Quantidade</th>
              <th>Data</th>
            </tr>
          </thead>
          <tbody>
            {movimentacoes.map((m) => (
              <tr key={m.id} className={classeTipoMovimentacao(m.tipo)}>
                <td>{m.produto_nome || `#${m.produto_id}`}</td>
                <td>{m.tipo === 'entrada' ? 'Entrada' : 'Saída'}</td>
                <td>{m.quantidade}</td>
<td>{new Date(m.data).toLocaleDateString('pt-BR', {
  day: '2-digit',
  month: '2-digit',
  year: 'numeric'
})}</td>


              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
