import os
from datetime import datetime


def take_screenshot(driver, name):

    folder = "screenshots"
    os.makedirs(folder, exist_ok=True)  # create folder if it doesn't exist

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    path = os.path.join(folder, filename)

    driver.save_screenshot(path)
    return path   # returned so conftest can log the exact path