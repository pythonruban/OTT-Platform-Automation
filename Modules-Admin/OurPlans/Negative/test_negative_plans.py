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
    
    def test_negative_plans(self,browser_setup):
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
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", price)

            # First test: Empty input
            try:
                price.clear()
                time.sleep(1)

                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.save_purchase_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                submit_button.click()
                print("Submitted with empty price")

                # Screenshot for empty field
                time.sleep(2)
                
                allure.attach(self.driver.get_screenshot_as_png(), name="empty_price", attachment_type=allure.attachment_type.PNG)
                print("Screenshot taken for empty price field")
            except Exception as e1:
                print(f"Error during empty price submission: {e1}")

            # Second test: Valid 3-digit number (no screenshot)
            try:
                valid_price = str(random.randint(100, 999))
                price.clear()
                time.sleep(1)
                price.send_keys(valid_price)
                time.sleep(1)

                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.save_purchase_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                submit_button.click()
                print(f"Submitted with 3-digit price: {valid_price}")
            except Exception as e2:
                print(f"Error during valid price submission: {e2}")

        except Exception as e:
            print(f"Failed to handle price field: {e}")

        try:
            product = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.product_id_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product)

            # Test case 1: 150 characters (expecting validation error)
            try:
                long_input = ''.join(random.choices(string.ascii_letters + string.digits, k=150))
                product.clear()
                time.sleep(1)
                product.send_keys(long_input)
                time.sleep(1)

                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.save_purchase_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                submit_button.click()
                print("Submitted with 150-character Product ID")

                # Take screenshot of validation error
                time.sleep(2)
                
                allure.attach(self.driver.get_screenshot_as_png(), name="product_id_150char", attachment_type=allure.attachment_type.PNG)
                print("Screenshot taken for 150-character Product ID")
            except Exception as e1:
                print(f"Error during long Product ID test: {e1}")

            # Test case 2: 5-character valid alphanumeric (no screenshot)
            try:
                valid_input = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
                product.clear()
                time.sleep(1)
                product.send_keys(valid_input)
                time.sleep(1)

                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.save_purchase_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                submit_button.click()
                print(f"Submitted with 5-character Product ID: {valid_input}")
            except Exception as e2:
                print(f"Error during valid Product ID test: {e2}")

        except Exception as e:
            print(f"Failed to handle Product ID field: {e}")
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

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 
        print("Browser closed successfully.")
