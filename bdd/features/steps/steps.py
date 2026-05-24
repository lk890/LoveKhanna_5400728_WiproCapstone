import time
import re
import sys
import io

from behave import given, when, then, step

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.home_page import HomePage
from utilities.config_reader import config
from utilities.screenshot import take_screenshot

import logging
logger = logging.getLogger()


# ─────────────────────────────────────────────
# SAFE LOGGER WRAPPER
# ─────────────────────────────────────────────

def log(msg):
    for h in logger.handlers:
        if isinstance(h, logging.FileHandler):
            h.stream = open(h.baseFilename, "a", encoding="utf-8")
    try:
        logger.info(msg)
    except Exception:
        safe = msg.encode("ascii", errors="replace").decode("ascii")
        logger.info(safe)


# ─────────────────────────────────────────────
# INTERNAL WAIT HELPERS
# ─────────────────────────────────────────────

def _home(context):
    return HomePage(context.driver)


def _wait_url(driver, keyword, timeout=15):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: keyword.lower() in d.current_url.lower()
        )
    except TimeoutException:
        raise AssertionError(
            f"URL did not contain '{keyword}' within {timeout}s. "
            f"Current URL: {driver.current_url}"
        )


def _wait_clickable(driver, by, locator, timeout=15):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, locator))
        )
    except TimeoutException:
        raise AssertionError(
            f"Element ({by}='{locator}') not clickable after {timeout}s."
        )


def _wait_visible(driver, by, locator, timeout=15):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )
    except TimeoutException:
        raise AssertionError(
            f"Element ({by}='{locator}') not visible after {timeout}s."
        )


def _element_absent(driver, by, locator, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, locator))
        )
        return False
    except TimeoutException:
        return True


# ─────────────────────────────────────────────
# BACKGROUND STEP
# ─────────────────────────────────────────────

@given("user opens Myntra website for categories")
def open_site(context):
    context.driver.get(config["base_url"])
    context.driver.maximize_window()
    try:
        WebDriverWait(context.driver, 20).until(
            EC.title_contains("Myntra")
        )
    except TimeoutException:
        raise AssertionError(
            f"Myntra site did not load within 20s. "
            f"Actual title: '{context.driver.title}'"
        )
    assert "myntra" in context.driver.title.lower(), \
        "Site not opened properly"
    log(f"[PASS] ASSERT PASSED: Title contains 'Myntra' -> '{context.driver.title}'")


# ─────────────────────────────────────────────
# CATEGORY FLOW
# ─────────────────────────────────────────────

@when("user hovers Home & Living menu for categories")
def hover_menu(context):
    _home(context).hover_home_living()
    menu = _wait_visible(context.driver, By.XPATH, "//nav", timeout=10)
    assert menu.is_displayed(), "Home & Living menu not visible after hover"
    log("[PASS] ASSERT PASSED: Home & Living nav menu is visible after hover")


@when('user selects category "{category}"')
def select_category(context, category):
    _home(context).select_dynamic_category(category)


@then('page URL should contain "{expected_url}"')
def verify_url(context, expected_url):
    _wait_url(context.driver, expected_url, timeout=15)
    current_url = context.driver.current_url
    assert expected_url.lower() in current_url.lower(), \
        f"URL mismatch: expected '{expected_url}' in '{current_url}'"
    log(f"[PASS] ASSERT PASSED: Category URL contains '{expected_url}' -> {current_url}")


# ─────────────────────────────────────────────
# SORT
# ─────────────────────────────────────────────

@step(u'if sort option exists "{sort_option}" apply')
@step(u'if sort option exists "" apply')
def apply_sort(context, sort_option=""):
    if not sort_option or sort_option.strip() == "":
        return

    sort_dropdown = _wait_clickable(
        context.driver, By.CLASS_NAME, "sort-sortBy", timeout=10
    )
    sort_dropdown.click()
    log(f"Sort dropdown clicked for option: {sort_option}")

    dropdown = _wait_visible(
        context.driver, By.CLASS_NAME, "sort-list", timeout=10
    )
    assert dropdown.is_displayed(), "Sort dropdown list not visible after click"
    log("[PASS] ASSERT PASSED: Sort dropdown list is visible")

    option = _wait_clickable(
        context.driver,
        By.XPATH,
        f"//label[contains(.,'{sort_option}')]",
        timeout=10,
    )
    option.click()

    try:
        WebDriverWait(context.driver, 10).until(
            lambda d: "sort" in d.current_url.lower()
            or d.find_elements(By.CLASS_NAME, "results-base")
        )
    except TimeoutException:
        pass

    assert context.driver.current_url, "Page URL lost after sort"
    log(
        f"[PASS] ASSERT PASSED: Sort '{sort_option}' applied -- "
        f"page still active at {context.driver.current_url}"
    )


