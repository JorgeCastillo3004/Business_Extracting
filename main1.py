from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from datetime import date, timedelta, datetime
from selenium import webdriver
import random
import string
import json
import os
import re
import time
from common import *
import pandas as pd

def launch_navigator_old(url, headless = True):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-application-cache")
    # options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    # options.add_argument("--disable-infobars")
    # options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-web-security")
    # options.add_argument("--incognito")
    # options.add_argument("--start-maximized")
    # options.add_argument("--disable-blink-features=AutomationControlled")     
    # options.add_experimental_option("excludeSwitches", ["enable-automation"]) ----
    options.add_experimental_option("useAutomationExtension", False)
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')  ---  
    # chrome_path = os.getcwd()+'/chrome_files'
    # print("chrome_path: ", chrome_path)
    chrome_path = '/home/jorge/.config/google-chrome/'
    options.add_argument(r"user-data-dir={}".format(chrome_path))
    # Default
    # options.add_argument(r"profile-directory=Default")
    options.add_argument(r"profile-directory=Profile 6")

    drive_path = Service('/usr/local/bin/chromedriver')

    driver = webdriver.Chrome(service=drive_path,  options=options)
    driver.get(url)
    return driver

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

def make_search(driver, search_word, search_localization):
    # Simulación de interacción humana
    random_mouse_movement(driver)
    random_page_interaction(driver)

    # Simulación de búsqueda
    category_element = driver.find_element(By.ID, 'search_keyword')
    random_sleep(start=0, end=0.5)
    category_element.clear()
    print(f"search_word: {search_word}")
    human_typing(category_element, search_word+'\n', start=0.05, end=0.15)
    random_sleep()

    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    localization_element = driver.find_element(By.ID, 'search_location')
    random_sleep(start=0, end=0.5)
    localization_element.clear()
    print(f"search_localization: {search_localization}")
    human_typing(localization_element, search_localization +'\n', start=0.05, end=0.15)
    random_sleep()
    webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()

def extrac_phones(block):
    phone_options = block.find_elements(By.CLASS_NAME, 'phoneOption')
    phone_numbers = {}
    for option in phone_options:
        prefix = option.find_element(By.CLASS_NAME, 'business--telephonePrefix').text.strip()
        number = option.find_element(By.CLASS_NAME, 'business--telephoneNumber').text.strip()
        phone_numbers[prefix] = number
    return phone_numbers

def create_row(search_rank, company_name,profile_URL, full_address,
                phone_numbers, website, rating, year_business, location_category):

    row ={
    'Search Location':location_category['location'],
    'Search Rank':search_rank,
    'Profile/Company Name':company_name,
    'Category':location_category['category'],
    'Profile URL':profile_URL,    
    'Full Address':full_address,
    'Phone Number': phone_numbers,
    'Email Address': '',
    'Website':website,
    'Rating':rating,
    'No. of Reviews':'',
    'Years in Business':year_business,
    'Email': '',
    'Phone': '',
    'Social Media Profiles': '',
    'Facebook': '',
    'Twitter': '',
    'Instagram': '',    
    }
    return row

def get_website(block):
    try:
        xpath_expression = "//a[contains(text(), 'Website')]"
        return block.find_element(By.XPATH, xpath_expression).get_attribute('href')
    except:
        return ''

def get_company_name_profile_URL(block, start_1 = 1, start_2 = 2, end_1 = 3, end_2 = 3):
    random_sleep(start=start_1, end=end_1)    
    try:
        wait = WebDriverWait(block, 10)
        company_url = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'businessCapsule--title')))    
        company_name =  company_url.text
        profile_URL =  company_url.get_attribute('href')
        random_sleep(start=start_2, end=end_2)        
        return clean_string(company_name), profile_URL
    except:
        return '', ''

def get_profile_URL(block):
    return block.find_element(By.CSS_SELECTOR, 'a[data-tracking="LIST:MOREINFO"]').get_attribute('href')

