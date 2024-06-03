from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from datetime import date, timedelta, datetime
from selenium import webdriver
import chromedriver_autoinstaller
import random
import string
import os
import re
import time
import pandas as pd

from common import *

def launch_navigator(url, headless=True):
    options = webdriver.ChromeOptions()
    
    # Configuraciones para evitar detección de bot
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-web-security")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # User-Agent aleatorio para Linux
    user_agents = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    user_agent = random.choice(user_agents)
    options.add_argument(f"user-agent={user_agent}")
    
    if headless:
        options.add_argument('--headless')
    
    # Directorio del perfil de Chrome
    chrome_path = '/home/jorge/.config/google-chrome/'
    options.add_argument(r"user-data-dir={}".format(chrome_path))
    options.add_argument(r"profile-directory=Default")
    
    # Ruta del driver
    drive_path = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=drive_path, options=options)
    
    # Emulación del comportamiento humano
    driver.get(url)
    time.sleep(random.uniform(1, 3))  # Espera aleatoria
    
    # Simulación de movimiento del mouse
    webdriver.ActionChains(driver).move_by_offset(random.randint(0, 10), random.randint(0, 10)).perform()
    
    return driver

def random_sleep(start=1, end=2):
    time.sleep(random.uniform(start, end))

def human_typing(element, text, start=0.05, end=0.15):
    for char in text:
        element.send_keys(char)
        random_sleep(start, end)

def random_mouse_movement(driver):
    action = ActionChains(driver)
    for _ in range(random.randint(5, 10)):
        x_offset = random.randint(0, 20)
        y_offset = random.randint(0, 20)
        action.move_by_offset(x_offset, y_offset).perform()
        random_sleep(0.2, 0.5)

def random_page_interaction(driver):
    actions = [Keys.PAGE_DOWN, Keys.PAGE_UP, Keys.HOME, Keys.END]
    action = ActionChains(driver)
    for _ in range(random.randint(3, 7)):
        action.send_keys(random.choice(actions)).perform()
        random_sleep(0.5, 1.5)

def wait_update_page(driver, url, class_name):
    wait = WebDriverWait(driver, 10)
    current_tab = driver.find_elements(By.CLASS_NAME, class_name)
    driver.get(url)

    if len(current_tab) == 0:
        current_tab = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name)))
    else:
        element_updated = wait.until(EC.staleness_of(current_tab[0]))   

def make_search(driver, category, city):
    search_category = driver.find_element(By.ID, 'search_description')
    search_category.click()

    human_typing(search_category, category, start=0.05, end=0.15)
    search_category.send_keys(Keys.TAB)

    search_localization = driver.find_element(By.ID, 'search_location')
    human_typing(search_localization, city + '\n', start=0.05, end=0.15)

    # search_localization.send_keys(city + '\n')

def extract_name(block, start_1 = 1, start_2 = 2, end_1 = 3, end_2 = 3):
    random_sleep(start=start_1, end=end_1)
    wait = WebDriverWait(block, 10)
    # company_name = block.find_element(By.XPATH, ".//div[contains(@class, 'businessName')]").text
    company_name = wait.until(EC.presence_of_element_located((By.XPATH, ".//div[starts-with(@class, 'businessName')]")))
    random_sleep(start=start_2, end=end_2)
    return company_name.text

def extract_numeric_value(text):
    # Define la expresión regular para encontrar números, incluyendo decimales
    pattern = r'[-+]?\d*\.\d+|\d+'
    match = re.search(pattern, text)
    
    if match:
        return float(match.group())
    return None

def extract_reviews_rating(block):
    try:
        rating, no_of_reviews = block.find_elements(By.XPATH, ".//div[./span[contains(text(), 'review')]]/span")
        rating = extract_numeric_value(rating.text)
        no_of_reviews = extract_numeric_value(no_of_reviews.text)
        return rating, no_of_reviews
    except:
        return None, None
    
