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

from selenium.webdriver.firefox.webdriver import WebDriver

from utilities.readProp import ReadConfig

import glob
import os

@pytest.mark.usefixtures("browser_setup")
class TestAddNewUser:
    
    driver: WebDriver

    # # image and video local path
    # base_dir = os.path.join(os.getcwd(), "tmp")
    # imageFile_path_9_16 = os.path.join(base_dir, "9_16.jpg")
    # imageFile1280_720_path = os.path.join(base_dir, "1280_720 px.png")
    # videoFile_path = os.path.join(base_dir, "sample2.mp4")
    # pdfFile_path = os.path.join(base_dir, "sample2.pdf")
    # subFile_path = os.path.join(base_dir, "sample2.srt")
    # # video path
    # names = os.path.abspath(os.path.join(base_dir, "sample1.mp4"))

                 # *******Server Path*******#    
    base_dir = os.path.join(os.getcwd(), "/home/automationflickn/public_html/tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "9_16.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "1280_720 px.png")
    imageFile480_path = os.path.join(base_dir,"tmp\sample2_480.png")
    videoFile_path = os.path.join(base_dir, "sample2.mp4")
    pdfFile_path = os.path.join(base_dir, "sample2.pdf")
    subFile_path = os.path.join(base_dir, "sample2.srt")
    # video path
    names = os.path.abspath(os.path.join(base_dir, "sample1.mp4")) 

    email_element = "//input[@name='email']"
    password_element = "//input[@name='password']"
    signin_BTN_element = "//button[@type='submit']"

    all_menu_element = "//span[normalize-space()='Menu']"
    mobileSide_menu_element = "//span[normalize-space()='Mobile Side Menus']"

    add_mobile_menu_element = "//button[normalize-space()='Add Mobile Menu']"

    mobile_menu_name_element = "//input[contains(@name,'name')]"
    short_note_element = "//input[@name='short_note']"
    mobile_menu_image_element = "//input[@type='file']"

    submit_btn_element = "//button[text()='Save Menu']"

    check_add_element = "//div[text()='Test Mobile Menu']"

    def setup_class(self):
        self.driver.get(ReadConfig.getAdminPageURL()) #Enter website url
        self.driver.maximize_window()

    def test_EditUser(self):        

        action = ActionChains(self.driver)
        
        WebDriverWait(self.driver, 15).until(lambda driver: driver.current_url == ReadConfig.getAdminPageURL())
        
        ele = self.driver.find_elements(By.XPATH, self.email_element)
        ele[1].send_keys("admin@admin.com")
        self.driver.find_element(By.XPATH, self.password_element).send_keys("Webnexs123!@#")
        ele = self.driver.find_elements(By.XPATH, self.signin_BTN_element)
        ele[1].click()

        time.sleep(3)

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.all_menu_element)))
        all_menu = self.driver.find_element(By.XPATH, self.all_menu_element)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", all_menu)
        time.sleep(2)
        all_menu.click()

        mobile_menu = self.driver.find_element(By.XPATH, self.mobileSide_menu_element)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", mobile_menu)
        time.sleep(2)
        mobile_menu.click()
        time.sleep(2)

        self.driver.find_element(By.XPATH, self.add_mobile_menu_element).click()

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.mobile_menu_name_element)))
        time.sleep(2)

        self.driver.find_element(By.XPATH, self.mobile_menu_name_element).send_keys("Test Mobile Menu")
        self.driver.find_element(By.XPATH, self.short_note_element).send_keys("Test Mobile Menu")

        self.driver.find_element(By.XPATH, self.mobile_menu_image_element).send_keys(self.imageFile_path_9_16)

        allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "Add Mobile Menu Page", attachment_type= AttachmentType.PNG)

        submit = self.driver.find_element(By.XPATH, self.submit_btn_element)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", submit)
        time.sleep(2)
        submit.click()
        time.sleep(10)

        try:
            WebDriverWait(self.driver, 25).until(EC.visibility_of_element_located((By.XPATH, self.check_add_element)))
            time.sleep(5)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "New Mobile Menu Created Successfully", attachment_type= AttachmentType.PNG)     
            assert True                
        except:
            time.sleep(5)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "Bug: New Mobile Menu Is Not Created", attachment_type= AttachmentType.PNG)     
            assert False 
        

              def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 