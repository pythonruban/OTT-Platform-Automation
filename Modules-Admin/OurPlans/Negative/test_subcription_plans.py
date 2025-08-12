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
class TestOurPlans:
    driver = webdriver.Firefox

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    plans_element = "//span[text()='Plans']"
    Manage_subcription_element = "//span[text()='Manage Subscription Plans']"
    create_plan_element = "//span[text()='Add Plan']"
    #create plan
    plan_name_element= "//input[@name='plans_name']"
    billing_interval_element ="//select[@name='billing_interval']"
    billing_type_element= "//input[@name='billing_type']"
    Andriod_stack_element ="//input[@name='andriod_paystack_url']"
    content_element ="//div[@contenteditable='true' and contains(@class, 'jodit-wysiwyg')]"
    #Status Settings
    plan_status_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[1]"
    plan_trail_element="(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[3]"
    plan_active_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[2]"
    #Plan Description
    price_element="//input[@name='price']"
    trail_days_element ="//input[@name='plan_trail_days']"
    ios_product_id_element="//input[@name='ios_product_id']"
    ios_product_price_element ="//input[@name='ios_plan_price']"
    recurring_element = "//input[@name='recurring']"
    #Devices      "(//p[contains(@class, 'indicator-on-off') and contains(@class, 'on')])[3]"
    laptop_element ="(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[4]"
    laptop_input_element = "//input[@name='devices_count_1']"
    mobile_input_elemet = "//input[@name='devices_count_2']"
    mobile_element ="(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[5]"
    TV_input_element =" //input[@name='devices_count_3']"
    TV_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[6]"
    #save
    save_plan_element= "//span[text()='Create Plan']"
    
    def test_negative_subcription_plans(self,browser_setup):
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

        # Navigate to Plans
        
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            plans = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.plans_element))
            )
            self.driver.execute_script("arguments[0].click();", plans)
            print(" Navigated to 'Player Setting Management '")
            time.sleep(2)
        except Exception as e:
            print(f" Failed to click 'Plans': {e}")

        try:
            Manage_app = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.Manage_subcription_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Manage_app)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", Manage_app)
            print("Clicked 'Manage app purchase plans'")
            time.sleep(6)
        except Exception as e:
            print(" Failed to click 'Manage app purchase plans':", e)

        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.create_plan_element))
            ).click()
            time.sleep(6)
        except Exception as e:
            print(" Failed to click on 'Create Plan':", e)

        # Example for plan_name input
        try:
            test_data = [
                ("Test 1: 1-char (Negative Title)", ''.join(random.choices(string.ascii_uppercase, k=1))),
                ("Test 2: 202-char (Negative Title)", ''.join(random.choices(string.ascii_uppercase + string.digits, k=102))),
                ("Test 3: Auto Title (Valid)", ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 7))))
            ]    

            for test_name, title_value in test_data:
                try:
                    print(f"\nRunning: {test_name}")

                    # Locate and clear title input
                    title_input = WebDriverWait(self.driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, self.plan_name_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_input)
                    time.sleep(1)
                    title_input.clear()
                    title_input.send_keys(title_value)
                    print(f"Title entered: {title_value[:30]}")

                    # Click Submit button
                    submit_button = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, self.save_plan_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", submit_button)
                    print("Form submitted")

                    # If test is a negative case, take screenshot
                    if "Negative" in test_name:
                        time.sleep(2)
                        screenshot_name = f"screenshots/{test_name.replace(':', '').replace(' ', '_')}.png"
                        self.driver.save_screenshot(screenshot_name)
                        allure.attach.file(screenshot_name, name=test_name, attachment_type=AttachmentType.PNG)
                        print(f"Screenshot captured for negative case: {test_name}")

                    # Optional: Scroll back to title field
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_input)
                    time.sleep(1)

                except Exception as case_error:
                    print(f"{test_name} - Error: {case_error}")

        except Exception as total_error:
            print(f"Outer error in title validation block: {total_error}")

        # Billing Interval
        try:
            # Step 1: Submit without selecting any billing interval
            try:
                submit_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.save_plan_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                time.sleep(1)
                submit_btn.click()
                print("Submitted without selecting billing interval.")

                # Take screenshot for validation error
                time.sleep(2)
                
                allure.attach(self.driver.get_screenshot_as_png(), name="BillingIntervalEmpty", attachment_type=AttachmentType.PNG)
                print("Screenshot captured for missing billing interval.")
            except Exception as e1:
                print("Error during empty submit:", e1)

            # Step 2: Select valid option and submit
            try:
                billing = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.billing_interval_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", billing)
                Select(billing).select_by_visible_text("Year")
                time.sleep(1)
                print("Selected valid billing interval: Year")

                submit_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.save_plan_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                submit_btn.click()
                print("Submitted with valid billing interval.")
            except Exception as e2:
                print("Error selecting valid billing interval:", e2)

        except Exception as e:
            print("Outer error in billing interval test:", e)
        try:
            # Step 1: Leave empty and submit
            try:
                billing_type = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, self.billing_type_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", billing_type)

                # Manually clear input (for some JS input fields)
                billing_type.click()
                billing_type.send_keys(Keys.CONTROL + "a")
                billing_type.send_keys(Keys.BACKSPACE)
                time.sleep(1)

                submit_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.save_plan_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                submit_btn.click()
                print("Submitted with empty billing type.")

                # Take screenshot for negative case
                time.sleep(2)
                
                allure.attach(self.driver.get_screenshot_as_png(), name="BillingTypeEmpty", attachment_type=AttachmentType.PNG)
                print("Screenshot taken for empty billing type.")
            except Exception as e1:
                print(f" Error during negative billing type test: {e1}")

            # Step 2: Enter valid value ("UPI") — submit optional
            try:
                billing_type = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, self.billing_type_element))
                )
                billing_type.click()
                billing_type.send_keys(Keys.CONTROL + "a")
                billing_type.send_keys(Keys.BACKSPACE)
                billing_type.send_keys("UPI")
                print(" Entered valid billing type: UPI")

                # Optional: Uncomment this if you want to submit
                # submit_btn = WebDriverWait(self.driver, 10).until(
                #     EC.element_to_be_clickable((By.XPATH, self.save_plan_element))
                # )
                # submit_btn.click()
                # print("Submitted with valid billing type.")
            except Exception as e2:
                print(f" Error during valid billing type input: {e2}")

        except Exception as outer:
            print(f" Outer test failure: {outer}")
        
        # Andriod Stack
        try:
            andriod_stack=WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.Andriod_stack_element))
            )
            andriod_stack.clear()
            time.sleep(2)
            andriod_stack.send_keys("https://api.paystack.co/transaction/initialize.")
            time.sleep(2)
        except Exception as e:
            print(" Failed to enter Andriod Stack URL:", e)
        # Content
        try:
            live_description = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.content_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", live_description)
            time.sleep(2)
            live_description.click()
            time.sleep(3)
            actions.send_keys(
            "Artificial intelligence is a field of science concerned with building computers and machines that can reason, learn, and act in such a way that would normally require human intelligence or that involves data whose scale exceeds what humans can analyze."
             ).perform()
            time.sleep(3)
            print(" Entered Live Description")
        except Exception as e:
            print(f" Failed to enter Live Description: {e}")
        # Status Settings
        try:
            plan_status = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.plan_status_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", plan_status)
            if plan_status.is_displayed():
                plan_status.click()
                time.sleep(1)  # Wait for UI to register change
                    # Click again
                print(" Toggle button clicked.")
            else:
                
                print(" Toggle button is not available.")
            time.sleep(2)

        except Exception as e:
            print(f" Failed to interact with plan status toggle: {e}")  
        
        # Plan Trail
        try:

            toggle = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.plan_trail_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
            is_enabled = toggle.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                toggle.click()
                print(" toggle already enabled.")
            else:
                toggle.click()
                print(" toggle enabled.")
            try:
                
                Days=WebDriverWait(self.driver, 45).until(
                    EC.presence_of_element_located((By.XPATH, self.trail_days_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Days)
                Days.clear()
                time.sleep(2)
                Days.send_keys("7")
                time.sleep(2)
            except Exception as e:
                print(f" Failed to enter trail days: {e}")

        except Exception as e:
            print(f"Failed to interact with toggle control: {e}")
        time.sleep(2)

        try:

            toggle2 = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.plan_active_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2)
            is_enabled = toggle2.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                toggle2.click()
                print(" toggle already enabled.")
            else:
                print(" toggle enabled.")
            


        except Exception as e:
            print(f"Failed to interact with toggle control: {e}")
        time.sleep(2)


        
        try:
            # Step 1: Submit with invalid (empty) Plan Price
            try:
                price_field = WebDriverWait(self.driver, 45).until(
                    EC.presence_of_element_located((By.XPATH, self.price_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", price_field)
                price_field.clear()
                print("Cleared Plan Price for negative test.")

                submit_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.save_plan_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                submit_btn.click()
                print("Submitted with empty Plan Price.")

                time.sleep(2)
                
                allure.attach(self.driver.get_screenshot_as_png(), name="InvalidPlanPrice", attachment_type=AttachmentType.PNG)
                print("Screenshot taken for invalid Plan Price.")
            except Exception as e1:
                print("Error submitting with empty Plan Price:", e1)

            # Step 2: Enter valid price (no submit)
            try:
                # Step 1: Submit with empty Quality field
                try:
                    quality_input = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//input[contains(@id, 'react-select')]"))
                    )
                    print("Located Quality input field.")

                    submit_btn = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, self.save_plan_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                    submit_btn.click()
                    print("Submitted with empty Quality field.")

                    time.sleep(2)
                    
                    allure.attach(self.driver.get_screenshot_as_png(), name="EmptyQualityField", attachment_type=AttachmentType.PNG)
                    print("Screenshot taken for empty Quality field.")
                except Exception as e1:
                    print("Error submitting with empty Quality field:", e1)
            except Exception as e1:
                    print("Error submitting with empty Quality field:", e1)

                # Step 2: Enter valid quality values (no submit)
            try:
                    quality_input.click()
                    quality_options = ["720p", "360p", "480p", "240p"]
                    for option in quality_options:
                        quality_input.send_keys(option)
                        time.sleep(0.5)
                        quality_input.send_keys(Keys.RETURN)
                        time.sleep(0.5)
                    print("Entered valid quality values.")
            except Exception as e2:
                print("Error entering valid quality options:", e2)

        except Exception as e:
            print("Test failed in quality field:", e)
        

        try:
            ios_id=WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.ios_product_id_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ios_id)
            ios_id.clear()
            time.sleep(2)
            ios_id.send_keys("Qwerty!@#123")
            time.sleep(2)

            ios_price=WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.ios_product_price_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ios_price)
            ios_price.clear()
            time.sleep(2)
            ios_price.send_keys("1699")
            time.sleep(2)
        except Exception as e:
            print(f" Failed to enter iOS product ID or price: {e}")
        # Recurring
        try:

            recurring= WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.recurring_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", recurring)
            recurring.click()
            time.sleep(6)
        except Exception as e:
            print(f" Failed to interact with recurring toggle: {e}")

        try:
         

            laptop = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.laptop_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", laptop)
            if laptop.is_displayed():
                laptop.click()
                time.sleep(1)  # Wait for UI to register change# Click again
                print(" Toggle button clicked.")
            else:
                laptop.click()
                print(" Toggle button is not available.")
            time.sleep(1)

            count1= WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.laptop_input_element))
            )
            count1.clear()
            time.sleep(2)
            count1.send_keys("4")
            time.sleep(2)
        except Exception as e:
            print(f" Failed to interact with laptop toggle: {e}")

        try:
            # Mobile
            mobile = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.mobile_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mobile)
            if mobile.is_displayed():
                mobile.click()
                time.sleep(1)  # Wait for UI to register change
                    # Click again
                print(" Toggle button clicked.")
            else:
                mobile.click()
                print(" Toggle button is not available.")
            time.sleep(1)

            count2= WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.mobile_input_elemet))
            )
            count2.clear()
            time.sleep(2)
            count2.send_keys("4")
            time.sleep(2)
        except Exception as e:
            print(f" Failed to interact with mobile toggle: {e}")
        
        try:
            TV = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.TV_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", TV)
            if TV.is_displayed():
                TV.click()
                time.sleep(1)  # Wait for UI to register change
                # Click again
                print(" Toggle button clicked.")
            else:
                TV.click()
                print(" Toggle button is not available.")
            time.sleep(1)

            count3= WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.TV_input_element))
            )
            count3.clear()
            time.sleep(2)
            count3.send_keys("4")
            time.sleep(2)
        except Exception as e:
            print(f" Failed to interact with TV toggle: {e}")

        try:
            create = WebDriverWait(self.driver, 45).until(
                EC.visibility_of_element_located((By.XPATH, self.save_plan_element))
            )
            # Scroll using JavaScript to the element
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", create)
            time.sleep(2)  # Wait for the scroll to complete
            # Ensure it's clickable
            create = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.save_plan_element))
            )
            create.click()
            print(" Create Plan button clicked successfully.")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Create Plan was successfully", attachment_type=AttachmentType.PNG)
            time.sleep(4)
            pytest.fail("Plan created successfully, but this test is expected to fail for demonstration purposes.")
        except Exception as e:
            print(f" Failed to click Create Plan button: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Create Plan Error", attachment_type=AttachmentType.PNG)
            pytest.fail(f"Failed to create plan: {e}")  



        

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")
        