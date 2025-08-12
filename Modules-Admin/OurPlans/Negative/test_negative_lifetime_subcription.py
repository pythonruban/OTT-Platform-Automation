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
    
    def test_negative_lifetime_subcription(self,browser_setup):
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
            test_data = [
                ("Test 1: 1-char (Negative Title)", ''.join(random.choices(string.ascii_uppercase, k=1))),
                ("Test 2: 202-char (Negative Title)", ''.join(random.choices(string.ascii_uppercase + string.digits, k=102))),
                ("Test 3: Auto Title (Valid)", ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 7))))
            ]    

            for test_name, title_value in test_data:
                try:
                    print(f"\nRunning: {test_name}")

                    # Locate and clear title input
                    title_input = WebDriverWait(self.driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, self.name_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_input)
                    time.sleep(1)
                    title_input.clear()
                    title_input.send_keys(title_value)
                    print(f"Title entered: {title_value[:30]}")

                    # Click Submit button
                    submit_button = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, self.update_plan_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", submit_button)
                    print("Form submitted")

                    # If test is a negative case, take screenshot
                    if "Negative" in test_name:
                        time.sleep(2)
                        screenshot_name = f"screenshots/{test_name.replace(':', '').replace(' ', '_')}.png"
                        self.driver.save_screenshot(screenshot_name)
                        allure.attach.file(screenshot_name, name=test_name, attachment_type=AttachmentType.PNG)
                        print(f"Screenshot captured for negative case: {test_name}")

                    # Optional: Scroll back to title field
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_input)
                    time.sleep(1)

                except Exception as case_error:
                    print(f"{test_name} - Error: {case_error}")

        except Exception as total_error:
            print(f"Outer error in title validation block: {total_error}")

        # Enter Price
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
                    EC.element_to_be_clickable((By.XPATH, self.update_plan_element))
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
                    EC.element_to_be_clickable((By.XPATH, self.update_plan_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                submit_button.click()
                print(f"Submitted with 3-digit price: {valid_price}")
            except Exception as e2:
                print(f"Error during valid price submission: {e2}")

        except Exception as e:
            print(f"Failed to handle price field: {e}")

        # Plan status toggle
        try:
            toggle = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.plan_status_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
            time.sleep(1)

            is_enabled = self.driver.execute_script("return arguments[0].getAttribute('aria-pressed');", toggle) == "true"

            self.driver.execute_script("arguments[0].click();", toggle)
            if not is_enabled:
                print("Toggle was OFF, now clicked to ON.")
            else:
                print("Toggle was ON, now clicked to OFF.")

        except Exception as e:
            print(f"Failed to interact with toggle control: {e}")

        # Laptop toggle
        try:
            toggles = {
                "Laptop": self.laptop_element,
                "Mobile": self.mobile_element,
                "TV": self.TV_element
            }

            for label, xpath in toggles.items():
                try:
                    toggle = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
                    time.sleep(1)

                    # Use JS to read aria-pressed safely
                    aria_pressed = self.driver.execute_script("return arguments[0].getAttribute('aria-pressed');", toggle)
                    is_enabled = aria_pressed == "true"

                    if is_enabled:
                        self.driver.execute_script("arguments[0].click();", toggle)  # JS click
                        print(f"{label} toggle was ON — now turned OFF via JS.")
                    else:
                        print(f"{label} toggle already OFF.")
                    time.sleep(1)

                except Exception as toggle_err:
                    print(f"Failed to handle {label} toggle: {toggle_err}")

            # Click Submit
            try:
                submit_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.update_plan_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", submit_btn)
                print("Submitted with all toggles OFF.")
            except Exception as submit_err:
                print(f"Failed to click submit button: {submit_err}")

            # Screenshot for validation error
            time.sleep(2)
            
            allure.attach(self.driver.get_screenshot_as_png(), name="AllTogglesOff", attachment_type=AttachmentType.PNG)
            print("Screenshot taken for all toggles OFF validation.")

        except Exception as e:
            print(f"Test failed with error: {e}")
        # Click Update button
        try:
            WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.update_plan_element))
            ).click()
            time.sleep(10)
            print("✅ Device was added in the plan successfully")
        except Exception as e:
            print(f"[ERROR] Clicking update plan button failed: {e}")



    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 
        print("Browser closed successfully.")