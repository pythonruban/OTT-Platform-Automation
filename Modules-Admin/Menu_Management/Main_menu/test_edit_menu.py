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
class TestAdd_Menu:
   
    driver: WebDriver
    
    
       #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "1280_720 px.jpg")
    image_path_2 = os.path.join(base_dir, "1080.1080.jpg")



                
     # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH
    
    menu_element="//span[text()='Menu']"
    main_menu_element="//span[text()='Main Menu']"
    
    dot_element="(//span[@class='editdropdown-button'])[7]"
    edit_element="(//span[text()='Edit'])[7]"
    
    menu_name_element="(//input[@id='inputField'])[1]"
    menu_item_element="(//select[@id='selectField'])[1]"
    menu_url_element="(//input[@id='inputField'])[2]"
    drop_down_element="(//select[@id='selectField'])[2]"
    drop_sub_element="//div[@id='react-select-27-placeholder' and contains(@class, 'css-1jqq78o-placeholder')]"
    
    enable_home_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    enable_menu_element="(//span[@class='admin-slider position-absolute admin-round '])[2]"
    enable_icon_element="(//span[@class='admin-slider position-absolute admin-round '])[3]"
    
    dark_element="//input[@type='file' and contains(@class, 'AdminImageUploader')]"
    light_element="//input[@type='file' and @name='light' and @id='8']"
    save_element="(//span[text()='Update Menu'])[1]"
    
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

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.main_menu_element)))
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
        
       
        
        menu=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.menu_name_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
        menu.clear()
        time.sleep(1)
        menu.send_keys("Demo Testing")
    
        
        
        drop_down1= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.menu_item_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down1) 
        time.sleep(2)
        select = Select(drop_down1)
        select.select_by_visible_text("Site Url")
        
        url=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.menu_url_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", url)
        time.sleep(1)
        url.send_keys("http://node-admin.webnexs.org/addfootermenu")
        
        drop_down2= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.drop_down_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down2) 
        time.sleep(2)
        select = Select(drop_down2)
        select.select_by_visible_text("Audio Categories")
        
        drop_down3= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.drop_sub_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down3) 
        time.sleep(2)
        select = Select(drop_down3)
        select.select_by_visible_text("Menu Status")
        
        toggle1 = self.driver.find_element(By.XPATH, self.enable_home_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1) 
        time.sleep(2)  
        actions = ActionChains(self.driver)
        actions.double_click(toggle1).perform()

        
        toggle2 = self.driver.find_element(By.XPATH, self.enable_menu_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2) 
        time.sleep(2)  
        actions = ActionChains(self.driver)
        actions.double_click(toggle2).perform()

        
        toggle3 = self.driver.find_element(By.XPATH, self.enable_icon_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3) 
        time.sleep(2)  
        actions = ActionChains(self.driver)
        actions.double_click(toggle3).perform()

        
              # Upload Image
        ime=WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, self.dark_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ime)  
        ime.send_keys(self.image_path_1)
        print("✅ Image is Uploaded Successfully")
        time.sleep(2)
        
              # Upload Image
        im=WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, self.light_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",im)  
        im.send_keys(self.image_path_2)
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
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Menu details Updated successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  




   