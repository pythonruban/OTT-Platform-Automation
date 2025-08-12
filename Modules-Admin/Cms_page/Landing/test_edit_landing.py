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
class TestEdit_Landing:
   
    driver: WebDriver

       # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    page_element="//span[text()='Pages']"
    landing_element="//span[text()='Landing Pages']"

   
    dot_element="(//span[@class='editdropdown-button'])[1]"
    edit_element="(//span[text()='Edit'])[1]"

   
    title_element="(//input[@id='inputField'])[1]"
    slug_element="(//input[@id='inputField'])[2]"
    page_content_element="//div[@class='jodit-wysiwyg']"
    contents_element="(//textarea[@id='customArea'])[1]"
    custom_element="(//textarea[@id='customArea'])[2]"
    bootstrap_element="(//textarea[@id='customArea'])[3]"

    enable_status_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    enable_page_element="(//span[@class='admin-slider position-absolute admin-round '])[2]"

    submit_element="(//span[text()='Save Page'])[2]"




    
    def test_Edit_Landing(self,browser_setup):
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

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.landing_element)))
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



       
        try :
            length= 6 
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")
 
            print(f"Using XPath: {self.title_element}")
 
            # Wait for the title input to be clickable
            name = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.title_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
            time.sleep(2)
            name.clear()
            time.sleep(2)  # small delay to ensure field is cleared
            name.send_keys(auto_name)
            time.sleep(2)
            print(" Auto name entered in the title field.")
 
        except Exception as e:
            print(f" Failed to enter title: {e}")

        sg=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.slug_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",sg)  
        sg.clear()
        time.sleep(1)
        sg.send_keys("Manivel")
        time.sleep(3)

        ma=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.page_content_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ma)  
        ma.clear()
        time.sleep(1)
        ma.send_keys("Demo")
        time.sleep(3)

        cm=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.contents_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",cm)  
        cm.clear()
        time.sleep(1)
        cm.send_keys("Testing")
        time.sleep(3)

        cus=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.custom_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",cus)  
        cus.clear()
        cus.send_keys("Customize")
        time.sleep(3)

        bot=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.bootstrap_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",bot)  
        bot.clear()
        time.sleep(1)
        bot.send_keys("StrapBoot")
        time.sleep(3)

        try:
            toggle2 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.enable_status_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle2).perform()
            time.sleep(2)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        try:
            toggle3 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.enable_page_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle3).perform()
            time.sleep(2)
        except Exception as e:
          print(f"An unexpected error occurred: {e}")

       
        

        save=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.submit_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save) 
        save.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Landing page details Updated successfully.", attachment_type=AttachmentType.PNG)
    
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 








    