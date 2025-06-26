# estagio1
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
import time

# define uma classe chamada Browser que automatiza a abertura de páginas da web 
# usando o navegador Google Chrome com Selenium WebDriver.

class Browser:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        ]
        chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def pagina(self, url):
        self.driver.get(url)
        time.sleep(3)

        if "detected unusual traffic" in self.driver.page_source.lower():
            print("CAPTCHA detectado.")
            return None

        return self.driver.page_source

    def fechar(self):
        try:
            self.driver.quit()
        except Exception:
            pass
