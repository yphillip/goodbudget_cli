from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class GbSeleniumDriver:
    def __init__(self, webdriver_path):
        # Setup chrome options
        chrome_options = Options()
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

    def click_add_transation(self):
        add_transaction_button = self.driver.find_element(
            By.LINK_TEXT, "Add Transaction"
        )
        self.driver.execute_script("arguments[0].click();", add_transaction_button)

    def enter_date(self, in_date):
        expense_date = self.driver.find_element(By.ID, "expense-date")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(expense_date)
        ).click()
        expense_date.clear()
        expense_date.send_keys(in_date)
