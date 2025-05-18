import './produto_page.css';
import { useEffect, useState } from 'react';
import type { Produto, ProdutoFormDataManual } from '@/schema/produto_schema';
import {
  getProdutos,
  createProduto,
  updateProduto,
  deleteProduto,
} from '@/repository/produto_repository';
import {
  ordenarProdutosPorNome,
  formatarPreco,
  calcularValorTotal,
  normalizarForm,
} from '@/service/produto_service';

import Modal from '@/components/modal';
import Alert from '@/components/alert';
import Loader from '@/components/loader';
import {
  required,
  greaterThanZero,
  greaterThanOrEqualToZero,
  uniqueName,
  validate,
} from '@/utils/validators';
import PageTitle from '@/components/page_title';

export default function ProdutoPage() {
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [alerta, setAlerta] = useState<{ type: 'success' | 'danger'; message: string } | null>(null);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [produtoAtual, setProdutoAtual] = useState<Produto | null>(null);

  const [formData, setFormData] = useState<ProdutoFormDataManual>({
    nome: '',
    descricao: '',
    categoria: '',
    preco_unitario: '',
    quantidade: '',
  });

  const [formErrors, setFormErrors] = useState<Record<string, string | null>>({});

  useEffect(() => {
    carregarProdutos();
  }, []);

  const carregarProdutos = async () => {
    setLoading(true);
    try {
      const response = await getProdutos();
      const ordenados = ordenarProdutosPorNome(response.data);
      setProdutos(ordenados);
    } catch (err: any) {
      setErro('Erro ao carregar produtos: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    if (formErrors[name]) {
      setFormErrors((prev) => ({ ...prev, [name]: null }));
    }
  };

  const validateForm = () => {
    const errors: Record<string, string | null> = {};

    errors.nome = validate(formData.nome, [
      required,
      (value) => uniqueName(value, produtos, produtoAtual?.id),
    ]);
    errors.categoria = required(formData.categoria);
    errors.preco_unitario = validate(formData.preco_unitario, [required, greaterThanZero]);
    errors.quantidade = validate(formData.quantidade, [required, greaterThanOrEqualToZero]);

    setFormErrors(errors);

    return !Object.values(errors).some((err) => err !== null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      const dados = normalizarForm(formData);

      setLoading(true);
      if (produtoAtual) {
        await updateProduto(produtoAtual.id, dados);
        setAlerta({ type: 'success', message: 'Produto atualizado com sucesso!' });
      } else {
        await createProduto(dados);
        setAlerta({ type: 'success', message: 'Produto criado com sucesso!' });
      }
      await carregarProdutos();
      fecharModal();
    } catch (err: any) {
      setAlerta({ type: 'danger', message: 'Erro: ' + err.message });
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (produto: Produto) => {
    setProdutoAtual(produto);
    setFormData({
      nome: produto.nome,
      descricao: produto.descricao || '',
      categoria: produto.categoria,
      preco_unitario: produto.preco_unitario.toString(),
      quantidade: produto.quantidade.toString(),
    });
    setIsModalOpen(true);
  };

  const handleDelete = async () => {
    if (!produtoAtual) return;

    try {
      setLoading(true);
      await deleteProduto(produtoAtual.id);
      await carregarProdutos();
      setAlerta({ type: 'success', message: 'Produto excluído com sucesso!' });
      setIsDeleteModalOpen(false);
    } catch (err: any) {
      const mensagem = err?.response?.data?.detail || err.message;

      if (mensagem.includes('movimentações registradas')) {
        setAlerta({
          type: 'danger',
          message: ' Não é possível excluir produtos que já possuem movimentações de entrada ou saída.',
        });
      } else {
        setAlerta({ type: 'danger', message: 'Erro ao excluir produto: ' + mensagem });
      }
    } finally {
      setLoading(false);
    }
  };

  const confirmarExclusao = (produto: Produto) => {
    setProdutoAtual(produto);
    setIsDeleteModalOpen(true);
  };

  const abrirNovoModal = () => {
    setProdutoAtual(null);
    setFormData({
      nome: '',
      descricao: '',
      categoria: '',
      preco_unitario: '',
      quantidade: '',
    });
    setFormErrors({});
    setIsModalOpen(true);
  };

  const fecharModal = () => {
    setProdutoAtual(null);
    setIsModalOpen(false);
    setFormErrors({});
  };

  return (
    <div className="container">
      <PageTitle texto="Cadastro e Listagem de Produtos" />

      {alerta && (
        <Alert
          type={alerta.type}
          message={alerta.message}
          onClose={() => setAlerta(null)}
        />
      )}

      <div className="card">
        <div className="card-header">
          <button className="btn btn-primary" onClick={abrirNovoModal}>
            Cadastrar Novo Produto
          </button>
        </div>

        {loading && <Loader />}
        {erro && <div className="alert alert-danger">{erro}</div>}

        {!loading && !erro && (
          <table className="table">
            <thead>
              <tr>
                <th>Produto</th>
                <th>Categoria</th>
                <th>Preço Unitário</th>
                <th>Quantidade</th>
                <th>Valor Total</th>
                <th>Ferramentas</th>
              </tr>
            </thead>
            <tbody>
              {produtos.length === 0 ? (
                <tr>
                  <td colSpan={6} style={{ textAlign: 'center' }}>
                    Nenhum produto encontrado.
                  </td>
                </tr>
              ) : (
                produtos.map((produto) => (
                  <tr key={produto.id}>
                    <td className="coluna-produto">{produto.nome}</td>
                    <td>{produto.categoria}</td>
                    <td>{formatarPreco(produto.preco_unitario)}</td>
                    <td>{produto.quantidade}</td>
                    <td>{formatarPreco(calcularValorTotal(produto))}</td>
                    <td style={{ textAlign: 'center' }}>
                      <div className="acoes-container">
                        <button className="btn btn-sm btn-primary" onClick={() => handleEdit(produto)}>
                          Editar
                        </button>
                        <button className="btn btn-sm btn-danger" onClick={() => confirmarExclusao(produto)}>
                          Excluir
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        )}
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={fecharModal}
        title={produtoAtual ? 'Editar Produto' : 'Novo Produto'}
        footer={
          <>
            <button className="btn btn-secondary" onClick={fecharModal}>
              Cancelar
            </button>
            <button className="btn btn-primary" onClick={handleSubmit}>
              {loading ? 'Salvando...' : 'Salvar'}
            </button>
          </>
        }
      >
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Nome *</label>
            <input
              type="text"
              name="nome"
              value={formData.nome}
              onChange={handleInputChange}
              className="form-control"
            />
            {formErrors.nome && <div className="form-error">{formErrors.nome}</div>}
          </div>

          <div className="form-group">
            <label>Descrição</label>
            <textarea
              name="descricao"
              value={formData.descricao}
              onChange={handleInputChange}
              className="form-control"
            />
          </div>

          <div className="form-group">
            <label>Categoria *</label>
            <input
              type="text"
              name="categoria"
              value={formData.categoria}
              onChange={handleInputChange}
              className="form-control"
            />
            {formErrors.categoria && <div className="form-error">{formErrors.categoria}</div>}
          </div>

          <div className="form-group">
            <label>Preço Unitário *</label>
            <input
              type="number"
              name="preco_unitario"
              value={formData.preco_unitario}
              onChange={handleInputChange}
              step="0.01"
              min="0.01"
              className="form-control"
            />
            {formErrors.preco_unitario && (
              <div className="form-error">{formErrors.preco_unitario}</div>
            )}
          </div>

          <div className="form-group">
            <label>Quantidade *</label>
            <input
              type="number"
              name="quantidade"
              value={formData.quantidade}
              onChange={handleInputChange}
              min="0"
              step="1"
              className="form-control"
            />
            {formErrors.quantidade && (
              <div className="form-error">{formErrors.quantidade}</div>
            )}
          </div>
        </form>
      </Modal>

      <Modal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        title="Confirmar Exclusão"
        footer={
          <>
            <button className="btn btn-secondary" onClick={() => setIsDeleteModalOpen(false)}>
              Cancelar
            </button>
            <button className="btn btn-danger" onClick={handleDelete}>
              {loading ? 'Excluindo...' : 'Confirmar Exclusão'}
            </button>
          </>
        }
      >
        <p>Tem certeza que deseja excluir o produto "{produtoAtual?.nome}"?</p>
        <p>Essa ação não poderá ser desfeita.</p>
        <br/>
        <p>OBS: Produtos com movimentações não pode ser excluídos.</p>
      </Modal>
    </div>
  );
}