from pydantic import BaseModel, Field, conint
from typing import Optional, Literal
from datetime import date

#inteiro estritamente positivo
StrictPositiveInt = conint(strict=True, gt=0)


class ComandoRequest(BaseModel):
    """
    Requisição enviada ao agente inteligente contendo um comando em linguagem natural.
    """
    comando: str = Field(..., description="Comando em linguagem natural", example="Movimentar entrada de 10 lápis no dia 14/05/2025")


class ComandoInterpretado(BaseModel):
    """
    Representação estruturada do comando após interpretação semântica.
    Pode ser usada internamente ou retornada para depuração/testes.
    """
    acao: Literal["movimentar", "consultar"] = Field(..., description="Verbo de ação identificado")
    tipo: Optional[Literal["entrada", "saida"]] = Field(None, description="Tipo da movimentação (entrada ou saída)")
    produto: Optional[str] = Field(None, description="Nome do produto identificado")
    quantidade: Optional[StrictPositiveInt] = Field(None, description="Quantidade da movimentação")
    data: Optional[date] = Field(None, description="Data da movimentação (deve ser a data atual)")
    data_inicio: Optional[date] = Field(None, description="Data inicial da consulta")
    data_fim: Optional[date] = Field(None, description="Data final da consulta")
    periodo_texto: Optional[str] = Field(None, description="Texto original que representa o período (ex: 'abril de 2025')")

    model_config = {
        "from_attributes": True
    }


class ComandoResponse(BaseModel):
    """
    Resposta estruturada do agente com base na interpretação e execução do comando.
    Compatível com o frontend.
    """
    tipo_acao: Literal["movimentar", "consultar"] = Field(..., description="Tipo de ação executada")
    tipo_movimentacao: Optional[Literal["entrada", "saida"]] = Field(None, description="Tipo da movimentação, se aplicável")
    nome_produto: Optional[str] = Field(None, description="Nome do produto envolvido na movimentação ou consulta")
    quantidade: Optional[int] = Field(None, description="Quantidade movimentada, se aplicável")
    data_inicio: Optional[date] = Field(None, description="Data inicial da consulta, se aplicável")
    data_fim: Optional[date] = Field(None, description="Data final da consulta, se aplicável")
    data_movimentacao: Optional[date] = Field(None, description="Data da movimentação (deve ser a data atual)")
    mensagem: Optional[str] = Field(None, description="Mensagem final retornada ao usuário")