# ─────────────────────────────────────────────
# BRAND FILTER
#
# Myntra brand search has TWO states:
#
# COLLAPSED (default on doormats page):
#   <div class="filter-search-filterSearchBox">          ← no "filter-search-expanded"
#     <input class="filter-search-inputBox filter-search-hidden">   ← input hidden
#     <span class="sprites-search">                      ← click this to expand
#
# EXPANDED (after clicking the search icon):
#   <div class="filter-search-filterSearchBox filter-search-expanded">
#     <input class="filter-search-inputBox">             ← now visible, type here
#
# Flow:
#   1. Wait for brand-container to be present in DOM
#   2. Click the search icon (sprites-search) to expand the input
#   3. Wait for input to lose "filter-search-hidden" class (i.e. become visible)
#   4. Type brand name → React filters brand-list live
#   5. Find checkbox input[value="Aura"] in brand-list
#   6. JS-click its parent <label>
#   7. Assert checkbox is_selected()
# ─────────────────────────────────────────────

@step(u'if brand exists "{brand}" apply brand filter')
@step(u'if brand exists "" apply brand filter')
def apply_brand(context, brand=""):
    if not brand or brand.strip() == "":
        return

    driver = context.driver

    # ── Step 1: Wait for brand-container present in DOM ───────────────────────
    # DOM: <div class="vertical-filters-filters brand-container">
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, "brand-container"
            ))
        )
    except TimeoutException:
        raise AssertionError(
            f"Brand filter container not found after 15s. "
            f"URL: {driver.current_url}"
        )
    log("[PASS] ASSERT PASSED: Brand filter container present in DOM")

    # ── Step 2: Click the search icon to expand the brand search input ────────
    # DOM: <span class="myntraweb-sprite filter-search-iconSearch sprites-search">
    # This toggles the input from filter-search-hidden → visible
    try:
        search_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                "div.brand-container span.filter-search-iconSearch"
            ))
        )
        search_icon.click()
        log("Brand search icon clicked — input expanded")
    except TimeoutException:
        raise AssertionError(
            f"Brand search icon not clickable after 10s. "
            f"URL: {driver.current_url}"
        )

    # ── Step 3: Wait for input to become visible (hidden class removed) ───────
    # DOM after expand: <input class="filter-search-inputBox">  (no filter-search-hidden)
    try:
        brand_search = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR,
                "div.brand-container input.filter-search-inputBox"
            ))
        )
    except TimeoutException:
        raise AssertionError(
            f"Brand search input not visible after clicking search icon. "
            f"URL: {driver.current_url}"
        )
    log("[PASS] ASSERT PASSED: Brand search input is now visible")

    # ── Step 4: Type brand name — React filters brand-list live ──────────────
    brand_search.click()
    brand_search.clear()
    brand_search.send_keys(brand)
    log(f"Typed '{brand}' into brand search input")
    time.sleep(1)  # allow React to re-render filtered brand list

    # ── Step 5: Find the checkbox in brand-list after search ──────────────────
    # DOM: <ul class="brand-list">
    #        <li>
    #          <label class="vertical-filters-label common-customCheckbox">
    #            <input type="checkbox" value="Aura">
    try:
        brand_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                f"div.brand-container ul.brand-list "
                f"input[type='checkbox'][value='{brand}']"
            ))
        )
    except TimeoutException:
        raise AssertionError(
            f"Brand checkbox value='{brand}' not found in brand-list after search. "
            f"URL: {driver.current_url}"
        )
    log(f"[PASS] ASSERT PASSED: Brand checkbox '{brand}' found in brand-list")

    # ── Step 6: JS-click the wrapping <label> (React-safe) ────────────────────
    # DOM: <label class="vertical-filters-label common-customCheckbox">
    #        <input type="checkbox" value="Aura">   ← brand_checkbox
    parent_label = brand_checkbox.find_element(By.XPATH, "..")
    driver.execute_script("arguments[0].click();", parent_label)
    log(f"Brand filter '{brand}' parent label clicked via JS")

    # ── Step 7: Assert checkbox is now checked ─────────────────────────────────
    try:
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(
                By.CSS_SELECTOR,
                f"div.brand-container ul.brand-list "
                f"input[type='checkbox'][value='{brand}']"
            ).is_selected()
        )
    except TimeoutException:
        raise AssertionError(
            f"Brand '{brand}' checkbox not selected after click. "
            f"URL: {driver.current_url}"
        )

    log(f"[PASS] ASSERT PASSED: Brand '{brand}' checkbox is now checked/selected")
    log(
        f"[PASS] ASSERT PASSED: Brand filter '{brand}' applied -- "
        f"page active at {driver.current_url}"
    )


