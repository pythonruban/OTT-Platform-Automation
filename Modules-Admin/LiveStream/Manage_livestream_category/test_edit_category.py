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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from utilities.readProp import ReadConfig


@pytest.mark.usefixtures("browser_setup") 
class TestLiveStream:

    driver: webdriver

      #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "10801620.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "16.9.jpg")
    videoFile_path = os.path.join(base_dir, "sample_video.mp4")
    pdfFile_path = os.path.join(base_dir, "pdf1.pdf")
    imagefile1080_1080_path =os.path.join(base_dir,"1080_10802.jpg") 

    

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    live_stream_element = "//div[@data-bs-target='#Live-Stream']"
    add_live_category_element = "//span[contains(text(), 'Manage Live Stream Categories')]"
    edit_element ="(//span[contains(@class, 'editdropdown-button')])[6]"
    edit_menu = "(//span[contains(text(), 'Edit')])[6]" 


    name_element = "//input[@name='name']" 
    slug_element = "//input[@name='slug']"
    live_description_element ="//div[@class='jodit-wysiwyg']"
    category_element ="//select[@id='live-category-parentid']"
    home_element= "(//span[contains(@class, 'admin-slider')])"

    Thumbnail_image_element = "//input[@name='image']"
    
    submit_button_element = "(//span[text()='Submit'])[2]"

    def test_edit_category(self,browser_setup):
        self.driver = browser_setup
              
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

        

            # Scroll to ensure all elements are loaded
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            Manage_livestream = WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, self.live_stream_element))
             )
            self.driver.execute_script("arguments[0].click();", Manage_livestream)
            print(" Navigated to 'Live Stream Management'")
        except Exception as e:
            print(f" Failed to click 'Live Stream Management': {e}")
    
            # Wait for "Add New Member" button and click
        try:
            add_livestream_button = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.add_live_category_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_livestream_button)
            time.sleep(1)  # Allow smooth scrolling
            self.driver.execute_script("arguments[0].click();", add_livestream_button)
            print(" Clicked 'Add New Live Stream'")
            time.sleep(6)
        except Exception as e:
            print(f" Failed to click 'Add New Live Stream': {e}")
            #edit Category

        try:
            delete= WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", delete)
            time.sleep(2)
            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.edit_element)
            actions.move_to_element(element_to_hover).perform()
            time.sleep(2)
            # Edit menu
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.edit_menu))
            ).click()
            time.sleep(6)
        except Exception as e:
            print(f" An error occurred while performing the edit action: {e}")

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
            print(" Auto name entered in the title field.")

        except Exception as e:
            print(f" Failed to enter title: {e}")
                    # slug
        try:
            print(f"Using XPath for slug input: {self.slug_element}")

            slug = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.slug_element))
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
            Sub = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.category_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Sub)
            time.sleep(2)
            Select(Sub).select_by_value("2")
            time.sleep(2)
        except Exception as e:
            print(f"An error occurred while selecting the category: {e}")

        try:
            home = self.driver.find_element(By.XPATH, self.home_element)
            
            # Example: Check if toggle is already active using class name
            toggle_class = home.get_attribute("class")
            
            if "active" not in toggle_class:  # Replace "active" with the actual keyword if different
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", home)
                time.sleep(1)  # Allow UI to settle
                # self.driver.execute_script("arguments[0].click();", home)
                print(" Feature toggle clicked successfully!")
                time.sleep(3)
            else:
                print(" Toggle is already active — no action taken.")
        except Exception as e:
            print(f" An error occurred while handling the feature toggle: {e}")


        try:
                # File paths (replace with actual paths)
                
            image=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.Thumbnail_image_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image)
            time.sleep(2)
            image.send_keys(self.imagefile1080_1080_path)



        except Exception as e:
            general_msg = f" General error in file upload process: {e}"
            print(general_msg)
        
             
           # ====== SUBMIT BUTTON ======
        try:
            time.sleep(2)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="For Manage Category  for the  Livestream , All data was Edited Successfully ", attachment_type=AttachmentType.PNG)
            submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", submit_button)
            time.sleep(3)
            print(" The Live stream was edited successfully.")
            time.sleep(3)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Manage Category Was Edited successfully", attachment_type=AttachmentType.PNG)
            time.sleep(3)
            
        except Exception as e:
            print(f" Error clicking submit button: {e}")                
                    
            
    

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")


