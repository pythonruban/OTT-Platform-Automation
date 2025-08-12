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
class TestPlayerSetting:
    
    driver = webdriver.Firefox


     #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "10801620.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "16.9.jpg")
    videoFile_path = os.path.join(base_dir, "sample_video.mp4")
    pdfFile_path = os.path.join(base_dir, "pdf1.pdf")


    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    video_player_element = "//span[text()='Video Player Settings']"
    #Player Settings

    top_element = "//input[@name='watermark_top']" 
    bottom_element = "//input[@name='watermark_bottom']"
    left_element = "//input[@name='watermark_left']"
    right_element ="//input[@name='watermark_right']"
    #toogle button
    skip_intro_element ="(//span[contains(@class, 'admin-slider') ])[1]"
    Show_logos_element ="(//span[contains(@class, 'admin-slider') ])[2]"
    Add_Watermark_element ="(//span[contains(@class, 'admin-slider') ])[3]"
    Playback_speed_element ="(//span[contains(@class, 'admin-slider') ])[4]"

    opacity_element ="//input[@name='watermark_opacity']"
    Link_element ="//input[@name='watermar_link']"
    width_element="//input[@name='watermar_width']"
    #image upload   
    logo_image_element= "//input[@id='watermark_logo']"
    player_thumbnail_element = "//input[@id='player_thumbnail']"

    #subtitle toggle
    subtitle_toggle_element ="(//span[contains(@class, 'admin-slider') ])[5]"

    upload_player_element = "(//span[text()='Update Player'])[2]"
    def test_video_palyer_setting(self,browser_setup):
        self.driver = browser_setup
       
        """Login to the admin panel"""
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()
        action = ActionChains(self.driver)
        
        try:
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
                Player_setting = WebDriverWait(self.driver, 50).until(
                    EC.element_to_be_clickable((By.XPATH, self.video_player_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Player_setting)
                self.driver.execute_script("arguments[0].click();", Player_setting)
                print(" Navigated to 'Player Setting Management '")
            except Exception as e:
                print(f"Failed to click Player Setting: {e}")
            time.sleep(3)

            # Top
            try:
                top = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.top_element)))
                top.clear()
                time.sleep(2)
                top.send_keys("100")
            except Exception as e:
                print(f"Error interacting with Top field: {e}")
            time.sleep(2)

            # Bottom
            try:
                bottom = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.bottom_element)))
                bottom.clear()
                time.sleep(2)
                bottom.send_keys("200")
            except Exception as e:
                print(f"Error interacting with Bottom field: {e}")
            time.sleep(2)

            # Left
            try:
                left = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.left_element)))
                left.clear()
                time.sleep(2)
                left.send_keys("12")
            except Exception as e:
                print(f"Error interacting with Left field: {e}")
            time.sleep(2)

            # Right
            try:
                right = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.right_element)))
                right.clear()
                time.sleep(2)
                right.send_keys("100")
            except Exception as e:
                print(f"Error interacting with Right field: {e}")
            time.sleep(2)

            # Toggle 1
            try:
                toggle1 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.skip_intro_element)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1)
                is_enabled = toggle1.get_attribute("aria-pressed") == "true"
                if not is_enabled:
                    print("toggle1 already enabled.")
                else:
                    toggle1.click()
                    print("toggle1 enabled.")
            except Exception as e:
                print(f"Failed to interact with toggle1: {e}")
            time.sleep(2)

            
            # Toggle 3
            try:
                toggle3 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.Show_logos_element)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3)
                is_enabled = toggle3.get_attribute("aria-pressed") == "true"
                if not is_enabled:
                    print("toggle3 already enabled.")
                else:
                    toggle3.click()
                    print("toggle3 enabled.")
            except Exception as e:
                print(f"Failed to interact with toggle3: {e}")
            time.sleep(2)

            # Toggle 4
            try:
                toggle4 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.Add_Watermark_element)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle4)
                is_enabled = toggle4.get_attribute("aria-pressed") == "true"
                if not is_enabled:
                    print("toggle4 already enabled.")
                else:
                    toggle4.click()
                    print("toggle4 enabled.")
            except Exception as e:
                print(f"Failed to interact with toggle4: {e}")
            time.sleep(2)

            # Toggle 5
            try:
                toggle5 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.Playback_speed_element)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle5)
                is_enabled = toggle5.get_attribute("aria-pressed") == "true"
                if not is_enabled:
                    print("toggle5 already enabled.")
                else:
                    toggle5.click()
                    print("toggle5 enabled.")
                # Playback speed input
                try:
                    playback = self.driver.find_element(By.XPATH, "(//input[@type='text' and @aria-autocomplete='list'])[1]")
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", playback)
                    self.driver.execute_script("arguments[0].click();", playback)
                    
                    for _ in range(10):  # adjust count based on how many selections are expected
                        playback.send_keys(Keys.BACKSPACE)
                        time.sleep(0.5)

                    options_to_select = ["0.5", "1", "1.25","1.5" ,"1.75", "2"]
                    for option in options_to_select:

                        playback.send_keys(option)
                        time.sleep(1)
                        playback.send_keys(Keys.RETURN)
                        time.sleep(2)
                except Exception as e:
                    print(f"Playback speed setting failed: {e}")
            except Exception as e:
                print(f"Failed to interact with toggle5: {e}")
            time.sleep(2)

            # Toggle 6
            try:
                toggle6 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.subtitle_toggle_element)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle6)
                is_enabled = toggle6.get_attribute("aria-pressed") == "true"
                if not is_enabled:
                    print("toggle6 already enabled.")
                else:
                    toggle6.click()
                    print("toggle6 enabled.")
            except Exception as e:
                print(f"Failed to interact with toggle6: {e}")
            time.sleep(2)

            

            try:
            
                others_control = self.driver.find_element(By.XPATH, "(//input[@type='text' and @aria-autocomplete='list'])[2]")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", others_control)
                self.driver.execute_script("arguments[0].click();", others_control)

                # Clear using JavaScript to set value directly
                for _ in range(10):  # adjust count based on how many selections are expected
                    others_control.send_keys(Keys.BACKSPACE)
                    time.sleep(0.5)

                options_to_select = ["Speed",  "Quality"]
                for option in options_to_select:
                    others_control.send_keys(option)
                    time.sleep(1)
                    others_control.send_keys(Keys.RETURN)
                    time.sleep(5)
            except Exception as e:
                print(f"Other Controls speed setting failed: {e}")

            # Opacity
            try:
                # Wait for and scroll to opacity input
                opacity = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.opacity_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", opacity)
                time.sleep(1)

                # Clear via JS in case .clear() fails
                self.driver.execute_script("arguments[0].value = '';", opacity)
                opacity.send_keys("100000")
                print("Entered invalid opacity value.")

                # Submit the form
                submit_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.upload_player_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                
                try:
                    submit_btn.click()
                except:
                    self.driver.execute_script("arguments[0].click();", submit_btn)

                print("Submitted with invalid opacity.")
                time.sleep(2)

                allure.attach(self.driver.get_screenshot_as_png(), name="InvalidOpacity", attachment_type=AttachmentType.PNG)
                print("Screenshot attached for invalid opacity.")

            except Exception as e:
                print(f"Error during invalid opacity test: {e}")

            # Step 2: Enter valid opacity (no submit)
            try:
                opacity = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.opacity_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", opacity)
                time.sleep(1)
                self.driver.execute_script("arguments[0].value = '';", opacity)
                opacity.send_keys("1")
                print("Entered valid opacity value.")
            except Exception as e:
                print(f"Error entering valid opacity: {e}")

            # Link Field - Invalid Input
            try:
                link_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.Link_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link_input)
                link_input.clear()
                link_input.send_keys("invalid-link")  # Invalid format

                # Wait for proper button (not span)
                submit_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.upload_player_element))
                )

                # JS click to avoid layout issues
                try:
                    submit_btn.click()
                except:
                    self.driver.execute_script("arguments[0].click();", submit_btn)

                print("Submitted with invalid link.")

                time.sleep(2)
                allure.attach(self.driver.get_screenshot_as_png(), name="InvalidLink", attachment_type=AttachmentType.PNG)

            except Exception as e:
                print(f"Error during invalid link test: {e}")
                        # Link Field - Valid Input (No Submit)
            try:
                link = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.Link_element))
                )
                link.clear()
                time.sleep(1)
                link.send_keys("https://flicknexs.com")
                print("Entered valid link.")
            except Exception as e:
                print(f"Error entering valid link: {e}")
            # Width
            try:
                width =WebDriverWait(self.driver, 10).until(
                
                    EC.presence_of_element_located((By.XPATH, self.width_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", width)
                time.sleep(2)
                width.clear()
                time.sleep(2)
                width.send_keys("200")
            except Exception as e:
                print(f"Failed to set Width: {e}")
            time.sleep(2)

            # Logo Image
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
                                    EC.presence_of_element_located((By.XPATH, self.logo_image_element))
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
                            msg = f" Image file not found: {self.imageFile_path_9_16}"
                            print(msg)
                        else:
                            try:
                                upload_element = WebDriverWait(self.driver, 20).until(
                                    EC.presence_of_element_located((By.XPATH, self.logo_image_element))
                                )
                                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_element)
                                upload_element.send_keys(self.imageFile_path_9_16)
                                time.sleep(2)

                                msg = f" Image '{self.imageFile_path_9_16}' uploaded successfully."
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
                                    EC.presence_of_element_located((By.XPATH, self.player_thumbnail_element))
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
                                    EC.presence_of_element_located((By.XPATH, self.player_thumbnail_element))
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

            # Upload Button
            try:
                WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, self.upload_player_element))
                    ).click()
                print("The Player video setting Uploaded successfully")
                time.sleep(4)
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Upload Status", attachment_type=AttachmentType.PNG)
            except Exception as e:
                print(f"Failed to click Upload button: {e}")
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Upload_Button_Error", attachment_type=AttachmentType.PNG)
                time.sleep(3)

        except Exception as e:
           pytest.fail(f"Test failed due to error: {e}")

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 
    
   


