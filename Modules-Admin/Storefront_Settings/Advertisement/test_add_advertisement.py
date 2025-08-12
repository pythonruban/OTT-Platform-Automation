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
class TestAddAdvertisement:
   
    driver: WebDriver
   # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    storefront_element="(//span[text()='Storefront Settings'])[2]"
    advertisement_element="//h5[text()='Advertisement Settings']"

    enable_video_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    enable_live_element="(//span[@class='admin-slider position-absolute admin-round '])[2]"
    enable_audio_element="(//span[@class='admin-slider position-absolute admin-round '])[3]"
    enable_episode_element="(//span[@class='admin-slider position-absolute admin-round '])[4]"
    enable_24_7_element="(//span[@class='admin-slider position-absolute admin-round '])[5]"

    submit_element="//button[text()='Update']"


  
    def test_Add_Advertisement(self,browser_setup):
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

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.advertisement_element)))
        front = self.driver.find_element(By.XPATH, self.advertisement_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", front)
        time.sleep(2)
        front.click()

        toggle = self.driver.find_element(By.XPATH, self.enable_video_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle) 
        actions = ActionChains(self.driver)
        actions.double_click(toggle).perform()
        time.sleep(2)

        toggle1 = self.driver.find_element(By.XPATH, self.enable_live_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1) 
        actions = ActionChains(self.driver)
        actions.double_click(toggle1).perform()
        time.sleep(2)
       

        toggle2 = self.driver.find_element(By.XPATH, self.enable_audio_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2) 
        actions = ActionChains(self.driver)
        actions.double_click(toggle2).perform()
        time.sleep(2)

        toggle3 = self.driver.find_element(By.XPATH, self.enable_episode_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3) 
        actions = ActionChains(self.driver)
        actions.double_click(toggle3).perform()
        time.sleep(2)
        
        toggle4 = self.driver.find_element(By.XPATH, self.enable_24_7_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle4) 
        actions = ActionChains(self.driver)
        actions.double_click(toggle4).perform()
        time.sleep(2)

            # update or save element
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.submit_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Advertisement details Saved successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 






        