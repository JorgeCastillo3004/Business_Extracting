from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json
import os
import time
import random

def load_json(filename):
    # Opening JSON file
    if os.path.isfile(filename):
        with open(filename, 'r') as openfile:        
            json_object = json.load(openfile)
        return json_object
    return []

def save_list_to_json(file_path, data_list):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_list, json_file, ensure_ascii=False, indent=4)
    print(f"Data saved to {file_path} successfully.")

def save_check_point(filename, dictionary):
    json_object = json.dumps(dictionary, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(json_object)

def load_check_point(filename):
    # Opening JSON file
    if os.path.isfile(filename):
        with open(filename, 'r') as openfile:        
            json_object = json.load(openfile)
        return json_object['index'] + 1

    else:
        return 0

def open_firefox_with_profile(url, headless= True, profile_directory=''):
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

    driver = webdriver.Firefox(service=service, options=options)
    
    driver.get(url)
    
    return driver

def continue_stop():
    user = input('Type s to stop: ')
    if user == 's':
        print(stop)

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f'Folder created : {directory_path}')
    else:
        print(f'Folder exist: {directory_path}')

def extract_social_media_links(driver, url):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    # Open the specified URL
    if not 'https://www.' in url:
        url = 'https://www.' + url
    try:
        driver.get(url)

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
                print(f"platform found: {platform}")
            else:
                social_media_links[platform] = ''
        social_media_links['Email']= get_business_email(driver)
        random_sleep(start=0.2, end=1.5)
        close_back_main_window(driver)
        return social_media_links
    except:
        random_sleep(start=0.2, end=1.5)
        close_back_main_window(driver)
        return {}
    
def close_back_main_window(driver):
    all_windows = driver.window_handles
    if len(all_windows)!= 1:
        driver.close()
        all_windows = driver.window_handles
        driver.switch_to.window(all_windows[-1])

def get_business_email(driver):
    email = None
    
    # Regular expression to match email patterns
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    try:
        # Search for mailto links
        # mailto_link = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href, 'mailto:')]"))        )
        mailto_link = driver.find_element(By.XPATH, "//a[starts-with(@href, 'mailto:')]")        
        email = mailto_link.get_attribute('href').replace('mailto:', '')
        return email
    except:
        print("Mail don't found")
    
    try:
        # Search for email in visible text
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        emails_found = re.findall(email_regex, body_text)
        if emails_found:
            return emails_found[0]
    except:
        print("Email in visible text not found:")
    
    try:
        # Search for email in meta tags
        meta_tags = driver.find_elements(By.XPATH, "//meta[@name='email' or @name='contact']")
        for tag in meta_tags:
            content = tag.get_attribute('content')
            emails_found = re.findall(email_regex, content)
            if emails_found:
                return emails_found[0]
    except:
        print("Email in meta tags not found:")
    
    try:
        # Search for email in a specific div or p tag
        email_divs = driver.find_elements(By.XPATH, "//div[contains(text(), '@')] | //p[contains(text(), '@')]| //a[contains(text(), '@')]")
        for div in email_divs:
            emails_found = re.findall(email_regex, div.text)
            if emails_found:
                return emails_found[0]
    except:
        print("Email in specific div or p tags not found:")
    return ''

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

