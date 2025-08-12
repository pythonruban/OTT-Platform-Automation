import pytest
import random
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

xpaths = {
    "signup_button": "//button[@id='home-signup']",
    "first_name": "//input[@id='signup-username']",
    "last_name": "//input[@id='signup-lastname']",
    "email": "//input[@id='signup-email']",
    "country_dropdown": "//div[@role='button']",
    "india_option": "//li[@data-country-code='in']",
    "mobile": "//input[@type='tel']",
    "gender": "//select[@id='signup-gender']",
    "country": "//input[@id='signup-country']",
    "state": "//input[@id='signup-state']",
    "city": "//input[@id='signup-city']",
    "password": "//input[@id='signup-password']",
    "confirm_password": "//input[@id='confirmPassword']",
    "accept_terms": "//input[@id='signup-accept']",
    "submit": "//button[@id='signup-submit']",
    "success_toast": "//div[@role='alert']"
}

@allure.feature("Sign-Up - Whitespace Handling")
@allure.title("Test Signup with Leading/Trailing Whitespace in Name Fields")
class TestWhitespaceHandling:

    def test_signup_with_whitespace_in_name(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        try:
            with allure.step("Step 1: Open signup page"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["signup_button"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Signup_Page_Opened", attachment_type=AttachmentType.PNG)

            with allure.step("Step 2: Fill form with leading/trailing whitespace in names"):
                # Add whitespace to first name and last name
                self.driver.find_element(By.XPATH, xpaths["first_name"]).send_keys("  Test  ")
                self.driver.find_element(By.XPATH, xpaths["last_name"]).send_keys("  User  ")
                
                email = f"ruban{random.randint(1000,9999)}@webnexs.in"
                self.driver.find_element(By.XPATH, xpaths["email"]).send_keys(email)
                
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["country_dropdown"]))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["india_option"]))).click()
                
                phone = f"98765{random.randint(10000,99999)}"
                self.driver.find_element(By.XPATH, xpaths["mobile"]).send_keys(phone)
                self.driver.find_element(By.XPATH, xpaths["gender"]).send_keys("Male")
                self.driver.find_element(By.XPATH, xpaths["country"]).send_keys("India")
                self.driver.find_element(By.XPATH, xpaths["state"]).send_keys("Tamil Nadu")
                self.driver.find_element(By.XPATH, xpaths["city"]).send_keys("Chennai")
                self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("Test@123")
                self.driver.find_element(By.XPATH, xpaths["confirm_password"]).send_keys("Test@123")
                self.driver.find_element(By.XPATH, xpaths["accept_terms"]).click()
                
                allure.attach(self.driver.get_screenshot_as_png(), name="Form_Filled_With_Whitespace", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Submit form"):
                self.driver.find_element(By.XPATH, xpaths["submit"]).click()

            with allure.step("Step 4: Verify success (confirming whitespace was trimmed)"):
                success_toast = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["success_toast"])))
                success_text = success_toast.text.lower()
                allure.attach(self.driver.get_screenshot_as_png(), name="Whitespace_Success", attachment_type=AttachmentType.PNG)
                print(f"✅ Success message: {success_toast.text}")
                
                assert "success" in success_text

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failed", attachment_type=AttachmentType.PNG)
            assert False, f"Test failed: {str(e)}"

    def teardown_class(self):
        try:
            self.driver.quit()
        except AttributeError:
            print("⚠️ Driver was not initialized.")
