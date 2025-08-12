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
    "error_toast": "//div[@role='alert']"
}

@pytest.mark.parametrize("invalid_phone", ["123", "abcdefghij", "987654321012345", "12345-6789"])
@allure.feature("Sign-Up - Phone Validation")  
@allure.title("Test Signup with Invalid Phone Numbers")
def test_signup_with_invalid_phone_number(browser_setup, invalid_phone):
    driver = browser_setup
    wait = WebDriverWait(driver, 30)
    base_url = ReadConfig.getHomePageURL()
    try:
        with allure.step(f"Open signup page and fill with invalid phone '{invalid_phone}'"):
            driver.get(base_url)
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["signup_button"]))).click()
            driver.find_element(By.XPATH, xpaths["first_name"]).send_keys("Test")
            driver.find_element(By.XPATH, xpaths["last_name"]).send_keys("User")
            email = f"ruban{random.randint(1000,9999)}@webnexs.in"
            driver.find_element(By.XPATH, xpaths["email"]).send_keys(email)
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["country_dropdown"]))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["india_option"]))).click()
            driver.find_element(By.XPATH, xpaths["mobile"]).send_keys(invalid_phone)
            driver.find_element(By.XPATH, xpaths["gender"]).send_keys("Male")
            driver.find_element(By.XPATH, xpaths["country"]).send_keys("India")
            driver.find_element(By.XPATH, xpaths["state"]).send_keys("Tamil Nadu")
            driver.find_element(By.XPATH, xpaths["city"]).send_keys("Chennai")
            driver.find_element(By.XPATH, xpaths["password"]).send_keys("Test@123")
            driver.find_element(By.XPATH, xpaths["confirm_password"]).send_keys("Test@123")
            driver.find_element(By.XPATH, xpaths["accept_terms"]).click()

        with allure.step("Submit form and check error"):
            driver.find_element(By.XPATH, xpaths["submit"]).click()
            error_toast = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["error_toast"])))
            error_text = error_toast.text.lower()
            allure.attach(driver.get_screenshot_as_png(), name="Invalid_Phone_Error", attachment_type=AttachmentType.PNG)
            assert ("mobile" in error_text or "phone" in error_text or "invalid" in error_text or "number" in error_text)
    finally:
        driver.quit()
