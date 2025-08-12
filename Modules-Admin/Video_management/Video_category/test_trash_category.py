import time
import allure
import pytest
 
from conftest import *
from allure_commons.types import AttachmentType
from webdriver_manager.firefox import GeckoDriverManager
 
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
 
 
from utilities.readProp import ReadConfig
 
 
@pytest.mark.usefixtures("browser_setup")
class TestCategoryDelete:
   
    driver: WebDriver
    # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH
 
    video_element="//span[text()='Videos']"
    manage_element="//span[text()='Manage Video Categories']"
 
    dot_element="(//span[@class='editdropdown-button'])[6]"
    delete_element="(//span[text()='Delete'])[6]"
    pop_element="(//span[text()='Delete'])[1]"
 
 
           
    def test_Delete_Category(self,browser_setup):
        self.driver = browser_setup
        self.driver.maximize_window()
        self.driver.get(ReadConfig.getAdminPageURL())
 
   
        # Login to the application
        self.driver.find_element(By.XPATH, self.email_element).send_keys(ReadConfig.getAdminId())
        self.driver.find_element(By.XPATH, self.password_element).send_keys(ReadConfig.getPassword())
        self.driver.find_element(By.XPATH, self.login_element).click()
 
       
        try:
            WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.dashboard_element))).click()
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login was successful and the UI elements have been loaded.", attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login successful and the UI elements have not loaded due to timeout", attachment_type=AttachmentType.PNG)
            raise e
 
       
 
        # Scroll to ensure all elements are loaded
        user=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.video_element)))
        self.driver.find_element(By.XPATH, self.video_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", user)
       
        role=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.manage_element)))
        self.driver.find_element(By.XPATH, self.video_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", role)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", role)
        
        menu = WebDriverWait(self.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, self.dot_element))
        )

        # Scroll into view
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
        time.sleep(1)

        # Hover over menu to reveal submenu
        actions = ActionChains(self.driver)
        actions.move_to_element(menu).perform()

        # Wait and click submenu
        submenu = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, self.delete_element))
        )
        submenu.click()
        
       
        WebDriverWait(self.driver, 30).until(
               EC.element_to_be_clickable((By.XPATH, self.pop_element))
            )
        time.sleep(2)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Video Category details Deleted Successfully.", attachment_type=AttachmentType.PNG)

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
   