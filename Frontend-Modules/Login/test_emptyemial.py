import pytest
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Use ReadConfig for base URL

# Centralized XPaths
xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']"
}

@allure.feature("Login Flow - Empty Email Validation")
class TestLoginEmptyEmail:

    def test_invalid_email(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()  # ✅ Fetch from config

        try:
            with allure.step("Step 1: Open site and click login icon"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Icon", attachment_type=AttachmentType.PNG)

            with allure.step("Step 2: Leave email empty, enter only password"):
                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["password"]))).send_keys("program12@12A")
                allure.attach(self.driver.get_screenshot_as_png(), name="Entered_Only_Password", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Click Login button"):
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_btn"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Button", attachment_type=AttachmentType.PNG)

            with allure.step("Step 4: Check if email field is still visible"):
                email_visible = EC.visibility_of_element_located((By.XPATH, xpaths["email"]))(self.driver)
                if email_visible:
                    print("✅ Email field still visible — validation working")
                    allure.attach(self.driver.get_screenshot_as_png(), name="Validation_Passed", attachment_type=AttachmentType.PNG)
                    assert True
                else:
                    print("❌ Email field disappeared — form submitted wrongly")
                    allure.attach(self.driver.get_screenshot_as_png(), name="Validation_Failed", attachment_type=AttachmentType.PNG)
                    assert False, "Form submitted even with empty email"

            time.sleep(2)

        except Exception as e:
            print(f"❌ Test failed due to exception: {str(e)}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Error_Screenshot", attachment_type=AttachmentType.PNG)
            assert False, str(e)

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("⚠️ Driver was not initialized.")
