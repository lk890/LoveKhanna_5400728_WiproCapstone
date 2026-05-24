from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class LoginPage:

    def __init__(self, driver):
        self.driver = driver

    MOBILE_INPUT = (
        By.CSS_SELECTOR,
        "input.mobileNumberInput"
    )

    CHECKBOX = (
        By.CSS_SELECTOR,
        "input.consentCheckbox"
    )

    CONTINUE_BTN = (
        By.CSS_SELECTOR,
        ".submitBottomOption"
    )

    OTP_INPUT = (
        By.XPATH,
        "//input[@type='tel']"
    )

    def enter_mobile(self, number):

        mobile = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                self.MOBILE_INPUT
            )
        )

        mobile.clear()

        mobile.send_keys(number)

    def click_checkbox(self):

        checkbox = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(
                self.CHECKBOX
            )
        )

        if not checkbox.is_selected():

            checkbox.click()

    def click_continue(self):

        continue_btn = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(
                self.CONTINUE_BTN
            )
        )

        continue_btn.click()

    def handle_login_flow(self):

        # First continue click
        self.click_continue()

        # Wait for resend timer
        time.sleep(30)

        # Second continue click
        try:

            second_continue = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.element_to_be_clickable(
                    self.CONTINUE_BTN
                )
            )

            second_continue.click()

        except Exception:
            pass

        # Wait until OTP field appears
        WebDriverWait(self.driver, 180).until(
            EC.presence_of_element_located(
                self.OTP_INPUT
            )
        )

        # Wait until user logs in
        WebDriverWait(self.driver, 300).until(
            EC.url_contains("checkout")
        )