def get_address(block):
    try:
        return block.find_element(By.XPATH, './/span[@itemprop="address"]').text
    except:
        return ''

def get_rating(block):
    rating = block.find_elements(By.CLASS_NAME, 'starRating--average')
    if rating:
        rating = rating[0].text
    else:
        rating = ''
    return rating

def get_year_business(block):
    try:
        year_business = block.find_element(By.CLASS_NAME, 'col-sm-12').text
        return found_numbers(year_business)
    except:
        year_business = None
        return year_business

def get_phone(block):
    try:
        block_contact = block.find_element(By.CLASS_NAME, 'col-sm-24.businessCapsule--ctas')    
        phone = block_contact.find_element(By.XPATH, './label[@class="business--telephone"]')
        phone.click()
        wait = WebDriverWait(block, 10)
        phone = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "phoneOption")))    
        phone_numbers = extrac_phones(block)
        return phone_numbers
    except:
        return ''

def click_next(driver, search_counter, index, maxtry = 5):
    webdriver.ActionChains(driver).send_keys(Keys.END).perform()
    wait = WebDriverWait(driver, 10)
    
    count = 0
    while count < maxtry:
        try:
            webdriver.ActionChains(driver).send_keys(Keys.END).perform()
            next_page_button = driver.find_elements(By.XPATH, "//a[contains(text(), 'Next')]")
            if next_page_button:        
                blocks = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'row.businessCapsule--mainRow')))
                next_page_button[0].click()

                if len(blocks) != 0: # Check if exists blocks
                    wait.until(EC.staleness_of(blocks[0])) # wait until staleness first block

                # else:
                blocks = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'row.businessCapsule--mainRow')))
                search_counter += index + 1
                print("Click Next sucessfull")
                return search_counter, True
            else:
                return search_counter, False
        except:
            count += 1
            random_sleep()
    return search_counter, False

def click_social_media_links(block, driver):
    
    # driver.execute_script("window.open('');")    
    # Open the specified URL
    try:
        xpath_expression = ".//a[contains(text(), 'Website')]"
        block.find_element(By.XPATH, xpath_expression).click()
        driver.switch_to.window(driver.window_handles[1])
        random_sleep(start=1, end=2)
        webdriver.ActionChains(driver).send_keys(Keys.END).perform()        
        random_sleep(start=1, end=3)
        # Wait for the page to load completely
        wait = WebDriverWait(driver, 10)

        # Define the social media keywords to search for
        social_media_keywords = {
            'Twitter': "contains(@href, 'twitter.com') or contains(@href, 'x.com')",
            'Linkedin': "contains(@href, 'linkedin.com')",
            'Facebook': "contains(@href, 'facebook.com')",
            'Instagram': "contains(@href, 'instagram.com')"
        }
        # Create a dictionary to store the found links
        social_media_links = {}

        # Iterate through each keyword and search for corresponding links
        for platform, keyword in social_media_keywords.items():

            # Use XPath to find elements containing the keyword in their href attribute
            xpath_expression = f"//a[{keyword}]"
            link_element = driver.find_elements(By.XPATH, xpath_expression)
            if link_element:
                link_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath_expression)))
                social_media_links[platform] = link_element.get_attribute('href')
            else:
                social_media_links[platform] = ''
        social_media_links['Email']= get_business_email(driver)        
        random_sleep(start=2, end=3)
        close_back_main_window(driver)
        return social_media_links
    except:
        random_sleep(start=0.2, end=1.5)
        close_back_main_window(driver)
        return {}

