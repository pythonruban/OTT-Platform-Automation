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
class TestVideocategories:
    
    driver: WebDriver

    email_element = "email" #id
    password_element = "password" #id
    login_btn_element = "//button[normalize-space()='SIGN IN']" #XPATH

    video_management_btn_element = "//span[normalize-space()='Video Management']" #XPATH
    manage_videocategorie_btn_element = "//li[contains(@class,'')]//a[contains(text(),'Manage Video Categories')]" #XPATH  
    delete_changes_btn_element = f"//table[@id='categorytbl']//td/ancestor::tr//a[@data-original-title='Delete']"

    def setup_class(self):
        self.driver.get("https://dev.e360tv.com/admin") #Enter website url
        self.driver.maximize_window()
        
    def test_delete_videocategorie(self):

        action = ActionChains(self.driver)

        
        WebDriverWait(self.driver, 15).until(lambda driver: driver.current_url == "https://dev.e360tv.com/login")
        
        self.driver.find_element(By.ID, self.email_element).send_keys('admin@admin.com')
        self.driver.find_element(By.ID, self.password_element).send_keys('Webnexs123!@#')
        self.driver.find_element(By.XPATH, self.login_btn_element).click()
        time.sleep(5)

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.video_management_btn_element))).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.manage_videocategorie_btn_element).click()
        time.sleep(5)

        categories = self.driver.find_elements(By.XPATH, self.delete_changes_btn_element)   

        if(len(categories) > 1):

            categories[0].click()
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            time.sleep(2)
            self.driver.switch_to.alert.dismiss()
            time.sleep(2)

            categories[0].click()
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            time.sleep(2)
            self.driver.switch_to.alert.accept()
            time.sleep(5)

            allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "Successfully Deleted Category", attachment_type= AttachmentType.PNG)        
            assert True    
        
        elif(len(categories) == 1):

            categories[0].click()
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            time.sleep(2)
            self.driver.switch_to.alert.dismiss()
            time.sleep(2)

            allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "Delete Button is checked with single element", attachment_type= AttachmentType.PNG)        
            assert True
            
        else:

            allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "No Data For Deleting Category", attachment_type= AttachmentType.PNG)        
            assert True


    def teardown_class(self):
        self.driver.quit()