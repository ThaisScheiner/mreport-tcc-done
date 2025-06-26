import os
import re
import json
import unicodedata
from bs4 import BeautifulSoup
from fpdf import FPDF, XPos, YPos

input_dir = "C:/Temp/paginas"
output_dir = "C:/Temp/tokenize"
os.makedirs(output_dir, exist_ok=True)

relatorio_class_path = r"C:\Users\Thais\Desktop\mreport\relatorios\relatorio_classificado.json"
relatorio_links_path = r"C:\Users\Thais\Desktop\mreport\relatorios\links_malware_bing_ultimo_mes_completo.txt"

def limpar_texto(texto):
    if not texto:
        return ""
    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ASCII', 'ignore').decode('ASCII')
    texto = ''.join(ch for ch in texto if ch.isprintable())
    texto = texto.replace('\n', ' ').replace('\r', ' ')
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

# ✅ QUEBRA SEGURA COM largura máxima
def escrever_linhas(pdf, texto, fonte="Helvetica", estilo="", tamanho=11, altura_linha=7, cor=(0, 0, 0), largura=160):
    pdf.set_font(fonte, estilo, tamanho)
    pdf.set_text_color(*cor)

    texto = limpar_texto(texto)
    linhas = [texto[i:i+110] for i in range(0, len(texto), 110)]
    for linha in linhas:
        try:
            pdf.set_x(15)  # margem esquerda
            pdf.multi_cell(largura, altura_linha, linha.strip(), align="L")
        except Exception as e:
            print(f"[ERRO ao renderizar linha]: {e}")
            pdf.multi_cell(largura, altura_linha, "[ERRO AO ESCREVER LINHA]", align="L")

# Carregamento dos dados
if os.path.exists(relatorio_class_path):
    with open(relatorio_class_path, "r", encoding="utf-8") as f:
        relatorio_classificado = json.load(f)
else:
    relatorio_classificado = {}

if os.path.exists(relatorio_links_path):
    with open(relatorio_links_path, "r", encoding="utf-8") as f:
        links = [linha.strip() for linha in f if linha.strip()]
    mapa_links = {f"pagina{i+1}.html": link for i, link in enumerate(links)}
else:
    mapa_links = {}

arquivos_html = [f for f in os.listdir(input_dir) if f.endswith(".html")]

print("===== ESTÁGIO tokenize =====\n")

for arq in arquivos_html:
    input_path = os.path.join(input_dir, arq)
    pagina_num = re.findall(r'\d+', arq)
    pagina_str = pagina_num[0] if pagina_num else "?"

    with open(input_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        titulo = soup.title.string.strip() if soup.title else "Sem título"
        paragrafos = soup.find_all('p')
        corpo = "\n\n".join(p.get_text(strip=True) for p in paragrafos if p.get_text(strip=True))

    if not corpo.strip():
        print(f"[IGNORADO] Página sem conteúdo: {arq}")
        continue

    arquivo_txt = arq.replace(".html", ".txt")
    classificacoes = relatorio_classificado.get(arquivo_txt, {}).get("classificacoes", [])
    link = mapa_links.get(arq, "Link não disponível")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Título
    escrever_linhas(pdf, f"Página {pagina_str} - {limpar_texto(titulo)}", estilo="B", tamanho=14, altura_linha=9)

    pdf.ln(5)

    # Classificações
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 0, 128)
    pdf.cell(0, 8, "Classificações de Malware:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    if classificacoes:
        for c in classificacoes:
            classe = limpar_texto(c.get("classificacao", "N/D"))
            categoria = limpar_texto(c.get("categoria", "N/D"))
            escrever_linhas(pdf, f"- {classe} ({categoria})", tamanho=11)
    else:
        escrever_linhas(pdf, "Nenhuma classificação encontrada.", estilo="I", tamanho=11, cor=(100, 100, 100))

    pdf.ln(6)

    # Corpo da notícia
    escrever_linhas(pdf, limpar_texto(corpo), tamanho=11, altura_linha=7)

    pdf.ln(5)

    # Link
    escrever_linhas(pdf, f"Link: {link}", estilo="I", tamanho=10, altura_linha=6)

    # Salvar PDF
    pdf_output_path = os.path.join(output_dir, arq.replace(".html", ".pdf"))
    try:
        pdf.output(pdf_output_path)
        print(f"[OK] PDF salvo: {pdf_output_path}")
    except PermissionError:
        print(f"[ERRO] Feche o PDF aberto: {pdf_output_path}")

    # Salvar TXT
    saida_txt_path = os.path.join(output_dir, arq.replace(".html", ".txt"))
    with open(saida_txt_path, "w", encoding="utf-8") as txt_out:
        txt_out.write(f"TÍTULO: {titulo}\n\nCORPO DA NOTÍCIA:\n{corpo}")
    print(f"[OK] TXT salvo: {saida_txt_path}")

print("\n[OK] Conversão de HTML para PDF + TXT finalizada.")
