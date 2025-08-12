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
class TestPagination:
   
    driver: WebDriver

      # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    users_element="//span[text()='Users']"
    all_element="//span[text()='All User']"
    
     
    pagination_element="//p[text()='Showing rows 1 to 10 of 102']"
    first_element="//button[@id='pageNumber1' and text()='1']"
    second_element="//button[@id='pageNumber2' and text()='2']"
    
    
    
    def test_Pagination(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.users_element)))
        user = self.driver.find_element(By.XPATH, self.users_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.all_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()
        
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.pagination_element)))
        page = self.driver.find_element(By.XPATH, self.pagination_element)
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);" ,page)
        time.sleep(2)
        

        
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.first_element)))
        first = self.driver.find_element(By.XPATH, self.first_element)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);", first)
        time.sleep(2)
        # first.click()
        # time.sleep(2)
        # allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Cast & Crew User Pagination details Updated successfully.", attachment_type=AttachmentType.PNG)
        
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.second_element)))
        second = self.driver.find_element(By.XPATH, self.second_element)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);",second)
        time.sleep(2)
        second.click()
        time.sleep(2)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="User Management Pagination details clicked successfully.", attachment_type=AttachmentType.PNG)
    
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
    