def extract(driver, check_point, outfile):
    print("Input check point: ", check_point)
    folder = outfile.split('/')[0]    
    enable = False
    search_counter = 1   
    data = load_json(f'{folder}/data.json')    
    # check_point = load_check_point(f'{folder}/checkpoint.json')

    while True:
        wait = WebDriverWait(driver, 10)
        xpath_expression = 'row.businessCapsule--mainRow'
        blocks = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, xpath_expression)))
        random_sleep(start=0.5, end=1)
        for index, block in enumerate(blocks[:3]):# delete [content]            
            # Update search rank value
            search_rank = search_counter + index            
            if search_rank > int(check_point['search_rank']) or check_point['search_rank'] == 1: # enable if search_rank match with checkpoint.
                enable = True
    #         enable = False
            if enable:
                #############################################
                #         EXTRACT COMPANY NAME              #
                #############################################
                company_name, profile_URL = get_company_name_profile_URL(block, start_1 = 1, start_2 = 2, end_1 = 3, end_2 = 3)                
                print(f"Search_rank: {search_rank} index {index} comapany name: {company_name}")
                #############################################
                #       EXTRACT PROFILE URL  ADDRESS        #
                #############################################
                full_address = get_address(block)
                random_sleep(start=0.2, end=1.5)

                #############################################
                #         EXTRACT SEARCH RANKING            #
                #############################################                
                search_rank = search_counter + index                
                random_sleep(start=0.2, end=1.5)

                #############################################
                #    EXTRACT YEAR BUSINESS AND RATING       #
                #############################################
                year_business = get_year_business(block)    
                rating = get_rating(block)
                random_sleep(start=0.2, end=1.5)

                #############################################
                #    EXTRACT WEBSITE AND PHONE NUMBERS      #
                #############################################
                phone_numbers = get_phone(block)
                random_sleep(start=0.2, end=1.5)

                #############################################
                #         EXTRACT CATEGORY                  #
                #############################################    
                # categories = extract_categories(driver)

                #############################################
                #    CREATE ROW AND EXTRACT WEBSITE         #
                #############################################
                website = get_website(block)
                row = create_row(search_rank, company_name, profile_URL, full_address,
                            phone_numbers, website, rating, year_business, check_point)
                
                random_sleep(start=0.5, end=1.5)
                social_links = {}
                
                if profile_URL != '':
                    social_links = click_social_media_links(block, driver)

                row.update(social_links)
                data.append(row)
                
                save_check_point(f'{folder}/data.json', data)

                # SAVE CHECK POINT 
                check_point = {'category':check_point['category'], 'location':check_point['location'],
                                'search_rank':search_rank}
                save_check_point(f'{folder}/checkpoint.json', check_point)                
        # continue_stop()
        df = pd.DataFrame(data)
        df.to_csv(f'{folder}/{folder}_out.csv')
        #############################################
        #         CLICK NEXT PAGE                   #
        #############################################
        search_counter, next_found = click_next(driver, search_counter, index)
        random_sleep(start = 1, end = 1.5)            
        print(f"search_counter {search_counter}")
        print("Click Next ready")
        if not next_found:
            break
    return data

def main():
    url1 = 'https://www.yell.com/'
    driver = open_firefox_with_profile(url1, headless= False)
    directory_path = 'files_yell'    
    check_point = restart_continue(directory_path) # check and load checkpoint.
    search_settings = load_json('search_settings.json')
    count = 0
    for category in search_settings['categories']:
        for location in search_settings['locations']:

            cond1 = check_point['category'] == category
            cond2 = check_point['location'] == location
            cond3 = check_point['category'] == ''
            
            if cond1 and  cond2 or cond3:
                print(category, location)
                check_point['category'] = category
                check_point['location'] = location
                make_search(driver, category, location)
                random_sleep(start = 4, end= 5)
                ensure_directory_exists(directory_path)
                # extract(driver, location, f'{directory_path}/{category}_{category}_out.csv')
                data = extract(driver, check_point, f'{directory_path}/{category}_{category}_out.csv')
                check_point['category'] == ''
        if data:
            df = pd.DataFrame(data)
            df.to_csv(f'{directory_path}/{directory_path}_out.csv')

if __name__ == "__main__":
    main()