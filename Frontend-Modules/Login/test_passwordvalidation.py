import pytest
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Use ReadConfig for URL

# Centralized XPaths dictionary
xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "toast_error": "//div[contains(@class,'Toastify__toast--error') or contains(text(),'Invalid') or contains(text(),'incorrect')]"
}

@allure.feature("Login Flow - Invalid Password Validation")
class TestInvalidPassword:

    def test_invalid_password(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()  # ✅ Load from config

        try:
            with allure.step("Step 1: Open login page and click login icon"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Icon", attachment_type=AttachmentType.PNG)

            with allure.step("Step 2: Enter valid email and wrong password"):
                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys("test@tests.com")
                self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("program12@1")  # ❌ Invalid password
                allure.attach(self.driver.get_screenshot_as_png(), name="Entered_Email_Wrong_Password", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Click Login button"):
                self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Button", attachment_type=AttachmentType.PNG)

            with allure.step("Step 4: Validate error toast appears"):
                error_toast = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["toast_error"])))
                allure.attach(self.driver.get_screenshot_as_png(), name="Toast_Error", attachment_type=AttachmentType.PNG)
                print("❌ Login failed as expected. Error message:", error_toast.text)
                assert "invalid" in error_toast.text.lower() or "incorrect" in error_toast.text.lower()

        except Exception as e:
            print(f"❌ Test failed due to exception: {str(e)}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Exception_Screenshot", attachment_type=AttachmentType.PNG)
            assert False, str(e)

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("⚠️ Driver not initialized.")
