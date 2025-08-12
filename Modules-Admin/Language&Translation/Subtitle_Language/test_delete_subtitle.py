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
    subtitle_element ="//span[text()='Subtitle Languages']"
    edit_subtitle_element = "(//span[@class='editdropdown-button'])[1]"
    delete_subtitle_element ="(//span[text()='Delete'])[1]"
    confrim_delete_element= "(//button[text()='Delete'])[1]"

  
    
    def test_delete_subtitle(self,browser_setup):
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
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All required data was entered and login was successful", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="login_error", attachment_type=AttachmentType.PNG)
            print(f" Failed to enter email: {e}")
 
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            Manage_app = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.Manage_language_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Manage_app)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", Manage_app)
            print("Clicked 'Language'")
            time.sleep(6)
        except Exception as e:
            print(f"Error clicking 'Language': {e}")

        # Click Subtitle tab
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.subtitle_element))
            ).click()
            time.sleep(2)
        except Exception as e:
            print(f"Error clicking Subtitle tab: {e}")

                    # ====== EDIT ELEMENT ======
        try:
            edit = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.edit_subtitle_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit)
            time.sleep(3)
            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.edit_subtitle_element)
            actions.move_to_element(element_to_hover).perform()
            time.sleep(2)
        
        except Exception as e:
            print(f"Failed to locate or scroll to the edit subtitle element: {e}")
            

        

        # ====== CLICK DELETE SUBTITLE ELEMENT ======
        try:
            delete_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.delete_subtitle_element))
            )
            delete_button.click()
            print("Edit element and menu interaction succeeded.")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name=" The specific live video was successfully deleted from the All Live page.", attachment_type=AttachmentType.PNG)
            time.sleep(5)
          
            
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name=" The specific live video was successfully deleted from the All Live page.", attachment_type=AttachmentType.PNG)
            print(f"Failed to click the delete subtitle element: {e}")
            raise

                

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
