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
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from utilities.readProp import ReadConfig

# Add the project root (D:\Automation\) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))



@pytest.mark.usefixtures("browser_setup")

class TestLanguage:
    driver = webdriver.Firefox

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
   
    Manage_language_element = "//span[text()='Manage Language']"
    translate_element ="//span[text()='Manage Translate Languages']"
    edit_element ="(//span[contains(@class, 'editdropdown-button')])[2]"#xpath
    delete_menu = "(//div[@class='editdropdown-menu']//div[contains(@class, 'commonActionPadding')]//span[normalize-space(text())='Delete'])[2]"  
    delete_language_button_element= "//button[span[text()='Delete']]"


    
    def test_delete_translate(self,browser_setup):
        self.driver = browser_setup
        """Login to the admin panel"""
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()

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
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name=" All required data was entered and login was successful", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="login_error", attachment_type=AttachmentType.PNG)
            print(f" Failed to enter email: {e}")
            
        # Locate and click 'Manage Language'
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(" Scrolled to bottom of page")
            Manage_app = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.Manage_language_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Manage_app)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", Manage_app)
            print(" Clicked 'Language'")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to click 'Language': {e}")

        try:
            translate_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.translate_element))
            )
            translate_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Failed to click 'Translate': {e}")
        

        try:
            # ====== EDIT ELEMENT ======
            edit = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit)
            time.sleep(3)

            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.edit_element)
            actions.move_to_element(element_to_hover).perform()
            time.sleep(2)
            # ====== EDIT MENU ======
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.delete_menu))
            ).click()
            time.sleep(6)

            print(" delete element and menu interaction succeeded.")
        
        except Exception as e:
            print(f" Failed to interact with edit element or menu: {e}")  

        try:
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.delete_language_button_element))
            ).click()
            print("Language Was Edited Successfully")
            time.sleep(5)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="the Added Translation was Deleted Successfully", attachment_type=AttachmentType.PNG)
            time.sleep(2)
        except Exception as e:
            error_msg = f"Error while confirming delete: {e}"
            print(error_msg)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="delete eas not happening it was an Error", attachment_type=AttachmentType.PNG)
            
        
    
    

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 
    