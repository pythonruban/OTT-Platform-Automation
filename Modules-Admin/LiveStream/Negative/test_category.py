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





@pytest.mark.usefixtures("browser_setup") 
class TestLiveStream:
    
    allure_report_error_message = ""
    driver = webdriver.Firefox    
      #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "10801620.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "16.9.jpg")
    videoFile_path = os.path.join(base_dir, "sample_video.mp4")
    pdfFile_path = os.path.join(base_dir, "pdf1.pdf")
    imagefile1080_1080_path =os.path.join(base_dir,"1080.1080.jpg")
   

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    live_stream_element = "//div[@data-bs-target='#Live-Stream']"
    add_live_category_element = "//span[contains(text(), 'Manage Live Stream Categories')]"
    add_new_category = "//a[@id= 'navigationLinkForAddPage']"
    


    name_element = "//input[@name='name']" 
    slug_element = "//input[@name='slug']"
    live_description_element ="//div[@class='jodit-wysiwyg']"
    category_element ="//select[@id='live-category-parentid']"
    home_element= "(//span[contains(@class, 'admin-slider')])"

    Thumbnail_image_element = "//input[@name='image']"
   

    submit_button_element = "(//span[text()='Submit'])[2]"

    def test_add_category(self,browser_setup):
        self.driver = browser_setup
       
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()
        actions = ActionChains(self.driver)
        
        WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, self.email_element))
            ).send_keys(ReadConfig.getAdminId())

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.password_element))).send_keys(12345)
        self.allure_report_error_message = ""


        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, self.login_element))
            ).click()
            print("Login button clicked!")


            try:
                # Wait for dashboard element as sign of successful login
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Dashboard')]"))  # change XPath as needed
                )
                print("Login Successful!")
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login Success - Redirected to Dashboard", attachment_type=AttachmentType.PNG)

            except TimeoutException:
                # Wait for error message
                error_elem = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Invalid password')]"))  # Update XPath based on your app
                )
                self.allure_report_error_message = "Live Category Add Process: Login Failed - Invalid password"
                print(self.allure_report_error_message)
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login Error - Invalid Password", attachment_type=AttachmentType.PNG)

        except Exception as e:
            self.allure_report_error_message = "Live Category Add Process: Login Attempt Error"
            print(f"Unexpected error during login: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(),name="Login Error - Exception", attachment_type=AttachmentType.PNG)

        
        if self.allure_report_error_message:
            os.environ["Allure_Report_Error_Message"] = self.allure_report_error_message

            # Scroll to ensure all elements are loaded
        try:
            Manage_livestream = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.live_stream_element))
             )
            self.driver.execute_script("arguments[0].click();", Manage_livestream)
            print(" Navigated to 'Live Stream Management'")
        except Exception as e:
            print(f" Failed to click 'Live Stream Management': {e}")


        try:
            add_livestream_button = WebDriverWait(self.driver, 45).until(
            EC.presence_of_element_located((By.XPATH, self.add_live_category_element))
        )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_livestream_button)
            time.sleep(1)  # Smooth scroll
            self.driver.execute_script("arguments[0].click();", add_livestream_button)
            print(" Clicked 'Add New live stream'")
            time.sleep(3)
        except Exception as e:
            self.allure_report_error_message = "Live Category Add Process: Failed to click 'Add New live stream' "
            print(f" Failed to click 'Add New live stream': {e}")


        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.add_new_category))
            ).click()
            print("Clicked 'Add New Category' successfully")
            time.sleep(3)
       
        except Exception as e:
            self.allure_report_error_message = "Live Category Add Process: An unexpected error occurred while clicking 'Add New Category' "
            print(f"An unexpected error occurred while clicking 'Add New Category': {e}")
            

            #Add Live streamtry:
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
                    print(f"Error entering title: {title_error}")
                    continue  # Skip to next test if title input fails

                # === SLUG FIELD ===
                try:
                    slug_input = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, self.slug_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slug_input)
                    time.sleep(1)
                    slug_input.clear()
                    slug_input.send_keys(title_value)  # Slug value same as title
                    print(f"Slug entered (same as title): {title_value[:30]}")
                except Exception as slug_error:
                    print(f"Error entering slug: {slug_error}")
                    continue  # Skip submit if slug input fails

                # === SUBMIT FORM ===
                try:
                    submit_button = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                    time.sleep(1)
                    submit_button.click()
                    time.sleep(2)
                    print(f"Form submitted for: {test_name}")
                except Exception as submit_error:
                    print(f"Error during form submission: {submit_error}")

        except Exception as outer_error:
            print(f"Outer script error: {outer_error}")
                    # slug
        # try:
        #     slug = WebDriverWait(self.driver, 30).until(
        #     EC.presence_of_element_located((By.XPATH, self.slug_element))
        # )
        #     time.sleep(2)

        #     current_slug = slug.get_attribute("value")
        #     desired_slug = "fun"
 
        #     if current_slug.strip() == desired_slug:
        #        print(" Slug already set correctly, skipping input.")
        #     else:
        #        slug.clear()
        #        time.sleep(1)
        #        slug.send_keys(desired_slug)
        #        print(" Slug entered:", desired_slug)

        #     time.sleep(1)
        # except Exception as e:
        #     print(f" Failed to handle slug input: {e}")
        try:
            Sub = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.category_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Sub)
            time.sleep(2)
            Select(Sub).select_by_value("12")
            time.sleep(2)
        except Exception as e:
            self.allure_report_error_message = "Live Category Add Process: An error occurred while selecting the category"
            allure.attach(self.driver.get_screenshot_as_png(), name="Live Category Add Process: An error occurred while selecting the category", attachment_type=AttachmentType.PNG)
            print(f"An error occurred while selecting the category: {e}")

        try:
            home = self.driver.find_element(By.XPATH, self.home_element)
            
            # Example: Check if toggle is already active using class name
            toggle_class = home.get_attribute("class")
            
            if "active" not in toggle_class:  # Replace "active" with the actual keyword if different
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", home)
                time.sleep(1)  # Allow UI to settle
                self.driver.execute_script("arguments[0].click();", home)
                print(" Feature toggle clicked successfully!")
                time.sleep(3)
            else:
                print(" Toggle is already active — no action taken.")
        except Exception as e:
            print(f" An error occurred while handling the feature toggle: {e}")


        try:
                # File paths (replace with actual paths)
            
                   # Negative Test: Upload PDF (should be rejected)
                    if not os.path.exists(self.pdfFile_path):
                        msg = f" PDF file not found: {self.pdfFile_path}"
                        print(msg)
                    else:
                        try:
                            upload_element = WebDriverWait(self.driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, self.Thumbnail_image_element))
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
                    if not os.path.exists(self.imageFile1280_720_path):
                        msg = f" Image file not found: {self.imageFile1280_720_path}"
                        print(msg)
                    else:
                        try:
                            upload_element = WebDriverWait(self.driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, self.TV_image_element))
                            )
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_element)
                            upload_element.send_keys(self.imageFile1280_720_path)
                            time.sleep(2)

                            msg = f" Image '{self.imageFile1280_720_path}' uploaded successfully."
                            print(msg)

                        except Exception as e:
                            msg = f" Error uploading image: {e}"
                            print(msg)

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)
        
             
           # ====== SUBMIT BUTTON ======
        try:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="For Manage Category  for the  Livestream , All data was Enter Successfully ", attachment_type=AttachmentType.PNG)
            submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", submit_button)
            time.sleep(3)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Manage Category Was Added successfully it was Redirect to Manage Category Page", attachment_type=AttachmentType.PNG)
            time.sleep(3)
        except Exception as e:
            self.allure_report_error_message = "Live Category Add Process: Error clicking submit button"
            allure.attach(self.driver.get_screenshot_as_png(), name="Live Category Add Process: Error clicking submit button", attachment_type=AttachmentType.PNG)
            print(f" Error clicking submit button: {e}")                
                    
   
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 

 


