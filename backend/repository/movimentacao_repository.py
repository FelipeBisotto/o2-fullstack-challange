from sqlalchemy.orm import Session
from model.movimentacao import Movimentacao
from model.produto import Produto
from sqlalchemy.orm import joinedload

def buscar_produto(db: Session, produto_id: int) -> Produto | None:
    return db.query(Produto).filter(Produto.id == produto_id).first()

def salvar_movimentacao(db: Session, produto: Produto, movimentacao: Movimentacao) -> Movimentacao:
    db.add(produto)
    db.add(movimentacao)
    db.commit()
    db.refresh(movimentacao)
    return movimentacao

def listar_movimentacoes(db: Session) -> list[Movimentacao]:
    return (
        db.query(Movimentacao)
        .options(joinedload(Movimentacao.produto))
        .order_by(Movimentacao.data.desc(), Movimentacao.id.desc())
        .all()
    )

def listar_movimentacoes_por_produto(db: Session, produto_id: int) -> list[Movimentacao]:
    return (
        db.query(Movimentacao)
        .filter(Movimentacao.produto_id == produto_id)
        .order_by(Movimentacao.data.desc(), Movimentacao.id.desc())
        .all()
    )

