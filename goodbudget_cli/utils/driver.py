from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait


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

    def maximize(self):
        self.driver.maximize_window()
