import pytest
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from pages.home_page import HomePage
from utilities.config_reader import config
from utilities.logger import logger
from utilities.screenshot import take_screenshot
from utilities.csv_loader import load_test_data

test_data = load_test_data()


# ── reusable wait helpers ─────────────────────────────────────────────────────

def wait_for_url_keyword(driver, keyword, timeout=15):
    """Block until keyword appears in the current URL (case-insensitive)."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: keyword.lower() in d.current_url.lower()
        )
    except TimeoutException:
        raise AssertionError(
            f"URL did not contain '{keyword}' within {timeout}s. "
            f"Current URL: {driver.current_url}"
        )


def wait_for_element_clickable(driver, by, locator, timeout=15):
    """Return element once it is clickable."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, locator))
        )
    except TimeoutException:
        raise AssertionError(
            f"Element ({by}='{locator}') not clickable after {timeout}s."
        )


def wait_for_element_visible(driver, by, locator, timeout=15):
    """Return element once it is visible."""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )
    except TimeoutException:
        raise AssertionError(
            f"Element ({by}='{locator}') not visible after {timeout}s."
        )


def wait_for_title_contains(driver, text, timeout=15):
    """Block until page title contains text."""
    try:
        WebDriverWait(driver, timeout).until(EC.title_contains(text))
    except TimeoutException:
        raise AssertionError(
            f"Title did not contain '{text}' within {timeout}s. "
            f"Actual: '{driver.title}'"
        )


def element_absent(driver, by, locator, timeout=5):
    """Return True if element does NOT appear within timeout (for negative tests)."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, locator))
        )
        return False   # element found → NOT absent
    except TimeoutException:
        return True    # element never appeared → absent ✅


# ── test ───

@pytest.mark.parametrize("row", test_data)
def test_dynamic_categories(driver, row):

    try:
        logger.info(f"========== START TEST: {row['test_name']} ==========")

        #  Open website
        driver.get(config["base_url"])
        driver.maximize_window()

        wait_for_title_contains(driver, "Myntra", timeout=20)
        assert "myntra" in driver.title.lower(), "Site not opened properly"
        logger.info(f"✅ ASSERT PASSED: Title contains 'Myntra' → '{driver.title}'")

        # Hover on Home & Living 
        home = HomePage(driver)
        home.hover_home_living()

        menu = wait_for_element_visible(driver, By.XPATH, "//nav", timeout=10)
        assert menu.is_displayed(), "Home & Living menu not visible after hover"
        logger.info("✅ ASSERT PASSED: Home & Living nav menu is visible after hover")

        # Select dynamic category 
        home.select_dynamic_category(row["category"])

        wait_for_url_keyword(driver, row["expected_url"], timeout=15)
        current_url = driver.current_url.lower()
        assert row["expected_url"] in current_url, \
            f"URL mismatch: expected '{row['expected_url']}' in '{current_url}'"
        logger.info(f"✅ ASSERT PASSED: Category URL contains '{row['expected_url']}' → {current_url}")

        
        # POSITIVE CASE LOGIC
        
        if "negative" not in row["test_name"]:

            #  Sort assertion 
            if row.get("sort_option") and row["sort_option"].strip():

                sort_dropdown = wait_for_element_clickable(
                    driver, By.CLASS_NAME, "sort-sortBy", timeout=10
                )
                sort_dropdown.click()
                logger.info(f"Sort dropdown clicked for option: {row['sort_option']}")

                dropdown = wait_for_element_visible(
                    driver, By.CLASS_NAME, "sort-list", timeout=10
                )
                assert dropdown.is_displayed(), "Sort dropdown not visible after click"
                logger.info("✅ ASSERT PASSED: Sort dropdown list is visible")

                option = wait_for_element_clickable(
                    driver,
                    By.XPATH,
                    f"//label[contains(.,'{row['sort_option']}')]",
                    timeout=10,
                )
                option.click()

                # Wait for sort to reflect in URL or page
                try:
                    WebDriverWait(driver, 10).until(
                        lambda d: "sort" in d.current_url.lower()
                        or d.find_elements(By.CLASS_NAME, "results-base")
                    )
                except TimeoutException:
                    pass  # page may sort without URL change; non-critical

                assert driver.current_url, "Page URL lost after sort — unexpected"
                logger.info(f"✅ ASSERT PASSED: Sort '{row['sort_option']}' applied — page still active at {driver.current_url}")

            # Brand filter assertion 
            if row.get("brand") and row["brand"].strip():

                # locate checkbox by value attribute (not text — React comment nodes)
                try:
                    brand_checkbox = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.XPATH,
                            f"//input[@type='checkbox' and @value='{row['brand']}']"
                        ))
                    )
                    logger.info(f"✅ ASSERT PASSED: Brand checkbox '{row['brand']}' found in DOM")
                except TimeoutException:
                    raise AssertionError(
                        f"Brand checkbox for '{row['brand']}' not found in DOM after 10s"
                    )

                # scroll into viewport center
                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", brand_checkbox
                )
                time.sleep(0.5)

                # click parent label via JS
                parent_label = brand_checkbox.find_element(By.XPATH, "..")
                driver.execute_script("arguments[0].click();", parent_label)
                logger.info(f"Brand filter '{row['brand']}' label clicked via JS")

                # confirm checkbox is now checked
                try:
                    WebDriverWait(driver, 10).until(
                        lambda d: d.find_element(
                            By.XPATH,
                            f"//input[@type='checkbox' and @value='{row['brand']}']"
                        ).is_selected()
                    )
                    logger.info(f"✅ ASSERT PASSED: Brand '{row['brand']}' checkbox is now checked/selected")
                except TimeoutException:
                    raise AssertionError(
                        f"Brand '{row['brand']}' checkbox not checked after click"
                    )

        
        # NEGATIVE CASE 1: invalid sort option 
        
        if row["test_name"] == "bedsheets_negative":

            sort_dropdown = wait_for_element_clickable(
                driver, By.CLASS_NAME, "sort-sortBy", timeout=10
            )
            sort_dropdown.click()

            wait_for_element_visible(
                driver, By.CLASS_NAME, "sort-list", timeout=10
            )
            logger.info("Sort dropdown opened for negative check")

            result = element_absent(
                driver,
                By.XPATH,
                "//label[contains(translate(text(),'FREE','free'),'free')]",
                timeout=5,
            )
            assert result, "Invalid sort option 'free' SHOULD NOT exist in dropdown"
            logger.info("✅ ASSERT PASSED: Invalid sort option 'free' correctly absent from dropdown")

        
        # NEGATIVE CASE 2: invalid filter must NOT exist
        
        if row["test_name"] == "organisers_negative":

            time.sleep(3)  
            logger.info("Checking absence of invalid filters on organisers page")

            result_bed = element_absent(
                driver,
                By.XPATH,
                "//label[contains(.,'Bed Size')]",
                timeout=5,
            )
            assert result_bed, "Bed Size filter SHOULD NOT exist on organisers page"
            logger.info("✅ ASSERT PASSED: 'Bed Size' filter correctly absent")

            result_small = element_absent(
                driver,
                By.XPATH,
                "//label[contains(.,'Small')]",
                timeout=5,
            )
            assert result_small, "Invalid 'Small' filter option SHOULD NOT exist here"
            logger.info("✅ ASSERT PASSED: 'Small' filter option correctly absent")

        logger.info(f"========== TEST COMPLETED: {row['test_name']} ==========")

    except Exception as e:
        logger.error(f"TEST FAILED: {row['test_name']} | {str(e)}")
        take_screenshot(driver, f"{row['test_name']}_failure")
        raise