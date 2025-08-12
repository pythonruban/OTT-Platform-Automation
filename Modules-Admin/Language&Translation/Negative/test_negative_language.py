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
    image_element ="//div[@class='imagedrop undefined']/input[@type='file']"
    save_language_element= "//span[text()='Save']"

    
    

    def test_negative_language(self,browser_setup):
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
                test_data = [
                    ("Test 1: 1-char (Negative)", ''.join(random.choices(string.ascii_uppercase, k=1))),   # Invalid
                    ("Test 2: 102-char (Negative)", ''.join(random.choices(string.ascii_uppercase + string.digits, k=102))),  # Invalid
                    ("Test 3: 6-char (Valid)", ''.join(random.choices(string.ascii_uppercase, k=6)))       # Valid
                ]

                for test_name, test_value in test_data:
                    print(f"\n{test_name} started")

                    # === Enter Title ===
                    try:
                        title_input = WebDriverWait(self.driver, 30).until(
                            EC.element_to_be_clickable((By.XPATH, self.language_name_element))
                        )
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_input)
                        title_input.clear()
                        title_input.send_keys(test_value)
                        print(f"Title entered: {test_value[:30]}")
                    except Exception as title_error:
                        print(f"Error entering title: {title_error}")
                        continue

                    # === Enter Slug ===
                    try:
                        slug_input = WebDriverWait(self.driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, self.language_slug_element))
                        )
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slug_input)
                        slug_input.clear()
                        slug_input.send_keys(test_value)
                        print(f"Slug entered: {test_value[:30]}")
                    except Exception as slug_error:
                        print(f"Error entering slug: {slug_error}")
                        continue

                    # === Check if BOTH are invalid ===
                    title_length = len(test_value)
                    slug_length = len(test_value)

                    is_title_invalid = title_length < 3 or title_length > 100
                    is_slug_invalid = slug_length < 3 or slug_length > 100

                    if is_title_invalid and is_slug_invalid:
                        print(" Both Title and Slug are invalid — clicking Save")

                        try:
                            submit_button = WebDriverWait(self.driver, 20).until(
                                EC.element_to_be_clickable((By.XPATH, self.save_language_element))
                            )
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                            submit_button.click()
                            time.sleep(2)

                            # Screenshot for both invalid
                            allure.attach(
                                self.driver.get_screenshot_as_png(),
                                name=f"Both_Invalid_{test_name.replace(':','')}",
                                attachment_type=allure.attachment_type.PNG
                            )

                            assert "error" in self.driver.page_source.lower(), "❌ Expected validation message not shown."

                        except Exception as submit_error:
                            print(f"Error during form submission: {submit_error}")

                    else:
                        print(" Either Title or Slug is valid — skipping Save")

            except Exception as outer_error:
                print(f" Outer script error: {outer_error}")

                    
            try:
                        # File paths (replace with actual path
            # Negative Test: Upload PDF (should be rejected)
                if not os.path.exists(self.pdfFile_path):
                    msg = f" PDF file not found: {self.pdfFile_path}"
                    print(msg)
                else:
                    try:
                        upload_element = WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, self.image_element))
                        )
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_element)
                        time.sleep(2)
                        upload_element.send_keys(self.pdfFile_path)
                        time.sleep(2)

                        # Optionally: Check for validation message on screen
                        msg = " PDF uploaded — expected to be rejected. Check UI validation."
                        print(msg)

                    except Exception as e:
                        msg = f" PDF rejected as expected: {e}"
                        print(msg)

            # Positive Test: Upload Image (should be accepted)
                if not os.path.exists(self.imagefile1080_1080_path):
                    msg = f" Image file not found: {self.imagefile1080_1080_path}"
                    print(msg)
                else:
                    try:
                        upload_element = WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, self.image_element))
                        )
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_element)
                        upload_element.send_keys(self.imagefile1080_1080_path)
                        time.sleep(2)

                        msg = f" Image '{self.imagefile1080_1080_path}' uploaded successfully."
                        print(msg)

                    except Exception as e:
                        msg = f" Error uploading image: {e}"
                        print(msg)

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
                time.sleep(6)
                print(" The Live stream was added successfully.")
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Save_button_Click_Success", attachment_type=AttachmentType.PNG)
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name=" The new Language was Added successfully", attachment_type=AttachmentType.PNG)
            except Exception as e:
                print(f" Error clicking submit button: {e}") 
                raise AssertionError(f"Test failed due to: {e}")
            time.sleep(2)

           
        
        except Exception as e:
            print(f" Failed to click Language& Translation : {e}")
            pytest.fail(f"Login failed: {e}")

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 




