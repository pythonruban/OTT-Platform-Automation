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
    # driver = webdriver.Firefox

    

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
   
    Manage_language_element = "//span[text()='Manage Language']"
    Subtitle_element ="//span[text()='Subtitle Languages']"
    edit1_Subtitle_element = "(//span[@class='editdropdown-button'])[1]"
    edit_Subtile_element ="(//span[contains(text(), 'Edit')])[1]"
    subtitle_name_element = "//input[@name='name']"
    short_code_element ="//input[@name='short_code']"
    update_subtitle_element= "//button[@id='adminButton']"
    

    
    
    def test_edit_subtitle(self,browser_setup):
        self.driver = browser_setup
        """Login to the admin panel"""
        # self.driver.get(ReadConfig.getAdminPageURL())
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
            # allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All required data was entered and login was successful", attachment_type=AttachmentType.PNG)

        except Exception as e:
            # allure.attach(self.driver.get_full_page_screenshot_as_png(), name="login_error", attachment_type=AttachmentType.PNG)
            print(f" Failed to enter email: {e}")
 

        # Click on 'Language' under Manage
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
                EC.presence_of_element_located((By.XPATH, self.Subtitle_element))
            ).click()
            time.sleep(2)
        except Exception as e:
            print(f"Error clicking Subtitle tab: {e}")

        try:
            # ====== EDIT ELEMENT ======
            edit = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.edit1_Subtitle_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit)
            time.sleep(3)

            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.edit1_Subtitle_element)
            actions.move_to_element(element_to_hover).perform()
            time.sleep(2)

            # ====== EDIT MENU ======
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.edit_Subtile_element))
            ).click()
            time.sleep(6)

            print(" Edit element and menu interaction succeeded.")
        
        except Exception as e:
            print(f" Failed to interact with edit element or menu: {e}")

        try:
            # Generate a random uppercase string of length between 5 and 7
            length = random.randint(5, 7)
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")

            print(f"Using XPath: {self.subtitle_name_element}")

            # Wait for the title input to be clickable
            name = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.subtitle_name_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
            time.sleep(2)
            name.clear()
            time.sleep(2)  # small delay to ensure field is cleared
            name.send_keys(auto_name)
            time.sleep(2)
            print(" Auto name entered in the title field.")

        except Exception as e:
            print(f" Failed to enter title: {e}")
        # Enter Slug
        try:
            print(f"Using XPath for slug input: {self.short_code_element}")

            slug = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.short_code_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slug)
            time.sleep(2)
            slug.clear()
            time.sleep(2)
            slug.send_keys(auto_name)
            time.sleep(2)
            print(" Auto slug entered using the name.")

        except Exception as e:
            print(f" Failed to enter slug: {e}")


        try:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="The Subtitle was edited successfully ", attachment_type=AttachmentType.PNG)                
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.update_subtitle_element))
            ).click()
            time.sleep(2)   
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="The Subtitle was edited successfully ", attachment_type=AttachmentType.PNG)                
            print("Subtitle was added successfully.")
            time.sleep(5)
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="The Subtitle was edited successfully ", attachment_type=AttachmentType.PNG)
            pytest.fail()                
            print(f"An error occurred: {e}")
            raise
                
       

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
   

  
