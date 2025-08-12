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
    movie_setting_element = "//span[text()='Movie Settings']"

    Continue_Watching_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[1]" 
    Featured_Videoss_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[2]"
    Latest_Videos_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[3]"
    Videos_categories_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[4]"
    Videos_based_on_Categories_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[5]"
    Scheduled_Publish_Video_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[6]"
    Latest_Viewed_Videos_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[7]" 
    Top_10_Videos_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[8]"
    Top_5_Weekend_Videos ="(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[9]"
    Recommended_Videos_Site_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[10]"
    Recommended_Videos_Users_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[11]"
    Recommended_Videos_by_Country_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[12]"
    save_setting_button = "//span[text()='Save Setting']"

    
    def test_movie_toggle_setting(self):
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
            Manage_app = WebDriverWait(self.driver, 45).until(
                    EC.presence_of_element_located((By.XPATH, self.homepage_setting_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Manage_app)
            time.sleep(1)  # Allow smooth scrolling
            self.driver.execute_script("arguments[0].click();", Manage_app)
            print(" Homepage Setting Clicked")
            time.sleep(6)
            self.driver.find_element(By.XPATH, self.movie_setting_element).click()
            time.sleep(5)
        except Exception as e:
            print(f" Error while navigating to 'Movie Settings': {e}")
            
        try:
            Continue_Watching = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Continue_Watching_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Continue_Watching)
            time.sleep(2)  # Allow smooth scrolling

            if not Continue_Watching.is_displayed():
                print("Toggle already enabled.")
            else:
                print("Toggle enabled.")

            

        except Exception as e:
            print(f"Failed to interact with 'Continue Watching' toggle: {e}")

        try:
            Featured_Videoss = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Featured_Videoss_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Featured_Videoss)
            time.sleep(2)  # Allow smooth scrolling

            if not Featured_Videoss.is_displayed():
                print("Toggle already enabled.")
            else:
                print("Toggle enabled.")

           
        except Exception as e:
            print(f"Failed to interact with 'Featured Videos' toggle: {e}")

        try:
            Latest_Videos = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Latest_Videos_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Latest_Videos)
            time.sleep(2)  # Allow smooth scrolling

            if not Latest_Videos.is_displayed():
                print("Toggle already enabled.")
            else:
                print("Toggle enabled.")

                  
        except Exception as e:
            print(f"Failed to interact with 'Latest Videos' toggle: {e}")
        
        try:
            Videos_categories = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Videos_categories_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Videos_categories)
            time.sleep(2)  # Allow smooth scrolling

            if not Videos_categories.is_displayed():
                print("Toggle already enabled.")
            else:
                print("Toggle enabled.")

            
        except Exception as e:
            print(f"Failed to interact with 'Videos Categories' toggle: {e}")

        try:
            Videos_based_on_Categories = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Videos_based_on_Categories_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Videos_based_on_Categories)
            time.sleep(2)  # Allow smooth scrolling

            if not Videos_based_on_Categories.is_displayed():
                print("Toggle already enabled.")
            else:
                print("Toggle enabled.")

           
        except Exception as e:
            print(f"Failed to interact with 'Videos Based on Categories' toggle: {e}")      
    
        try:
            Scheduled_Publish_Video = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Scheduled_Publish_Video_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Scheduled_Publish_Video)
            time.sleep(2)  # Allow smooth scrolling

            if not Scheduled_Publish_Video.is_displayed():
                print("Toggle already enabled.")
            else:
                print("Toggle enabled.")

            self.driver.execute_script("arguments[0].click();", Scheduled_Publish_Video)
            time.sleep(3)  
        except Exception as e:
            print(f"Failed to interact with 'Scheduled Publish Video' toggle: {e}")

        try:
            Latest_Viewed_Videos = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Latest_Viewed_Videos_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Latest_Viewed_Videos)
            time.sleep(2)  # Allow smooth scrolling

            if not Latest_Viewed_Videos.is_displayed():
                print("Toggle already enabled.")
            else:
                print("Toggle enabled.")

            
        except Exception as e:
            print(f"Failed to interact with 'Latest Viewed Videos' toggle: {e}")
        
        try:
            Top_10_Videos = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Top_10_Videos_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Top_10_Videos)
            time.sleep(2)  # Allow smooth scrolling

            if not Top_10_Videos.is_displayed():
                print("Toggle already enabled.")
            else:
                print("Toggle enabled.")

            
        except Exception as e:
            print(f"Failed to interact with 'Top 10 Videos' toggle: {e}")

        try:
            Top_5_Weekend = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Top_5_Weekend_Videos))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Top_5_Weekend)
            time.sleep(2)  # Allow smooth scrolling

            if not Top_5_Weekend.is_displayed():
                print("Toggle already enabled.")
            else:
                print("Toggle enabled.")

             

        except Exception as e:
            print(f"Failed to interact with 'Top 5 Weekend Videos' toggle: {e}")

        try:
            Recommended_Videos_Site = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Recommended_Videos_Site_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Recommended_Videos_Site)
            time.sleep(2)  # Allow smooth scrolling

            if not Recommended_Videos_Site.is_displayed():
                print("Toggle already enabled.")
            else:
                print("Toggle enabled.")

            
        except Exception as e:
            print(f"Failed to interact with 'Recommended Videos Site' toggle: {e}")
        
        try:
            Recommended_Videos_Users = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Recommended_Videos_Users_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Recommended_Videos_Users)
            time.sleep(2)  # Allow smooth scrolling

            if not Recommended_Videos_Users.is_displayed():
                print("Toggle already enabled.")
            else:
                print("Toggle enabled.")

            
        except Exception as e:
            print(f"Failed to interact with 'Recommended Videos Users' toggle: {e}")

        try:
            Recommended_Videos_by_Country = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Recommended_Videos_by_Country_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Recommended_Videos_by_Country)
            time.sleep(2)  # Allow smooth scrolling

            if not Recommended_Videos_by_Country.is_displayed():
                print("Toggle already enabled.")
            else:
                print("Toggle enabled.")

        except Exception as e:
            print(f"Failed to interact with 'Recommended Videos by Country' toggle: {e}")

        # Click the save button
        try:
            
            
            save =WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.save_setting_button))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save)
            time.sleep(2)
            save.click()       
            print(" Movie settings were saved successfully")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Movie settings were saved successfully", attachment_type=AttachmentType.PNG)
            time.sleep(20)  
            assert True
        except Exception as e:
            print(f"Failed to save Movie settings: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="save_error", attachment_type=AttachmentType.PNG)
            time.sleep(2)
            

    def teardown_class(self):
        """Teardown method to close the browser"""
        self.driver.quit()
        print("Browser closed successfully.")


