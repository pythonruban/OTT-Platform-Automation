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
class TestAddLogin:
   
    driver: WebDriver
        #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "916.jpg")
    image_path_2 = os.path.join(base_dir, "thumbnail1.jpeg")
    image_path_3 = os.path.join(base_dir, "916.jpg")
   
   # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    storefront_element="(//span[text()='Storefront Settings'])[2]"
    log_element="//h5[text()='Login Page Settings']"

    log_text_element="(//input[@id='inputField'])[1]"
    pusher_element="(//input[@id='inputField'])[2]"
    signature_element="//div[@class='jodit-wysiwyg']"

    login_image_element="(//input[@id='[object Object]'])[1]"
    notifi_image_element="(//input[@id='[object Object]'])[2]"
    email_image_element="(//input[@id='[object Object]'])[3]"

    submit_element="(//span[text()='Update'])[2]"

   
    def test_Add_Login(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.storefront_element)))
        user = self.driver.find_element(By.XPATH, self.storefront_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.log_element)))
        front = self.driver.find_element(By.XPATH, self.log_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", front)
        time.sleep(2)
        front.click()

        dis=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.log_text_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dis) 
        dis.clear()
        time.sleep(2)
        dis.send_keys("Wait And Watch")
        time.sleep(2)

        push=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.pusher_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", push)
        push.clear()
        time.sleep(2)
        push.send_keys("i am back")
        time.sleep(2)

        sig=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.signature_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sig)
        sig.clear()
        time.sleep(2)
        sig.send_keys("tharu18@gmail.com")
        time.sleep(2)

        image1=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.login_image_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image1)
        time.sleep(2)
        image1.send_keys(self.image_path_1)
        time.sleep(2)

        
        image2=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.notifi_image_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image2)
        time.sleep(2)
        image2.send_keys(self.image_path_2)
        time.sleep(2)

        
        image3=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.email_image_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image3)
        time.sleep(2)
        image3.send_keys(self.image_path_3)
        time.sleep(2)

             # update or save element
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.submit_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login Page details Saved successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 


