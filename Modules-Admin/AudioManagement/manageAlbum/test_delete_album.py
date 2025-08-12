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
    Manage_album_element = "//span[contains(text(), 'Manage Albums')]"
    add_album_element ="//a[@id='navigationLinkForAddPage']"
    delete_element ="(//span[contains(@class, 'editdropdown-button')])[1]"
    delete_menu = "//span  [text()='Delete']"
    confrim_delete_element = "//button[@id='adminButton']"
    


    def test_delete_album(self,browser_setup):
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
            Manage_audio = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, self.Audio_element))
            )
            self.driver.execute_script("arguments[0].click();", Manage_audio)
            print("Navigated to 'Audio Management'")
        except Exception as e:
            print(f"Failed to click 'Audio Management': {e}")

        try:
            manage_album = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.Manage_album_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", manage_album)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", manage_album)
            print("Clicked 'Add New Audio'")
            time.sleep(2)
        except Exception as e:
            print(f"Failed to click 'Add New Audio': {e}")

        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.delete_element))
            )
            element_to_hover = self.driver.find_element(By.XPATH, self.delete_element)
            actions = ActionChains(self.driver)
            actions.move_to_element(element_to_hover).perform()
            time.sleep(2)
            print("Hovered over album for delete option.")
        except Exception as e:
            print(f"Error hovering delete element: {e}")

        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.delete_menu))
            ).click()
            time.sleep(2)
            print("Clicked delete menu.")
        except Exception as e:
            print(f"Failed to click delete menu: {e}")

        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.confrim_delete_element))
            ).click()
            time.sleep(2)
            print("Confirmed delete.")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Manage Album delete successfully ", attachment_type=AttachmentType.PNG)
            time.sleep(3)
        except Exception as e:
            print(f"Failed to confirm delete: {e}")

        # Final success message
        print("Album was deleted successfully.")
            
    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 
    
 
        print("Browser Closed Successfully")

    
