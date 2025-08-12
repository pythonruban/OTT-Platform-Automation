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
class TestLinkSettings:
   
    driver: WebDriver


     # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    link_element="//span[text()='Link Settings']"

    ios_id_element="//input[@name='ios_app_store_id']"
    ipad_id_element="//input[@name='ipad_app_store_id']"
    android_id_element="//input[@name='android_app_store_id']"
    window_id_element="//input[@name='windows_phone_app_store_id']"

    ios_url_element="//input[@name='ios_url']"
    ipad_url_element="//input[@name='ipad_url']"
    android_url_element="//input[@name='android_url']"
    window_url_element="//input[@name='windows_phone_url']"

    update_element="//span[text()='Update Settings']"


    
    def test_Link_Settings(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.link_element)))
        user = self.driver.find_element(By.XPATH, self.link_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

           # Scroll to ensure all elements are loaded
        ios=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.ios_id_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ios)
        time.sleep(2)
        ios.send_keys("ABCDE12345.com.foocompany.appname")

           # Scroll to ensure all elements are loaded
        ipad=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.ipad_id_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ipad)
        time.sleep(2)
        ipad.send_keys("johnsmith@icloud.com")

           # Scroll to ensure all elements are loaded
        android=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.android_id_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", android)
        time.sleep(2)
        android.send_keys("38400000-8cf0-11bd-b23e-10b96e40000d")

           # Scroll to ensure all elements are loaded
        win=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.window_id_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", win)
        time.sleep(2)
        win.send_keys("e5a2b8f7-c9d4-4e1d-9746-3b8670d02973")


        # URL 

           # Scroll to ensure all elements are loaded
        try :
            ios_url=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.ios_url_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ios_url)
            ios_url.clear()
            time.sleep(2)
            ios_url.send_keys("https://")
        except Exception as e:
            print(f" Failed to enter IOS URL: {e}")



        try :   # Scroll to ensure all elements are loaded
            ipad_url=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.ipad_url_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ipad_url)
            ipad_url.clear()
            time.sleep(2)
            ipad_url.send_keys("https://")
        except Exception as e:
            print(f" Failed to enter Ipad URL: {e}")


           # Scroll to ensure all elements are loaded
        try :
            andro_url=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.android_url_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", andro_url)
            andro_url.clear()
            time.sleep(2)
            andro_url.send_keys("https://")
        except Exception as e:
            print(f" Failed to enter Android URL: {e}")


           # Scroll to ensure all elements are loaded
        try :
            dow_url=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.window_url_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dow_url)
            dow_url.clear()
            time.sleep(2)
            dow_url.send_keys("https://")
        except Exception as e:
            print(f" Failed to enter Windows URL: {e}")



        # update or save element
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Link Settings details Updated successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 

