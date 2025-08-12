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
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

import glob
import os

@pytest.mark.usefixtures("browser_setup")
class TestmasterVideolist:
    
    driver: WebDriver

    email_element = "email" #id
    password_element = "password" #id
    login_btn_element = "//button[normalize-space()='SIGN IN']" #XPATH

    video_management_btn_element = "//span[normalize-space()='Video Management']" #XPATH
    master_videolist_btn_elements = "//a[@class='iq-waves-effect'][normalize-space()='Master Video List']" #XPATH
    total_masterlist_btn_element = "//p[normalize-space()='Total Master list']"


    def setup_class(self):
        self.driver.get("https://dev.e360tv.com/admin") #Enter website url
        self.driver.maximize_window()
        
    @pytest.mark.skip
    def test_masterlist(self):

        action = ActionChains(self.driver)

        try:
            self.driver.set_page_load_timeout(10)
        
            WebDriverWait(self.driver, 15).until(lambda driver: driver.current_url == "https://dev.e360tv.com/login")
            
            self.driver.find_element(By.ID, self.email_element).send_keys('admin@admin.com')
            self.driver.find_element(By.ID, self.password_element).send_keys('Webnexs123!@#')
            self.driver.find_element(By.XPATH, self.login_btn_element).click()
            time.sleep(5)

            WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.video_management_btn_element))).click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, self.master_videolist_btn_elements).click()

            try:
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.total_masterlist_btn_element))).tag_name
                if(res == 'a' or res == 'button'):
                    assert True
                else:
                    allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "Total Master Video List button is not clickable.", attachment_type= AttachmentType.PNG)        
                    assert False      

            except:
                print("Total Master Video List button is not found.")
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "Total Master Video List button is not found.", attachment_type= AttachmentType.PNG)        
                assert False

        except:      
            self.driver.execute_script("window.stop();")    
            try: 
                res = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, self.total_masterlist_btn_element))).tag_name                
                if(res == 'a' or res == 'button'):
                    assert True
                else:
                    allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "Total Master Video List button is not clickable.", attachment_type= AttachmentType.PNG)        
                    assert False
                    
            except:
                print("Total Master Video page is taking longer than usual to load.")
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "Total Master Video page is taking longer than usual to load.", attachment_type= AttachmentType.PNG)        
                assert False

    def teardown_class(self):
       self.driver.quit()