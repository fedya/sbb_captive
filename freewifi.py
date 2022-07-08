#!/usr/bin/env python3

# pip3 install selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
from time import sleep
from tqdm import tqdm, trange

# Test url must not be https so that the captive portal redirect can catch it
http_url="http://google.com"

# If the above url redirects normally, this is what it redirects to.
https_url="https://www.google.com"

# Timing variables, self-explanatory
sleep_time = 60
retry_time = 3
num_retries = 3

chrome_options = Options()
chrome_options.add_argument("--headless")


def check_status():
    print("checking for Serbian BroadBand captive portal")
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(http_url)
    current_url = browser.current_url
    # SBB
    # https://freewifizona.sbb.rs/free-wifi-zona/
    browser.quit()
    if (not current_url.startswith(https_url)):
        print("current url is {}".format(current_url))
        print("need to autorize...")
        return True
    else:
        print("Current url is {}".format(current_url))
        return False


def render_page():
    try:
        print("render the page")
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(http_url)
        elements = WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".btn.blue-btn")))
        print("trying to push submit button")
        signInButton = browser.find_element(By.CSS_SELECTOR, ".btn.blue-btn")
        signInButton.click()
        print("Captive portal login succeeded, we think.")
        browser.quit()
        return True
    except Exception:
        return False


def autorize():
    status = None
    status = check_status()
    if status is True:
        if render_page() is True:
            for i in tqdm(range(1745)):
                time.sleep(1)
    else:
        time.sleep(10)



for i in range(0,100):
    while (True):
        try:
            autorize()
        except Exception:
            continue
