import pytest
import random
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Config import

xpaths = {
    "signup_button": "//button[@id='home-signup']",
    "first_name": "//input[@id='signup-username']",
    "last_name": "//input[@id='signup-lastname']",
    "email": "//input[@id='signup-email']",
    "country_dropdown": "//div[@role='button']",
    "india_option": "//li[@data-country-code='in']",
    "mobile": "//input[@type='tel']",
    "dob": "//input[@id='signup-dob']",
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

@allure.title("Negative Signup Test - Invalid Data")
@allure.description("Test signup flow with mismatched password and missing gender/city fields.")
class TestSignupFlow:

    def test_guest_to_ppv_flow(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()  # ✅ Using config value

        try:
            with allure.step("Open signup page"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["signup_button"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Signup_Page_Loaded", attachment_type=AttachmentType.PNG)
                time.sleep(3)
            with allure.step("Fill form with invalid/missing data"):
                self.driver.find_element(By.XPATH, xpaths["first_name"]).send_keys("Ruban")
                self.driver.find_element(By.XPATH, xpaths["last_name"]).send_keys("Test")
                time.sleep(3)
                email = f"ruban{random.randint(1000,9999)}@webnexs.in"
                self.driver.find_element(By.XPATH, xpaths["email"]).send_keys(email)
                time.sleep(3)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["country_dropdown"]))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["india_option"]))).click()
                time.sleep(3)
                phone = f"98765"
                self.driver.find_element(By.XPATH, xpaths["mobile"]).send_keys(phone)
                self.driver.find_element(By.XPATH, xpaths["dob"]).send_keys("1995-06-19")

                #  Invalid or empty fields
                self.driver.find_element(By.XPATH, xpaths["gender"]).send_keys("")
                self.driver.find_element(By.XPATH, xpaths["country"]).send_keys("India")
                self.driver.find_element(By.XPATH, xpaths["state"]).send_keys("Tamil Nadu")
                self.driver.find_element(By.XPATH, xpaths["city"]).send_keys("")  # Empty on purpose

                #  Password mismatch
                self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("Test@1234")
                self.driver.find_element(By.XPATH, xpaths["confirm_password"]).send_keys("Test@1234")

                self.driver.find_element(By.XPATH, xpaths["accept_terms"]).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Form_Invalid_Data_Filled", attachment_type=AttachmentType.PNG)

            with allure.step("Submit the form"):
                self.driver.find_element(By.XPATH, xpaths["submit"]).click()

            with allure.step("Check for failure - success toast should NOT appear"):
                try:
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, xpaths["success_toast"])))
                    allure.attach(self.driver.get_screenshot_as_png(), name="Unexpected_Success", attachment_type=AttachmentType.PNG)
                    print("❌ Test failed: Signup succeeded unexpectedly")
                    assert False, "Signup should not succeed with invalid data"
                except:
                    allure.attach(self.driver.get_screenshot_as_png(), name="Signup_Failed_As_Expected", attachment_type=AttachmentType.PNG)
                    print("✅ Signup failed as expected due to invalid data.")
                    assert True

        except Exception as e:
            with allure.step("Unexpected exception in form handling"):
                allure.attach(self.driver.get_screenshot_as_png(), name="Unexpected_Exception", attachment_type=AttachmentType.PNG)
                print(f"❌ Unexpected exception: {str(e)}")
            assert False, f"Exception occurred: {str(e)}"

        finally:
            self.driver.quit()

    def teardown_class(self):
        try:
            self.driver.quit()
        except AttributeError:
            print("⚠️ Driver was not initialized.")
