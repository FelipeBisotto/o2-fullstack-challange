from datetime import date, datetime, time  # importar time e datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from schema.agent_schema import ComandoInterpretado, ComandoResponse
from schema.movimentacao_schema import MovimentacaoCreate
from service.movimentacao_service import MovimentacaoService
from service.dashboard_service import DashboardService
from repository.produto_repository import buscar_produto_por_nome


class AgentService:
    def __init__(self, db: Session):
        self.db = db
        self.movimentacao_service = MovimentacaoService(db)
        self.dashboard_service = DashboardService(db)

    def executar_comando(self, comando: ComandoInterpretado) -> ComandoResponse:
        if comando.acao == "movimentar":
            return self._executar_movimentacao(comando)
        elif comando.acao == "consultar":
            return self._executar_consulta(comando)
        else:
            raise HTTPException(status_code=400, detail="Ação inválida. Use 'movimentar' ou 'consultar'.")

    def _executar_movimentacao(self, comando: ComandoInterpretado) -> ComandoResponse:
        produto = buscar_produto_por_nome(self.db, comando.produto)
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto '{comando.produto}' não encontrado.")

        if comando.tipo not in ["entrada", "saida"]:
            raise HTTPException(status_code=400, detail="Tipo de movimentação inválido. Use 'entrada' ou 'saida'.")

        if comando.data != date.today():
            raise HTTPException(status_code=400, detail="Movimentações só podem ser registradas com a data atual.")

        dados = MovimentacaoCreate(
            tipo=comando.tipo,
            quantidade=comando.quantidade,
            data=comando.data,
            produto_id=produto.id
        )

        self.movimentacao_service.registrar_movimentacao(dados)

        return ComandoResponse(
            tipo_acao="movimentar",
            tipo_movimentacao=comando.tipo,
            nome_produto=produto.nome,
            quantidade=comando.quantidade,
            data_movimentacao=comando.data,
            mensagem=f"Movimentação de {comando.tipo} registrada com sucesso para o produto '{produto.nome}' ({comando.quantidade} unidade(s))."
        )

    def _executar_consulta(self, comando: ComandoInterpretado) -> ComandoResponse:
        data_inicio = comando.data_inicio or comando.data
        data_fim = comando.data_fim or comando.data

        if not data_inicio or not data_fim:
            raise HTTPException(status_code=400, detail="Comando de consulta incompleto. Informe uma data ou período para consulta.")

        # Ajuste para incluir todo o dia final
        inicio_dt = datetime.combine(data_inicio, time.min)
        fim_dt = datetime.combine(data_fim, time.max)

        resposta = self.dashboard_service.obter_dados_dashboard(inicio_dt, fim_dt)
        total_vendas = resposta.total_vendas
        total_itens = resposta.total_itens_vendidos

        if comando.periodo_texto:
            periodo = comando.periodo_texto
        elif data_inicio == data_fim:
            periodo = f"no dia {data_inicio.strftime('%d/%m/%Y')}"
        else:
            periodo = f"de {data_inicio.strftime('%d/%m/%Y')} até {data_fim.strftime('%d/%m/%Y')}"

        return ComandoResponse(
            tipo_acao="consultar",
            data_inicio=data_inicio,
            data_fim=data_fim,
            mensagem=f"Foram vendidos {total_itens} item(ns), totalizando R$ {total_vendas:,.2f} em vendas {periodo}.".replace(",", "X").replace(".", ",").replace("X", ".")

        )
