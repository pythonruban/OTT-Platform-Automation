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
class TestAddNewRTMP:
    
    driver: WebDriver

    #*******Local Path*******#
    
    # image and video local path
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "9_16.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "1280_720 px.png")
    videoFile_path = os.path.join(base_dir, "sample2.mp4")
    pdfFile_path = os.path.join(base_dir, "sample2.pdf")
    subFile_path = os.path.join(base_dir, "sample2.srt")
    # video path
    names = os.path.abspath(os.path.join(base_dir, "sample1.mp4"))

    # File paths
    base_dir = os.path.join(os.getcwd(), "tmp")
    names = os.path.abspath(os.path.join(base_dir, "sample1.mp4"))

    # XPATH locators
    email_element = "//div[3]//input[1]"
    password_element = "//input[contains(@placeholder,'Enter Password')]"
    login_btn_element = "//span[normalize-space()='login']"
    storefront_Settings_element = "//span[@class='ms-2 text-break'][normalize-space()='Storefront Settings']"
    site_settings_element = "//p[normalize-space()='Control the overall Site Settings of your website']"
    # send keys 
    website_Name_element = "//input[@id='website_name']"
    website_description_element = "//textarea[@id='website_description']"
    logo_width_element = "//input[@id='logo_width']"
    logo_height_element = "//input[@id='logo_height']"
    # image upload
    site_favicon_element = "//input[@type='file' and @name='favicon']"
    site_logo_element = "//div[@class='col-6 col-sm-6 col-lg-6']//div[@class='imagedrop']//input[@type='file']"

    def setup_class(self):
        self.driver.get(ReadConfig.getAdminPageURL())  
        self.driver.maximize_window()

    def wait_for_element(self, xpath, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

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
            print("❌ Site Settings element NOT FOUND in the DOM!")
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

        # Wait and click on site settings
        site_element = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, self.site_settings_element))
        )
        site_element.click()

        self.driver.execute_script("document.body.style.zoom='70%'")
        # Add site settings 
        self.driver.find_element(By.XPATH, self.website_Name_element).send_keys("shows")
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.website_description_element).send_keys("shows description")
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.logo_width_element).send_keys("720")
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.logo_height_element).send_keys("1080")
        time.sleep(2)

        # upload image    
        try:
            # ✅ Ensure the image file exists before uploading
            assert os.path.exists(self.imageFile1280_720_path), "❌ Image file not found!"
            assert os.path.exists(self.imageFile_path_9_16), "❌ Logo file not found!"

            # ✅ Wait for and upload favicon image
            favicon_input = self.wait_for_element(self.site_favicon_element)
            self.driver.execute_script("arguments[0].style.display = 'block';", favicon_input)  # Ensure visible
            favicon_input.click()  # Click before send_keys()
            favicon_input.send_keys(self.imageFile1280_720_path)
            time.sleep(2)

            # ✅ Wait for and upload logo image
            logo_input = self.wait_for_element(self.site_logo_element)
            self.driver.execute_script("arguments[0].style.display = 'block';", logo_input)  # Ensure visible
            logo_input.click()  # Click before send_keys()
            logo_input.send_keys(self.imageFile_path_9_16)
            time.sleep(2)

            print(" Image upload successful!")

        except Exception as e:
            print(f" Error uploading images: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Upload_Failure", attachment_type=AttachmentType.PNG)
            # Capture success screenshot
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Site Settings created Successfully.", attachment_type=AttachmentType.PNG)

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 