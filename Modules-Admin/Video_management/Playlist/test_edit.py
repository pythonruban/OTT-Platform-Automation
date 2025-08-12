import time
import allure
import pytest
import os
import glob
 
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
class TestPlaylistEdit:
   
    driver: WebDriver
 
           #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "1080.1620.jpg")

    # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH
 

    video_element="//span[text()='Videos']"
    playlist_element="//span[text()='Manage Video Playlist']"
    
    dot_element="(//span[@class='editdropdown-button'])[1]"
    edit_element="(//span[text()='Edit'])[1]"


    edit_title_element="//input[@id='video-playlist-title']"
    edit_slug_element="//input[@id='video-playlist-slug']"
    edit_descrip_element="//textarea[@id='video-playlist-description']"
    edit_image_element="//input[@id='video-playlist-image']"
    update_element="(//span[text()='Update Playlist'])[1]"

  

    
        
    def test_Edit_Playlist(self,browser_setup):
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

          
        WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.dot_element))
            ).click()
        time.sleep(2)

        # single click using WebDriverWait
          
        WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.edit_element))
            ).click()
        time.sleep(2)

              
        ## Clear and send Keys:
         
        text1=self.driver.find_element(By.XPATH, self.edit_title_element)
        text1.clear()
        time.sleep(2)
        text1.send_keys("Beast")
        time.sleep(2)

              
        text2=WebDriverWait(self.driver, 30).until(
               EC.element_to_be_clickable((By.XPATH, self.edit_slug_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", text2)
        text2.clear()
        time.sleep(5)
        text2.send_keys("Movie")
        time.sleep(2)

              
         ## Clear and send Keys:
         
        text3=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.edit_descrip_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", text3)
        text3.click()
        text3.clear()
        time.sleep(5)
        text3.send_keys("A beast is generally understood as an animal, particularly a large or wild one, or a person behaving in a crude, cruel, or savage way.")
        time.sleep(2)

        # upload image
        upload=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.edit_image_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload)
        upload.send_keys(self.image_path_1)
        time.sleep(2)

          # update or save element
        save_element=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(2)
        print("Updated successfully!")
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Playlist User details Updated successfully.", attachment_type=AttachmentType.PNG)
    
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 

