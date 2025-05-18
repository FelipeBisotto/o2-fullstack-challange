import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import date
from sqlalchemy.orm import Session
from database.connection import get_db, Base, engine
from model.produto import Produto
from model.movimentacao import Movimentacao

client = TestClient(app)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def setup_dados():
    db: Session = next(get_db())
    db.query(Movimentacao).delete()
    db.query(Produto).delete()

    produto = Produto(
        nome="Lápis Preto",
        descricao="Lápis de escrever",
        categoria="Escritorio",
        preco_unitario=1.50,
        quantidade=200
    )
    db.add(produto)
    db.commit()
    db.refresh(produto)

    movimentacoes = [
        Movimentacao(tipo="entrada", quantidade=100,
                     data=date(2024, 6, 1), produto_id=produto.id),
        Movimentacao(tipo="saida", quantidade=20, data=date(
            2024, 6, 2), produto_id=produto.id),
    ]
    db.add_all(movimentacoes)
    db.commit()
    db.close()

# RR032, RR034, RR035
def test_relatorio_estoque_json(setup_dados):
    response = client.get(
        "/relatorios/estoque?format=json&data_inicio=2024-01-01&data_fim=2024-12-31")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item["nome"] == "Lápis Preto" for item in data)

# RR033, RR034
def test_relatorio_estoque_csv(setup_dados):
    response = client.get(
        "/relatorios/estoque?format=csv&data_inicio=2024-01-01&data_fim=2024-12-31")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    content = response.content.decode("utf-8")
    assert "Lápis Preto" in content
    assert "Produto,Quantidade Disponível,Valor Total" in content or "Produto,Quantidade Disponível,Valor Total (R$)" in content

# RR033 (PDF retornado)
def test_relatorio_estoque_pdf(setup_dados):
    response = client.get(
        "/relatorios/estoque?format=pdf&data_inicio=2024-01-01&data_fim=2024-12-31")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.headers["content-disposition"] == "attachment; filename=relatorio_estoque.pdf"
    assert response.content.startswith(b"%PDF") or len(response.content) > 50
