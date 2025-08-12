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
class TestMainSettings:
    driver = webdriver.Firefox
    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    Settings_element = "//div[@data-bs-target='#Settings']"
    transcode_job_elemnt ="//span[text()='Transcoding Jobs']"
    Active_element ="//div[contains(@class, 'theme-bg-color')]/h5[text()='Active']"
    Waiting_element ="//div[contains(@class, 'theme-bg-color')]/h5[text()='Waiting']"
    completed_element ="//div[contains(@class, 'theme-bg-color')]/h5[text()='Completed']"
    Failed_element = "//div[contains(@class, 'theme-bg-color')]/h5[text()='Failed']"
    
    
    def test_transcoding_job(self,browser_setup):
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
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            settings = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.Settings_element))
            )
            self.driver.execute_script("arguments[0].click();", settings)
            time.sleep(2)
            Transcode_job = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.transcode_job_elemnt))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Transcode_job)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", Transcode_job)
            print("Navigated to 'OTP Credentails'")
        except Exception as e:
            print(f"[ERROR] Clicking  failed: {e}")

        try:
                    # Active
            try:
                Active = WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, self.Active_element))
                )
                self.driver.execute_script("arguments[0].click();", Active)
                time.sleep(5)
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name="In Transcode Job , The Active Status Page", attachment_type=AttachmentType.PNG)
                time.sleep(3)
                print("The Active Page Clicked Successfully")
            except Exception as e:
                print(f"[ERROR] Clicking Active failed: {e}")

            # Waiting
            try:
                waiting = WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, self.Waiting_element))
                )
                self.driver.execute_script("arguments[0].click();", waiting)
                time.sleep(5)
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name="In Transcode Job , The Waiting Status Page", attachment_type=AttachmentType.PNG)
                time.sleep(3)
                print("The Waiting Page Clicked Successfully")
            except Exception as e:
                print(f"[ERROR] Clicking Waiting failed: {e}")

            # Completed
            try:
                completed = WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, self.completed_element))
                )
                self.driver.execute_script("arguments[0].click();", completed)
                time.sleep(5)
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name="In Transcode Job , The Completed Status Page", attachment_type=AttachmentType.PNG)
                time.sleep(3)
                print("The Completed Page Clicked Successfully")
            except Exception as e:
                print(f"[ERROR] Clicking Completed failed: {e}")

            # Failed
            try:
                failed = WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, self.Failed_element))
                )
                self.driver.execute_script("arguments[0].click();", failed)
                time.sleep(5)
                allure.attach(self.driver.get_full_page_screenshot_as_png(), name="In Transcode Job , The Failed Status Page", attachment_type=AttachmentType.PNG)
                time.sleep(3)
                print("The Failed Page Clicked Successfully")
            except Exception as e:
                print(f"[ERROR] Clicking Failed failed: {e}")

        except Exception as e:
                print(f"[ERROR] Clicking  failed: {e}")
    
    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")