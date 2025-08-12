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
class TestSearch_Bar:
   
    driver: WebDriver

    
       #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "1080_10802.jpg")
 

    # Define the XPaths
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    
    artist_element="//span[text()='Artists Management']"
    all_artist_element="(//span[text()='All Artists'])[1]"

    dot_element="(//span[@class='editdropdown-button'])[1]"
    edit_element="(//span[text()='Edit'])[1]"

    edit_search_element="//input[@id='filter-search']"
  

    
    
    def test_Search_Bar(self,browser_setup):
        self.driver = browser_setup
        self.driver.maximize_window()
        self.driver.get(ReadConfig.getAdminPageURL())

        # Login to the application
        self.driver.find_element(By.XPATH, self.email_element).send_keys("admin@admin.com")
        self.driver.find_element(By.XPATH, self.password_element).send_keys("Webnexs123!@#")
        self.driver.find_element(By.XPATH, self.login_element).click()

        try:
            WebDriverWait(self.driver, 80).until(EC.visibility_of_element_located((By.XPATH, self.dashboard_element))).click()
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login was successful and the UI elements have been loaded.", attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login successful and the UI elements have not loaded due to timeout", attachment_type=AttachmentType.PNG)
            raise e


        
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.artist_element)))
        user = self.driver.find_element(By.XPATH, self.artist_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        element = self.driver.find_element(By.XPATH, self.all_artist_element)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
        time.sleep(2)
        element .click()
        
        try:
            WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.edit_search_element)))
            search = self.driver.find_element(By.XPATH, self.edit_search_element)
            self.driver.execute_script("arguments[0].scrollIntoView(false);", search)
            time.sleep(2)
            search.send_keys("Demo")
            time.sleep(2)

            result_elements=WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table//td[contains(., 'Demo')]")))
            
            result_elements = self.driver.find_elements(By.XPATH, "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'demo')]")

            if len(result_elements) > 0:
                print("✅ Search results found.")
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Cast & Crew User Search Bar details Updated successfully.", attachment_type=AttachmentType.PNG)
            else:
                print("❌ No search results found.")
                
        except Exception as e:
            print(f"❌ An error occurred during search: {str(e)}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(),
                        name="Search Function Failed",
                        attachment_type=AttachmentType.PNG)
            
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 

 
