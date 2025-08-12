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
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"

    storeForntsetting_element="//a[contains(@href, '/settings') and contains(., 'Storefront Settings')]"
    Geofencing_setting_element="//h5[contains(text(), 'Geo Fencing Settings')]" #xpath
    Block_Country_Status_element ="(//span[contains(@class, 'admin-slider')])[1]"
    Avaliable_Country_Status_element ="(//span[contains(@class, 'admin-slider')])[2]" #xpath
    update_Setting_element ="//button[text()='Update']" #xpath
    

    def test_geofencing_setting(self,browser_setup):
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
            GEo=WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.Geofencing_setting_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", GEo)
            time.sleep(2)
            GEo.click()
            time.sleep(2)
            print(" Clicked 'Geo Fencing Setting'")
        except Exception as e:
            print(f" Error while clicking Setting': {e}")

        try:
            print(" Checking  toggle state...")
            Block_Countr = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.Block_Country_Status_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Block_Countr  )
            time.sleep(1)
            active_class = Block_Countr.get_attribute("class")
            if "active"  in active_class.lower():
                    print(" 'Active' toggle already ON. Skipped.")
            else:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.Block_Country_Status_element))
                )
                self.driver.execute_script("arguments[0].click();", Block_Countr)
                print("  toggle was OFF, now turned ON.")
                
        except Exception as e:
            print(f" Error handling  toggle: {e}")

        try:
            print(" Checking toggle state...")
            Avaliable_Country = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.Avaliable_Country_Status_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Avaliable_Country  )
            time.sleep(1)
            active_class = Avaliable_Country.get_attribute("class")
            if "active"  in active_class.lower():
                    print(" 'Active' toggle already ON. Skipped.")
            else:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.Avaliable_Country_Status_element))
                )
                self.driver.execute_script("arguments[0].click();", Avaliable_Country)
                print("  toggle was OFF, now turned ON.")
                
        except Exception as e:
            print(f" Error handling  toggle: {e}")
        
        try:
                self.driver.find_element(By.XPATH, self.update_Setting_element).click()
                print(" Payouts setting updated successfully")
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Geo Fencing Settings was  Successfully  Added in The StoreFront Settings ",  attachment_type=AttachmentType.PNG)
                time.sleep(4)

        except Exception as e:
            print(f" Error while saving Payouts Setting: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Geo Fencing SettingError",  attachment_type=AttachmentType.PNG)
                


    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")