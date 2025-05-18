from sqlalchemy.orm import Session
from model.produto import Produto
from schema.produto_schema import ProdutoCreate, ProdutoUpdate
from sqlalchemy import func


def criar_produto(db: Session, produto: ProdutoCreate) -> Produto:
    novo_produto = Produto(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

def listar_produtos(db: Session) -> list[Produto]:
    return db.query(Produto).all()

def buscar_produto_por_id(db: Session, produto_id: int) -> Produto | None:
    return db.query(Produto).filter(Produto.id == produto_id).first()

def atualizar_produto(db: Session, produto_id: int, dados: ProdutoUpdate) -> Produto | None:
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if produto:
        for campo, valor in dados.dict(exclude_unset=True).items():
            setattr(produto, campo, valor)
        db.commit()
        db.refresh(produto)
    return produto

def buscar_produto_por_nome(db: Session, nome: str) -> Produto | None:
    if not nome:
        return None 

    return db.query(Produto).filter(
        func.unaccent(func.lower(Produto.nome)) == func.unaccent(nome.lower())
    ).first()

def deletar_produto(db: Session, produto_id: int) -> bool:
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if produto:
        db.delete(produto)
        db.commit()
        return True
    return False
