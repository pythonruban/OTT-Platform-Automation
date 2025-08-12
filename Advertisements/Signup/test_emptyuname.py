import pytest
import allure
import time
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig


xpaths = {
    "sign_up_link": "//a[@id='advertiserSignup']",
    "company_name": "//input[@id='company_name']",
    "email": "//input[@id='signupemail']",
    "phone": "//input[@placeholder='Enter your phone number']",
    "license": "//input[@id='license_number']",
    "address": "//input[@id='address']",
    "password": "//input[@id='signuppassword']",
    "submit_btn": "//button[@type='submit']"
}


@pytest.mark.usefixtures("browser_setup")
class TestAdvertiserSignUp:

    def test_advertiser_signup_form(self, browser_setup):
        self.driver = browser_setup
        self.wait = WebDriverWait(self.driver, 20)

        try:
            # STEP 1: Open Sign-Up Page
            self.driver.get(ReadConfig.getAdvertiserPageURL())
            self.driver.maximize_window()

            # STEP 2: Click Sign-Up Link
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["sign_up_link"]))).click()

            # STEP 3: Fill the form
            random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            company_name = ""
            email = f"testuser_{random_suffix}@testmail.com"
            phone = "9876543210"
            license_number = "1234569874568755"
            address = "123 Main Street"
            password = "Test@1234"

            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["company_name"]))).send_keys(company_name)
            self.driver.find_element(By.XPATH, xpaths["email"]).send_keys(email)
            self.driver.find_element(By.XPATH, xpaths["phone"]).send_keys(phone)
            self.driver.find_element(By.XPATH, xpaths["license"]).send_keys(license_number)
            self.driver.find_element(By.XPATH, xpaths["address"]).send_keys(address)
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(password)

            # STEP 4: Submit Form
            self.driver.find_element(By.XPATH, xpaths["submit_btn"]).click()

            # STEP 5: Wait and verify redirect / success (customize as needed)
            time.sleep(3)  # Optional: replace with redirect condition
            allure.attach(self.driver.get_screenshot_as_png(), name="SignUp_Success", attachment_type=AttachmentType.PNG)

            print("✅ Sign-up test passed successfully.")

        except Exception as e:
            print("❌ Sign-up test failed:", str(e))
            allure.attach(self.driver.get_screenshot_as_png(), name="SignUp_Failure", attachment_type=AttachmentType.PNG)
            raise
