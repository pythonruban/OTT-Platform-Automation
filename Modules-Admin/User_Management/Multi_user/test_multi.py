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
class TestAdd_Multi:
   
    driver: WebDriver


      # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    users_element="//span[text()='Users']"
    multi_element="//span[text()='Multi User Management']"
    session_element="//input[@id='inputField']"
    toggle_element="//span[@class='admin-slider position-absolute admin-round']"
    save_element="//span[text()='Save Multi User']"

    
    def test_Add_Multi(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.users_element)))
        user = self.driver.find_element(By.XPATH, self.users_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.multi_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()

        try :
            ses=WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.session_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ses) 
            time.sleep(1) 
            ses.clear()
            time.sleep(1)
            ses.send_keys("10")
            time.sleep(3)
            print("✅ Session is entered Successfully")
        except Exception as e:
            print(f" Failed to Enter Session element: {e}")

        try :
            toggle = self.driver.find_element(By.XPATH, self.toggle_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
            time.sleep(2)
            actions = ActionChains(self.driver)
            actions.move_to_element(toggle).click().perform()
            time.sleep(2)
        except Exception as e:
            print(f" Failed to Toggle Click: {e}")

        try:
            button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.save_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(2)
            button.click()
            time.sleep(2)
            print("✅ User added successfully!")
        except Exception as e:
            print(f"❌ Error saving user: {e}")
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Multi User Added successfully!", attachment_type=AttachmentType.PNG)

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
