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
class TestMainSettings:
    driver = webdriver.Firefox
    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    Settings_element = "//div[@data-bs-target='#Settings']"
    otp_credentials_elemnt ="//span[text()='OTP Credentials']"
    Enable_otp_element ="//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')]"
    choose_otp_service ="//select[@name='otp_vai']"
    APIKEY24x7sms_element ="//input[@name ='otp_24x7sms_api_key']"
    Sender_ID24_7Sms_element = "//input[@name ='otp_24x7sms_sender_id']"
    Service_Name_24_7_Sms = "//input[@name ='otp_24x7sms_sevicename']"
    DLTTemplateID_element = "//input[@name ='DLTTemplateID']"
    Template_Message_element = "//input[@name ='template_message']"
    save_button_element = "//button[@id='adminButton']"
    
    def test_24_7sms(self,browser_setup):
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
        time.sleep(2)
    
    
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            settings = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.Settings_element))
            )
            self.driver.execute_script("arguments[0].click();", settings)
            time.sleep(2)
            otp = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.otp_credentials_elemnt))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", otp)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", otp)
            print("Navigated to 'OTP Credentails'")
        except Exception as e:
            print(f"[ERROR] Clicking  failed: {e}")

        try:
            Enable_OTP = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.Enable_otp_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Enable_OTP)
            time.sleep(1)
            feature_class = Enable_OTP.get_attribute("class")
            if "active" in feature_class.lower():
                print(" 'Feature' toggle already active. Skipped.")
            else:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.Enable_otp_element))
                )
                self.driver.execute_script("arguments[0].click();", Enable_OTP)
                print(" 'Feature' toggle was OFF, now turned ON.")
        except Exception as e:
            print(f" Error handling : {e}")

        try:
            choose = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.choose_otp_service))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", choose)
            time.sleep(2)
            Select(choose).select_by_value("24x7sms")
            time.sleep(2)
            print(" Choose OTP Service set fast2sms successfully.")
        except Exception as e:
            print(f" Error setting Choose OTP Service : {e}")
        
        try:
           
            APIKEY24x7sms  = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.APIKEY24x7sms_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", APIKEY24x7sms)
            time.sleep(2)
            APIKEY24x7sms.send_keys("otp_test_api_key_1234567890abcdef")
            print(" APIKEY24x7sms entered.")
            time.sleep(3)
        except Exception as e:
                print(f" Error entering  DATA: {e}")
    #API KEY - 24x7sms 
        try:
           
            Sender_ID   = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.Sender_ID24_7Sms_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Sender_ID)
            time.sleep(2)
            Sender_ID.send_keys("otp_test_api_key_1234567890abcdef")
            print(" Sender_ID entered.")
            time.sleep(3)
        except Exception as e:
                print(f" Error entering  DATA: {e}")

        try:
           
            Service_Name   = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.Service_Name_24_7_Sms))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Service_Name)
            time.sleep(2)
            Service_Name.send_keys("otp_test_api_key_1234567890abcdef")
            print(" Service_Name entered.")
            time.sleep(3)          
        except Exception as e:
                print(f" Error entering  DATA: {e}")

        try: 
            DLT_Template_ID   = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.DLTTemplateID_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", DLT_Template_ID)
            time.sleep(2)
            DLT_Template_ID.send_keys("otp_test_api_key_1234567890abcdef")
            print(" DLT_Template_ID entered.")
            time.sleep(3)          
        except Exception as e:
                print(f" Error entering  DATA: {e}")
        
        try: 
            Template_Message   = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.Template_Message_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Template_Message)
            time.sleep(2)
            Template_Message.send_keys("otp_test_api_key_1234567890abcdef")
            print(" Template_Message entered.")
            time.sleep(3)          
        except Exception as e:
                print(f" Error entering  DATA: {e}")
        try:
            submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.save_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", submit_button)
            print(" OIP Credential was save successfully.")
            time.sleep(6)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="The OTP credentials for the 24x7 sms API key were created successfully.",attachment_type=AttachmentType.PNG)
            time.sleep(2)
        except Exception as e:
            print(f" Error clicking submit button: {e}")  

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")