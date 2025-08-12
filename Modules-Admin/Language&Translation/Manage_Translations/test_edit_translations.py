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
    translate_element ="//span[text()='Manage Translations']"
   
    en_name_element = "(//td[contains(@class, 'theme-bg-color') and contains(@class, 'theme-text-color')])[8]"
    english_element = "//td[contains(@class, 'position-relative')]//input[@name='value']"
    save_btn ="(//button[@class='bg-transparent'])[1]"
    
    tr_name_element = "(//td[contains(@class, 'theme-bg-color') and contains(@class, 'theme-text-color')])[9]"
    turkeish_name_element ="//td[contains(@class, 'position-relative')]//input[@name='value']" 
    save_btn2 ="(//button[@class='bg-transparent'])[1]"
    
  
    
    def test_add_Translation(self,browser_setup):
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
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All Value login Credentials was entered, and the login button was clicked. it was redirect to Dashboard", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="login_error", attachment_type=AttachmentType.PNG)
            print(f" Failed to enter email: {e}")
            

        
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
            # Wait until the element is present in the DOM
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.translate_element))
            )
            # Attempt to click the element
            element.click()
            time.sleep(2)
            print("Element clicked successfully.")

        except Exception as e:
            print(f"An unexpected exception occurred: {e}")

        try:
            # Generate a random uppercase string of length between 5 and 7
            length = random.randint(5, 9)
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")

            print(f"Using XPath: {self.en_name_element}")

            # Wait for the title input to be clickable
            Lang = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.en_name_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Lang)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", Lang)
            name= self.driver.find_element(By.XPATH, self.english_element)
            time.sleep(2)
            name.clear()
            time.sleep(2)  # small delay to ensure field is cleared
            name.send_keys(auto_name)
            time.sleep(2)
            print(" Auto name entered in the title field.")
            self.driver.find_element(By.XPATH, self.save_btn).click()
            time.sleep(2)

        except Exception as e:
            print(f" Failed to enter title: {e}")   

            
        try:
            # Generate a random uppercase string of length between 5 and 7
            length = random.randint(4, 9)
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")

            print(f"Using XPath: {self.tr_name_element}")

            # Wait for the title input to be clickable
            value = WebDriverWait(self.driver, 130).until(
                EC.element_to_be_clickable((By.XPATH, self.tr_name_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", value)
            time.sleep(2)
            value.click()
            time.sleep(2)
            value2 = self.driver.find_element(By .XPATH , self.turkeish_name_element)
            time.sleep(2)
            value2.clear()
            time.sleep(2)  # small delay to ensure field is cleared
            value2.send_keys(auto_name)
            time.sleep(2)
            print(" Auto name entered in the title field.")
            self.driver.find_element(By.XPATH, self.save_btn2).click()
            time.sleep(4)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Manage Translation Key And Value was Edited Successfully", attachment_type=AttachmentType.PNG)

        except Exception as e:
            print(f" Failed to enter title: {e}") 

    
    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
