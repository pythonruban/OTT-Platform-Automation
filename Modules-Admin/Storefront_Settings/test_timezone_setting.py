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

class TestStorefrontsettings :

    driver = webdriver.Firefox
    
      #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "10801620.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "16.9.jpg")
    videoFile_path = os.path.join(base_dir, "sample_video.mp4")
    vttfile_path = os.path.join(base_dir, "vttfile.vtt")
    # Locators
    email_element = "(//input[@type='email'])[2]" #xpath
    password_element = "(//input[@name='password'])[1]" #xpath
    login_element = "(//button[@type='submit'])[2]"#xpath

    storeForntsetting_element="//a[contains(@href, '/settings') and contains(., 'Storefront Settings')]"
    Timezone_setting_element="//h5[contains(text(), 'TimeZone Settings')]" #xpath
    Choose_TimeZone_element ="default_time_zone" #id
    save_Timezone_element ="//button[text()='Update']" #xpath


    def test_timezone_setting(self,browser_setup):
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
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All Value login Credentials was entered, and the login button was clicked. it was redirect to Dashboard", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="login_error", attachment_type=AttachmentType.PNG)
            print(f" Failed to enter email: {e}")

    
        """Navigate and go to Series setting"""

        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            store_front = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, self.storeForntsetting_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", store_front)
            self.driver.execute_script("arguments[0].click();", store_front)
            print(" Navigated to 'store front setting'")
        except Exception as e:
            print(f" Error while navigating to 'store front setting': {e}")

        try:
            

            Timezone = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.Timezone_setting_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Timezone)
            time.sleep(2)
            Timezone.click()
            time.sleep(2)
            print(" Timezone setting clicked successfully")
        except Exception as e:
            print(f" Error while interacting with Timezone setting: {e}")

        try:
            # Time Zone Settings
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, self.Choose_TimeZone_element))
            )
            dropdown.click()
            time.sleep(2)
            # Wrap the WebElement in Select
            select = Select(dropdown)
            select.select_by_value("Asia/Calcutta")  
            print(" The Time Zone is selected successfully")

        except Exception as e:
            print(f" Error while selecting the Time Zone: {e}")


        try:
            self.driver.find_element(By.XPATH, self.save_Timezone_element).click()
            print(" Payouts setting updated successfully")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Timezone was successfully updated in the Storefront Settings page", attachment_type=AttachmentType.PNG)
            time.sleep(4)
        except Exception as e:
            print(f" Error while saving Timezone setting: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="SaveTimezoneError", attachment_type=AttachmentType.PNG)
            


    

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")
 
 
