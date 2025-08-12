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
class TestEditSubscriber:
   
    driver: WebDriver

       #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "1691.jpg")

    
    # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    series_element="(//span[text()='Series & Episodes'])[2]"
    all_new_element="(//span[text()='All Series'])[1]"

    dot_element="(//span[@class='editdropdown-button'])[1]"
    edit_element="(//span[text()='Edit'])[1]" 
    
    manage_element="//span[text()='Manage Season & Episodes']"
    dot2_element="(//span[@class='editdropdown-button'])[1]"
    edit2_element="(//span[text()=' Edit'])[1]"
    
    
    season_element="//span[text()='Create Season']"
    
    title_element="//input[@id='edit-series-tile-modal']"
    image_element="//input[@id='edit-series-fileInputRef4']"
    user_element="//select[@id='season-access']"
    customize_element="//span[text()='Customize PPV']"
    #customize_element="//button[@id='series-custom-ppv-button']"
    ppv_price_element="(//input[@id='countryPPVPrice'])[2]"
    ios_price_element="(//select[@id='countryPPVIOSPrice'])[2]"
    convert_element="(//span[text()='Convert'])[2]"
    done_element="(//span[text()='Done'])[2]"
    submit_element="(//span[text()='Edit Season'])[2]"
    

    
        
    def test_edit_Subscriber(self,browser_setup):
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

        add_role= self.driver.find_element(By.XPATH, self.all_new_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_role)
        time.sleep(2)
        add_role.click()
        
        
              # Wait until the menu element is present
        menu = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.dot_element))
        )
 
        # Scroll into view in case it's out of screen
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
        time.sleep(1)
 
        # Hover over the menu to make the submenu visible
        actions = ActionChains(self.driver)
        actions.move_to_element(menu).perform()  # pause to ensure hover effect takes place
 
        # Wait for submenu to appear and be clickable
        submenu = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, self.edit_element))
        )
        # Click the submenu
        submenu.click()
       
        manage=WebDriverWait(self.driver,120).until(EC.presence_of_element_located((By.XPATH, self.manage_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", manage)
        time.sleep(2)


              # Wait until the menu element is present
        menu = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.dot2_element))
        )
 
        # Scroll into view in case it's out of screen
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
        time.sleep(1)
 
        # Hover over the menu to make the submenu visible
        actions = ActionChains(self.driver)
        actions.move_to_element(menu).perform()  # pause to ensure hover effect takes place
 
        # Wait for submenu to appear and be clickable
        submenu = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, self.edit2_element))
        )
 
        # Click the submenu
        submenu.click()
       

            
        try :
            length= 6 
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")
 
            print(f"Using XPath: {self.title_element}")
 
            # Wait for the title input to be clickable
            name = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.title_element))
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

              # Image  
        try :
            image1 =WebDriverWait(self.driver, 80).until(
                    EC.presence_of_element_located((By.XPATH, self.image_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image1)
            time.sleep(2)
            image1.send_keys(self.image_path_1)
            time.sleep(2)
        except Exception as e:
            print(f" Failed to Upload Image: {e}")

                    
# Select user role Dropdown
        try :
            down1 = self.driver.find_element(By.XPATH, self.user_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",down1) 
            time.sleep(2)
            select = Select(down1)
            select.select_by_visible_text("PPV Users (Pay per movie)")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to Select Access User: {e}")



        cust=WebDriverWait(self.driver, 80).until(
        EC.element_to_be_clickable((By.XPATH, self.customize_element)))
        cust.click()
        
        ppv=WebDriverWait(self.driver, 80).until(
        EC.presence_of_element_located((By.XPATH, self.ppv_price_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ppv)
        time.sleep(2)
        ppv.send_keys("15")
        
        down2 = self.driver.find_element(By.XPATH, self.ios_price_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",down2) 
        time.sleep(2)
        select = Select(down2)
        select.select_by_visible_text('1000')
    
        
        con=WebDriverWait(self.driver, 80).until(
        EC.presence_of_element_located((By.XPATH, self.convert_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",con) 
        time.sleep(2)
        con.click()
        
        do=WebDriverWait(self.driver, 80).until(
        EC.presence_of_element_located((By.XPATH, self.done_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", do)
        do.click()
        
              # update or save element
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.submit_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Season Subscriber details Updated successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 

        
    