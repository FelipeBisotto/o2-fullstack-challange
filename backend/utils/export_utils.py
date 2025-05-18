from io import BytesIO
from fpdf import FPDF

def formatar_valor(valor: float) -> str:
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def exportar_estoque_para_pdf(produtos_em_estoque, data_inicio, data_fim):
    pdf = FPDF()
    pdf.add_page()

    largura_total = 160
    margem_lateral = (210 - largura_total) / 2

    col1 = 80
    col2 = 40
    col3 = 40

    # Título
    pdf.set_font("Arial", 'B', 13)
    pdf.set_x(margem_lateral)
    pdf.cell(largura_total, 10, txt="Relatório de Estoque", ln=True, align='C')

    # Período
    periodo_str = f"Período: de {data_inicio.strftime('%d/%m/%Y')} até {data_fim.strftime('%d/%m/%Y')}"
    pdf.set_font("Arial", '', 11)
    pdf.set_x(margem_lateral)
    pdf.cell(largura_total, 8, txt=periodo_str, ln=True, align='C')
    pdf.ln(8)

    # Cabeçalho – azul claro
    pdf.set_fill_color(173, 216, 230)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_x(margem_lateral)
    pdf.cell(col1, 10, "Produto", 1, align='C', fill=True)
    pdf.cell(col2, 10, "Quantidade", 1, align='C', fill=True)
    pdf.cell(col3, 10, "Valor Total (R$)", 1, align='C', fill=True)
    pdf.ln()

    # Dados da tabela
    pdf.set_font("Arial", size=11)
    total_geral = 0
    fill = False

    for item in produtos_em_estoque:
        nome = item.nome[:40]
        quantidade = str(item.quantidade_disponivel)
        valor = formatar_valor(item.valor_total)

        pdf.set_x(margem_lateral)
        pdf.set_fill_color(240, 248, 255) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.cell(col1, 10, nome, 1, align='C', fill=True)
        pdf.cell(col2, 10, quantidade, 1, align='C', fill=True)
        pdf.cell(col3, 10, valor, 1, align='C', fill=True)
        pdf.ln()

        fill = not fill
        total_geral += item.valor_total

    # Total geral – azul claro
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(173, 216, 230)
    pdf.set_x(margem_lateral)
    pdf.cell(col1 + col2, 10, "Total Geral", 1, align='C', fill=True)
    pdf.cell(col3, 10, formatar_valor(total_geral), 1, align='C', fill=True)
    pdf.ln()

    # Mostrando a FastAPI
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    output = BytesIO(pdf_bytes)
    output.seek(0)
    return output
