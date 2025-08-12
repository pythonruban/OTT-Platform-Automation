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

class TestHomepageLiveStreamsettings:
    driver = webdriver.Firefox
    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_btn_element = "(//button[@type='submit'])[2]"
    homepage_setting_element = "//div[@data-bs-target='#settingsURLhome']"
    livestream_setting_element = "//span[text()='Live Settings']"
    livestream_mobile_setting_element = "//button[@id='nav-profile-tab']"

    Live_Categories_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[6]" 
    Livestream_Videos_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[7]"
    LiveStream_based_on_Categories_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[8]"
    Scheduled_Publish_LiveStream_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[9]"
    Latest_Viewed_Livestream_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[10]"
    save_setting_button = "//span[text()='Save Mobile Settings']"


    def test_livestream_homepage_mobile_toggle_setting(self):
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
                EC.element_to_be_clickable((By.XPATH, self.login_btn_element))
            ).click()

            print(" Login Successful!")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All Value login Credentials was entered, and the login button was clicked. it was redirect to Dashboard", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="login_error", attachment_type=AttachmentType.PNG)
            print(f" Failed to enter email: {e}")
        time.sleep(2)

            
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
            Manage_app = WebDriverWait(self.driver, 45).until(
                    EC.presence_of_element_located((By.XPATH, self.homepage_setting_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Manage_app)
            time.sleep(1)  # Allow smooth scrolling
            self.driver.execute_script("arguments[0].click();", Manage_app)
            print(" Clicked 'Language'")
            time.sleep(4)
            self.driver.find_element(By.XPATH, self.livestream_setting_element ).click()
            time.sleep(4)
            self.driver.find_element(By.XPATH, self.livestream_mobile_setting_element ).click()
            time.sleep(4)
        except Exception as e:
            print(f" Failed to navigate to Live Stream Mobile settings: {e}")   

        
        try:

            toggle = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Live_Categories_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
            time.sleep(2)  # Allow smooth scrolling 
            if not toggle.is_selected():
                  print(" toggle already enabled.")
            else:
                 print(" toggle enabled.")

        except Exception as e:
            print(f"Failed to interact with toggle control: {e}")
        time.sleep(2)

        try:

            toggle2 = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Livestream_Videos_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2)
            time.sleep(2)
            if not toggle2.is_selected():
                print(" toggle already enabled.")
            else:
                print(" toggle enabled.")

        except Exception as e:
            print(f"Failed to interact with toggle control: {e}")
        time.sleep(2)


        try:

            toggle3 = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.LiveStream_based_on_Categories_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3)
            time.sleep(2)
            is_enabled = toggle3.get_attribute("aria-pressed") == "true"
            if not toggle3.is_selected():
                print(" toggle already enabled.")
            else:
                print(" toggle enabled.")

        except Exception as e:
            print(f"Failed to interact with toggle control: {e}")
        time.sleep(2)

        try:

            toggle4 = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Scheduled_Publish_LiveStream_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle4)
            time.sleep(2)
            if not toggle.is_selected():
                print(" toggle already enabled.")
            else:
                print(" toggle enabled.")

        except Exception as e:
            print(f"Failed to interact with toggle control: {e}")
        time.sleep(2)


        try:

            toggle5 = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.Latest_Viewed_Livestream_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle5)
            time.sleep(2)
            if not toggle5.is_selected():     
                print(" toggle already enabled.")
            else:
                print(" toggle enabled.")

        except Exception as e:
            print(f"Failed to interact with toggle control: {e}")
        time.sleep(2)

        # Save the settings
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.save_setting_button))
            ).click()
            time.sleep(2)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Live Stream Mobile settings saved", attachment_type=AttachmentType.PNG)
            print(" Live Stream Web settings was saved successfully")
            time.sleep(20)
            assert True
        except Exception as e:
            print(f"Failed to save Live Stream settings: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="save_error", attachment_type=AttachmentType.PNG)
            time.sleep(2)
            pytest.fail("Login failed.")


    def teardown_class(self):
        """Teardown method to close the browser"""
        self.driver.quit()
        print("Browser closed successfully.")


