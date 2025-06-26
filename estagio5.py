# estagio5 
from fpdf import FPDF, XPos, YPos
import json
import os
import re

ARQ_JSON = r"C:\Users\Thais\Desktop\mreport\relatorios\relatorio_classificado.json"
PASTA_TEXTOS = r"C:\Users\Thais\Desktop\mreport\relatorios\textos_finais"
PDF_OUTPUT = r"C:\Users\Thais\Desktop\mreport\relatorios\relatorio_final.pdf"

def limpar_texto(texto):
    texto = texto.replace("\u2013", "-").replace("\u2014", "-")
    texto = texto.replace("\u2018", "'").replace("\u2019", "'")
    texto = texto.replace("\u201c", '"').replace("\u201d", '"')
    texto = re.sub(r"[^\x00-\x7F]+", "", texto)
    return texto.strip()

def extrair_titulo(caminho_txt):
    if not os.path.exists(caminho_txt):
        return "Título não encontrado"

    with open(caminho_txt, "r", encoding="utf-8") as f:
        for linha in f:
            if linha.strip().lower().startswith("título:"):
                return limpar_texto(linha.split(":", 1)[-1])
    return "Título não encontrado"

def extrair_corpo(caminho_txt):
    if not os.path.exists(caminho_txt):
        return "Texto não disponível"

    with open(caminho_txt, "r", encoding="utf-8") as f:
        conteudo = f.read()

    match = re.search(r"CORPO DA NOT[IÍ]CIA:\s*(.+?)(\n===|\Z)", conteudo, re.DOTALL | re.IGNORECASE)
    if match:
        return limpar_texto(match.group(1))
    return "Texto não disponível"

def gerar_pdf():
    if not os.path.exists(ARQ_JSON):
        print("[ERRO] Arquivo JSON não encontrado")
        return

    with open(ARQ_JSON, "r", encoding="utf-8") as f:
        dados = json.load(f)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Título geral do relatório
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "RELATÓRIO DE MALWARES DE TODAS PÁGINAS ENCONTRADAS", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    for arquivo, info in dados.items():
        caminho_txt = os.path.join(PASTA_TEXTOS, arquivo)

        titulo_real = extrair_titulo(caminho_txt)
        corpo = extrair_corpo(caminho_txt)
        classificacoes = info.get("classificacoes", [])

        # TÍTULO
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 8, f"Título: {titulo_real}", align="L")

        # CLASSIFICAÇÕES
        if classificacoes:
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(0, 0, 180)  # azul
            pdf.cell(0, 8, "Classificações de Malware:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(0, 0, 0)
            for c in classificacoes:
                classif = limpar_texto(c.get("classificacao", "N/D"))
                categoria = limpar_texto(c.get("categoria", "N/D"))
                texto_final = f"- {classif} ({categoria})"
                pdf.cell(0, 8, texto_final, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        else:
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 8, "Nenhuma classificação encontrada.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # ORIGEM
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 7, f"Origem: {arquivo}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # CORPO
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 8, corpo, align="J")

        pdf.ln(5)

    pdf.output(PDF_OUTPUT)
    print(f"[OK] PDF gerado com sucesso: {PDF_OUTPUT}")

if __name__ == "__main__":
    gerar_pdf()
