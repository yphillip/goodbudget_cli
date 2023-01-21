import argparse
import getpass
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .utils.util import format_date, get_envelope_from_alias, parse_config
from .utils.driver import GbSeleniumDriver


def main():
    # Parser for login email
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username for Goodbudget", action="store")
    args = parser.parse_args()

    # Get password
    gb_password = getpass.getpass(prompt="Enter your Goodbudget password: ")

    print("Logging in. Please wait...")

    gb_driver = GbSeleniumDriver(parse_config()["webdriver_path"])

    # Get page
    gb_driver.driver.get("https://goodbudget.com/login")

    # General check of the login page
    # Extract description from page and print
    description = gb_driver.driver.find_element(By.NAME, "description").get_attribute(
        "content"
    )
    assert (
        description == "Log in to Goodbudget. Budget well. Live life. Do good."
    )  # subject to change

    # Log in
    username = gb_driver.driver.find_element(By.ID, "username")
    username.send_keys(args.username)

    password = gb_driver.driver.find_element(By.ID, "password")
    password.send_keys(gb_password)

    login_button = gb_driver.driver.find_element(
        By.XPATH,
        "//button[@class='elementor-button elementor-size-sm "
        "elementor-animation-grow']",
    )
    login_button.click()
    assert (
        gb_driver.driver.title == "Home | Goodbudget"
    ), f"Got browser title of {gb_driver.driver.title} instead"
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
        add_transaction_button = gb_driver.driver.find_element(
            By.LINK_TEXT, "Add Transaction"
        )
        gb_driver.driver.execute_script("arguments[0].click();", add_transaction_button)

        # Clear out the Date
        expense_date = gb_driver.driver.find_element(By.ID, "expense-date")
        WebDriverWait(gb_driver.driver, 10).until(
            EC.element_to_be_clickable(expense_date)
        ).click()
        expense_date.clear()
        # Enter the correct Date
        expense_date.send_keys(formatted_date)

        # Enter Payee
        expense_payee = gb_driver.driver.find_element(By.ID, "expense-receiver")
        expense_payee.click()
        expense_payee.send_keys(input_payee)

        # Enter Amount
        expense_amount = gb_driver.driver.find_element(By.ID, "expense-amount")
        # expense_amount.click()
        gb_driver.driver.execute_script(
            "arguments[0].click();", expense_amount
        )  # TODO: do this for other clicks
        expense_amount.send_keys(input_amount)

        # Choose correct Envelope
        # Could not get Selenium selector to work,
        # so went with solution of typing out the first few letters
        # of the desired envelope. This relies on the big assumption
        # that the "Enter Amount" was the field visited right before this
        actions = ActionChains(gb_driver.driver)
        actions.send_keys(Keys.TAB)
        actions.perform()
        actions.send_keys(found_envelope)
        actions.perform()

        # Enter Notes
        expense_notes = gb_driver.driver.find_element(By.ID, "expense-notes")
        expense_notes.click()
        expense_notes.send_keys(input_notes)

        # Click the Save button
        save_button = gb_driver.driver.find_element(By.ID, "addTransactionSave")
        # save_button.click() didn't work, so have to use this
        gb_driver.driver.execute_script("arguments[0].click();", save_button)

        time.sleep(1)
        print("Success! Your transaction was entered into Goodbudget.\n")
        input_more_transactions = input(
            "Do you want to enter another transaction? (Y/n) "
        )
        if input_more_transactions.lower() not in ["y", "yes"]:
            more_transactions = False

    print("\nThank you for using goodbudget_cli! See you next time!")
    gb_driver.driver.save_screenshot("screenshot.png")
    gb_driver.driver.quit()
