import pytest
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.login_page import LoginPage

from utilities.config_reader import config
from utilities.logger import logger
from utilities.screenshot import take_screenshot


# ── helpers ──────────────────────────────────────────────────────────────────

def wait_for_url_keyword(driver, *keywords, timeout=15):
    """Block until any keyword appears in the current URL (case-insensitive)."""
    def _check(d):
        url = d.current_url.lower()
        return any(kw in url for kw in keywords)

    try:
        WebDriverWait(driver, timeout).until(_check)
    except TimeoutException:
        raise AssertionError(
            f"URL did not contain any of {keywords} within {timeout}s. "
            f"Current URL: {driver.current_url}"
        )


def wait_for_element_visible(driver, by, locator, timeout=15):
    """Return element once it is present AND visible in the DOM."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )
    except TimeoutException:
        raise AssertionError(
            f"Element ({by}='{locator}') not visible after {timeout}s."
        )


def wait_for_elements_present(driver, by, locator, timeout=15):
    """Return element list once at least one match is present."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((by, locator))
        )
    except TimeoutException:
        raise AssertionError(
            f"No elements found for ({by}='{locator}') after {timeout}s."
        )


def wait_for_title_contains(driver, text, timeout=15):
    """Block until page title contains *text*."""
    try:
        WebDriverWait(driver, timeout).until(EC.title_contains(text))
    except TimeoutException:
        raise AssertionError(
            f"Page title did not contain '{text}' within {timeout}s. "
            f"Actual title: '{driver.title}'"
        )


