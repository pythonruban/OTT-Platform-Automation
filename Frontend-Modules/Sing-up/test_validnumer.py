import pytest
import allure
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Use config URL

# Define all XPaths
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

class TestSignupFlow:

    @allure.title("Signup Flow - Guest to PPV")
    @allure.description("Captures Allure screenshots from start to finish, including on failures.")
    def test_guest_to_ppv_flow(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()  # ✅ Use from config

        try:
            with allure.step("Open signup page"):
                self.driver.get(base_url)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["signup_button"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Signup_Page_Opened", attachment_type=AttachmentType.PNG)
                time.sleep(3)
            with allure.step("Fill personal details"):
                self.driver.find_element(By.XPATH, xpaths["first_name"]).send_keys("Ruban")
                self.driver.find_element(By.XPATH, xpaths["last_name"]).send_keys("Test")
                email = f"ruban{random.randint(1000, 9999)}@webnexs.in"
                self.driver.find_element(By.XPATH, xpaths["email"]).send_keys(email)
                allure.attach(self.driver.get_screenshot_as_png(), name="Personal_Info_Entered", attachment_type=AttachmentType.PNG)
                time.sleep(3)
            with allure.step("Select mobile country and enter number"):
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["country_dropdown"]))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["india_option"]))).click()
                phone = f"98765{random.randint(10000,99999)}"
                self.driver.find_element(By.XPATH, xpaths["mobile"]).send_keys(phone)
                allure.attach(self.driver.get_screenshot_as_png(), name="Mobile_Selected_And_Entered", attachment_type=AttachmentType.PNG)
                time.sleep(3)
            with allure.step("Fill remaining signup fields"):
                
                self.driver.find_element(By.XPATH, xpaths["gender"]).send_keys("Male")
                self.driver.find_element(By.XPATH, xpaths["country"]).send_keys("India")
                self.driver.find_element(By.XPATH, xpaths["state"]).send_keys("Tamil Nadu")
                self.driver.find_element(By.XPATH, xpaths["city"]).send_keys("Chennai")
                self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("Test@123")
                self.driver.find_element(By.XPATH, xpaths["confirm_password"]).send_keys("Test@123")
                allure.attach(self.driver.get_screenshot_as_png(), name="All_Fields_Filled", attachment_type=AttachmentType.PNG)
                time.sleep(3)
            with allure.step("Accept terms and submit form"):
                self.driver.find_element(By.XPATH, xpaths["accept_terms"]).click()
                self.driver.find_element(By.XPATH, xpaths["submit"]).click()

            with allure.step("Verify signup success"):
                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["success_toast"])))
                allure.attach(self.driver.get_screenshot_as_png(), name="Signup_Success", attachment_type=AttachmentType.PNG)
                print(f"✅ Signup successful with email: {email}")
                assert True

        except Exception as e:
            with allure.step("Signup failed - capturing error screenshot"):
                allure.attach(self.driver.get_screenshot_as_png(), name="Signup_Failed", attachment_type=AttachmentType.PNG)
                print(f"❌ Signup failed: {str(e)}")
            assert False, f"Test failed: {str(e)}"

        finally:
            self.driver.quit()

    def teardown_class(self):
        try:
            self.driver.quit()
        except AttributeError:
            print("⚠️ Driver was not initialized.")
