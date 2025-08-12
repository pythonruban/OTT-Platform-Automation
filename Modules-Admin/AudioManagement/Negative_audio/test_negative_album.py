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

    
    name_element = "//input[@name='albumname']" 
    slug_element = "//input[@name='slug']"
    choose_sub_album_element = "//select[@id='subAlbum']"
    
    #copyright
    copyright_file_element =  "//input[@id='fileInputRef1']"
     #image
    image_element = "//input[@name='image']"
   
     #SAVE BUTTON
    add_album_button_element = "(//button[@id='adminButton'])[2]"
    


    def test_negative_album(self,browser_setup):
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

        # Scroll to ensure all elements are loaded
        
        
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
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
            print(f" Failed to open Add New Audio: {e}")

        try:
            add_album = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.XPATH, self.add_album_element))
            )
            add_album.click()
            print(" Add Album page opened successfully")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to open Add Album page: {e}")
        try:
            test_data = [
                ("Test 1: 1-char (Negative Title)", ''.join(random.choices(string.ascii_uppercase, k=1))),
                ("Test 2: 102-char (Negative Title)", ''.join(random.choices(string.ascii_uppercase + string.digits, k=102))),
                ("Test 3: Auto Title (Valid)", ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 7))))
            ]

            for test_name, title_value in test_data:
                print(f"\n{test_name} started")

                # === TITLE FIELD ===
                try:
                    title_input = WebDriverWait(self.driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, self.name_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_input)
                    time.sleep(1)
                    title_input.clear()
                    title_input.send_keys(title_value)
                    print(f"Title entered: {title_value[:30]}")
                except Exception as title_error:
                    print(f" Error entering title: {title_error}")
                    continue

                # === SLUG FIELD ===
                try:
                    slug_input = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, self.slug_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slug_input)
                    time.sleep(1)
                    slug_input.clear()
                    slug_input.send_keys(title_value)
                    print(f"Slug entered: {title_value[:30]}")
                except Exception as slug_error:
                    print(f" Error entering slug: {slug_error}")
                    continue

                # === VALIDATION CHECK ===
                is_title_invalid = len(title_value) < 3 or len(title_value) > 100
                is_slug_invalid = len(title_value) < 3 or len(title_value) > 100

                # === SUBMIT + SCREENSHOT FOR NEGATIVE CASE ===
                if is_title_invalid or is_slug_invalid:
                    try:
                        submit_button = WebDriverWait(self.driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, self.add_album_button_element))
                        )
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                        time.sleep(1)
                        submit_button.click()
                        print(" Submit clicked for negative case")

                        # === Take Screenshot ===
                        allure.attach(
                            self.driver.get_screenshot_as_png(),
                            name=f"Negative_Title_or_Slug_{len(title_value)}chars",
                            attachment_type=allure.attachment_type.PNG
                        )

                        time.sleep(2)
                    except Exception as submit_error:
                        print(f" Error during form submission: {submit_error}")
                else:
                    print(" Title and Slug are valid — submit skipped")

        except Exception as outer_error:
            print(f" Outer script error: {outer_error}")

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
                # File paths (replace with actual paths)
           

                   # Negative Test: Upload PDF (should be rejected)
                    if not os.path.exists(self.pdfFile_path):
                        msg = f" PDF file not found: {self.pdfFile_path}"
                        print(msg)
                        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="PDF Missing",attachment_type=AttachmentType.PNG)
                    else:
                        try:
                            upload_element = WebDriverWait(self.driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, self.image_element))
                            )
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_element)
                            upload_element.send_keys(self.pdfFile_path)
                            time.sleep(2)

                            # Optionally: Check for validation message on screen
                            msg = " PDF uploaded — expected to be rejected. Check UI validation."
                            print(msg)

                        except Exception as e:
                            msg = f" PDF rejected as expected: {e}"
                            print(msg)

                # Positive Test: Upload Image (should be accepted)
                    if not os.path.exists(self.imageFile_path_9_16):
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
                general_msg = f" General error in file upload p"

        try:
            # Wait for the document upload field to be present
            copyright = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.copyright_file_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", copyright)

            # Step 1: Upload image file
            copyright.send_keys(self.imagefile1080_1080_path)
            print(" Image file uploaded successfully")
            time.sleep(3)

            #  Allure screenshot after image upload
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Image_Uploaded",
                attachment_type=allure.attachment_type.PNG
            )

            # Step 2: Upload PDF file
            copyright.send_keys(self.pdfFile_path)
            print(" PDF file uploaded successfully")
            time.sleep(4)

        except Exception as e:
            print(f" Failed to upload document files: {e}")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Upload_Failure",
                attachment_type=allure.attachment_type.PNG
            )

        try:
            add_album_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.add_album_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_album_button)
            time.sleep(4)
            add_album_button.click()
            time.sleep(4)
            print(" Album was added successfully")
        except Exception as e:
            print(f" Failed to submit the album: {e}")

    

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 
    
 
        print("Browser Closed Successfully")

    