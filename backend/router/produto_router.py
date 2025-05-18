from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from service.produto_service import ProdutoService
from schema.produto_schema import ProdutoCreate, ProdutoUpdate, ProdutoRead
from database.connection import get_db

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("/", response_model=ProdutoRead, status_code=status.HTTP_201_CREATED, summary="Criar um novo produto")
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    try:
        service = ProdutoService(db)
        return service.criar_produto(produto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ProdutoRead], summary="Listar todos os produtos")
def listar_produtos(db: Session = Depends(get_db)):
    service = ProdutoService(db)
    return service.listar_produtos()

@router.get("/{produto_id}", response_model=ProdutoRead, summary="Buscar produto por ID")
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    service = ProdutoService(db)
    produto = service.buscar_por_id(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.put("/{produto_id}", response_model=ProdutoRead, summary="Atualizar um produto existente")
def atualizar_produto(produto_id: int, dados: ProdutoUpdate, db: Session = Depends(get_db)):
    try:
        service = ProdutoService(db)
        return service.atualizar_produto(produto_id, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Excluir um produto")
def deletar_produto(
    produto_id: int,
    confirmado: bool = Query(False),
    db: Session = Depends(get_db)
):
    try:
        service = ProdutoService(db)
        service.deletar_produto(produto_id, confirmado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
