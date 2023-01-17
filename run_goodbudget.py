import argparse
import getpass
import os.path
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TEST_DATA = {
    "date": "01/17/2023",
    "payee": "TEST_PAYEE",
    "amount": "155.70",
    "envelope": "Groceries",
    "notes": "TEST_NOTES",
}

ENVELOPES = [
    "Misc:Required",
    "Misc:House Stufff",
    "Misc:Fun",
    "Groceries",
    "Eating and Drinking Out",
    "Transportation",
    "Health",
    "Pure Fun",
    "Roth IRA",
    "Travel/Vacation",
    "Ally",
    "Merrill",
]


# Parser for login email
parser = argparse.ArgumentParser()
parser.add_argument("username", help="Username for Goodbudget", action="store")
args = parser.parse_args()

# Get password
gb_password = getpass.getpass(prompt="Enter your Goodbudget password: ")


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
password.send_keys(gb_password)

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
# expense_amount.click()
browser.execute_script("arguments[0].click();", expense_amount)  # TODO: do this for other clicks
expense_amount.send_keys(TEST_DATA["amount"])

# Choose correct Envelope
# Could not get Selenium selector to work,
# so went with solution of typing out the first few letters
# of the desired envelope
actions = ActionChains(browser)
actions.send_keys(Keys.TAB)
actions.perform()
actions.send_keys(TEST_DATA["envelope"])  # TODO: make smarter logic
actions.perform()

# Enter Notes
expense_notes = browser.find_element(By.ID, "expense-notes")
expense_notes.click()
expense_notes.send_keys(TEST_DATA["notes"])

# Click the Save button
save_button = browser.find_element(By.ID, "addTransactionSave")
# save_button.click() didn't work, so have to use this
browser.execute_script("arguments[0].click();", save_button)

time.sleep(1)
browser.save_screenshot("screenshot.png")
browser.quit()
