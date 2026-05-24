import pytest
import allure

from selenium import webdriver
from drivers.driver_factory import get_driver

from utilities.logger import logger
from utilities.screenshot import take_screenshot


# ── Driver fixture ────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()


# ── Auto screenshot + allure attach on failure ────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Only act on the actual test call (not setup/teardown)
    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver")

        if driver:
            test_name = item.name

            # ── 1. Save screenshot to file ────────────────────────────────
            screenshot_path = take_screenshot(driver, test_name)
            logger.error(f"📸 Screenshot saved: {screenshot_path}")

            # ── 2. Attach screenshot to allure report ─────────────────────
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"FAILED_{test_name}",
                    attachment_type=allure.attachment_type.PNG,
                )
                logger.error(f"📎 Screenshot attached to Allure report")
            except Exception as e:
                logger.error(f"Allure attach failed: {e}")

            # ── 3. Attach current URL to allure report ────────────────────
            try:
                allure.attach(
                    driver.current_url,
                    name="Failed at URL",
                    attachment_type=allure.attachment_type.TEXT,
                )
            except Exception as e:
                logger.error(f"Allure URL attach failed: {e}")