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
@allure.feature("Forgot Password - Whitespace Handling")
@allure.title("Test Forgot Password with Leading/Trailing Whitespace in Email")
class TestForgotPasswordWhitespace:

    @pytest.mark.parametrize("email_with_whitespace", [
        "  ruban@webnexs.in",  # Leading whitespace
        "ruban@webnexs.in  ",  # Trailing whitespace
        "  ruban@webnexs.in  "   # Both leading and trailing
    ])
    def test_whitespace_in_email(self, browser_setup, email_with_whitespace):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        try:
            with allure.step("Step 1: Navigate to Forgot Password Page"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["forgot_link"]))).click()

            with allure.step(f"Step 2: Enter email with whitespace: '{email_with_whitespace}'"):
                email_input = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email_field"])))
                email_input.clear()
                email_input.send_keys(email_with_whitespace)
                allure.attach(self.driver.get_screenshot_as_png(), name="Entered_Whitespace_Email", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Click Submit button"):
                submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["submit_btn"])))
                submit_btn.click()

            with allure.step("Step 4: Validate success toast, confirming whitespace was trimmed"):
                toast = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["toast"])))
                toast_text = toast.text.strip().lower()
                allure.attach(self.driver.get_screenshot_as_png(), name="Success_Toast_Whitespace", attachment_type=AttachmentType.PNG)
                print(f"✅ Success Toast with whitespace: {toast.text}")

                assert "otp sent successfully" in toast_text or "email sent" in toast_text, \
                    f"Whitespace was likely not trimmed. Unexpected message: {toast.text}"

        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Error_Screenshot", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {str(e)}")

    def teardown_class(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"⚠️ Driver quit failed: {str(e)}")

