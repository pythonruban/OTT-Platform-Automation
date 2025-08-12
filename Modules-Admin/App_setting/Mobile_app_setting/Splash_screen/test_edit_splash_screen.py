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
    gifFile_path = os.path.join(base_dir, "Gif2.gif")  
    gifTvFile_path = os.path.join(base_dir, "tvgif.gif")  

    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_btn_element = "(//button[@type='submit'])[2]"
    app_setting_element = "//span[contains(@class, 'ms-2') and contains(@class, 'text-break') and text()='App Settings']"
    Mobile_app_setting_element = "//span[contains(@class, 'ms-2') and contains(@class, 'text-break') and text()='Mobile App Settings']"
    splash_menu_element = "//button[@id='pills-home-tab']"

    edit_element ="(//span[contains(@class, 'editdropdown-button')])[1]"
    edit_menu = "(//span[contains(text(), 'Edit')])[1]"


    splash_screen_ios_element = "//input[@type='file' and @id='splash-splash']"
    splash_screen_andriod_element = "//input[@type='file' and @id='splash-android']"
    splash_screen_andriodTv_element = "//input[@type='file' and @id='splash-androidTv']"
    splash_screen_LGTV_element = "//input[@type='file' and @id='splash-lgTv']"
    splash_screen_rokuTV_element = "//input[@type='file' and @id='splash-rokuTv']"
    splash_screen_SamsungTV_element = "//input[@type='file' and @id='splash-samsungTv']"
    splash_screen_FireTV_element = "//input[@type='file' and @id='splash-fireTv']"
    save_splash_screen_element ="//button[contains(normalize-space(.), 'Update Splash')]"



    def test_edit_splash_screen(self,browser_setup):
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
            print("App setting page is opened successfully")
            self.driver.execute_script("arguments[0].click();", Mobile)
            time.sleep(2)
            splash_menu =WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, self.splash_menu_element))
                )
            splash_menu.click()
        
        except Exception as e:
            print(f"Failed to open playout setting page: {e}")

        try:
            # ====== EDIT ELEMENT ======
            edit = WebDriverWait(self.driver, 130).until(
                EC.presence_of_element_located((By.XPATH, self.edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit)
            time.sleep(3)

            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.edit_element)
            actions.move_to_element(element_to_hover).perform()
            time.sleep(2)

            # ====== EDIT MENU ======
            WebDriverWait(self.driver, 130).until(
                EC.presence_of_element_located((By.XPATH, self.edit_menu))
            ).click()
            time.sleep(6)

            print(" Edit element and menu interaction succeeded.")
        
        except Exception as e:
            print(f" Failed to interact with edit element or menu: {e}")


        try:
            image1=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.splash_screen_ios_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image1)
            time.sleep(2)
            image1.send_keys(self.imageFile_path_9_16) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)
        
        try:
            splash_screen_andriod=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.splash_screen_andriod_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", splash_screen_andriod)
            time.sleep(2)
            splash_screen_andriod.send_keys(self.imageFile_path_9_16) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)
                
        try:
            splash_screen_andriodTv=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.splash_screen_andriodTv_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", splash_screen_andriodTv)
            time.sleep(2)
            splash_screen_andriodTv.send_keys(self.gifTvFile_path) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)

        try:
            splash_screen_LGTV=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.splash_screen_LGTV_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", splash_screen_LGTV)
            time.sleep(2)
            splash_screen_LGTV.send_keys(self.gifFile_path) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)

        try:
            splash_screen_rokuTV=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.splash_screen_rokuTV_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", splash_screen_rokuTV)
            time.sleep(2)
            splash_screen_rokuTV.send_keys(self.imageFile1280_720_path) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)
        
        try:
            splash_screen_SamsungTV=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.splash_screen_SamsungTV_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", splash_screen_SamsungTV)
            time.sleep(2)
            splash_screen_SamsungTV.send_keys(self.imageFile1280_720_path) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)

        try:
            splash_screen_FireTV=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.splash_screen_FireTV_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", splash_screen_FireTV)
            time.sleep(2)
            splash_screen_FireTV.send_keys(self.gifFile_path) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)

        try:
            save=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.save_splash_screen_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save)
            time.sleep(2)
            save.click() 
            time.sleep(5)
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
