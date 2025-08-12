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
    life_subscription_element = "//span[text()='Life Time Subscription']"
    name_element = "//input[@name='name']"
    price_element = "//input[@name='price']"
    #Status Settings
    plan_status_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[1]"
    #Devices 
    laptop_element ="(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[2]"
    mobile_element ="(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[3]"
    TV_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[4]"
    #save
    update_plan_element= "//span[text()='Update Plan']"
    
    def test_lifetime_subcription(self,browser_setup):
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

        # Scroll to load all elements
        
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
            print(f"[ERROR] Clicking 'Player Setting Management' failed: {e}")

        # Click "Lifetime Subscription"
        try:
            subscription = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.life_subscription_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", subscription)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", subscription)
            print("Clicked 'Lifetime Subscription'")
            time.sleep(6)
        except Exception as e:
            print(f"[ERROR] Clicking 'Lifetime Subscription' failed: {e}")

        # Enter Name
        try:
            # Generate a random uppercase string of length between 5 and 7
            length = random.randint(5, 7)
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")

            print(f"Using XPath: {self.name_element}")

            # Wait for the title input to be clickable
            name = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.name_element))
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

        # Enter Price
        try:
            price = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.price_element))
            )
            price.clear()
            time.sleep(2)
            price.send_keys("499")
            time.sleep(2)
        except Exception as e:
            print(f"[ERROR] Entering price failed: {e}")

        # Plan status toggle
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

        # Laptop toggle
        try:

            toggle = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.laptop_element))
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

        # Mobile toggle
        try:

            toggle2 = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.mobile_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2)
            is_enabled = toggle2.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                toggle2.click()
                print(" toggle already enabled.")
            else:
                toggle2.click()
                print(" toggle enabled.")

        except Exception as e:
            print(f"Failed to interact with toggle control: {e}")
        time.sleep(2)

        # TV toggle (commented block)
        try:

            toggle3 = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.TV_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3)
            is_enabled = toggle3.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                toggle3.click()
                print(" toggle already enabled.")
            else:
                toggle3.click()
                print(" toggle enabled.")

        except Exception as e:
            print(f"Failed to interact with toggle control: {e}")
        time.sleep(2)

        # Click Update button
        try:
            WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.update_plan_element))
            ).click()
            time.sleep(10)
            print("✅ Device was added in the plan successfully")
        except Exception as e:
            print(f"[ERROR] Clicking update plan button failed: {e}")



    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")