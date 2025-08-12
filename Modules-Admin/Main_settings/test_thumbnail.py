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
class Test_Enable_Comment:
   
    driver: WebDriver

     
       #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "1080x1080.jpg")

      # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    settings_element="//span[text()='Settings']"
    thumbnail_element="//span[text()='Thumbnail Settings']"

    enable_title_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    enable_age_element="(//span[@class='admin-slider position-absolute admin-round '])[2]"
    enable_rating_element="(//span[@class='admin-slider position-absolute admin-round '])[3]"
    enable_pubyear_element="(//span[@class='admin-slider position-absolute admin-round '])[4]"
    enable_pubon_element="(//span[@class='admin-slider position-absolute admin-round '])[5]"
    enable_duration_element="(//span[@class='admin-slider position-absolute admin-round '])[6]"
    enable_featured_element="(//span[@class='admin-slider position-absolute admin-round '])[7]"
    enable_cost_element="(//span[@class='admin-slider position-absolute admin-round '])[8]"
    enable_category_element="(//span[@class='admin-slider position-absolute admin-round '])[9]"
    enable_trailer_element="(//span[@class='admin-slider position-absolute admin-round '])[10]"
    enable_reels_element="(//span[@class='admin-slider position-absolute admin-round '])[11]"
    enable_description_element="(//span[@class='admin-slider position-absolute admin-round '])[12]"
    image_element="//div[@class='imagedrop']/input[@type='file']"

    update_element=" //span[text()='Update Settings']"
                                                       
    def test_Enable_Comment(self,browser_setup):
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

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.thumbnail_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()

        try:
            toggle = self.driver.find_element(By.XPATH, self.enable_title_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))   


        try:
            toggle1 = self.driver.find_element(By.XPATH, self.enable_age_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle1).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))   


        try:
            toggle2 = self.driver.find_element(By.XPATH, self.enable_rating_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle2).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))  

        try:
            toggle3 = self.driver.find_element(By.XPATH, self.enable_pubyear_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle3).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))    

        try:
            toggle4 = self.driver.find_element(By.XPATH, self.enable_pubon_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle4)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle4).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e)) 

        try:
            toggle5 = self.driver.find_element(By.XPATH, self.enable_duration_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle5)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle5).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))  


        try:
            toggle6 = self.driver.find_element(By.XPATH, self.enable_featured_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle6)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle6).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))    

        try:
            toggle7 = self.driver.find_element(By.XPATH, self.enable_cost_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle7)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle7).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle8 = self.driver.find_element(By.XPATH, self.enable_category_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle8)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle8).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))     
            
        try:
            toggle9 = self.driver.find_element(By.XPATH, self.enable_trailer_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle9)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle9).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle10 = self.driver.find_element(By.XPATH, self.enable_reels_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle10)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle10).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle11 = self.driver.find_element(By.XPATH, self.enable_description_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle11)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle11).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        # Upload Image
        ime=WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, self.image_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ime)  
        self.driver.execute_script("arguments[0].style.display = 'block';", ime) 
        time.sleep(1)
        ime.send_keys(self.image_path_1)
        time.sleep(2)

        save=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save) 
        time.sleep(2)  
        save.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Thumbnail Settings in Main Settings details Saved successfully.", attachment_type=AttachmentType.PNG)
    
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")     
        
          
         
         

