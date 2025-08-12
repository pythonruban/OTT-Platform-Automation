import time
import allure
import pytest
from conftest import *
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from utilities.readProp import ReadConfig
import os

@pytest.mark.usefixtures("browser_setup")
class TestRegistrationsettings:
    
    driver: WebDriver

    # File paths
    base_dir = os.path.join(os.getcwd(), "tmp")
    names = os.path.abspath(os.path.join(base_dir, "sample1.mp4"))

    # XPATH locators
    email_element = "//div[3]//input[1]"
    password_element = "//input[contains(@placeholder,'Enter Password')]"
    login_btn_element = "//span[normalize-space()='login']"
    storefront_Settings_element = "//span[@class='ms-2 text-break'][normalize-space()='Storefront Settings']"
    Registration_settings_element = "//h5[normalize-space()='Registration Settings']"
    # toggle button
    Enable_Free_Registration_ele = "//span[@name='free_registration']"
    Require_users_ele = "//span[@name='activation_email']"
    Enable_registered_ele = "//span[@name='premium_upgrade']"
    Access_Free_Content_ele = "//span[@name='access_free']"
    Enable_LandingPage_ele = "//span[@name='enable_landing_page']"
    Update_settings_ele ="//button[@class='btn btn-primary']"

    def setup_class(self):
        self.driver.get(ReadConfig.getAdminPageURL())  
        self.driver.maximize_window()

    def test_Registrationsettings(self):
        action = ActionChains(self.driver)

        WebDriverWait(self.driver, 20).until(lambda driver: driver.current_url == ReadConfig.getAdminPageURL())

        # Login
        self.driver.find_element(By.XPATH, self.email_element).send_keys(ReadConfig.getAdminId())
        self.driver.find_element(By.XPATH, self.password_element).send_keys(ReadConfig.getPassword())
        self.driver.find_element(By.XPATH, self.login_btn_element).click()

        # Wait for the element to be present (not necessarily visible)
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.storefront_Settings_element))
            )
        except:
            print("❌ Storefront Settings element NOT FOUND in the DOM!")
            print(self.driver.page_source)  # Debugging: Print HTML source to check if the element exists
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Element_Not_Found", attachment_type=AttachmentType.PNG)
            raise  # Rethrow exception after logging

        # Scroll into view
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(2)  # Give time for UI adjustment
        except:
            print("⚠️ ScrollIntoView() failed, trying alternative scroll...")
            self.driver.execute_script("window.scrollBy(0, 500);")

        # Ensure the element is visible and clickable
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.storefront_Settings_element))
        )

        # Click using ActionChains for better interaction handling
        action.move_to_element(element).click().perform()

        # Wait and click on RTMP settings
        registration_settings = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, self.Registration_settings_element))
        )
        registration_settings.click()
        

        # Enable Free Registration
        # Click on the toggle button to switch it ON
        toggle_button = self.driver.find_element(By.XPATH,self.Enable_Free_Registration_ele)
        toggle_button.click()
        time.sleep(2)
        # # Click on the toggle button to switch it OFF
        toggle_button = self.driver.find_element(By.XPATH,self.Enable_Free_Registration_ele)
        toggle_button.click()
        time.sleep(2)

        # Require users to activate their account
        # Click on the toggle button to switch it ON
        toggle_button = self.driver.find_element(By.XPATH,self.Require_users_ele)
        toggle_button.click()
        time.sleep(2)
        # Click on the toggle button to switch it OFF
        toggle_button = self.driver.find_element(By.XPATH,self.Require_users_ele)
        toggle_button.click()
        time.sleep(2)

        # Enable registered users to upgrade to premium
        # Click on the toggle button to switch it ON
        toggle_button = self.driver.find_element(By.XPATH,self.Enable_registered_ele)
        toggle_button.click()
        time.sleep(2)
        # Click on the toggle button to switch it OFF
        toggle_button = self.driver.find_element(By.XPATH,self.Enable_registered_ele)
        toggle_button.click()
        time.sleep(2)

        # Access Free Content
        # Click on the toggle button to switch it ON
        toggle_button = self.driver.find_element(By.XPATH,self.Access_Free_Content_ele)
        toggle_button.click()
        time.sleep(2)
        # Click on the toggle button to switch it OFF
        toggle_button = self.driver.find_element(By.XPATH,self.Access_Free_Content_ele)
        toggle_button.click()
        time.sleep(2)

        # Enable Landing Page
        # Click on the toggle button to switch it ON
        toggle_button = self.driver.find_element(By.XPATH,self.Enable_LandingPage_ele)
        toggle_button.click()
        time.sleep(2)
        # Click on the toggle button to switch it OFF
        toggle_button = self.driver.find_element(By.XPATH,self.Enable_LandingPage_ele)
        toggle_button.click()
        time.sleep(2)

        # Click on the Update settings button
        self.driver.find_element(By.XPATH, self.Update_settings_ele).click()
        time.sleep(2)

        # Capture success screenshot
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Registration Settings Updated Successfully", attachment_type=AttachmentType.PNG)

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 




        
