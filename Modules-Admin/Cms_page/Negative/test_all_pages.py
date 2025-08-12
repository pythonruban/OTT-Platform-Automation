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
class TestAdd_Allpages:
   
    driver: WebDriver

    
       #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "1692.jpg")


       # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    page_element="//span[text()='Pages']"
    All_element="//span[text()='All Pages']"

    add_page_element="//span[text()='Add Page']"
    title_element="(//input[@id='inputField'])[1]"
    slug_element="(//input[@id='inputField'])[2]"
    content_element="//div[@class='jodit-wysiwyg']"
    image_element="//input[@id='fileId']"
    enable_page_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    enable_footer_element="(//span[@class='admin-slider position-absolute admin-round '])[2]"

    submit_element="(//button[@id='adminButton'])[2]"




    def test_Add_Allpages(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.page_element)))
        user = self.driver.find_element(By.XPATH, self.page_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.All_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()

        ad=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.add_page_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ad)
        time.sleep(2)
        ad.click()

        try :
            name=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.title_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)  
            name.clear()
            time.sleep(1)
            name.send_keys("")
            time.sleep(3)
            
        except Exception as e:
            print(f" Failed to enter title: {e}")

        sg=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.slug_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",sg)  
        sg.send_keys("Vijay")
        time.sleep(3)
        try :
            ma=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.content_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ma) 
            ma.clear()
            time.sleep(1) 
            ma.send_keys("")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to enter Page Content: {e}")


        image1 =WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.image_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image1)
        time.sleep(2)
        image1.send_keys(self.image_path_1)
        time.sleep(2)
        
        toggle1 = self.driver.find_element(By.XPATH, self.enable_page_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle1)
        time.sleep(2)

        toggle2 = self.driver.find_element(By.XPATH, self.enable_footer_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle2)
        time.sleep(2)

        save=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.submit_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save) 
        save.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="CMS page All Pages details Added successfully.", attachment_type=AttachmentType.PNG)
    
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 








    