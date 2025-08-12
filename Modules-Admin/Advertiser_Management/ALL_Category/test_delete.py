import time
import pytest
import os
import sys
import allure
import random
import string

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from allure_commons.types import AttachmentType

from utilities.readProp import ReadConfig

# Add the project root (D:\Automation\) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


@pytest.mark.usefixtures("browser_setup")
class TestAdvertiser:

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    advertiser_category_element = "//span[text()='Ads List']"
    edit_element = "(//span[contains(@class, 'editdropdown-button')])[1]"
    delete_menu = "(//span[contains(text(), 'Delete')])[1]"
    confirm_delete_button = "(//span[contains(text(), 'Delete')])[2]"

    def test_advertiser_delete(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        actions = ActionChains(self.driver)

        # Step 1: Login
        with allure.step("Login to Admin Panel"):
            self.driver.get(ReadConfig.getAdminPageURL())
            self.driver.maximize_window()

            wait.until(EC.presence_of_element_located((By.XPATH, self.email_element))).send_keys(ReadConfig.getAdminId())
            wait.until(EC.presence_of_element_located((By.XPATH, self.password_element))).send_keys(ReadConfig.getPassword())
            wait.until(EC.element_to_be_clickable((By.XPATH, self.login_element))).click()
            allure.attach(self.driver.get_screenshot_as_png(), name="Login_Success", attachment_type=AttachmentType.PNG)

        # Step 2: Navigate to Ads List
        with allure.step("Navigate to Ads List"):
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            advertiser = wait.until(EC.presence_of_element_located((By.XPATH, self.advertiser_category_element)))
            self.driver.execute_script("arguments[0].click();", advertiser)
            time.sleep(2)

        # Step 3: Hover on Edit Icon and Click Delete
        with allure.step("Click Delete on First Ad"):
            edit = wait.until(EC.presence_of_element_located((By.XPATH, self.edit_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit)
            actions.move_to_element(edit).perform()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, self.delete_menu))).click()
            time.sleep(2)

        # Step 4: Confirm Deletion
        with allure.step("Confirm Deletion"):
            wait.until(EC.presence_of_element_located((By.XPATH, self.confirm_delete_button))).click()
            time.sleep(3)
            allure.attach(self.driver.get_screenshot_as_png(), name="Deleted_Successfully", attachment_type=AttachmentType.PNG)

    def teardown_method(self, method):
        """Close the browser after each test method"""
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Driver quit failed: {e}")