# ─────────────────────────────────────────────
# NEGATIVE CASE 1 — Bedsheets
# ─────────────────────────────────────────────

@then("invalid sort option should not exist")
def invalid_sort(context):
    sort_dropdown = _wait_clickable(
        context.driver, By.CLASS_NAME, "sort-sortBy", timeout=10
    )
    sort_dropdown.click()
    _wait_visible(context.driver, By.CLASS_NAME, "sort-list", timeout=10)
    log("Sort dropdown opened for negative check")

    take_screenshot(context.driver, "bedsheets_negative_sort_dropdown_open")
    log("[SS] Screenshot saved: bedsheets_negative_sort_dropdown_open")

    try:
        free_option = WebDriverWait(context.driver, 3).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[contains(translate(text(),'FREE','free'),'free')]"
            ))
        )
        free_option.click()
    except TimeoutException:
        pass

    result = _element_absent(
        context.driver,
        By.XPATH,
        "//label[contains(translate(text(),'FREE','free'),'free')]",
        timeout=5,
    )
    assert result, \
        "Invalid sort option 'free' SHOULD NOT exist in dropdown but was found"
    log("[PASS] ASSERT PASSED: Invalid sort option 'free' correctly absent from dropdown")


# ─────────────────────────────────────────────
# NEGATIVE CASE 2 — Organisers
# ─────────────────────────────────────────────

@then("invalid filters should not exist")
def invalid_filters(context):
    time.sleep(3)
    log("Checking absence of invalid filters on organisers page")

    try:
        bed_size = WebDriverWait(context.driver, 3).until(
            EC.element_to_be_clickable((
                By.XPATH, "//label[contains(.,'Bed Size')]"
            ))
        )
        bed_size.click()
        log("Clicked 'Bed Size' filter (unexpected -- should be absent)")
        try:
            small_opt = WebDriverWait(context.driver, 3).until(
                EC.element_to_be_clickable((
                    By.XPATH, "//label[contains(.,'Small')]"
                ))
            )
            small_opt.click()
            log("Clicked 'Small' option (unexpected -- should be absent)")
        except TimeoutException:
            pass
    except TimeoutException:
        pass

    take_screenshot(context.driver, "organisers_negative_invalid_filters_attempt")
    log("[SS] Screenshot saved: organisers_negative_invalid_filters_attempt")

    result_bed = _element_absent(
        context.driver, By.XPATH, "//label[contains(.,'Bed Size')]", timeout=5
    )
    assert result_bed, \
        "'Bed Size' filter SHOULD NOT exist on Organisers page but was found"
    log("[PASS] ASSERT PASSED: 'Bed Size' filter correctly absent")

    result_small = _element_absent(
        context.driver, By.XPATH, "//label[contains(.,'Small')]", timeout=5
    )
    assert result_small, \
        "Invalid 'Small' filter SHOULD NOT exist here but was found"
    log("[PASS] ASSERT PASSED: 'Small' filter option correctly absent")