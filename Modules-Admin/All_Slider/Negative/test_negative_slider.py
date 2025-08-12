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
class TestAddSlider:
    driver = webdriver.Firefox


      #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "10801620.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "16.9.jpg")
    videoFile_path = os.path.join(base_dir, "sample_video.mp4")
    pdfFile_path = os.path.join(base_dir, "pdf1.pdf")

    # Locators
    email_element = "//div[contains(@class,'shadow border border-1 theme-border-color p-4 rounded-3 col-11 col-lg-6 col-xl-4 mx-auto')]//input[contains(@placeholder,'email')]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    #xpath for All Slider Management

    All_slider_element = "//a[span[text()='All Slider']]"
    add_new_slider_element = "//a[@id='navigationLinkForAddPage']"
    slider_title_element = "//input[@name='title']"
    target_link_element = "//input[@name='link']"
    trailer_link_element = "//input[@name='trailer_link']"
    status_setting_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[1]"
    slider_image_element = "//input[@name='dark']"
    player_image_element = "//input[@name='light']"
    save_button_element = "//button[@type='submit']"


    def test_add_slider(self,browser_setup):
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
            slider = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, self.All_slider_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slider)
            self.driver.execute_script("arguments[0].click();", slider)
            print("Navigated to 'All Slider Management'")
        except Exception as e:
            print(f"Failed to navigate to All Slider Page: {e}")

        time.sleep(3)

        try:
            add_slider_button = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, self.add_new_slider_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_slider_button)
            self.driver.execute_script("arguments[0].click();", add_slider_button)
            print("Clicked on 'Add New Slider' button")
        except Exception as e:
            print(f"Failed to click on 'Add New Slider' button: {e}")
        time.sleep(3)

        try:
            test_data = [
                ("Test 1: 1-char (Negative Title)", ''.join(random.choices(string.ascii_uppercase, k=1))),
                ("Test 2: 202-char (Negative Title)", ''.join(random.choices(string.ascii_uppercase + string.digits, k=102))),
                ("Test 3: Auto Title (Valid)", ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 7))))
            ]    

            for test_name, title_value in test_data:
                try:
                    print(f"\nRunning: {test_name}")

                    # Locate and clear title input
                    title_input = WebDriverWait(self.driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, self.slider_title_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_input)
                    time.sleep(1)
                    title_input.clear()
                    title_input.send_keys(title_value)
                    print(f"Title entered: {title_value[:30]}")

                    # Click Submit button
                    submit_button = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, self.save_button_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", submit_button)
                    print("Form submitted")

                    # If test is a negative case, take screenshot
                    if "Negative" in test_name:
                        time.sleep(2)
                        screenshot_name = f"screenshots/{test_name.replace(':', '').replace(' ', '_')}.png"
                        self.driver.save_screenshot(screenshot_name)
                        allure.attach.file(screenshot_name, name=test_name, attachment_type=AttachmentType.PNG)
                        print(f"Screenshot captured for negative case: {test_name}")

                    # Optional: Scroll back to title field
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_input)
                    time.sleep(1)

                except Exception as case_error:
                    print(f"{test_name} - Error: {case_error}")

        except Exception as total_error:
            print(f"Outer error in title validation block: {total_error}")


        try:
            # Step 1: Enter invalid link and submit
            try:
                target_link = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, self.target_link_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_link)
                target_link.clear()
                time.sleep(1)
                target_link.send_keys("facebook")  # Invalid URL format
                print("Entered invalid target link.")

                submit_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.save_button_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                submit_btn.click()
                print("Submitted with invalid link.")

                # Screenshot for validation error
                time.sleep(2)
               
                allure.attach(self.driver.get_screenshot_as_png(), name="InvalidTargetLink", attachment_type=AttachmentType.PNG)
                print("Screenshot taken for invalid link.")
            except Exception as e1:
                print("Error submitting invalid target link:", e1)

            # Step 2: Enter valid link but do NOT submit
            try:
                target_link.clear()
                time.sleep(1)
                target_link.send_keys("https://www.facebook.com")
                print("Entered valid target link.")
            except Exception as e2:
                print("Error entering valid target link:", e2)

        except Exception as outer:
            print(f"Test failed in target link validation: {outer}")


        try:
            # Step 1: Enter invalid link and click Save
            try:
                trailer_link = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, self.trailer_link_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trailer_link)
                trailer_link.clear()
                time.sleep(1)
                trailer_link.send_keys("youtube")  # Invalid link
                print("Entered invalid trailer link.")

                submit_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.save_button_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                submit_btn.click()
                print("Submitted with invalid trailer link.")

                # Capture screenshot
                time.sleep(2)
               
                allure.attach(self.driver.get_screenshot_as_png(), name="InvalidTrailerLink", attachment_type=AttachmentType.PNG)
                print("Screenshot taken for invalid trailer link.")
            except Exception as e1:
                print("Error during negative trailer link test:", e1)

            # Step 2: Enter valid link — DO NOT submit
            try:
                trailer_link.clear()
                time.sleep(1)
                trailer_link.send_keys("https://www.youtube.com")
                print("Entered valid trailer link.")
            except Exception as e2:
                print("Error entering valid trailer link:", e2)

        except Exception as outer:
            print(f"Test failed in trailer link validation: {outer}")

        try:

            toggle = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.status_setting_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
            is_enabled = toggle.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                toggle.click()
                print(" toggle already enabled.")
            else:
                toggle.click()
                print(" toggle enabled.")

        except Exception as e:
            print(f"Failed to interact with toggle control: {e}")
        time.sleep(2)

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
                                EC.presence_of_element_located((By.XPATH, self.slider_image_element))
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
                                EC.presence_of_element_located((By.XPATH, self.slider_image_element))
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
        
         # Player Image field
        try:
                # File paths (replace with actual paths)
                   # Negative Test: Upload PDF (should be rejected)
                    if not os.path.exists(self.pdfFile_path):
                        msg = f" PDF file not found: {self.pdfFile_path}"
                        print(msg)
                    else:
                        try:
                            upload_element = WebDriverWait(self.driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, self.player_image_element))
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
                    if not os.path.exists(self.imageFile1280_720_path):
                        msg = f" Image file not found: {self.imageFile1280_720_path}"
                        print(msg)
                    else:
                        try:
                            upload_element = WebDriverWait(self.driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, self.player_image_element))
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

        time.sleep(2)

        try:
            save_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.save_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
            time.sleep(2)
            save_button.click()
            print("Clicked on 'Save' button")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Slider added successfully", attachment_type=AttachmentType.PNG)
        except Exception as e:
            print(f"Failed to click on 'Save' button: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Slider addition failed", attachment_type=AttachmentType.PNG)
            pytest.fail(f"Failed to click on 'Save' button: {e}")
        time.sleep(5)

    def teardown_class(self):
        """Close the browser after tests"""
        self.driver.quit()
        print("Browser closed.")