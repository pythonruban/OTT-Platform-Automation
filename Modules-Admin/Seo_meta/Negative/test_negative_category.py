import time
import allure
import pytest
import os
import random
import string
 
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
class TestNegativeCategory:
   
    driver: WebDriver

       #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "1691.jpg")

     # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    manage_element="//span[text()='Manage FAQ']"
    faq_category_element="(//span[text()='FAQ Category'])[1]"

    add_category_element="//span[text()='Add Categories']"


    title_element="(//input[@id='inputField'])[1]"
    slug_element="(//input[@id='inputField'])[2]"
    genre_element="//select[@id='selectField']"
    image_element="//input[@id='fileId']"
    submit_element="(//span[text()='Add Categories'])[2]"
    

          
    dot2_element="(//span[@class='editdropdown-button'])[1]"
    edit2_element="(//span[text()=' Edit'])[1]"
    
    manage_element="//span[text()='Manage Season & Episodes']"
    season_element="//span[text()='Create Season']"
    title_element="//input[@id='edit-series-tile-modal']"
    image_element="//input[@id='edit-series-fileInputRef4']"
    user_element="//select[@id='season-access']"
    submit_element="(//span[text()='Edit Season'])[2]"
    

    
        
    def test_Negative_category(self,browser_setup):

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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.manage_element)))
        user = self.driver.find_element(By.XPATH, self.manage_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        # Scroll to ensure all elements are loaded
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.faq_category_element)))
        faq = self.driver.find_element(By.XPATH, self.faq_category_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", faq)
        time.sleep(2)
        faq.click()


        # Scroll to ensure all elements are loaded
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.add_category_element)))
        add = self.driver.find_element(By.XPATH, self.add_category_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add)
        time.sleep(2)
        add.click()

        WebDriverWait(self.driver,80).until(EC.presence_of_element_located((By.XPATH, self.dot_element))).click()

        WebDriverWait(self.driver,80).until(EC.presence_of_element_located((By.XPATH, self.edit_element))).click()
        time.sleep(2)

        manage=WebDriverWait(self.driver,120).until(EC.presence_of_element_located((By.XPATH, self.manage_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", manage)
        time.sleep(2)



        try :
            tit=WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.title_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tit)
            tit.send_keys("")
            time.sleep(2)         

        except Exception as e:
            print(f" Failed to enter title: {e}")
        
        
        try :
            slug=WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.slug_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slug)
            slug.send_keys("")
            time.sleep(2)
        
        except Exception as e:
            print(f" Failed to enter title: {e}")

              
# Select user role Dropdown
        try :
            drop_down1= WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, self.genre_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down1) 
            time.sleep(2)
            select = Select(drop_down1)
            select.select_by_visible_text("Select an Genre")
        
        except Exception as e:
            print(f" Failed to enter title: {e}")


           # Image  
        try :
            image1 =WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, self.image_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image1)
            image1.send_keys(self.image_path_1)
            time.sleep(2)
        except Exception as e:
            print(f" Failed to enter title: {e}")

           # update or save element
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.submit_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name=" Manage FAQ Category details Added successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 