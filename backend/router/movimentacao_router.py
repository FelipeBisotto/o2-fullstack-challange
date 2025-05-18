from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from service.movimentacao_service import MovimentacaoService
from schema.movimentacao_schema import MovimentacaoCreate, MovimentacaoRead
from database.connection import get_db

router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])

@router.post("/", response_model=MovimentacaoRead, status_code=status.HTTP_201_CREATED, summary="Registrar nova movimentação de estoque")
def registrar_movimentacao(mov: MovimentacaoCreate, db: Session = Depends(get_db)):
    try:
        service = MovimentacaoService(db)
        return service.registrar_movimentacao(mov)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[MovimentacaoRead], summary="Listar todas as movimentações")
def listar_movimentacoes(db: Session = Depends(get_db)):
    service = MovimentacaoService(db)
    return service.listar_todas()

@router.get("/produto/{produto_id}", response_model=list[MovimentacaoRead], summary="Listar movimentações de um produto")
def listar_por_produto(produto_id: int, db: Session = Depends(get_db)):
    service = MovimentacaoService(db)
    return service.listar_por_produto(produto_id)
