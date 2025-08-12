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
class TestUpdateSocial:
   
    driver: WebDriver
   # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    storefront_element="(//span[text()='Storefront Settings'])[2]"
    social_element="//h5[text()='Social Network Settings']"

    faceid_element="//input[@name='facebook_page_id']"
    googleid_element="//input[@name='google_page_id']"
    xuser_element="//input[@name='twitter_page_id']"
    insta_element="//input[@name='instagram_page_id']"
    tiktok_element="//input[@name='tiktok_page_id']"

    linkedin_element="//input[@name='linkedin_page_id']"
    whatsapp_element="//input[@name='whatsapp_page_id']"
    teams_element="//input[@name='skype_page_id']" 
    youtube_element="//input[@name='youtube_page_id']"
    mail_element="//input[@name='email_page_id']"

    update_element="(//button[text()='Update'])[2]"



       
      
    def test_Update_Social(self,browser_setup):
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

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.social_element)))
        front = self.driver.find_element(By.XPATH, self.social_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", front)
        time.sleep(2)
        front.click()

        fid=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.faceid_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fid) 
        time.sleep(2)
        fid.send_keys("Tharun")
        time.sleep(2)

        
        gooid=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.googleid_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gooid) 
        time.sleep(2)
        gooid.send_keys("tharun001")
        time.sleep(2)

        
        xid=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.xuser_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", xid) 
        time.sleep(2)
        xid.send_keys("Tharun")
        time.sleep(2)

        
        instid=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.insta_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", instid) 
        time.sleep(2)
        instid.send_keys("runraj12")
        time.sleep(2)

        
        tikid=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.tiktok_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tikid) 
        time.sleep(2)
        tikid.send_keys("raj12")
        time.sleep(2)

        
        linkid=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.linkedin_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", linkid) 
        time.sleep(2)
        linkid.send_keys("Tharunraj")
        time.sleep(2)

        whatsid=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.whatsapp_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", whatsid) 
        time.sleep(2)
        whatsid.send_keys("raj")
        time.sleep(2)

        teamsid=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.teams_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", teamsid) 
        time.sleep(2)
        teamsid.send_keys("Tharunraj")
        time.sleep(2)

        youid=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.youtube_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", youid) 
        youid.clear()
        time.sleep(2)
        youid.send_keys("Rajaraj")
        time.sleep(2)

        mailid=WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.mail_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mailid) 
        time.sleep(2)
        mailid.send_keys("tharunraj20@gmail.com")
        time.sleep(2)

          # update or save element
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Social User details Updated successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 




        
