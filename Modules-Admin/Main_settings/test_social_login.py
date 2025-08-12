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
class Test_Social_login:
   
    driver: WebDriver

      # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    settings_element="//span[text()='Settings']"
    social_element="//span[text()='Social Login Settings']"
    enable_fb_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    fb_client_element="//input[@id='facebook_client_id']"
    fb_key_element="//input[@id='facebook_secrete_key']"
    fbcall_element="//input[@id='facebook_callback']"

    enable_goo_element="(//span[@class='admin-slider position-absolute admin-round '])[2]"
    goo_client_element="//input[@id='google_client_id']"
    goo_key_element="//input[@id='google_secrete_key']"
    goocall_element="//input[@id='google_callback']"

    update_element="(//span[text()='Update Settings'])[2]"



    def test_Social_login(self,browser_setup):
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

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.social_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()

        toggle1 = self.driver.find_element(By.XPATH, self.enable_fb_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1)
        time.sleep(2)
        self.driver.execute_script("arguments[0].click();", toggle1)


        bg=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.fb_client_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",bg) 
        bg.clear()
        time.sleep(1) 
        bg.send_keys("Britto Praba")
        time.sleep(3)

        sk=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.fb_key_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sk) 
        sk.clear()
        time.sleep(1) 
        sk.send_keys("Bp")
        time.sleep(3)

        fbc=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.fbcall_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fbc) 
        fbc.clear()
        time.sleep(1) 
        fbc.send_keys("https://yourapp.com/webhooks/sms/callback")
        time.sleep(3)

        toggle2 = self.driver.find_element(By.XPATH, self.enable_goo_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2)
        time.sleep(2)
        self.driver.execute_script("arguments[0].click();", toggle2)


        gc=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.goo_client_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gc) 
        gc.clear()
        time.sleep(1) 
        gc.send_keys("Britto Praba")
        time.sleep(3)

        gk=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.goo_key_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gk) 
        gk.clear()
        time.sleep(1) 
        gk.send_keys("Britto")
        time.sleep(3)

        gl=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.goocall_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gl) 
        gl.clear()
        time.sleep(1) 
        gl.send_keys("https://www.example.com/api/auth/callback/google")
        time.sleep(3)

        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Social Login Settings in Main Settings details Updated successfully.", attachment_type=AttachmentType.PNG)
    
    def teardown_class(self):
        
        "Close the browser"
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 



 