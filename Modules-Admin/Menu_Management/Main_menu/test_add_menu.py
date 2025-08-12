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
    image_path_1 = os.path.join(base_dir, "1080.1080.jpg")
    image_path_2 = os.path.join(base_dir, "1280_720 px.jpg")




     # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH
    
    menu_element="//span[text()='Menu']"
    main_menu_element="//span[text()='Main Menu']"
    Add_menu_element="//span[text()='Add Menu']"
    
    menu_name_element="(//input[@id='inputField'])[1]"
    menu_item_element="(//select[@id='selectField'])[1]"
    menu_url_element="(//input[@id='inputField'])[2]"
    drop_down_element="(//select[@id='selectField'])[2]"
    drop_sub_element="//div[@id='react-select-23-placeholder' and contains(@class, 'css-1jqq78o-placeholder')]"
    
    enable_home_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    enable_menu_element="(//span[@class='admin-slider position-absolute admin-round '])[2]"
    enable_icon_element="(//span[@class='admin-slider position-absolute admin-round '])[3]"
    
    dark_element="(//input[@id='fileId'])[1]"
    light_element="(//input[@id='fileId'])[2]"
    save_element="(//span[text()='Save Menu'])[1]"
    
    def test_Add_Menu(self,browser_setup):
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
        
        add=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.Add_menu_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add)
        time.sleep(2)
        add.click()
        
        menu=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.menu_name_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
        time.sleep(1)
        menu.send_keys("Test")
    
        
        
        drop_down1= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.menu_item_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down1) 
        time.sleep(2)
        select = Select(drop_down1)
        select.select_by_visible_text("Custom Url")
        
        url=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.menu_url_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", url)
        time.sleep(1)
        url.send_keys("http://node-admin.webnexs.org/addfootermenu")
        
        drop_down2= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.drop_down_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down2) 
        time.sleep(2)
        select = Select(drop_down2)
        select.select_by_visible_text("Video Categories")
        
        drop_down3= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.drop_sub_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down3) 
        time.sleep(2)
        select = Select(drop_down3)
        select.select_by_visible_text("Action")
        
        toggle1 = self.driver.find_element(By.XPATH, self.enable_home_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle1)
        time.sleep(2)
        
        toggle2 = self.driver.find_element(By.XPATH, self.enable_menu_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle2)
        time.sleep(2)
        
        toggle3 = self.driver.find_element(By.XPATH, self.enable_icon_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle3)
        time.sleep(2)
        
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
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Menu details Added successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  




   