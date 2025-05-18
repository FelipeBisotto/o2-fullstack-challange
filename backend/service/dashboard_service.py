from sqlalchemy.orm import Session
from datetime import datetime
from repository.dashboard_repository import DashboardRepository
from schema.dashboard_schema import (
    DashboardResponse,
    ProdutoEstoque,
    ProdutoMovimentado,
    SaidaPorMes,
    MovimentacaoResumo,
    HistoricoMovimentacoes,
    MovimentacaoDetalhada
)

from collections import defaultdict

class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def obter_dados_dashboard(self, data_inicio: datetime, data_fim: datetime) -> DashboardResponse:
        """
        Os parâmetros são datetime para garantir que movimentações com hora sejam corretamente incluídas nos filtros.
        """

        # RN16 – Buscar produtos em estoque com valor total
        produtos_estoque_raw = DashboardRepository.buscar_produtos_em_estoque(self.db)
        produtos_estoque = [
            ProdutoEstoque(
                nome=row.nome,
                quantidade_disponivel=row.quantidade_disponivel,
                valor_total=float(row.valor_total)
            ) for row in produtos_estoque_raw
        ]

        # RN18 – Calcular valor total do estoque
        valor_total_estoque = float(DashboardRepository.calcular_valor_total_estoque(self.db))

        # RN19 – Buscar produtos mais movimentados
        produtos_movimentados_raw = DashboardRepository.buscar_produtos_mais_movimentados(self.db)
        produtos_movimentados = [
            ProdutoMovimentado(
                nome=row.nome,
                total_movimentacoes=row.total_movimentacoes
            ) for row in produtos_movimentados_raw
        ]

        # RN21 – Gerar gráfico de saídas mensais
        grafico_raw = DashboardRepository.gerar_grafico_saidas_por_mes(self.db, data_inicio, data_fim)
        grafico_saidas_mensal = [
            SaidaPorMes(
                mes=f"{int(row.mes):02d}/{int(row.ano)}",
                valor_total_saida=float(row.valor_total_saida)
            ) for row in grafico_raw
        ]

        # RN27 – Calcular valor total de vendas (somente saídas)
        total_vendas = float(DashboardRepository.calcular_vendas_totais(self.db, data_inicio, data_fim))

        # RN28 – Somar total de itens vendidos
        total_itens_vendidos = int(DashboardRepository.somar_total_itens_vendidos(self.db, data_inicio, data_fim))

        # RN26 – Listar movimentações com tipo, data e quantidade
        movimentacoes_raw = DashboardRepository.buscar_movimentacoes_resumidas(self.db, data_inicio, data_fim)
        movimentacoes = [
            MovimentacaoResumo(
                produto=row.produto,
                tipo=row.tipo,
                data=row.data.strftime("%d/%m/%Y"),  # RN29 – Formato brasileiro de data
                quantidade=row.quantidade
            ) for row in movimentacoes_raw
        ]

        # RN22, RN23, RN24, RN25 – Detalhamento de movimentações por produto e tipo
        historico_raw = DashboardRepository.buscar_historico_movimentacoes(self.db, data_inicio, data_fim)
        agrupado = defaultdict(lambda: {"entradas": [], "saidas": [], "todas": set()})

        for row in historico_raw:
            data_formatada = row.data.strftime("%d/%m/%Y")  # RN29
            agrupado[row.produto]["todas"].add(data_formatada)
            if row.tipo == "entrada":
                agrupado[row.produto]["entradas"].append(MovimentacaoDetalhada(data=data_formatada, quantidade=row.quantidade))
            elif row.tipo == "saida":
                agrupado[row.produto]["saidas"].append(MovimentacaoDetalhada(data=data_formatada, quantidade=row.quantidade))

        historico_movimentacoes = [
            HistoricoMovimentacoes(
                produto=produto,
                entradas=dados["entradas"],
                saidas=dados["saidas"],
                todas=sorted(dados["todas"])
            ) for produto, dados in agrupado.items()
        ]

        # RN30 e RN31 – Consolidar dados no schema de resposta (JSON por padrão)
        return DashboardResponse(
            valor_total_estoque=valor_total_estoque,
            total_vendas=total_vendas,
            total_itens_vendidos=total_itens_vendidos,
            produtos_em_estoque=produtos_estoque,
            produtos_movimentados=produtos_movimentados,
            grafico_saidas_mensal=grafico_saidas_mensal,
            historico_movimentacoes=historico_movimentacoes,
            movimentacoes=movimentacoes
        )
