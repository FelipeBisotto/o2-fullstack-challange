from pydantic import BaseModel
from typing import List
from datetime import date


# RN16 – Relatório de estoque por produto
class ProdutoEstoque(BaseModel):
    nome: str
    quantidade_disponivel: int
    valor_total: float  # preco_unitario * quantidade


# RN19 – Produtos mais movimentados
class ProdutoMovimentado(BaseModel):
    nome: str
    total_movimentacoes: int


# RN21 – Gráfico de barras: total de vendas por mês
class SaidaPorMes(BaseModel):
    mes: str  # formato: MM/AAAA
    valor_total_saida: float


# RN23, RN24, RN25 – Detalhes de movimentações por tipo
class MovimentacaoDetalhada(BaseModel):
    data: str  # formato DD/MM/AAAA (RN29)
    quantidade: int


class HistoricoMovimentacoes(BaseModel):
    produto: str
    entradas: List[MovimentacaoDetalhada]
    saidas: List[MovimentacaoDetalhada]
    todas: List[str]  # datas de todas as movimentações (RN23)


# RN26 – Lista de movimentações com tipo e quantidade
class MovimentacaoResumo(BaseModel):
    produto: str
    tipo: str  # "entrada" ou "saida"
    data: str  # formato DD/MM/AAAA
    quantidade: int


# Resumo principal do Dashboard
class DashboardResponse(BaseModel):
    valor_total_estoque: float                 # RN18
    total_vendas: float                        # RN27
    total_itens_vendidos: int                 # RN28
    produtos_em_estoque: List[ProdutoEstoque] # RN16
    produtos_movimentados: List[ProdutoMovimentado]  # RN19
    grafico_saidas_mensal: List[SaidaPorMes]         # RN21
    historico_movimentacoes: List[HistoricoMovimentacoes]  # RN24, RN25
    movimentacoes: List[MovimentacaoResumo]   # RN26
