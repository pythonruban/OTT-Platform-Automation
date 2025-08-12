import time
import pytest
import os
import allure
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

@pytest.mark.usefixtures("browser_setup")
class TestViewCategories:

    driver: webdriver
    allure_report_error_message = ""

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    live_stream_element = "//div[@data-bs-target='#Live-Stream']"
    manage_live_category_element = "//span[contains(text(), 'Manage Live Stream Categories')]"
    category_list_table = "//table[@id='your_category_table_id']" # Please update with the actual table ID/XPath
    pagination_element = "//div[@class='your_pagination_class']" # Please update with the actual pagination element
    sort_by_name_asc = "//th[@data-sort='name_asc']" # Example for sorting
    filter_input = "//input[@id='your_filter_input_id']" # Example for filtering

    def test_view_category_list(self, browser_setup):
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

            # Verify Category List is displayed
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.category_list_table))
            )
            print("Category list table is visible.")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Category_List_View", attachment_type=AttachmentType.PNG)

            # TODO: Add assertions to check for number of rows, specific categories, etc.

        except Exception as e:
            self.allure_report_error_message = f"Error viewing category list: {e}"
            allure.attach(self.driver.get_screenshot_as_png(), name="View_Category_Error", attachment_type=AttachmentType.PNG)
            print(self.allure_report_error_message)

    # TODO: Add more tests for pagination, sorting, and filtering

    def teardown_method(self):
        """Close the browser"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

