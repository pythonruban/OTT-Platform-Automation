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

# XPaths
xpaths = {
    "email": "//input[@id='advertiseremail']",
    "password": "//input[@id='advertiserpassword']",
    "login_submit": "//button[@id='advertisersubmit']",
    "adver_menu": "//span[contains(text(), 'Advertisements')]",
    "all_adver": "//a[@id='alladvertisersidebaradvertiser']",
    "edit_element": "(//span[contains(@class, 'editdropdown-button')])[1]",
    "delete_menu": "(//span[contains(text(), 'Delete')])[1]",
    "comfrm_delete_button": "//span[text()='Delete']"
}

# Helper: Click with scroll & wait
def wait_and_click(driver, wait, xpath):
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    time.sleep(0.5)
    element.click()
    time.sleep(3)

# Helper: Send keys with scroll & wait
def wait_and_send_keys(driver, wait, xpath, value):
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    element.clear()
    element.send_keys(value)
    time.sleep(3)

@allure.feature("Advertisement Module")
class TestAdvertisementUpload:

    @allure.story("Delete Advertisement from All Advertisement list")
    def test_advertiser_delete_flow(self, setup: WebDriver):
        driver = setup
        wait = WebDriverWait(driver, 20)

        driver.get(ReadConfig.getAdvertiserPageURL())

        with allure.step("Login to Advertiser Panel"):
            wait_and_send_keys(driver, wait, xpaths["email"], ReadConfig.getAdverEmail())
            wait_and_send_keys(driver, wait, xpaths["password"], ReadConfig.getAdverPassword())
            wait_and_click(driver, wait, xpaths["login_submit"])
            allure.attach(driver.get_screenshot_as_png(), name="Login_Success", attachment_type=AttachmentType.PNG)

        with allure.step("Click Advertisement Menu"):
            wait_and_click(driver, wait, xpaths["adver_menu"])
            allure.attach(driver.get_screenshot_as_png(), name="Clicked_Adver_Menu", attachment_type=AttachmentType.PNG)

        with allure.step("Click All Advertisement"):
            wait_and_click(driver, wait, xpaths["all_adver"])
            allure.attach(driver.get_screenshot_as_png(), name="Clicked_All_Ads", attachment_type=AttachmentType.PNG)

        with allure.step("Click Edit Icon (⋮)"):
            wait_and_click(driver, wait, xpaths["edit_element"])
            allure.attach(driver.get_screenshot_as_png(), name="Clicked_Edit_Icon", attachment_type=AttachmentType.PNG)

        with allure.step("Click Delete in Dropdown"):
            wait_and_click(driver, wait, xpaths["delete_menu"])
            allure.attach(driver.get_screenshot_as_png(), name="Clicked_Delete", attachment_type=AttachmentType.PNG)

        with allure.step("Click Yes in Confirmation Popup"):
            wait_and_click(driver, wait, xpaths["comfrm_delete_button"])
            allure.attach(driver.get_screenshot_as_png(), name="Confirmed_Delete", attachment_type=AttachmentType.PNG)

        with allure.step("Verify Delete"):
            assert "success" in driver.page_source.lower() or "deleted" in driver.page_source.lower(), "Delete may have failed"
