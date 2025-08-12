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
@allure.feature("Forgot Password - Success")
@allure.title("Test Successful Password Reset Request")
class TestForgotPasswordSuccess:

    def test_successful_password_reset_request(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()
        # IMPORTANT: Use an email that is known to be registered in your test environment
        registered_email = "ruban@webnexs.in"

        try:
            with allure.step("Step 1: Navigate to Forgot Password Page"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["forgot_link"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Forgot_Password_Page", attachment_type=AttachmentType.PNG)

            with allure.step(f"Step 2: Enter registered email: {registered_email}"):
                email_input = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email_field"])))
                email_input.clear()
                email_input.send_keys(registered_email)
                allure.attach(self.driver.get_screenshot_as_png(), name="Entered_Registered_Email", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Click Submit button"):
                submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["submit_btn"])))
                submit_btn.click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Submit", attachment_type=AttachmentType.PNG)

            with allure.step("Step 4: Validate success toast message"):
                toast = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["toast"])))
                toast_text = toast.text.strip().lower()
                allure.attach(self.driver.get_screenshot_as_png(), name="Success_Toast", attachment_type=AttachmentType.PNG)
                print(f"✅ Success Toast Message: {toast.text}")

                # Assert that the toast indicates success
                assert "otp sent successfully" in toast_text or "email sent" in toast_text, \
                    f"Unexpected success message: {toast.text}"

        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Error_Screenshot", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {str(e)}")

    def teardown_class(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"⚠️ Driver quit failed: {str(e)}")
