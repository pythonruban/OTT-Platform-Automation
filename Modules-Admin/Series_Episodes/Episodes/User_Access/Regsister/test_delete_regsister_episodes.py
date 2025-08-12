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

class TestSeries_EpisodesUserAccess:

    driver = webdriver.Firefox
    
      #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "10801620.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "16.9.jpg")
    videoFile_path = os.path.join(base_dir, "sample_video.mp4")
    vttfile_path = os.path.join(base_dir, "vttfile.vtt") 
    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    Series_episodes_element = "//div[@data-bs-target='#Series-Episode']"
    all_series_element = "//span[text()='All Series']"
    edit_element ="(//span[contains(@class, 'editdropdown-button')])[1]"
    edit_menu = "(//span[contains(text(), 'Edit')])[1]"

    #episodes 
    Manage_episode_element ="(//span[contains(@class, 'editdropdown-button')])[1]"
    episodes_menu = "(//span[contains(text(), 'Manage Episode')])[1]"
      #edit video 
    Edit_video_menu_element = "(//span[contains(@class, 'editdropdown-button')])[1]"
    delete_video_elemnt ="(//span[contains(text(), 'Delete')])[1]"
    confrim_delete ="(//button[@id='adminButton'])[2]"


    def test_delete_regsister_episodes(self,browser_setup):
        self.driver = browser_setup
        """Navigate and add a Live Stream """
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
            print(" Scrolled to bottom of the page.")
            
        except Exception as e:
            
            print(f" Failed to scroll the page: {e}")

# W
        try:
            all_series = WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, self.Series_episodes_element))
             )
            self.driver.execute_script("arguments[0].click();", all_series)
            print(" Navigated to 'Live Stream Management'")
        except Exception as e:
            print(f" Failed to click 'Live Stream Management': {e}")
   
            

        try:
            add_series_button = WebDriverWait(self.driver, 45).until(
            EC.presence_of_element_located((By.XPATH, self.all_series_element))
        )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_series_button)
            time.sleep(1)  # Smooth scroll
            self.driver.execute_script("arguments[0].click();", add_series_button)
            print(" Clicked 'Add New live stream'")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to click 'Add New live stream': {e}")

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
            # ====== EDIT ELEMENT ======
            Manage_episodes = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.Manage_episode_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Manage_episodes)
            time.sleep(3)

            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.Manage_episode_element)
            actions.move_to_element(element_to_hover).perform()
            time.sleep(2)

            # ====== EDIT MENU ======
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.episodes_menu))
            ).click()
            time.sleep(6)

            print(" Manage Episodes element and menu interaction succeeded.")
        
        except Exception as e:
            print(f" Failed to interact with edit element or menu: {e}")

        try:
            # ====== EDIT ELEMENT ======
            EDit_video = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.Edit_video_menu_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", EDit_video)
            time.sleep(3)

            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.Edit_video_menu_element)
            actions.move_to_element(element_to_hover).perform()
            time.sleep(2)

            # ====== EDIT MENU ======
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.delete_video_elemnt))
            ).click()
            time.sleep(6)

            print(" Manage Episodes element and menu interaction succeeded.")
        
        except Exception as e:
            print(f" Failed to interact with edit element or menu: {e}")

        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.confrim_delete))
            ).click()
            print("Episodes was deleted successfully")
            time.sleep(2)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name=" The specific live video was successfully deleted from the All Episodes page.", attachment_type=AttachmentType.PNG)
            time.sleep(6)
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Delete didn’t work — it showed an error.",attachment_type=AttachmentType.PNG)
           
    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")
 
