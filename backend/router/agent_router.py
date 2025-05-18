from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schema.agent_schema import ComandoRequest, ComandoResponse
from utils.agent_parser import interpretar_comando

from service.agent_service import AgentService
from database.connection import get_db

router = APIRouter(prefix="/agente", tags=["Agente Inteligente"])


@router.post("/interpretar-comando", response_model=ComandoResponse)
def interpretar_comando_endpoint(
    request: ComandoRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint que interpreta e executa comandos em linguagem natural relacionados a movimentações ou consultas.
    """
    comando_interpretado = interpretar_comando(request.comando)
    service = AgentService(db)
    resposta = service.executar_comando(comando_interpretado)
    return resposta
