#thn.py
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class Thn:
    def __init__(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def buscar_malwares_maio_2025(self, max_links=25):
        self.driver.get("https://thehackernews.com/")
        time.sleep(5)

        resultados = []
        links_adicionados = set()

        artigos = self.driver.find_elements(By.XPATH, '//div[@class="bc_latest_news"]/ul/li/a')

        for a in artigos:
            href = a.get_attribute("href")
            title = a.text.strip()

            if not href or href in links_adicionados:
                continue

            # Abrir notícia em nova aba
            self.driver.execute_script("window.open(arguments[0]);", href)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(3)

            try:
                data_element = self.driver.find_element(By.XPATH, '//div[@class="item-label"]/span')
                data_text = data_element.text.lower()

                if "2025" in data_text and ("may" in data_text or "maio" in data_text):
                    resultados.append((title, href))
                    links_adicionados.add(href)
                    print(f"Adicionado: {title} | {data_text}")
            except Exception as e:
                print(f"Erro ao obter data da notícia: {href} ({e})")

            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

            if len(resultados) >= max_links:
                break

        return resultados

    def fechar(self):
        try:
            self.driver.quit()
        except Exception:
            pass
