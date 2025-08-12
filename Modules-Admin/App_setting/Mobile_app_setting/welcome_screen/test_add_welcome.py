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

class TestAppSettings:
    driver = webdriver.Firefox
    # Locators
     #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "10801620.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "1920x1080-hd.jpg")
    videoFile_path = os.path.join(base_dir, "sample_video.mp4")
    pdfFile_path = os.path.join(base_dir, "pdf1.pdf")  


    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_btn_element = "(//button[@type='submit'])[2]"
    app_setting_element = "//span[contains(@class, 'ms-2') and contains(@class, 'text-break') and text()='App Settings']"
    Mobile_app_setting_element = "//span[contains(@class, 'ms-2') and contains(@class, 'text-break') and text()='Mobile App Settings']"
    welcomw_menu_element = "//button[@id='pills-profile-tab']"
    add_welcome_element = "//button[@data-bs-target='#welcome']"
    welcome_title_element = "//input[@name='name']"
    Wlocome_description_element = "//textarea[@name='description']"
    welcome_screen_element = "//input[@type='file' and @id='fileInputRef3']"
    welcome_screen_andriod_element = "//input[@type='file' and @id='fileInputRef9']"
    welcome_screen_andriodTv_element = "(//input[@type='file' and @id='fileInputRef1'])[2]"
    welcome_screen_LGTV_element = "//input[@type='file' and @id='fileInputRef11']"
    welcome_screen_rokuTV_element = "//input[@type='file' and @id='fileInputRef12']"
    welcome_screen_SamsungTV_element = "//input[@type='file' and @id='fileInputRef13']"
    welcome_screen_FireTV_element = "//input[@type='file' and @id='fileInputRef8']"
    save_welcome_screen_element ="//button[contains(normalize-space(.), 'Save Welcome Screen')]"



    def test_add_welcome_screen(self,browser_setup):
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
            print("Playout setting page is opened successfully")
            self.driver.execute_script("arguments[0].click();", Mobile)
            time.sleep(2)
            welcome_menu =WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, self.welcomw_menu_element))
                )
            welcome_menu.click()
            time.sleep(2)
            welcome =WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, self.add_welcome_element))
                )
            welcome.click()
        except Exception as e:
            print(f"Failed to open playout setting page: {e}")

        try:
            element = WebDriverWait(self.driver, 110).until(
                EC.visibility_of_element_located((By.XPATH, self.welcome_title_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)
            element.clear()
            element.send_keys("Home")
            time.sleep(4)

            desc = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.Wlocome_description_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", desc)
            time.sleep(1)
            desc.clear()
            desc.send_keys("This the Description odf the Welcome Screen")
            time.sleep(4)
            
            image1=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.welcome_screen_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image1)
            time.sleep(2)
            image1.send_keys(self.imageFile1280_720_path) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)
        
        try:
            welcome_screen_andriod=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.welcome_screen_andriod_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", welcome_screen_andriod)
            time.sleep(2)
            welcome_screen_andriod.send_keys(self.imageFile1280_720_path) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)
                
        try:
            welcome_screen_andriodTv=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.welcome_screen_andriodTv_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", welcome_screen_andriodTv)
            time.sleep(2)
            welcome_screen_andriodTv.send_keys(self.imageFile1280_720_path) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)

        try:
            welcome_screen_LGTV=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.welcome_screen_LGTV_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", welcome_screen_LGTV)
            time.sleep(2)
            welcome_screen_LGTV.send_keys(self.imageFile1280_720_path) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)

        try:
            welcome_screen_rokuTV=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.welcome_screen_rokuTV_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", welcome_screen_rokuTV)
            time.sleep(2)
            welcome_screen_rokuTV.send_keys(self.imageFile1280_720_path) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)
        
        try:
            welcome_screen_SamsungTV=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.welcome_screen_SamsungTV_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", welcome_screen_SamsungTV)
            time.sleep(2)
            welcome_screen_SamsungTV.send_keys(self.imageFile1280_720_path) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)

        try:
            welcome_screen_FireTV=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.welcome_screen_FireTV_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", welcome_screen_FireTV)
            time.sleep(2)
            welcome_screen_FireTV.send_keys(self.imageFile1280_720_path) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)

        try:
            save=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.save_welcome_screen_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save)
            time.sleep(2)
            save.click() 
            time.sleep(2)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All Splash Screen Image was upload successfully and save", attachment_type=AttachmentType.PNG)
            time.sleep(15)

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All Splash Screen Image Error", attachment_type=AttachmentType.PNG)

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")
        except Exception as e:
            print(f"Unexpected error while quitting the driver: {e}")