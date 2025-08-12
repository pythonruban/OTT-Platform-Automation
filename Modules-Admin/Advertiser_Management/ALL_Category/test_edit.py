import time
import random
import string
import pytest
import os
import sys
import allure

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType

from utilities.readProp import ReadConfig

# Add project root path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

xpaths = {
    "email": "(//input[@type='email'])[2]",
    "password": "(//input[@name='password'])[1]",
    "login_btn": "(//button[@type='submit'])[2]",
    "ads_list": "//span[text()='Ads List']",
    "edit_icon": "(//span[contains(@class, 'editdropdown-button')])[1]",
    "edit_menu": "(//span[contains(text(), 'Edit')])[1]",
    "adver_name": "//input[@name='ads_name']",
    "slider_button": "//span[@class='admin-slider position-absolute admin-round ']",
    "submit_btn": "//span[@class='undefined   ']",

    
}

@pytest.mark.usefixtures("browser_setup")
class TestAdvertiser:
    def test_edit_advertisement_and_update(self, browser_setup):
        driver = browser_setup
        wait = WebDriverWait(driver, 20)

        driver.get(ReadConfig.getAdminPageURL())
        driver.maximize_window()

        # Login
        with allure.step("Login to Admin"):
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getAdminId())
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["password"]))).send_keys(ReadConfig.getPassword())
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_btn"]))).click()
            allure.attach(driver.get_screenshot_as_png(), name="Admin_Login", attachment_type=AttachmentType.PNG)

        # Navigate to Ads List
        with allure.step("Navigate to Ads List"):
            time.sleep(10)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            ads_list = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["ads_list"])))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", ads_list)
            driver.execute_script("arguments[0].click();", ads_list)

        # Click Edit
        with allure.step("Click Edit from first ad entry"):
            edit_btn = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["edit_icon"])))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", edit_btn)
            ActionChains(driver).move_to_element(edit_btn).perform()
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["edit_menu"]))).click()
            time.sleep(2)

        # Generate random name
        new_name = ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 7)))

        # Update name
        with allure.step("Update Advertisement Name"):
            name_field = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["adver_name"])))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", name_field)
            name_field.clear()
            name_field.send_keys(new_name)
            allure.attach(driver.get_screenshot_as_png(), name="Ad_Name_Update", attachment_type=AttachmentType.PNG)

        # Select Upload Type: slider
        with allure.step("slider button enable"):
            slider = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["slider_button"])))
            driver.execute_script("arguments[0].click();", slider)
            allure.attach(driver.get_screenshot_as_png(), name="slider_button", attachment_type=AttachmentType.PNG)
            time.sleep(3)
        
        # Submit update
        with allure.step("Submit Updated Advertisement"):
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["submit_btn"]))).click()
            allure.attach(driver.get_screenshot_as_png(), name="Final_Submit", attachment_type=AttachmentType.PNG)
            time.sleep(3)

        # Final Assertion
        with allure.step("Verify update successful"):
            assert "success" in driver.page_source.lower() or "updated" in driver.page_source.lower(), "Update Failed"
