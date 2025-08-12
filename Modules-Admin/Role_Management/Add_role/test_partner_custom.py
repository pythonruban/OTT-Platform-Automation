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
class TestPartner_custom:
   
    driver: WebDriver


     # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    roles_element="//span[text()='Roles']"
    add_role_element="(//span[text()='Add Role'])[1]"

    name_element="//input[@id='inputField']"
    role_type_element="(//select[@id='selectField'])[1]"
    access_type_element="(//select[@id='selectField'])[2]"

    # Video Management
    vmcheckbox1_element="(//input[@name='read'])[1]"
    vmcheckbox2_element="(//input[@name='add'])[1]"
    vmcheckbox3_element="(//input[@name='update'])[1]"
    vmcheckbox4_element="(//input[@name='delete'])[1]"

    # Series And Episode Management
    seriescheckbox1_element="(//input[@name='read'])[2]"
    seriescheckbox2_element="(//input[@name='add'])[2]"
    seriescheckbox3_element="(//input[@name='update'])[2]"
    seriescheckbox4_element="(//input[@name='delete'])[2]"

    # Live Stream Management
    livecheckbox1_element="(//input[@name='read'])[3]"
    livecheckbox2_element="(//input[@name='add'])[3]"
    livecheckbox3_element="(//input[@name='update'])[3]"
    livecheckbox4_element="(//input[@name='delete'])[3]"      

    # Audio Management
    audiocheckbox1_element="(//input[@name='read'])[4]"
    audiocheckbox2_element="(//input[@name='add'])[4]"
    audiocheckbox3_element="(//input[@name='update'])[4]"
    audiocheckbox4_element="(//input[@name='delete'])[4]"  

    # Artist Management 

    artistcheckbox1_element="(//input[@name='read'])[5]"
    artistcheckbox2_element="(//input[@name='add'])[5]"
    artistcheckbox3_element="(//input[@name='update'])[5]"
    artistcheckbox4_element="(//input[@name='delete'])[5]"

    # Video Category Management
    categorycheckbox1_element="(//input[@name='read'])[7]"
    categorycheckbox2_element="(//input[@name='add'])[7]"
    categorycheckbox3_element="(//input[@name='update'])[7]"
    categorycheckbox4_element="(//input[@name='delete'])[7]" 

    # Playlist Managemet

    playcheckbox1_element="(//input[@name='read'])[8]"
    playcheckbox2_element="(//input[@name='add'])[8]"
    playcheckbox3_element="(//input[@name='update'])[8]"
    playcheckbox4_element="(//input[@name='delete'])[8]" 

    # Live Stream Category Management 

    streamcheckbox1_element="(//input[@name='read'])[9]"
    streamcheckbox2_element="(//input[@name='add'])[9]"
    streamcheckbox3_element="(//input[@name='update'])[9]"
    streamcheckbox4_element="(//input[@name='delete'])[9]" 

    # Audio Category Management 
    aucatecheckbox1_element="(//input[@name='read'])[10]"
    aucatecheckbox2_element="(//input[@name='add'])[10]"
    aucatecheckbox3_element="(//input[@name='update'])[10]"
    aucatecheckbox4_element="(//input[@name='delete'])[10]" 

    # Audio Album Management

    albumcheckbox1_element="(//input[@name='read'])[11]"
    albumcheckbox2_element="(//input[@name='add'])[11]"
    albumcheckbox3_element="(//input[@name='update'])[11]"
    albumcheckbox4_element="(//input[@name='delete'])[11]" 

    submit_element="(//span[text()='Add Role'])[2]"

    
    def test_Partner_Custom(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.roles_element)))
        user = self.driver.find_element(By.XPATH, self.roles_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.add_role_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()

        try :
            length= 6 
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
        
        

        drop_down1= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.role_type_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down1) 
        time.sleep(2)
        select = Select(drop_down1)
        select.select_by_visible_text("Partner Permission")

        drop_down2= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.access_type_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down2) 
        # time.sleep(2)
        # drop_down1.click()
        time.sleep(2)
        select = Select(drop_down2)
        select.select_by_visible_text("Custom")


        # Video Management 
        WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.vmcheckbox1_element))).click()
        self.driver.find_element(By.XPATH, self.vmcheckbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.vmcheckbox3_element).click()
        self.driver.find_element(By.XPATH, self.vmcheckbox4_element).click()

         # Series And Episode Management

        WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.seriescheckbox1_element))).click()
        self.driver.find_element(By.XPATH, self.seriescheckbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.seriescheckbox3_element).click()
        self.driver.find_element(By.XPATH, self.seriescheckbox4_element).click()

           # Live Stream Management

        WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.livecheckbox1_element))).click()
        self.driver.find_element(By.XPATH, self.livecheckbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.livecheckbox3_element).click()
        self.driver.find_element(By.XPATH, self.livecheckbox4_element).click()


        # Audio Management 

        man=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.audiocheckbox1_element)))
        man.click()
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", man)
        self.driver.find_element(By.XPATH, self.audiocheckbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.audiocheckbox3_element).click()
        self.driver.find_element(By.XPATH, self.audiocheckbox4_element).click()

        # Artist Management

        artist=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.artistcheckbox1_element)))
        artist.click()
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", artist)
        self.driver.find_element(By.XPATH, self.artistcheckbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.artistcheckbox3_element).click()
        self.driver.find_element(By.XPATH, self.artistcheckbox4_element).click()

        # Video Category Management

        cate=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.categorycheckbox1_element)))
        cate.click()
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cate)
        self.driver.find_element(By.XPATH, self.categorycheckbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.categorycheckbox3_element).click()
        self.driver.find_element(By.XPATH, self.categorycheckbox4_element).click()

        # Playlist Management 

        pay=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.playcheckbox1_element)))
        pay.click()
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pay)
        self.driver.find_element(By.XPATH, self.playcheckbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.playcheckbox3_element).click()
        self.driver.find_element(By.XPATH, self.playcheckbox4_element).click()


          # Live Stream Category Management

        strem=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.streamcheckbox1_element)))
        strem.click()
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", strem)
        self.driver.find_element(By.XPATH, self.streamcheckbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.streamcheckbox3_element).click()
        self.driver.find_element(By.XPATH, self.streamcheckbox4_element).click()

        # Audio Category Management 

        adio=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.aucatecheckbox1_element)))
        adio.click()
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", adio)
        self.driver.find_element(By.XPATH, self.aucatecheckbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.aucatecheckbox3_element).click()
        self.driver.find_element(By.XPATH, self.aucatecheckbox4_element).click()

        # Audio Album Management

        mag=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.albumcheckbox1_element)))
        mag.click()
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mag)
        self.driver.find_element(By.XPATH, self.albumcheckbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.albumcheckbox3_element).click()
        self.driver.find_element(By.XPATH, self.albumcheckbox4_element).click()

          
          # update or save element
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.submit_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Partner permission Custom  details Added successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 









    