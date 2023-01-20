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

from .utils.util import format_date, get_envelope_from_alias


def main():
    # Parser for login email
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username for Goodbudget", action="store")
    args = parser.parse_args()

    # Get password
    gb_password = getpass.getpass(prompt="Enter your Goodbudget password: ")

    print("Logging in. Please wait...")

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
    assert (
        description == "Log in to Goodbudget. Budget well. Live life. Do good."
    )  # subject to change

    # Log in
    username = browser.find_element(By.ID, "username")
    username.send_keys(args.username)

    password = browser.find_element(By.ID, "password")
    password.send_keys(gb_password)

    login_button = browser.find_element(
        By.XPATH,
        "//button[@class='elementor-button elementor-size-sm "
        "elementor-animation-grow']",
    )
    login_button.click()
    assert (
        browser.title == "Home | Goodbudget"
    ), f"Got browser title of {browser.title} instead"
    print("Logged in.\n")

    more_transactions = True
    while more_transactions:
        input_date = input("Date of transaction (today / yesterday / mm/dd/yyyy): ")
        formatted_date = format_date(input_date)
        input_payee = input("Payee: ")
        input_amount = input("Amount: ")
        input_envelope = input("Envelope: ")
        found_envelope = get_envelope_from_alias(input_envelope)
        input_notes = input("Notes (optional): ")

        summary_of_transaction = f"""
        Summary of your transcation:

            Date: {formatted_date}
            Payee: {input_payee}
            Amount: ${input_amount}
            Envelope: {found_envelope} (based on your alias of '{input_envelope}')
            Notes: {input_notes if input_notes else "<none>"}
        """
        print(summary_of_transaction)
        input_confirmation = input("Is everything correct? (Y/n) ")
        if input_confirmation.lower() not in ["y", "yes"]:
            print("Exiting the program.")
            quit()

        # Click the Add Transaction button
        add_transaction_button = browser.find_element(By.LINK_TEXT, "Add Transaction")
        browser.execute_script("arguments[0].click();", add_transaction_button)

        # Clear out the Date
        expense_date = browser.find_element(By.ID, "expense-date")
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(expense_date)
        ).click()
        expense_date.clear()
        # Enter the correct Date
        expense_date.send_keys(formatted_date)

        # Enter Payee
        expense_payee = browser.find_element(By.ID, "expense-receiver")
        expense_payee.click()
        expense_payee.send_keys(input_payee)

        # Enter Amount
        expense_amount = browser.find_element(By.ID, "expense-amount")
        # expense_amount.click()
        browser.execute_script(
            "arguments[0].click();", expense_amount
        )  # TODO: do this for other clicks
        expense_amount.send_keys(input_amount)

        # Choose correct Envelope
        # Could not get Selenium selector to work,
        # so went with solution of typing out the first few letters
        # of the desired envelope. This relies on the big assumption
        # that the "Enter Amount" was the field visited right before this
        actions = ActionChains(browser)
        actions.send_keys(Keys.TAB)
        actions.perform()
        actions.send_keys(found_envelope)
        actions.perform()

        # Enter Notes
        expense_notes = browser.find_element(By.ID, "expense-notes")
        expense_notes.click()
        expense_notes.send_keys(input_notes)

        # Click the Save button
        save_button = browser.find_element(By.ID, "addTransactionSave")
        # save_button.click() didn't work, so have to use this
        browser.execute_script("arguments[0].click();", save_button)

        time.sleep(1)
        print("Success! Your transaction was entered into Goodbudget.\n")
        input_more_transactions = input(
            "Do you want to enter another transaction? (Y/n) "
        )
        if input_more_transactions.lower() not in ["y", "yes"]:
            more_transactions = False

    print("\nThank you for using goodbudget_cli! See you next time!")
    browser.save_screenshot("screenshot.png")
    browser.quit()
