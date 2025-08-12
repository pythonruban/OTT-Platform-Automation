import time
import pytest 
import os
import sys 
import allure 

from conftest import *
from selenium.webdriver import ActionChains
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver

from utilities.readProp import ReadConfig

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

@pytest.mark.usefixtures("browser_setup")
class TestBulkOperations:
    driver = webdriver.Firefox

    # Locators
    email_element = "//div[contains(@class,'shadow border border-1 theme-border-color p-4 rounded-3 col-11 col-lg-6 col-xl-4 mx-auto')]//input[contains(@placeholder,'email')]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    
    # Slider management locators
    All_slider_element = "//a[span[text()='All Slider']]"
    
    # Bulk operation locators
    select_all_checkbox = "//input[@type='checkbox']"  # Common ID for select all
    slider_checkboxes = "//input[@type='checkbox']" # Common name for slider checkboxes
    bulk_delete_button = "//button[@id='deleteActionButton']" # Common ID for bulk delete
    confirm_delete_button = "//button[@id='adminButton']" # Common ID for confirm delete

    def login_and_navigate_to_slider_list(self):
        """Helper method to login and navigate to slider list page"""
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()
        
        try:
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
            time.sleep(2)
            
            # Navigate to All Slider
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            slider = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, self.All_slider_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slider)
            self.driver.execute_script("arguments[0].click();", slider)
            print("Navigated to 'All Slider Management'")
            time.sleep(3)
            
        except Exception as e:
            pytest.fail(f"Failed to login and navigate: {e}")

    def test_bulk_selection_and_deselection(self, browser_setup):
        """Test bulk selection and deselection of sliders"""
        self.driver = browser_setup
        self.login_and_navigate_to_slider_list()
        
        try:
            # Find all slider checkboxes
            checkboxes = self.driver.find_elements(By.XPATH, self.slider_checkboxes)
            if not checkboxes:
                pytest.fail("No slider checkboxes found on the page.")

            # Select the first two checkboxes
            for checkbox in checkboxes[:2]:
                checkbox.click()
                time.sleep(1)
                assert checkbox.is_selected(), "Checkbox was not selected."
            
            print(f"✓ Successfully selected {len(checkboxes[:2])} checkboxes.")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Bulk Selection", attachment_type=AttachmentType.PNG)

            # Deselect the first checkbox
            checkboxes[0].click()
            time.sleep(1)
            assert not checkboxes[0].is_selected(), "Checkbox was not deselected."
            print("✓ Successfully deselected a checkbox.")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Bulk Deselection", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Bulk Selection Failed", attachment_type=AttachmentType.PNG)
            pytest.fail(f"Bulk selection test failed: {e}")

    def test_select_all_functionality(self, browser_setup):
        """Test 'Select All' functionality"""
        self.driver = browser_setup
        self.login_and_navigate_to_slider_list()
        
        try:
            # Find and click the 'Select All' checkbox
            select_all = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.select_all_checkbox)))
            select_all.click()
            time.sleep(2)

            # Verify all checkboxes are selected
            checkboxes = self.driver.find_elements(By.XPATH, self.slider_checkboxes)
            for checkbox in checkboxes:
                assert checkbox.is_selected(), "Not all checkboxes were selected."
            
            print("✓ 'Select All' functionality works as expected.")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Select All", attachment_type=AttachmentType.PNG)

            # Uncheck 'Select All'
            select_all.click()
            time.sleep(2)

            # Verify all checkboxes are deselected
            for checkbox in checkboxes:
                assert not checkbox.is_selected(), "Not all checkboxes were deselected."

            print("✓ 'Deselect All' functionality works as expected.")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Deselect All", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Select All Failed", attachment_type=AttachmentType.PNG)
            pytest.fail(f"'Select All' test failed: {e}")

    def test_bulk_delete_functionality(self, browser_setup):
        """Test bulk delete functionality"""
        self.driver = browser_setup
        self.login_and_navigate_to_slider_list()
        
        try:
            # Select the first two sliders for deletion
            checkboxes = self.driver.find_elements(By.XPATH, self.slider_checkboxes)
            if len(checkboxes) < 2:
                pytest.skip("Not enough sliders to perform bulk delete.")

            for checkbox in checkboxes[:2]:
                checkbox.click()

            initial_slider_count = len(checkboxes)
            print(f"Initial slider count: {initial_slider_count}")

            # Click the bulk delete button
            bulk_delete = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.bulk_delete_button)))
            bulk_delete.click()
            time.sleep(2)

            # Confirm deletion
            confirm_delete = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.confirm_delete_button)))
            confirm_delete.click()
            time.sleep(10)

            # Verify sliders are deleted
            remaining_checkboxes = self.driver.find_elements(By.XPATH, self.slider_checkboxes)
            assert len(remaining_checkboxes) == initial_slider_count - 2, "Bulk delete failed."

            print("✓ Bulk delete functionality works as expected.")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Bulk Delete Success", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Bulk Delete Failed", attachment_type=AttachmentType.PNG)
            pytest.fail(f"Bulk delete test failed: {e}")

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")
