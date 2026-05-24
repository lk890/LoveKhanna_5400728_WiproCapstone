from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):

    # Locator for all visible products
    PRODUCTS = (
        By.XPATH,
        "//li[contains(@class,'product-base')]"
    )

    # Locator for Add to Bag button
    ADD_TO_BAG = (
        By.XPATH,
        "//div[contains(text(),'ADD TO BAG')]"
    )

    # Locator for Bag button in header
    BAG_BUTTON = (
        By.XPATH,
        "//span[contains(text(),'Bag')]"
    )

    def select_first_product(self):

        # Fetch all available products
        products = self.get_elements(self.PRODUCTS)

        # Open first product from listing
        products[0].click()

    def switch_to_new_tab(self):

        # Switch webdriver control to newly opened tab
        self.driver.switch_to.window(
            self.driver.window_handles[1]
        )

    def add_product_to_bag(self):

        # Click Add to Bag button
        self.click_element(self.ADD_TO_BAG)

    def open_bag(self):

        # Open shopping bag/cart page
        self.click_element(self.BAG_BUTTON)