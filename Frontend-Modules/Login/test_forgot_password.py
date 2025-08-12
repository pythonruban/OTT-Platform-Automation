import pytest
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

# Centralized XPaths
xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "forgot_password_link": "//a[contains(text(),'Forgot Password')]",
    "password_reset_header": "//h1[contains(text(),'Reset Password')]" # Adjust if your reset page has a different identifier
}

@allure.feature("Login Flow - Forgot Password Link")
class TestForgotPassword:

    def test_forgot_password_link_navigation(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        try:
            with allure.step("Step 1: Open site and click login icon"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Icon", attachment_type=AttachmentType.PNG)

            with allure.step("Step 2: Find and click the 'Forgot Password' link"):
                forgot_link = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["forgot_password_link"])))
                forgot_link.click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Forgot_Password_Link", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Validate navigation to the password reset page"):
                # Option 1: Check for a unique element on the reset page
                wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["password_reset_header"])))
                
                # Option 2: Check if the URL contains 'reset-password' or similar
                wait.until(EC.url_contains("reset-password")) # Adjust the keyword as needed
                
                current_url = self.driver.current_url
                print(f"✅ Successfully navigated to password reset page: {current_url}")
                allure.attach(self.driver.get_screenshot_as_png(), name="Password_Reset_Page", attachment_type=AttachmentType.PNG)
                assert "reset-password" in current_url.lower()

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
