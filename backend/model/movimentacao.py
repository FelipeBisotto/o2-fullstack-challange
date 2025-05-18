from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database.connection import Base
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.sql import func

class Movimentacao(Base):
    __tablename__ = "movimentacao"

    id = Column(Integer, primary_key=True, index=True) 
    tipo = Column(String(10), nullable=False)
    quantidade = Column(Integer, nullable=False)
   
    data = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    produto_id = Column(Integer, ForeignKey("produto.id"), nullable=False)

    produto = relationship("Produto", backref="movimentacoes")

    __table_args__ = (
        CheckConstraint("tipo IN ('entrada', 'saida')", name="check_tipo_valido"),
        CheckConstraint("quantidade > 0", name="check_quantidade_positiva"),
    )
