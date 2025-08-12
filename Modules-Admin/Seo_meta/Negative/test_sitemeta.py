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
class TestEditSite:
   
    driver: WebDriver

    
       #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "1691.jpg")


     # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    site_meta_element="//span[text()='Site Meta Settings']"

    dot_element="(//span[@class='editdropdown-button'])[1]" 
    edit_element="(//span[text()='Edit Site'])[1]"

    page_element="//select[@id='page_name']"
    title_element="//input[@id='page_title']"
    meta_element="//input[@id='meta_keyword']"
    page_meta_element="//div[@class='jodit-wysiwyg']"
    image_element="//input[@type='file']"
   
    submit_element="//span[text()='Update Settings']"

    
    def test_Edit_Site(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.site_meta_element)))
        user = self.driver.find_element(By.XPATH, self.site_meta_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.dot_element))
            )
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.edit_element))
            )
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")


        try :
            drop_down1= WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, self.page_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down1) 
            time.sleep(2)
            select = Select(drop_down1)
            select.select_by_visible_text("Select an Page Name")
        except TimeoutException:
            print("Error: The element was not clickable within the given time.")

           # Scroll to ensure all elements are loaded
        try :
            tit=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.title_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tit)
            time.sleep(1)
            tit.clear()
            time.sleep(2)
            tit.send_keys("")
        
        except TimeoutException:
            print("Error: The element was not clickable within the given time.")

           # Scroll to ensure all elements are loaded
        try :
            meta=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.meta_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", meta)
            time.sleep(1)
            meta.clear()
            time.sleep(2)
            meta.send_keys("")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Site Meta details Update", attachment_type=AttachmentType.PNG)
       
        
        except TimeoutException:
            print("Error: The element was not clickable within the given time.")

           # Scroll to ensure all elements are loaded
        try :
            page_meta=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.page_meta_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", page_meta)
            time.sleep(1)
            page_meta.clear()
            time.sleep(2)
            page_meta.send_keys("")
            
        except TimeoutException:
            print("Error: The element was not clickable within the given time.")

        try :
            file_input = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH, self.image_element)))

            # Use JavaScript to remove 'display: none' if it's hidden
            self.driver.execute_script("arguments[0].style.display = 'block';", file_input)

            # Scroll it into view just in case
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", file_input)

            # Upload the image
            file_input.send_keys(self.image_path_1)

            # Wait to allow upload processing
            time.sleep(2)
        
        except TimeoutException:
            print("Error: The element was not clickable within the given time.")

           # update or save element
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.submit_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Edit Site Meta details Updated successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 



