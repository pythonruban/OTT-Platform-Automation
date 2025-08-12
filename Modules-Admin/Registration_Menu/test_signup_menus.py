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
class TestRegistrationMenu:
    driver = webdriver.Firefox

    # Locators
    email_element = "//div[contains(@class,'shadow border border-1 theme-border-color p-4 rounded-3 col-11 col-lg-6 col-xl-4 mx-auto')]//input[contains(@placeholder,'email')]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    register_menu_element = "//div[@data-bs-target='#RegistrationMenu']"
    signup_menu_element = "//span[normalize-space(text())='Signup Menus']"
    #xpath
    Profile_name_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[1]"
    Profile_email_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[2]"
    profile_mobile_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[3]"
    profile_image_element ="(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[4]"
    profile_password_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[5]"
    profile_password_cofrim_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[6]"
    profile_DOB_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[7]"
    Region_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[8]"
    profile_support_username_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[9]"
    Gender_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[10]"
    Submit_element = "//button[span[text()='Submit']]"


    def test_signup_menus(self,browser_setup):
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


    
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            Regsister = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, self.register_menu_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Regsister)
            self.driver.execute_script("arguments[0].click();", Regsister)
            print("Navigated to 'Registration Menu Management'")
        except Exception as e:
            print(f"Failed to navigate to Regsister Menu Page: {e}")

        time.sleep(3)

        try:
            
            Signup = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, self.signup_menu_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Signup)
            self.driver.execute_script("arguments[0].click();", Signup)
            print("Navigated to 'Sigup  Management'")
        except Exception as e:
            print(f"Failed to navigate to Signup Menu Page: {e}")

        time.sleep(3)

        try:
            Profile_name = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Profile_name_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Profile_name)
            is_enabled = Profile_name.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Profile_name toggle already enabled.")
            else:
                Profile_name.click()
                print("Profile_name toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with Profile_name control: {e}")
        time.sleep(2)

        try:

            Profile_email = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Profile_email_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Profile_email)
            is_enabled = Profile_email.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Profile_email toggle already enabled.")
            else:
                Profile_email.click()
                print("Profile_email toggle enabled.")

        except Exception as e:
            print(f"Failed to interact with Profile_email control: {e}")
        time.sleep(2)

        try:

            profile_mobile = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.profile_mobile_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", profile_mobile)
            is_enabled = profile_mobile.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("profile_mobile toggle already enabled.")
            else:
                profile_mobile.click()
                print("profile_mobile toggle enabled.") 
        except Exception as e:
            print(f"Failed to interact with profile_mobile control: {e}")
        time.sleep(2)

        try:

            profile_image = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.profile_image_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", profile_image)
            is_enabled = profile_image.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("profile_image toggle already enabled.")
            else:
                profile_image.click()
                print("profile_image toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with profile_image control: {e}")
        time.sleep(2)

        try:
            profile_password = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.profile_password_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", profile_password)
            is_enabled = profile_password.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("profile_password toggle already enabled.")
            else:
                profile_password.click()
                print("profile_password toggle enabled.")
        
        except Exception as e:
            print(f"Failed to interact with Voluprofile_passwordme control: {e}")
        time.sleep(2)

        try:

            profile_password_cofrim = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.profile_password_cofrim_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", profile_password_cofrim)
            is_enabled = profile_password_cofrim.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("profile_password_cofrim toggle already enabled.")
            else:
                profile_password_cofrim.click()
                print("profile_password_cofrim toggle enabled.")
        except Exception as e:  
            print(f"Failed to interact with profile_password_cofrim control: {e}")
        time.sleep(2)

        try:
            profile_DOB = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.profile_DOB_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", profile_DOB)
            is_enabled = profile_DOB.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                profile_DOB.click()
                print("profile_DOB toggle already enabled.")
            else:
                print("profile_DOB toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with profile_DOB control: {e}")
        time.sleep(2)

        try:
            Region = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Region_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Region)
            is_enabled = Region.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Volume toggle already enabled.")
            else:
                Region.click()
                print("Volume toggle enabled.")
        
        except Exception as e:
            print(f"Failed to interact with Region control: {e}")
        time.sleep(2)

        try:
            profile_support_username = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.profile_support_username_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", profile_support_username)
            is_enabled = profile_support_username.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Volume toggle already enabled.")
            else:
                profile_support_username.click()
                print("Volume toggle enabled.")
        
        except Exception as e:
            print(f"Failed to interact with profile_support_username control: {e}")
        time.sleep(2)

        try:

            Gender = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Gender_element)) 
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center]);", Gender)
            is_enabled = Gender.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Gender toggle already enabled.") 
            else:
                Gender.click()
                print("Gender toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with Gender control: {e}")
        time.sleep(2)


        try:
            Submit = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Submit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Submit)
            time.sleep(2)
            Submit.click()
            print("Submit button clicked successfully.")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="In registration page all Toggle was checked and Submit button was clicked successfully", attachment_type=AttachmentType.PNG)
        except Exception as e:

            print(f"Failed to click Submit button: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="submit_error", attachment_type=AttachmentType.PNG)
            time.sleep(3)
            pytest.fail("Test failed due to an error in the Signup Menus test case.")


    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 
