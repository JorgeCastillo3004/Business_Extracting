from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
import time

def open_firefox_with_profile(url, headless= True):
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
    # profile_path = "/home/jorge/.mozilla/firefox/lf4ga6zv.default-release"
    # profile = FirefoxProfile(profile_path)
    # options.profile = profile
    service = Service(geckodriver_path)
    driver = webdriver.Firefox(options=options)    
    driver.get(url)
    driver.execute_script("document.body.style.zoom='50%'")    
    return driver

def create_webdriver_with_profile(url, profile_path = '', headless=True):
    # profile_path = '/home/jorge/.mozilla/firefox/lf4ga6zv.default-release'
    """
    Crea un controlador de navegador Firefox con un perfil personalizado y opciones de navegación.

    Args:
    - profile_path (str): Ruta al directorio del perfil de Firefox.
    - headless (bool): Indica si el navegador debe ejecutarse en modo headless (sin interfaz gráfica).
    
    Returns:
    - WebDriver: Objeto del controlador de navegador Firefox configurado.
    """
    # Ruta al ejecutable de Geckodriver
    geckodriver_path = "/usr/local/bin/geckodriver" 

    # Configurar opciones del navegador
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    if headless:
        options.add_argument('--headless')

    # Crear un perfil de Firefox personalizado
    # if profile_path != '':
    profile = FirefoxProfile(profile_path)
    options.profile = profile

    # Configurar el servicio de Geckodriver
    service = Service(geckodriver_path)

    # Crear el controlador de navegador Firefox
    driver = webdriver.Firefox(options=options, service=service)

    # Configurar el agente de usuario de forma aleatoria
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
        # Agrega más agentes de usuario según sea necesario
    ]
    random_user_agent = random.choice(user_agents)
    profile.set_preference("general.useragent.override", random_user_agent)

    # Configurar la resolución de pantalla de forma aleatoria
    resolutions = [
        "1920x1080",
        "1366x768",
        "1440x900",
        # Agrega más resoluciones según sea necesario
    ]
    random_resolution = random.choice(resolutions)
    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference("intl.accept_languages", "en-US, en")
    profile.set_preference("media.navigator.permission.disabled", True)
    profile.set_preference("permissions.default.microphone", 1)
    profile.set_preference("permissions.default.camera", 1)
    profile.set_preference("dom.webnotifications.enabled", False)
    profile.set_preference("dom.popup_maximum", 0)
    profile.set_preference("browser.fullscreen.autohide", True)
    profile.set_preference("browser.fullscreen.animate", False)
    profile.set_preference("toolkit.cosmeticAnimations.enabled", False)
    profile.set_preference("layers.acceleration.disabled", True)
    profile.set_preference("network.predictor.enabled", False)
    profile.set_preference("browser.startup.page", 0)
    profile.set_preference("browser.sessionstore.resume_from_crash", False)
    profile.set_preference("browser.sessionstore.max_resumed_crashes", 0)
    profile.set_preference("security.dialog_enable_delay", 0)
    profile.set_preference("security.sandbox.content.level", 0)
    profile.set_preference("security.sandbox.logging.level", 0)
    profile.set_preference("network.dns.disablePrefetch", True)
    profile.set_preference("network.prefetch-next", False)
    profile.set_preference("network.predictor.enable-prefetch", False)
    profile.set_preference("network.http.speculative-parallel-limit", 0)
    profile.set_preference("dom.workers.maxPerDomain", 0)
    profile.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", False)
    profile.set_preference("plugin.state.flash", 0)
    profile.set_preference("media.autoplay.default", 0)
    profile.set_preference("media.block-autoplay-until-in-foreground", True)
    profile.set_preference("media.autoplay.allow-muted", False)
    profile.set_preference("privacy.trackingprotection.fingerprinting.enabled", True)
    profile.set_preference("privacy.trackingprotection.cryptomining.enabled", True)
    profile.set_preference("privacy.trackingprotection.enabled", True)
    profile.set_preference("privacy.trackingprotection.socialtracking.enabled", True)
    profile.set_preference("privacy.trackingprotection.pbmode.enabled", True)
    profile.set_preference("privacy.trackingprotection.annotate_channels", True)
    profile.set_preference("privacy.trackingprotection.lower_network_priority", False)
    profile.set_preference("privacy.donottrackheader.enabled", True)
    profile.set_preference("privacy.donottrackheader.value", 1)
    profile.set_preference("privacy.resistFingerprinting", True)
    profile.set_preference("privacy.resistFingerprinting.block_mozAddonManager", True)
    profile.set_preference("privacy.resistFingerprinting.letterboxing", True)
    profile.set_preference("privacy.resistFingerprinting.letterboxing.dimensions", f"{random_resolution},1")
    profile.update_preferences()

    # Devolver el controlador de navegador configurado
    driver.get(url)
    return driver

