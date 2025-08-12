import pytest
import random
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Config reader

xpaths = {
    "signup_button": "//button[@id='home-signup']",
    "first_name": "//input[@id='signup-username']",
    "last_name": "//input[@id='signup-lastname']",
    "email": "//input[@id='signup-email']",
    "country_dropdown": "//div[@role='button']",
    "india_option": "//li[@data-country-code='in']",
    "mobile": "//input[@type='tel']",
   
    "gender": "//select[@id='signup-gender']",
    "country": "//input[@id='signup-country']",
    "state": "//input[@id='signup-state']",
    "city": "//input[@id='signup-city']",
    "password": "//input[@id='signup-password']",
    "confirm_password": "//input[@id='confirmPassword']",
    "accept_terms": "//input[@id='signup-accept']",
    "submit": "//button[@id='signup-submit']",
    "terms_error_text": "//*[contains(text(),'Accept and Terms & Conditions checkbox before proceeding')]"
}

class TestSignupNegative:

    def test_terms_not_accepted(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()  # ✅ Replaced hardcoded URL

        try:
            with allure.step("Open signup page"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["signup_button"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Signup_Page", attachment_type=AttachmentType.PNG)
                time.sleep(5)
            with allure.step("Fill signup form without accepting terms"):
                self.driver.find_element(By.XPATH, xpaths["first_name"]).send_keys("Ruban")
                self.driver.find_element(By.XPATH, xpaths["last_name"]).send_keys("Test")
                email = f"ruban{random.randint(1000,9999)}@webnexs.in"
                self.driver.find_element(By.XPATH, xpaths["email"]).send_keys(email)
                time.sleep(5)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["country_dropdown"]))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["india_option"]))).click()
                phone = f"98765{random.randint(10000,99999)}"
                self.driver.find_element(By.XPATH, xpaths["mobile"]).send_keys(phone)
                self.driver.find_element(By.XPATH, xpaths["gender"]).send_keys("Male")
                self.driver.find_element(By.XPATH, xpaths["country"]).send_keys("India")
                self.driver.find_element(By.XPATH, xpaths["state"]).send_keys("Tamil Nadu")
                self.driver.find_element(By.XPATH, xpaths["city"]).send_keys("Chennai")
                self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("Test@123")
                self.driver.find_element(By.XPATH, xpaths["confirm_password"]).send_keys("Test@123")

                # ❌ DO NOT click the terms checkbox
                allure.attach(self.driver.get_screenshot_as_png(), name="Form_Filled_No_Terms", attachment_type=AttachmentType.PNG)

            with allure.step("Click submit without accepting terms"):
                self.driver.find_element(By.XPATH, xpaths["submit"]).click()

            with allure.step("Verify error message appears"):
                error = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["terms_error_text"])))
                assert error.is_displayed()
                allure.attach(self.driver.get_screenshot_as_png(), name="Terms_Error", attachment_type=AttachmentType.PNG)
                print("✅ Test Passed: Terms not accepted error appeared")

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failed_Screenshot", attachment_type=AttachmentType.PNG)
            print("❌ Test failed:", str(e))
            assert False, "Error message not found or other failure"

        finally:
            self.driver.quit()

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("⚠️ Driver was not initialized.")
