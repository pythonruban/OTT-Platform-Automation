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
from selenium.webdriver.common.keys import Keys
import os

@pytest.mark.usefixtures("browser_setup")
class TestSystemsettings:
    
    driver: WebDriver

    # File paths
    base_dir = os.path.join(os.getcwd(), "tmp")
    names = os.path.abspath(os.path.join(base_dir, "sample1.mp4"))

    # XPATH locators
    email_element = "//div[3]//input[1]"
    password_element = "//input[contains(@placeholder,'Enter Password')]"
    login_btn_element = "//span[normalize-space()='login']"
    storefront_Settings_element = "//span[@class='ms-2 text-break'][normalize-space()='Storefront Settings']"
    System_settings_element = "//h5[normalize-space()='System Settings']"

    # send keys
    System_Email_ele = "//input[@name='system_email']"
    GoogleAnalytics_TrackingID_ele = "//input[@name='google_tracking_id']"
    GoogleOauth_ClientID_Key_ele = "//input[@name='google_oauth_key']"
    SystemPhone_Number_ele = "//input[@name='system_phone_number']"
    System_Address_ele = "//div[@class='jodit-wysiwyg']"
    # toggle button
    Status_Settings_ele = "//span[@id='coupon_status']"




    def setup_class(self):
        self.driver.get(ReadConfig.getAdminPageURL())  
        self.driver.maximize_window()

    def test_Systemsettings(self):
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

        # Wait and click on system settings
        System_settings = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, self.System_settings_element))
        )
        System_settings.click()

        self.driver.execute_script("document.body.style.zoom='50%'")
        # System settings
        # System Email
        System_Email = self.driver.find_element(By.XPATH,self.System_Email_ele)
        System_Email.clear()    
        System_Email.send_keys("2")
        time.sleep(2)
        # Google Analytics Tracking ID
        GoogleAnalytics_TrackingID = self.driver.find_element(By.XPATH,self.GoogleAnalytics_TrackingID_ele)
        GoogleAnalytics_TrackingID.clear()
        GoogleAnalytics_TrackingID.send_keys("https://analytics.google.com/analytics/web/?authuser=2#/p277143767/reports/intelligenthome")
        time.sleep(2)
        # Google Oauth Client ID Key
        GoogleOauth_ClientID_Key = self.driver.find_element(By.XPATH,self.GoogleOauth_ClientID_Key_ele)
        GoogleOauth_ClientID_Key.clear()
        GoogleOauth_ClientID_Key.send_keys("2")
        time.sleep(2)
        # System Phone Number
        SystemPhone_Number = self.driver.find_element(By.XPATH,self.SystemPhone_Number_ele)
        SystemPhone_Number.clear()
        SystemPhone_Number.send_keys("9876543210")
        time.sleep(2)
        # System Address
        System_Address = self.driver.find_element(By.XPATH,self.System_Address_ele)
        System_Address.clear()
        System_Address.send_keys("sample testing address")
        time.sleep(2)

        # Status Settings

        # Click on the toggle button to switch it ON
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.driver.find_element(By.XPATH, self.Status_Settings_ele))
        toggle_button = self.driver.find_element(By.XPATH,self.Status_Settings_ele)
        toggle_button.click()   
        time.sleep(2)
        # Click on the toggle button to switch it OFF
        toggle_button = self.driver.find_element(By.XPATH,self.Status_Settings_ele)
        toggle_button.click()
        time.sleep(2)

        # Screenshot
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "System settings created successfully", attachment_type= AttachmentType.PNG)
       


    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 



