import os
import logging

from selenium import webdriver
from datetime import datetime


# =========================================================
# CREATE LOGS FOLDER
# =========================================================

if not os.path.exists("logs"):
    os.makedirs("logs")

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")


# =========================================================
# LOGGER CONFIG
# =========================================================

log_file = f"logs/bdd_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()


# =========================================================
# BEFORE SCENARIO
# =========================================================

def before_scenario(context, scenario):

    logger.info(f"========== START: {scenario.name} ==========")

    context.driver = webdriver.Chrome()

    context.driver.maximize_window()


# =========================================================
# AFTER SCENARIO
# =========================================================

def after_scenario(context, scenario):

    if scenario.status == "failed":

        screenshot_name = (
            f"screenshots/{scenario.name}.png"
        )

        context.driver.save_screenshot(screenshot_name)

        logger.error(
            f"SCENARIO FAILED: {scenario.name}"
        )

        logger.error(
            f"Screenshot saved: {screenshot_name}"
        )

    else:

        logger.info(
            f"SCENARIO PASSED: {scenario.name}"
        )

    context.driver.quit()

    logger.info(
        f"========== END: {scenario.name} =========="
    )