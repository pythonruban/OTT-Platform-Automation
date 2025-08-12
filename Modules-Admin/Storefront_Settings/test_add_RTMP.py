import os
import time
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig
from conftest import * 


@pytest.mark.usefixtures("browser_setup")
class TestAddNewRTMP:
    
    driver: WebDriver

    # File paths
    base_dir = os.path.join(os.getcwd(), "tmp")
    names = os.path.abspath(os.path.join(base_dir, "sample1.mp4"))

    # XPATH locators
    email_element = "//div[3]//input[1]"
    password_element = "//input[contains(@placeholder,'Enter Password')]"
    login_btn_element = "//span[normalize-space()='login']"
    storefront_Settings_element = "//span[@class='ms-2 text-break'][normalize-space()='Storefront Settings']"
    RTMP_URL_settings_element = "//a[contains(@href,'/site/rtmpurl')]//div[contains(@class,'sitecard p-2')]//div[contains(@class,'row')]//div[contains(@class,'col-lg-9')]//div[contains(@class,'card-body p-2')]//p[contains(@class,'card-text')][normalize-space()='Control the overall RTPM URLS of your website']"
    Add_RTMP_element = "//button[normalize-space()='Add RTMP']"

    def setup_class(self):
        self.driver.get(ReadConfig.getAdminPageURL())  
        self.driver.maximize_window()

    def test_AddNewRTMP(self):
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
        rtmp_element = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, self.RTMP_URL_settings_element))
        )
        rtmp_element.click()

        # Locate the RTMP URL input field and enter a value
        rtmp_input = self.driver.find_element(By.XPATH, "//input[@placeholder='rtmp://38.170.194.9:1935/show/']")
        rtmp_input.clear()
        rtmp_input.send_keys("rtmp://75.119.145.126:1935/show/")

        # Locate the HLS URL input field and enter a value
        hls_input = self.driver.find_element(By.XPATH, "//input[@placeholder='http://75.119.145.126:9090/hls/handleUpdatekey/index.m3u8']")
        hls_input.clear()
        hls_input.send_keys("http://75.119.145.126:9090/hls/handleUpdatekey/index.m3u8")

        # Locate and click the "Update RTMP Setting" button
        update_button = self.driver.find_element(By.XPATH, "//button[text()='Update RTMP Setting']")
        update_button.click()



        # Wait for some time to observe the result
        time.sleep(5)




        # Capture success screenshot
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="New RTMP created Successfully.", attachment_type=AttachmentType.PNG)

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 
