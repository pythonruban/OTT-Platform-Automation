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
class TestCategoryAdd:
   
    allure_report_error_message = "" 
    driver: WebDriver
       #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "1080.1080.jpg")
    image_path_2 = os.path.join(base_dir, "1691.jpg")
   

    # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH
 

    video_element="//span[text()='Videos']"
    category_element="//span[text()='Manage Video Categories']"

    add_element="//span[text()='Add Categories']"

    name_element="//input[@id='video-category-name']"
    slug_element="//input[@id='video-category-slug']"
    home_element="//input[@id='video-category-home-genre']"
    cate_element="//select[@id='video-category-parent-id']"

    hpage_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    menu_element="(//span[@class='admin-slider position-absolute admin-round '])[2]"
    banner_element="(//span[@class='admin-slider position-absolute admin-round '])[3]" 

    image1_element="//input[@id='video-category-image']"
    image2_element="//input[@id='video-category-banner-image']"
    submit_element="//button[@id='video-category-submit-down']"

    
        
    def test_Add_Category(self,browser_setup):
        self.driver = browser_setup
        self.driver.maximize_window()
        self.driver.get(ReadConfig.getAdminPageURL())

        # Login to the application
        self.driver.find_element(By.XPATH, self.email_element).send_keys(ReadConfig.getAdminId())

        self.driver.find_element(By.XPATH, self.password_element).send_keys(ReadConfig.getPassword())
        self.driver.find_element(By.XPATH, self.login_element).click()
        
        try:
            WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.login_element))).click()
            # self.allure_report_error_message = "Category Add Process: Login successful"
            
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login successful", attachment_type=AttachmentType.PNG)
        except Exception as e:
            self.allure_report_error_message = "Category Add Process: Login Error - UI elements did not load "
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login successful and the UI elements have not loaded due to timeout", attachment_type=AttachmentType.PNG)
            raise e
        if self.allure_report_error_message:
            os.environ["Allure_Report_Error_Message"] = self.allure_report_error_message


        # Scroll to ensure all elements are loaded
        user=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.video_element)))
        self.driver.find_element(By.XPATH, self.video_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()
        
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.category_element)))
        cate = self.driver.find_element(By.XPATH, self.category_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cate)
        time.sleep(2)
        cate.click()

        
        add=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.add_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add)
        add.click()
        time.sleep(2)
        
        try :
            length = 6
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")
 
            print(f"Using XPath: {self.name_element}")
 
            # Wait for the title input to be clickable
            name = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.name_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
            time.sleep(2)
            name.clear()
            time.sleep(2)  # small delay to ensure field is cleared
            name.send_keys(auto_name)
            time.sleep(2)
            print(" Auto name entered in the title field.")
 
        except Exception as e:
            print(f" Failed to enter title: {e}")
            
        try :
            length = 6
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")
 
            print(f"Using XPath: {self.slug_element}")
 
            # Wait for the title input to be clickable
            name = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.slug_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
            time.sleep(2)
            name.clear()
            time.sleep(2)  # small delay to ensure field is cleared
            name.send_keys(auto_name)
            time.sleep(2)
            print(" Auto name entered in the title field.")
 
        except Exception as e:
            print(f" Failed to enter title: {e}")
 

       

           # Send keys using wait Statement
        pa=WebDriverWait(self.driver, 50).until(
               EC.presence_of_element_located((By.XPATH, self.home_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pa) 
        pa.send_keys("Cinema")
        time.sleep(2)

        
# Select user role Dropdown
        drop_down = self.driver.find_element(By.XPATH, self.cate_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", drop_down) 
        drop_down.click()
        time.sleep(2)
        select = Select(drop_down)
        select.select_by_visible_text("Action")

                   
# Image
        image=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.image1_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image)
        image.send_keys(self.image_path_1)
        time.sleep(2)

             
# Image
        image2=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.image2_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image2)
        image2.send_keys(self.image_path_2)
        time.sleep(2)


        dash = self.driver.find_element(By.XPATH, self.hpage_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dash) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", dash)
        time.sleep(2)

        dash1 = self.driver.find_element(By.XPATH, self.menu_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dash1) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", dash1)
        time.sleep(2)

        # dash2 = self.driver.find_element(By.XPATH, self.banner_element)
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dash2) 
        # time.sleep(2)  
        # self.driver.execute_script("arguments[0].click();", dash2)
        # time.sleep(2)

  
        
          # update or save element
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.submit_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Video Category details Added successfully.", attachment_type=AttachmentType.PNG)

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 




