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
    """
    Selenium webdriver for Chrome to interact with Goodbudget website

    Attributes:
        webdriver_path (str): path to the chrome webdriver
        use_gui (bool): show browser if True
        screenshot (bool): save screenshot if True

    Methods:
        log_in(in_username, in_password): log into goodbudget
        enter_expense(
            in_date,
            in_payee,
            in_amount,
            in_envelope,
            in_notes
        ): enter an expense into goodbudget
        enter_income(
            in_date,
            in_payee,
            in_amount,
            in_notes
        ): enter an income into goodbudget
        exit_driver(): quits the webdriver
    """

    def __init__(self, webdriver_path, use_gui=False, screenshot=False):
        """Sets class attributes and initializes driver."""
        self.webdriver_path = webdriver_path
        self.use_gui = use_gui
        self.screenshot = screenshot
        self.driver = self._initialize_driver()

    def log_in(self, in_username, in_password):
        """Logs into goodbudget."""
        username = self.driver.find_element(By.ID, "username")
        username.send_keys(in_username)

        password = self.driver.find_element(By.ID, "password")
        password.send_keys(in_password)

        login_button = self.driver.find_element(
            By.XPATH,
            "//button[@class='elementor-button elementor-size-sm "
            "elementor-animation-grow']",
        )
        self.driver.execute_script("arguments[0].click();", login_button)
        assert (
            self.driver.title == "Home | Goodbudget"
        ), f"Got browser title of {self.driver.title} instead"
        # TODO: allow user to retry entering password
        print("Logged in.\n")

    def enter_expense(self, in_date, in_payee, in_amount, in_envelope, in_notes=None):
        """Enters an expense into goodbudget."""
        print("Entering expense. Please wait...\n")
        self._click_add_transation()
        self._enter_date(in_date)
        self._enter_payee(in_payee)
        self._enter_amount(in_amount)
        self._enter_envelope(in_envelope)
        self._enter_notes(in_notes)
        self._click_save_transaction()

    def enter_income(self, in_date, in_payer, in_amount, in_notes=None):
        """Enters an income into goodbudget."""
        print("Entering income. Please wait...\n")
        self._click_add_transation()
        self._click_income()
        self._enter_date(in_date)
        self._enter_payer(in_payer)
        self._enter_amount(in_amount)
        self._enter_notes(in_notes)
        self._click_save_transaction()

    def exit_driver(self):
        """Quits the webdriver."""
        if self.screenshot:
            self.driver.save_screenshot("screenshot.png")
            print("\nScreenshot saved to screenshot.png")
        print("\nThank you for using goodbudget_cli! See you next time!")
        self.driver.quit()

    def _initialize_driver(self):
        """Set the initial options and starts the webdriver."""
        # Setup chrome options
        chrome_options = Options()
        if not self.use_gui:
            chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("window-size=1024x768")

        # Set path to chromedriver as per your configuration
        webdriver_service = Service(self.webdriver_path)

        # Choose Chrome Browser
        driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

        driver.maximize_window()

        driver.get("https://goodbudget.com/login")
        # General check of the login page
        # Extract description from page and print
        description = driver.find_element(By.NAME, "description").get_attribute(
            "content"
        )
        assert (
            description == "Log in to Goodbudget. Budget well. Live life. Do good."
        )  # subject to change
        return driver

    def _click_add_transation(self):
        "Clicks the Add Transaction button."
        add_transaction_button = self.driver.find_element(
            By.LINK_TEXT, "Add Transaction"
        )
        self.driver.execute_script("arguments[0].click();", add_transaction_button)

    def _click_income(self):
        "Clicks the Income tab in the Add Transaction floating window"
        income_button = self.driver.find_element(By.LINK_TEXT, "Income")
        self.driver.execute_script("arguments[0].click();", income_button)

    def _enter_date(self, in_date):
        "Enters the transaction date in the Date field."
        expense_date = self.driver.find_element(By.ID, "expense-date")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(expense_date))
        self.driver.execute_script("arguments[0].click();", expense_date)
        expense_date.clear()
        expense_date.send_keys(in_date)

    def _enter_payer(self, in_payer):
        "Enters the transaction payer in the payer field."
        income_payer = self.driver.find_element(By.ID, "income-payer")
        self.driver.execute_script("arguments[0].click();", income_payer)
        income_payer.send_keys(in_payer)

    def _enter_payee(self, in_payee):
        "Enters the transaction payee in the payee field."
        expense_payee = self.driver.find_element(By.ID, "expense-receiver")
        self.driver.execute_script("arguments[0].click();", expense_payee)
        expense_payee.send_keys(in_payee)

    def _enter_amount(self, in_amount):
        "Enters the transaction dollar amount in the Amount field."
        expense_amount = self.driver.find_element(By.ID, "expense-amount")
        self.driver.execute_script("arguments[0].click();", expense_amount)
        expense_amount.send_keys(in_amount)

    def _enter_envelope(self, in_envelope):
        """Chooses the correct envelope from the Envelope dropdown menu."""
        # Could not get Selenium selector to work,
        # so went with solution of typing out the first few letters
        # of the desired envelope.
        actions = ActionChains(self.driver)
        actions.send_keys(
            Keys.TAB
        )  # Big assumption that "Enter Amount" was last field visited
        actions.perform()
        actions.send_keys(in_envelope)
        actions.perform()

    def _enter_notes(self, in_notes=None):
        "Enters the transaction notes in the Notes field."
        if not in_notes:
            in_notes = ""
        expense_notes = self.driver.find_element(By.ID, "expense-notes")
        self.driver.execute_script("arguments[0].click();", expense_notes)
        expense_notes.send_keys(in_notes)

    def _click_save_transaction(self):
        "Clicks the Save button"
        save_button = self.driver.find_element(By.ID, "addTransactionSave")
        self.driver.execute_script("arguments[0].click();", save_button)

        time.sleep(1)
        print("Success! Your transaction was entered into Goodbudget.\n")
