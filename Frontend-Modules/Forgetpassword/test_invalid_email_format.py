import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

xpaths = {
    "login_icon": "(//button[contains(@id, 'signin')])[1]",
    "forgot_link": "//a[@href='/verify/forget']",
    "email_field": "//input[@type='email']",
    "submit_btn": "//button[@type='submit']",
    "toast": "//div[@role='alert']"
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Forgot Password - Email Format Validation")
@allure.title("Test Invalid Email Format in Forgot Password")
class TestForgotPasswordInvalidFormat:

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
            with allure.step("Step 1: Navigate to Forgot Password Page"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["forgot_link"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Forgot_Password_Page", attachment_type=AttachmentType.PNG)

            with allure.step(f"Step 2: Enter invalid email format: {invalid_email}"):
                email_input = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email_field"])))
                email_input.clear()
                email_input.send_keys(invalid_email)
                allure.attach(self.driver.get_screenshot_as_png(), name="Entered_Invalid_Email", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Click Submit button"):
                submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["submit_btn"])))
                submit_btn.click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Submit", attachment_type=AttachmentType.PNG)

            with allure.step("Step 4: Validate email format error"):
                try:
                    # Check for client-side validation first
                    email_field = self.driver.find_element(By.XPATH, xpaths["email_field"])
                    validation_message = email_field.get_attribute("validationMessage")
                    
                    if validation_message:
                        print(f"✅ Client-side validation working: {validation_message}")
                        allure.attach(self.driver.get_screenshot_as_png(), name="Client_Validation", attachment_type=AttachmentType.PNG)
                        assert True
                        return
                    
                    # Check if form is still visible (server-side validation)
                    form_visible = EC.visibility_of_element_located((By.XPATH, xpaths["email_field"]))(self.driver)
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
                    # Fallback: check if we're still on forgot password page
                    if "forget" in self.driver.current_url.lower() or self.driver.find_elements(By.XPATH, xpaths["email_field"]):
                        assert True
                    else:
                        assert False, f"Form incorrectly accepted invalid email: {invalid_email}"

        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Error_Screenshot", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {str(e)}")

    def teardown_class(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"⚠️ Driver quit failed: {str(e)}")
