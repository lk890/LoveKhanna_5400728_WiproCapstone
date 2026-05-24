import allure
from selenium import webdriver


def attach_screenshot(driver, name="screenshot"):

    allure.attach(
        driver.get_screenshot_as_png(),
        name=name,
        attachment_type=allure.attachment_type.PNG
    )