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
    Manage_app_plans_element = "//span[text()='Manage In App Purchase Plans']"
    add_plan_element = "//span[text()='Add Plan']"
    price_element= "//input[@name='plan_price']"
    product_id_element ="//input[@name='product_id']"
    #Status Settings
    plan_status_element = "//p[contains(@class, 'indicator-on-off') and contains(@class, 'on')]"
    #save
    save_purchase_element= "//span[text()='Save Purchase']"
    
    def test_add_plan(self,browser_setup):
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

        # Navigate to Plans
        
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            plans = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.plans_element))
            )
            self.driver.execute_script("arguments[0].click();", plans)
            print(" Navigated to 'Player Setting Management '")
            time.sleep(2)
        except Exception as e:
            print(f" Failed to click 'Plans': {e}")

        try:
            Manage_app = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.Manage_app_plans_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Manage_app)
            time.sleep(1)  # Allow smooth scrolling
            self.driver.execute_script("arguments[0].click();", Manage_app)
            print(" Clicked 'Manage app purchase plans'")
            time.sleep(6)
        except Exception as e:
            print(f" Failed to click 'Manage In App Purchase Plans': {e}")

        # edit menu
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.add_plan_element))
            ).click()
            time.sleep(2)
        except Exception as e:
            print(f" Failed to click 'Add Plan': {e}")

        try:
            price = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.price_element))
            )
            price.clear()
            time.sleep(2)
            price.send_keys("1499")
            time.sleep(2)
        except Exception as e:
            print(f" Failed to enter price: {e}")

        try:
            product = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.product_id_element))
            )
            product.clear()
            time.sleep(2)
            product.send_keys("QWERTY!@1234")
            time.sleep(2)
        except Exception as e:
            print(f" Failed to enter product ID: {e}")

        # Status Settings
        try:

            toggle = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.plan_status_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
            is_enabled = toggle.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                toggle.click()
                print(" toggle already enabled.")
            else:
                toggle.click()
                print(" toggle enabled.")

        except Exception as e:
            print(f"Failed to interact with toggle control: {e}")
        time.sleep(2)

        try:
            WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.save_purchase_element))
            ).click()
            time.sleep(10)
            print(" Edited the plan successfully")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Plan added successfully", attachment_type=AttachmentType.PNG)
        except Exception as e:
            print(f" Failed to save purchase: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Plan save error", attachment_type=AttachmentType.PNG)
            pytest.fail(f"Plan save failed: {e}")           

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")