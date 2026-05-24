from behave import given, when, then

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.login_page import LoginPage

from utilities.config_reader import config
from utilities.logger import logger
from utilities.screenshot import take_screenshot


# =========================
# STEP 1: LAUNCH WEBSITE
# =========================
@given("user launches Myntra website")
def step_launch(context):

    try:
        logger.info("STEP 1: Launching Myntra website")

        context.driver.get(config["base_url"])
        context.driver.maximize_window()

        logger.info("Website launched successfully")

    except Exception as e:
        logger.error(f"Launch failed: {str(e)}")
        take_screenshot(context.driver, "launch_failure")
        raise


# =========================
# STEP 2: HOVER MENU
# =========================
@when("user hovers on Home and Living menu")
def step_hover(context):

    try:
        logger.info("STEP 2: Hovering on Home & Living menu")

        home = HomePage(context.driver)
        home.hover_home_living()

        logger.info("Hover successful")

    except Exception as e:
        logger.error(f"Hover failed: {str(e)}")
        take_screenshot(context.driver, "hover_failure")
        raise


# =========================
# STEP 3: SELECT CATEGORY
# =========================
@when("user selects Aromas and Candles category")
def step_select_category(context):

    try:
        logger.info("STEP 3: Selecting Aromas & Candles category")

        home = HomePage(context.driver)
        home.select_aromas_candles()

        logger.info("Category selected successfully")

    except Exception as e:
        logger.error(f"Category selection failed: {str(e)}")
        take_screenshot(context.driver, "category_failure")
        raise


# =========================
# STEP 4: OPEN PRODUCT
# =========================
@when("user opens first product")
def step_open_product(context):

    try:
        logger.info("STEP 4: Opening first product")

        product = ProductPage(context.driver)
        product.select_first_product()

        logger.info("Product opened successfully")

    except Exception as e:
        logger.error(f"Product opening failed: {str(e)}")
        take_screenshot(context.driver, "product_open_failure")
        raise


# =========================
# STEP 5: ADD TO BAG
# =========================
@when("user adds product to shopping bag")
def step_add_bag(context):

    try:
        logger.info("STEP 5: Adding product to bag")

        product = ProductPage(context.driver)

        product.switch_to_new_tab()
        product.add_product_to_bag()
        product.open_bag()

        # IMPORTANT: initialize cart page globally
        context.cart = CartPage(context.driver)

        logger.info("Product added to bag successfully")

    except Exception as e:
        logger.error(f"Add to bag failed: {str(e)}")
        take_screenshot(context.driver, "add_to_bag_failure")
        raise


# =========================
# STEP 6: PLACE ORDER
# =========================
@when("user clicks place order")
def step_place_order(context):

    try:
        logger.info("STEP 6: Clicking Place Order")

        context.cart.click_place_order()

        logger.info("Place order clicked successfully")

    except Exception as e:
        logger.error(f"Place order failed: {str(e)}")
        take_screenshot(context.driver, "place_order_failure")
        raise


# =========================
# STEP 7: LOGIN PAGE
# =========================
@when("user enters mobile number and logs in")
def step_login(context):

    try:
        logger.info("STEP 7: Login started")

        login = LoginPage(context.driver)

        mobile = config.get("mobile_number", "9760076422")

        login.enter_mobile(mobile)
        login.click_checkbox()
        login.click_continue()

        logger.info("Login request submitted")

    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        take_screenshot(context.driver, "login_failure")
        raise


# =========================
# STEP 8: OTP WAIT (MANUAL)
# =========================
@when("user completes OTP manually")
def step_otp(context):

    try:
        logger.info("STEP 8: Waiting for OTP completion (manual)")

        login = LoginPage(context.driver)

        # wait for manual OTP entry
        login.wait_for_otp(180)

        logger.info("OTP completed successfully")

    except Exception as e:
        logger.error(f"OTP handling failed: {str(e)}")
        take_screenshot(context.driver, "otp_failure")
        raise


# =========================
# FINAL ASSERTION
# =========================
@then("product should be visible in cart")
def step_verify(context):

    try:
        logger.info("FINAL STEP: Verifying product in cart")

        assert context.cart.verify_product_added()

        logger.info("Product successfully verified in cart")

    except Exception as e:
        logger.error(f"Cart verification failed: {str(e)}")
        take_screenshot(context.driver, "cart_failure")
        raise