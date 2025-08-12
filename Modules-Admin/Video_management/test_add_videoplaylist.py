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

import glob
import os

@pytest.mark.usefixtures("browser_setup")
class TestVideoplaylist:
    
    driver: WebDriver

    # imageFile_path = os.path.join(os.getcwd(), f'tmp\\sample2.png')
    imageFile_path = f'/home/automationflickn/public_html/tmp/sample2.png'

    email_element = "email" #id
    password_element = "password" #id
    login_btn_element = "//button[normalize-space()='SIGN IN']" #XPATH

    video_management_btn_element = "//span[normalize-space()='Video Management']" #XPATH
    manage_videoplaylist_btn_element = "//a[normalize-space()='Manage Video Playlist']" #XPATH
    addnew_btn_element = "//i[@class='fa fa-plus-circle']"
    # sendkeys element
    NVL_name_btn_element = "//input[@id='title']"
    NVL_slug_btn_element = "//input[@id='slug']"
    image_element = "//input[@id='image']"
    description_element = "//textarea[@name='description']"

    close_btn_element = "//button[contains(text(),'Close')]"
    save_changes_btn_element = "//button[@id='submit-new-cat']" 

    def setup_class(self):
        self.driver.get("https://dev.e360tv.com/admin") #Enter website url
        self.driver.maximize_window()
  
    def test_add_videoplaylist(self):

        action = ActionChains(self.driver)

        
        WebDriverWait(self.driver, 15).until(lambda driver: driver.current_url == "https://dev.e360tv.com/login")
        
        self.driver.find_element(By.ID, self.email_element).send_keys('admin@admin.com')
        self.driver.find_element(By.ID, self.password_element).send_keys('Webnexs123!@#') 
        self.driver.find_element(By.XPATH, self.login_btn_element).click()
        time.sleep(5)

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.video_management_btn_element))).click()
        time.sleep(2)

        self.driver.execute_script("document.body.style.zoom='65%'") 

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.manage_videoplaylist_btn_element))).click()
        
       
        # self.driver.find_element(By.XPATH, self.manage_videoplaylist_btn_element).click()
        time.sleep(2) 
        self.driver.find_element(By.XPATH, self.addnew_btn_element).click()
        time.sleep(5)
        
        self.driver.find_element(By.XPATH, self.NVL_name_btn_element).send_keys("Demolist")
        self.driver.find_element(By.XPATH, self.NVL_slug_btn_element).send_keys("test")
        self.driver.find_element(By.XPATH, self.image_element).send_keys(self.imageFile_path)

        # Save Button
        self.driver.find_element(By.XPATH, self.save_changes_btn_element).click()
        time.sleep(3)

        allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "New Video playList Created Successfully", attachment_type= AttachmentType.PNG)        
        time.sleep(2)

        # Close Button 
        # self.driver.find_element(By.XPATH, self.close_btn_element).click()

        assert True

    def teardown_class(self):
        self.driver.quit()