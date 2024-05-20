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
import requests
import json
import os
import re
import time
local_time_naive = datetime.now()
utc_time_naive = datetime.utcnow()
time_difference_naive = utc_time_naive - local_time_naive

def load_json(filename):
    # Opening JSON file
    with open(filename, 'r') as openfile:        
        json_object = json.load(openfile)
    return json_object

def save_check_point(filename, dictionary):
    json_object = json.dumps(dictionary, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(json_object)

def load_check_point(filename):
    # Opening JSON file
    if os.path.isfile(filename):
        with open(filename, 'r') as openfile:        
            json_object = json.load(openfile)
    else:
        json_object = {}
    return json_object

def launch_navigator(url, headless=False):
	options = webdriver.ChromeOptions()
	options.add_argument("--disable-application-cache")
	options.add_argument("--disable-extensions")
	options.add_argument("--disable-gpu")
	options.add_argument("--disable-infobars")
	options.add_argument("--disable-popup-blocking")
	options.add_argument("--disable-web-security")
	# options.add_argument("--incognito")
	# options.add_argument("--start-maximized")
	options.add_argument("--disable-blink-features=AutomationControlled")     
	# options.add_experimental_option("excludeSwitches", ["enable-automation"]) ----
	options.add_experimental_option("useAutomationExtension", False)
	if headless:
		options.add_argument('--headless')
	# options.add_argument('--no-sandbox')
	# options.add_argument('--disable-dev-shm-usage')  ---	
	# chrome_path = os.getcwd()+'/chrome_files'
	# print("chrome_path: ", chrome_path)
	# options.add_argument(r"user-data-dir={}".format(chrome_path))
	# options.add_argument(r"profile-directory=Profile1")

	drive_path = Service('/usr/local/bin/chromedriver')

	driver = webdriver.Chrome(service=drive_path,  options=options)
	driver.get(url)
	return driver

def login(driver, email_= "jignacio@jweglobal.com", password_ = "Caracas5050@\n"):
    wait = WebDriverWait(driver, 10)

    # Accept cookies
    accept_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
    accept_button.click()
    # Click on login
    login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'header__icon.header__icon--user')))
    # login_button = driver.find_element(By.CLASS_NAME, 'header__icon.header__icon--user')
    login_button.click()
    # Select login mode
    continue_email = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ui-button.ui-formButton.social__button.email")))
    continue_email.click()

    email = driver.find_element(By.ID,'email')
    email = wait.until(EC.visibility_of_element_located((By.ID,'email')))
    email.send_keys(email_)

    email = driver.find_element(By.ID,'passwd')
    email.send_keys(password_)
    time.sleep(6)
    print("Login...", '\n')
    # webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

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
    search_category.send_keys(Keys.DELETE * 50)
    search_category.send_keys(category)


    search_localization = driver.find_element(By.ID, 'search_location')

    search_localization.send_keys(Keys.DELETE * 50)
    search_localization.send_keys(city + '\n')