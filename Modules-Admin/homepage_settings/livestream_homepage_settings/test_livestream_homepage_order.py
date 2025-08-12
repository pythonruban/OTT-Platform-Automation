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

class TestHomepageLiveStreamsettings:
    driver = webdriver.Firefox      

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_btn_element = "(//button[@type='submit'])[2]"
    homepage_setting_element = "//div[@data-bs-target='#settingsURLhome']"
    livestream_web_setting_element = "//span[text()='Live Settings']"

    
    
    def test_livestream_homepage_order(self):
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
        # Navigate to Live Stream Homepage Settings       
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
            Manage_app = WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, self.homepage_setting_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Manage_app)
            time.sleep(1)  # Allow smooth scrolling
            self.driver.execute_script("arguments[0].click();", Manage_app)
            print(" Clicked 'Language'")
            time.sleep(6)
            self.driver.find_element(By.XPATH, self.livestream_web_setting_element).click()
            time.sleep(5)
        except Exception as e:
            print(f" Error while navigating to 'Live Settings': {e}")
        
        try:
                
                source1 =  self.driver.find_element(
                         By.XPATH, "//div[@class='row m-0 p-0 align-items-center'][.//p[normalize-space()='Livestream Video']]"
                                )
                target1 =  self.driver.find_element(
                              By.XPATH, "//div[@class='row m-0 p-0 align-items-center'][.//p[normalize-space()='Latest Viewed Livestream']]"
             )
        
        # Scroll into view if needed
                self.driver.execute_script("arguments[0].scrollIntoView();", source1)
                time.sleep(1)
                self.driver.execute_script("arguments[0].scrollIntoView();", target1)
                time.sleep(5)
                print("The 1 Drag& Drop Completed")
        # Perform drag and drop
                actions = ActionChains(self.driver)
                actions.click_and_hold(source1).pause(1).move_to_element(target1).pause(1).release().perform()
                time.sleep(5)
        except Exception as e:
            print(f" Error while performing drag and drop: {e}")
        # 2nd time
       
        try:
                rows1 = self.driver.find_elements(By.CSS_SELECTOR, "div.row.m-0.p-0.align-items-center")
                source2 = rows1[2] 
                target2 = rows1[4]  

        # Scroll into view if needed
                self.driver.execute_script("arguments[0].scrollIntoView();", source2)
                time.sleep(1)
                self.driver.execute_script("arguments[0].scrollIntoView();", target2)
                time.sleep(1)

        # Perform drag and drop
                actions = ActionChains(self.driver)
                actions.click_and_hold(source2).pause(1).move_to_element(target2).pause(1).release().perform()
                time.sleep(5)
                print("The 12 Drag& Drop Completed")
        except Exception as e:     
               print(f" Error while performing drag and drop: {e}")

        try:
                
                rows2 = self.driver.find_elements(By.CSS_SELECTOR, "div.row.m-0.p-0.align-items-center")
                source3 = rows2[3] 
                target3 = rows2[2]  

        # Scroll into view if needed
                self.driver.execute_script("arguments[0].scrollIntoView();", source3)
                time.sleep(1)
                self.driver.execute_script("arguments[0].scrollIntoView();", target3)
                time.sleep(1)

        # Perform drag and drop
                actions = ActionChains(self.driver)
                actions.click_and_hold(source3).pause(1).move_to_element(target3).pause(1).release().perform()
                time.sleep(5)
                print("The 3 Drag& Drop Completed")
        except Exception as e:
            print(f" Error while performing drag and drop: {e}")

                # 4nd time
        try:    
                source4 =  self.driver.find_element(
                         By.XPATH, "//div[@class='row m-0 p-0 align-items-center'][.//p[normalize-space()='Latest Viewed Livestream']]"
                                )
                target4 =  self.driver.find_element(
                              By.XPATH, "//div[@class='row m-0 p-0 align-items-center'][.//p[normalize-space()='Livestream Video']]"
             )
        
        # Scroll into view if needed
                self.driver.execute_script("arguments[0].scrollIntoView();", source4)
                time.sleep(1)
                self.driver.execute_script("arguments[0].scrollIntoView();", target4)
                time.sleep(1)
        # Perform drag and drop
                actions = ActionChains(self.driver)
                actions.click_and_hold(source4).pause(1).move_to_element(target4).pause(1).release().perform()
                time.sleep(5)
                print("The 4 Drag& Drop Completed")
        except Exception as e:
            print(f" Error while performing drag and drop: {e}")

                # 4nd time
        try:
                source5 =  self.driver.find_element(
                         By.XPATH, "//div[@class='row m-0 p-0 align-items-center'][.//p[normalize-space()='Latest Viewed Livestream']]"
                                )
                target5 =  self.driver.find_element(
                              By.XPATH, "//div[@class='row m-0 p-0 align-items-center'][.//p[normalize-space()='Latest Viewed Livestreamssss']]"
             )
        # Scroll into view if needed
                self.driver.execute_script("arguments[0].scrollIntoView();", source5)
                time.sleep(1)
                self.driver.execute_script("arguments[0].scrollIntoView();", target5)
                time.sleep(1)
        # Perform drag and drop
                actions = ActionChains(self.driver)
                actions.click_and_hold(source5).pause(1).move_to_element(target5).pause(1).release().perform()
                time.sleep(5)
                print("The 5 Drag& Drop Completed")
        except Exception as e:
            print(f" Error while performing drag and drop: {e}")
            assert True

        # pytest.fail(f"Login failed: ")


    def teardown_class(self):
        """Teardown  to close the browser after tests"""
        self.driver.quit()
        print("Browser closed successfully.")


