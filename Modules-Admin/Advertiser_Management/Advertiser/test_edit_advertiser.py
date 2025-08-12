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
    Advertiser_element = "//span[text()='Advertiser']"
    edit_element ="(//span[contains(@class, 'editdropdown-button')])[1]"
    edit_menu = "(//span[contains(text(), 'Edit')])[1]"
    Advertiser_name = "//input[@name='company_name']"
    email_element ="//input[@name='email_id']"
    password_element="//input[@name='password']"
    country_code_elemnt ="//select[@name='ccode']"
    mobile_number_element = "//input[@name='mobile_number']"
    license_number_elemnt ="//input[@name='license_number']"
    address_element= "//input[@name='address']"
    status_element = "//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')]"

    def test_advertiser(self,browser_setup):
        self.driver = browser_setup
        """Login to the admin panel"""
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()
        actions = ActionChains(self.driver)
        wait = WebDriverWait(self.driver, 30)

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
                EC.presence_of_element_located((By.XPATH, self.Advertiser_element))
            )
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
            # Generate random name
            auto_name = ''.join(random.choices(string.ascii_uppercase,
                                               k=random.randint(5, 7)))
            allure.attach(auto_name, "Generated Name", AttachmentType.TEXT)

            name_field = wait.until(EC.element_to_be_clickable((By.XPATH, self.Advertiser_name)))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", name_field)
            name_field.clear()
            name_field.send_keys(auto_name)
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(),
                          name="modal_submit_error", attachment_type=AttachmentType.PNG)
        try:
            email = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.email_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", email)
            time.sleep(2)
            email.clear()
            time.sleep(2)  # small delay to ensure field is cleared
            email.send_keys("https://www.facebook.com")
            time.sleep(2)
            print(" Target link entered in the target link field.")
        except Exception as e:
            print(f" Failed to enter target link: {e}")
        try:

            toggle = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.status_element))
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

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 