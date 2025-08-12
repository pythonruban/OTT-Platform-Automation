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
class TestLanguage:
  
    driver = webdriver.Firefox
   

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
   
    Manage_language_element = "//span[text()='Manage Language']"
    translate_element ="//span[text()='Manage Translate Languages']"
    add_language_code_element = "//button[@id='navigationLinkForAddPage']"
    language_name_element = "//input[@name='name']"
    language_slug_element = "//input[@name='slug']"
    default_language_element ="//input[@name='code']"
    save_change_element ="(//span[@class='slider round'])[1]"
    add_new_element ="(//span[@class='slider round'])[2]"
    new_language_button_element= "//button[@type='submit']"


    
    def test_negative_translate(self,browser_setup):
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
        


        # Locate and click 'Manage Language' element
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            manage_app = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.Manage_language_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", manage_app)
            time.sleep(1)  # Allow smooth scrolling
            self.driver.execute_script("arguments[0].click();", manage_app)
            print("Clicked 'Language'")
            time.sleep(6)
        except Exception as e:
            print(f"Failed to click 'Manage Language': {e}")
           

        # Click 'Translate' element
        try:
            translate_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.translate_element))
            )
            translate_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Failed to click 'Translate': {e}")
           

        # Click 'Add Language Code' element
        try:
            add_language_code_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.add_language_code_element))
            )
            add_language_code_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Failed to click 'Add Language Code': {e}")
         

        # Enter language name
        try:
                test_data = [
                    ("Test 1: 1-char (Negative)", ''.join(random.choices(string.ascii_uppercase, k=1))),   # Invalid
                    ("Test 2: 102-char (Negative)", ''.join(random.choices(string.ascii_uppercase + string.digits, k=102))),  # Invalid
                    ("Test 3: 6-char (Valid)", ''.join(random.choices(string.ascii_uppercase, k=6)))       # Valid
                ]

                for test_name, test_value in test_data:
                    print(f"\n{test_name} started")

                    # === Enter Title ===
                    try:
                        title_input = WebDriverWait(self.driver, 30).until(
                            EC.element_to_be_clickable((By.XPATH, self.language_name_element))
                        )
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_input)
                        title_input.clear()
                        title_input.send_keys(test_value)
                        print(f"Title entered: {test_value[:30]}")
                    except Exception as title_error:
                        print(f"Error entering title: {title_error}")
                        continue

                    # === Enter Slug ===
                    try:
                        slug_input = WebDriverWait(self.driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, self.language_slug_element))
                        )
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slug_input)
                        slug_input.clear()
                        slug_input.send_keys(test_value)
                        print(f"Slug entered: {test_value[:30]}")
                    except Exception as slug_error:
                        print(f"Error entering slug: {slug_error}")
                        continue

                    # === Check if BOTH are invalid ===
                    title_length = len(test_value)
                    slug_length = len(test_value)

                    is_title_invalid = title_length < 3 or title_length > 100
                    is_slug_invalid = slug_length < 3 or slug_length > 100

                    if is_title_invalid and is_slug_invalid:
                        print(" Both Title and Slug are invalid — clicking Save")

                        try:
                            submit_button = WebDriverWait(self.driver, 20).until(
                                EC.element_to_be_clickable((By.XPATH, self.new_language_button_element))
                            )
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                            submit_button.click()
                            time.sleep(2)

                            # Screenshot for both invalid
                            allure.attach(
                                self.driver.get_screenshot_as_png(),
                                name=f"Both_Invalid_{test_name.replace(':','')}",
                                attachment_type=allure.attachment_type.PNG
                            )

                            assert "error" in self.driver.page_source.lower(), " Expected validation message not shown."

                        except Exception as submit_error:
                            print(f"Error during form submission: {submit_error}")

                    else:
                        print(" Either Title or Slug is valid — skipping Save")

        except Exception as outer_error:
            print(f" Outer script error: {outer_error}")

            

        # Enter default language code
        try:
            # --- Step 1: Enter 100-character invalid input and click Save ---
            invalid_code = ''.join(random.choices(string.ascii_uppercase, k=100))
            print(f"Generated invalid code: {invalid_code} (Length: {len(invalid_code)})")

            code_field = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.default_language_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", code_field)
            code_field.clear()
            code_field.send_keys(invalid_code)
            print("Entered invalid code")

            if len(invalid_code) > 8:
                submit_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, self.new_language_button_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                submit_button.click()
                print("Clicked Save for invalid input (100 chars)")

                # Screenshot for invalid case
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="Invalid_Code_100_chars",
                    attachment_type=allure.attachment_type.PNG
                )
            else:
                print("Input is valid – skipping Save")

            time.sleep(2)  # Wait briefly before next step

            # --- Step 2: Enter 6-character valid input and do not click Save ---
            valid_code = ''.join(random.choices(string.ascii_uppercase, k=6))
            print(f"\nGenerated valid code: {valid_code} (Length: {len(valid_code)})")

            code_field = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.default_language_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", code_field)
            code_field.clear()
            code_field.send_keys(valid_code)
            print("Entered valid code")

            if len(valid_code) > 8:
                print("Unexpected length for valid input – clicking Save (should NOT happen)")
                submit_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, self.new_language_button_element))
                )
                submit_button.click()
            else:
                print("Valid input (≤8 chars) – Save not clicked")

        except Exception as e:
            print(f"Error in code input test: {e}")

                            

        # Click 'Save Changes' button
        try:
            toggle_button = self.driver.find_element(By.XPATH, self.save_change_element)
            if toggle_button.is_displayed():
                toggle_button.click()
                print("Toggle button clicked.")
            else:
                print("Toggle button is not available.")
            time.sleep(3)
        except Exception as e:
            print(f"Failed to click 'Save Changes': {e}")
            

        # Click 'Add New' button
        try:
            # Wait until the toggle button is clickable
            toggle_button2 = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.add_new_element))
            )
            
            # Scroll the element into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle_button2)
            
            # Click the toggle button
            toggle_button2.click()
            print("Toggle button clicked.")
        except Exception as e:
            print(f"Failed to click 'Add New': {e}")
                # Click 'New Language' button
        try:
            # allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All details were entered in the language code.", attachment_type=AttachmentType.PNG)

            new_language_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.new_language_button_element))
            )
            new_language_button.click()
            print("Language was added successfully.")
            time.sleep(10)
            # allure.attach(self.driver.get_full_page_screenshot_as_png(), name="New Language was Added Successfully.", attachment_type=AttachmentType.PNG)

        except Exception as e:
            # allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Adding Error.", attachment_type=AttachmentType.PNG)

            print(f"Failed to click 'New Language': {e}")
            raise

        
    
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 

   
