import time
import allure
import pytest
from conftest import *
from allure_commons.types import AttachmentType

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import ActionChains, Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.webdriver import WebDriver
from utilities.readProp import ReadConfig

import glob
import os
# 

@pytest.mark.usefixtures("browser_setup")
class TestLibraryUpload:
    
    driver: WebDriver

    
    #*******Local Path*******#
    
    # image and video local path
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "9_16.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "1280_720 px.png")
    videoFile_path = os.path.join(base_dir, "sample2.mp4")
    pdfFile_path = os.path.join(base_dir, "sample2.pdf")
    subFile_path = os.path.join(base_dir, "sample2.srt")
    # video path
    names = os.path.abspath(os.path.join(base_dir, "sample1.mp4"))
    audio = os.path.abspath(os.path.join(base_dir, "sample1.mp3"))

    email_element = "signin-email" #ID
    password_element =  "signin-password" #ID
    login_btn_element = "signin-submit" #ID
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    manage_library_btn_element = "libraryManagement" #ID
    add_video_audio_btn_element = "addLibrary" #ID 
    add_audio_btn_element = "audioButton" #ID
    audio_upload_element = "//input[@id='fileInput']" #XPATH
    lib_element = "//span[normalize-space()='Lib']"
    retry_element = "//button[contains(@class,'indicatorButon mx-3 theme-border-secondary rounded-2 cancelText')]" #XPATH
    uparrow_element = "//button[@type='button']//*[name()='svg']" #XPATH



    def test_add_audio(self,browser_setup):
        self.driver = browser_setup

        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()
        time.sleep(2)
        self.driver.find_element(By.ID, self.email_element).send_keys(ReadConfig.getAdminId())
        self.driver.find_element(By.ID, self.password_element).send_keys(ReadConfig.getPassword())
        self.driver.find_element(By.ID, self.login_btn_element).click()
        time.sleep(2)
        
        try:
            WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.dashboard_element))).click()
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login was successful and the UI elements have been loaded.", attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login successful and the UI elements have not loaded due to timeout", attachment_type=AttachmentType.PNG)
            raise e


         # Click on the "Manage Library" button

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.ID, self.manage_library_btn_element))).click()
        time.sleep(3)
        self.driver.find_element(By.ID, self.add_video_audio_btn_element).click()
        time.sleep(3)
        self.driver.find_element(By.ID, self.add_audio_btn_element).click()
        time.sleep(3)
        self.driver.find_element(By.XPATH, self.audio_upload_element).send_keys(self.audio)
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.uparrow_element).click()
        time.sleep(2)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Audio Uploading", attachment_type=AttachmentType.PNG)

        # try:
        #     WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.audio_upload_element))).send_keys(self.audio)
        #     allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Audio Uploading", attachment_type=AttachmentType.PNG)
        # except TimeoutException:
        #     allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Audio Uploading failed", attachment_type=AttachmentType.PNG)
        #     raise TimeoutException("Audio Uploading failed")
        # time.sleep(2)

        # WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.lib_element))).click()
        # time.sleep(3)
        
        max_attempts = 5
        libbutton_clicked = False

        for attempt in range(max_attempts):
            try:
                # Try to find and click the libbutton if it's visible
                lib_button = self.driver.find_element(By.XPATH, self.lib_element)
                if lib_button.is_displayed():
                    lib_button.click()
                    allure.attach(self.driver.get_full_page_screenshot_as_png(), name=f"Lib Button Clicked - Attempt {attempt + 1}", attachment_type=AttachmentType.PNG)
                    libbutton_clicked = True
                    break
            except NoSuchElementException:
                pass

            # If libbutton not found, try clicking the trybutton
            try:
                try_button = self.driver.find_element(By.XPATH, self.retry_element)
                try_button.click()
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name=f"Try Button Clicked - Attempt {attempt + 1}", attachment_type=AttachmentType.PNG)
            except NoSuchElementException:
                pass

            time.sleep(2)  # Wait before the next attempt

        if not libbutton_clicked:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Failed to Click Lib Button After 5 Tries", attachment_type=AttachmentType.PNG)
            assert False, "Lib Button not found or clickable after multiple attempts"

        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Audio Added Successfully", attachment_type=AttachmentType.PNG)




        
    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 



