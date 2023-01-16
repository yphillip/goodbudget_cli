import argparse
import os.path
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select

TEST_DATA = {
    "date": "11/06/2022",
    "payee": "test_payee",
    "amount": "123.45",
    "envelope": "pure fun",
    "notes": "testing notes",
}


# Parser for password
parser = argparse.ArgumentParser()
parser.add_argument("username", help="Username for Goodbudget", action="store")
parser.add_argument("password", help="Password for Goodbudget", action="store")
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
browser.maximize_window()

# Get page
browser.get("https://goodbudget.com/login")

# General check of the login page
# Extract description from page and print
description = browser.find_element(By.NAME, "description").get_attribute("content")
print(f"{description}")

# Log in
username = browser.find_element(By.ID, "username")
username.send_keys(args.username)

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


# Click the Add Transaction button
add_transaction_button = browser.find_element(By.LINK_TEXT, "Add Transaction")
add_transaction_button.click()

# Clear out the Date
expense_date = browser.find_element(By.ID, "expense-date")
WebDriverWait(browser, 10).until(EC.element_to_be_clickable(expense_date)).click()
expense_date.clear()
# Enter the correct Date
expense_date.send_keys(TEST_DATA["date"])

# Enter Payee
expense_payee = browser.find_element(By.ID, "expense-receiver")
expense_payee.click()
expense_payee.send_keys(TEST_DATA["payee"])


# Enter Amount
expense_amount = browser.find_element(By.ID, "expense-amount")
expense_amount.click()
expense_amount.send_keys(TEST_DATA["amount"])

# Choose correct Envelope
# WebDriverWait(browser, 10).until(EC.element_to_be_clickable(select_element)).click()
iframes = browser.find_elements(By.TAG_NAME, "iframe")
breakpoint()
assert len(iframes) == 1
browser.switch_to.frame(iframes[0])
select_element = browser.find_element(By.XPATH, "//select[@name='envelopeUuid']")
select_element.click()
browser.execute_script("arguments[0].scrollIntoView();", select_element)
time.sleep(1)
browser.save_screenshot("screenshot.png")
# select = Select(select_element)
# select.select_by_visible_text("Pure Fun")


# Enter Notes
expense_notes = browser.find_element(By.ID, "expense-notes")
expense_notes.click()
expense_notes.send_keys(TEST_DATA["notes"])

# Click the Save button

time.sleep(1)
browser.quit()
