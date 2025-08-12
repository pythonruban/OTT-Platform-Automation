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
class TestAdvertiser:
    driver = webdriver.Firefox
    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    Advertiser_category_element = "//span[text()='Ads Categories']"
    edit_element ="(//span[contains(@class, 'editdropdown-button')])[1]"
    edit_menu = "(//span[contains(text(), 'Edit')])[1]"
    name_element = "//input[@name='AdsCategories_name']"
    slug_element = "//input[@name='AdsCategories_slug']"
    status_element = "//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')]"
    Add_category_button_element = "//button[@type='submit' and contains(@class,'btn-primary') and normalize-space()='Add Category']"

    def test_advertiser(self,browser_setup):
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
            Advertiser = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.Advertiser_category_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Advertiser)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", Advertiser)
            time.sleep(2)

            print("Navigated to 'Advertiser'")
        except Exception as e:
            print(f"[ERROR] Clicking 'Advertiser' failed: {e}")

        try:
            # ====== EDIT ELEMENT ======
            edit = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit)
            time.sleep(3)

            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.edit_element)
            actions.move_to_element(element_to_hover).perform()
            time.sleep(2)

            # ====== EDIT MENU ======
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.edit_menu))
            ).click()
            time.sleep(6)

            print(" Edit element and menu interaction succeeded.")
        
        except Exception as e:
            print(f" Failed to interact with edit element or menu: {e}")


        try:    
            # Generate a random uppercase string of length between 5 and 7
            length = random.randint(5, 7)
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")

            print(f"Using XPath: {self.title_element}")

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
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="name_error", attachment_type=AttachmentType.PNG)
            print(f"An error occurred while entering 'Name': {e}")

        try:
    
            print(f"Using XPath for slug input: {self.slug_element}")

            slug = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.slug_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slug)
            time.sleep(2)
            slug.clear()
            time.sleep(2)
            slug.send_keys(auto_name)
            time.sleep(2)
            print(" Auto slug entered using the name.")

        except Exception as e:
                print(f" Failed to enter slug: {e}")
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="slug_error", attachment_type=AttachmentType.PNG)
            print(f"An error occurred while entering 'Slug': {e}")

        try:
            status = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.status_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", status)
            time.sleep(3)
            status_class = status.get_attribute("class")
            if "active" in status_class.lower():
                print(" 'Status' toggle already active. Skipped.")
            else:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.status_element))
                )
                self.driver.execute_script("arguments[0].click();", status)
                print(" 'Status' toggle was OFF, now turned ON.")
        except Exception as e:
            print(f" Error handling 'Status' toggle: {e}")
        
        try:    
            Add_category_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.Add_category_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Add_category_button)
            time.sleep(1)
            Add_category_button.click()
            time.sleep(2)
            print("Category added successfully.") 
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Add_category_button_success", attachment_type=AttachmentType.PNG)  
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Add_category_button_error", attachment_type=AttachmentType.PNG)
            print(f"An error occurred while clicking 'Add Category' button: {e}")

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 