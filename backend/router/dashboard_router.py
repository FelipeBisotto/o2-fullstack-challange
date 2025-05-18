from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date, timedelta, datetime, time

from database.connection import get_db
from service.dashboard_service import DashboardService
from schema.dashboard_schema import DashboardResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/", response_model=DashboardResponse)
def obter_dashboard(
    db: Session = Depends(get_db),
    data_inicio: date = Query(None, description="Data inicial (formato: AAAA-MM-DD)"),
    data_fim: date = Query(None, description="Data final (formato: AAAA-MM-DD)")
):
    # RN20 – Se não forem informadas datas, assume os últimos 12 meses
    if not data_inicio or not data_fim:
        data_fim = date.today()
        data_inicio = data_fim - timedelta(days=365)

    # Ajustando para capturar todo o intervalo do dia
    data_inicio_dt = datetime.combine(data_inicio, time.min)  # 00:00:00
    data_fim_dt = datetime.combine(data_fim, time.max)        # 23:59:59.999999

    dashboard_service = DashboardService(db)
    return dashboard_service.obter_dados_dashboard(data_inicio_dt, data_fim_dt)
