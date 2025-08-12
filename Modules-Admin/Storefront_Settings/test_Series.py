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
class TestSeriessettings:
    
    driver: WebDriver

    # File paths
    base_dir = os.path.join(os.getcwd(), "tmp")
    names = os.path.abspath(os.path.join(base_dir, "sample1.mp4"))

    # XPATH locators
    email_element = "//div[3]//input[1]"
    password_element = "//input[contains(@placeholder,'Enter Password')]"
    login_btn_element = "//span[normalize-space()='login']"
    storefront_Settings_element = "//span[@class='ms-2 text-break'][normalize-space()='Storefront Settings']"
    Series_settings_element = "//h5[normalize-space()='Series Settings']"
    # toggle button
    Enable_PPV_Season_ele = "//span[@name='series_season']" 
    TV_Shows_Networks_ele = "//span[@name='series_networks_status']"

    update_button_ele = "//button[@class='btn btn-primary']"
    

    def setup_class(self,browser_setup):
        self.driver = browser_setup
        self.driver.get(ReadConfig.getAdminPageURL())  
        self.driver.maximize_window()

    def test_Seriessettings(self):
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
        Series_settings = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, self.Series_settings_element))
        )
        Series_settings.click()

        # Click on the toggle button to switch it ON
        toggle_button = self.driver.find_element(By.XPATH , self.Enable_PPV_Season_ele)
        toggle_button.click()
        time.sleep(1)
        # Click on the toggle button to switch it OFF
        toggle_button = self.driver.find_element(By.XPATH , self.Enable_PPV_Season_ele)
        toggle_button.click()
        time.sleep(1)
        # Click on the toggle button to switch it ON
        toggle_button = self.driver.find_element(By.XPATH , self.TV_Shows_Networks_ele)
        toggle_button.click()
        time.sleep(1)
        # Click on the toggle button to switch it OFF
        toggle_button = self.driver.find_element(By.XPATH , self.TV_Shows_Networks_ele)
        toggle_button.click()
        time.sleep(1)

        self.driver.find_element(By.XPATH, self.update_button_ele).click()
        time.sleep(1)

        # capture screenshot
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "Series updated successfully", attachment_type= AttachmentType.PNG)

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 


            
    