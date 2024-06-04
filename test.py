
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

def create_firefox_driver(url, headless=False):
    # Ruta al binario de geckodriver
    geckodriver_path = "/usr/local/bin/geckodriver" 

    # Configurar las opciones del navegador
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    if headless:
        print('Mode headless')
        options.add_argument('--headless')

    service = Service(geckodriver_path)

    driver = webdriver.Firefox(options=options)
    
    driver.get(url)
    
    return driver

# Ejemplo de uso
url = "https://www.example.com"
driver = create_firefox_driver(url)
print(driver.title)
driver.quit()
