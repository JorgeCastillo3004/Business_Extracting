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
import re
import threading
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# import chromedriver_autoinstaller

def load_json(filename):
    # Opening JSON file
    if os.path.isfile(filename):
        with open(filename, 'r') as openfile:        
            json_object = json.load(openfile)
        return json_object
    return []

def restart_continue(folder):
    user = input('Type r to restart or any to continue: ')
    if user == 'r':
        data = []
        save_check_point(f'{folder}/data.json', data)
        check_point = {'category':'', 'location':'', 'page':1,'index':0,'search_rank':1}
        save_check_point(f'{folder}/checkpoint.json', check_point)
        print("Restart search")
    else:        
        check_point = load_check_point(f'{folder}/checkpoint.json')
    return check_point

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
        return json_object
    else:
        return {'category':'', 'location':'', 'search_rank':1}

def launch_navigator(url, hadless=False):
	options = webdriver.ChromeOptions()
	options.add_argument("--disable-application-cache")
	options.add_argument("--disable-extensions")
	options.add_argument("--disable-gpu")
	options.add_argument("--disable-infobars")
	options.add_argument("--disable-popup-blocking")
	options.add_argument("--disable-web-security")
	options.add_argument("--incognito")
	options.add_argument("--start-maximized")
	options.add_argument("--disable-blink-features=AutomationControlled")     
	# options.add_experimental_option("excludeSwitches", ["enable-automation"]) ----
	options.add_experimental_option("useAutomationExtension", False)
	if hadless:
		options.add_argument('--headless')
	options.add_argument('--no-sandbox')
	# options.add_argument('--disable-dev-shm-usage')  ---	
	# chrome_path = os.getcwd()+'/chrome_files'
	# print("chrome_path: ", chrome_path)
	# options.add_argument(r"user-data-dir={}".format(chrome_path))
	# options.add_argument(r"profile-directory=Profile1")

	drive_path = Service('/usr/local/bin/chromedriver')
    
	driver = webdriver.Chrome()#service=drive_path,  options=options
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
        pass
    
    try:
        # Search for email in visible text
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        emails_found = re.findall(email_regex, body_text)
        if emails_found:
            return emails_found[0]
    except:
        pass
    
    try:
        # Search for email in meta tags
        meta_tags = driver.find_elements(By.XPATH, "//meta[@name='email' or @name='contact']")
        for tag in meta_tags:
            content = tag.get_attribute('content')
            emails_found = re.findall(email_regex, content)
            if emails_found:
                return emails_found[0]
    except:
        pass
    
    try:
        # Search for email in a specific div or p tag
        email_divs = driver.find_elements(By.XPATH, "//div[contains(text(), '@')] | //p[contains(text(), '@')]| //a[contains(text(), '@')]")
        for div in email_divs:
            emails_found = re.findall(email_regex, div.text)
            if emails_found:
                return emails_found[0]
    except:
        pass
    return ''

def random_sleep(start=1, end=2):
    time.sleep(random.uniform(start, end))

def human_typing(element, text, start=0.05, end=0.15):
    for char in text:
        element.send_keys(char)
        random_sleep(start, end)

def random_mouse_movement(driver):
    try:
        action = ActionChains(driver)
        for _ in range(random.randint(5, 10)):
            x_offset = random.randint(0, 20)
            y_offset = random.randint(0, 20)
            action.move_by_offset(x_offset, y_offset).perform()
            random_sleep(0.2, 0.5)
    except:
        pass

def random_page_interaction(driver):
    try:
        actions = [Keys.PAGE_DOWN, Keys.PAGE_UP, Keys.HOME, Keys.END]
        action = ActionChains(driver)
        for _ in range(random.randint(3, 7)):
            action.send_keys(random.choice(actions)).perform()
            random_sleep(0.5, 1.5)
    except:
        pass

def clean_string(string):
    string = string.replace('\n', ' ').replace('\r', ' ')    
    string = re.sub(r'\s+', ' ', string).strip()
    return string

def found_numbers(string):
    decimals = re.findall(r'\d+', string)
    # Convertir los números a enteros
    if decimals:
        decimals = decimals[0]
        return float(decimals)
    else:
        return None

class TimeoutExpired(Exception):
    pass

def input_with_timeout(prompt, timeout):
    def get_input():
        nonlocal user_input
        user_input = input(prompt)
    
    user_input = None
    thread = threading.Thread(target=get_input)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        raise TimeoutExpired
    return user_input

def get_input_user(mensaje, valor_por_defecto, tiempo_limite):
    try:
        user_input = input_with_timeout(f"{mensaje} (Type r to restart '{valor_por_defecto}') o espera {tiempo_limite} segundos: ", tiempo_limite)
        if user_input is None or user_input.strip() == "":
            return valor_por_defecto
        return user_input
    except TimeoutExpired:
        return valor_por_defecto
