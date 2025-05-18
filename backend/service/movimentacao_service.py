
from datetime import datetime, date, timezone
from sqlalchemy.orm import Session
from model.movimentacao import Movimentacao
from schema.movimentacao_schema import MovimentacaoCreate
from repository.movimentacao_repository import (
    buscar_produto,
    salvar_movimentacao,
    listar_movimentacoes,
    listar_movimentacoes_por_produto,
)

class MovimentacaoService:
    def __init__(self, db: Session):
        self.db = db

    def registrar_movimentacao(self, dados: MovimentacaoCreate) -> Movimentacao:
        if dados.quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        if dados.tipo not in ["entrada", "saida"]:
            raise ValueError("Tipo de movimentação inválido.")

        produto = buscar_produto(self.db, dados.produto_id)
        if not produto:
            raise ValueError(
                "Produto associado à movimentação não encontrado.")

        if dados.tipo == "saida":
            if produto.quantidade < dados.quantidade:
                raise ValueError("Quantidade insuficiente em estoque.")
            produto.quantidade -= dados.quantidade
        else:  
            produto.quantidade += dados.quantidade

        nova = Movimentacao(**dados.dict(), data=datetime.now(timezone.utc))
        return salvar_movimentacao(self.db, produto, nova)

    def listar_todas(self) -> list[Movimentacao]:
        movimentacoes = listar_movimentacoes(self.db)

        for m in movimentacoes:
            m.produto_nome = m.produto.nome  

        return movimentacoes 

    def listar_por_produto(self, produto_id: int) -> list[Movimentacao]:
        return listar_movimentacoes_por_produto(self.db, produto_id)
