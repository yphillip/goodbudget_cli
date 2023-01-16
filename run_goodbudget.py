import argparse
import os.path
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Parser for password
parser = argparse.ArgumentParser()
parser.add_argument("--username", help="Username for Goodbudget", action="store")
parser.add_argument("--password", help="Password for Goodbudget", action="store")
args = parser.parse_args()

# Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")

# Set path to chromedriver as per your configuration
homedir = os.path.expanduser("~")
webdriver_service = Service(f"{homedir}/Downloads/chromedriver/stable/chromedriver")

# Choose Chrome Browser
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Get page
browser.get("https://goodbudget.com/login")

# General check of the login page
# Extract description from page and print
description = browser.find_element(By.NAME, "description").get_attribute("content")
print(f"{description}")

# Log in
username = browser.find_element(By.ID, "username")
username.send_keys("yphillip@gmail.com")

password = browser.find_element(By.ID, "password")
password.send_keys(args.password)

login_button = browser.find_element(
    By.XPATH,
    "//button[@class='elementor-button elementor-size-sm elementor-animation-grow']",
)
login_button.click()
assert (
    browser.title == "Home | Goodbudget"
), f"Got browser title of {browser.title} instead"

time.sleep(1)
browser.save_screenshot("screenshot.png")
browser.quit()
