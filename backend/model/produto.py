from sqlalchemy import Column, Integer, String, Numeric
from database.connection import Base

class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), unique=True, nullable=False)
    descricao = Column(String)
    categoria = Column(String(50), nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    quantidade = Column(Integer, nullable=False)
