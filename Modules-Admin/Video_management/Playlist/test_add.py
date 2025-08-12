import time
import allure
import pytest
import os
import glob
import random
import string
 
from conftest import *
from allure_commons.types import AttachmentType
 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
 
from utilities.readProp import ReadConfig

 
@pytest.mark.usefixtures("browser_setup")
class TestPlaylist_Add:
   
    driver: WebDriver
 
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 =  os.path.join(base_dir, "1080_1620.jpg")

    # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    video_element="//span[text()='Videos']"
    playlist_element="//span[text()='Manage Video Playlist']"

    add_element="(//span[text()='Video Playlist'])[2]"
    title_element="//input[@id='video-playlist-title']"
    slug_element="//input[@id='video-playlist-slug']"
    description_element="//textarea[@id='video-playlist-description']"
    image_element="//input[@id='video-playlist-image']"


    submit_element="(//span[text()='Add Playlist'])[1]"

    
        
    def test_Add_Playlist(self,browser_setup):
        self.driver = browser_setup
        self.driver.maximize_window()
        self.driver.get(ReadConfig.getAdminPageURL())


        # Login to the application
        self.driver.find_element(By.XPATH, self.email_element).send_keys(ReadConfig.getAdminId())
        self.driver.find_element(By.XPATH, self.password_element).send_keys(ReadConfig.getPassword())
        self.driver.find_element(By.XPATH, self.login_element).click()

        
        try:
            WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.dashboard_element))).click()
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login was successful and the UI elements have been loaded.", attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login successful and the UI elements have not loaded due to timeout", attachment_type=AttachmentType.PNG)
            raise e


        

        # Scroll to ensure all elements are loaded
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.video_element)))
        user = self.driver.find_element(By.XPATH, self.video_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        add_role= self.driver.find_element(By.XPATH, self.playlist_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_role)
        time.sleep(2)
        add_role.click()

        
        # single click using WebDriverWait
          
        WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.add_element))
            ).click()
        time.sleep(2)

          # Send keys using wait Statement
        WebDriverWait(self.driver, 50).until(
               EC.presence_of_element_located((By.XPATH, self.title_element))
            ).send_keys("Kudumbasthan")
        time.sleep(2)

          # Send keys using wait Statement
        WebDriverWait(self.driver, 50).until(
               EC.presence_of_element_located((By.XPATH, self.slug_element))
            ).send_keys("Tamil")
        time.sleep(2)

          # Send keys using wait Statement
        WebDriverWait(self.driver, 50).until(
               EC.presence_of_element_located((By.XPATH, self.description_element))
            ).send_keys("Kudumbasthan, which translates to Family Man, is a 2025 Tamil comedy-drama film. It's directed by Rajeshwar Kalisamy and stars K. Manikandan and Saanve Meghana")
        time.sleep(2)

        
        # upload image
        upload=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.image_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload)
        upload.send_keys(self.image_path_1)
        time.sleep(2)

         
          # update or save element
        save_element=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.submit_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(2)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Playlist Meta details Added successfully.", attachment_type=AttachmentType.PNG)


    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 





