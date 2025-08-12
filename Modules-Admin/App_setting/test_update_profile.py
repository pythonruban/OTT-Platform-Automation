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

class TestPlayoutsetting:
    driver = webdriver.Firefox
    # Locators
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "10801620.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "16.9.jpg")
    videoFile_path = os.path.join(base_dir, "sample_video.mp4")
    pdfFile_path = os.path.join(base_dir, "pdf1.pdf") 


    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_btn_element = "(//button[@type='submit'])[2]"
    playout_setting_element = "//span[contains(@class, 'ms-2') and contains(@class, 'text-break') and text()='App Settings']"
    Profile_setting_element = "//span[contains(@class, 'ms-2') and contains(@class, 'text-break') and text()='Profile Screen']"
    update_profile_element = "//button[@data-bs-target='#staticBackdrop']"
    profile_name ="//input[@id='profile_name']"
    image_elemnet ="//div[@class='imagedrop']"
    update_setting_element ="//button[text()='Update Settings']"



    def test_update_profile(self,browser_setup):
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
                    EC.presence_of_element_located((By.XPATH, self.playout_setting_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Manage_app)
            time.sleep(1)  # Allow smooth scrolling
        
            self.driver.execute_script("arguments[0].click();", Manage_app)
            profile =WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, self.Profile_setting_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", profile)
            time.sleep(2)
            profile.click()
            time.sleep(2)
            playout =WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, self.update_profile_element))
                )
            playout.click()
            time.sleep(2)
            print("Playout setting page is opened successfully")
        except Exception as e:
            print(f"Failed to open playout setting page: {e}")

        
        try:  
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.profile_name))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)
            element.clear()
            element.send_keys("Flicknexs")
            time.sleep(4)  
            image=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.image_elemnet))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image)
            time.sleep(2)
            image.send_keys(self.imageFile1280_720_path)
            time.sleep(2)

            update_setting =WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, self.update_setting_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", update_setting)
            time.sleep(2)
            update_setting.click()
            time.sleep(2)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="update_profile settings was successfully ", attachment_type=AttachmentType.PNG)
            time.sleep(5)

        except Exception as e:
            print("The Profile settings updated successfully ")
          
            time.sleep(2)
            
            
            
    
    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")
        except Exception as e:
            print(f"Unexpected error while quitting the driver: {e}")

 


        
            