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
class TestMulti_Delete:
   
    driver: WebDriver


    # Define the XPaths
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH
    
    artist_element="//span[text()='Artists Management']"
    all_artist_element="(//span[text()='All Artists'])[1]"
    
    checkbox1_element="(//input[@type='checkbox'])[2]"
    checkbox2_element="(//input[@type='checkbox'])[3]"
    checkbox3_element="(//input[@type='checkbox'])[4]"

    delete_element="(//span[text()='Delete'])[1]"
    delete_pop_element="(//span[text()='Delete'])[1]"


    def test_Multi_Delete(self,browser_setup):
        self.driver = browser_setup
        self.driver.maximize_window()
        self.driver.get(ReadConfig.getAdminPageURL())

        # Login to the application
        self.driver.find_element(By.XPATH, self.email_element).send_keys("admin@admin.com")
        self.driver.find_element(By.XPATH, self.password_element).send_keys("Webnexs123!@#")
        self.driver.find_element(By.XPATH, self.login_element).click()

        try:
            WebDriverWait(self.driver, 80).until(EC.visibility_of_element_located((By.XPATH, self.dashboard_element))).click()
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login was successful and the UI elements have been loaded.", attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login successful and the UI elements have not loaded due to timeout", attachment_type=AttachmentType.PNG)
            raise e

        
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.artist_element)))
        user = self.driver.find_element(By.XPATH, self.artist_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        element = self.driver.find_element(By.XPATH, self.all_artist_element)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
        time.sleep(2)
        element .click()
        
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.checkbox1_element)))
        check1 = self.driver.find_element(By.XPATH, self.checkbox1_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", check1)
        time.sleep(2)
        check1.click()
        
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.checkbox2_element)))
        check2 = self.driver.find_element(By.XPATH, self.checkbox2_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", check2)
        time.sleep(2)
        check2.click()
        
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.checkbox3_element)))
        check3 = self.driver.find_element(By.XPATH, self.checkbox3_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", check3)
        time.sleep(2)
        check3.click()
        
        dele = self.driver.find_element(By.XPATH, self.delete_element)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", dele)
        time.sleep(2)
        dele.click()
        
        
        delete = self.driver.find_element(By.XPATH, self.delete_pop_element)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", delete)
        time.sleep(2)
        delete.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Cast & Crew User Multi details Deleted successfully.", attachment_type=AttachmentType.PNG)
                  
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
        
        
        