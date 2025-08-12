import time
import allure
import pytest
import os

 
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
class Test_Storage:
   
    driver: WebDriver

      # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    settings_element="//span[text()='Settings']"
    storage_element="//span[text()='Storage Settings']"

    enable_site_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    enable_aws_element="(//span[@class='admin-slider position-absolute admin-round '])[2]"
    enable_cdn_element="(//span[@class='admin-slider position-absolute admin-round '])[3]"
    enable_flucdn_element="(//span[@class='admin-slider position-absolute admin-round '])[4]"
    enable_vicdn_element="(//span[@class='admin-slider position-absolute admin-round '])[5]"

    size_element="//input[@id='storageLimit']"
    store_element="//select[@id='storageType']"

    save_element="//span[text()='Update Settings']"

    def test_Storage(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.settings_element)))
        user = self.driver.find_element(By.XPATH, self.settings_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.storage_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.enable_site_element)))
        toggle = self.driver.find_element(By.XPATH, self.enable_site_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
        time.sleep(2)

        # Perform double-click
        actions = ActionChains(self.driver)
        actions.double_click(toggle).perform()
        time.sleep(2)
    

    
        toggle1 = self.driver.find_element(By.XPATH, self.enable_aws_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1)
        time.sleep(2)

        # Perform double-click
        actions = ActionChains(self.driver)
        actions.double_click(toggle1).perform()
        time.sleep(2)
    

    
        toggle2 = self.driver.find_element(By.XPATH, self.enable_cdn_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2)
        time.sleep(2)

        # Perform double-click
        actions = ActionChains(self.driver)
        actions.double_click(toggle2).perform()
        time.sleep(2)


    
        toggle3 = self.driver.find_element(By.XPATH, self.enable_flucdn_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3)
        time.sleep(2)

        # Perform double-click
        actions = ActionChains(self.driver)
        actions.double_click(toggle3).perform()
        time.sleep(2)
    
    
        toggle4 = self.driver.find_element(By.XPATH, self.enable_vicdn_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle4)
        time.sleep(2)

        # Perform double-click
        actions = ActionChains(self.driver)
        actions.double_click(toggle4).perform()
        time.sleep(2)
    
        
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.size_element)))
        upload = self.driver.find_element(By.XPATH, self.size_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload)
        upload.clear()
        time.sleep(2)
        upload.send_keys("500")
        time.sleep(1)
        
        drop_down = self.driver.find_element(By.XPATH, self.store_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", drop_down) 
        time.sleep(2)
        select = Select(drop_down)
        select.select_by_visible_text("Megabyte - (MB)")


        save=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.save_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save) 
        time.sleep(2)  
        save.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Storage Settings in Main Settings details Saved successfully.", attachment_type=AttachmentType.PNG)
    
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")     
        
          
         
         

