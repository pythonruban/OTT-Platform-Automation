import os
import sys
import time
import pytest
import allure

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

# Add root path for config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# XPaths
xpaths = {
    "email": "//input[@id='advertiseremail']",
    "password": "//input[@id='advertiserpassword']",
    "login_submit": "//button[@id='advertisersubmit']",
    "adver_menu": "//span[contains(text(), 'Advertisements')]",
    "all_adver": "//a[@id='alladvertisersidebaradvertiser']",
    "edit_element": "(//span[contains(@class, 'editdropdown-button')])[1]",
    "edit_menu": "(//span[@class='ms-2 theme-text-color '])[1]",
    "adver_name": "//input[@id='advertiserads_name']",
    "adver_upload": "//select[@id='advertiserads_upload_type']",
    "adver_path": "//input[@id='advertiserads_path']",
    "adver_redirect": "//input[@id='advertiserads_redirection_url']",
    "adver_category_input": "(//div[contains(@class,'control')])[2]//input",
    "category_option": "//div[contains(text(),'test')]",  # change to actual category
    "adver_position": "//select[@id='advertiserads_position']",
    "submit": "//button[@id='advertiser-update-button']"
}

@pytest.fixture
def setup():
    driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()

@allure.feature("Advertisement Edit Flow")
class TestAdvertiserEdit:

    @allure.story("Edit Advertisement with Path upload type")
    def test_edit_advertisement_upload(self, setup):
        driver = setup
        wait = WebDriverWait(driver, 25)

        driver.get(ReadConfig.getAdvertiserPageURL())
        time.sleep(3)

        # Login
        with allure.step("Login to Advertiser Panel"):
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getAdverEmail())
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["password"]))).send_keys(ReadConfig.getAdverPassword())
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_submit"]))).click()
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="Login_Success", attachment_type=AttachmentType.PNG)

        # Navigate to Advertisement > All Advertiser
        with allure.step("Navigate to Advertisement > All Advertiser"):
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["adver_menu"]))).click()
            time.sleep(3)
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["all_adver"]))).click()
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="Opened_All_Adver", attachment_type=AttachmentType.PNG)

        # Click Edit
        with allure.step("Click Edit Button"):
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["edit_element"]))).click()
            time.sleep(2)
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["edit_menu"]))).click()
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="Opened_Edit_Form", attachment_type=AttachmentType.PNG)

        # Update Advertisement Name
        with allure.step("Update Advertisement Name"):
            name_input = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["adver_name"])))
            name_input.clear()
            name_input.send_keys("Edited Ad Name")
            time.sleep(2)

        # Select Upload Type: Path
        with allure.step("Select Upload Type: Path"):
            upload_select = Select(wait.until(EC.presence_of_element_located((By.XPATH, xpaths["adver_upload"]))))
            upload_select.select_by_visible_text("Path")
            time.sleep(2)

        # Enter Path (e.g., internal path string)
        with allure.step("Enter Path for Upload"):
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["adver_path"]))).send_keys("https://cdn.myserver.com/sample.mp4")
            time.sleep(2)

        # Enter Redirection URL
        with allure.step("Enter Redirection URL"):
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["adver_redirect"]))).send_keys("https://google.com")
            time.sleep(2)

        # Select Category
        with allure.step("Select Advertisement Category"):
            category_input = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["adver_category_input"])))
            category_input.send_keys("test")  # adjust if needed
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["category_option"]))).click()
            time.sleep(2)

        # Select Position
        with allure.step("Select Advertisement Position"):
            position_select = Select(wait.until(EC.presence_of_element_located((By.XPATH, xpaths["adver_position"]))))
            position_select.select_by_visible_text("Pre")  # adjust if needed
            time.sleep(2)

        # Submit Form
        with allure.step("Submit the Updated Advertisement"):
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["submit"]))).click()
            time.sleep(4)
            allure.attach(driver.get_screenshot_as_png(), name="Submitted_Update", attachment_type=AttachmentType.PNG)
