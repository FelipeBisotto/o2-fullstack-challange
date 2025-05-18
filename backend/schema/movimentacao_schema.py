from pydantic import BaseModel, Field, conint
from typing import Literal
from datetime import datetime  

StrictPositiveInt = conint(strict=True, gt=0)

class MovimentacaoBase(BaseModel):
    tipo: Literal["entrada", "saida"]
    quantidade: StrictPositiveInt = Field(..., description="Deve ser > 0")
    produto_id: StrictPositiveInt = Field(..., description="ID do produto válido")

class MovimentacaoCreate(MovimentacaoBase):
    pass  

class MovimentacaoRead(MovimentacaoBase):
    id: int
    data: datetime 
    produto_nome: str | None = None

    model_config = {
        "from_attributes": True
    }
