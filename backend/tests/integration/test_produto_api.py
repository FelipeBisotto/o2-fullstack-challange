import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4

client = TestClient(app)

BASE_URL = "/produtos/"

@pytest.fixture
def produto_payload():
    return {
        "nome": "Produto Teste",
        "descricao": "Descricao de teste",
        "categoria": "Categoria X",
        "preco_unitario": 100.0,
        "quantidade": 10
    }

# RN01, RN02, RN03, RN04, RN05
# Testa a criação bem-sucedida de um produto com dados válidos.
def test_criar_produto_sucesso(produto_payload):
    
    produto_payload["nome"] = f"Produto Teste {uuid4()}"  # Garante nome único
    response = client.post(BASE_URL, json=produto_payload)

    print("STATUS:", response.status_code)
    print("RESPONSE JSON:", response.json())
    print("RESPONSE TEXT:", response.text)

    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == produto_payload["nome"]
    assert data["quantidade"] == produto_payload["quantidade"]


# RN01
# Testa a falha ao tentar criar um produto com nome vazio.
def test_criar_produto_falha_nome_vazio(produto_payload):
    produto_payload["nome"] = "   "  
    response = client.post(BASE_URL, json=produto_payload)
    assert response.status_code == 400
    assert "nome do produto" in response.json()["detail"].lower()

# Testa a listagem de todos os produtos cadastrados.
def test_listar_produtos():
    response = client.get(BASE_URL)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Testa se um produto recém-criado pode ser recuperado por seu ID.
def test_buscar_produto_por_id(produto_payload):
    produto_payload["nome"] = f"Produto Teste {uuid4()}"
    post = client.post(BASE_URL, json=produto_payload)
    assert post.status_code == 201, f"Erro ao criar produto: {post.status_code} - {post.text}"
    produto_id = post.json()["id"]
    ...

# RN07
# Testa a atualização de um produto, incluindo validações dos campos atualizados.
def test_atualizar_produto_sucesso(produto_payload):
    produto_payload["nome"] = f"Produto Teste {uuid4()}"
    post = client.post(BASE_URL, json=produto_payload)
    produto_id = post.json()["id"]

    novo_nome = f"Produto Atualizado {uuid4()}"
    update_payload = {
        "nome": novo_nome,
        "quantidade": 20
    }

    response = client.put(f"{BASE_URL}{produto_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["nome"] == novo_nome
    assert response.json()["quantidade"] == 20

# RN08
# Testa a tentativa de deletar um produto sem confirmação explícita.
def test_deletar_produto_sem_confirmacao(produto_payload):
    produto_payload["nome"] = f"Produto Teste {uuid4()}"
    post = client.post(BASE_URL, json=produto_payload)
    produto_id = post.json()["id"]

    response = client.delete(f"{BASE_URL}{produto_id}")
    assert response.status_code == 400
    assert "exclusão não confirmada" in response.json()["detail"].lower()

# RN08
# Testa a exclusão bem-sucedida de um produto com confirmação explícita.
def test_deletar_produto_com_confirmacao(produto_payload):
    produto_payload["nome"] = f"Produto Teste {uuid4()}"
    post = client.post(BASE_URL, json=produto_payload)
    produto_id = post.json()["id"]

    response = client.delete(f"{BASE_URL}{produto_id}?confirmado=true")
    assert response.status_code == 204
