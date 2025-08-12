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
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "password_error": "//span[contains(@class,'error') or contains(text(),'required') or contains(text(),'Password')]"
}

@allure.feature("Login Flow - Empty Password Validation")
class TestEmptyPassword:

    def test_empty_password(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        try:
            with allure.step("Step 1: Open site and click login icon"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Icon", attachment_type=AttachmentType.PNG)

            with allure.step("Step 2: Enter email but leave password empty"):
                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys("test@example.com")
                # Leave password field empty intentionally
                allure.attach(self.driver.get_screenshot_as_png(), name="Entered_Only_Email", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Click Login button"):
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_btn"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Button", attachment_type=AttachmentType.PNG)

            with allure.step("Step 4: Validate password field is still visible (form not submitted)"):
                password_visible = EC.visibility_of_element_located((By.XPATH, xpaths["password"]))(self.driver)
                if password_visible:
                    print("✅ Password field still visible — validation working")
                    allure.attach(self.driver.get_screenshot_as_png(), name="Validation_Passed", attachment_type=AttachmentType.PNG)
                    assert True
                else:
                    print("❌ Password field disappeared — form submitted wrongly")
                    allure.attach(self.driver.get_screenshot_as_png(), name="Validation_Failed", attachment_type=AttachmentType.PNG)
                    assert False, "Form submitted even with empty password"

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
