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

     #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "10801620.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "16.9.jpg")
    videoFile_path = os.path.join(base_dir, "sample_video.mp4")
    pdfFile_path = os.path.join(base_dir, "pdf1.pdf")  

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    Settings_element = "//div[@data-bs-target='#Settings']"
    apps_elemnt ="//span[text()='Apps']"
    android_app_elemnt ="//button[@id='pills-App-tab']"
    name_element ="//input[@id='app_name']"
    package_name_element = "//input[@name ='otp_24x7sms_sender_id']"
    app_icon_elemnt = "//input[@name='app_icon']"
    Android_TV_element = "//button[@id='pills-TV-tab']"
    Fire_Tv_element = "//button[@id='pills-Fire-tab']"
    LG_Tv_element = "//button[@id='pills-LG-tab']"
    submit_element = "//button[@id='adminButton']"
    
    def test_app(self,browser_setup):
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
            apps = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.apps_elemnt))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", apps)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", apps)
            print("Navigated to 'apps'")
        except Exception as e:
            print(f"[ERROR] Clicking  failed: {e}")

        try:
            android_app = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.android_app_elemnt))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", android_app)
            time.sleep(1)
            android_app.click()
            time.sleep(2)
            try:
                # Generate a random uppercase string of length between 5 and 7
                length = random.randint(5, 7)
                auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
                print(f"Generated name: {auto_name}")

                print(f"Using XPath: {self.name_element}")

                # Wait for the title input to be clickable
                name = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, self.name_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
                time.sleep(2)
                name.clear()
                time.sleep(2)  # small delay to ensure field is cleared
                name.send_keys(auto_name)
                time.sleep(2)
                print(" Auto name entered in the name field.")

                package_name= WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, self.name_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
                time.sleep(2)
                package_name.clear()
                time.sleep(2)  # small delay to ensure field is cleared
                package_name.send_keys( "vod_admin_automation")
                time.sleep(2)
                print("  name entered in the package_name field.")

                icon =WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.app_icon_elemnt))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", icon)
                time.sleep(2)
                icon.send_keys(self.imageFile_path_9_16)

            except Exception as e:
                print(f" Failed to enter : {e}")
            
        except Exception as e:
            print(f" Error handling : {e}")

        try:
            submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_element))
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
    #Android_TV
        try:
            Android_TV = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.XPATH, self.Android_TV_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Android_TV)
            time.sleep(1)
            Android_TV.click()
            time.sleep(2)
            try:
                # Generate a random uppercase string of length between 5 and 7
                length = random.randint(5, 7)
                auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
                print(f"Generated name: {auto_name}")

                print(f"Using XPath: {self.name_element}")

                # Wait for the title input to be clickable
                name = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, self.name_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
                time.sleep(2)
                name.clear()
                time.sleep(2)  # small delay to ensure field is cleared
                name.send_keys(auto_name)
                time.sleep(2)
                print(" Auto name entered in the name field.")

                package_name= WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, self.name_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
                time.sleep(2)
                package_name.clear()
                time.sleep(2)  # small delay to ensure field is cleared
                package_name.send_keys( "vod_admin_automation")
                time.sleep(2)
                print("  name entered in the package_name field.")

                icon =WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.app_icon_elemnt))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", icon)
                time.sleep(2)
                icon.send_keys(self.imageFile_path_9_16)

            except Exception as e:
                print(f" Failed to enter : {e}")
            
        except Exception as e:
            print(f" Error handling : {e}")

        try:
            submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_element))
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
        #Fire_TV
        try:
            Fire_TV = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.Fire_Tv_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Fire_TV)
            time.sleep(1)
            Fire_TV.click()
            time.sleep(2)
            try:
                # Generate a random uppercase string of length between 5 and 7
                length = random.randint(5, 7)
                auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
                print(f"Generated name: {auto_name}")

                print(f"Using XPath: {self.name_element}")

                # Wait for the title input to be clickable
                name = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, self.name_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
                time.sleep(2)
                name.clear()
                time.sleep(2)  # small delay to ensure field is cleared
                name.send_keys(auto_name)
                time.sleep(2)
                print(" Auto name entered in the name field.")

                package_name= WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, self.name_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
                time.sleep(2)
                package_name.clear()
                time.sleep(2)  # small delay to ensure field is cleared
                package_name.send_keys( "vod_admin_automation")
                time.sleep(2)
                print("  name entered in the package_name field.")

                icon =WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.app_icon_elemnt))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", icon)
                time.sleep(2)
                icon.send_keys(self.imageFile_path_9_16)

            except Exception as e:
                print(f" Failed to enter : {e}")
            
        except Exception as e:
            print(f" Error handling : {e}")

        try:
            submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_element))
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
        #LG_TV 
        try:
            LG_TV = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.LG_Tv_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", android_app)
            time.sleep(1)
            LG_TV.click()
            time.sleep(2)
            try:
                # Generate a random uppercase string of length between 5 and 7
                length = random.randint(5, 7)
                auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
                print(f"Generated name: {auto_name}")

                print(f"Using XPath: {self.name_element}")

                # Wait for the title input to be clickable
                name = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, self.name_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
                time.sleep(2)
                name.clear()
                time.sleep(2)  # small delay to ensure field is cleared
                name.send_keys(auto_name)
                time.sleep(2)
                print(" Auto name entered in the name field.")

                package_name= WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, self.name_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
                time.sleep(2)
                package_name.clear()
                time.sleep(2)  # small delay to ensure field is cleared
                package_name.send_keys( "vod_admin_automation")
                time.sleep(2)
                print("  name entered in the package_name field.")

                icon =WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.app_icon_elemnt))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", icon)
                time.sleep(2)
                icon.send_keys(self.imageFile_path_9_16)

            except Exception as e:
                print(f" Failed to enter : {e}")
            
        except Exception as e:
            print(f" Error handling : {e}")

        try:
            submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", submit_button)
            print(" OIP Credential was save successfully.")
            time.sleep(6)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name=".",attachment_type=AttachmentType.PNG)
            time.sleep(2)
        except Exception as e:
            print(f" Error clicking submit button: {e}")

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  