import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class GbSeleniumDriver:
    def __init__(self, webdriver_path, use_gui):
        # Setup chrome options
        chrome_options = Options()
        if not use_gui:
            chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")

        # Set path to chromedriver as per your configuration
        webdriver_service = Service(webdriver_path)

        # Choose Chrome Browser
        self.driver = webdriver.Chrome(
            service=webdriver_service, options=chrome_options
        )

        self.driver.maximize_window()
        self.driver.get("https://goodbudget.com/login")
        # General check of the login page
        # Extract description from page and print
        description = self.driver.find_element(By.NAME, "description").get_attribute(
            "content"
        )
        assert (
            description == "Log in to Goodbudget. Budget well. Live life. Do good."
        )  # subject to change

    def log_in(self, in_username, in_password):
        username = self.driver.find_element(By.ID, "username")
        username.send_keys(in_username)

        password = self.driver.find_element(By.ID, "password")
        password.send_keys(in_password)

        login_button = self.driver.find_element(
            By.XPATH,
            "//button[@class='elementor-button elementor-size-sm "
            "elementor-animation-grow']",
        )
        login_button.click()
        assert (
            self.driver.title == "Home | Goodbudget"
        ), f"Got browser title of {self.driver.title} instead"
        print("Logged in.\n")

    def enter_transaction(self, in_date, in_payee, in_amount, in_envelope, in_notes):
        self._click_add_transation()
        self._enter_date(in_date)
        self._enter_payee(in_payee)
        self._enter_amount(in_amount)
        self._enter_envelope(in_envelope)
        self._enter_notes(in_notes)
        self._click_save_transaction()

    def _click_add_transation(self):
        add_transaction_button = self.driver.find_element(
            By.LINK_TEXT, "Add Transaction"
        )
        self.driver.execute_script("arguments[0].click();", add_transaction_button)

    def _enter_date(self, in_date):
        expense_date = self.driver.find_element(By.ID, "expense-date")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(expense_date)
        ).click()
        expense_date.clear()
        expense_date.send_keys(in_date)

    def _enter_payee(self, in_payee):
        expense_payee = self.driver.find_element(By.ID, "expense-receiver")
        expense_payee.click()
        expense_payee.send_keys(in_payee)

    def _enter_amount(self, in_amount):
        expense_amount = self.driver.find_element(By.ID, "expense-amount")
        self.driver.execute_script(
            "arguments[0].click();", expense_amount
        )  # TODO: do this for other clicks
        expense_amount.send_keys(in_amount)

    def _enter_envelope(self, in_envelope):
        # Choose correct Envelope
        # Could not get Selenium selector to work,
        # so went with solution of typing out the first few letters
        # of the desired envelope. This relies on the big assumption
        # that the "Enter Amount" was the field visited right before this
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB)
        actions.perform()
        actions.send_keys(in_envelope)
        actions.perform()

    def _enter_notes(self, in_notes):
        expense_notes = self.driver.find_element(By.ID, "expense-notes")
        expense_notes.click()
        expense_notes.send_keys(in_notes)

    def _exit_driver(self):
        print("\nThank you for using goodbudget_cli! See you next time!")
        self.driver.save_screenshot("screenshot.png")
        self.driver.quit()

    def _click_save_transaction(self):
        # Click the Save button
        save_button = self.driver.find_element(By.ID, "addTransactionSave")
        # save_button.click() didn't work, so have to use this
        self.driver.execute_script("arguments[0].click();", save_button)

        time.sleep(1)
        print("Success! Your transaction was entered into Goodbudget.\n")