def extract_categories(driver):
    try:
        # Encuentra la sección de categorías
        category_section = driver.find_element(By.CSS_SELECTOR, 'div[aria-labelledby="filterSetCategory"]')

        # Encuentra todos los botones dentro de la sección de categorías
        category_buttons = category_section.find_elements(By.CSS_SELECTOR, 'button.filterToggle__09f24__XF_eF')

        # Extrae el texto de cada botón
        categories = [button.find_element(By.TAG_NAME, 'p').text for button in category_buttons]
        return categories
    except:
        return ''    

def click_more_info(block):
    # click on more info
    wait = WebDriverWait(block, 10)
    more_info = wait.until(EC.element_to_be_clickable((By.XPATH, './/a[contains(text(),"more")]')))
    more_info.click()

def change_windows(driver):
    time.sleep(1)
    all_windows = driver.window_handles    
    driver.switch_to.window(all_windows[1])   

def get_phone_url_addres(driver):
    wait = WebDriverWait(driver, 4)
    try:
        xpath_expression = "//p[contains(text(), 'Business website')]/following-sibling::p/a"
        profile_URL = wait.until(EC.presence_of_element_located((By.XPATH, xpath_expression))).text
        # xpath_expression = "//p[contains(text(), 'Business website')]/following-sibling::p/a"
        # profile_URL = driver.find_element(By.XPATH, xpath_expression).text
    except:
        profile_URL = ''
    print(f"profile_URL {profile_URL}")
    
    try:
        xpath_expression = "//p[contains(text(), 'Phone number')]/following-sibling::p"
        phone_number = driver.find_element(By.XPATH, xpath_expression).text
    except:
        phone_number = ''
    print(f"phone_number: {phone_number}")
    
    try:
        xpath_expression = "//p[a[contains(text(), 'Get Directions')]]/following-sibling::p"
        full_address = driver.find_element(By.XPATH, xpath_expression).text
    except:
        full_address = ''
    print(f"full_address: {full_address}")

    return profile_URL, phone_number, full_address

def get_website(driver):
    try:
        xpath_expression = "//a[.//span[contains(text(), 'Website')]]"
        return driver.find_element(By.XPATH, xpath_expression).get_attribute('href')
    except:
        return ''

def complete_data(city, search_rank, company_name, categories, profile_URL, full_address, phone_numbers, website, rating, no_of_reviews):
    row ={
    'Search Location':city,
    'Search Rank':search_rank,
    'Profile/Company Name':company_name,
    'Category':categories,
    'Profile URL':profile_URL,    
    'Full Address':full_address,
    'Phone Number': phone_numbers,
    'Email Address': '',
    'Website':website,
    'Rating':rating,
    'No. of Reviews':no_of_reviews,
    'Years in Business':'',
    'Email': '',
    'Phone': '',
    'Social Media Profiles': '',
    # 'Facebook': '',
    # 'Twitter': '',
    # 'Instagram': '',
    }
    return row

def extract_search_rank_and_company_name(text, search_counter, index):
    # Define the regular expression pattern
    pattern = r"^(\d+)\.\s*(.+)"
    
    # Search for the pattern in the provided text
    match = re.match(pattern, text)
    
    if match:
        # Extract the search rank and company name
        search_rank = int(match.group(1))
        company_name = match.group(2)
        return search_rank, company_name
    else:        
        search_rank = search_counter + index
        return search_rank, text

def get_more_info(driver, block, max_value = 5):
    if max_value == 1:
        max_value = 2
    count_try = 0
    more_info = block.find_elements(By.XPATH, './/a[contains(text(),"more")]')
    print("Check if more info exist: ",len(more_info))
    while True and more_info:
        # try:
            count_try += 1
            if count_try == max_value:
                break
            click_more_info(block)
            random_sleep(start=1, end=2)
            change_windows(driver)
            profile_URL, phone_numbers, full_address = get_phone_url_addres(driver)
            #############################################
            random_sleep(start=1, end=2)
            website = get_website(driver) # Get business website

            random_sleep(start=1, end=2)
            close_back_main_window(driver)
            return profile_URL, phone_numbers, full_address, website
        # except:                
        #     all_windows = driver.window_handles
        #     if len(all_windows) != 1:
        #         driver.close()
        #         all_windows = driver.window_handles
        #         driver.switch_to.window(all_windows[0])
    return '', '', '', ''

