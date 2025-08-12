import os
import sys
import time
import pytest
import allure

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, StaleElementReferenceException, ElementNotInteractableException
)
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

# Add root path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# All XPaths
xpaths = {
    "admin_username": "//input[@id='signin-email']",
    "admin_password": "//input[@id='signin-password']",
    "admin_login_btn": "//span[text()='Login']",
    "Advertiser_category_element": "//span[text()='Advertiser']",
    "rounded_button": "(//button[@class='p-2 rounded-2'])[9]",
    "confirmation_button": "//button[@class='btn btn-primary']"
}


# === Helper: Click Element (with JS fallback and retry) ===
def wait_and_click(driver, wait, xpath, label=""):
    retries = 3
    for attempt in range(retries):
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            try:
                element.click()  # Try native click
            except ElementNotInteractableException:
                print(f"[WARN] {label} not interactable, using JS click.")
                driver.execute_script("arguments[0].click();", element)

            if label:
                allure.attach(driver.get_screenshot_as_png(), name=f"Clicked_{label}", attachment_type=AttachmentType.PNG)
            time.sleep(3)
            break
        except (StaleElementReferenceException, ElementNotInteractableException) as e:
            print(f"[WARN] Retrying click for {label}, attempt {attempt + 1}: {e}")
            time.sleep(1)
        except Exception as e:
            print(f"[ERROR] Failed to click {label}: {e}")
            allure.attach(driver.get_screenshot_as_png(), name=f"Failed_Click_{label}", attachment_type=AttachmentType.PNG)
            raise


# === Helper: Send Keys ===
def wait_and_send_keys(driver, wait, xpath, value, label=""):
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.clear()
        element.send_keys(value)
        if label:
            allure.attach(driver.get_screenshot_as_png(), name=f"Entered_{label}", attachment_type=AttachmentType.PNG)
        time.sleep(3)
    except Exception as e:
        print(f"[ERROR] Couldn't send keys to {label}: {e}")


@pytest.mark.usefixtures("browser_setup")
class TestAdvertiserPopupFlow:

    def test_full_popup_flow(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 20)

        with allure.step("Redirect to Admin and Login"):
            self.driver.get(ReadConfig.getAdminPageURL())
            time.sleep(2)
            wait_and_send_keys(self.driver, wait, xpaths["admin_username"], ReadConfig.getAdminId(), "Admin_Username")
            wait_and_send_keys(self.driver, wait, xpaths["admin_password"], ReadConfig.getPassword(), "Admin_Password")
            wait_and_click(self.driver, wait, xpaths["admin_login_btn"], "Login_Button")

        with allure.step("Scroll and Click Advertiser Menu"):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            wait_and_click(self.driver, wait, xpaths["Advertiser_category_element"], "Advertiser_Menu")

        with allure.step("Click Rounded Button"):
            wait_and_click(self.driver, wait, xpaths["rounded_button"], "Rounded_Button")

        with allure.step("Click Confirmation Button in Popup"):
            wait_and_click(self.driver, wait, xpaths["confirmation_button"], "Confirmation_Button")

    @classmethod
    def teardown_class(cls):
        try:
            cls.driver.quit()
        except:
            print("Driver already closed or not initialized.")
