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
    "form_errors": "//span[contains(@class,'error') or contains(text(),'required')]"
}

@allure.feature("Login Flow - Both Fields Empty Validation")
class TestEmptyFields:

    def test_both_fields_empty(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        try:
            with allure.step("Step 1: Open site and click login icon"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Icon", attachment_type=AttachmentType.PNG)

            with allure.step("Step 2: Leave both email and password fields empty"):
                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"])))
                # Both fields remain empty intentionally
                allure.attach(self.driver.get_screenshot_as_png(), name="Both_Fields_Empty", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Click Login button"):
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_btn"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Button", attachment_type=AttachmentType.PNG)

            with allure.step("Step 4: Validate form remains visible (not submitted)"):
                form_visible = EC.visibility_of_element_located((By.XPATH, xpaths["email"]))(self.driver)
                if form_visible:
                    print("✅ Login form still visible — validation working for empty fields")
                    allure.attach(self.driver.get_screenshot_as_png(), name="Validation_Passed", attachment_type=AttachmentType.PNG)
                    assert True
                else:
                    print("❌ Login form disappeared — form submitted incorrectly")
                    allure.attach(self.driver.get_screenshot_as_png(), name="Validation_Failed", attachment_type=AttachmentType.PNG)
                    assert False, "Form submitted with both fields empty"

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
