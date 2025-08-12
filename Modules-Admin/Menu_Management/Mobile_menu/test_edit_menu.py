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
class TestEdit_Menu:
   
    driver: WebDriver
    
    
       #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "1080.1080.jpg")
    
    
     # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH
    
    menu_element="//span[text()='Menu']"
    mobile_menu_element="//span[text()='Mobile Side Menus']"
    
    dot_element="//span[@class='editdropdown-button']"
    edit_element="//span[text()='Edit']"
    
    name_element="//input[@id='inputField']"
    description_element="//textarea[@id='customArea']"
    enable_menu_element="//span[@class='admin-slider position-absolute admin-round ']"
    mobile_image_element="//input[@type='file' and @name='light']"
    save_element="(//span[text()='Update Mobile Menu'])[1]"
    
    
    
    def test_Edit_Menu(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.menu_element)))
        user = self.driver.find_element(By.XPATH, self.menu_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.mobile_menu_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()
        
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
        
        
        menu=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.name_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
        menu.clear()
        time.sleep(1)
        menu.send_keys("Testing")
        
        descrip=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.description_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", descrip)
        descrip.clear()
        time.sleep(1)
        descrip.send_keys("Demo Testing")
        
        
        toggle1 = self.driver.find_element(By.XPATH, self.enable_menu_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1) 
        time.sleep(2)  
        actions = ActionChains(self.driver)
        actions.double_click(toggle1).perform()

        
        
                # Upload Image
        ime=WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, self.mobile_image_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ime)  
        ime.send_keys(self.image_path_1)
        print("✅ Image is Uploaded Successfully")
        time.sleep(2)
        
        
                    # update or save element
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.save_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Mobile Menu details Updated successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
        
        
        
   