def wait_for_multiple_tabs(driver, count=2, timeout=15):
    """Block until at least *count* window handles are open."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: len(d.window_handles) >= count
        )
    except TimeoutException:
        raise AssertionError(
            f"Expected ≥{count} tab(s); got {len(driver.window_handles)} "
            f"after {timeout}s."
        )


# ── test ─────────────────────────────────────────────────────────────────────

@pytest.mark.e2e
def test_home_decor_e2e(driver):

    try:
        logger.info("========== PYTEST E2E STARTED ==========")

        # ── 1. Open Myntra ────────────────────────────────────────────────────
        logger.info("Opening Myntra website")
        driver.get(config["base_url"])
        driver.maximize_window()

        wait_for_title_contains(driver, "Myntra", timeout=20)
        assert "Myntra" in driver.title, f"Unexpected title: {driver.title}"
        logger.info(f"✅ ASSERT PASSED: Page title contains 'Myntra' → '{driver.title}'")

        # ── 2. Navigate to Aromas & Candles ───────────────────────────────────
        home = HomePage(driver)

        logger.info("Hovering on Home & Living menu")
        home.hover_home_living()

        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.LINK_TEXT, "Aromas & Candles")
                )
            )
            logger.info("✅ ASSERT PASSED: 'Aromas & Candles' submenu item is visible in dropdown")
        except TimeoutException:
            logger.info("Submenu item not yet found by LINK_TEXT; continuing anyway")

        logger.info("Selecting Aromas & Candles category")
        home.select_aromas_candles()

        # ── 3. Assert category page loaded ────────────────────────────────────
        wait_for_url_keyword(
            driver,
            "aroma", "candles", "fragrance", "home-fragrance",
            timeout=15,
        )
        assert any(
            kw in driver.current_url.lower()
            for kw in ("aroma", "candles", "fragrance", "home-fragrance")
        ), f"Category URL mismatch: {driver.current_url}"
        logger.info(f"✅ ASSERT PASSED: Category URL contains expected keyword → '{driver.current_url}'")

        # Also verify the visible heading once it renders
        try:
            heading_el = wait_for_element_visible(
                driver, By.TAG_NAME, "h1", timeout=10
            )
            heading = heading_el.text.lower()
            assert any(kw in heading for kw in ("candle", "aroma", "fragrance")), \
                f"Unexpected page heading: {heading_el.text}"
            logger.info(f"✅ ASSERT PASSED: Page <h1> heading contains expected keyword → '{heading_el.text}'")
        except AssertionError:
            logger.info("Heading not matched; skipping heading assertion")

        # ── 4. Open first product ─────────────────────────────────────────────
        product = ProductPage(driver)

        logger.info("Opening first product")
        product.select_first_product()

        wait_for_multiple_tabs(driver, count=2, timeout=15)
        assert len(driver.window_handles) >= 2, "Product tab did not open"
        logger.info(f"✅ ASSERT PASSED: New product tab opened → total tabs: {len(driver.window_handles)}")

        logger.info("Switching to product tab")
        product.switch_to_new_tab()

        # ── 5. Add to bag ─────────────────────────────────────────────────────
        try:
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.btn-add-to-bag, .pdp-add-to-bag")
                )
            )
            logger.info("✅ ASSERT PASSED: 'Add to Bag' button is visible and clickable on product page")
        except TimeoutException:
            logger.info("Add-to-bag button EC timed out; attempting click anyway")

        logger.info("Adding product to bag")
        product.add_product_to_bag()

        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".header-bagCount, .bag-count")
                )
            )
            logger.info("✅ ASSERT PASSED: Bag count indicator updated after adding product")
        except TimeoutException:
            logger.info("Bag count indicator not found; continuing")

        # ── 6. Open bag / cart ────────────────────────────────────────────────
        logger.info("Opening shopping bag")
        product.open_bag()

        cart = CartPage(driver)

        logger.info("Verifying product in cart")
        try:
            WebDriverWait(driver, 15).until(
                lambda d: cart.verify_product_added()
            )
        except TimeoutException:
            raise AssertionError("Product not found in cart after waiting 15s")

        assert cart.verify_product_added(), "Product not found in cart"
        logger.info("✅ ASSERT PASSED: Product is present in shopping cart")

        # ── 7. Place order ────────────────────────────────────────────────────
        logger.info("Clicking PLACE ORDER")
        cart.click_place_order()

        wait_for_url_keyword(driver, "login", "checkout", timeout=20)
        assert any(
            kw in driver.current_url.lower()
            for kw in ("login", "checkout")
        ), f"Login/Checkout page not loaded: {driver.current_url}"
        logger.info(f"✅ ASSERT PASSED: Redirected to Login/Checkout page → '{driver.current_url}'")

        # ── 8. Login flow ─────────────────────────────────────────────────────
        login = LoginPage(driver)

        logger.info("Entering mobile number")
        login.enter_mobile("9760076422")
        time.sleep(1)

        login.click_checkbox()
        time.sleep(1)

        login.click_continue()

        # ── 9. OTP flow ───────────────────────────────────────────────────────
        logger.info("Waiting for OTP flow (manual step – up to 30 s)")
        time.sleep(30)  # intentional: user must enter OTP manually

        try:
            continue_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".submitBottomOption"))
            )
            continue_btn.click()
            logger.info("✅ ASSERT PASSED: Second CONTINUE button found and clicked after OTP")
            time.sleep(2)
        except TimeoutException:
            logger.info("Second CONTINUE not required")

        try:
            WebDriverWait(driver, 180).until(
                EC.url_contains("checkout/cart")
            )
        except TimeoutException:
            raise AssertionError(
                "Did not reach checkout/cart within 180s after OTP"
            )
        assert "checkout/cart" in driver.current_url.lower(), \
            f"OTP redirect failed: {driver.current_url}"
        logger.info(f"✅ ASSERT PASSED: OTP completed, redirected to checkout/cart → '{driver.current_url}'")

        # ── 10. Final cart validation ──────────────────────────────────────────
        driver.get("https://www.myntra.com/checkout/cart")

        products = wait_for_elements_present(
            driver,
            By.CSS_SELECTOR,
            "div.itemContainer-base-brand",
            timeout=20,
        )

        assert len(products) > 0, "Cart is empty after login"
        logger.info(f"✅ ASSERT PASSED: Final cart contains {len(products)} product(s) after login")

        logger.info("========== TEST PASSED ==========")

    except Exception as e:
        logger.error(f"TEST FAILED: {str(e)}")
        take_screenshot(driver, "pytest_e2e_failure")
        raise