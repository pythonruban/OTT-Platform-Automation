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
    recaptcha_setting_element="//h5[contains(text(), 'Recaptcha Settings')]" #xpath
    captcha_site_key_element ="//input[@name='captcha_site_key']" #xpath
    captcha_secert_key_element = "//input[@name='captcha_secret_key']" #xpath
    Enable_Signin_Captcha= "(//span[contains(@class, 'admin-slider')])[1]" #xpath
    Enable_Signup_Captcha= "(//span[contains(@class, 'admin-slider')])[2]" #xpath
    Enable_contactUs_Captcha= "(//span[contains(@class, 'admin-slider')])[3]" #xpath
    save_captcha_element ="//button[text()='Save Re-captcha']" #xpath


    def test_Recaptcha_setting(self,browser_setup):
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
            # Wait for the reCAPTCHA settings element to be clickable
            recaptcha = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.recaptcha_setting_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", recaptcha)
            time.sleep(2)
            recaptcha.click()
            time.sleep(2)

        
        except Exception as e:
            # Handle other exceptions
            print(f"An unexpected error occurred: {e}")
            

        try:
            # Locate and clear the CAPTCHA Site Key input field
            captcha = self.driver.find_element(By.XPATH, self.captcha_site_key_element)
            captcha.clear()
            time.sleep(3)
            captcha.send_keys("CAPTCHA")
            time.sleep(2)

            # Locate and clear the CAPTCHA Secret Key input field
            secret_key = self.driver.find_element(By.XPATH, self.captcha_secert_key_element)
            secret_key.clear()
            time.sleep(3)
            secret_key.send_keys("CAPTCHA@123")
            time.sleep(2)

            # Optionally, add code to save the settings here

            print("Site created and CAPTCHA settings updated successfully")

    
            
        except Exception as e:
            # Handle other exceptions
            print(f"An unexpected error occurred: {e}")
            

                #Status Settings
        try:
            print(" Checking 'Active' toggle state...")
            signin = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.Enable_Signin_Captcha))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", signin  )
            time.sleep(1)
            active_class = signin.get_attribute("class")
            if "active"  in active_class.lower():
                    print(" 'Active' toggle already ON. Skipped.")
            else:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.Enable_Signin_Captcha))
                )
                self.driver.execute_script("arguments[0].click();", signin)
                print("  toggle was OFF, now turned ON.")
                
        except Exception as e:
            print(f" Error handling  toggle: {e}")

        try:
            print(" Checking 'Active' toggle state...")
            signup = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.Enable_Signup_Captcha))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", signup  )
            time.sleep(1)
            active_class = signup.get_attribute("class")
            if "active"  in active_class.lower():
                    print(" 'Active' toggle already ON. Skipped.")
            else:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.Enable_Signup_Captcha))
                )
                self.driver.execute_script("arguments[0].click();", signup)
                print("  toggle was OFF, now turned ON.")
                
        except Exception as e:
            print(f" Error handling  toggle: {e}")

        try:
            print(" Checking 'Active' toggle state...")
            Contact = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.Enable_contactUs_Captcha))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Contact  )
            time.sleep(1)
            active_class = Contact.get_attribute("class")
            if "active"  in active_class.lower():
                    print(" 'Active' toggle already ON. Skipped.")
            else:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.Enable_contactUs_Captcha))
                )
                self.driver.execute_script("arguments[0].click();", Contact)
                print("  toggle was OFF, now turned ON.")
                
        except Exception as e:
            print(f" Error handling  toggle: {e}")
        
        try:
                self.driver.find_element(By.XPATH, self.save_captcha_element).click()
                print(" Payouts setting updated successfully")
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Captcha Was Saved Successful in Store Front Settings",  attachment_type=AttachmentType.PNG)
                time.sleep(4)

        except Exception as e:
            print(f" Error while saving Payouts Setting: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="CaptchaSaveError",  attachment_type=AttachmentType.PNG)


        
    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")
    
    