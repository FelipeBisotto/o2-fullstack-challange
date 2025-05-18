from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from model.produto import Produto
from model.movimentacao import Movimentacao
from datetime import datetime
from typing import List, Dict


class DashboardRepository:

    @staticmethod
    def buscar_produtos_em_estoque(db: Session) -> List[Dict]:
        return db.query(
            Produto.nome,
            Produto.quantidade.label("quantidade_disponivel"),
            (Produto.preco_unitario * Produto.quantidade).label("valor_total")
        ).all()

    @staticmethod
    def calcular_valor_total_estoque(db: Session) -> float:
        return db.query(
            func.coalesce(func.sum(Produto.preco_unitario * Produto.quantidade), 0.0)
        ).scalar()

    @staticmethod
    def buscar_produtos_mais_movimentados(db: Session) -> List[Dict]:
        return db.query(
            Produto.nome,
            func.count(Movimentacao.id).label("total_movimentacoes")
        ).join(Movimentacao).group_by(Produto.nome).order_by(func.count(Movimentacao.id).desc()).all()

    @staticmethod
    def gerar_grafico_saidas_por_mes(db: Session, data_inicio: datetime, data_fim: datetime) -> List[Dict]:
        return db.query(
            extract('month', Movimentacao.data).label("mes"),
            extract('year', Movimentacao.data).label("ano"),
            func.sum(Movimentacao.quantidade * Produto.preco_unitario).label("valor_total_saida")
        ).join(Produto).filter(
            Movimentacao.tipo == "saida",
            Movimentacao.data.between(data_inicio, data_fim)
        ).group_by("ano", "mes").order_by("ano", "mes").all()

    @staticmethod
    def calcular_vendas_totais(db: Session, data_inicio: datetime, data_fim: datetime) -> float:
        # Subquery blindada para garantir join e cálculo correto
        subquery = db.query(
            Movimentacao.quantidade,
            Produto.preco_unitario
        ).join(Produto).filter(
            Movimentacao.tipo == 'saida',
            func.date(Movimentacao.data).between(data_inicio.date(), data_fim.date())
        ).subquery()

        return db.query(
            func.coalesce(func.sum(subquery.c.quantidade * subquery.c.preco_unitario), 0.0)
        ).scalar()

    @staticmethod
    def somar_total_itens_vendidos(db: Session, data_inicio: datetime, data_fim: datetime) -> int:
        return db.query(
            func.coalesce(func.sum(Movimentacao.quantidade), 0)
        ).filter(
            Movimentacao.tipo == 'saida',
            func.date(Movimentacao.data).between(data_inicio.date(), data_fim.date())
        ).scalar()

    @staticmethod
    def buscar_movimentacoes_resumidas(db: Session, data_inicio: datetime, data_fim: datetime) -> List[Dict]:
        return db.query(
            Produto.nome.label("produto"),
            Movimentacao.tipo,
            Movimentacao.data,
            Movimentacao.quantidade
        ).join(Produto).filter(
            Movimentacao.data.between(data_inicio, data_fim)
        ).order_by(Movimentacao.data).all()

    @staticmethod
    def buscar_historico_movimentacoes(db: Session, data_inicio: datetime, data_fim: datetime) -> List[Dict]:
        return db.query(
            Produto.nome.label("produto"),
            Movimentacao.tipo,
            Movimentacao.data,
            Movimentacao.quantidade
        ).join(Produto).filter(
            Movimentacao.data.between(data_inicio, data_fim)
        ).order_by(Produto.nome, Movimentacao.data).all()
