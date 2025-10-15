from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Caminho de saída do novo PDF
output_path = "Checklist_Central_Auto_Center_Profissional.pdf"

# Configurações de estilos
styles = getSampleStyleSheet()
style_title = styles["Heading1"]
style_title.alignment = 1  # Centralizado
style_normal = styles["Normal"]

# Criação do documento
doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
elements = []

# Título
elements.append(Paragraph("<b>CHECKLIST - CENTRAL AUTO CENTER</b>", style_title))
elements.append(Spacer(1, 12))

# Informações do Cliente
elements.append(Paragraph("<b>Informações do Cliente</b>", style_normal))
client_table_data = [
    ["Nome:", "", "Carro:", ""],
    ["Placa:", "", "Ano:", ""],
    ["Km:", "", "CPF:", ""],
]
client_table = Table(client_table_data, colWidths=[50, 180, 50, 180])
client_table.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 10),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
elements.append(client_table)
elements.append(Spacer(1, 16))

# Observações do Cliente (4 linhas)
elements.append(Paragraph("<b>Observações do Cliente:</b>", style_normal))
obs_lines = [[" "], [" "], [" "], [" "]]  # 4 linhas
obs_table = Table(obs_lines, colWidths=[500], rowHeights=22)
obs_table.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
]))
elements.append(obs_table)
elements.append(Spacer(1, 20))

# Peças e Serviços (expandido até o final da página)
elements.append(Paragraph("<b>Peças e Serviços</b>", style_normal))
parts_header = [["Qtd", "Nome da Peça / Serviço", "Observação"]]
parts_rows = [["", "", ""] for _ in range(20)]  # 20 linhas
parts_table = Table(parts_header + parts_rows, colWidths=[50, 250, 200], rowHeights=22)
parts_table.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 10),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
elements.append(parts_table)

# Gera o PDF
doc.build(elements)

print(f"PDF gerado com sucesso: {output_path}")
