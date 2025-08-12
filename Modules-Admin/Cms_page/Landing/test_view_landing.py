import time
import allure
import pytest
import os
import random
import string
 
from conftest import *
from allure_commons.types import AttachmentType
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
 
from utilities.readProp import ReadConfig

 
@pytest.mark.usefixtures("browser_setup")
class TestView_Landing:
   
    driver: WebDriver

       # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    page_element="//span[text()='Pages']"
    landing_element="//span[text()='Landing Pages']"

    toggle_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    slider_element="//span[text()='Enable']"
    dot_element="(//span[@class='editdropdown-button'])[1]"
    view_element="(//span[text()='View'])[1]"


   
    def test_View_Landing(self,browser_setup):
        self.driver = browser_setup
        self.driver.maximize_window()
        self.driver.get(ReadConfig.getAdminPageURL())

        # Login to the application
        self.driver.find_element(By.XPATH, self.email_element).send_keys(ReadConfig.getAdminId())
        self.driver.find_element(By.XPATH, self.password_element).send_keys(ReadConfig.getPassword())
        self.driver.find_element(By.XPATH, self.login_element).click()

        try:
            WebDriverWait(self.driver, 80).until(EC.visibility_of_element_located((By.XPATH, self.dashboard_element))).click()
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login was successful and the UI elements have been loaded.", attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login successful and the UI elements have not loaded due to timeout", attachment_type=AttachmentType.PNG)
            raise e

        

        # Scroll to ensure all elements are loaded
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.page_element)))
        user = self.driver.find_element(By.XPATH, self.page_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.landing_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()

        toggle1=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.toggle_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle1)
        time.sleep(4)

        self.driver.find_element(By.XPATH, self.slider_element).click()
        time.sleep(2)
        
                # Hover over the dot element
        dot_elem = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.dot_element))
        )
        ActionChains(self.driver).move_to_element(dot_elem).perform()

        # Optional: click after hover
        self.driver.execute_script("arguments[0].click();", dot_elem)

        # Wait for and click the view element
        elem = WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.view_element))
        )
        ActionChains(self.driver).move_to_element(elem).perform()
        self.driver.execute_script("arguments[0].click();", elem)
        time.sleep(4)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Landing page details View successfully.", attachment_type=AttachmentType.PNG)
    
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 

