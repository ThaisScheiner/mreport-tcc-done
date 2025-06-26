# estagio2
from estagio1 import Browser
from datetime import datetime, timedelta
from urllib.parse import urlparse
from calendar import month_name
import os
import re

# para baixar e salvar páginas HTML de links que contêm informações 
# sobre malwares publicados nos últimos 30 dias (ou em um mês específico), 
# usando a classe Browser do Selenium

input_path = 'relatorios/links_malware_bing_ultimo_mes_completo.txt'
saida_dir = "C:/Temp/paginas"
os.makedirs(saida_dir, exist_ok=True)

# Escolher = automático(ultimos 30  dias) ou mês específico
usar_mes_especifico = True  # True = mês específico / False = Para modo automático
mes_especifico = "June"    # usado apenas se usar_mes_especifico = True
ano_especifico = 2025

# Validação do mês se modo específico
if usar_mes_especifico:
    if mes_especifico not in list(month_name):
        print(f"[ERRO] Mês inválido: {mes_especifico}")
        exit(1)
    numero_mes = list(month_name).index(mes_especifico)
    mes_escolhido = f"{ano_especifico}/{numero_mes:02d}"
    meses_validos = [mes_escolhido]
else:
    hoje = datetime.today()
    mes_atual = hoje.strftime('%Y/%m')
    mes_anterior = (hoje.replace(day=1) - timedelta(days=1)).strftime('%Y/%m')
    meses_validos = [mes_atual, mes_anterior]

# Leitura dos links
if not os.path.exists(input_path):
    print(f"[ERRO] Arquivo não encontrado: {input_path}")
    exit(1)

with open(input_path, "r", encoding="utf-8") as f:
    links = [linha.strip() for linha in f if linha.strip()]

if not links:
    print(f"[AVISO] Nenhum link para processar no arquivo: {input_path}")
    exit(0)

# Regex para extrair trecho tipo /2025/04
padrao_data_url = re.compile(r'/(\d{4}/\d{2})')

# Inicia navegador
browser = Browser()

salvos = 0
ignorados = 0

for i, link in enumerate(links):
    match = padrao_data_url.search(link)
    if match:
        data_url = match.group(1)
        if data_url not in meses_validos:
            print(f"[AVISO] Ignorando (fora do período): {link}")
            ignorados += 1
            continue
    else:
        print(f"[AVISO] Ignorando (sem data reconhecida): {link}")
        ignorados += 1
        continue

    try:
        conteudo = browser.pagina(link)
        if conteudo:
            nome_arquivo = os.path.join(saida_dir, f"pagina{salvos + 1}.html")
            with open(nome_arquivo, "w", encoding="utf-8") as arq:
                arq.write(conteudo)
            print(f"[OK] Página salva: pagina{salvos + 1}.html")
            salvos += 1
        else:
            print(f"[AVISO] Conteúdo nulo (possível CAPTCHA ou bloqueio): {link}")
    except Exception as e:
        print(f"[ERRO] Ao baixar {link}: {e}")

browser.fechar()

print(f"\n[OK] Total salvos: {salvos}")
print(f"[AVISO] Total ignorados: {ignorados}")
