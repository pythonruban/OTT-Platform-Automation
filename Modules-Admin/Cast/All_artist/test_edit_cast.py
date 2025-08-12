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
class TestEdit_cast:
   
    driver: WebDriver

    
       #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "1080_10802.jpg")
 

    # Define the XPaths
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    
    artist_element="//span[text()='Artists Management']"
    all_artist_element="(//span[text()='All Artists'])[1]"

    dot_element="(//span[@class='editdropdown-button'])[1]"
    edit_element="(//span[text()='Edit'])[1]"

    edit_name_element="//input[@name='artist_name']"
    edit_slug_element="//input[@name='artist_slug']"
    edit_email_element="//input[@name='artist_email']"
    edit_type_element="//select[@name='artist_type']"
    edit_image_element="//input[@name='image']"
    edit_decrip_element="//textarea[@id='artist-description']"
    update_element="(//span[text()='Update Artist'])[2]"


    
    
    def test_Edit_Cast(self,browser_setup):
        self.driver = browser_setup
        self.driver.maximize_window()
        self.driver.get(ReadConfig.getAdminPageURL())

        # Login to the application
        self.driver.find_element(By.XPATH, self.email_element).send_keys("admin@admin.com")
        self.driver.find_element(By.XPATH, self.password_element).send_keys("Webnexs123!@#")
        self.driver.find_element(By.XPATH, self.login_element).click()

        try:
            WebDriverWait(self.driver, 80).until(EC.visibility_of_element_located((By.XPATH, self.dashboard_element))).click()
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login was successful and the UI elements have been loaded.", attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login successful and the UI elements have not loaded due to timeout", attachment_type=AttachmentType.PNG)
            raise e


        # Scroll to ensure all elements are loaded
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.artist_element)))
        user = self.driver.find_element(By.XPATH, self.artist_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        element = self.driver.find_element(By.XPATH, self.all_artist_element)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
        time.sleep(2)
        element .click()

        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.dot_element))
            )
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.edit_element))
            )
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")


         # Fill required fields
        length = 6
        auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
        
        name = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.edit_name_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
        time.sleep(2)
        name.clear()
        name.send_keys(auto_name)
        
        # Fill slug
        slug = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.edit_slug_element)))
        slug.clear()
        time.sleep(2)
        slug.send_keys(auto_name.lower())
        
        mail = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.edit_email_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mail)
        mail.clear()
        time.sleep(2)
        mail.send_keys("kanna78@gmail.com")
        print("✅ Email has been updated successfully")
        time.sleep(3)

          # Select user role
        drop_down = self.driver.find_element(By.XPATH, self.edit_type_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", drop_down)
        select = Select(drop_down)
        select.select_by_visible_text("Director")
        print("✅ Artist type has been selected successfully")

         # Image
        image=WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.edit_image_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image)
        image.send_keys(self.image_path_1)
        print("✅ Image has been uploaded successfully")
        time.sleep(2)

        des=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.edit_decrip_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", des) 
        self.driver.execute_script("arguments[0].value = '';", des)
        time.sleep(3)
        des.send_keys("Vijay is a prominent Indian actor, primarily known for his work in Tamil cinema")
        time.sleep(3)
        
         # update or save element
        save_element=WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH, self.update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element)
        save_element.click()
        time.sleep(2)
        print("✅ Cast & Crew Details updated successfully!")
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Cast & Crew User details Updated successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 
    



    
