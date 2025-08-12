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

class TestAudioManagement:
    driver = webdriver.Firefox

    # Locators
      #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "10801620.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "16.9.jpg")
    videoFile_path = os.path.join(base_dir, "sample_video.mp4")
    pdfFile_path = os.path.join(base_dir, "pdf1.pdf")
    imagefile1080_1080_path =os.path.join(base_dir,"1080.1080.jpg")
    Audio1_file =os.path.join(base_dir,"Audio1.mp3")
    Audio2_file =os.path.join(base_dir,"Audio2.mp3")

    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    Audio_element = "//div[@data-bs-target='#Audio-Management']"
    Manage_album_element = "//span[contains(text(), 'Manage Albums')]"
    add_album_element ="//a[@id='navigationLinkForAddPage']"
    edit_element ="(//span[contains(@class, 'editdropdown-button')])[1]"
    edit_menu = "//span  [text()='Edit']"

    
    name_element = "//input[@name='albumname']" 
    slug_element = "//input[@name='slug']"
    choose_sub_album_element = "//select[@id='subAlbum']"
    
    copyright_file_element =  "//input[@id='fileInputRef1']"
    
     #image
    image_element = "//input[@name='image']"
   
     #SAVE BUTTON
    add_album_button_element = "(//button[@id='adminButton'])[2]" 
    


    def test_edit_album(self,browser_setup):
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
            Manage_audio = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, self.Audio_element))
            )
            self.driver.execute_script("arguments[0].click();", Manage_audio)
            print(" Navigated to 'Audio Management'")
        except Exception as e:
            print(f" Failed to click Audio Management: {e}")

        try:
            manage_album = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.Manage_album_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", manage_album)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", manage_album)
            print(" Clicked 'Add New Audio'")
            time.sleep(2)
        except Exception as e:
            print(f" Failed to click 'Add New Audio': {e}")

        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.edit_element))
            )
            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.edit_element)
            actions.move_to_element(element_to_hover).perform()
            time.sleep(2)
        except Exception as e:
            print(f" Failed to hover on edit icon: {e}")

        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.edit_menu))
            ).click()
            time.sleep(2)
        except Exception as e:
            print(f" Failed to click edit menu: {e}")

        try:
            # Generate a random uppercase string of length between 5 and 7
            length = random.randint(5, 7)
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")

            print(f"Using XPath: {self.title_element}")

            # Wait for the title input to be clickable
            name = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.title_element))
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

        try:
            slug = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.slug_element))
            )
            slug.clear()
            time.sleep(2)
            slug.send_keys(auto_name)
            time.sleep(3)
        except Exception as e:
            print(f" Failed to enter slug: {e}")

        try:
            choose_sub = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.choose_sub_album_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", choose_sub)
            Select(choose_sub).select_by_value("1")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to select sub-album: {e}")

        try:
            image = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.image_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image)
            image.send_keys(self.imagefile1080_1080_path)
            time.sleep(2)
        except Exception as e:
            print(f" Failed to upload image: {e}")

        try:
            copyright = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.copyright_file_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", copyright)
            copyright.send_keys(self.pdfFile_path)
            time.sleep(4)
        except Exception as e:
            print(f" Failed to upload copyright file: {e}")
        try:
            add_album_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.add_album_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_album_button)
            time.sleep(4)
            add_album_button.click()
            time.sleep(4)
            print(" Album was added successfully")
            allure.attach(self.driver.get_full_page_screenshot_as_png(),
                        name="Album_Submission_Success",
                        attachment_type=AttachmentType.PNG)
            time.sleep(3)
        except Exception as e:
            print(f" Failed to submit the album: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(),
                        name="Album_Submission_Failure",
                        attachment_type=AttachmentType.PNG)

        

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 
    
 
        print("Browser Closed Successfully")

    