def set_random_window_size(driver):
    # Lista de resoluciones seleccionables
    resolutions = [
        (1600, 900),
        (1680, 1050),
        (1920, 1080),
        (1920, 1200),
        (2560, 1440),
        (2560, 1600),
        # Agrega más resoluciones según sea necesario
    ]

    # Seleccionar una resolución aleatoria
    random_resolution = random.choice(resolutions)

    # Cambiar el tamaño de la ventana del navegador
    driver.set_window_size(random_resolution[0], random_resolution[1])

def simulate_human_interaction(driver):
    """
    Simula el comportamiento humano en una página web.

    Args:
    - driver: Objeto del controlador de navegador.

    Returns:
    - None
    """
    # Inicia acciones de control del ratón
    actions = ActionChains(driver)

    # Obtener el tamaño de la ventana del navegador
    window_size = driver.get_window_size()
    window_width = window_size['width']
    window_height = window_size['height']
    print(window_width, window_height)
    # Realiza varios movimientos del ratón y acciones humanas
    for _ in range(5):  # Realiza 5 acciones

        # Desplazamiento de página hacia abajo o arriba
        if random.random() < 0.5:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1, 2))  # Espera entre 1 y 2 segundos
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(random.uniform(1, 2))  # Espera entre 1 y 2 segundos
        else:
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(random.uniform(1, 2))  # Espera entre 1 y 2 segundos
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1, 2))  # Espera entre 1 y 2 segundos

        # Realiza clics aleatorios en elementos clickeables
        # clickable_elements = driver.find_elements(By.XPATH, "//*[self::a or self::button or @role='button']")
        # print("Len clickables elements: ", len(clickable_elements))
        # if clickable_elements:
        #     random_element = random.choice(clickable_elements)
        #     try:
        #         actions.move_to_element(random_element).click().perform()
        #         time.sleep(random.uniform(2, 4))  # Espera entre 2 y 4 segundos
        #     except Exception as e:
        #         print("Error al hacer clic en el elemento:", e)

        # Realiza un zoom out aleatorio
        actions.key_down(Keys.CONTROL).send_keys(Keys.SUBTRACT).key_up(Keys.CONTROL).perform()
        time.sleep(random.uniform(1, 2))  # Espera entre 1 y 2 segundos

        # Realiza movimientos aleatorios del ratón
        random_x = random.randint(0, window_width/2)
        random_y = random.randint(0, window_height/2)
        target_x = min(max(random_x, 0), window_width)
        target_y = min(max(random_y, 0), window_height)        
        
        print("Random_x ", random_x)
        print("Random_y ", random_y)
        try:
            actions.move_by_offset(target_x, target_y).perform()
            time.sleep(random.uniform(1, 2))  # Espera entre 1 y 2 segundos
        except:
            print("Issue coordinates ")

        # Realiza un zoom out aleatorio
        actions.key_down(Keys.CONTROL).send_keys(Keys.SUBTRACT).key_up(Keys.CONTROL).perform()
        time.sleep(random.uniform(1, 2))  # Espera entre 1 y 2 segundos

        # Realiza un zoom in aleatorio
        actions.key_down(Keys.CONTROL).send_keys(Keys.ADD).key_up(Keys.CONTROL).perform()
        time.sleep(random.uniform(1, 2))  # Espera entre 1 y 2 segundos

    # Desplazarse a la parte superior de la página
    driver.execute_script("window.scrollTo(0, 0);")