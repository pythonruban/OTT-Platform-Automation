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
class TestLanguage:

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    Manage_language_element = "//span[text()='Manage Language']"
    translate_element = "//span[text()='Manage Translations']"
    translation_delete_button_element = "(//td[contains(@class, 'theme-bg-color')]//button[contains(text(), 'Delete')])[2]"
    confrim_delete_button = "//span[contains(text(), 'Delete')]"

    def test_delete_Translation(self,browser_setup):
        self.driver = browser_setup
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

        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            manage_lang = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.Manage_language_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", manage_lang)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", manage_lang)
            print("Clicked 'Language'")
            time.sleep(3)
        except Exception as e:
            print(f"Failed to click Language&Translation: {e}")
            pytest.fail(f"Login failed: {e}")

        try:
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.translate_element))
            )
            element.click()
            time.sleep(2)
            print("Element clicked successfully.")
        except Exception as e:
            print(f"An unexpected exception occurred: {e}")

        try:
            delete_btn = WebDriverWait(self.driver, 90).until(
                EC.element_to_be_clickable((By.XPATH, self.translation_delete_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", delete_btn)
            time.sleep(2)
            delete_btn.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error while trying to click the delete button: {e}")

        try:
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.confrim_delete_button))
            ).click()
            print("Subtitle was deleted successfully.")
            time.sleep(4)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Manage Translation the data was Delete successfully", attachment_type=AttachmentType.PNG)

        except (TimeoutException, NoSuchElementException, Exception) as e:
            allure.attach(
            self.driver.get_full_page_screenshot_as_png(),
            name="Failed to delete subtitle",
            attachment_type=AttachmentType.PNG
            )
            print(f"Error while trying to delete the subtitle: {e}")

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")   
