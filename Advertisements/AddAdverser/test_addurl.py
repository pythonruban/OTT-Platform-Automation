import os
import sys
import time
import random
import string
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

@pytest.fixture
def setup():
    driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    try:
        if driver.service.is_connectable():
            driver.quit()
    except Exception as e:
        print("⚠️ Driver already closed or unreachable:", e)

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
    "adver_category": "(//div[contains(@class,'indicatorContainer')])[2]",
    "adver_category_input": "(//div[contains(@class,'control')])[2]//input",
    "adver_position": "(//div[contains(@class,'indicatorContainer')])[3]",
    "adver_position_input": "(//div[contains(@class,'control')])[3]//input",
    "submit": "//button[@id='advertiserSubmitButton']",
    
}

# Helper: wait for overlays
def add_url(driver, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "overlay-container"))
        )
    except:
        pass

# Helper: click
def wait_and_click(driver, wait, xpath):
    add_url(driver)
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

# Helper: generate random ad name
def generate_random_ad_name(length=8):
    return "Ad_" + ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@allure.feature("Advertisement Module")
class TestAdvertisementurlUpload:

    @allure.story("Add Advertisement using Ads Video Upload")
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

        with allure.step("Open Advertisement module"):
            wait_and_click(driver, wait, xpaths["adver_menu"])
            allure.attach(driver.get_screenshot_as_png(), name="Open_Adver_Module", attachment_type=AttachmentType.PNG)

        with allure.step("Click Add Advertisement"):
            wait_and_click(driver, wait, xpaths["add_adver"])
            allure.attach(driver.get_screenshot_as_png(), name="Add_Adver_Click", attachment_type=AttachmentType.PNG)

        ad_name = generate_random_ad_name()

        with allure.step(f"Enter Advertisement Name: {ad_name}"):
            wait_and_send_keys(driver, wait, xpaths["adver_name"], ad_name)
            allure.attach(driver.get_screenshot_as_png(), name="Enter_Adver_Name", attachment_type=AttachmentType.PNG)

        with allure.step("Select Upload Type: Ads Video Upload"):
            wait_and_click(driver, wait, xpaths["adver_upload"])
            wait_and_send_keys(driver, wait, xpaths["adver_upload_input"], "Ads Video Upload")
            wait_and_click(driver, wait, "//div[contains(text(),'Ads Video Upload')]")
            allure.attach(driver.get_screenshot_as_png(), name="Upload_VideoOption_Selected", attachment_type=AttachmentType.PNG)

        with allure.step("Upload Video File"):
            video_path = os.path.abspath("C:/vodwebsite/tmp/SampleVideo_1280x720_1mb.mp4")
            video_input = wait.until(EC.presence_of_element_located((By.ID, "advertiserAdsFile")))
            video_input.send_keys(video_path)
            allure.attach(driver.get_screenshot_as_png(), name="Video_File_Uploaded", attachment_type=AttachmentType.PNG)

        with allure.step("Enter Redirect URL"):
            redirect_input = wait.until(EC.presence_of_element_located((By.ID, "advertiserRedirectUrl")))
            redirect_input.clear()
            redirect_input.send_keys("https://google.com")
            allure.attach(driver.get_screenshot_as_png(), name="Redirect_URL_Entered", attachment_type=AttachmentType.PNG)

        with allure.step("Select Category: Sample"):
            wait_and_click(driver, wait, xpaths["adver_category"])
            wait_and_send_keys(driver, wait, xpaths["adver_category_input"], "Sample")
            wait_and_click(driver, wait, "//div[contains(text(),'Sample')]")
            allure.attach(driver.get_screenshot_as_png(), name="Category_Sample", attachment_type=AttachmentType.PNG)

        with allure.step("Select Position: pre"):
            wait_and_click(driver, wait, xpaths["adver_position"])
            wait_and_send_keys(driver, wait, xpaths["adver_position_input"], "pre")
            wait_and_click(driver, wait, "//div[contains(text(),'pre')]")
            allure.attach(driver.get_screenshot_as_png(), name="Position_pre", attachment_type=AttachmentType.PNG)

        with allure.step("Submit Advertisement"):
            wait_and_click(driver, wait, xpaths["submit"])
            allure.attach(driver.get_screenshot_as_png(), name="Submit_Adver", attachment_type=AttachmentType.PNG)

        with allure.step("Verify Advertisement Submission"):
            assert "success" in driver.page_source.lower() or "added" in driver.page_source.lower(), "Submission failed"
            allure.attach(driver.get_screenshot_as_png(), name="Adver_Verified", attachment_type=AttachmentType.PNG)

        