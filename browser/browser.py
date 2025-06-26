#browser.py
class Browser:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # User-Agent aleatório
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
            "Mozilla/5.0 (X11; Linux x86_64)..."
        ]
        chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def pagina(self, url):
        self.driver.get(url)
        time.sleep(3)

        # verificacao de CAPTCHA simplificada
        if "detected unusual traffic" in self.driver.page_source.lower():
            print("CAPTCHA detectado.")
            return None

        return self.driver.page_source

    def fechar(self):
        try:
            self.driver.quit()
        except Exception:
            pass
