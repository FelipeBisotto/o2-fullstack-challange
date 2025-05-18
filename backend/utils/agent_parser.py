import re
from datetime import datetime
from fastapi import HTTPException
from schema.agent_schema import ComandoInterpretado

VERBO_MOVIMENTACAO = "movimentar"
VERBO_CONSULTA = "consultar"
TIPOS_MOVIMENTACAO = ["entrada", "saida", "saída"]

def interpretar_comando(comando: str) -> ComandoInterpretado:
    comando = comando.lower()

    # Ação: movimentar ou consultar
    if VERBO_MOVIMENTACAO in comando and any(t in comando for t in TIPOS_MOVIMENTACAO):
        acao = "movimentar"
    elif VERBO_CONSULTA in comando or re.search(r"de\s+\d{2}/\d{2}/\d{4}\s+até\s+\d{2}/\d{2}/\d{4}", comando):
        acao = "consultar"
    else:
        raise HTTPException(
            status_code=400,
            detail="Comando não reconhecido. Exemplos válidos:\n"
                   "- 'Movimentar entrada de 10 lápis no dia 14/05/2025'\n"
                   "- 'Consultar vendas de 01/05/2025 até 10/05/2025'\n"
                   "- 'Consultar vendas no dia 15/05/2025'"
        )

    tipo = None
    produto = None
    quantidade = None
    data = None
    data_inicio = None
    data_fim = None
    periodo_texto = None

    # MOVIMENTAÇÃO
    if acao == "movimentar":
        # Tipo
        if "entrada" in comando:
            tipo = "entrada"
        elif "saida" in comando or "saída" in comando:
            tipo = "saida"

        # Quantidade
        match_qtd = re.search(r"\b(\d+)\b", comando)
        if match_qtd:
            quantidade = int(match_qtd.group(1))

        # Produto
        match_produto = re.search(
            r"movimentar\s+(?:entrada|sa[íi]da)\s+de\s+\d+\s+(.+?)(?:\s+no\s+dia|\s+em\s+\d{2}/\d{2}/\d{4}|$)", comando)
        if match_produto:
            produto = match_produto.group(1).strip()

        # Data explícita ou padrão hoje
        match_data = re.search(r"(\d{2}/\d{2}/\d{4})", comando)
        if match_data:
            try:
                data = datetime.strptime(match_data.group(1), "%d/%m/%Y").date()
            except ValueError:
                data = None
        else:
            data = datetime.today().date()

    # CONSULTA
    elif acao == "consultar":
        # Intervalo: "de 01/04/2025 até 10/04/2025"
        match = re.search(r"de\s+(\d{2}/\d{2}/\d{4})\s+até\s+(\d{2}/\d{2}/\d{4})", comando)
        if match:
            try:
                data_inicio = datetime.strptime(match.group(1), "%d/%m/%Y").date()
                data_fim = datetime.strptime(match.group(2), "%d/%m/%Y").date()
                periodo_texto = f"{match.group(1)} até {match.group(2)}"
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data inválido no intervalo.")

        # Data única: "no dia 15/05/2025"
        else:
            unica = re.search(r"no\s+dia\s+(\d{2}/\d{2}/\d{4})", comando)
            if unica:
                try:
                    data_unica = datetime.strptime(unica.group(1), "%d/%m/%Y").date()
                    data_inicio = data_fim = data_unica
                    periodo_texto = f"no dia {unica.group(1)}"
                except ValueError:
                    raise HTTPException(status_code=400, detail="Formato de data inválido na consulta.")
            else:
                raise HTTPException(status_code=400, detail="Informe uma data ou intervalo para consulta.")

    return ComandoInterpretado(
        acao=acao,
        tipo=tipo,
        produto=produto,
        quantidade=quantidade,
        data=data,
        data_inicio=data_inicio,
        data_fim=data_fim,
        periodo_texto=periodo_texto
    )
