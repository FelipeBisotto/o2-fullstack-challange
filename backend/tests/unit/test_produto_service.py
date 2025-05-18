import sys
from unittest.mock import MagicMock
sys.modules["psycopg2"] = MagicMock()

import pytest
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError
from service.produto_service import ProdutoService
from schema.produto_schema import ProdutoCreate, ProdutoUpdate
from model.produto import Produto
from pydantic import ValidationError


@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def service(mock_db):
    return ProdutoService(db=mock_db)

def make_produto(nome="Produto Teste", descricao="desc", categoria="cat", preco=100.0, qtd=5):
    return ProdutoCreate(
        nome=nome,
        descricao=descricao,
        categoria=categoria,
        preco_unitario=preco,
        quantidade=qtd
    )

# RN01
# Testa a falha ao criar produto com nome vazio.
def test_rn01_nome_obrigatorio(service):
    dto = make_produto(nome="  ")
    with pytest.raises(ValueError, match="O nome do produto é obrigatório."):
        service.criar_produto(dto)

# RN02
# Testa a falha ao criar produto com nome duplicado.
def test_rn02_nome_unico(service):
    dto = make_produto()
    with patch("repository.produto_repository.criar_produto", side_effect=IntegrityError("","","")):
        with pytest.raises(ValueError, match="Já existe um produto com esse nome."):
            service.criar_produto(dto)

# RN03
# Testa a falha ao criar produto com preço zero ou negativo.
def test_rn03_preco_maior_que_zero(service):
    dto = make_produto(preco=0)
    with pytest.raises(ValueError, match="O preço unitário deve ser maior que zero."):
        service.criar_produto(dto)

# RN04
# Testa a falha ao criar produto com quantidade negativa (via schema).
def test_rn04_schema_valida_quantidade_negativa():
    with pytest.raises(ValidationError, match="greater than 0"):
        ProdutoCreate(
            nome="Teste",
            descricao="Teste",
            categoria="Teste",
            preco_unitario=10.0,
            quantidade=-1
        )

# RN05
# Testa a falha ao criar produto com categoria vazia.
def test_rn05_categoria_obrigatoria(service):
    dto = make_produto(categoria=" ")
    with pytest.raises(ValueError, match="A categoria do produto é obrigatória."):
        service.criar_produto(dto)

# RN06
# Testa a falha ao tentar excluir produto com movimentações.
def test_rn06_exclusao_com_movimentacoes(service, mock_db):
    mock_db.query().filter().first.return_value = Produto()
    with patch("repository.movimentacao_repository.listar_movimentacoes_por_produto", return_value=[MagicMock()]):
        with pytest.raises(ValueError, match="Não é possível excluir um produto com movimentações registradas."):
            service.deletar_produto(1, confirmado=True)

# RN07
# Testa as validações ao atualizar um produto.
def test_rn07_validacao_update(service, mock_db):
    mock_db.query().filter().first.return_value = Produto(nome="a", categoria="b", preco_unitario=1.0, quantidade=1)

    # nome inválido
    with pytest.raises(ValueError, match="O nome do produto é obrigatório."):
        service.atualizar_produto(1, ProdutoUpdate(nome=" "))

    # categoria inválida
    with pytest.raises(ValueError, match="A categoria do produto é obrigatória."):
        service.atualizar_produto(1, ProdutoUpdate(categoria=" "))

    # preco inválido
    with pytest.raises(ValueError, match="O preço unitário deve ser maior que zero."):
        service.atualizar_produto(1, ProdutoUpdate(preco_unitario=0))

# RN07
# Testa a validação do schema ao passar quantidade negativa na atualização.
def test_rn07_schema_valida_quantidade_negativa_update():
    with pytest.raises(ValidationError, match="greater than 0"):
        ProdutoUpdate(quantidade=-10)

# RN08
# Testa a falha ao excluir produto sem confirmação explícita.
def test_rn08_exclusao_sem_confirmacao(service):
    with pytest.raises(ValueError, match="Exclusão não confirmada. Marque como confirmada para prosseguir."):
        service.deletar_produto(1, confirmado=False)

# RN09
# Testa a listagem de todos os produtos.
def test_rn09_listar_produtos(service):
    with patch("repository.produto_repository.listar_produtos", return_value=["produto1", "produto2"]) as mock_list:
        result = service.listar_produtos()
        mock_list.assert_called_once()
        assert result == ["produto1", "produto2"]

# RN10
# Testa a busca de produto por ID.
def test_rn10_buscar_por_id(service):
    with patch("repository.produto_repository.buscar_produto_por_id", return_value="produto") as mock_busca:
        result = service.buscar_por_id(123)
        mock_busca.assert_called_once_with(service.db, 123)
        assert result == "produto"
