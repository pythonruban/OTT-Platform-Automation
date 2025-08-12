import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

@pytest.mark.usefixtures("browser_setup")
class TestEnableDisableCategory:

    driver: webdriver
    allure_report_error_message = ""

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    live_stream_element = "//div[@data-bs-target='#Live-Stream']"
    manage_live_category_element = "//span[contains(text(), 'Manage Live Stream Categories')]"
    
    # Enable/Disable toggle locators (update with actual locators)
    enable_disable_toggle_element = "(//span[contains(@class, 'toggle-switch')])[1]"  # Update with actual toggle locator
    category_status_element = "(//td[contains(@class, 'status')])[1]"  # Update with actual status cell locator
    category_name_element = "(//td[contains(@class, 'category-name')])[1]"  # Update with actual category name locator

    def test_enable_disable_category_toggle(self, browser_setup):
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

        # Navigate to Manage Livestream Categories
        try:
            manage_livestream = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.live_stream_element))
            )
            self.driver.execute_script("arguments[0].click();", manage_livestream)
            print("Navigated to 'Live Stream Management'")

            manage_category_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.manage_live_category_element))
            )
            self.driver.execute_script("arguments[0].click();", manage_category_button)
            print("Clicked 'Manage Live Stream Categories'")
            time.sleep(3)

            # Get the current category name for reference
            category_name = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.category_name_element))
            ).text
            print(f"Testing category: {category_name}")

            # Get initial status
            initial_status = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.category_status_element))
            ).text
            print(f"Initial status: {initial_status}")

            # Click the enable/disable toggle
            toggle_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.enable_disable_toggle_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle_element)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", toggle_element)
            time.sleep(2)
            print("Clicked enable/disable toggle")

            # Verify status changed
            updated_status = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.category_status_element))
            ).text
            print(f"Updated status: {updated_status}")

            # Assert that status has changed
            assert initial_status != updated_status, f"Status should have changed from {initial_status} to {updated_status}"
            
            allure.attach(self.driver.get_full_page_screenshot_as_png(), 
                         name=f"Category_Status_Changed_From_{initial_status}_To_{updated_status}", 
                         attachment_type=AttachmentType.PNG)

            # Toggle back to original state
            self.driver.execute_script("arguments[0].click();", toggle_element)
            time.sleep(2)
            print("Toggled back to original state")

            # Verify status is back to original
            final_status = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.category_status_element))
            ).text
            print(f"Final status: {final_status}")

            assert initial_status == final_status, f"Status should be back to original: {initial_status}"
            
            allure.attach(self.driver.get_full_page_screenshot_as_png(), 
                         name=f"Category_Status_Restored_To_{final_status}", 
                         attachment_type=AttachmentType.PNG)

            print("Enable/Disable toggle test completed successfully!")

        except Exception as e:
            self.allure_report_error_message = f"Error during enable/disable toggle test: {e}"
            allure.attach(self.driver.get_screenshot_as_png(), name="Enable_Disable_Toggle_Error", attachment_type=AttachmentType.PNG)
            print(self.allure_report_error_message)
            raise

    def teardown_method(self):
        """Close the browser"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
