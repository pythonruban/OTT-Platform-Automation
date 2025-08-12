import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

@pytest.mark.usefixtures("browser_setup")
class TestValidationCategories:

    driver: webdriver
    allure_report_error_message = ""

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    live_stream_element = "//div[@data-bs-target='#Live-Stream']"
    add_live_category_element = "//span[contains(text(), 'Manage Live Stream Categories')]"
    add_new_category = "//a[@id= 'navigationLinkForAddPage']"
    submit_button_element = "(//span[text()='Submit'])[2]"
    name_error_message_element = "//span[contains(text(), 'Title cannot be empty')]" # Update with actual error message locator
    slug_error_message_element = "//span[contains(text(), 'Slug cannot be empty')]" # Update with actual error message locator

    def test_category_form_validation(self, browser_setup):
        self.driver = browser_setup
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()

        # Login
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.email_element))
        ).send_keys(ReadConfig.getAdminId())

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.password_element))
        ).send_keys(ReadConfig.getPassword())

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.login_element))
        ).click()
        print("Login Successful!")
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login_Success", attachment_type=AttachmentType.PNG)

        # Navigate to Add New Category page
        try:
            manage_livestream = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.live_stream_element))
            )
            self.driver.execute_script("arguments[0].click();", manage_livestream)

            add_livestream_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.add_live_category_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_livestream_button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", add_livestream_button)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.add_new_category))
            ).click()
            print("Navigated to Add New Category page")
            time.sleep(3)

            # Submit form with empty fields
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
             )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", submit_button)
            print("Clicked submit with empty fields")
            time.sleep(2)

            # Verify validation messages
            name_error = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.name_error_message_element))
            ).text
            assert "Name is required" in name_error

            slug_error = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.slug_error_message_element))
            ).text
            assert "Slug is required" in slug_error

            print("Validation messages appeared as expected.")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Validation_Error_Messages", attachment_type=AttachmentType.PNG)

        except Exception as e:
            self.allure_report_error_message = f"Error during form validation test: {e}"
            allure.attach(self.driver.get_screenshot_as_png(), name="Validation_Test_Error", attachment_type=AttachmentType.PNG)
            print(self.allure_report_error_message)


    def teardown_method(self):
        """Close the browser"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()