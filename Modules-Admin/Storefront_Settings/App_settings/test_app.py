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
class TestApp:
   
    driver: WebDriver
   # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    storefront_element="(//span[text()='Storefront Settings'])[2]"
    app_settings_element="//h5[text()='APP Settings']"

    android_element="(//input[@id='inputField'])[1]"
    ios_element="(//input[@id='inputField'])[2]"
    android_tv_element="(//input[@id='inputField'])[3]"
    fire_tv_element="(//input[@id='inputField'])[4]"
    samsung_tv_element="(//input[@id='inputField'])[5]"
    lg_tv_element="(//input[@id='inputField'])[6]"
    roku_tv_element="(//input[@id='inputField'])[7]"

    submit_element="//button[text()='Save App URL']"


      
    def test_Update_Appsettings(self,browser_setup):
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

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.app_settings_element)))
        front = self.driver.find_element(By.XPATH, self.app_settings_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", front)
        time.sleep(2)
        front.click()

        an=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.android_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", an) 
        an.clear()
        time.sleep(2)
        an.send_keys("https://en.wikipedia.org/wiki/Android_(operating_system)")
        time.sleep(2)

        io=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.ios_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", io) 
        io.clear()
        time.sleep(2)
        io.send_keys("https://en.wikipedia.org/wiki/IOS")
        time.sleep(2)

        id=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.android_tv_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", id) 
        id.clear()
        time.sleep(2)
        id.send_keys("https://en.wikipedia.org/wiki/Android_TV")
        time.sleep(2)

        os=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.fire_tv_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", os) 
        os.clear()
        time.sleep(2)
        os.send_keys("https://en.wikipedia.org/wiki/Amazon_Fire_TV")
        time.sleep(2)

        re=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.samsung_tv_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", re) 
        re.clear()
        time.sleep(2)
        re.send_keys("https://en.wikipedia.org/wiki/Samsung_Electronics")
        time.sleep(2)

        ng=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.lg_tv_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ng) 
        ng.clear()
        time.sleep(2)
        ng.send_keys("https://en.wikipedia.org/wiki/LG_Electronics")
        time.sleep(2)

        lg=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.roku_tv_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lg) 
        lg.clear()
        time.sleep(2)
        lg.send_keys("https://en.wikipedia.org/wiki/Roku")
        time.sleep(2)

             # update or save element
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.submit_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="App Settings details Saved successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 








