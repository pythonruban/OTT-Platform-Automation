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
class TestAddGenre:
   
    driver: WebDriver

       #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "1691.jpg")
    image_path_2 = os.path.join(base_dir, "1080.1080.jpg")
   



    
    # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    series_element="(//span[text()='Series & Episodes'])[2]"
    manage_genre_element="//span[text()='Manage Series Genre']"

    add_cate_element="//span[text()='Add Categories']"

    title_element="//input[@id='series-category-name']" 
    slug_element="//input[@id='series-category-slug']"
    category_element="//select[@id='series-category-parent-id']"
    image_element="//input[@id='series-category-image']"
    banner_element="//input[@id='series-category-banner-image']"
    enable_menu_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    enable_home_element="(//span[@class='admin-slider position-absolute admin-round '])[2]"
    # enable_footer_element="(//span[@class='admin-slider position-absolute admin-round '])[3]"
    submit_element="(//span[text()='Submit'])[2]"


    
    def test_Add_Genre(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.series_element)))
        user = self.driver.find_element(By.XPATH, self.series_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        add_role= self.driver.find_element(By.XPATH, self.manage_genre_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_role)
        time.sleep(2)
        add_role.click()

        WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.add_cate_element))
            ).click()

            
        try :
            name=WebDriverWait(self.driver, 30).until(
               EC.element_to_be_clickable((By.XPATH, self.title_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name) 
            name.clear()
            time.sleep(2)
            name.send_keys("")
            time.sleep(2)
          
           
        except Exception as e:
            print(f" Failed to enter title: {e}")
        
        
        try :
            slug=WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.slug_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slug) 
            slug.clear()
            time.sleep(2)
            slug.send_keys("")
            time.sleep(2)
        except Exception as e:
            print(f" Failed to enter Slug: {e}")
        

                
# Select user role Dropdown
        try :
            drop_down1= WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, self.category_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down1) 
            time.sleep(2)
            select = Select(drop_down1)
            select.select_by_visible_text("Choose an category")
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
            print(f" Failed to Upload Image: {e}")
        

        try :
            image2=WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, self.banner_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image2)
            image2.send_keys(self.image_path_2)
            time.sleep(2)
        except Exception as e:
            print(f" Failed to Upload Image: {e}")
        

        toggle1 = self.driver.find_element(By.XPATH, self.enable_menu_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle1)
        time.sleep(2)

        toggle2 = self.driver.find_element(By.XPATH, self.enable_home_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle2)
        time.sleep(2)

        # toggle3 = self.driver.find_element(By.XPATH, self.enable_footer_element)
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3) 
        # time.sleep(2)  
        # self.driver.execute_script("arguments[0].click();", toggle3)
        # time.sleep(2)

           # update or save element
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.submit_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Series Genre User details Added successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 




