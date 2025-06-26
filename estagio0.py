# estagio0.py
from selenium import webdriver  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote_plus
from datetime import datetime, timedelta
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import time
import os
import re

site_desejado = "thehackernews.com"
usar_mes_especifico = True  # True para usar mês específico, false automaticamente busca os ultimos 30 dias
mes_especifico = "June"
ano_especifico = 2025

def gerar_mes_anterior():
    hoje = datetime.today()
    primeiro_dia_mes_atual = datetime(hoje.year, hoje.month, 1)
    mes_anterior = primeiro_dia_mes_atual - timedelta(days=1)
    nome_mes = mes_anterior.strftime('%B')
    ano = mes_anterior.year
    return nome_mes, ano

def fechar_banner_cookies(driver):
    seletores_banners = [
        'button[aria-label="Aceitar"]',
        'button#bnp_btn_accept',
        'div.bnp_desc_left button',
        'button[title="Aceitar"]',
        'input[title="Aceitar"]'
    ]
    for selector in seletores_banners:
        try:
            elemento = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            elemento.click()
            print(f"[INFO] Banner de cookies fechado com seletor: {selector}")
            return
        except:
            continue
    print("[INFO] Nenhum banner de cookies detectado ou já fechado.")

def buscar_links_bing(driver, termo, site_alvo, max_paginas=5):
    url = f"https://www.bing.com/search?q={quote_plus(termo)}"
    driver.get(url)
    fechar_banner_cookies(driver)
    todos_links = set()
    wait = WebDriverWait(driver, 15)

    for pagina in range(max_paginas):
        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.b_algo h2 a')))
            resultados = driver.find_elements(By.CSS_SELECTOR, 'li.b_algo h2 a')
            for r in resultados:
                try:
                    href = r.get_attribute("href")
                    if href and site_alvo in href:
                        todos_links.add(href)
                except Exception as e:
                    print(f"[AVISO] Erro ao acessar link: {e}")
                    continue

            print(f"Página {pagina + 1} - {len(todos_links)} links coletados até agora.")

            try:
                next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.sb_pagN')))
            except:
                print("[INFO] Botão 'Próxima' não encontrado. Fim da navegação.")
                break

            if next_button and pagina < max_paginas - 1:
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(2)
            else:
                break

        except Exception as e:
            print(f"[ERRO] Falha ao processar página {pagina + 1}: {e}")
            with open(f"pagina_erro_{pagina + 1}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            break

    return todos_links

def limpar_texto(texto):
    texto = texto.replace('\n', ' ').strip()
    texto = re.sub(r'[^\x20-\x7E]', '', texto)  # remove caracteres invisíveis
    return texto

def salvar_links_em_pdf(links, caminho_pdf, titulo_pdf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 12, titulo_pdf, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(8)
    pdf.set_font("Helvetica", size=12)

    for link in sorted(links):
        try:
            link_limpo = limpar_texto(link)
            while len(link_limpo) > 0:
                parte = link_limpo[:180]
                pdf.multi_cell(0, 8, parte)
                link_limpo = link_limpo[180:]
            pdf.ln(2)
        except Exception as e:
            print(f"[ERRO] Falha ao escrever link no PDF: {e}")
            pdf.multi_cell(0, 8, "[ERRO AO ESCREVER LINK]")

    pdf.output(caminho_pdf)
    print(f"\n[OK] Links salvos em PDF: {caminho_pdf}")

# === Execução principal ===

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Define mês e ano a usar
if usar_mes_especifico:
    nome_mes = mes_especifico
    ano = ano_especifico
else:
    nome_mes, ano = gerar_mes_anterior()

termo = f"{site_desejado} malware {nome_mes} {ano}"

print(f"\nBuscando por: {termo}")
links_encontrados = buscar_links_bing(driver, termo, site_desejado)
print(f"\nTotal de links encontrados: {len(links_encontrados)}")
driver.quit()

# Geração dos arquivos
output_dir = os.path.join(os.getcwd(), 'relatorios')
os.makedirs(output_dir, exist_ok=True)

# Arquivo .txt
output_txt = os.path.join(output_dir, f'links_malware_{nome_mes}_{ano}.txt')
if links_encontrados:
    with open(output_txt, "w", encoding="utf-8") as f:
        for link in sorted(links_encontrados):
            f.write(link + "\n")
    print(f"\n[OK] Links salvos em TXT: {output_txt}")

    # Cópia extra
    copia_simples = os.path.join(output_dir, 'links_malware_bing_ultimo_mes_completo.txt')
    with open(copia_simples, "w", encoding="utf-8") as f:
        for link in sorted(links_encontrados):
            f.write(link + "\n")
    print(f"[OK] Cópia salva para uso contínuo: {copia_simples}")

    # PDF
    output_pdf = os.path.join(output_dir, f'links_malware_{nome_mes}_{ano}.pdf')
    titulo = f"Links de Malware encontrado no The Hacker News - {nome_mes} {ano}"
    salvar_links_em_pdf(links_encontrados, output_pdf, titulo)

else:
    print("[AVISO] Nenhum link encontrado. Nenhum arquivo foi criado.")
