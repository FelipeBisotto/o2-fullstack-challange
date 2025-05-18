import sys
from unittest.mock import MagicMock
sys.modules["psycopg2"] = MagicMock()

import pytest
from datetime import date, timedelta
from unittest.mock import patch, MagicMock
from schema.movimentacao_schema import MovimentacaoCreate
from service.movimentacao_service import MovimentacaoService
from model.produto import Produto
from pydantic import ValidationError



@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def service(mock_db):
    return MovimentacaoService(db=mock_db)


def make_mov(tipo="entrada", quantidade=5, dias=0, produto_id=1):
    return MovimentacaoCreate(
        tipo=tipo,
        quantidade=quantidade,
        data=date.today() + timedelta(days=dias),
        produto_id=produto_id
    )

# RN09
# Testa a falha ao registrar movimentação com produto inexistente.
def test_rn09_produto_inexistente(service):
    mov = make_mov(quantidade=1)
    with patch("service.movimentacao_service.buscar_produto", return_value=None), \
         patch("service.movimentacao_service.atualizar_estoque"), \
         patch("service.movimentacao_service.salvar_movimentacao"):
        with pytest.raises(ValueError, match="Produto associado à movimentação não encontrado."):
            service.registrar_movimentacao(mov)

# RN10
# Testa a falha ao registrar movimentação com quantidade zero.
def test_rn10_quantidade_invalida():
    with pytest.raises(ValidationError, match="greater than 0"):
        make_mov(quantidade=0)


# RN11
# Testa a falha ao registrar movimentação com data futura.
def test_rn11_data_futura(service):
    mov = make_mov(dias=1)
    with patch("repository.movimentacao_repository.buscar_produto", return_value=Produto()):
        with pytest.raises(ValueError, match="A data da movimentação não pode ser no futuro."):
            service.registrar_movimentacao(mov)

# RN12
# Testa a falha ao instanciar movimentação com tipo inválido.
def test_rn12_tipo_invalido():
    with pytest.raises(ValidationError, match="entrada|saida"):
        make_mov(tipo="teste")

# RN13
# Testa a falha ao registrar movimentação de saída com estoque insuficiente.
def test_rn13_saida_estoque_insuficiente(service):
    produto = Produto()
    produto.quantidade = 2  # Atribuição manual
    mov = make_mov(tipo="saida", quantidade=5)
    with patch("service.movimentacao_service.buscar_produto", return_value=produto):
        with pytest.raises(ValueError, match="Quantidade insuficiente em estoque."):
            service.registrar_movimentacao(mov)

# RN14 + RN15
# Testa movimentação de entrada e saída com atualização automática de estoque e registro final.
def test_rn14_entrada_saida_sucesso(service):
    produto = Produto()
    produto.quantidade = 10

    entrada = make_mov(tipo="entrada", quantidade=5)
    with patch("service.movimentacao_service.buscar_produto", return_value=produto), \
         patch("service.movimentacao_service.atualizar_estoque") as mock_update, \
         patch("service.movimentacao_service.salvar_movimentacao", return_value="ok") as mock_save:

        result = service.registrar_movimentacao(entrada)
        mock_update.assert_called_once()
        mock_save.assert_called_once()
        assert produto.quantidade == 15
        assert result == "ok"

    saida = make_mov(tipo="saida", quantidade=5)
    with patch("service.movimentacao_service.buscar_produto", return_value=produto), \
         patch("service.movimentacao_service.atualizar_estoque") as mock_update, \
         patch("service.movimentacao_service.salvar_movimentacao", return_value="ok") as mock_save:

        result = service.registrar_movimentacao(saida)
        mock_update.assert_called_once()
        mock_save.assert_called_once()
        assert produto.quantidade == 10
        assert result == "ok"

def test_listagens(service):
    with patch("service.movimentacao_service.listar_movimentacoes", return_value=["m1"]) as mock_all, \
         patch("service.movimentacao_service.listar_movimentacoes_por_produto", return_value=["m2"]) as mock_prod:

        assert service.listar_todas() == ["m1"]
        assert service.listar_por_produto(123) == ["m2"]
        mock_all.assert_called_once()
        mock_prod.assert_called_once_with(service.db, 123)

