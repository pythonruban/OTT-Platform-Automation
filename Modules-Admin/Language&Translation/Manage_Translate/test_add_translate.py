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
    add_language_code_element = "//button[@id='navigationLinkForAddPage']"
    language_name_element = "//input[@name='name']"
    language_slug_element = "//input[@name='slug']"
    default_language_element ="//input[@name='code']"
    save_change_element ="(//span[@class='slider round'])[1]"
    add_new_element ="(//span[@class='slider round'])[2]"
    new_language_button_element= "//button[@type='submit']"


    
    def test_add_translate(self,browser_setup):
        self.driver = browser_setup
        """Login to the admin panel"""
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
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name=" All required data was entered and login was successful", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="login_error", attachment_type=AttachmentType.PNG)
            print(f" Failed to enter email: {e}")
 

   
        
       

        # Locate and click 'Manage Language' element
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            manage_app = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.Manage_language_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", manage_app)
            time.sleep(1)  # Allow smooth scrolling
            self.driver.execute_script("arguments[0].click();", manage_app)
            print("Clicked 'Language'")
            time.sleep(6)
        except Exception as e:
            print(f"Failed to click 'Manage Language': {e}")
           

        # Click 'Translate' element
        try:
            translate_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.translate_element))
            )
            translate_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Failed to click 'Translate': {e}")
           

        # Click 'Add Language Code' element
        try:
            add_language_code_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.add_language_code_element))
            )
            add_language_code_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Failed to click 'Add Language Code': {e}")
         

        # Enter language name
        try:
            # Generate a random uppercase string of length between 5 and 7
            length = random.randint(5, 7)
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")

            print(f"Using XPath: {self.language_name_element}")

            # Wait for the title input to be clickable
            name = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.language_name_element))
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

        # try:
        #     print(f"Using XPath for slug input: {self.language_slug_element}")

        #     slug = WebDriverWait(self.driver, 30).until(
        #         EC.element_to_be_clickable((By.XPATH, self.language_slug_element))
        #     )
        #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slug)
        #     time.sleep(2)
        #     slug.clear()
        #     time.sleep(2)
        #     slug.send_keys(auto_name)
        #     time.sleep(2)
        #     print(" Auto slug entered using the name.")

        # except Exception as e:
        #         print(f" Failed to enter slug: {e}")

            

        # Enter default language code
        try:
            length = random.randint(2, 3)
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")

            print(f"Using XPath: {self.language_name_element}")

            # Wait for the title input to be clickable
            code_filed = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.default_language_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", code_filed)
            time.sleep(2)
            code_filed.clear()
            time.sleep(2)  # small delay to ensure field is cleared
            code_filed.send_keys(auto_name)
            time.sleep(2)
        except Exception as e:
            print(f"Failed to enter default language code: {e}")
            

        # Click 'Save Changes' button
        try:
            toggle_button = self.driver.find_element(By.XPATH, self.save_change_element)
            if toggle_button.is_displayed():
                toggle_button.click()
                print("Toggle button clicked.")
            else:
                print("Toggle button is not available.")
            time.sleep(3)
        except Exception as e:
            print(f"Failed to click 'Save Changes': {e}")
            

        # Click 'Add New' button
        try:
            # Wait until the toggle button is clickable
            toggle_button2 = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.add_new_element))
            )
            
            # Scroll the element into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle_button2)
            
            # Click the toggle button
            toggle_button2.click()
            print("Toggle button clicked.")
        except Exception as e:
            print(f"Failed to click 'Add New': {e}")
                # Click 'New Language' button
        try:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All details were entered in the language code.", attachment_type=AttachmentType.PNG)
            new_language_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.new_language_button_element))
            )
            new_language_button.click()
            print("Language was added successfully.")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="New Language was Added Successfully.", attachment_type=AttachmentType.PNG)
            time.sleep(5)
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Adding Error.", attachment_type=AttachmentType.PNG)

            print(f"Failed to click 'New Language': {e}")
            raise

        
    
    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")

   