def click_next(driver, search_counter, index):
    wait = WebDriverWait(driver, 10)
    next_page_button = driver.find_elements(By.XPATH, "//button[span[contains(text(), 'Next Page')]]")
    if next_page_button:

        xpath_expression = "//li/div[starts-with(@class, 'container__')]"        
        blocks = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_expression)))
    #     block_test  = blocks[0].copy

    #     time.sleep(0.5)
    #     next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Next Page')]]")))
        next_page_button[0].click()

        if len(blocks) != 0: # Check if exists blocks
            wait.until(EC.staleness_of(blocks[0])) # wait until staleness first block 
            
        # else:
        blocks = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_expression)))
        search_counter += index
    return search_counter

def extract(driver, city, outfile):
    folder = outfile.split('/')[0]
    data = load_json(f'{folder}/data.json')
    check_point = load_check_point(f'{folder}/checkpoint.json')
    enable = False
    search_counter = 1

    print("search_counter: ", search_counter)
    print(f"check_point {check_point}")
    while True:
    #     blocks = driver.find_elements(By.XPATH, '//div[@data-testid="serp-ia-card"]')
        wait = WebDriverWait(driver, 10)
        xpath_expression = "//li/div[starts-with(@class, 'container__')]"
        blocks = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_expression)))
        random_sleep(start=0.5, end=1)
        for index, block in enumerate(blocks):
            print(f"Index {index}, search_counter: {search_counter}")
            if check_point == index or check_point >= len(blocks): # enable if index match with checkpoint.
                enable = True
    #         enable = False
            if enable:
                #############################################
                #         EXTRACT COMPANY NAME              #
                #############################################
                company_name = extract_name(block, start_1 = 1, start_2 = 2, end_1 = 3, end_2 = 3)

                #############################################
                #         EXTRACT SEARCH RANKING            #
                #############################################
                search_rank, company_name =  extract_search_rank_and_company_name(company_name, search_counter, index)
                print(f"search_rank: {search_rank}, company_name: {company_name}")
                random_sleep(start=0.2, end=1.5)
                
                #############################################
                #           EXTRACT REVIEWS                 #
                #############################################
                rating, no_of_reviews = extract_reviews_rating(block)
                random_sleep(start=0.5, end=1.5)

                #############################################
                #         CLICK MORE INFO                   #
                #############################################
                profile_URL, phone_numbers, full_address, website = get_more_info(driver, block, max_value = 5)

                #############################################
                #         EXTRACT CATEGORY                  #
                #############################################    
                categories = extract_categories(driver)

                #############################################
                #         BUILD DATA DICT                   #
                #############################################
                row = complete_data(city, search_rank, company_name, categories, profile_URL, full_address,
                              phone_numbers, website, rating, no_of_reviews)
                random_sleep(start=0.5, end=1.5)
                social_links = {}
                if profile_URL != '':
                    social_links = extract_social_media_links(driver, profile_URL)

                row.update(social_links)
        #         continue_stop()
                data.append(row)
                save_check_point(f'{folder}/data.json', data)

                # SAVE CHECK POINT 
                save_check_point(f'{folder}/checkpoint.json', {'index':index})
        #############################################
        #         CLICK NEXT PAGE                   #
        #############################################
        try:
            print("Click on next")
            search_counter = click_next(driver, search_counter, index)
            random_sleep(start = 1, end = 1.5)
            print(f"search_counter {search_counter}")
        except:
            break
        
    df = pd.DataFrame(data)
    df.to_csv(outfile)
    
def main():
    # driver = launch_navigator('https://www.yelp.co.uk/')
    directory_path = 'files_yelp'    
    driver = open_firefox_with_profile('https://www.yelp.co.uk/', headless= False)    
    continue_stop()
    search_settings = load_json('search_settings.json')
    count = 0
    for category in search_settings['categories']:
        for city in search_settings['locations']:
            print(category, city)            
            make_search(driver, category, city)
            ensure_directory_exists(directory_path)
            extract(driver, city, f'{directory_path}/{category}_{category}_out.csv')

if __name__ == "__main__":
    main()