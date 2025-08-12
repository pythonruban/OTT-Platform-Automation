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
class TestAdd_Pop:
   
    driver: WebDriver

    
       #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "dummy.pdf")


     # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    home_element="//span[text()='Home Settings']"
    pop_element="//span[text()='Home Page Pop Up Settings']"

    header_element="//input[@id='popup_header']"
    footer_element="//input[@id='popup_footer']"
    before_login_element="//input[@id='before_login_link']"
    after_login_element="//input[@id='after_login_link']"
    content_element="//div[@class='jodit-wysiwyg']"
    image_element="//input[@type='file']"
    enable_pop_element="//span[@class='admin-slider position-absolute admin-round']"
    

    update_element="//span[text()='Update Settings']"

    def test_Add_Pop(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.home_element)))
        user = self.driver.find_element(By.XPATH, self.home_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.pop_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()
        
        try :
            head=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.header_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",head)  
            time.sleep(1)
            head.clear()
            head.send_keys("")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to Enter Header: {e}")

        try : 
            foot=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.footer_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",foot) 
            time.sleep(1) 
            foot.clear()
            foot.send_keys("")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to Enter Footer: {e}")

        try :
            before=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.before_login_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",before)  
            time.sleep(1)
            before.clear()
            before.send_keys("")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to Enter Before Login Link: {e}")

        try :
            after=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.after_login_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",after)
            time.sleep(1)
            after.clear()
            after.send_keys("")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to Enter After Login Link: {e}")

        try :
            cont=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.content_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",cont)  
            time.sleep(1)
            cont.clear()
            cont.send_keys("")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to Enter Content Page: {e}")


            # Upload Image
        try :
            image1 =WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, self.image_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image1)
            time.sleep(1)
            image1.send_keys(self.image_path_1)
            time.sleep(2)
        except Exception as e:
            print(f" Failed to Upload Image: {e}")


        
        toggle1 = self.driver.find_element(By.XPATH, self.enable_pop_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle1)
        time.sleep(2)


        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Home Pop-Up setting details Added.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 
        





