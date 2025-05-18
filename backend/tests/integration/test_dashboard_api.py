import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database.connection import Base, get_db
from model.produto import Produto
from model.movimentacao import Movimentacao
from datetime import date

# Banco de dados temporário para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture
def setup_dados():
    db = TestingSessionLocal()
    db.query(Movimentacao).delete()
    db.query(Produto).delete()

    produto = Produto(
        nome="Caneta Azul",
        descricao="Caneta esferográfica",
        categoria="Escritorio",
        preco_unitario=2.50,
        quantidade=100
    )
    db.add(produto)
    db.commit()
    db.refresh(produto)

    movimentacoes = [
        Movimentacao(tipo="entrada", quantidade=50, data=date(2024, 5, 1), produto_id=produto.id),
        Movimentacao(tipo="saida", quantidade=10, data=date(2024, 5, 2), produto_id=produto.id),
        Movimentacao(tipo="saida", quantidade=5, data=date(2024, 5, 10), produto_id=produto.id),
    ]
    db.add_all(movimentacoes)
    db.commit()
    db.close()

def test_dashboard_endpoint_com_dados(setup_dados):
    response = client.get("/dashboard?data_inicio=2024-01-01&data_fim=2024-12-31")  # RN17
    assert response.status_code == 200
    data = response.json()

    # RN18 – Valor total do estoque
    assert "valor_total_estoque" in data
    assert data["valor_total_estoque"] == 250.0

    # RN27 – Valor total de vendas (10 + 5) * 2.5
    assert "total_vendas" in data
    assert data["total_vendas"] == 37.5

    # RN28 – Quantidade total de itens vendidos
    assert "total_itens_vendidos" in data
    assert data["total_itens_vendidos"] == 15

    # RN16 – Produto aparece no estoque com nome e quantidade
    assert any(produto["nome"] == "Caneta Azul" for produto in data["produtos_em_estoque"])

    # RN19 – Produto aparece como mais movimentado
    assert any(produto["nome"] == "Caneta Azul" for produto in data["produtos_movimentados"])

    # RN21 – Gráfico de saídas mensais contém valores corretos
    assert isinstance(data["grafico_saidas_mensal"], list)
    assert any(mes["mes"] == "05/2024" for mes in data["grafico_saidas_mensal"])

    # RN22 – Produtos com movimentações aparecem
    assert any(historico["produto"] == "Caneta Azul" for historico in data["historico_movimentacoes"])

    # RN23 – Datas de movimentações estão presentes
    datas = [d for h in data["historico_movimentacoes"] if h["produto"] == "Caneta Azul" for d in h["todas"]]
    assert "01/05/2024" in datas and "02/05/2024" in datas

    # RN24 – Datas/quantidades de saídas separadas
    saidas = [s for h in data["historico_movimentacoes"] if h["produto"] == "Caneta Azul" for s in h["saidas"]]
    assert any(s["quantidade"] == 10 for s in saidas)

    # RN25 – Datas/quantidades de entradas separadas
    entradas = [e for h in data["historico_movimentacoes"] if h["produto"] == "Caneta Azul" for e in h["entradas"]]
    assert any(e["quantidade"] == 50 for e in entradas)

    # RN26 – Verifica tipo e quantidade de movimentações
    assert any(m["tipo"] == "saida" and m["quantidade"] == 10 for m in data["movimentacoes"])

    # RN29 – Datas devem estar no formato brasileiro
    assert all("/" in m["data"] and len(m["data"]) == 10 for m in data["movimentacoes"])

    # RN30 – Endpoint está consolidando dados
    assert isinstance(data, dict)

    # RN31 – Retorno está em JSON
    assert response.headers["content-type"] == "application/json"
