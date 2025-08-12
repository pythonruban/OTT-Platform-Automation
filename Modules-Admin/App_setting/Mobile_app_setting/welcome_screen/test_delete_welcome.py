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

class TestAppSettings:
    driver = webdriver.Firefox
    # Locators
     

    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_btn_element = "(//button[@type='submit'])[2]"
    app_setting_element = "//span[contains(@class, 'ms-2') and contains(@class, 'text-break') and text()='App Settings']"
    Mobile_app_setting_element = "//span[contains(@class, 'ms-2') and contains(@class, 'text-break') and text()='Mobile App Settings']"
    welcome_menu_element = "//button[@id='pills-profile-tab']"

    delete_element ="(//span[contains(@class, 'editdropdown-button')])[2]"
    delete_menu = "(//span[contains(text(), 'Delete')])[2]"
    confrim_delete_element ="//button[normalize-space(text())='Yes']"


    
    def test_delete_welcome_screen(self,browser_setup):
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
                EC.element_to_be_clickable((By.XPATH, self.login_btn_element))
            ).click()

            print(" Login Successful!")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All Value login Credentials was entered, and the login button was clicked. it was redirect to Dashboard", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="login_error", attachment_type=AttachmentType.PNG)
            print(f" Failed to enter email: {e}")
        time.sleep(2)
       
    
    
        try:
       
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
            Manage_app = WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, self.app_setting_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Manage_app)
            time.sleep(1)  # Allow smooth scrolling
        
            self.driver.execute_script("arguments[0].click();", Manage_app)
            time.sleep(2)
            Mobile =WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, self.Mobile_app_setting_element))
                )
            Mobile.click()
            time.sleep(2)
            print("App setting page is opened successfully")
            self.driver.execute_script("arguments[0].click();", Mobile)
            time.sleep(2)
            splash_menu =WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, self.welcome_menu_element))
                )
            splash_menu.click()
            print("Welcome menu buuton was click successfully ")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All Welcome Screen Image was Deleted successfully ", attachment_type=AttachmentType.PNG)
            time.sleep(5)
        
        except Exception as e:
            print(f"Failed to open playout setting page: {e}")

        try:
            # ====== EDIT ELEMENT ======
            edit = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.delete_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit)
            time.sleep(3)

            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.delete_element)
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
            confrim=WebDriverWait(self.driver, 130).until(
                EC.presence_of_element_located((By.XPATH, self.confrim_delete_element))
            )

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confrim)
            time.sleep(2)
            confrim.click()
            time.sleep(12)
            

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")
        except Exception as e:
            print(f"Unexpected error while quitting the driver: {e}")
        