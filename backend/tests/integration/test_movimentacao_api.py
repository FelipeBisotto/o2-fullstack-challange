import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
from datetime import date, timedelta

client = TestClient(app)

BASE_URL_PRODUTO = "/produtos/"
BASE_URL_MOV = "/movimentacoes/"


@pytest.fixture
def produto_valido():
    payload = {
        "nome": f"Produto Teste {uuid4()}",
        "descricao": "Descricao para movimentacao",
        "categoria": "Estoque",
        "preco_unitario": 50.0,
        "quantidade": 10
    }
    response = client.post(BASE_URL_PRODUTO, json=payload)
    assert response.status_code == 201
    return response.json()

# RN09, RN10, RN11, RN12, RN14
# Testa o registro bem-sucedido de uma movimentacao de entrada.
def test_criar_movimentacao_entrada_sucesso(produto_valido):
    mov_payload = {
        "tipo": "entrada",
        "quantidade": 5,
        "data": str(date.today()),
        "produto_id": produto_valido["id"]
    }
    response = client.post(BASE_URL_MOV, json=mov_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["tipo"] == "entrada"
    assert data["quantidade"] == 5
    assert data["produto_id"] == produto_valido["id"]

# RN09
# Testa a tentativa de criar movimentacao com produto inexistente.
def test_movimentacao_produto_inexistente():
    mov_payload = {
        "tipo": "entrada",
        "quantidade": 5,
        "data": str(date.today()),
        "produto_id": 999999  # ID inexistente
    }
    response = client.post(BASE_URL_MOV, json=mov_payload)
    assert response.status_code == 400
    assert "produto associado" in response.json()["detail"].lower()

# RN10
# Testa a tentativa de criar movimentacao com quantidade zero.
def test_movimentacao_quantidade_invalida(produto_valido):
    mov_payload = {
        "tipo": "entrada",
        "quantidade": 0,
        "data": str(date.today()),
        "produto_id": produto_valido["id"]
    }
    response = client.post(BASE_URL_MOV, json=mov_payload)
    assert response.status_code == 422  # Validação do Pydantic

# RN11
# Testa a falha ao registrar movimentação com data futura.
def test_movimentacao_data_futura(produto_valido):
    mov_payload = {
        "tipo": "entrada",
        "quantidade": 1,
        "data": str(date.today() + timedelta(days=1)),
        "produto_id": produto_valido["id"]
    }
    response = client.post(BASE_URL_MOV, json=mov_payload)
    assert response.status_code == 400
    assert "data da movimentacao" in response.json()["detail"].lower().replace("ç", "c").replace("ã", "a")

# RN12
# Testa a tentativa de criar movimentacao com tipo inválido.
def test_movimentacao_tipo_invalido(produto_valido):
    mov_payload = {
        "tipo": "reajuste",
        "quantidade": 1,
        "data": str(date.today()),
        "produto_id": produto_valido["id"]
    }
    response = client.post(BASE_URL_MOV, json=mov_payload)
    assert response.status_code == 422  # Validação automática do Pydantic

# RN13
# Testa a tentativa de movimentacao de saida maior que o estoque.
def test_movimentacao_saida_maior_que_estoque(produto_valido):
    mov_payload = {
        "tipo": "saida",
        "quantidade": produto_valido["quantidade"] + 5,
        "data": str(date.today()),
        "produto_id": produto_valido["id"]
    }
    response = client.post(BASE_URL_MOV, json=mov_payload)
    assert response.status_code == 400
    assert "quantidade insuficiente" in response.json()["detail"].lower()

# RN14
# Testa se a quantidade do produto é atualizada após uma movimentação de entrada
def test_movimentacao_entrada_atualiza_estoque(produto_valido):
    produto_id = produto_valido["id"]
    estoque_anterior = produto_valido["quantidade"]

    mov_payload = {
        "tipo": "entrada",
        "quantidade": 3,
        "data": str(date.today()),
        "produto_id": produto_id
    }

    response = client.post(BASE_URL_MOV, json=mov_payload)
    assert response.status_code == 201

    atualizado = client.get(f"{BASE_URL_PRODUTO}{produto_id}")
    assert atualizado.status_code == 200
    assert atualizado.json()["quantidade"] == estoque_anterior + 3


# RN15
# Testa que uma movimentacao nao pode ser atualizada ou deletada.
def test_movimentacao_nao_editavel_ou_excluivel(produto_valido):
    mov_payload = {
        "tipo": "entrada",
        "quantidade": 1,
        "data": str(date.today()),
        "produto_id": produto_valido["id"]
    }
    post = client.post(BASE_URL_MOV, json=mov_payload)
    assert post.status_code == 201
    movimentacao_id = post.json()["id"]

    put = client.put(f"{BASE_URL_MOV}{movimentacao_id}", json=mov_payload)
    delete = client.delete(f"{BASE_URL_MOV}{movimentacao_id}")

    assert put.status_code in [404, 405]
    assert delete.status_code in [404, 405]
