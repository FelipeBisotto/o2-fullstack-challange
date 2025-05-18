from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date

from database.connection import Base, engine, SessionLocal
from model.produto import Produto
from model.movimentacao import Movimentacao
from router import produto_router, movimentacao_router
from router.dashboard_router import router as dashboard_router
from router.relatorio_router import router as relatorio_router
from router import agent_router

app = FastAPI(
    title="API de Gestão de Estoque",
    description="API para controle de produtos e movimentações de estoque",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

def popular_dados_iniciais():
    db: Session = SessionLocal()
    print("Populando banco com dados iniciais...")

    # Dados iniciais dos produtos
    dados_produtos = [
        {"nome": "Monitor 27", "descricao": "Monitor LED Full HD 27 polegadas", "categoria": "TI", "preco_unitario": 1200.0, "quantidade": 100},
        {"nome": "Notebook", "descricao": "Notebook com 16GB RAM e SSD 512GB", "categoria": "TI", "preco_unitario": 4500.0, "quantidade": 100},
        {"nome": "Computador", "descricao": "PC Gamer com RTX 3060 e Ryzen 7", "categoria": "TI", "preco_unitario": 7500.0, "quantidade": 100},
        {"nome": "Impressora", "descricao": "Impressora multifuncional sem fio", "categoria": "TI", "preco_unitario": 850.0, "quantidade": 100},
        {"nome": "Teclado", "descricao": "Teclado mecânico RGB para gamers", "categoria": "TI", "preco_unitario": 450.0, "quantidade": 100},
        {"nome": "Caneta verde", "descricao": "Caneta esferográfica tinta vermelha 1.0mm", "categoria": "Office", "preco_unitario": 2.5, "quantidade": 50},
        {"nome": "Caneta preta", "descricao": "Caneta esferográfica tinta azul 1.0mm", "categoria": "Office", "preco_unitario": 2.5, "quantidade": 50},
    ]

    entradas = [10, 20, 30, 40, 50]
    datas_entrada = ["2024-11-30", "2024-12-31", "2025-01-31", "2025-02-28", "2025-03-31"]

    saidas = [5, 10, 15, 20, 25]
    datas_saida = ["2024-12-31", "2025-01-31", "2025-02-28", "2025-03-31", "2025-04-30"]

    for dados in dados_produtos:
        produto_existente = db.query(Produto).filter_by(nome=dados["nome"]).first()

        if not produto_existente:
            produto = Produto(**dados)
            db.add(produto)
            db.flush()  # garante ID imediato
        else:
            produto = produto_existente

        # Entradas
        for qtd, data_str in zip(entradas, datas_entrada):
            mov_entrada = Movimentacao(
                produto_id=produto.id,
                tipo="entrada",
                quantidade=qtd,
                data=date.fromisoformat(data_str)
            )
            db.add(mov_entrada)
            db.flush()
            print(f"✔ Entrada: {produto.nome} ({qtd}) em {data_str}")

        # Saídas
        for qtd, data_str in zip(saidas, datas_saida):
            mov_saida = Movimentacao(
                produto_id=produto.id,
                tipo="saida",
                quantidade=qtd,
                data=date.fromisoformat(data_str)
            )
            db.add(mov_saida)
            db.flush()
            print(f"✔ Saída: {produto.nome} ({qtd}) em {data_str}")

    db.commit()
    db.close()
    print("Dados populados com sucesso!")

# Executa o populate ao iniciar
popular_dados_iniciais()

# Rotas da aplicação
app.include_router(produto_router)
app.include_router(movimentacao_router)
app.include_router(dashboard_router)
app.include_router(relatorio_router)
app.include_router(agent_router.router)
