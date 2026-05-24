from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage

import time


class HomePage(BasePage):

    HOME_LIVING_MENU = (
        By.XPATH,
        "//a[@data-group='home']"
    )

    AROMAS_CANDLES = (
        By.XPATH,
        "//a[contains(text(),'Aromas & Candles')]"
    )

    def hover_home_living(self):

        menu = self.get_element(self.HOME_LIVING_MENU)
        ActionChains(self.driver).move_to_element(menu).perform()
        time.sleep(1)  # small wait so dropdown becomes visible

    def select_aromas_candles(self):

        # Re-hover before clicking so dropdown stays open
        menu = self.get_element(self.HOME_LIVING_MENU)
        ActionChains(self.driver).move_to_element(menu).perform()
        time.sleep(1)

        self.click_element(self.AROMAS_CANDLES)

    def select_dynamic_category(self, category_name):

        # ── Step 1: re-hover so dropdown is open before we try to click ──────
        menu = self.get_element(self.HOME_LIVING_MENU)
        ActionChains(self.driver).move_to_element(menu).perform()
        time.sleep(1)  # let dropdown fully render

        # ── Step 2: wait for the category link to be VISIBLE in dropdown ─────
        locator = (
            By.XPATH,
            f"//a[contains(text(),'{category_name}')]"
        )

        try:
            element = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            raise AssertionError(
                f"Category '{category_name}' not visible in dropdown after 15s"
            )

        # ── Step 3: scroll into view then JS click (avoids interception) ─────
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        self.driver.execute_script("arguments[0].click();", element)