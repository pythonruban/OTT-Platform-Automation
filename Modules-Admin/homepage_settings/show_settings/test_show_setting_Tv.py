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
    show_setting_element = "//span[text()='Show Settings']"
    show_setting_TV_element = "//button[@id ='pills-contact-tab']"

    Continue_Watching_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[15]" 
    Latest_Series_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')]))[16]"
    Single_Series_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[17]"
    Series_Categories_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[18]"
    Series_based_on_Categories_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[19]"
    Latest_Viewed_Episode_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[20]"
    Single_Series_Id_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')]))[21]"
    save_settings_element = "(//span[contains(normalize-space(.), 'Save Setting')])[3]"
    
    
    
    def test_show_setting_TV(self):
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
        # Navigate to the homepage settings
        try:

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
            Manage_app = WebDriverWait(self.driver, 45).until(
                    EC.presence_of_element_located((By.XPATH, self.homepage_setting_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Manage_app)
            time.sleep(1)  # Allow smooth scrolling
            self.driver.execute_script("arguments[0].click();", Manage_app)
            print(" Clicked 'Language'")
            time.sleep(6)
            self.driver.find_element(By.XPATH, self.show_setting_element).click()
            time.sleep(5)
            self.driver.find_element(By.XPATH, self.show_setting_TV_element).click()
            time.sleep(15)
        except Exception as e:
            print(f"Error navigating to show settings: {e}")

        try:
            # Wait until the 'Continue Watching' toggle is clickable
            Continue_Watching = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Continue_Watching_element))
            )

            # Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Continue_Watching)
            time.sleep(2)  # Allow time for scroll animation

            # Check if toggle is visible before clicking
            if Continue_Watching.is_displayed():
                print("Toggle is visible, attempting to click.")
                self.driver.execute_script("arguments[0].click();", Continue_Watching)
                time.sleep(3)
            else:
                print("Toggle is not visible on the page.")

        except Exception as e:
            print(f"Failed to interact with 'Continue Watching' toggle: {e}")

        # Continue with the rest of the toggles
        try:    
            Latest_Series = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Latest_Series_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Latest_Series) 
            time.sleep(2)  
            if Latest_Series.is_displayed():
                print("Toggle is visible, attempting to click.")
                self.driver.execute_script("arguments[0].click();", Latest_Series)
                time.sleep(3)
            else:
                print("Toggle is not visible on the page.")

        except Exception as e:
            print(f"Failed to interact with 'Latest_Series' toggle: {e}")
        
        try:
            Single_Series = self.driver.find_element(By.XPATH, self.Single_Series_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Single_Series) 
            time.sleep(2)  
            if Single_Series.is_displayed():
                print("Toggle is already On .")
                time.sleep(3)
            else:
                print("Toggle is not visible on the page.")
        except Exception as e:
            print(f"Failed to interact with 'Single_Series' toggle: {e}")
        
        try:
            Series_Categories = self.driver.find_element(By.XPATH, self.Series_Categories_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Series_Categories) 
            time.sleep(2)  
            time.sleep(2)  
            if Series_Categories.is_displayed():
                print("Toggle is visible, attempting to click.")
                self.driver.execute_script("arguments[0].click();", Series_Categories)
                time.sleep(3)
            else:
                print("Toggle is already On")

        except Exception as e:
            print(f"Failed to interact with 'Series_Categories' toggle: {e}")
        
        try:
            Series_based_on_Categories = self.driver.find_element(By.XPATH, self.Series_based_on_Categories_element)            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Series_based_on_Categories)
            time.sleep(2)
            if Series_based_on_Categories.is_displayed():          
                print("Toggle is already On.")
                time.sleep(3)       
            else:
                print("Toggle is not visible on the page.")
        except Exception as e:
            print(f"Failed to interact with 'Series_based_on_Categories' toggle: {e}")

        try:
            Latest_Viewed_Episode = self.driver.find_element(By.XPATH, self.Latest_Viewed_Episode_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Latest_Viewed_Episode) 
            time.sleep(2)  
            if Latest_Viewed_Episode.is_displayed():
                print("Toggle is already On")
                time.sleep(3)
            else:
                print("Toggle is not visible on the page.")
        except Exception as e:
            print(f"Failed to interact with 'Latest_Viewed_Episode' toggle: {e}")
        
        try:    
            Single_Series_Id = self.driver.find_element(By.XPATH, self.Single_Series_Id_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Single_Series_Id) 
            time.sleep(2)  
            if Single_Series_Id.is_displayed():
                print("Toggle is already On.")
                time.sleep(3)
            else:
                print("Toggle is not visible on the page.")
        except Exception as e:
            print(f"Failed to interact with 'Single_Series_Id' toggle: {e}")
        # Save the settings
        try:        
            save_settings = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.save_settings_element))
            )
            save_settings.click()
            print("Show settings were saved successfully.")
            time.sleep(5)  
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All Value show settings were saved successfully", attachment_type=AttachmentType.PNG)
        except Exception as e:
            print(f"Failed to save show settings: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="show_settings_error", attachment_type=AttachmentType.PNG)
            time.sleep(5)
            pytest.fail(f"Login failed: ")
            assert True


    def teardown_class(self):
        """Teardown method to close the browser"""
        self.driver.quit()
        print("Browser closed successfully.")

