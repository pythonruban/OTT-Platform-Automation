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

class TestLanguage:
   
    driver = webdriver.Firefox
      #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "temp")
    imageFile_path_9_16 = os.path.join(base_dir, "10801620.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "16.9.jpg")
    videoFile_path = os.path.join(base_dir, "sample_video.mp4")
    pdfFile_path = os.path.join(base_dir, "pdf1.pdf")
    imagefile1080_1080_path =os.path.join(base_dir,"1080.1080.jpg")

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
   
    Manage_language_element = "//span[text()='Manage Language']"
    language_element ="//a[span[text()='Language']]"
    add_language_element = "//span[text()='Add Language']"
    language_name_element = "//input[@name='name']"
    language_slug_element = "//input[@name='slug']"
    image_element ="//input[@name='dark']"
    save_language_element= "//span[text()='Save']"

    
    

    def test_Add_language(self,browser_setup):
        self.driver = browser_setup
        """Login to the admin panel"""
        # self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()

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
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name=" All required data was entered and login was successful", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="login_error", attachment_type=AttachmentType.PNG)
            print(f" Failed to enter email: {e}")
 
    
        
        try:
            
            # Locate and click 'Manage Language'
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print(" Scrolled to bottom of page")
                Manage_app = WebDriverWait(self.driver, 45).until(
                    EC.presence_of_element_located((By.XPATH, self.Manage_language_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Manage_app)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", Manage_app)
                print(" Clicked 'Language'")
                time.sleep(3)
            except Exception as e:
                print(f" Failed to click 'Language': {e}")

            # Click language dropdown
            try:
                WebDriverWait(self.driver, 130).until(
                    EC.element_to_be_clickable((By.XPATH, self.language_element))
                ).click()
                print(" Clicked language dropdown")
                time.sleep(2)
            except Exception as e:
                print(f" Failed to click language dropdown: {e}")

            # Click 'Add Language' button
            try:
                WebDriverWait(self.driver, 130).until(
                    EC.element_to_be_clickable((By.XPATH, self.add_language_element))
                ).click()
                print(" Clicked 'Add Language'")
                time.sleep(2)
            except Exception as e:
                print(f" Failed to click 'Add Language': {e}")

            # Enter Language Name
            try:
                # Generate a random uppercase string of length between 5 and 7
                length = random.randint(5, 7)
                auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
                print(f"Generated name: {auto_name}")

                print(f"Using XPath: {self.language_name_element}")

                # Wait for the title input to be clickable
                name = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, self.language_name_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
                time.sleep(2)
                name.clear()
                time.sleep(2)  # small delay to ensure field is cleared
                name.send_keys(auto_name)
                time.sleep(2)
                print(" Auto name entered in the title field.")

            except Exception as e:
                print(f" Failed to enter title: {e}")
            # Enter Slug
            try:
                print(f"Using XPath for slug input: {self.language_slug_element}")

                slug = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, self.language_slug_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slug)
                time.sleep(2)
                slug.clear()
                time.sleep(2)
                slug.send_keys(auto_name)
                time.sleep(2)
                print(" Auto slug entered using the name.")

            except Exception as e:
                print(f" Failed to enter slug: {e}")


            try:
                image=WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.image_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image)
                time.sleep(2)
                image.send_keys(self.imagefile1080_1080_path) 

            except Exception as e:
                    general_msg = f" General error in file upload process: {e}"
                    print(general_msg)

            try:
                submit_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, self.save_language_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                time.sleep(2)
                self.driver.execute_script("arguments[0].click();", submit_button)
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Save_button_Click_Success", attachment_type=AttachmentType.PNG)
                time.sleep(6)
                print(" The Language was added successfully.")
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name=" The new Language was Added successfully", attachment_type=AttachmentType.PNG)
                time.sleep(5)
            except Exception as e:
                print(f" Error clicking submit button: {e}") 
                raise AssertionError(f"Test failed due to: {e}")
            time.sleep(2)

           
        
        except Exception as e:
            print(f" Failed to click Language& Translation : {e}")
            pytest.fail(f"Login failed: {e}")

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")




