import time
import re 
import random
import string
import pytest 
import os
import sys 
import allure 


 
from conftest import *
from selenium.webdriver import ActionChains, Keys
from allure_commons.types import AttachmentType
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from utilities.readProp import ReadConfig


@pytest.mark.usefixtures("browser_setup") 
class TestLiveStream:
    driver = webdriver.Firefox    
    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    live_stream_element = "//div[@data-bs-target='#Live-Stream']"
    add_live_category_element = "//span[contains(text(), 'Manage Live Stream Categories')]"
    delete_element ="(//span[contains(@class, 'editdropdown-button')])[6]"
    delete_menu = "(//span[text()='Delete'])[6]"
    confrim_delete = "(//button[span[text()='Delete']])[1]"

    def test_delete_category(self,browser_setup):
        self.driver = browser_setup
        """Navigate and delete live stream """
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()
        actions = ActionChains(self.driver)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.email_element))
            ).send_keys(ReadConfig.getAdminId())

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.password_element))
            ).send_keys(ReadConfig.getPassword())

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.login_element))
            ).click()

            print(" Login Successful!")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name=" login Credentials was entered, and the login button was clicked. it was redirect to Dashboard", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="login_error", attachment_type=AttachmentType.PNG)
            print(f" Failed to enter email: {e}")

        
            # Scroll to ensure all elements are loaded
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            Manage_livestream = WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, self.live_stream_element))
             )
            self.driver.execute_script("arguments[0].click();", Manage_livestream)
            print(" Navigated to 'Live Stream Management'")
        except Exception as e:
            print(f" Failed to click 'Live Stream Management': {e}")

    
            # Wait for "Add New Member" button and click
        try:
            add_livestream_button = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.add_live_category_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_livestream_button)
            time.sleep(1)  # Allow smooth scrolling
            self.driver.execute_script("arguments[0].click();", add_livestream_button)
            print(" Clicked 'Add New Live Stream'")
            time.sleep(6)
        except Exception as e:
            print(f" Failed to click 'Add New Live Stream': {e}")

            #edit element
        try:
            delete=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.delete_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", delete)
            time.sleep(2)
            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.delete_element)
            actions.move_to_element(element_to_hover).perform()
            time.sleep(2)
            # Edit menu
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.delete_menu))
            ).click()
            time.sleep(6)
        except Exception as e:
             print(f" An error occurred while performing the edit action: {e}")
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.confrim_delete))
            ).click()
            print("Live Stream was deleted successfully")
            time.sleep(3)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name=" In all, the Manage Category page The Particular  Category was deleted successfully", attachment_type=AttachmentType.PNG)
            time.sleep(6)

        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Unexpected Error", attachment_type=AttachmentType.PNG)
           
    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")


