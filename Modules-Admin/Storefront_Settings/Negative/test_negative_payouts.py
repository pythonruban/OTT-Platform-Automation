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
    payouts_setting_element="//h5[contains(text(), 'Payouts Settings')]" #xpath
    payout_status_element ="(//span[contains(@class, 'admin-slider')])[1]" #xpath
    Monetization_View_Limitn_element ="//input[@name='viewcount_limit']" #xpath
    Amount_per_view_element = "//input[@name='views_amount']" #xpath
    Video_View_Limit_element = "//input[@name='video_viewcount_limit']" #xpath
    save_Payouts_element ="//button[text()='Save Payouts']" #xpath


    def test_negative_payouts(self,browser_setup):
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
            store_click = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.storeForntsetting_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", store_click)
            time.sleep(1)  # Allow smooth scrolling
            self.driver.execute_script("arguments[0].click();", store_click)
            print(" Clicked 'Store Front Setting'")
        except Exception as e:
            print(f" Error while clicking 'Store Front Setting': {e}")

        # Click 'Payouts Setting'
        try:
            pAyouts_page=WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.payouts_setting_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pAyouts_page )
            time.sleep(2)
            pAyouts_page.click()
            time.sleep(2)
            print(" Clicked 'Payouts Setting'")
        except Exception as e:
            print(f" Error while clicking 'Payouts Setting': {e}")

        #Partner Monetization Settings
        try:
            print(" Checking 'Active' toggle state...")
            pAyouts = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.payout_status_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pAyouts  )
            time.sleep(1)
            active_class = pAyouts.get_attribute("class")
            if "active"  in active_class.lower():
                    print(" 'Active' toggle already ON. Skipped.")
            else:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.payout_status_element))
                )
                self.driver.execute_script("arguments[0].click();", pAyouts)
                print("  toggle was OFF, now turned ON.")
                
        except Exception as e:
            print(f" Error handling  toggle: {e}")
                                
    #Partner Monetization Settings
        try:
            # Locate Monetization View Limit field
            monetization_field = self.driver.find_element(By.XPATH, self.Monetization_View_Limitn_element)
            
            # Step 1: Clear and click Submit with field empty
            monetization_field.clear()
            time.sleep(1)

            # Locate and click the Submit button
            submit_button = self.driver.find_element(By.XPATH, self.save_Payouts_element)
            submit_button.click()
            print("Clicked Submit with empty 'Monetization View Limit'")
            time.sleep(2)

            # (Optional) Check for validation error message here if needed

            # Step 2: Enter invalid alphabetic value but DO NOT click submit
            monetization_field.send_keys("abc")
            time.sleep(1)
            entered_value = monetization_field.get_attribute("value")

            if not entered_value.isdigit():
                print("Alphabetic value entered (but not submitted) in 'Monetization View Limit'")
            else:
                print("Unexpected: Non-numeric input accepted as numeric")

        except Exception as e:
            print(f" Exception in Monetization View Limit test: {e}")


            # Amount Per View
            amount_field = self.driver.find_element(By.XPATH, self.Amount_per_view_element)
            amount_field.clear()
            time.sleep(2)
            amount_field.send_keys("abc")
            time.sleep(1)

            entered_value = amount_field.get_attribute("value")
            if not entered_value.isdigit():
                amount_field.clear()
                time.sleep(2)
                amount_field.send_keys("100")
                print(" Entered valid number in 'Amount Per View'")
            else:
                print(" Alphabetic value was incorrectly accepted in 'Amount Per View'")

            time.sleep(2)

            # Video View Limit
            view_limit_field = self.driver.find_element(By.XPATH, self.Video_View_Limit_element)
            view_limit_field.clear()
            time.sleep(2)
            view_limit_field.send_keys("abc")
            time.sleep(1)

            entered_value = view_limit_field.get_attribute("value")
            if not entered_value.isdigit():
                view_limit_field.clear()
                time.sleep(2)
                view_limit_field.send_keys("200000000000000000")
                print(" Entered valid number in 'Video View Limit'")
            else:
                print(" Alphabetic value was incorrectly accepted in 'Video View Limit'")

            time.sleep(2)

        except Exception as e:
            print(f" Error while entering monetization data: {e}")



        try:
                self.driver.find_element(By.XPATH, self.save_Payouts_element).click()
                print(" Payouts setting updated successfully")
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name="PayoutsSaved",  attachment_type=AttachmentType.PNG)
                time.sleep(4)

        except Exception as e:
            print(f" Error while saving Payouts Setting: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="PayoutsSaveError",  attachment_type=AttachmentType.PNG)
            

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 
    
    

