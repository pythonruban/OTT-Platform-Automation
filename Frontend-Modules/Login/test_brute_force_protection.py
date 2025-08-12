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
    "toast_error": "//div[contains(@class,'Toastify__toast--error')]",
    "lockout_message": "//div[contains(text(),'Too many attempts') or contains(text(),'locked') or contains(text(),'blocked')]"
}

@allure.feature("Login Flow - Brute Force Protection")
class TestBruteForceProtection:

    def test_multiple_failed_attempts(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 10) # Shorter wait for faster failures
        base_url = ReadConfig.getHomePageURL()
        max_attempts = 5  # Adjust based on your application's limit

        try:
            with allure.step("Step 1: Open site and click login icon"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Icon", attachment_type=AttachmentType.PNG)

            for attempt in range(1, max_attempts + 2): # Try one more time to confirm lockout
                with allure.step(f"Step {attempt + 1}: Attempt {attempt} - Enter invalid credentials"):
                    email_field = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email"])))
                    password_field = self.driver.find_element(By.XPATH, xpaths["password"])
                    
                    # Use a context manager to handle stale elements gracefully
                    try:
                        email_field.clear()
                        email_field.send_keys("brute_force_test@example.com")
                        password_field.clear()
                        password_field.send_keys(f"invalidPassword{attempt}")
                    except Exception as e:
                        print(f"Could not clear or send keys on attempt {attempt}: {e}")
                        # Refresh and try again if elements are stale
                        self.driver.refresh()
                        wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                        continue

                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Attempt_{attempt}_Credentials", attachment_type=AttachmentType.PNG)
                    self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()

                try:
                    # Check for a lockout message
                    lockout_msg = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["lockout_message"])))
                    print(f"✅ Account locked after {attempt} attempts. Message: {lockout_msg.text}")
                    allure.attach(self.driver.get_screenshot_as_png(), name="Account_Locked", attachment_type=AttachmentType.PNG)
                    assert True
                    return # Test passes if lockout is confirmed

                except Exception:
                    # If not locked, check for a standard error toast
                    try:
                        error_toast = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["toast_error"])))
                        print(f"Attempt {attempt} failed as expected. Error: {error_toast.text}")
                        # Wait for toast to disappear
                        wait.until(EC.invisibility_of_element_located((By.XPATH, xpaths["toast_error"])))
                    except Exception:
                        print(f"No error toast or lockout message on attempt {attempt}.")
            
            # If the loop completes without a lockout
            allure.attach(self.driver.get_screenshot_as_png(), name="No_Lockout", attachment_type=AttachmentType.PNG)
            pytest.fail(f"Account was not locked after {max_attempts} failed login attempts.")

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Error_Screenshot", attachment_type=AttachmentType.PNG)
            pytest.fail(f"An exception occurred: {e}")

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("⚠️ Driver was not initialized.")

