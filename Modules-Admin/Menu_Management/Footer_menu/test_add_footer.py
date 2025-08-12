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
class TestAdd_Footer:
   
    driver: WebDriver


     # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH
    
    menu_element="//span[text()='Menu']"
    footer_menu_element="//span[text()='Footer Menus']"
    Add_footer_element="//span[text()='Add Footer Menu']"
    footer_name_element="(//input[@id='inputField'])[1]"
    footer_url_element="(//select[@id='selectField'])[1]"
    menu_url_element="(//input[@id='inputField'])[2]"
    column_position_element="(//select[@id='selectField'])[2]"
    enable_footer_element="//span[@class='admin-slider position-absolute admin-round ']"
    save_footer_element="(//span[text()='Save Footer Menu'])[1]"
    
    
       
    def test_Add_Footer(self,browser_setup):
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

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.footer_menu_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()
        
        add=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.Add_footer_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add)
        time.sleep(2)
        add.click()
        
        menu=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.footer_name_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
        time.sleep(1)
        menu.send_keys("Test")
    
        
        
        drop_down1= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.footer_url_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down1) 
        time.sleep(2)
        select = Select(drop_down1)
        select.select_by_visible_text("Custom Url")
        
        url=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.menu_url_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", url)
        time.sleep(1)
        url.send_keys("http://node-admin.webnexs.org/addfootermenu")
    
        
        drop_down2= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.column_position_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down2) 
        time.sleep(2)
        select = Select(drop_down2)
        select.select_by_visible_text("Services")
        
        toggle1 = self.driver.find_element(By.XPATH, self.enable_footer_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle1)
        time.sleep(2)

        
             # update or save element
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.save_footer_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Footer Menu details Added successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  

