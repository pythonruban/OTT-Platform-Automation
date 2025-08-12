import pytest
import allure
import time
import sys, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from allure_commons.types import AttachmentType

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig

xpaths = {
    "email_input": "(//input[@name='email'])[2]",
    "password_input": "//input[@name='password']",
    "login_button": "//span[text()='Login']",
    "dashboard_check": "//span[normalize-space()='Dashboard']",
    "settings": "//span[text()='Settings']",
    "email_settings": "//span[text()='Email Settings']",
    "edit_dropdown_btn": "(//span[@class='editdropdown-button'])[1]",
    "input_field_1": "(//input[@name='template_type'])[1]",
    "input_field_2": "(//input[@type='text'])[3]",
    "paragraph_3": "//div[@class='jodit-wysiwyg']",
    "submit_btn": "//button[@id='adminButton']",
    
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Admin - Email Template")
@allure.title("Edit first email template and update")
class TestEditTemplate:

    def click(self, by, locator, label, scroll=True):
        try:
            wait = WebDriverWait(self.driver, 20)
            elem = wait.until(EC.presence_of_element_located((by, locator)))
            if scroll:
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", elem)
                time.sleep(1)
            wait.until(EC.element_to_be_clickable((by, locator)))
            elem.click()
            print(f"✅ Clicked: {label}")
            allure.attach(self.driver.get_screenshot_as_png(), name=label, attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Failed to click {label}: {e}")

    def enter_text(self, by, locator, value, label):
        try:
            wait = WebDriverWait(self.driver, 20)
            elem = wait.until(EC.presence_of_element_located((by, locator)))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", elem)
            elem.clear()
            elem.send_keys(value)
            print(f"✅ Entered: {label} → {value}")
            allure.attach(self.driver.get_screenshot_as_png(), name=label, attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Failed to enter {label}: {e}")

    def test_edit_one_template(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()

        try:
            # Login
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email_input"]))).send_keys(ReadConfig.getAdminId())
            self.driver.find_element(By.XPATH, xpaths["password_input"]).send_keys(ReadConfig.getPassword())
            self.driver.find_element(By.XPATH, xpaths["login_button"]).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["dashboard_check"])))

            # Navigate
            self.click(By.XPATH, xpaths["settings"], "Settings")
            self.click(By.XPATH, xpaths["email_settings"], "Email Settings")
            self.click(By.XPATH, xpaths["edit_dropdown_btn"], "Edit Dropdown")

            # Fill inputs
            self.enter_text(By.XPATH, xpaths["input_field_1"], "Welcome_vod", "Template Type")
            self.enter_text(By.XPATH, xpaths["input_field_2"], "Welcome vod", "Title")

            # Enter content in Jodit using WebElement + JS
            editor_elem = self.driver.find_element(By.XPATH, xpaths["paragraph_3"])
            self.driver.execute_script("""
                arguments[0].innerHTML = arguments[1];
                arguments[0].dispatchEvent(new Event('input'));
            """, editor_elem, "welcome vod team!")
            print("✅ JS Entered: Paragraph")
            allure.attach(self.driver.get_screenshot_as_png(), name="Paragraph", attachment_type=AttachmentType.PNG)

            # Submit
            self.click(By.XPATH, xpaths["submit_btn"], "Submit")

            

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Failure", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {e}")
