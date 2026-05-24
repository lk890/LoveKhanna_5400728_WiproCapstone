from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Waits:

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator, time=10):

        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator)
        )