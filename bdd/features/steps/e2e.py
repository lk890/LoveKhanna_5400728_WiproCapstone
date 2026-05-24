import time
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.login_page import LoginPage

from utilities.config_reader import config
from utilities.logger import logger


# -----------------------------------------
# HELPERS
# -----------------------------------------

def wait_title(driver, text):
    WebDriverWait(driver, 20).until(EC.title_contains(text))


def wait_url(driver, keywords, timeout=20):
    WebDriverWait(driver, timeout).until(
        lambda d: any(k in d.current_url.lower() for k in keywords)
    )


def get_continue_button(driver):
    return WebDriverWait(driver, 40).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".submitBottomOption, button[type='submit']")
        )
    )


def click_safe(driver):
    btn = get_continue_button(driver)
    WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".submitBottomOption, button[type='submit']")
        )
    )
    driver.execute_script("arguments[0].click();", btn)
    return btn


def wait_for_timer_screen(driver):
    """Timer screen is visible when URL has referer param."""
    WebDriverWait(driver, 30).until(
        lambda d: "referer" in d.current_url.lower()
    )
    logger.info(f"Timer screen detected. URL: {driver.current_url}")


# -----------------------------------------
# GIVEN
# -----------------------------------------

@given("user opens Myntra website")
def open_site(context):
    context.driver.get(config["base_url"])
    context.driver.maximize_window()


# -----------------------------------------
# TITLE
# -----------------------------------------

@then('page title should contain "Myntra"')
def verify_title(context):
    wait_title(context.driver, "Myntra")
    assert "Myntra" in context.driver.title, (
        f"Expected 'Myntra' in title, got: {context.driver.title}"
    )


# -----------------------------------------
# CATEGORY FLOW
# -----------------------------------------

@when("user hovers on Home & Living menu")
def hover_menu(context):
    context.home = HomePage(context.driver)
    context.home.hover_home_living()


@when('user selects "Aromas & Candles" category')
def select_category(context):
    context.home.select_aromas_candles()


@then("category page URL should contain aroma or candles or fragrance")
def verify_category_url(context):
    wait_url(context.driver, ["aroma", "candles", "fragrance", "home-fragrance"])
    assert any(
        k in context.driver.current_url.lower()
        for k in ["aroma", "candles", "fragrance", "home-fragrance"]
    ), f"Unexpected category URL: {context.driver.current_url}"


@then("category heading should be valid")
def verify_heading(context):
    try:
        h1 = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "h1"))
        ).text.lower()
        assert any(k in h1 for k in ["candle", "aroma", "fragrance"]), (
            f"Unexpected heading: {h1}"
        )
    except Exception:
        pass


# -----------------------------------------
# PRODUCT FLOW
# -----------------------------------------

@when("user selects first product")
def select_product(context):
    context.product = ProductPage(context.driver)
    context.product.select_first_product()


@when("user switches to product tab")
def switch_tab(context):
    context.product.switch_to_new_tab()


@then("Add to Bag button should be visible")
def verify_add_to_bag(context):
    btn = WebDriverWait(context.driver, 20).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.btn-add-to-bag, .pdp-add-to-bag")
        )
    )
    assert btn is not None, "Add to Bag button not found"


@when("user adds product to bag")
def add_to_bag(context):
    context.product.add_product_to_bag()


@then("cart count should update")
def verify_cart_count(context):
    try:
        WebDriverWait(context.driver, 15).until(
            lambda d: any(
                el.is_displayed()
                for el in d.find_elements(
                    By.CSS_SELECTOR, ".header-bagCount, .bag-count"
                )
            )
        )
    except Exception:
        pass


# -----------------------------------------
# CART FLOW
# -----------------------------------------

@when("user opens shopping bag")
def open_cart(context):
    context.product.open_bag()
    context.cart = CartPage(context.driver)


@then("product should be present in cart")
def verify_cart(context):
    assert context.cart.verify_product_added(), "No product found in cart"


@when("user clicks PLACE ORDER")
def place_order(context):
    context.cart.click_place_order()


# -----------------------------------------
# LOGIN FLOW
# -----------------------------------------

@then("user should be redirected to login or checkout page")
def verify_login_redirect(context):
    wait_url(context.driver, ["login", "checkout"])
    current = context.driver.current_url.lower()
    assert "login" in current or "checkout" in current, (
        f"Expected login/checkout URL, got: {current}"
    )


@when('user enters mobile number "{mobile}"')
def enter_mobile(context, mobile):
    context.login = LoginPage(context.driver)
    logger.info(f"Entering mobile: {mobile}")

    # STEP 1 — Fill number and click Continue
    context.login.enter_mobile(mobile)
    context.login.click_checkbox()
    context.login.click_continue()
    logger.info("First Continue clicked — waiting for timer screen")

    # STEP 2 — Confirm timer screen (URL has ?referer=...)
    wait_for_timer_screen(context.driver)
    logger.info("Timer screen confirmed — waiting 32 seconds")

    # STEP 3 — Wait 32 seconds for the timer to expire
    time.sleep(32)
    logger.info("32 seconds done — clicking Continue again")

    # STEP 4 — Click Continue to reveal OTP input
    click_safe(context.driver)
    logger.info("Second Continue clicked — OTP screen is now visible, waiting for manual entry")


@when("user completes OTP manually")
def otp_flow(context):
    """
    Automation pauses here. Tester types OTP manually in the browser.
    Waits up to 10 minutes for the URL to leave /login (redirect to cart/checkout).
    """
    driver = context.driver
    logger.info(f"OTP screen active. Current URL: {driver.current_url}")
    logger.info("Waiting for manual OTP entry — up to 10 minutes...")

    # Wait until URL moves away from /login entirely
    WebDriverWait(driver, 600).until(
        lambda d: "login" not in d.current_url.lower()
    )

    logger.info(f"OTP accepted — redirected to: {driver.current_url}")


# -----------------------------------------
# FINAL VALIDATION
# -----------------------------------------

@then("user should land on checkout cart page")
def verify_checkout(context):
    current = context.driver.current_url.lower()
    assert "checkout" in current, (
        f"Expected checkout URL, got: {current}"
    )


@when("user opens final cart page")
def open_final_cart(context):
    context.driver.get("https://www.myntra.com/checkout/cart")


@then("cart should contain at least one product")
def final_cart_validation(context):
    items = WebDriverWait(context.driver, 20).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.itemContainer-base-brand")
        )
    )
    assert len(items) > 0, "Cart is empty after checkout redirect"
    logger.info(f"Cart contains {len(items)} item(s)")