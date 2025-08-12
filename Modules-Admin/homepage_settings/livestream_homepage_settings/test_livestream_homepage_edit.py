import time
import re 
import random
import string
import pytest 
import os
import sys 
import allure 


 
from conftest import *
from selenium.webdriver import ActionChains, Keys
from allure_commons.types import AttachmentType
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from utilities.readProp import ReadConfig

# Add the project root (D:\Automation\) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


@pytest.mark.usefixtures("browser_setup")  

class TestHomepageLiveStreamsettings:

    driver = webdriver.Firefox
    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_btn_element = "(//button[@type='submit'])[2]"
    homepage_setting_element = "//div[@data-bs-target='#settingsURLhome']"
    livestream_setting_element = "//span[text()='Live Settings']"
    edit_element = "(//span[@class='editdropdown-button'])[1]"
    edit_menu_element = "(//span[text()='Edit'])[1]"

    header_name_element= "//input[@name='header_name']"
    site_url_element= "//input[@name='url']"
    upadate_order_element="//span[text()='Update Order']"

    edit2_element = "(//span[@class='editdropdown-button'])[2]"
    edit2_menu_element = "(//span[text()='Edit'])[2]"

    edit3_element = "(//span[@class='editdropdown-button'])[3]"
    edit3_menu_element = "(//span[text()='Edit'])[3]"
    
    edit4_element = "(//span[@class='editdropdown-button'])[4]"
    edit4_menu_element = "(//span[text()='Edit'])[4]"

    edit5_element = "(//span[@class='editdropdown-button'])[5]"
    edit5_menu_element = "(//span[text()='Edit'])[5]"
    

    
    def test_livestream_homepage_edit(self):
        """Login to the admin panel"""
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()
        actions = ActionChains(self.driver)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.email_element))
            ).send_keys(ReadConfig.getAdminId())

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.password_element))
            ).send_keys(ReadConfig.getPassword())

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.login_btn_element))
            ).click()

            print(" Login Successful!")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All Value login Credentials was entered, and the login button was clicked. it was redirect to Dashboard", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="login_error", attachment_type=AttachmentType.PNG)
            print(f" Failed to enter email: {e}")
        time.sleep(2)
    
   
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
            Manage_app = WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, self.homepage_setting_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Manage_app)
            time.sleep(1)  # Allow smooth scrolling
            self.driver.execute_script("arguments[0].click();", Manage_app)
            print(" Clicked 'Language'")
            time.sleep(6)
            self.driver.find_element(By.XPATH, self.livestream_setting_element).click()
            time.sleep(5)
        except Exception as e:
            print(f" Error while navigating to 'Live Settings': {e}")
        #edit menu
        try:
            app = WebDriverWait(self.driver, 45).until(
                    EC.presence_of_element_located((By.XPATH, self.edit_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", app)
            time.sleep(2)
            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.edit_element)  # Replace with actual locator
            actions.move_to_element(element_to_hover).perform()

                #Edit menu
            WebDriverWait(self.driver, 130).until(
                    EC.presence_of_element_located((By.XPATH, self.edit_menu_element))
                ).click()
            time.sleep(2)
        except Exception as e:
            print(f" Error while clicking on edit menu: {e}")
          
        try:
            name= WebDriverWait(self.driver, 130).until(
                    EC.presence_of_element_located((By.XPATH, self.header_name_element))
                )
            name.clear()
            time.sleep(2)
            name.send_keys("Livestream Videos")
            time.sleep(2)

            url= WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.site_url_element))
                )
            url.clear()
            time.sleep(2)
            url.send_keys("https://flicknexs.com/")
            time.sleep(2)
            

            self.driver.find_element(By.XPATH , self.upadate_order_element).click()
            print(" The  livestream  was Updated Successfully")
            time.sleep(2)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Livestream homepage edit", attachment_type=AttachmentType.PNG)
            time.sleep(2)
            # Go back to the previous page
            self.driver.back()
            time.sleep(5)
        except Exception as e:
            print(f" Error while updating livestream: {e}")

        #2nd oned
        try:
            app1 = WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, self.edit2_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", app1)
            time.sleep(2)
            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.edit2_element)  # Replace with actual locator
            actions.move_to_element(element_to_hover).perform()
            WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.edit2_menu_element))
                ).click()
            time.sleep(2)
        except Exception as e:
            print(f" Error while clicking on second edit menu: {e}")

        try:
            name= WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.header_name_element))
                )
            name.clear()
            time.sleep(2)
            name.send_keys("Live Categories")
            time.sleep(2)

            url= WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.site_url_element))
                )
            url.clear()
            time.sleep(2)
            url.send_keys("https://flicknexs.com/")
            time.sleep(2)

            self.driver.find_element(By.XPATH , self.upadate_order_element).click()
            print(" The Livestream  was Updated Successfully")
            time.sleep(2)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Second Livestream homepage edit", attachment_type=AttachmentType.PNG)
            time.sleep(2)
            self.driver.back()
            time.sleep(5)
        except Exception as e:
            print(f" Error while updating second livestream: {e}")
        #3nd one
        try:
            app2 = WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, self.edit3_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", app2)
            time.sleep(2)
            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.edit3_element)  # Replace with actual locator
            actions.move_to_element(element_to_hover).perform()
            WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.edit3_menu_element))
                ).click()
            time.sleep(2)
        except Exception as e:
            print(f" Error while clicking on third edit menu: {e}")
            # Edit menu
        try:
            name= WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.header_name_element))
                )
            name.clear()
            time.sleep(2)
            name.send_keys("LiveStream based on Categories")
            time.sleep(2)

            url= WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.site_url_element))
                )
            url.clear()
            time.sleep(2)
            url.send_keys("https://flicknexs.com/")
            time.sleep(2)

            self.driver.find_element(By.XPATH , self.upadate_order_element).click()
            print(" The Livestream was Updated Successfully")
            time.sleep(2)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Third Livestream homepage edit", attachment_type=AttachmentType.PNG)
            time.sleep(2)
            self.driver.back()
            time.sleep(5)
        except Exception as e:
            print(f" Error while updating third livestream: {e}")
            #4 one
        try:
            app3 = WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, self.edit4_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", app3)
            time.sleep(2)
            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.edit4_element)  # Replace with actual locator
            actions.move_to_element(element_to_hover).perform()
            WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.edit4_menu_element))
                ).click()
            time.sleep(2)

        except Exception as e:
            print(f" Error while clicking on fourth edit menu: {e}")    

        try:
            name= WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.header_name_element))
                )
            name.clear()
            time.sleep(2)
            name.send_keys("Scheduled Publish LiveStream")
            time.sleep(2)

            url= WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.site_url_element))
                )
            url.clear()
            time.sleep(2)
            url.send_keys("https://flicknexs.com/")
            time.sleep(2)

            self.driver.find_element(By.XPATH , self.upadate_order_element).click()
            print(" The Livestream  was Updated Successfully")
            time.sleep(2)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Fourth Livestream homepage edit", attachment_type=AttachmentType.PNG)
            time.sleep(2)
            self.driver.back()
            time.sleep(4)
        except Exception as e:
            print(f" Error while updating fourth livestream: {e}")

        #           
            #5 one
        try:
            app4 = WebDriverWait(self.driver, 145).until(
                    EC.presence_of_element_located((By.XPATH, self.edit5_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", app4)
            time.sleep(2)
            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.edit5_element)  # Replace with actual locator
            actions.move_to_element(element_to_hover).perform()
            WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.edit5_menu_element))
                ).click()
            time.sleep(2)
        except Exception as e:
            print(f" Error while clicking on fifth edit menu: {e}")


        try:
            name= WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.header_name_element))
                )
            name.clear()
            time.sleep(2)
            name.send_keys("Latest Viewed Livestream")
            time.sleep(2)

            url= WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.site_url_element))
                )
            url.clear()
            time.sleep(2)
            url.send_keys("https://flicknexs.com/")
            time.sleep(2)
            
            self.driver.find_element(By.XPATH , self.upadate_order_element).click()
            print(" The Livestream  was Updated Successfully")
            time.sleep(2)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Fifth Livestream homepage edit", attachment_type=AttachmentType.PNG)
            time.sleep(2)
            self.driver.back()
            time.sleep(4)
            assert True
        except Exception as e:
            print(f" Error while updating fifth livestream: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Fifth Livestream homepage edit", attachment_type=AttachmentType.PNG)
            assert False, f"Test failed due to error: {e}"
    
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 
      
