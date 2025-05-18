from pydantic import BaseModel
from datetime import date
from typing import Literal

class RelatorioMovimentacaoItem(BaseModel):
    data: date
    produto_nome: str
    tipo: Literal["entrada", "saida"]
    quantidade: int
