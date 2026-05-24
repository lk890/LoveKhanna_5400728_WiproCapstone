from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:

    def __init__(self, driver):

        # Store webdriver instance
        self.driver = driver

    # Locator for PLACE ORDER button
    PLACE_ORDER_BTN = (
        By.XPATH,
        "//div[text()='PLACE ORDER']/parent::button"
    )

    # Locator for product name displayed in cart
    PRODUCT_NAME = (
        By.CSS_SELECTOR,
        "div.itemContainer-base-brand"
    )

    def click_place_order(self):

        try:

            # Wait until place order button becomes clickable
            wait = WebDriverWait(self.driver, 15)

            button = wait.until(
                EC.element_to_be_clickable(
                    self.PLACE_ORDER_BTN
                )
            )

            # Click place order button
            button.click()

        except Exception as e:

            raise Exception(
                f"Place Order button click failed: {str(e)}"
            )

    def verify_product_added(self):

        try:

            # Wait until product appears inside cart
            wait = WebDriverWait(self.driver, 15)

            product = wait.until(
                EC.presence_of_element_located(
                    self.PRODUCT_NAME
                )
            )

            # Return True if product is visible
            return product.is_displayed()

        except Exception as e:

            raise Exception(
                f"Product verification failed: {str(e)}"
            )