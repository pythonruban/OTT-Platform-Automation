import time
import allure
import pytest
import os

 
from conftest import *
from allure_commons.types import AttachmentType
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
 
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
class Test_Image:
   
    driver: WebDriver

      # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    settings_element="//span[text()='Settings']"
    image_element="//span[text()='Image Settings']"
    compress_size_element="//input[@id='inputField']"
    compress_format_element="//select[@id='selectField']"

    enable_image_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    enable_compress_element="(//span[@class='admin-slider position-absolute admin-round '])[2]"

    enable_video_element="(//span[@class='admin-slider position-absolute admin-round '])[3]"
    enable_livevideos_element="(//span[@class='admin-slider position-absolute admin-round '])[4]"
    enable_series_element="(//span[@class='admin-slider position-absolute admin-round '])[5]"
    enable_season_element="(//span[@class='admin-slider position-absolute admin-round '])[6]"
    enable_episode_element="(//span[@class='admin-slider position-absolute admin-round '])[7]"
    enable_audio_element="(//span[@class='admin-slider position-absolute admin-round '])[8]"

    update_element="//span[text()='Save Settings']"
    


    def test_image(self,browser_setup):
        self.driver = browser_setup
        self.driver.maximize_window()
        self.driver.get(ReadConfig.getAdminPageURL())

        # Login to the application
        self.driver.find_element(By.XPATH, self.email_element).send_keys(ReadConfig.getAdminId())
        self.driver.find_element(By.XPATH, self.password_element).send_keys(ReadConfig.getPassword())
        self.driver.find_element(By.XPATH, self.login_element).click()

        try:
            WebDriverWait(self.driver, 80).until(EC.visibility_of_element_located((By.XPATH, self.dashboard_element))).click()
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login was successful and the UI elements have been loaded.", attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login successful and the UI elements have not loaded due to timeout", attachment_type=AttachmentType.PNG)
            raise e
        
           # Scroll to ensure all elements are loaded
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.settings_element)))
        user = self.driver.find_element(By.XPATH, self.settings_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.image_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()

        ag=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.compress_size_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ag)
        time.sleep(1) 
        ag.clear()
        time.sleep(2)
        ag.send_keys("100")
        time.sleep(3)

        try :
            drop_down1= WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, self.compress_format_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down1) 
            #drop_down1.click()
            time.sleep(2)
            select = Select(drop_down1)
            select.select_by_value("WebP")
        except Exception as e:
            print("select a value:", str(e))

        try:
            toggle = self.driver.find_element(By.XPATH, self.enable_image_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))      

        try:
            toggle1 = self.driver.find_element(By.XPATH, self.enable_compress_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle1).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))    

        try:
            toggle2 = self.driver.find_element(By.XPATH, self.enable_video_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle2).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))             

        try:
            toggle3 = self.driver.find_element(By.XPATH, self.enable_livevideos_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle3).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e)) 


        try:
            toggle4 = self.driver.find_element(By.XPATH, self.enable_series_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle4)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle4).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))   

        try:
            toggle5 = self.driver.find_element(By.XPATH, self.enable_season_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle5)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle5).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))             

        try:
            toggle6 = self.driver.find_element(By.XPATH, self.enable_episode_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle6)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle6).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))             

        try:
            toggle7 = self.driver.find_element(By.XPATH, self.enable_audio_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle7)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle7).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))      
            
        save_element=WebDriverWait(self.driver, 80).until(
        EC.presence_of_element_located((By.XPATH, self.update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Image Settings in Main Settings details Updated successfully.", attachment_type=AttachmentType.PNG)       

        
    def teardown_class(self):
        "Close the browser"
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  

