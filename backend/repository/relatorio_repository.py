from sqlalchemy.orm import Session
from model.movimentacao import Movimentacao
from model.produto import Produto
from datetime import date
from typing import List
from sqlalchemy import and_

class RelatorioRepository:
    @staticmethod
    def buscar_movimentacoes(db: Session, data_inicio: date, data_fim: date) -> List[Movimentacao]:
        return db.query(Movimentacao).join(Produto).filter(
            and_(
                Movimentacao.data >= data_inicio,
                Movimentacao.data <= data_fim
            )
        ).order_by(Movimentacao.data.asc()).all()
