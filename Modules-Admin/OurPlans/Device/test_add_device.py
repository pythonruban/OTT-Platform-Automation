import time
import re 
import random
import string
import pytest 
import os
import sys 
import allure 


 
from conftest import *
from selenium.webdriver import ActionChains, Keys
from allure_commons.types import AttachmentType
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from utilities.readProp import ReadConfig

# Add the project root (D:\Automation\) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

    

@pytest.mark.usefixtures("browser_setup")
class TestOurPlans:
    driver = webdriver.Firefox
    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    plans_element = "//span[text()='Plans']"
    device_element = "//span[text()='Devices']"
    add_device_button_element = "//button//span[text()='Add Device']"
    device_name_element = "//input[@name='devices_name']"
    #save
    device_added_element= "(//span[text()='Add Device'])[2]"
    
    
    def test_add_device(self,browser_setup):
        self.driver = browser_setup
        """Login to the admin panel"""
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()
        actions = ActionChains(self.driver)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.email_element))
            ).send_keys(ReadConfig.getAdminId())

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.password_element))
            ).send_keys(ReadConfig.getPassword())

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.login_element))
            ).click()

            print(" Login Successful!")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All Value login Credentials was entered, and the login button was clicked. it was redirect to Dashboard", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="login_error", attachment_type=AttachmentType.PNG)
            print(f" Failed to enter email: {e}")
        time.sleep(2)
    
        
        try:

            

            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                plans = WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, self.plans_element))
                )
                self.driver.execute_script("arguments[0].click();", plans)
                print("Navigated to 'Player Setting Management'")
            except Exception as e:
                print(f"[ERROR] Clicking 'Player Setting Management' failed: {e}")

            try:
                device = WebDriverWait(self.driver, 45).until(
                    EC.presence_of_element_located((By.XPATH, self.device_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", device)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", device)
                print("Clicked 'DEVICES'")
                time.sleep(6)
            except Exception as e:
                print(f"[ERROR] Interacting with 'DEVICES' failed: {e}")

            try:
                WebDriverWait(self.driver, 45).until(
                    EC.presence_of_element_located((By.XPATH, self.add_device_button_element))
                ).click()
                time.sleep(2)
            except Exception as e:
                print(f"[ERROR] Clicking 'Add Device' button failed: {e}")

            try:
                # Generate a random uppercase string of length between 5 and 7
                length = random.randint(5, 7)
                auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
                print(f"Generated name: {auto_name}")

                print(f"Using XPath: {self.device_name_element}")

                # Wait for the title input to be clickable
                name = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, self.device_name_element))
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


            try:
                WebDriverWait(self.driver, 45).until(
                    EC.presence_of_element_located((By.XPATH, self.device_added_element))
                ).click()
                time.sleep(5)
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name="BillingTypeEmpty", attachment_type=AttachmentType.PNG)
                print("Device was added in the plan successfully")
                assert True
            except Exception as e:
                print(f"[ERROR] Final device confirmation failed: {e}")
                assert False
                


        except Exception as e:
                  print(f" Login failed: {e}")
                  pytest.fail(f"Login failed: {e}")

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")


   

 