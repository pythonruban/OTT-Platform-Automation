import pytest
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Load URL from config

# Centralized XPaths dictionary
xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "login_success_toast": "//div[@role='alert']"
}

@allure.feature("Login Flow - Success Toast Validation")
class TestLoginValid:

    def test_valid_login(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()  # ✅ Load from config.ini

        try:
            with allure.step("Step 1: Open website and click login icon"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Icon", attachment_type=AttachmentType.PNG)

            with allure.step("Step 2: Enter valid credentials"):
                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys("admin@admin.com")
                self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("Webnexs123!@#")
                allure.attach(self.driver.get_screenshot_as_png(), name="Entered_Valid_Credentials", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Submit login"):
                self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Login_Button", attachment_type=AttachmentType.PNG)

            with allure.step("Step 4: Validate success toast appears"):
                wait.until(EC.text_to_be_present_in_element((By.XPATH, xpaths["login_success_toast"]), "Login successful"))
                toast = self.driver.find_element(By.XPATH, xpaths["login_success_toast"])
                allure.attach(self.driver.get_screenshot_as_png(), name="Login_Success_Toast", attachment_type=AttachmentType.PNG)
                print("✅ Login successful toast appeared:", toast.text)
                assert "login successful" in toast.text.lower()

            time.sleep(2)

        except Exception as e:
            print("❌ Login failed:", str(e))
            allure.attach(self.driver.get_screenshot_as_png(), name="Error_Screenshot", attachment_type=AttachmentType.PNG)
            assert False, str(e)

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("⚠️ Driver was not initialized.")
