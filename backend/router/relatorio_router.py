from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import date, timedelta, datetime, time
from io import StringIO
import csv

from model.movimentacao import Movimentacao
from model.produto import Produto
from database.connection import get_db
from service.dashboard_service import DashboardService
from utils.export_utils import exportar_estoque_para_pdf
from schema.relatorio_schema import RelatorioMovimentacaoItem

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.get("/estoque")
def gerar_relatorio_estoque(
    format: str = Query("json", description="Formato de saída: json, csv ou pdf"),
    db: Session = Depends(get_db),
    data_inicio: date = Query(None, description="Data inicial (AAAA-MM-DD)"),
    data_fim: date = Query(None, description="Data final (AAAA-MM-DD)")
):
    if not data_inicio or not data_fim:
        data_fim = date.today()
        data_inicio = data_fim - timedelta(days=365)

    #  Converte para datetime (para compatibilidade com dashboard_service)
    data_inicio = datetime.combine(data_inicio, time.min)
    data_fim = datetime.combine(data_fim, time.max)

    dashboard_service = DashboardService(db)
    dados = dashboard_service.obter_dados_dashboard(data_inicio, data_fim)
    produtos = dados.produtos_em_estoque

    if format == "csv":
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Produto", "Quantidade Disponível", "Valor Total (R$)"])
        for item in produtos:
            writer.writerow([item.nome, item.quantidade_disponivel, f"{item.valor_total:.2f}"])
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=relatorio_estoque.csv"}
        )

    elif format == "pdf":
        output = exportar_estoque_para_pdf(produtos, data_inicio, data_fim)
        return StreamingResponse(
            output,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=relatorio_estoque.pdf"}
        )

    return produtos


@router.get("/movimentacoes", response_model=list[RelatorioMovimentacaoItem])
def gerar_relatorio_movimentacoes(
    data_inicio: date = Query(..., description="Data inicial (AAAA-MM-DD)"),
    data_fim: date = Query(..., description="Data final (AAAA-MM-DD)"),
    db: Session = Depends(get_db)
):
    data_fim_completo = datetime.combine(data_fim, time.max)  # inclui o dia todo

    resultado = (
        db.query(Movimentacao)
        .join(Produto)
        .filter(Movimentacao.data >= data_inicio, Movimentacao.data <= data_fim_completo)
        .all()
    )

    return [
        RelatorioMovimentacaoItem(
            data=mov.data.date(),
            produto_nome=mov.produto.nome,
            tipo=mov.tipo,
            quantidade=mov.quantidade
        )
        for mov in resultado
    ]
