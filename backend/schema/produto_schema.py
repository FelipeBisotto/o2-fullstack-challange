from pydantic import BaseModel, Field, conint
from typing import Optional

StrictPositiveInt = conint(strict=True, gt=0)

class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    categoria: str
    preco_unitario: float
    quantidade: StrictPositiveInt = Field(..., description="Deve ser um inteiro estritamente maior que 0")

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    preco_unitario: Optional[float] = None
    quantidade: Optional[conint(strict=True, gt=0)] = Field(None, description="Se informado, deve ser um inteiro estritamente maior que 0")

class ProdutoRead(ProdutoBase):
    id: int

    model_config = {
        "from_attributes": True
    }
