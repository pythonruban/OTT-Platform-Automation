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
    "login_success_toast": "//div[@role='alert']"
}

@allure.feature("Login Flow - Whitespace Handling")
class TestWhitespaceHandling:

    @pytest.mark.parametrize("email, password", [
        ("  admin@admin.com", "Webnexs123!@#"),  # Leading space in email
        ("admin@admin.com  ", "Webnexs123!@#"),  # Trailing space in email
        ("admin@admin.com", "  Webnexs123!@#"), # Leading space in password
        ("admin@admin.com", "Webnexs123!@#  ")  # Trailing space in password
    ])
    def test_whitespace_trimming(self, browser_setup, email, password):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        try:
            with allure.step("Step 1: Open site and click login icon"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Icon", attachment_type=AttachmentType.PNG)

            with allure.step(f"Step 2: Enter credentials with whitespace - Email: '{email}', Password: '{password}'"):
                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(email)
                self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(password)
                allure.attach(self.driver.get_screenshot_as_png(), name="Entered_Whitespace_Credentials", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Click Login button"):
                self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Button", attachment_type=AttachmentType.PNG)

            with allure.step("Step 4: Validate success toast appears, confirming whitespace was trimmed"):
                wait.until(EC.text_to_be_present_in_element((By.XPATH, xpaths["login_success_toast"]), "Login successful"))
                toast = self.driver.find_element(By.XPATH, xpaths["login_success_toast"])
                allure.attach(self.driver.get_screenshot_as_png(), name="Login_Success_Toast_Whitespace", attachment_type=AttachmentType.PNG)
                print(f"✅ Login successful with whitespace. Toast: {toast.text}")
                assert "login successful" in toast.text.lower()

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
