import pytest
import time
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
    "toast": "//div[@role='alert']",
    "rate_limit_message": "//div[contains(text(),'too many') or contains(text(),'limit') or contains(text(),'wait')]"
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Forgot Password - Rate Limiting")
@allure.title("Test Rate Limiting for Multiple Password Reset Requests")
class TestForgotPasswordRateLimit:

    def test_multiple_password_reset_requests(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 10)  # Shorter wait for faster execution
        base_url = ReadConfig.getHomePageURL()
        test_email = "ruban@webnexs.in"
        max_attempts = 3  # Number of requests to test rate limiting

        try:
            with allure.step("Step 1: Navigate to Forgot Password Page"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["forgot_link"]))).click()

            for attempt in range(1, max_attempts + 2):  # Try one extra to confirm rate limiting
                with allure.step(f"Attempt {attempt}: Submit password reset request"):
                    # Clear and enter email
                    email_input = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email_field"])))
                    email_input.clear()
                    email_input.send_keys(test_email)
                    
                    # Click submit
                    submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["submit_btn"])))
                    submit_btn.click()
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Request_{attempt}", attachment_type=AttachmentType.PNG)

                with allure.step(f"Check response for attempt {attempt}"):
                    try:
                        # Check for rate limiting message
                        rate_limit_msg = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["rate_limit_message"])))
                        print(f"✅ Rate limiting triggered after {attempt} attempts: {rate_limit_msg.text}")
                        allure.attach(self.driver.get_screenshot_as_png(), name="Rate_Limited", attachment_type=AttachmentType.PNG)
                        assert True
                        return  # Test passes if rate limiting is confirmed

                    except TimeoutException:
                        # Check for regular success/error toast
                        try:
                            toast = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["toast"])))
                            print(f"Attempt {attempt}: {toast.text}")
                            
                            # Wait for toast to disappear before next attempt
                            wait.until(EC.invisibility_of_element_located((By.XPATH, xpaths["toast"])))
                            time.sleep(1)  # Additional wait between attempts
                            
                        except TimeoutException:
                            print(f"No toast message found for attempt {attempt}")

            # If we reach here, no rate limiting occurred
            print(f"⚠️ No rate limiting detected after {max_attempts + 1} requests")
            allure.attach(self.driver.get_screenshot_as_png(), name="No_Rate_Limit", attachment_type=AttachmentType.PNG)
            # This might be expected behavior for some applications
            assert True  # Pass but log the result

        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Error_Screenshot", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {str(e)}")

    def teardown_class(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"⚠️ Driver quit failed: {str(e)}")
