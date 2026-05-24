from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):

        # Store webdriver instance
        self.driver = driver

    def click_element(self, locator):

        # Wait until element becomes clickable
        # then perform click action
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locator)
        ).click()

    def get_element(self, locator):

        # Wait until single element is present
        # and return the web element
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )

    def get_elements(self, locator):

        # Wait until multiple elements are loaded
        # and return list of elements
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(locator)
        )