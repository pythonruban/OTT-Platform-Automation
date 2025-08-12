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
class TestUpdateTranscoding:
   
    driver: WebDriver
   # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    storefront_element="(//span[text()='Storefront Settings'])[2]"
    transcode_element="//h5[text()='Transcoding Settings']"

    select_element="//div[@class=' css-13cymwt-control']"
    url_element="//input[@id='testing-transcoding-url']"
    enable_transcode_element="(//span[@class='admin-slider position-absolute admin-round'])[1]"
    enable_videoclip_element="(//span[@class='admin-slider position-absolute admin-round'])[2]"

    save_element="//span[text()='Save Transcoding']"



    
     
    def test_Update_Transcoding(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.storefront_element)))
        user = self.driver.find_element(By.XPATH, self.storefront_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.transcode_element)))
        front = self.driver.find_element(By.XPATH, self.transcode_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", front)
        time.sleep(2)
        front.click()
        
        try :
            action = ActionChains(self.driver)
            sele=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.select_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",sele) 
            time.sleep(2)
            sele.click()
            time.sleep(1)
            action.send_keys('1080p').perform()
            action.send_keys(Keys.ENTER).perform()  
            time.sleep(1)
        except Exception as e:
             print(f"An unexpected error occurred: {e}")    

        try :
            name=WebDriverWait(self.driver, 30).until(
               EC.element_to_be_clickable((By.XPATH, self.url_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name) 
            name.clear()
            time.sleep(2)
            name.send_keys("")
            time.sleep(2)
           
        except Exception as e:
            print(f" Failed to enter URL: {e}")

        toggle1 = self.driver.find_element(By.XPATH, self.enable_transcode_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1)
        time.sleep(2)

        actions = ActionChains(self.driver)
        actions.double_click(toggle1).perform()
        time.sleep(2)

        toggle2 = self.driver.find_element(By.XPATH, self.enable_videoclip_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle2)
        time.sleep(2)

           # update or save element
        save=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.save_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", save)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Transcoding details Added successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 