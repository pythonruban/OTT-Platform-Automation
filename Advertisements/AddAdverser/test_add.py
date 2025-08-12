import os
import sys
import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

# Add project root for config access
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Firefox WebDriver Fixture
@pytest.fixture
def setup():
    driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()

# XPaths dictionary
xpaths = {
    "email": "//input[@id='advertiseremail']",
    "password": "//input[@id='advertiserpassword']",
    "login_submit": "//button[@id='advertisersubmit']",
    "adver_menu": "//span[contains(text(), 'Advertisements')]",
    "all_adver": "//a[@id='alladvertisersidebaradvertiser']",
    "add_adver": "//a[@id='addnewadvertisersidebaradvertiser']",
    "adver_name": "//input[@id='advertiserName']",
    "adver_upload": "(//div[contains(@class,'indicatorContainer')])[1]",
    "adver_upload_input": "(//div[contains(@class,'control')])[1]//input",
    "adver_url_input": "//input[@id='advertiserAdsUrl']",
    "adver_category": "(//div[contains(@class,'indicatorContainer')])[2]",
    "adver_category_input": "(//div[contains(@class,'control')])[2]//input",
    "adver_position": "(//div[contains(@class,'indicatorContainer')])[3]",
    "adver_position_input": "(//div[contains(@class,'control')])[3]//input",
    "submit": "//button[@id='advertiserSubmitButton']",
    "admin_username": "//input[@id='signin-email']",
    "admin_password": "//input[@id='signin-password']",
    "admin_login_btn": "//span[text()='Login']",
    "ads_list_menu": "//a[@href='/ads-list']",
    "enable_switch": "(//span[@class='admin-slider position-absolute admin-round '])[1]",
    "enable_popup_btn": "//span[text()='Enable']"
}

# Helper: wait for overlays
def Adverser_add(driver, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "overlay-container"))
        )
    except:
        pass

# Helper: click
def wait_and_click(driver, wait, xpath):
    Adverser_add(driver)
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    time.sleep(0.3)
    element.click()

# Helper: send keys
def wait_and_send_keys(driver, wait, xpath, value):
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    element.clear()
    element.send_keys(value)

@allure.feature("Advertisement Module")
class TestAdvertisementUpload:

    @allure.story("Add Advertisement using Tag URL")
    def test_add_advertisement(self, setup: WebDriver):
        driver = setup
        wait = WebDriverWait(driver, 15)

        url = ReadConfig.getAdvertiserPageURL()
        email = ReadConfig.getAdverEmail()
        password = ReadConfig.getAdverPassword()

        driver.get(url)

        with allure.step("Login using advertiser credentials"):
            wait_and_send_keys(driver, wait, xpaths["email"], email)
            wait_and_send_keys(driver, wait, xpaths["password"], password)
            wait_and_click(driver, wait, xpaths["login_submit"])
            allure.attach(driver.get_screenshot_as_png(), name="Login_Advertiser", attachment_type=AttachmentType.PNG)
            time.sleep(2)
        with allure.step("Open Advertisement module"):
            wait_and_click(driver, wait, xpaths["adver_menu"])
            allure.attach(driver.get_screenshot_as_png(), name="Open_Adver_Module", attachment_type=AttachmentType.PNG)
            time.sleep(2)
        with allure.step("Click Add Advertisement"):
            wait_and_click(driver, wait, xpaths["add_adver"])
            allure.attach(driver.get_screenshot_as_png(), name="Add_Adver_Click", attachment_type=AttachmentType.PNG)
            time.sleep(2)
        with allure.step("Enter Advertisement Name"):
            wait_and_send_keys(driver, wait, xpaths["adver_name"], "Sample")
            allure.attach(driver.get_screenshot_as_png(), name="Enter_Adver_Name", attachment_type=AttachmentType.PNG)
            time.sleep(2)
        with allure.step("Select Upload Type: Tag URL"):
            wait_and_click(driver, wait, xpaths["adver_upload"])
            wait_and_send_keys(driver, wait, xpaths["adver_upload_input"], "Tag URL")
            wait_and_click(driver, wait, "//div[contains(text(),'Tag URL')]")
            allure.attach(driver.get_screenshot_as_png(), name="Upload_TagURL", attachment_type=AttachmentType.PNG)

        with allure.step("Enter Tag URL"):
            wait_and_send_keys(driver, wait, xpaths["adver_url_input"], "https://google.com")
            allure.attach(driver.get_screenshot_as_png(), name="Enter_Tag_URL", attachment_type=AttachmentType.PNG)
               
        with allure.step("Select Category: test"):
            wait_and_click(driver, wait, xpaths["adver_category"])
            wait_and_send_keys(driver, wait, xpaths["adver_category_input"], "Sample")
            wait_and_click(driver, wait, "//div[contains(text(),'Sample')]")
            allure.attach(driver.get_screenshot_as_png(), name="Category_test", attachment_type=AttachmentType.PNG)

        with allure.step("Select Position: pre"):
            wait_and_click(driver, wait, xpaths["adver_position"])
            wait_and_send_keys(driver, wait, xpaths["adver_position_input"], "pre")
            wait_and_click(driver, wait, "//div[contains(text(),'pre')]")
            allure.attach(driver.get_screenshot_as_png(), name="Position_pre", attachment_type=AttachmentType.PNG)

        with allure.step("Submit Advertisement"):
            wait_and_click(driver, wait, xpaths["submit"])
            allure.attach(driver.get_screenshot_as_png(), name="Submit_Adver", attachment_type=AttachmentType.PNG)
            time.sleep(2)
        with allure.step("Verify Advertisement Submission"):
            assert "success" in driver.page_source.lower() or "added" in driver.page_source.lower(), "Submission failed"
            allure.attach(driver.get_screenshot_as_png(), name="Adver_Verified", attachment_type=AttachmentType.PNG)
            time.sleep(4)
        with allure.step("Redirect to Admin Page and open Ads L ist"):
            admin_url = ReadConfig.getAdminPageURL()
            driver.get(admin_url)
            time.sleep(2)

            username = ReadConfig.getAdminId()
            password = ReadConfig.getPassword()

            wait_and_send_keys(driver, wait, xpaths["admin_username"], username)
            wait_and_send_keys(driver, wait, xpaths["admin_password"], password)
            wait_and_click(driver, wait, xpaths["admin_login_btn"])
            allure.attach(driver.get_screenshot_as_png(), name="Admin_Login", attachment_type=AttachmentType.PNG)

            driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
            time.sleep(1)

            wait_and_click(driver, wait, xpaths["ads_list_menu"])
            allure.attach(driver.get_screenshot_as_png(), name="Open_Ads_List", attachment_type=AttachmentType.PNG)

        with allure.step("Enable newly added ad"):
            wait_and_click(driver, wait, xpaths["enable_switch"])
            allure.attach(driver.get_screenshot_as_png(), name="Enable_Toggle_Clicked", attachment_type=AttachmentType.PNG)

            wait_and_click(driver, wait, xpaths["enable_popup_btn"])
            allure.attach(driver.get_screenshot_as_png(), name="Enable_Confirmed", attachment_type=AttachmentType.PNG)

        with allure.step("Redirect back to Advertiser and open All Advertiser List"):
            advertiser_url = ReadConfig.getAdvertiserPageURL()
            driver.get(advertiser_url)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="All_list", attachment_type=AttachmentType.PNG)

    @classmethod
    def teardown_class(cls):
        try:
            cls.driver.quit()
        except Exception as e:
            print("⚠️ Driver quit failed:", str(e))

            

     


       