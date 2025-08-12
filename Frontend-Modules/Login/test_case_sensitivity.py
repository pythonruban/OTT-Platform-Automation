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
    "toast_error": "//div[contains(@class,'Toastify__toast--error') or contains(text(),'Invalid') or contains(text(),'incorrect')]"
}

@allure.feature("Login Flow - Password Case-Sensitivity")
class TestCaseSensitivity:

    def test_password_case_sensitive(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()
        correct_password = "Webnexs123!@#"  # The actual password
        incorrect_case_password = "webnexs123!@#"  # The password with incorrect casing

        try:
            with allure.step("Step 1: Open site and click login icon"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Icon", attachment_type=AttachmentType.PNG)

            with allure.step("Step 2: Enter valid email but password with incorrect case"):
                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys("admin@admin.com")
                self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(incorrect_case_password)
                allure.attach(self.driver.get_screenshot_as_png(), name="Entered_Incorrect_Case_Password", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Click Login button"):
                self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Button", attachment_type=AttachmentType.PNG)

            with allure.step("Step 4: Validate error toast appears, confirming case-sensitivity"):
                error_toast = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["toast_error"])))
                allure.attach(self.driver.get_screenshot_as_png(), name="Toast_Error_Case_Sensitive", attachment_type=AttachmentType.PNG)
                print(f"✅ Login failed as expected. Error message: {error_toast.text}")
                assert "invalid" in error_toast.text.lower() or "incorrect" in error_toast.text.lower()

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
