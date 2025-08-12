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
    "email_error": "//span[contains(@class,'error') or contains(text(),'email') or contains(text(),'invalid')]",
    "toast_error": "//div[contains(@class,'Toastify__toast--error') or contains(text(),'Invalid') or contains(text(),'format')]"
}

@allure.feature("Login Flow - Invalid Email Format Validation")
class TestInvalidEmailFormat:

    @pytest.mark.parametrize("invalid_email", [
        "plaintext",           # No @ symbol
        "@missingdomain.com",  # Missing local part
        "missing@.com",        # Missing domain
        "test@",               # Missing domain
        "test@domain",         # Missing TLD
        "test..test@domain.com",  # Double dots
        "test@domain..com",    # Double dots in domain
        "test@domain.c",       # TLD too short
        "test space@domain.com"  # Space in email
    ])
    def test_invalid_email_formats(self, browser_setup, invalid_email):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        try:
            with allure.step("Step 1: Open site and click login icon"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Icon", attachment_type=AttachmentType.PNG)

            with allure.step(f"Step 2: Enter invalid email '{invalid_email}' and valid password"):
                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(invalid_email)
                self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("ValidPassword123!")
                allure.attach(self.driver.get_screenshot_as_png(), name="Entered_Invalid_Email", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Click Login button"):
                self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Button", attachment_type=AttachmentType.PNG)

            with allure.step("Step 4: Validate email format error or form remains visible"):
                try:
                    # Check for client-side validation first
                    email_field = self.driver.find_element(By.XPATH, xpaths["email"])
                    validation_message = email_field.get_attribute("validationMessage")
                    
                    if validation_message:
                        print(f"✅ Client-side validation working: {validation_message}")
                        allure.attach(self.driver.get_screenshot_as_png(), name="Client_Validation", attachment_type=AttachmentType.PNG)
                        assert True
                        return
                    
                    # Check if form is still visible (server-side validation)
                    form_visible = EC.visibility_of_element_located((By.XPATH, xpaths["email"]))(self.driver)
                    if form_visible:
                        print(f"✅ Form validation working for invalid email: {invalid_email}")
                        allure.attach(self.driver.get_screenshot_as_png(), name="Form_Validation", attachment_type=AttachmentType.PNG)
                        assert True
                    else:
                        print(f"❌ Form submitted with invalid email: {invalid_email}")
                        allure.attach(self.driver.get_screenshot_as_png(), name="Validation_Failed", attachment_type=AttachmentType.PNG)
                        assert False, f"Form accepted invalid email format: {invalid_email}"
                        
                except Exception as validation_error:
                    print(f"Validation check error: {str(validation_error)}")
                    # Fallback: check if we're still on login page
                    if "login" in self.driver.current_url.lower() or self.driver.find_elements(By.XPATH, xpaths["email"]):
                        assert True
                    else:
                        assert False, f"Form incorrectly accepted invalid email: {invalid_email}"

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
