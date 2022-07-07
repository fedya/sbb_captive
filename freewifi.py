#!/usr/bin/env python3

# pip3 install selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

# Test url must not be https so that the captive portal redirect can catch it
http_url="http://google.com"

# If the above url redirects normally, this is what it redirects to.
https_url="https://www.google.com"

# Timing variables, self-explanatory
sleep_time = 15
retry_time = 3
num_retries = 3

chrome_options = Options()
chrome_options.add_argument("--headless")
# SBB
# https://freewifizona.sbb.rs/free-wifi-zona/

while (True):
    print("Checking for Serbian BroadBand captive portal")
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(http_url)
    current_url = browser.current_url
    print("Current url is {}".format(current_url))
    if (not current_url.startswith(https_url)):
        retries = num_retries
        while (retries > 0):
            try:
                print("render the page")
                elements = WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".btn.blue-btn")))
                print("trying to push submit button")
                signInButton = browser.find_element(By.CSS_SELECTOR, ".btn.blue-btn")
                signInButton.click()
                retries = 0
                print("Captive portal login succeeded, we think.")
            except Exception as e:
            	#### This exception occurs if the elements are not found in the webpage.
            	print ("Some error occured :(")
            	print(e)
            if (retries > 0):
            	print("{} left, sleeping a few".format(retries))
            	retries = retries - 1
            	time.sleep(retry_time)
            else:
            	print("Captive portal not found.")
    browser.quit()
    print("Sleeping for {} seconds before checking again.".format(sleep_time))
    time.sleep(sleep_time)

