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
class TestNegativefaq:
   
    driver: WebDriver

     # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    manage_element="//span[text()='Manage FAQ']"
    faq_element="//span[text()='FAQ']"

    add_category_element="(//span[text()='Add FAQ'])[1]"

    faq_question_element="//input[@id='inputField']"
    faq_answer_element="//textarea[@id='customArea']"
    genre_element="//select[@id='selectField']"
    submit_element="(//span[text()='Add FAQ'])[2]"
    


    
          
    def test_Negative_faq(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.manage_element)))
        user = self.driver.find_element(By.XPATH, self.manage_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        # Scroll to ensure all elements are loaded
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.faq_element)))
        faq = self.driver.find_element(By.XPATH, self.faq_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", faq)
        time.sleep(2)
        faq.click()

        # Scroll to ensure all elements are loaded
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.add_category_element)))
        add = self.driver.find_element(By.XPATH, self.add_category_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add)
        time.sleep(2)
        add.click()

          # Scroll to ensure all elements are loaded
        try :
            quest=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.faq_question_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", quest)
            time.sleep(2)
            quest.send_keys("")
        except TimeoutException:
            print("Error: The element was not clickable within the given time.")


          # Scroll to ensure all elements are loaded
        try :
            answer=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.faq_answer_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", answer)
            time.sleep(2)
            answer.send_keys("")
        except TimeoutException:
            print("Error: The element was not clickable within the given time.")

        try :
            drop_down1= WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, self.genre_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down1) 
            time.sleep(2)
            select = Select(drop_down1)
            select.select_by_visible_text("Select an Genre")
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
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name=" Manage FAQ details Added successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 



       
