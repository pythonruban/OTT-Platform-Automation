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
class TestAddCast:
    
    driver: WebDriver

    # Local Path
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_file_path = os.path.join(base_dir, "1080.1080.jpg")
  
    # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']"

    artist_element = "//span[text()='Artists Management']"
    add_element = "//span[text()='Add New Artists']"

    title_element = "//input[@id='artist-name']"
    slug_element = "//input[@id='artist-slug']"
    mail_element = "//input[@id='artist-email']"
    type_element = "//select[@id='artist-type']"
    image_element = "//input[@id='artist-image']"
    description_element = "//textarea[@id='artist-description']"
    submit_element = "(//span[text()='Add Artist'])[2]"

    def test_add_cast(self, browser_setup):
       
        self.driver = browser_setup
        self.driver.maximize_window()
        self.driver.get(ReadConfig.getAdminPageURL())

        # Login to the application
        self.driver.find_element(By.XPATH, self.email_element).send_keys(ReadConfig.getAdminId())
        self.driver.find_element(By.XPATH, self.password_element).send_keys(ReadConfig.getPassword())
        self.driver.find_element(By.XPATH, self.login_element).click()

        try:
            WebDriverWait(self.driver, 80).until(EC.visibility_of_element_located((By.XPATH, self.dashboard_element))).click()
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login successful", attachment_type=AttachmentType.PNG)
        except Exception:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login failed", attachment_type=AttachmentType.PNG)
            raise

        # Navigate to Artists Management
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.artist_element)))
        user = self.driver.find_element(By.XPATH, self.artist_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        # Go to Add New Artists
        ro = WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.add_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()

        # Fill required fields
        length = 6
        auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
        
        name = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.title_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
        time.sleep(2)
        name.clear()
        name.send_keys(auto_name)
        
        # Fill slug
        slug = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.slug_element)))
        slug.send_keys(auto_name.lower())
        
           # Fill email
        mail = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, self.mail_element)))
        mail.send_keys("test@example.com")

        # Select type
        drop_down = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, self.type_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", drop_down)
        time.sleep(2)
        select = Select(drop_down)
        select.select_by_visible_text("Actor")

        # Try to upload invalid file format
        ime = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, self.image_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ime)
        time.sleep(1)
        ime.send_keys(self.image_file_path)
        
        
        # Fill description
        des = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, self.description_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", des)
        des.send_keys("Test description image")



        # Skip image upload and submit
        save_element = WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH, self.submit_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element)
        time.sleep(2)
        save_element.click()
        time.sleep(5)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Artist Details Added Successfully", attachment_type=AttachmentType.PNG)
      
    
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")
