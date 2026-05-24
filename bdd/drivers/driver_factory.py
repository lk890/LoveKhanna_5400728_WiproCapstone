import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def get_driver():

    # Read configuration data from config file
    with open("config/config.json") as file:
        config = json.load(file)

    # Fetch browser related settings
    browser = config["browser"]
    implicit_wait = config["implicit_wait"]
    headless = config["headless"]

    driver = None

    # Launch Chrome browser
    if browser.lower() == "chrome":

        # Create Chrome options object
        chrome_options = Options()

        # Run browser in headless mode if enabled
        if headless:
            chrome_options.add_argument("--headless=new")

        # Open browser in maximized mode
        chrome_options.add_argument("--start-maximized")

        # Initialize Chrome WebDriver
        driver = webdriver.Chrome(
            options=chrome_options
        )

    # Apply implicit wait globally
    driver.implicitly_wait(implicit_wait)

    # Return driver instance
    return driver