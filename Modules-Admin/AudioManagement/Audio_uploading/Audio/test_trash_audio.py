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
class TestAudioManagement:

    driver = webdriver.Firefox
    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    Audio_element = "//div[@data-bs-target='#Audio-Management']"
    add_audio_element = "//span[text()='All Audios']"
    delete_element ="(//span[contains(@class, 'editdropdown-button')])[1]"
    delete_menu = "(//span[text()='Delete'])[1]"
    confrim_delete = "(//button[span[text()='Delete']])[1]"

 

    def test_trash_audio(self,browser_setup):
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

            # Scroll to ensure all elements are loaded
        # Scroll to ensure all elements are loaded
        # Click "Audio Management"
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            Manage_audio = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, self.Audio_element))
            )
            self.driver.execute_script("arguments[0].click();", Manage_audio)
            print(" Navigated to 'Audio Management'")
        except Exception as e:
            print(f" Failed to click 'Audio Management': {e}")
            

        # Click "Add New Audio"
        try:
            add_audio_button = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.add_audio_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_audio_button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", add_audio_button)
            print(" Clicked 'Add New Audio'")
            time.sleep(2)
        except Exception as e:
            print(f" Failed to click 'Add New Audio': {e}")
            #edit element
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.delete_element ))
            )
            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.delete_element)
            actions.move_to_element(element_to_hover).perform()
            print(" Hovered over the edit element successfully.")
            time.sleep(2)
        except Exception as e:
            print(f" Failed to hover over edit element: {e}")

        # Wait for and click edit menu
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.delete_menu))
            ).click()
            print(" Clicked on the edit menu successfully.")
            time.sleep(6)
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.confrim_delete))
            ).click()
            print("Audio  Was deleted Successfully  ")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="The Audio was deleted successfully from All audio page", attachment_type=AttachmentType.PNG)
            time.sleep(4)
        except Exception as e:
            print(f" Failed to click the edit menu: {e}")

        


        

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 
    
 
        print("Browser Closed Successfully")

    
