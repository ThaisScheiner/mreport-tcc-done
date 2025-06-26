import os
import re
import json
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# Base de classificação de malwares
BASE_MALWARE = {
    "worm": "Worm", "conficker": "Worm", "autorun": "Worm",
    "trojan": "Trojan", "trojanized": "Trojan", "banker": "Trojan", "dropper": "Trojan",
    "exploit": "Exploit", "zero-day": "Exploit", "0day": "Exploit", "cve": "Exploit",
    "ransomware": "Ransomware", "locker": "Ransomware", "crypto": "Ransomware", "encryptor": "Ransomware",
    "decryptor": "Ransomware", "wannacry": "Ransomware", "lockbit": "Ransomware", "revil": "Ransomware",
    "spyware": "Spyware", "keylogger": "Spyware", "logger": "Spyware", "snooper": "Spyware",
    "adware": "Adware", "popup": "Adware", "ads": "Adware",
    "rootkit": "Rootkit", "bootkit": "Rootkit", "stealth": "Rootkit",
    "virus": "Virus", "infection": "Virus", "infected": "Virus", "macro": "Virus", "file-infector": "Virus",
    "backdoor": "Backdoor", "remote-access": "Backdoor", "rat": "Backdoor",
    "builder": "Backdoor", "revshell": "Backdoor", "bindshell": "Backdoor"
}

def limpar_texto_para_pdf(texto):
    if not texto:
        return ""
    texto = texto.replace("\n", " ").replace("\r", " ")
    texto = re.sub(r"[^\wÀ-ÿ0-9 \-\.,:;()']", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()

def classificar_texto(texto, base_malware):
    texto = texto.lower()
    palavras = re.findall(r'\b\w+\b', texto)
    classificacoes = []
    palavras_encontradas = set()

    for palavra in palavras:
        if palavra in base_malware and palavra not in palavras_encontradas:
            classificacoes.append({
                "classificacao": palavra,
                "categoria": base_malware[palavra]
            })
            palavras_encontradas.add(palavra)

    return classificacoes

def processar_pasta(diretorio, resultado):
    if not os.path.exists(diretorio):
        print(f"[ERRO] Pasta não encontrada: {diretorio}")
        return

    arquivos_txt = [f for f in os.listdir(diretorio) if f.endswith(".txt")]
    if not arquivos_txt:
        print(f"[AVISO] Nenhum arquivo .txt encontrado em: {diretorio}")
        return

    for nome_arquivo in arquivos_txt:
        caminho_arquivo = os.path.join(diretorio, nome_arquivo)
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            texto = f.read()

        texto_limpo = re.sub(r"[^\w\s]", " ", texto)
        classificacoes = classificar_texto(texto_limpo, BASE_MALWARE)

        resultado[nome_arquivo] = {
            "classificacoes": classificacoes
        }

        status = "[OK]" if classificacoes else "[AVISO]"
        print(f"{status} {nome_arquivo} -> {len(classificacoes)} classificação(ões).")

def gerar_pdf_resumo_classificacoes(resultado, output_path):
    agrupado = {}

    for arquivo, dados in resultado.items():
        for c in dados.get("classificacoes", []):
            categoria = c["categoria"]
            palavra = c["classificacao"]
            if categoria not in agrupado:
                agrupado[categoria] = []
            agrupado[categoria].append((palavra, arquivo))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 12, "Resumo de Classificacoes de Malware", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(8)

    if not agrupado:
        pdf.set_font("Helvetica", "I", 12)
        pdf.cell(0, 10, "Nenhuma classificacao encontrada.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.output(output_path)
        return

    for categoria, ocorrencias in sorted(agrupado.items()):
        total = len(ocorrencias)
        categoria_limpa = limpar_texto_para_pdf(categoria.upper())

        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(0, 0, 128)
        pdf.multi_cell(0, 10, f"Categoria: {categoria_limpa} - {total} ocorrência(s)", align="L")
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(0, 0, 0)

        for palavra, arquivo in ocorrencias:
            try:
                palavra_limpa = limpar_texto_para_pdf(palavra)
                arquivo_limpo = limpar_texto_para_pdf(arquivo)
                texto = f"- {palavra_limpa} (Arquivo: {arquivo_limpo})"

                if not texto.strip():
                    continue

                # Quebra segura com largura menor (160), alinhado à esquerda
                partes = [texto[i:i+110] for i in range(0, len(texto), 110)]
                for parte in partes:
                    if parte.strip():
                        pdf.set_x(15)  # margem esquerda
                        pdf.multi_cell(160, 8, parte, align="L")

            except Exception as e:
                print(f"[ERRO ao escrever no PDF] {palavra}, {arquivo}: {e}")
                try:
                    pdf.set_x(15)
                    pdf.multi_cell(160, 8, "[ERRO AO ESCREVER LINHA]", align="L")
                except:
                    pass

        pdf.ln(4)

    pdf.output(output_path)
    print(f"[OK] PDF resumo salvo em: {output_path}")

def main():
    resultado = {}

    pastas_para_processar = [
        r"C:\Temp\tokenize",
        r"C:\Users\Thais\Desktop\mreport\relatorios\textos_finais"
    ]

    for pasta in pastas_para_processar:
        processar_pasta(pasta, resultado)

    # Caminho JSON
    pasta_saida = r"C:\Users\Thais\Desktop\mreport\relatorios"
    os.makedirs(pasta_saida, exist_ok=True)
    caminho_json = os.path.join(pasta_saida, "relatorio_classificado.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print(f"\n[SUCESSO] Arquivo relatorio_classificado.json salvo em:\n{caminho_json}")

    # Gera o PDF também
    caminho_pdf = os.path.join(pasta_saida, "resumo_classificacoes.pdf")
    gerar_pdf_resumo_classificacoes(resultado, caminho_pdf)

if __name__ == "__main__":
    main()
