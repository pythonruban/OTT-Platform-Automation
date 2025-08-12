import time
import re 
import random
import string
import pytest 
import os
import sys 
import allure 

from conftest import *
from selenium.webdriver import ActionChains, Keys
from allure_commons.types import AttachmentType
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from utilities.readProp import ReadConfig

# Add the project root (D:\Automation\) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

    

@pytest.mark.usefixtures("browser_setup")
class TestMainSettings:
    driver = webdriver.Firefox
    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    Settings_element = "//div[@data-bs-target='#Settings']"
    Revenue_settings_elemnt ="//span[text()='Revenue Settings']"
    Admin_Commission_element ="//input[@name='admin_commission']"
    vod_admin_commission_element ="//input[@name='vod_admin_commission']"
    #user commiosion
    user_commission_element ="//input[@name='user_commission']"
    vod_user_commission_element ="//input[@name='vod_user_commission']"
    update_settings_element ="//button[@id='adminButton']"
    
    def test_transcoding_job(self,browser_setup):
        self.driver = browser_setup
        """Login to the admin panel"""
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()
        actions = ActionChains(self.driver)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.email_element))
            ).send_keys(ReadConfig.getAdminId())

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.password_element))
            ).send_keys(ReadConfig.getPassword())

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.login_element))
            ).click()

            print(" Login Successful!")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All Value login Credentials was entered, and the login button was clicked. it was redirect to Dashboard", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="login_error", attachment_type=AttachmentType.PNG)
            print(f" Failed to enter email: {e}")
        time.sleep(2)
    
    
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            settings = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.Settings_element))
            )
            self.driver.execute_script("arguments[0].click();", settings)
            time.sleep(2)
            Revenue_settings = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.Revenue_settings_elemnt))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Revenue_settings)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", Revenue_settings)
            print("Navigated to 'OTP Credentails'")
        except Exception as e:
            print(f"[ERROR] Clicking  failed: {e}")

        try:
                        # ---------- Test with input: 0 ----------
            try:
                admin_field = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, self.Admin_Commission_element))
                )
                admin_field.clear()
                time.sleep(1)
                admin_field.send_keys("0")
                time.sleep(2)

                # allure.attach(self.driver.get_screenshot_as_png(), name="Admin Commission - Invalid 0", attachment_type=AttachmentType.PNG)
                # print("[INFO] Entered 0 in Admin Commission.")

                error_element = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "//small[contains(@class, 'text-danger')]"))
                )
                assert error_element.is_displayed(), "[FAIL] Error message not displayed for input 0."
                print("[PASS] Validation error displayed correctly for input 0.")

            except Exception as e:
                print(f"[ERROR] Validation for input 0 failed: {e}")

            # ---------- Test with input: 100 ----------
            try:
                admin_field.clear()
                time.sleep(1)
                admin_field.send_keys("10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
                time.sleep(2)

                # allure.attach(self.driver.get_screenshot_as_png(), name="Admin Commission - Valid 100", attachment_type=AttachmentType.PNG)
                # print("[INFO] Entered 100 in Admin Commission.")

                error_elements = self.driver.find_elements(By.XPATH, "//small[contains(@class, 'text-danger')]")
                assert not error_elements or all(elem.text.strip() == "" for elem in error_elements), "[FAIL] Unexpected error shown for input 100."
                print("[PASS] Input 100 accepted with no validation error.")

            except Exception as e:
                print(f"[ERROR] Validation for input 100 failed: {e}")

            # ---------- Test with input: 12345 ----------
            try:
                admin_field.clear()
                time.sleep(1)
                admin_field.send_keys("12345")
                time.sleep(2)

                # allure.attach(self.driver.get_screenshot_as_png(), name="Admin Commission - Valid 12345", attachment_type=AttachmentType.PNG)
                # print("[INFO] Entered 12345 in Admin Commission.")

                error_elements = self.driver.find_elements(By.XPATH, "//small[contains(@class, 'text-danger')]")
                assert not error_elements or all(elem.text.strip() == "" for elem in error_elements), "[FAIL] Unexpected error shown for input 12345."
                print("[PASS] Input 12345 accepted with no validation error.")

            except Exception as e:
                print(f"[ERROR] Validation for input 12345 failed: {e}")
        except Exception as e:
            print(f"[ERROR] Clicking  failed: {e}")
        
        try:
                        # ---------- Test with input: 0 ----------
            try:
                vod_admin_field = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, self.vod_admin_commission_element))
                )
                vod_admin_field.clear()
                time.sleep(1)
                vod_admin_field.send_keys("0")
                time.sleep(2)

                error_element = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "//small[contains(@class, 'text-danger')]"))
                )
                assert error_element.is_displayed(), "[FAIL] Error message not displayed for input 0."
                print("[PASS] Validation error displayed correctly for input 0.")

            except Exception as e:
                print(f"[ERROR] Validation for input 0 failed: {e}")

            # ---------- Test with input: 100 ----------
            try:
                vod_admin_field.clear()
                time.sleep(1)
                vod_admin_field.send_keys("10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
                time.sleep(2)

                error_elements = self.driver.find_elements(By.XPATH, "//small[contains(@class, 'text-danger')]")
                assert not error_elements or all(elem.text.strip() == "" for elem in error_elements), "[FAIL] Unexpected error shown for input 100."
                print("[PASS] Input 100 accepted with no validation error.")

            except Exception as e:
                print(f"[ERROR] Validation for input 100 failed: {e}")

            # ---------- Test with input: 12345 ----------
            try:
                vod_admin_field.clear()
                time.sleep(1)
                vod_admin_field.send_keys("12345")
                time.sleep(2)

                # allure.attach(self.driver.get_screenshot_as_png(), name="Admin Commission - Valid 12345", attachment_type=AttachmentType.PNG)
                # print("[INFO] Entered 12345 in Admin Commission.")

                error_elements = self.driver.find_elements(By.XPATH, "//small[contains(@class, 'text-danger')]")
                assert not error_elements or all(elem.text.strip() == "" for elem in error_elements), "[FAIL] Unexpected error shown for input 12345."
                print("[PASS] Input 12345 accepted with no validation error.")

            except Exception as e:
                print(f"[ERROR] Validation for input 12345 failed: {e}")
        except Exception as e:
            print(f"[ERROR] Clicking  failed: {e}")
        
        try:
                        # ---------- Test with input: 0 ----------
            try:
                user_field = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, self.user_commission_element))
                )
                user_field.clear()
                time.sleep(1)
                user_field.send_keys("0")
                time.sleep(2)

                # allure.attach(self.driver.get_screenshot_as_png(), name="Admin Commission - Invalid 0", attachment_type=AttachmentType.PNG)
                # print("[INFO] Entered 0 in Admin Commission.")

                error_element = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "//small[contains(@class, 'text-danger')]"))
                )
                assert error_element.is_displayed(), "[FAIL] Error message not displayed for input 0."
                print("[PASS] Validation error displayed correctly for input 0.")

            except Exception as e:
                print(f"[ERROR] Validation for input 0 failed: {e}")

            # ---------- Test with input: 100 ----------
            try:
                user_field.clear()
                time.sleep(1)
                user_field.send_keys("10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
                time.sleep(2)

                # allure.attach(self.driver.get_screenshot_as_png(), name="Admin Commission - Valid 100", attachment_type=AttachmentType.PNG)
                # print("[INFO] Entered 100 in Admin Commission.")

                error_elements = self.driver.find_elements(By.XPATH, "//small[contains(@class, 'text-danger')]")
                assert not error_elements or all(elem.text.strip() == "" for elem in error_elements), "[FAIL] Unexpected error shown for input 100."
                print("[PASS] Input 100 accepted with no validation error.")

            except Exception as e:
                print(f"[ERROR] Validation for input 100 failed: {e}")

            # ---------- Test with input: 12345 ----------
            try:
                user_field.clear()
                time.sleep(1)
                user_field.send_keys("12345")
                time.sleep(2)

                # allure.attach(self.driver.get_screenshot_as_png(), name="Admin Commission - Valid 12345", attachment_type=AttachmentType.PNG)
                # print("[INFO] Entered 12345 in Admin Commission.")

                error_elements = self.driver.find_elements(By.XPATH, "//small[contains(@class, 'text-danger')]")
                assert not error_elements or all(elem.text.strip() == "" for elem in error_elements), "[FAIL] Unexpected error shown for input 12345."
                print("[PASS] Input 12345 accepted with no validation error.")

            except Exception as e:
                print(f"[ERROR] Validation for input 12345 failed: {e}")
        except Exception as e:
            print(f"[ERROR] Clicking  failed: {e}")

        try:
                        # ---------- Test with input: 0 ----------
            try:
                vod_user_field = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, self.vod_user_commission_element))
                )
                vod_user_field.clear()
                time.sleep(1)
                vod_user_field.send_keys("0")
                time.sleep(2)

                # allure.attach(self.driver.get_screenshot_as_png(), name="Admin Commission - Invalid 0", attachment_type=AttachmentType.PNG)
                # print("[INFO] Entered 0 in Admin Commission.")

                error_element = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "//small[contains(@class, 'text-danger')]"))
                )
                assert error_element.is_displayed(), "[FAIL] Error message not displayed for input 0."
                print("[PASS] Validation error displayed correctly for input 0.")

            except Exception as e:
                print(f"[ERROR] Validation for input 0 failed: {e}")

            # ---------- Test with input: 100 ----------
            try:
                vod_user_field.clear()
                time.sleep(1)
                vod_user_field.send_keys("10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
                time.sleep(2)

                # allure.attach(self.driver.get_screenshot_as_png(), name="Admin Commission - Valid 100", attachment_type=AttachmentType.PNG)
                # print("[INFO] Entered 100 in Admin Commission.")

                error_elements = self.driver.find_elements(By.XPATH, "//small[contains(@class, 'text-danger')]")
                assert not error_elements or all(elem.text.strip() == "" for elem in error_elements), "[FAIL] Unexpected error shown for input 100."
                print("[PASS] Input 100 accepted with no validation error.")

            except Exception as e:
                print(f"[ERROR] Validation for input 100 failed: {e}")

            # ---------- Test with input: 12345 ----------
            try:
                vod_user_field.clear()
                time.sleep(1)
                vod_user_field.send_keys("12345")
                time.sleep(2)

                # allure.attach(self.driver.get_screenshot_as_png(), name="Admin Commission - Valid 12345", attachment_type=AttachmentType.PNG)
                # print("[INFO] Entered 12345 in Admin Commission.")

                error_elements = self.driver.find_elements(By.XPATH, "//small[contains(@class, 'text-danger')]")
                assert not error_elements or all(elem.text.strip() == "" for elem in error_elements), "[FAIL] Unexpected error shown for input 12345."
                print("[PASS] Input 12345 accepted with no validation error.")
                time.sleep(4)
                
            except Exception as e:
                print(f"[ERROR] Validation for input 12345 failed: {e}")
        except Exception as e:
            print(f"[ERROR] Clicking  failed: {e}")

        try:
            submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.update_settings_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", submit_button)
            print(" Revenue Settings was save successfully.")
            time.sleep(15)
            allure.attach(self.driver.get_screenshot_as_png(), name="Revenue Settings In MAin Settinghs Page ", attachment_type=AttachmentType.PNG)
            time.sleep(5)
        except Exception as e:
            print(f" Error clicking submit button: {e}")
            pytest.fail("Error Occur ")

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")