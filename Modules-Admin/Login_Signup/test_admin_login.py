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
class TestAddVideo:
    
    driver: WebDriver

    email_element = "//div[contains(@class,'shadow border border-1 theme-border-color p-4 rounded-3 col-11 col-lg-6 col-xl-4 mx-auto')]//input[contains(@placeholder,'email')]" #XPATH
    password_element =  "//input[contains(@placeholder,'Enter Password')]" #XPATH
    login_btn_element = "//span[normalize-space()='login']" #XPATH
 

    def setup_class(self):
        self.driver.get(ReadConfig.getAdminPageURL()) #Enter website url
        self.driver.maximize_window()
        
    def test_admin_login(self):

        action = ActionChains(self.driver)
        
        WebDriverWait(self.driver, 15).until(lambda driver: driver.current_url == ReadConfig.getAdminPageURL())

        self.driver.find_element(By.XPATH, self.email_element).send_keys("admin@admin.com")
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.password_element).send_keys(ReadConfig.getPassword())
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.login_btn_element).click() 
        time.sleep(7)

        current_url = self.driver.current_url

        allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "login successful with valid credentials", attachment_type= AttachmentType.PNG)





    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
     

