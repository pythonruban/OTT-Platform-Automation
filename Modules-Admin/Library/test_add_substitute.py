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

from selenium.webdriver.firefox.webdriver import WebDriver

from utilities.readProp import ReadConfig


import glob
import os

@pytest.mark.usefixtures("browser_setup")
class TestLibraryUpload:
    
    driver: WebDriver

    
    #*******Local Path*******#
    
    # image and video local path
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "9_16.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "1280_720 px.png")
    videoFile_path = os.path.join(base_dir, "Maaman.mp4")
    pdfFile_path = os.path.join(base_dir, "sample2.pdf")
    subFile_path = os.path.join(base_dir, "sample2.srt")
    # video path
    names = os.path.abspath(os.path.join(base_dir, "sample1.mp4"))
    audio = os.path.abspath(os.path.join(base_dir, "sample1.mp3"))
    substitute = os.path.abspath(os.path.join(base_dir, "sample2.pdf"))

    email_element = "signin-email" #ID
    password_element =  "signin-password" #ID
    login_btn_element = "signin-submit" #ID
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH


    manage_library_btn_element = "libraryManagement" #ID
    add_video_audio_btn_element = "addLibrary" #ID 
    add_substitute_btn_element = "substituteButton" #ID
    substitute_upload_element = "//input[@id='fileInput']" #XPATH
    lib_element = "//span[normalize-space()='Lib']"
    retry_element = "//button[contains(@class,'indicatorButon mx-3 theme-border-secondary rounded-2 cancelText')]" #XPATH
    uparrow_element = "//button[@type='button']//*[name()='svg']" #XPATH


    def test_add_substitute(self,browser_setup):
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
        except TimeoutException:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login Failed", attachment_type=AttachmentType.PNG)
            raise AssertionError("Login Failed")

         # Click on the "Manage Library" button

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.ID, self.manage_library_btn_element))).click()
        time.sleep(3)
        self.driver.find_element(By.ID, self.add_video_audio_btn_element).click()
        time.sleep(3)
        self.driver.find_element(By.ID, self.add_substitute_btn_element).click()
        time.sleep(3)
        self.driver.find_element(By.XPATH, self.substitute_upload_element).send_keys(self.names)
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.uparrow_element).click()
        time.sleep(2)

        # try:
        #     substitute_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.substitute_upload_element)))
        # except TimeoutException:
        #     allure.attach(self.driver.get_full_page_screenshot_as_png(), name="substitute Upload Element Timeout", attachment_type=AttachmentType.PNG)
        #     assert False, "substitute upload input element not found within the timeout period"

        # if substitute_input:
        #     substitute_input.send_keys(self.names)

        #     # Optional: Check if upload success indicator is visible (update XPath as needed)
        #     upload_success = WebDriverWait(self.driver, 10).until(
        #         EC.text_to_be_present_in_element((By.XPATH, "//span[@class='upload-status']"), "Uploaded")
        #     )

        #     if upload_success:
        #         allure.attach(self.driver.get_full_page_screenshot_as_png(), name="substitute Uploaded Successfully", attachment_type=AttachmentType.PNG)
        #     else:
        #         allure.attach(self.driver.get_full_page_screenshot_as_png(), name="substitute Upload Failed", attachment_type=AttachmentType.PNG)
        #         assert False, "substitute file upload did not complete successfully"
        # else:
        #     allure.attach(self.driver.get_full_page_screenshot_as_png(), name="substitute Upload Element Not Found", attachment_type=AttachmentType.PNG)
        #     assert False, "substitute upload input element not found"


        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.lib_element))).click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="substitute Added Successfully", attachment_type=AttachmentType.PNG)

 


        
    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 
 



